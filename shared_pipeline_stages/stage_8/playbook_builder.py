from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any
import hashlib
import json
import logging
import os
import time

if TYPE_CHECKING:
    from providers.embeddings import EmbeddingProvider
    from providers.storage import StorageProvider

logger = logging.getLogger(__name__)

from shared_pipeline_stages.stage_6_5.embedder import MockRunbookEmbedder, RunbookEmbedder
from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json
from shared_pipeline_stages.runbook_tags import infer_runbook_tags
from shared_pipeline_stages.brain_ontology_bridge import (
    brain_contracts_for_capabilities,
    brain_snippets_for_stage5_playbook,
)
from shared_pipeline_stages.stage_7.artifact_loader import load_artifact_index_from_pool
from shared_pipeline_stages.stage_7.merge_packet_builder import load_runbooks_by_procedure_id
from shared_pipeline_stages.stage_7.pass_through import promote_pass_through_runbook
from shared_pipeline_stages.stage_8.comparison_report import build_comparison_report, build_variant_report
from shared_pipeline_stages.stage_8.action_synthesis import (
    ACTION_PLAN_FIELDS,
    synthesize_diagnostic_action_plan,
    synthesize_node_type_output,
)
from shared_pipeline_stages.stage_8.linking_runner import PlaybookLinkClient
from shared_pipeline_stages.stage_8.linked_runbook_surface import attach_linked_runbooks
from shared_pipeline_stages.stage_8.normalize import (
    MAX_RUNBOOKS_PER_NODE,
    MIN_RETRIEVAL_FLOOR,
    _mark_terminal_outcomes,
    _annotate_link_roles,
    attach_catalog_gaps,
    build_branches_from_hints,
    build_decision_outcomes,
    build_retrieval_decision_telemetry,
    build_retrieval_eligibility_trace,
    enforce_procedure_limits,
    ensure_backend_evidence_pairing,
    enrich_node_structure,
    needs_graph_repair,
    evaluate_link_confidence,
    reconcile_llm_runbook_links,
    repair_playbook_graph_cycles,
    sanitize_playbook_branch_graph,
    select_runbook_matches,
    stage5_node_preservation_warnings,
    validate_finalized_playbook,
    StructuralValidationError,
    validate_workflow_graph,
)
from shared_pipeline_stages.stage_8.playbook_retrieval import (
    build_playbook_retrieval_card,
    build_playbook_retrieval_index,
    extraction_mode_for_variant,
    playbook_id_from_candidate,
)
from shared_pipeline_stages.stage_8.support_language import enrich_support_user_language_examples
from shared_pipeline_stages.stage_8.review_markdown import (
    safe_playbook_review_filename,
    write_playbook_review_files,
)
from shared_pipeline_stages.stage_8.runbook_search import RunbookCatalogSearch, build_node_query_text
from shared_pipeline_stages.stage_8.schemas import (
    PlaybookRunbookLinkRow,
    Stage8BuildResult,
    VariantFinalizationReport,
)

STAGE8_DIR_NAME = "stage_8_finalized_playbooks"
PILOT_CASE_IDS = ["228086", "228723"]
LEXICAL_RETRIEVAL_TOP_K = 150
PROMPT_VARIANTS = {
    "prompt_a_one_per_incident": "playbook_prompt_a_one_per_incident",
    "prompt_b_multi_flow": "playbook_prompt_b_multi_flow",
}


class Stage8BuildConfig:
    def __init__(
        self,
        *,
        case_ids: list[str] | None = None,
        top_k: int = 10,
        llm_used: bool = False,
        min_retrieval_floor: float = MIN_RETRIEVAL_FLOOR,
        incident_preference_margin: float = 0.02,
        max_runbooks_per_node: int = MAX_RUNBOOKS_PER_NODE,
        use_mock_embedder: bool = False,
        deterministic_action_fallback: bool = False,
        allow_lexical_fallback: bool = False,
    ) -> None:
        self.case_ids = case_ids or list(PILOT_CASE_IDS)
        self.top_k = top_k
        self.llm_used = llm_used
        self.min_retrieval_floor = min_retrieval_floor
        self.incident_preference_margin = incident_preference_margin
        self.max_runbooks_per_node = max_runbooks_per_node
        self.use_mock_embedder = use_mock_embedder
        self.deterministic_action_fallback = deterministic_action_fallback
        # Semantic (embedding-based) retrieval is the expected mode for real
        # playbook generation. If Azure OpenAI credentials are unavailable,
        # _resolve_embedder raises rather than silently degrading to
        # lexical-only scoring, unless the caller explicitly opts in here
        # (e.g. for offline/CI runs that intentionally accept jaccard-only
        # matching).
        self.allow_lexical_fallback = allow_lexical_fallback


