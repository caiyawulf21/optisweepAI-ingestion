from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.embedder import MockRunbookEmbedder, RunbookEmbedder
from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json
from shared_pipeline_stages.stage_7.artifact_loader import load_artifact_index_from_pool
from shared_pipeline_stages.stage_8.comparison_report import build_comparison_report, build_variant_report
from shared_pipeline_stages.stage_8.linking_runner import PlaybookLinkClient
from shared_pipeline_stages.stage_8.linked_runbook_surface import attach_linked_runbooks
from shared_pipeline_stages.stage_8.normalize import (
    MAX_RUNBOOKS_PER_NODE,
    MIN_RETRIEVAL_FLOOR,
    build_branches_from_hints,
    build_decision_outcomes,
    needs_graph_repair,
    evaluate_link_confidence,
    reconcile_llm_runbook_links,
    select_runbook_matches,
    validate_finalized_playbook,
)
from shared_pipeline_stages.stage_8.playbook_retrieval import (
    build_playbook_retrieval_card,
    build_playbook_retrieval_index,
    extraction_mode_for_variant,
    playbook_id_from_candidate,
)
from shared_pipeline_stages.stage_8.review_markdown import write_playbook_review_files
from shared_pipeline_stages.stage_8.runbook_search import RunbookCatalogSearch, build_node_query_text
from shared_pipeline_stages.stage_8.schemas import (
    PlaybookRunbookLinkRow,
    Stage8BuildResult,
    VariantFinalizationReport,
)

