"""Cumulative Stage 11: merge prior corpus, enrich operator language, gate, smoke, deliver."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from shared_pipeline_stages.stage_6_5.embedder import AzureOpenAIEmbedder, retrieval_text_hash
from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json
from shared_pipeline_stages.stage_11.corpus_merge import (
    merge_publish_bundles,
    rebuild_playbook_retrieval_text,
)
from shared_pipeline_stages.stage_11.duplicate_playbook_check import check_playbook_duplicates
from shared_pipeline_stages.stage_11.cosmos_publisher import publish_corpus_to_cosmos, upload_existing_publish_bundle
from shared_pipeline_stages.stage_11.image_blob_publisher import (
    assert_canonical_images_renderable,
    ensure_canonical_image_storage_uris,
)
from shared_pipeline_stages.stage_11.publish_gate import (
    inventory_from_bundle,
    load_deprecations,
    validate_cumulative_publish,
)
from shared_pipeline_stages.stage_11.gate_phrase_table import (
    GATE_PHRASE_BUNDLE_REL,
    GATE_PHRASE_DOC_ID,
    GATE_PHRASE_DOC_TYPE,
    build_gate_phrase_table,
    load_gate_phrase_table,
    smoke_gate_phrase_table,
)
from shared_pipeline_stages.stage_8.support_language import (
    collect_learned_phrases_from_playbooks,
    enrich_support_user_language_examples,
    write_learned_phrases,
)
from app_handoff_package.retrieval.local_hybrid_retriever import LocalHybridRetriever

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE = REPO_ROOT / "data/output/cosmos_publish"
DEFAULT_INCIDENTS_ROOT = REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents"
DEFAULT_SOURCE_ROOTS = [
    REPO_ROOT / "operationalknowledgeingestion/data/output/manual_optisweep_om_v3",
    REPO_ROOT / "operationalknowledgeingestion/data/output/training_video_day1",
    REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents/case_218550",
    REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents/case_223554",
    REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents/case_228086",
    REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents/case_228723",
]

SMOKE_QUERIES = [
    {"query": "AGVs stopped", "expect_case": "228086", "not_top_cases": ["218550", "223554"]},
    {"query": "AGVs stopped, no RMS alarms", "expect_case": "228086", "rank_above_cases": ["218550", "223554"]},
    {"query": "agvs aren't moving, rms showing no alarms", "expect_case": "228086", "rank_above_cases": ["218550", "223554"]},
    {"query": "bag out stopped AGV sequence", "expect_case": "218550"},
    {"query": "hospital induct blocked AGV tote state", "expect_case": "223554"},
    {"query": "zone unable to get a pair", "expect_case": "228723"},
    {"query": "every AMR goes to the hospital", "expect_case": "228723"},
]


@dataclass
class CumulativePublishResult:
    publish_version_id: str
    case_ids: list[str]
    playbook_ids: list[str]
    delivery_dir: Path
    merged_root: Path
    smoke_passed: bool
    gate_passed: bool
    uploaded: bool = False
    warnings: list[str] = field(default_factory=list)


def resolve_baseline_dir(explicit: str | Path | None = None) -> Path:
    if explicit is not None:
        path = Path(explicit)
        if path.exists():
            return path
        raise FileNotFoundError(f"Baseline publish dir not found: {path}")
    cosmos = REPO_ROOT / "data/output/cosmos_publish"
    if (cosmos / "publish_bundle").is_dir():
        return cosmos
    baseline_root = REPO_ROOT / "data/output/baseline_publishes"
    if baseline_root.is_dir():
        candidates = sorted(
            [p for p in baseline_root.iterdir() if p.is_dir() and (p / "publish_bundle").is_dir()],
            key=lambda p: p.name,
        )
        if candidates:
            return candidates[-1]
    raise FileNotFoundError(
        "No baseline publish found. Expected data/output/cosmos_publish or data/output/baseline_publishes/*."
    )


def run_cumulative_stage11(
    *,
    output_dir: str | Path,
    baseline_dir: str | Path | None = None,
    incidents_root: str | Path = DEFAULT_INCIDENTS_ROOT,
    source_roots: list[str | Path] | None = None,
    deprecations: str | Path | None = None,
    publish: bool = False,
    skip_assemble: bool = False,
    publish_version_id: str | None = None,
    run_smoke: bool = True,
    copy_to_delivery: bool = True,
) -> CumulativePublishResult:
    output_path = Path(output_dir)
    version_id = publish_version_id or f"publish_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
    stage11_dir = output_path / "stage_11_cosmos_publish"
    baseline_path = resolve_baseline_dir(baseline_dir)
    baseline_bundle = _resolve_bundle(baseline_path)
    roots = [Path(p) for p in (source_roots or DEFAULT_SOURCE_ROOTS)]
    incidents = Path(incidents_root)

    if not skip_assemble:
        publish_corpus_to_cosmos(
            stage7_dir=output_path / "stage_7_merged_runbooks",
            stage8_dir=output_path / "stage_8_finalized_playbooks",
            stage10_dir=output_path / "stage_10_embeddings",
            stage85_dir=output_path / "stage_8_5_relationship_linking",
            stage9_dir=output_path / "stage_9_validation",
            source_roots=roots,
            output_dir=output_path,
            publish=False,
            publish_version_id=version_id,
            # Upload Blob bytes whenever storage credentials are configured so
            # cumulative publishes do not overwrite live SAS URIs with metadata-only docs.
            upload_image_blobs=None,
        )

    candidate_bundle = stage11_dir / "publish_bundle"
    if not candidate_bundle.is_dir():
        raise FileNotFoundError(f"Candidate Stage 11 bundle missing: {candidate_bundle}")

    merged_root = stage11_dir / "cumulative_publish"
    if merged_root.exists():
        shutil.rmtree(merged_root)
    merged_bundle = merged_root / "publish_bundle"
    merged_bundle.mkdir(parents=True)

    merge_stats = merge_publish_bundles(
        candidate_bundle_dir=candidate_bundle,
        baseline_bundle_dir=baseline_bundle,
        output_bundle_dir=merged_bundle,
        publish_version_id=version_id,
        incidents_root=incidents,
    )
    learned_phrases = list(merge_stats.pop("learned_phrases", []) or [])
    write_learned_phrases(merged_root / "learned_operator_phrases.json", learned_phrases)
    write_json(merged_root / "merge_report.json", merge_stats)

    image_uri_stats = _ensure_merged_image_storage_uris(merged_bundle)
    write_json(merged_root / "canonical_image_storage_uri_report.json", image_uri_stats)

    embed_stats = _refresh_playbook_embeddings(
        merged_bundle,
        incidents_root=incidents,
        learned_phrases=learned_phrases,
    )
    write_json(merged_root / "embedding_refresh_report.json", embed_stats)

    final_playbooks: list[dict[str, Any]] = []
    playbook_vectors: dict[str, list[float]] = {}
    for variant in ("playbooks_prompt_a", "playbooks_prompt_b"):
        for doc in _load_list(merged_bundle / variant / "documents.json"):
            payload = doc.get("payload") if isinstance(doc.get("payload"), dict) else {}
            if payload:
                final_playbooks.append(payload)
        for emb in _load_list(merged_bundle / variant / "embeddings.json"):
            source_id = str(emb.get("source_record_id") or "")
            vector = emb.get("vector")
            if source_id and isinstance(vector, list):
                playbook_vectors[source_id] = vector
    learned_phrases = collect_learned_phrases_from_playbooks(final_playbooks)
    write_learned_phrases(merged_root / "learned_operator_phrases.json", learned_phrases)
    write_learned_phrases(output_path / "learned_operator_phrases.json", learned_phrases)

    duplicate_check = check_playbook_duplicates(
        final_playbooks,
        embeddings_by_playbook_id=playbook_vectors,
    )
    write_json(merged_root / "duplicate_playbook_report.json", duplicate_check.to_dict())

    prior_gate_rows = _load_list(baseline_bundle / GATE_PHRASE_BUNDLE_REL)
    prior_gate = load_gate_phrase_table(prior_gate_rows[0] if prior_gate_rows else None)
    gate_phrase_doc = build_gate_phrase_table(
        publish_version_id=version_id,
        playbooks=final_playbooks,
        prior_table=prior_gate,
        learned_phrases=learned_phrases,
    )
    write_json(merged_bundle / GATE_PHRASE_BUNDLE_REL, [gate_phrase_doc])
    write_json(merged_root / "gate_phrase_table.json", gate_phrase_doc)
    gate_phrase_smoke = smoke_gate_phrase_table(gate_phrase_doc)
    write_json(merged_root / "gate_phrase_smoke_report.json", gate_phrase_smoke)
    if not gate_phrase_smoke.get("passed"):
        raise ValueError(
            "gate_phrase_table smoke failed: missing "
            + ", ".join(gate_phrase_smoke.get("missing") or [])
        )

    baseline_inventory = inventory_from_bundle(baseline_bundle)
    candidate_inventory = inventory_from_bundle(merged_bundle)
    gate = validate_cumulative_publish(
        candidate=candidate_inventory,
        baseline=baseline_inventory,
        deprecated_ids=load_deprecations(deprecations),
        require_image_storage_uri=publish,
    )
    gate.warnings.extend(duplicate_check.warnings())
    write_json(merged_root / "publish_manifest_diff.json", gate.to_dict())
    if not gate.passed:
        raise ValueError("Pre-publish cumulative gate failed: " + "; ".join(gate.errors))

    write_json(
        merged_root / "publish_manifest.json",
        {
            "publish_version_id": version_id,
            "generated_at": datetime.now(UTC).isoformat(),
            "embedding_model": "text-embedding-3-small",
            "record_counts": _count_bundle(merged_bundle),
            "case_ids": sorted(candidate_inventory.case_ids),
            "playbook_ids": sorted(candidate_inventory.playbook_ids),
            "baseline_publish_dir": str(baseline_path),
            "merge_stats": merge_stats,
            "gate": gate.to_dict(),
            "duplicate_playbook_check": duplicate_check.to_dict(),
            "gate_phrase_table": {
                "container": "gate_phrase_tables",
                "doc_type": GATE_PHRASE_DOC_TYPE,
                "id": GATE_PHRASE_DOC_ID,
                "legacy_key_count": len((gate_phrase_doc.get("legacy_signal_phrases") or {})),
                "canonical_key_count": len((gate_phrase_doc.get("canonical_signal_phrases") or {})),
                "component_key_count": len((gate_phrase_doc.get("component_phrases") or {})),
                "smoke": gate_phrase_smoke,
            },
            "source_paths": {
                "candidate_bundle": str(candidate_bundle),
                "baseline_bundle": str(baseline_bundle),
                "merged_bundle": str(merged_bundle),
                "gate_phrase_table": str(merged_bundle / GATE_PHRASE_BUNDLE_REL),
            },
        },
    )
    write_json(
        merged_root / "case_inventory.json",
        {
            "case_ids": sorted(candidate_inventory.case_ids),
            "playbook_ids": sorted(candidate_inventory.playbook_ids),
            "prior_cases_retained": sorted(baseline_inventory.case_ids & candidate_inventory.case_ids),
            "added_cases": sorted(candidate_inventory.case_ids - baseline_inventory.case_ids),
        },
    )

    smoke = {"passed": True, "errors": [], "results": []}
    if run_smoke:
        smoke = _run_smoke(merged_bundle)
        write_json(merged_root / "retrieval_smoke_report.json", smoke)
        if not smoke.get("passed"):
            raise ValueError("Retrieval smoke failed: " + "; ".join(smoke.get("errors") or []))

    delivery_dir = REPO_ROOT / "data/output/cosmos_publish"
    if copy_to_delivery:
        if delivery_dir.exists():
            shutil.rmtree(delivery_dir)
        shutil.copytree(merged_root, delivery_dir)

    uploaded = False
    warnings: list[str] = list(image_uri_stats.get("warnings") or [])
    if publish:
        image_docs = _load_list(merged_bundle / "canonical_images" / "documents.json")
        assert_canonical_images_renderable(
            image_docs,
            context="cumulative Stage 11 Cosmos publish",
        )
        uploaded, _, warnings, _counts = upload_existing_publish_bundle(
            delivery_dir if copy_to_delivery else merged_root,
            publish_scope="all",
            baseline_publish_dir=baseline_path,
            allow_metadata_only_images=False,
        )
        if not uploaded:
            raise RuntimeError("Cosmos upload failed: " + "; ".join(warnings))

    return CumulativePublishResult(
        publish_version_id=version_id,
        case_ids=sorted(candidate_inventory.case_ids),
        playbook_ids=sorted(candidate_inventory.playbook_ids),
        delivery_dir=delivery_dir if copy_to_delivery else merged_root,
        merged_root=merged_root,
        smoke_passed=bool(smoke.get("passed")),
        gate_passed=True,
        uploaded=uploaded,
        warnings=warnings,
    )


def _ensure_merged_image_storage_uris(merged_bundle: Path) -> dict[str, Any]:
    images_path = merged_bundle / "canonical_images" / "documents.json"
    docs = _load_list(images_path)
    before_missing = sum(
        1
        for doc in docs
        if not str(doc.get("storage_uri") or "").startswith(("http://", "https://"))
    )
    updated, warnings = ensure_canonical_image_storage_uris(docs)
    write_json(images_path, updated)
    after_missing = sum(
        1
        for doc in updated
        if not str(doc.get("storage_uri") or "").startswith(("http://", "https://"))
    )
    return {
        "image_count": len(updated),
        "missing_before": before_missing,
        "missing_after": after_missing,
        "renderable": len(updated) - after_missing,
        "warnings": warnings,
    }


def _resolve_bundle(path: Path) -> Path:
    if (path / "publish_bundle").is_dir():
        return path / "publish_bundle"
    if path.is_dir():
        return path
    raise FileNotFoundError(f"Baseline publish bundle not found: {path}")


def _refresh_playbook_embeddings(
    bundle_dir: Path,
    *,
    incidents_root: Path,
    learned_phrases: list[str] | None = None,
) -> dict[str, Any]:
    embedder = AzureOpenAIEmbedder()
    refreshed = 0
    for variant in ("playbooks_prompt_a", "playbooks_prompt_b"):
        docs_path = bundle_dir / variant / "documents.json"
        emb_path = bundle_dir / variant / "embeddings.json"
        docs = _load_list(docs_path)
        embeddings = _load_list(emb_path)
        emb_by_source = {
            str(row.get("source_record_id") or ""): row
            for row in embeddings
            if str(row.get("source_record_id") or "")
        }
        for doc in docs:
            payload = doc.get("payload") if isinstance(doc.get("payload"), dict) else {}
            case_id = str(payload.get("case_id") or "")
            playbook_id = str(payload.get("playbook_id") or doc.get("record_id") or "")
            examples = list(payload.get("support_user_language_examples") or [])
            stage5_examples = _stage5_examples(
                incidents_root, case_id, playbook_id, str(payload.get("extraction_mode") or "")
            )
            if stage5_examples:
                examples = list(dict.fromkeys([*examples, *stage5_examples]))
            payload["support_user_language_examples"] = enrich_support_user_language_examples(
                examples,
                case_id=case_id,
                title=str(payload.get("title") or ""),
                observed_entry_symptoms=list(payload.get("observed_entry_symptoms") or []),
                learned_phrases=learned_phrases,
            )
            doc["payload"] = payload
            retrieval_text = rebuild_playbook_retrieval_text(payload)
            existing = emb_by_source.get(playbook_id)
            if existing and str(existing.get("embedded_text") or "") == retrieval_text and existing.get("vector"):
                continue
            vector = embedder.embed_texts([retrieval_text])[0]
            record_type = "playbook_prompt_a" if variant.endswith("_a") else "playbook_prompt_b"
            emb_by_source[playbook_id] = {
                "id": f"emb_{record_type}_{playbook_id}",
                "doc_type": "embedding",
                "publish_version_id": doc.get("publish_version_id"),
                "record_type": record_type,
                "source_record_id": playbook_id,
                "embedded_text": retrieval_text,
                "vector": vector,
                "embedding_model": embedder.model_name,
                "embedding_dimensions": len(vector),
                "retrieval_text_hash": retrieval_text_hash(retrieval_text),
                "filter_metadata": {
                    "playbook_id": playbook_id,
                    "case_id": case_id,
                    "extraction_mode": str(payload.get("extraction_mode") or ""),
                    "title": str(payload.get("title") or ""),
                },
                "source_refs": [{"playbook_candidate_id": payload.get("playbook_candidate_id")}],
            }
            refreshed += 1
        write_json(docs_path, docs)
        write_json(emb_path, list(emb_by_source.values()))
    return {"refreshed_playbook_embeddings": refreshed}


def _stage5_examples(incidents_root: Path, case_id: str, playbook_id: str, extraction_mode: str) -> list[str]:
    variants = (
        ["playbook_prompt_b_multi_flow", "playbook_prompt_a_one_per_incident"]
        if "separable" in extraction_mode or "multi" in extraction_mode
        else ["playbook_prompt_a_one_per_incident", "playbook_prompt_b_multi_flow"]
    )
    needle = playbook_id.replace("playbook_", "playbook_candidate_", 1)
    for variant in variants:
        path = incidents_root / f"case_{case_id}" / "stage_5_runbook_candidates" / variant / "playbook_candidates.json"
        if not path.exists():
            continue
        rows = read_json(path)
        if isinstance(rows, dict):
            rows = rows.get("playbook_candidates") or []
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            candidate_id = str(row.get("playbook_candidate_id") or "")
            if candidate_id == needle or candidate_id.replace("playbook_candidate_", "playbook_") == playbook_id:
                return [str(item) for item in row.get("support_user_language_examples") or [] if str(item).strip()]
        if len(rows) == 1 and isinstance(rows[0], dict):
            return [str(item) for item in rows[0].get("support_user_language_examples") or [] if str(item).strip()]
    return []


def _run_smoke(bundle_dir: Path) -> dict[str, Any]:
    embedder = AzureOpenAIEmbedder()
    records: list[dict[str, Any]] = []
    symptom_cards: dict[str, dict[str, Any]] = {}
    for variant, record_type in (
        ("playbooks_prompt_a", "playbook_prompt_a"),
        ("playbooks_prompt_b", "playbook_prompt_b"),
    ):
        docs = _load_list(bundle_dir / variant / "documents.json")
        embs = _load_list(bundle_dir / variant / "embeddings.json")
        for doc in docs:
            payload = doc.get("payload") if isinstance(doc.get("payload"), dict) else {}
            playbook_id = str(payload.get("playbook_id") or doc.get("record_id") or "")
            if playbook_id:
                symptom_cards[playbook_id] = {
                    "playbook_id": playbook_id,
                    "case_id": payload.get("case_id"),
                    "title": payload.get("title"),
                    "observed_entry_symptoms": payload.get("observed_entry_symptoms") or [],
                    "support_user_language_examples": payload.get("support_user_language_examples") or [],
                }
        for emb in embs:
            row = dict(emb)
            row["record_type"] = record_type
            card = symptom_cards.get(str(row.get("source_record_id") or ""), {})
            row["filter_metadata"] = {
                **(row.get("filter_metadata") or {}),
                "title": card.get("title"),
                "case_id": card.get("case_id"),
            }
            records.append(row)

    retriever = LocalHybridRetriever(records, symptom_cards=symptom_cards)
    results = []
    errors = []
    for spec in SMOKE_QUERIES:
        query = spec["query"]
        vector = embedder.embed_texts([query])[0]
        hits = retriever.search(
            query,
            query_vector=vector,
            record_types={"playbook_prompt_a", "playbook_prompt_b"},
            top_k=3,
        )
        top_rows = []
        for hit in hits:
            case_id = str(
                (hit.filter_metadata or {}).get("case_id")
                or symptom_cards.get(hit.source_record_id, {}).get("case_id")
                or ""
            )
            top_rows.append(
                {
                    "playbook_id": hit.source_record_id,
                    "case_id": case_id,
                    "title": hit.title,
                    "combined": hit.combined_score,
                    "cosine": hit.cosine_score,
                    "lexical": hit.jaccard_score,
                    "symptom": hit.symptom_score,
                    "coverage": hit.coverage,
                }
            )
        expect_case = str(spec.get("expect_case") or "")
        if expect_case and (not top_rows or top_rows[0]["case_id"] != expect_case):
            errors.append(
                f"Query '{query}' expected top case {expect_case}, got "
                f"{top_rows[0]['case_id'] if top_rows else None}"
            )
        for blocked in spec.get("not_top_cases") or []:
            if top_rows and top_rows[0]["case_id"] == blocked:
                errors.append(f"Query '{query}' top case must not be {blocked}")
        for other in spec.get("rank_above_cases") or []:
            expect_rank = next((i for i, row in enumerate(top_rows) if row["case_id"] == expect_case), None)
            other_rank = next((i for i, row in enumerate(top_rows) if row["case_id"] == other), None)
            if expect_rank is None:
                errors.append(f"Query '{query}' missing expected case {expect_case} in top-3")
            elif other_rank is not None and other_rank < expect_rank:
                errors.append(f"Query '{query}' case {expect_case} must rank above {other}")
        results.append({"query": query, "top3": top_rows})
    return {"passed": not errors, "errors": errors, "results": results}


def _count_bundle(bundle_dir: Path) -> dict[str, int]:
    counts = {}
    for rel in (
        "runbooks/documents.json",
        "runbooks/embeddings.json",
        "playbooks_prompt_a/documents.json",
        "playbooks_prompt_a/embeddings.json",
        "playbooks_prompt_b/documents.json",
        "playbooks_prompt_b/embeddings.json",
        "operational_context/rag_records.json",
        "source_artifacts/rag_records.json",
        "canonical_images/documents.json",
    ):
        counts[rel] = len(_load_list(bundle_dir / rel))
    links_dir = bundle_dir / "relationship_links"
    link_count = 0
    shard_count = 0
    if links_dir.is_dir():
        for path in links_dir.glob("shard_*.json"):
            shard_count += 1
            payload = read_json(path)
            if isinstance(payload, dict):
                link_count += len(payload.get("links") or [])
    counts["relationship_links"] = link_count
    counts["relationship_shards"] = shard_count
    counts["gate_phrase_tables/documents.json"] = len(_load_list(bundle_dir / GATE_PHRASE_BUNDLE_REL))
    return counts


def _load_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = read_json(path)
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    return []