def build_stage8_finalized_playbooks(
    pool_dir: str | Path,
    stage7_dir: str | Path,
    incidents_root: str | Path,
    output_dir: str | Path,
    *,
    config: Stage8BuildConfig | None = None,
    llm_client: PlaybookLinkClient | None = None,
    embedder: RunbookEmbedder | None = None,
    generated_at: str | None = None,
    brain_storage: StorageProvider | None = None,
    brain_embeddings: EmbeddingProvider | None = None,
) -> Stage8BuildResult:
    build_config = config or Stage8BuildConfig()
    if build_config.llm_used and llm_client is None:
        raise ValueError(
            "Shared Stage 8 requires an LLM client when llm_used=True. "
            "Deterministic playbook finalization is not supported."
        )
    generated = generated_at or datetime.now(UTC).isoformat().replace("+00:00", "Z")
    output_path = _resolve_output_path(Path(output_dir))

    # Ontology grounding now comes from Brain (brain_ontology_bridge.py)
    # instead of the static docs/ontology/catalogs/*.json files -- there is
    # no fallback to the static catalog path (2026-09-09, user-directed).
    # Defaults mirror mcp_server/providers_config.py's factory pattern so a
    # caller that already has these providers (e.g. a future orchestrator
    # holding one long-lived instance per run) can pass them in instead of
    # each Stage 8 run constructing its own.
    active_brain_storage = brain_storage or _default_brain_storage_provider()
    active_brain_embeddings = brain_embeddings or _default_brain_embedding_provider()

    runbooks = _load_runbooks_for_linking(stage7_dir, pool_dir)
    runbooks_by_id = {
        str(item.get("procedure_id") or ""): item for item in runbooks if str(item.get("procedure_id") or "").strip()
    }
    retrieval_cards = read_json(Path(pool_dir) / "retrieval_cards.json")
    retrieval_index = read_json(Path(pool_dir) / "runbook_retrieval_index.json")
    # The Stage 6.5 pool is built from raw per-source runbooks and runs before
    # Stage 7, so it always contains every pre-merge candidate ID -- including
    # ones Stage 7's LLM merge step later folds into a new canonical ID and
    # removes from canonical_runbooks.json. Without this filter, retrieval can
    # surface and link a pre-merge ID that runbooks_by_id (Stage 7-canonical)
    # no longer recognizes, producing a dangling procedure_id that fails Stage
    # 9 validation. Drop any pool entry whose ID is not in the canonical set.
    retrieval_cards = [
        card for card in retrieval_cards if str(card.get("finalized_runbook_id") or "") in runbooks_by_id
    ]
    retrieval_index = [
        entry for entry in retrieval_index if str(entry.get("finalized_runbook_id") or "") in runbooks_by_id
    ]
    _write_runbook_pool_diagnostic(
        output_path,
        pool_dir=Path(pool_dir),
        runbooks=runbooks,
        retrieval_index=retrieval_index,
        generated_at=generated,
    )
    catalog = RunbookCatalogSearch.from_pool_artifacts(
        retrieval_cards,
        retrieval_index,
        runbooks,
        incident_preference_margin=build_config.incident_preference_margin,
    )
    active_embedder = embedder or _resolve_embedder(build_config)
    artifact_index = load_artifact_index_from_pool(pool_dir)

    variant_reports: list[VariantFinalizationReport] = []
    total_playbooks = 0
    all_merged_case_ids: set[str] = set()

    for variant_key, variant_subdir in PROMPT_VARIANTS.items():
        variant_dir = output_path / variant_key
        variant_dir.mkdir(parents=True, exist_ok=True)
        review_dir = variant_dir / "review_markdown" / "playbooks"
        review_dir.mkdir(parents=True, exist_ok=True)
        existing_playbooks = _read_existing_records(variant_dir / "canonical_playbooks.json", "playbooks")
        stale_playbook_ids = {
            str(item.get("playbook_id") or "")
            for item in existing_playbooks
            if str(item.get("case_id") or "") in build_config.case_ids
        }
        for stale_id in stale_playbook_ids:
            stale_md = review_dir / safe_playbook_review_filename(stale_id)
            stale_html = stale_md.with_suffix(".html")
            for stale_review in (stale_md, stale_html):
                if stale_review.exists():
                    stale_review.unlink()

        finalized_playbooks: list[dict[str, Any]] = []
        link_rows: list[dict[str, Any]] = []
        retrieval_cards_out: list[dict[str, Any]] = []
        retrieval_telemetry_records: list[dict[str, Any]] = []
        warnings: list[str] = []
        extraction_mode = extraction_mode_for_variant(variant_key)

        for case_id in build_config.case_ids:
            candidates = _load_playbook_candidates(incidents_root, case_id, variant_subdir)
            for candidate in candidates:
                playbook_id = playbook_id_from_candidate(candidate, case_id)
                print(
                    f"Stage 8 finalizing {variant_key} case={case_id} playbook={playbook_id}",
                    flush=True,
                )
                candidate["support_user_language_examples"] = enrich_support_user_language_examples(
                    candidate.get("support_user_language_examples"),
                    case_id=case_id,
                    title=str(candidate.get("title") or ""),
                    observed_entry_symptoms=list(candidate.get("observed_entry_symptoms") or []),
                )
                card = build_playbook_retrieval_card(candidate, case_id=case_id, extraction_mode=extraction_mode)
                retrieval_cards_out.append(card.model_dump())
                playbook = _finalize_playbook_candidate(
                    candidate,
                    case_id=case_id,
                    extraction_mode=extraction_mode,
                    catalog=catalog,
                    runbooks_by_id=runbooks_by_id,
                    embedder=active_embedder,
                    build_config=build_config,
                    llm_client=llm_client,
                    brain_storage=active_brain_storage,
                    brain_embeddings=active_brain_embeddings,
                )
                playbook_warnings = validate_finalized_playbook(
                    playbook,
                    runbooks_by_id=runbooks_by_id,
                    max_runbooks_per_node=build_config.max_runbooks_per_node,
                )
                playbook_warnings.extend(
                    stage5_node_preservation_warnings(
                        [node for node in candidate.get("nodes") or [] if isinstance(node, dict)],
                        [node for node in playbook.get("nodes") or [] if isinstance(node, dict)],
                    )
                )
                repaired_edges = repair_playbook_graph_cycles(playbook)
                if repaired_edges:
                    playbook_warnings.append(
                        "Repaired workflow cycle edges: " + ", ".join(repaired_edges)
                    )
                graph_errors = validate_workflow_graph(playbook)
                if graph_errors:
                    if build_config.llm_used:
                        raise StructuralValidationError(
                            str(playbook.get("playbook_id") or playbook_id),
                            graph_errors,
                        )
                    warnings.extend(
                        f"{playbook.get('playbook_id') or playbook_id}: structural validation: {error}"
                        for error in graph_errors
                    )
                warnings.extend(playbook_warnings)
                playbook["needs_graph_repair"] = needs_graph_repair(playbook)
                retrieval_telemetry_records.extend(
                    {"playbook_id": playbook.get("playbook_id"), **record}
                    for record in playbook.pop("_retrieval_decision_telemetry", []) or []
                )
                finalized_playbooks.append(playbook)
                link_rows.extend(_flatten_link_rows(playbook))
                write_playbook_review_files(
                    playbook,
                    runbooks_by_id=runbooks_by_id,
                    review_dir=review_dir,
                    artifact_index=artifact_index,
                )

        cards_for_index = [
            build_playbook_retrieval_card(
                {
                    "playbook_candidate_id": playbook.get("playbook_candidate_id"),
                    "title": playbook.get("title"),
                    "user_facing_summary": playbook.get("user_facing_summary"),
                    "observed_entry_symptoms": playbook.get("observed_entry_symptoms"),
                    "support_user_language_examples": [],
                    "affected_systems_or_components": playbook.get("affected_systems_or_components"),
                    "nodes": playbook.get("nodes"),
                },
                case_id=str(playbook.get("case_id") or ""),
                extraction_mode=extraction_mode,
            )
            for playbook in finalized_playbooks
        ]
        index_entries, embedding_model = (
            build_playbook_retrieval_index(cards_for_index, embedder=active_embedder)
            if cards_for_index
            else ([], active_embedder.model_name)
        )

        # Stage 8 can be scoped to a subset of case_ids (routine single-case
        # ingestion). Case-scoped output files must merge with whatever this
        # variant already had on disk for OTHER cases rather than overwrite
        # it, or a scoped run would silently delete every other case's
        # finalized playbooks. Replace only the entries belonging to
        # build_config.case_ids; everything else on disk is carried forward.
        merged_playbooks = _merge_case_scoped(
            existing_playbooks, finalized_playbooks, case_ids=build_config.case_ids, key="case_id"
        )
        merged_links = _merge_case_scoped(
            _read_existing_records(variant_dir / "playbook_runbook_links.json", "links"),
            link_rows,
            case_ids=build_config.case_ids,
            key="case_id",
        )
        merged_cards = _merge_case_scoped(
            _read_existing_records(variant_dir / "playbook_retrieval_cards.json", "cards"),
            retrieval_cards_out,
            case_ids=build_config.case_ids,
            key="case_id",
        )
        existing_telemetry = _read_existing_records(variant_dir / "retrieval_decision_telemetry.json", "records")
        merged_telemetry = [
            record for record in existing_telemetry if str(record.get("playbook_id") or "") not in stale_playbook_ids
        ] + retrieval_telemetry_records
        existing_index = _read_existing_records(variant_dir / "playbook_retrieval_index.json", "entries")
        merged_index = [
            entry for entry in existing_index if str(entry.get("playbook_id") or "") not in stale_playbook_ids
        ] + [entry.model_dump() for entry in index_entries]
        merged_case_ids = sorted({str(item.get("case_id") or "") for item in merged_playbooks if item.get("case_id")})

        variant_report = build_variant_report(
            merged_playbooks,
            extraction_mode=extraction_mode,
            case_ids=merged_case_ids,
            warnings=warnings,
        )
        variant_reports.append(variant_report)

        write_json(variant_dir / "canonical_playbooks.json", {"playbooks": merged_playbooks, "generated_at": generated})
        write_json(
            variant_dir / "retrieval_decision_telemetry.json",
            {"records": merged_telemetry, "generated_at": generated},
        )
        write_json(variant_dir / "playbook_runbook_links.json", {"links": merged_links, "generated_at": generated})
        write_json(variant_dir / "playbook_retrieval_cards.json", {"cards": merged_cards, "generated_at": generated})
        write_json(
            variant_dir / "playbook_retrieval_index.json",
            {
                "embedding_model": embedding_model,
                "entries": merged_index,
                "generated_at": generated,
            },
        )
        write_json(
            variant_dir / "playbook_finalization_report.json",
            {
                **variant_report.model_dump(),
                "generated_at": generated,
                "llm_used": build_config.llm_used,
                "retrieval_mode": retrieval_mode_for_embedder(active_embedder),
                "embedding_model": active_embedder.model_name,
                "warnings": warnings,
            },
        )
        total_playbooks += len(finalized_playbooks)
        all_merged_case_ids.update(merged_case_ids)

    comparison = build_comparison_report(
        variant_reports, case_ids=sorted(all_merged_case_ids), generated_at=generated
    )
    write_json(output_path / "stage_8_comparison_report.json", comparison)

    return Stage8BuildResult(
        generated_at=generated,
        llm_used=build_config.llm_used,
        case_ids=build_config.case_ids,
        playbook_count=total_playbooks,
        variant_reports=variant_reports,
        retrieval_mode=retrieval_mode_for_embedder(active_embedder),
        embedding_model=active_embedder.model_name,
    )