STAGE8_DIR_NAME = "stage_8_finalized_playbooks"
PILOT_CASE_IDS = ["228086", "228723"]
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
    ) -> None:
        self.case_ids = case_ids or list(PILOT_CASE_IDS)
        self.top_k = top_k
        self.llm_used = llm_used
        self.min_retrieval_floor = min_retrieval_floor
        self.incident_preference_margin = incident_preference_margin
        self.max_runbooks_per_node = max_runbooks_per_node
        self.use_mock_embedder = use_mock_embedder


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
) -> Stage8BuildResult:
    build_config = config or Stage8BuildConfig()
    generated = generated_at or datetime.now(UTC).isoformat().replace("+00:00", "Z")
    output_path = _resolve_output_path(Path(output_dir))

    runbooks = _load_canonical_runbooks(stage7_dir)
    runbooks_by_id = {
        str(item.get("procedure_id") or ""): item for item in runbooks if str(item.get("procedure_id") or "").strip()
    }
    retrieval_cards = read_json(Path(pool_dir) / "retrieval_cards.json")
    retrieval_index = read_json(Path(pool_dir) / "runbook_retrieval_index.json")
    catalog = RunbookCatalogSearch.from_pool_artifacts(
        retrieval_cards,
        retrieval_index,
        runbooks,
        incident_preference_margin=build_config.incident_preference_margin,
    )
    active_embedder = embedder or (MockRunbookEmbedder() if build_config.use_mock_embedder else _default_embedder())
    artifact_index = load_artifact_index_from_pool(pool_dir)
    if build_config.use_mock_embedder or isinstance(active_embedder, MockRunbookEmbedder):
        _reindex_catalog_vectors(catalog, active_embedder)

    variant_reports: list[VariantFinalizationReport] = []
    total_playbooks = 0

    for variant_key, variant_subdir in PROMPT_VARIANTS.items():
        variant_dir = output_path / variant_key
        variant_dir.mkdir(parents=True, exist_ok=True)
        review_dir = variant_dir / "review_markdown" / "playbooks"
        review_dir.mkdir(parents=True, exist_ok=True)

        finalized_playbooks: list[dict[str, Any]] = []
        link_rows: list[dict[str, Any]] = []
        retrieval_cards_out: list[dict[str, Any]] = []
        warnings: list[str] = []
        extraction_mode = extraction_mode_for_variant(variant_key)

        for case_id in build_config.case_ids:
            candidates = _load_playbook_candidates(incidents_root, case_id, variant_subdir)
            for candidate in candidates:
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
                )
                playbook_warnings = validate_finalized_playbook(
                    playbook,
                    runbooks_by_id=runbooks_by_id,
                    max_runbooks_per_node=build_config.max_runbooks_per_node,
                )
                warnings.extend(playbook_warnings)
                playbook["needs_graph_repair"] = needs_graph_repair(playbook)
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

        variant_report = build_variant_report(
            finalized_playbooks,
            extraction_mode=extraction_mode,
            case_ids=build_config.case_ids,
            warnings=warnings,
        )
        variant_reports.append(variant_report)

        write_json(variant_dir / "canonical_playbooks.json", {"playbooks": finalized_playbooks, "generated_at": generated})
        write_json(variant_dir / "playbook_runbook_links.json", {"links": link_rows, "generated_at": generated})
        write_json(variant_dir / "playbook_retrieval_cards.json", {"cards": retrieval_cards_out, "generated_at": generated})
        write_json(
            variant_dir / "playbook_retrieval_index.json",
            {
                "embedding_model": embedding_model,
                "entries": [entry.model_dump() for entry in index_entries],
                "generated_at": generated,
            },
        )
        write_json(
            variant_dir / "playbook_finalization_report.json",
            {
                **variant_report.model_dump(),
                "generated_at": generated,
                "llm_used": build_config.llm_used,
                "warnings": warnings,
            },
        )
        total_playbooks += len(finalized_playbooks)

    comparison = build_comparison_report(variant_reports, case_ids=build_config.case_ids, generated_at=generated)
    write_json(output_path / "stage_8_comparison_report.json", comparison)

    return Stage8BuildResult(
        generated_at=generated,
        llm_used=build_config.llm_used,
        case_ids=build_config.case_ids,
        playbook_count=total_playbooks,
        variant_reports=variant_reports,
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
        for playbook in payload.get("playbooks") or []:
            if not isinstance(playbook, dict):
                continue
            for node in playbook.get("nodes") or []:
                if isinstance(node, dict):
                    attach_linked_runbooks(node, runbooks_by_id=runbooks_by_id)
            write_playbook_review_files(
                playbook,
                runbooks_by_id=runbooks_by_id,
                review_dir=review_dir,
                artifact_index=artifact_index,
                repo_root=root,
            )
            refreshed += 1
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
) -> dict[str, Any]:
    playbook_id = playbook_id_from_candidate(candidate, case_id)
    branch_hints = [hint for hint in candidate.get("branch_hints") or [] if isinstance(hint, dict)]
    node_candidates: dict[str, list[dict[str, Any]]] = {}
    node_vectors: dict[str, list[float]] = {}

    affected_systems = [str(item) for item in candidate.get("affected_systems_or_components") or [] if str(item).strip()]

    for node in candidate.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("node_id") or "")
        query_text = build_node_query_text(node, affected_systems=affected_systems)
        query_vector = embedder.embed_texts([query_text])[0] if query_text else []
        node_vectors[node_id] = query_vector
        matches = catalog.search_for_node(
            node,
            query_vector=query_vector,
            top_k=build_config.top_k,
            min_score=build_config.min_retrieval_floor,
            case_id=case_id,
            affected_systems=affected_systems,
        )
        node_candidates[node_id] = [match.model_dump() for match in matches]

    llm_payload = {
        "case_id": case_id,
        "playbook_candidate": candidate,
        "branch_hints": branch_hints,
        "node_runbook_candidates": node_candidates,
        "linking_policy": {
            "max_runbooks_per_node": build_config.max_runbooks_per_node,
            "min_retrieval_floor": build_config.min_retrieval_floor,
            "prefer_incident_derived_runbooks_for_procedure_reference_only": True,
            "incident_preference_margin": build_config.incident_preference_margin,
            "allow_low_confidence_partial_match": True,
            "use_normalized_node_queries": True,
            "boost_by_procedure_type": True,
            "prefer_manual_over_training_video": True,
        },
    }
    llm_response = llm_client.link(llm_payload) if llm_client and build_config.llm_used else {}

    finalized_nodes: list[dict[str, Any]] = []
    playbook_branches: list[dict[str, Any]] = []
    for node in candidate.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("node_id") or "")
        llm_node = _find_llm_node(llm_response, node_id)
        matches = catalog.search_for_node(
            node,
            query_vector=node_vectors.get(node_id),
            top_k=build_config.top_k,
            min_score=build_config.min_retrieval_floor,
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
        else:
            selected = select_runbook_matches(
                node,
                matches,
                runbooks_by_id=runbooks_by_id,
                max_runbooks=build_config.max_runbooks_per_node,
            )
            finalized_node = _build_node_from_matches(node, selected)
        linked_ids = [str(item) for item in finalized_node.get("resolved_runbook_ids") or []]
        finalized_node["decision_outcomes"] = llm_node.get("decision_outcomes") if llm_node else build_decision_outcomes(
            node,
            runbooks_by_id,
            linked_runbook_ids=linked_ids,
            branch_hints=branch_hints,
        )
        node_type = str(node.get("node_type") or "")
        llm_branches = llm_node.get("branches") if llm_node else None
        finalized_node["branches"] = build_branches_from_hints(node, branch_hints, llm_branches=llm_branches)
        if node_type == "branching_condition" and finalized_node["branches"]:
            playbook_branches.extend(
                {**branch, "from_node_id": node_id}
                for branch in finalized_node["branches"]
                if isinstance(branch, dict)
            )
        finalized_node["inherited_image_refs"] = _collect_inherited_image_refs(finalized_node, runbooks_by_id)
        attach_linked_runbooks(finalized_node, runbooks_by_id=runbooks_by_id)
        finalized_nodes.append(finalized_node)

    if llm_response.get("branches"):
        playbook_branches.extend(
            branch for branch in llm_response.get("branches") or [] if isinstance(branch, dict)
        )

    return {
        "playbook_id": playbook_id,
        "playbook_candidate_id": candidate.get("playbook_candidate_id"),
        "case_id": case_id,
        "extraction_mode": extraction_mode,
        "title": candidate.get("title"),
        "user_facing_summary": candidate.get("user_facing_summary"),
        "playbook_goal": candidate.get("playbook_goal"),
        "observed_entry_symptoms": candidate.get("observed_entry_symptoms") or [],
        "affected_systems_or_components": candidate.get("affected_systems_or_components") or [],
        "confidence": candidate.get("confidence"),
        "confidence_reason": candidate.get("confidence_reason"),
        "validation_status": "needs_sme_review",
        "nodes": finalized_nodes,
        "branches": playbook_branches,
        "branch_hints": branch_hints,
        "source_refs": candidate.get("source_refs") or [],
        "evidence_source_refs": candidate.get("evidence_source_refs") or [],
    }


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
            }
        )
    merged = dict(node)
    merged["resolved_runbook_ids"] = resolved_ids
    merged["runbook_links"] = links
    return merged