def refresh_stage8_playbook_reviews(
    stage8_dir: str | Path,
    *,
    pool_dir: str | Path,
    stage7_dir: str | Path,
    repo_root: Path | None = None,
) -> int:
    stage8_path = _resolve_output_path(Path(stage8_dir))
    root = repo_root or Path(__file__).resolve().parents[2]
    artifact_index = load_artifact_index_from_pool(pool_dir)
    runbooks_by_id = {
        str(item.get("procedure_id") or ""): item
        for item in _load_canonical_runbooks(stage7_dir)
        if str(item.get("procedure_id") or "").strip()
    }
    refreshed = 0
    for variant_key in PROMPT_VARIANTS:
        variant_dir = stage8_path / variant_key
        payload = read_json(variant_dir / "canonical_playbooks.json")
        review_dir = variant_dir / "review_markdown" / "playbooks"
        review_dir.mkdir(parents=True, exist_ok=True)
        for stale_review in (*review_dir.glob("*.md"), *review_dir.glob("*.html")):
            stale_review.unlink()
        playbooks = []
        for playbook in payload.get("playbooks") or []:
            if not isinstance(playbook, dict):
                continue
            for node in playbook.get("nodes") or []:
                if isinstance(node, dict):
                    node.update(
                        enrich_node_structure(
                            node,
                            decision_outcomes=list(node.get("decision_outcomes") or []),
                            branches=list(node.get("branches") or []),
                        )
                    )
                    node["runbook_links"] = enforce_procedure_limits(
                        node,
                        list(node.get("runbook_links") or []),
                        runbooks_by_id=runbooks_by_id,
                    )
                    node["resolved_runbook_ids"] = [
                        str(link.get("procedure_id") or "")
                        for link in node["runbook_links"]
                        if str(link.get("procedure_id") or "")
                    ]
                    attach_linked_runbooks(node, runbooks_by_id=runbooks_by_id)
                    attach_catalog_gaps(node)
            sanitize_playbook_branch_graph(playbook)
            playbooks.append(playbook)
            write_playbook_review_files(
                playbook,
                runbooks_by_id=runbooks_by_id,
                review_dir=review_dir,
                artifact_index=artifact_index,
                repo_root=root,
            )
            refreshed += 1
        if playbooks:
            payload["playbooks"] = playbooks
            write_json(variant_dir / "canonical_playbooks.json", payload)
    return refreshed


def _finalize_playbook_candidate(
    candidate: dict[str, Any],
    *,
    case_id: str,
    extraction_mode: str,
    catalog: RunbookCatalogSearch,
    runbooks_by_id: dict[str, dict[str, Any]],
    embedder: RunbookEmbedder,
    build_config: Stage8BuildConfig,
    llm_client: PlaybookLinkClient | None,
    brain_storage: StorageProvider,
    brain_embeddings: EmbeddingProvider,
) -> dict[str, Any]:
    playbook_id = playbook_id_from_candidate(candidate, case_id)
    branch_hints = [hint for hint in candidate.get("branch_hints") or [] if isinstance(hint, dict)]
    playbook_context = {
        "observed_entry_symptoms": candidate.get("observed_entry_symptoms") or [],
        "support_user_language_examples": candidate.get("support_user_language_examples") or [],
    }
    node_candidates: dict[str, list[dict[str, Any]]] = {}
    node_vectors: dict[str, list[float]] = {}
    node_retrieval_traces: dict[str, list[dict[str, Any]]] = {}
    node_retrieval_telemetry: dict[str, dict[str, Any]] = {}
    ontology_by_node: dict[str, list[dict[str, Any]]] = {}

    affected_systems = [str(item) for item in candidate.get("affected_systems_or_components") or [] if str(item).strip()]
    retrieval_top_k, retrieval_min_score = _retrieval_search_params(embedder, build_config)

    for node in candidate.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        existing_contracts = {
            str(item.get("id") or item.get("capability") or ""): item
            for item in node.get("ontology_capabilities") or []
            if isinstance(item, dict)
        }
        for contract in brain_contracts_for_capabilities(set(existing_contracts), storage=brain_storage):
            existing = existing_contracts.get(contract["id"], {})
            existing.update({key: value for key, value in contract.items() if value})
            existing_contracts[contract["id"]] = existing
        if existing_contracts:
            node["ontology_capabilities"] = list(existing_contracts.values())
            node["backend_observability"] = [
                mapping
                for contract in existing_contracts.values()
                for mapping in contract.get("backend_mappings") or []
                if isinstance(mapping, dict)
            ]
        node_id = str(node.get("node_id") or "")
        query_text = build_node_query_text(node, affected_systems=affected_systems)
        query_vector = embedder.embed_texts([query_text])[0] if query_text else []
        node_vectors[node_id] = query_vector
        matches = catalog.search_for_node(
            node,
            query_vector=query_vector,
            top_k=retrieval_top_k,
            min_score=retrieval_min_score,
            case_id=case_id,
            affected_systems=affected_systems,
        )
        node_candidates[node_id] = [match.model_dump() for match in matches]
        node_retrieval_traces[node_id] = build_retrieval_eligibility_trace(
            node,
            matches,
            runbooks_by_id=runbooks_by_id,
        )

    for node in candidate.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("node_id") or "")
        ontology_by_node[node_id] = brain_snippets_for_stage5_playbook(
            " ".join(
                str(node.get(key) or "")
                for key in (
                    "title",
                    "intent",
                    "goal",
                    "runbook_placeholder",
                    "expected_or_observed_result",
                    "evidence_required",
                    "healthy_indicators",
                    "unhealthy_indicators",
                    "inconclusive_indicators",
                )
            ),
            embeddings=brain_embeddings,
            storage=brain_storage,
        )

    llm_payload = {
        "case_id": case_id,
        "playbook_candidate": candidate,
        "branch_hints": branch_hints,
        "node_runbook_candidates": node_candidates,
        "ontology_snippets": ontology_by_node,
        "linking_policy": {
            "max_runbooks_per_node": build_config.max_runbooks_per_node,
            "min_retrieval_floor": build_config.min_retrieval_floor,
            "prefer_incident_derived_runbooks_for_procedure_reference_only": True,
            "incident_preference_margin": build_config.incident_preference_margin,
            "allow_low_confidence_partial_match": True,
            "use_normalized_node_queries": True,
            "boost_by_procedure_type": True,
            "prefer_manual_over_training_video": True,
            "use_capability_tag_constraints": False,
            "use_expects_as_surface_hint_only": True,
            "use_ontology_snippets_for_intent": True,
            "outcome_evidence_priority": True,
            "prefer_case_local_runbook_for_procedure_reference": True,
            "candidate_source_balance": "retain manual, training_video_day1, training_video_day2, and incident candidates",
        },
    }
    llm_response = llm_client.link(llm_payload) if llm_client and build_config.llm_used else {}
    if llm_client and build_config.llm_used:
        pause_seconds = float(os.getenv("STAGE8_LLM_PAUSE_SECONDS") or "3")
        if pause_seconds > 0:
            time.sleep(pause_seconds)

    finalized_nodes: list[dict[str, Any]] = []
    playbook_branches: list[dict[str, Any]] = []
    candidate_nodes = [node for node in candidate.get("nodes") or [] if isinstance(node, dict)]
    for node in candidate_nodes:
        node_id = str(node.get("node_id") or "")
        llm_node = _find_llm_node(llm_response, node_id)
        matches = catalog.search_for_node(
            node,
            query_vector=node_vectors.get(node_id),
            top_k=retrieval_top_k,
            min_score=retrieval_min_score,
            case_id=case_id,
            affected_systems=affected_systems,
        )
        candidate_scores = {match.procedure_id: match.combined_score for match in matches}
        if llm_node:
            finalized_node = _merge_llm_node(
                node,
                llm_node,
                runbooks_by_id=runbooks_by_id,
                retrieval_matches=matches,
            )
            node_retrieval_telemetry[node_id] = build_retrieval_decision_telemetry(
                node, matches, runbooks_by_id=runbooks_by_id
            )
        else:
            selected = select_runbook_matches(
                node,
                matches,
                runbooks_by_id=runbooks_by_id,
                max_runbooks=build_config.max_runbooks_per_node,
            )
            finalized_node = _build_node_from_matches(node, selected)
            node_retrieval_telemetry[node_id] = build_retrieval_decision_telemetry(
                node, matches, runbooks_by_id=runbooks_by_id, selected=selected
            )
        finalized_node["runbook_links"] = enforce_procedure_limits(
            finalized_node,
            list(finalized_node.get("runbook_links") or []),
            runbooks_by_id=runbooks_by_id,
        )
        finalized_node["retrieval_eligibility_trace"] = node_retrieval_traces.get(node_id, [])
        finalized_node["resolved_runbook_ids"] = [
            str(link.get("procedure_id") or "")
            for link in finalized_node["runbook_links"]
            if str(link.get("procedure_id") or "")
        ]
        linked_ids = [str(item) for item in finalized_node.get("resolved_runbook_ids") or []]
        finalized_node["decision_outcomes"] = _mark_terminal_outcomes(
            llm_node.get("decision_outcomes") or []
            if llm_node
            else build_decision_outcomes(
                node,
                runbooks_by_id,
                linked_runbook_ids=linked_ids,
                branch_hints=branch_hints,
                playbook_context=playbook_context,
                all_nodes=candidate_nodes,
            )
        )
        node_type = str(node.get("node_type") or "")
        llm_branches = llm_node.get("branches") if llm_node else None
        finalized_node["branches"] = build_branches_from_hints(
            node,
            branch_hints,
            llm_branches=llm_branches,
            all_nodes=candidate_nodes,
        )
        finalized_node = enrich_node_structure(
            finalized_node,
            decision_outcomes=finalized_node["decision_outcomes"],
            branches=finalized_node["branches"],
        )
        if node_type == "branching_condition" and finalized_node["branches"]:
            playbook_branches.extend(
                {**branch, "from_node_id": node_id}
                for branch in finalized_node["branches"]
                if isinstance(branch, dict)
            )
        finalized_node["inherited_image_refs"] = _collect_inherited_image_refs(finalized_node, runbooks_by_id)
        finalized_node["image_refs"] = list(finalized_node["inherited_image_refs"])
        attach_linked_runbooks(finalized_node, runbooks_by_id=runbooks_by_id)
        attach_catalog_gaps(finalized_node)
        node_type_output = synthesize_node_type_output(
            finalized_node,
            links=finalized_node.get("runbook_links") or [],
            runbooks_by_id=runbooks_by_id,
        )
        for field, value in node_type_output.items():
            if field not in finalized_node or finalized_node.get(field) in (None, "", []):
                finalized_node[field] = value
        if node_type in {"diagnostic_decision", "branching_condition", "validation_gate"}:
            quality_plan = synthesize_diagnostic_action_plan(
                finalized_node,
                ontology_evidence=ontology_by_node.get(node_id, []),
                links=finalized_node.get("runbook_links") or [],
                runbooks_by_id=runbooks_by_id,
            )
            for field in (
                "diagnostic_classification",
                "question",
                "optional_corroboration_surface",
                "technical_field_mapping",
                "runbook_execution_result",
                "node_interpretation_mapping",
                "ontology_evidence",
            ):
                if quality_plan.get(field) not in (None, "", []):
                    finalized_node[field] = quality_plan[field]
            if isinstance(finalized_node.get("evidence_to_collect"), list):
                finalized_node["evidence_to_collect"] = list(finalized_node["evidence_to_collect"])[:8]
        if not build_config.llm_used and build_config.deterministic_action_fallback:
            finalized_node.update(
                synthesize_diagnostic_action_plan(
                    finalized_node,
                    ontology_evidence=ontology_by_node.get(node_id, []),
                    links=finalized_node.get("runbook_links") or [],
                    runbooks_by_id=runbooks_by_id,
                )
            )
        # Action synthesis can finalize the node's support surface after the
        # initial link pass. Reapply the same contract once so a procedure that
        # only matched the pre-enrichment query cannot survive on a wrong
        # surface (for example, a WCS SQL check on an Event Viewer node).
        finalized_node["runbook_links"] = enforce_procedure_limits(
            finalized_node,
            list(finalized_node.get("runbook_links") or []),
            runbooks_by_id=runbooks_by_id,
        )
        # Guaranteed backend-vs-UI completion pass (docs/design_decisions/
        # stage_8_playbook_finalization.md): for nodes in scope, ensure a
        # WCS/SSMS backend link is present alongside at most one RMS/UI link.
        finalized_node["runbook_links"] = ensure_backend_evidence_pairing(
            finalized_node,
            list(finalized_node.get("runbook_links") or []),
            runbooks_by_id=runbooks_by_id,
            candidates=matches,
        )
        finalized_node["resolved_runbook_ids"] = [
            str(link.get("procedure_id") or "")
            for link in finalized_node["runbook_links"]
            if str(link.get("procedure_id") or "")
        ]
        attach_linked_runbooks(finalized_node, runbooks_by_id=runbooks_by_id)
        finalized_nodes.append(finalized_node)

    if llm_response.get("branches"):
        playbook_branches.extend(
            branch for branch in llm_response.get("branches") or [] if isinstance(branch, dict)
        )

    playbook = {
        "playbook_id": playbook_id,
        "playbook_candidate_id": candidate.get("playbook_candidate_id"),
        "case_id": case_id,
        "extraction_mode": extraction_mode,
        "title": candidate.get("title"),
        "user_facing_summary": candidate.get("user_facing_summary"),
        "playbook_goal": candidate.get("playbook_goal"),
        "observed_entry_symptoms": candidate.get("observed_entry_symptoms") or [],
        "support_user_language_examples": enrich_support_user_language_examples(
            candidate.get("support_user_language_examples"),
            case_id=case_id,
            title=str(candidate.get("title") or ""),
            observed_entry_symptoms=list(candidate.get("observed_entry_symptoms") or []),
        ),
        "affected_systems_or_components": candidate.get("affected_systems_or_components") or [],
        "confidence": candidate.get("confidence"),
        "confidence_reason": candidate.get("confidence_reason"),
        "validation_status": "needs_sme_review",
        "nodes": finalized_nodes,
        "branches": playbook_branches,
        "branch_hints": branch_hints,
        "source_refs": candidate.get("source_refs") or [],
        "evidence_source_refs": candidate.get("evidence_source_refs") or [],
        # Internal-only debug telemetry (Section 10 of the retrieval fix plan).
        # Never rendered into the playbook; stripped before canonical_playbooks.json
        # is written and persisted separately as retrieval_decision_telemetry.json.
        "_retrieval_decision_telemetry": list(node_retrieval_telemetry.values()),
    }
    return sanitize_playbook_branch_graph(playbook)