def _merge_llm_node(
    node: dict[str, Any],
    llm_node: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    retrieval_matches: list[Any] | None = None,
) -> dict[str, Any]:
    match_by_id = {match.procedure_id: match for match in retrieval_matches or []}
    merged = dict(node)
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
        return _build_node_from_matches(node, selected)
    links = reconcile_llm_runbook_links(
        node,
        links,
        list(retrieval_matches or []),
        runbooks_by_id=runbooks_by_id,
    )
    resolved_ids = [str(link.get("procedure_id") or "") for link in links if str(link.get("procedure_id") or "")]
    merged["resolved_runbook_ids"] = resolved_ids[:MAX_RUNBOOKS_PER_NODE]
    merged["runbook_links"] = links[:MAX_RUNBOOKS_PER_NODE]
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


def _load_canonical_runbooks(stage7_dir: str | Path) -> list[dict[str, Any]]:
    payload = read_json(Path(stage7_dir) / "canonical_runbooks.json")
    runbooks = payload.get("runbooks") if isinstance(payload, dict) else payload
    if not isinstance(runbooks, list):
        raise ValueError("canonical_runbooks.json must contain a runbooks list.")
    return [item for item in runbooks if isinstance(item, dict)]


def _load_playbook_candidates(incidents_root: str | Path, case_id: str, variant_subdir: str) -> list[dict[str, Any]]:
    path = Path(incidents_root) / f"case_{case_id}" / "stage_5_runbook_candidates" / variant_subdir / "playbook_candidates.json"
    payload = read_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"Expected list in {path}")
    return [item for item in payload if isinstance(item, dict)]


def _default_embedder() -> RunbookEmbedder:
    from shared_pipeline_stages.stage_6_5.embedder import AzureOpenAIEmbedder

    return AzureOpenAIEmbedder()


def _reindex_catalog_vectors(catalog: RunbookCatalogSearch, embedder: RunbookEmbedder) -> None:
    texts = [card.retrieval_text for card in catalog.cards]
    vectors = embedder.embed_texts(texts) if texts else []
    catalog.vectors = {
        card.finalized_runbook_id: vector
        for card, vector in zip(catalog.cards, vectors, strict=True)
    }


def _resolve_output_path(output_dir: Path) -> Path:
    if output_dir.name == STAGE8_DIR_NAME:
        return output_dir
    return output_dir / STAGE8_DIR_NAME