def _build_node_from_matches(
    node: dict[str, Any],
    selected: list[tuple[Any, str, list[str], float]],
) -> dict[str, Any]:
    links: list[dict[str, Any]] = []
    resolved_ids: list[str] = []
    for rank, (match, confidence, gaps, boosted) in enumerate(selected, start=1):
        resolved_ids.append(match.procedure_id)
        links.append(
            {
                "procedure_id": match.procedure_id,
                "link_confidence": confidence,
                "link_rationale": f"Retrieval match ({match.combined_score:.4f}, boosted {boosted:.4f}) for placeholder.",
                "match_gaps": gaps,
                "preferred_incident_source": match.preferred_incident_source,
                "retrieval_combined_score": match.combined_score,
                "boosted_score": boosted,
                "link_rank": rank,
                "link_role": "primary" if rank == 1 else "alternate",
            }
        )
    merged = dict(node)
    merged["resolved_runbook_ids"] = resolved_ids
    merged["runbook_links"] = _annotate_link_roles(links)
    return merged


def _coerce_optional_corroboration(value: Any) -> list[dict[str, Any]]:
    """Normalize optional_corroboration to list[dict] despite prompt guidance.

    The LLM occasionally returns plain strings (e.g. ["If active errors are
    suspected, corroborate with SSMS/API evidence."]) instead of the required
    object shape, which fails FinalizedNode's pydantic validation and shows up
    as a playbook warning. Coerce rather than drop, since the content itself
    is still useful SME-review context.
    """
    if not isinstance(value, list):
        return []
    coerced: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, dict):
            coerced.append(item)
        elif isinstance(item, str) and item.strip():
            coerced.append({"note": item.strip()})
    return coerced


def _merge_llm_node(
    node: dict[str, Any],
    llm_node: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    retrieval_matches: list[Any] | None = None,
) -> dict[str, Any]:
    match_by_id = {match.procedure_id: match for match in retrieval_matches or []}
    merged = dict(node)
    nested_action_plan = llm_node.get("diagnostic_action_plan")
    if not isinstance(nested_action_plan, dict):
        nested_action_plan = {}
    for field in ACTION_PLAN_FIELDS:
        if field in llm_node:
            merged[field] = llm_node[field]
        elif field in nested_action_plan:
            merged[field] = nested_action_plan[field]
    if "optional_corroboration" in merged:
        merged["optional_corroboration"] = _coerce_optional_corroboration(merged["optional_corroboration"])
    links = []
    resolved_ids = []
    for rank, link in enumerate(llm_node.get("runbook_links") or [], start=1):
        if not isinstance(link, dict):
            continue
        procedure_id = str(link.get("procedure_id") or "")
        if procedure_id and procedure_id not in runbooks_by_id:
            continue
        if not procedure_id:
            continue
        match = match_by_id.get(procedure_id)
        if retrieval_matches and match is None:
            continue
        if match:
            confidence, boosted, gaps = evaluate_link_confidence(
                node,
                match,
                runbook=runbooks_by_id.get(procedure_id),
                llm_confidence=str(link.get("link_confidence") or ""),
                link_rank=rank,
            )
        else:
            confidence = str(link.get("link_confidence") or "medium")
            boosted = 0.0
            gaps = list(link.get("match_gaps") or [])
        resolved_ids.append(procedure_id)
        links.append(
            {
                "procedure_id": procedure_id,
                "link_confidence": confidence,
                "link_rationale": str(link.get("link_rationale") or ""),
                "match_gaps": gaps or list(link.get("match_gaps") or []),
                "preferred_incident_source": bool(link.get("preferred_incident_source")),
                "retrieval_combined_score": match.combined_score if match else None,
                "boosted_score": boosted,
                "link_rank": rank,
            }
        )
    if not links:
        selected = select_runbook_matches(
            node,
            list(retrieval_matches or []),
            runbooks_by_id=runbooks_by_id,
            max_runbooks=MAX_RUNBOOKS_PER_NODE,
        )
        linked_node = _build_node_from_matches(node, selected)
        for field in ACTION_PLAN_FIELDS:
            if field in merged:
                linked_node[field] = merged[field]
        return linked_node
    links = reconcile_llm_runbook_links(
        node,
        links,
        list(retrieval_matches or []),
        runbooks_by_id=runbooks_by_id,
    )
    if str(node.get("node_type") or "") == "procedure_reference":
        linked_ids = {str(item.get("procedure_id") or "") for item in links}
        local_matches = [
            match
            for match in retrieval_matches or []
            if match.preferred_incident_source and match.procedure_id not in linked_ids
        ]
        if local_matches:
            local = local_matches[0]
            links.append(
                {
                    "procedure_id": local.procedure_id,
                    "link_confidence": "medium",
                    "link_rationale": "Case-local procedure retained for a procedure-reference node.",
                    "match_gaps": [],
                    "preferred_incident_source": True,
                    "retrieval_combined_score": local.combined_score,
                    "boosted_score": local.combined_score,
                    "link_role": "case_local",
                }
            )
    resolved_ids = [str(link.get("procedure_id") or "") for link in links if str(link.get("procedure_id") or "")]
    merged["resolved_runbook_ids"] = resolved_ids[:MAX_RUNBOOKS_PER_NODE]
    merged["runbook_links"] = _annotate_link_roles(links[:MAX_RUNBOOKS_PER_NODE])
    return merged


def _find_llm_node(llm_response: dict[str, Any], node_id: str) -> dict[str, Any] | None:
    for node in llm_response.get("nodes") or []:
        if isinstance(node, dict) and str(node.get("node_id") or "") == node_id:
            return node
    return None


def _collect_inherited_image_refs(node: dict[str, Any], runbooks_by_id: dict[str, dict[str, Any]]) -> list[str]:
    refs: list[str] = []
    seen: set[str] = set()
    for procedure_id in node.get("resolved_runbook_ids") or []:
        runbook = runbooks_by_id.get(str(procedure_id), {})
        for key in ("visual_references", "screens_or_images"):
            for item in runbook.get(key) or []:
                if not isinstance(item, dict):
                    continue
                artifact_id = str(item.get("artifact_id") or "")
                if artifact_id and artifact_id not in seen:
                    seen.add(artifact_id)
                    refs.append(artifact_id)
        for step in runbook.get("steps") or []:
            if not isinstance(step, dict):
                continue
            for item in step.get("screens_or_images") or []:
                if not isinstance(item, dict):
                    continue
                artifact_id = str(item.get("artifact_id") or "")
                if artifact_id and artifact_id not in seen:
                    seen.add(artifact_id)
                    refs.append(artifact_id)
    return refs


def _flatten_link_rows(playbook: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        for link in node.get("runbook_links") or []:
            if not isinstance(link, dict):
                continue
            row = PlaybookRunbookLinkRow(
                case_id=str(playbook.get("case_id") or ""),
                playbook_id=str(playbook.get("playbook_id") or ""),
                node_id=str(node.get("node_id") or ""),
                procedure_id=str(link.get("procedure_id") or ""),
                link_confidence=str(link.get("link_confidence") or ""),
                link_rank=int(link.get("link_rank") or 1),
                extraction_mode=str(playbook.get("extraction_mode") or ""),
            )
            rows.append(row.model_dump())
    return rows


def _read_existing_records(path: Path, records_key: str) -> list[dict[str, Any]]:
    """Load a case-scoped Stage 8 output file's existing records so a scoped
    run can merge into them instead of overwriting other cases' data. Missing
    file (first run, or fresh output_dir) means no prior records -- that is
    the only case treated as empty; a present-but-corrupt file raises, since
    silently treating corruption as "no prior data" would delete every other
    case's already-finalized output on the next scoped Stage 8 run."""
    if not path.is_file():
        return []
    payload = read_json(path)
    records = payload.get(records_key) if isinstance(payload, dict) else None
    return [item for item in records or [] if isinstance(item, dict)]


def _merge_case_scoped(
    existing: list[dict[str, Any]],
    new_records: list[dict[str, Any]],
    *,
    case_ids: list[str],
    key: str,
) -> list[dict[str, Any]]:
    case_id_set = set(case_ids)
    carried_forward = [item for item in existing if str(item.get(key) or "") not in case_id_set]
    return carried_forward + new_records


def _load_canonical_runbooks(stage7_dir: str | Path) -> list[dict[str, Any]]:
    payload = read_json(Path(stage7_dir) / "canonical_runbooks.json")
    runbooks = payload.get("runbooks") if isinstance(payload, dict) else payload
    if not isinstance(runbooks, list):
        raise ValueError("canonical_runbooks.json must contain a runbooks list.")
    return [item for item in runbooks if isinstance(item, dict)]


def _load_merged_away_procedure_ids(stage7_dir: str | Path) -> set[str]:
    """Pool procedure IDs Stage 7 explicitly folded into a new canonical ID.

    Stage 6.5's pool is built from raw per-source runbooks before Stage 7 runs,
    so it always still contains every pre-merge ID. Without this exclusion,
    _load_runbooks_for_linking's pass-through fallback (for any pool ID not in
    canonical_runbooks.json) would silently re-add a procedure Stage 7 just
    deliberately merged away, letting Stage 8 link to an ID that no longer
    exists in the canonical catalog (dangling reference, fails Stage 9).
    """
    try:
        report = read_json(Path(stage7_dir) / "runbook_merge_report.json")
    except Exception:
        return set()
    if not isinstance(report, dict):
        return set()
    merged_away: set[str] = set()
    for result in report.get("cluster_results") or []:
        if not isinstance(result, dict) or result.get("merge_decision") != "merged":
            continue
        merged_away.update(
            str(pid).strip()
            for pid in result.get("merged_from_procedure_ids") or []
            if str(pid).strip()
        )
    return merged_away


def _hydrate_runbook_from_pool(
    runbook: dict[str, Any], *, source: dict[str, Any], metadata: dict[str, Any]
) -> dict[str, Any]:
    """Fills in access_surface/capability_tags/audience_roles/source_type/
    source_id/source_path/validation_status from the Stage 6.5 pool's
    source runbook + pool metadata, whenever `runbook` doesn't already
    have that field. Shared by both branches of _load_runbooks_for_linking
    -- a runbook that's ALREADY in canonical_runbooks.json, and a
    pool-only runbook that only exists via promote_pass_through_runbook()
    (which sets metadata/merged_from_procedure_ids/canonical_source_procedure_ids
    only, never these fields) -- so neither branch can silently skip
    hydration. A real test (test_active_error_sql_is_retained_as_composite_diagnostic_evidence)
    asserts source_id/source_type/access_surface/capability_tags directly
    on a pool-only runbook; before this fix that branch never populated
    them, a KeyError confirmed against 8 of 270 real pool runbooks."""
    hydrated = dict(runbook)
    for field in (
        "access_surface",
        "capability_tags",
        "audience_roles",
        "source_type",
        "source_id",
        "source_path",
        "validation_status",
    ):
        value = source.get(field) or metadata.get(field)
        if not hydrated.get(field) and value:
            hydrated[field] = list(value) if isinstance(value, list) else value
    if not hydrated.get("access_surface") or not hydrated.get("capability_tags"):
        infer_runbook_tags(hydrated)
    return hydrated


def _load_runbooks_for_linking(stage7_dir: str | Path, pool_dir: str | Path) -> list[dict[str, Any]]:
    runbooks = _load_canonical_runbooks(stage7_dir)
    by_id = {
        str(item.get("procedure_id") or ""): item
        for item in runbooks
        if isinstance(item, dict) and str(item.get("procedure_id") or "").strip()
    }
    merged_away = _load_merged_away_procedure_ids(stage7_dir)
    try:
        pool_runbooks = load_runbooks_by_procedure_id(pool_dir)
        pool_payload = read_json(Path(pool_dir) / "runbook_pool.json")
        pool_metadata = {
            str(item.get("finalized_runbook_id") or ""): item
            for item in (pool_payload.get("entries") or [])
            if isinstance(item, dict)
        }
    except Exception:
        pool_runbooks = {}
        pool_metadata = {}
    for procedure_id, source in pool_runbooks.items():
        if not procedure_id or not isinstance(source, dict):
            continue
        if procedure_id in merged_away:
            continue
        metadata = pool_metadata.get(procedure_id, {})
        if procedure_id not in by_id:
            base = promote_pass_through_runbook(dict(source))
        else:
            base = dict(by_id[procedure_id])
        hydrated = _hydrate_runbook_from_pool(base, source=source, metadata=metadata)
        by_id[procedure_id] = hydrated
    for procedure_id, runbook in list(by_id.items()):
        if not runbook.get("access_surface") or not runbook.get("capability_tags"):
            infer_runbook_tags(runbook)
            by_id[procedure_id] = runbook
    return list(by_id.values())


def _write_runbook_pool_diagnostic(
    output_path: Path,
    *,
    pool_dir: Path,
    runbooks: list[dict[str, Any]],
    retrieval_index: list[dict[str, Any]],
    generated_at: str,
) -> Path:
    target_ids = {
        "proc_query_active_agv_errors_from_the_wcs_database_v1",
        "proc_corroborate_agv_active_errors_using_agv_active_error_db_model_error_code_dictionary_sort_guid_v1",
    }
    loaded_ids = {
        str(item.get("procedure_id") or "")
        for item in runbooks
        if isinstance(item, dict)
    }
    index_ids = {
        str(item.get("finalized_runbook_id") or "")
        for item in retrieval_index
        if isinstance(item, dict)
    }
    hash_payload = {
        "runbook_ids": sorted(item for item in loaded_ids if item),
        "retrieval_index_ids": sorted(item for item in index_ids if item),
    }
    pool_hash = hashlib.sha256(
        json.dumps(hash_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    diagnostic = {
        "generated_at": generated_at,
        "runbook_pool_path": str((pool_dir / "runbook_pool.json").resolve()),
        "total_runbooks_loaded": len(runbooks),
        "helix_ssms_runbooks_loaded": sorted(loaded_ids & target_ids),
        "retrieval_index_version": hashlib.sha256(
            json.dumps(sorted(index_ids), separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:16],
        "candidate_pool_hash": pool_hash,
    }
    output_path.mkdir(parents=True, exist_ok=True)
    target = output_path / "runbook_pool_diagnostic.json"
    target.write_text(json.dumps(diagnostic, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def _load_playbook_candidates(incidents_root: str | Path, case_id: str, variant_subdir: str) -> list[dict[str, Any]]:
    path = Path(incidents_root) / f"case_{case_id}" / "stage_5_runbook_candidates" / variant_subdir / "playbook_candidates.json"
    payload = read_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"Expected list in {path}")
    return [item for item in payload if isinstance(item, dict)]


def _default_embedder() -> RunbookEmbedder:
    from shared_pipeline_stages.stage_6_5.embedder import AzureOpenAIEmbedder

    return AzureOpenAIEmbedder()


class _EmptyQueryEmbedder:
    @property
    def model_name(self) -> str:
        return "lexical-query-only"

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[] for _ in texts]


class EmbeddingCredentialsUnavailableError(RuntimeError):
    """Raised when semantic retrieval is required but Azure OpenAI embedding credentials are missing."""


def _default_brain_storage_provider() -> StorageProvider:
    from mcp_server.providers_config import get_storage_provider

    return get_storage_provider()


def _default_brain_embedding_provider() -> EmbeddingProvider:
    from mcp_server.providers_config import get_embedding_provider

    return get_embedding_provider()


def retrieval_mode_for_embedder(embedder: RunbookEmbedder) -> str:
    return "lexical" if embedder.model_name == _EmptyQueryEmbedder().model_name else "semantic"


def _retrieval_search_params(embedder: RunbookEmbedder, build_config: Stage8BuildConfig) -> tuple[int, float]:
    return max(build_config.top_k, LEXICAL_RETRIEVAL_TOP_K), 0.0


def _resolve_embedder(build_config: Stage8BuildConfig) -> RunbookEmbedder:
    if build_config.use_mock_embedder:
        return _EmptyQueryEmbedder()
    try:
        return _default_embedder()
    except RuntimeError as exc:
        if not build_config.allow_lexical_fallback:
            raise EmbeddingCredentialsUnavailableError(
                "Semantic retrieval requires a working Azure OpenAI embedder, but it could "
                f"not be initialized ({exc}). Refusing to silently continue with lexical-only "
                "(jaccard) scoring, since that materially changes which procedures are "
                "eligible/ranked and must not happen unnoticed for review or canonical "
                "artifacts. Fix the Azure OpenAI embedding credentials, or pass "
                "Stage8BuildConfig(allow_lexical_fallback=True) / --lexical-only to opt into "
                "lexical-only retrieval explicitly."
            ) from exc
        logger.warning(
            "Falling back to lexical-only retrieval: Azure OpenAI embedder could not be "
            "initialized (%s). Node queries will have no embedding vector, so scoring "
            "relies entirely on token-overlap (jaccard) similarity for this run. This was "
            "explicitly allowed via allow_lexical_fallback=True.",
            exc,
        )
        return _EmptyQueryEmbedder()


def _resolve_output_path(output_dir: Path) -> Path:
    if output_dir.name == STAGE8_DIR_NAME:
        return output_dir
    return output_dir / STAGE8_DIR_NAME
