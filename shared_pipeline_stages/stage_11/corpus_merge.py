from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_8.playbook_retrieval import build_playbook_retrieval_text
from shared_pipeline_stages.stage_8.schemas import PlaybookRetrievalCard
from shared_pipeline_stages.stage_8.support_language import (
    collect_learned_phrases_from_playbooks,
    enrich_playbook_record,
    enrich_support_user_language_examples,
)


def merge_publish_bundles(
    *,
    candidate_bundle_dir: str | Path,
    baseline_bundle_dir: str | Path,
    output_bundle_dir: str | Path,
    publish_version_id: str,
    incidents_root: str | Path | None = None,
    learned_phrases: list[str] | None = None,
) -> dict[str, Any]:
    candidate_root = Path(candidate_bundle_dir)
    baseline_root = Path(baseline_bundle_dir)
    output_root = Path(output_bundle_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    stats: dict[str, Any] = {
        "kept_from_candidate": 0,
        "merged_from_baseline": 0,
        "datasets": {},
    }

    seed_playbooks: list[dict[str, Any]] = []
    for root in (baseline_root, candidate_root):
        for variant in ("playbooks_prompt_a", "playbooks_prompt_b"):
            for doc in _load_rows(root / variant / "documents.json"):
                payload = doc.get("payload") if isinstance(doc.get("payload"), dict) else doc
                if isinstance(payload, dict):
                    seed_playbooks.append(payload)
    phrases = list(learned_phrases or [])
    phrases.extend(collect_learned_phrases_from_playbooks(seed_playbooks))
    phrases = enrich_support_user_language_examples(phrases)

    dataset_files = {
        "runbooks/documents.json": "id",
        "runbooks/embeddings.json": "id",
        "playbooks_prompt_a/documents.json": "id",
        "playbooks_prompt_a/embeddings.json": "id",
        "playbooks_prompt_b/documents.json": "id",
        "playbooks_prompt_b/embeddings.json": "id",
        "operational_context/rag_records.json": "id",
        "operational_context/embeddings.json": "id",
        "source_artifacts/rag_records.json": "id",
        "source_artifacts/embeddings.json": "id",
        "canonical_images/documents.json": "id",
    }

    for rel_path, id_key in dataset_files.items():
        candidate_rows = _load_rows(candidate_root / rel_path)
        baseline_rows = _load_rows(baseline_root / rel_path)
        if rel_path == "canonical_images/documents.json":
            merged, kept, added = _merge_canonical_images(
                candidate_rows,
                baseline_rows,
                publish_version_id=publish_version_id,
            )
        elif rel_path.startswith("playbooks_prompt_a/"):
            # Prompt A is one-playbook-per-incident: key by case_id so a
            # regenerated candidate (new playbook_candidate_id slug) replaces
            # the prior playbook for that case instead of accumulating
            # alongside it under a different document id.
            merged, kept, added = _merge_playbooks_by_case(
                candidate_rows,
                baseline_rows,
                publish_version_id=publish_version_id,
            )
        else:
            merged, kept, added = _merge_by_key(
                candidate_rows,
                baseline_rows,
                id_key=id_key,
                publish_version_id=publish_version_id,
            )
        if "playbooks_prompt" in rel_path and rel_path.endswith("documents.json"):
            merged = [
                _enrich_playbook_doc(
                    doc,
                    incidents_root=incidents_root,
                    learned_phrases=phrases,
                )
                for doc in merged
            ]
        _write_rows(output_root / rel_path, merged)
        stats["kept_from_candidate"] += kept
        stats["merged_from_baseline"] += added
        stats["datasets"][rel_path] = {
            "candidate": len(candidate_rows),
            "baseline": len(baseline_rows),
            "merged": len(merged),
            "added_from_baseline": added,
        }

    cand_shards = _load_relationship_shards(candidate_root)
    base_shards = _load_relationship_shards(baseline_root)
    merged_links = _merge_relationship_links(cand_shards, base_shards)
    shard_docs = _shard_links(merged_links, publish_version_id=publish_version_id)
    for index, shard in enumerate(shard_docs):
        _write_rows(output_root / f"relationship_links/shard_{index:03d}.json", shard)
    stats["datasets"]["relationship_links"] = {
        "candidate_links": sum(len(shard.get("links") or []) for shard in cand_shards),
        "baseline_links": sum(len(shard.get("links") or []) for shard in base_shards),
        "merged_links": len(merged_links),
        "shards": len(shard_docs),
    }
    stats["learned_phrase_count"] = len(phrases)
    stats["learned_phrases"] = phrases
    return stats


def rebuild_playbook_retrieval_text(payload: dict[str, Any]) -> str:
    card = PlaybookRetrievalCard(
        playbook_id=str(payload.get("playbook_id") or ""),
        playbook_candidate_id=str(payload.get("playbook_candidate_id") or ""),
        case_id=str(payload.get("case_id") or ""),
        extraction_mode=str(payload.get("extraction_mode") or ""),
        title=str(payload.get("title") or ""),
        user_facing_summary=str(payload.get("user_facing_summary") or ""),
        observed_entry_symptoms=[
            str(item) for item in payload.get("observed_entry_symptoms") or [] if str(item).strip()
        ],
        support_user_language_examples=[
            str(item)
            for item in payload.get("support_user_language_examples") or []
            if str(item).strip()
        ],
        affected_systems_or_components=[
            str(item)
            for item in payload.get("affected_systems_or_components") or []
            if str(item).strip()
        ],
    )
    return build_playbook_retrieval_text(card)


def _enrich_playbook_doc(
    doc: dict[str, Any],
    *,
    incidents_root: str | Path | None,
    learned_phrases: list[str] | None = None,
) -> dict[str, Any]:
    payload = doc.get("payload")
    if not isinstance(payload, dict):
        return doc
    examples = list(payload.get("support_user_language_examples") or [])
    if incidents_root is not None:
        stage5_examples = _examples_from_stage5(
            incidents_root,
            case_id=str(payload.get("case_id") or ""),
            playbook_id=str(payload.get("playbook_id") or ""),
            extraction_mode=str(payload.get("extraction_mode") or ""),
        )
        if stage5_examples:
            examples = list(dict.fromkeys([*examples, *stage5_examples]))
    payload["support_user_language_examples"] = enrich_support_user_language_examples(
        examples,
        case_id=str(payload.get("case_id") or ""),
        title=str(payload.get("title") or ""),
        observed_entry_symptoms=list(payload.get("observed_entry_symptoms") or []),
        learned_phrases=learned_phrases,
    )
    enrich_playbook_record(payload, learned_phrases=learned_phrases)
    doc["payload"] = payload
    return doc


def _examples_from_stage5(
    incidents_root: str | Path,
    *,
    case_id: str,
    playbook_id: str,
    extraction_mode: str,
) -> list[str]:
    if not case_id:
        return []
    variant = (
        "playbook_prompt_a_one_per_incident"
        if "one_playbook_candidate_per_incident" in extraction_mode or playbook_id.count("_") < 0
        else "playbook_prompt_b_multi_flow"
    )
    if "multi" in extraction_mode or "separable" in extraction_mode:
        variant = "playbook_prompt_b_multi_flow"
    elif "one_playbook" in extraction_mode or extraction_mode.endswith("one_per_incident"):
        variant = "playbook_prompt_a_one_per_incident"
    else:
        # Try both variants.
        for candidate_variant in (
            "playbook_prompt_a_one_per_incident",
            "playbook_prompt_b_multi_flow",
        ):
            examples = _match_stage5_examples(incidents_root, case_id, playbook_id, candidate_variant)
            if examples:
                return examples
        return []
    return _match_stage5_examples(incidents_root, case_id, playbook_id, variant)


def _match_stage5_examples(
    incidents_root: str | Path,
    case_id: str,
    playbook_id: str,
    variant: str,
) -> list[str]:
    path = (
        Path(incidents_root)
        / f"case_{case_id}"
        / "stage_5_runbook_candidates"
        / variant
        / "playbook_candidates.json"
    )
    if not path.exists():
        return []
    rows = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("playbook_candidates") or []
    if not isinstance(rows, list):
        return []
    needle = playbook_id.replace("playbook_", "playbook_candidate_", 1)
    for row in rows:
        if not isinstance(row, dict):
            continue
        candidate_id = str(row.get("playbook_candidate_id") or "")
        if candidate_id == needle or candidate_id.replace("playbook_candidate_", "playbook_") == playbook_id:
            return [str(item) for item in row.get("support_user_language_examples") or [] if str(item).strip()]
    if len(rows) == 1 and isinstance(rows[0], dict):
        return [str(item) for item in rows[0].get("support_user_language_examples") or [] if str(item).strip()]
    return []


def _merge_by_key(
    candidate_rows: list[dict[str, Any]],
    baseline_rows: list[dict[str, Any]],
    *,
    id_key: str,
    publish_version_id: str,
) -> tuple[list[dict[str, Any]], int, int]:
    merged: dict[str, dict[str, Any]] = {}
    for row in baseline_rows:
        key = _row_key(row, id_key)
        if not key:
            continue
        cloned = dict(row)
        cloned["publish_version_id"] = publish_version_id
        merged[key] = cloned
    baseline_count = len(merged)
    for row in candidate_rows:
        key = _row_key(row, id_key)
        if not key:
            continue
        cloned = dict(row)
        cloned["publish_version_id"] = publish_version_id
        merged[key] = cloned
    added = max(0, len(merged) - len(candidate_rows))
    # Prefer counting true baseline-only additions:
    candidate_keys = {_row_key(row, id_key) for row in candidate_rows if _row_key(row, id_key)}
    added_from_baseline = sum(1 for key in merged if key not in candidate_keys)
    kept = len(candidate_keys)
    _ = baseline_count
    return list(merged.values()), kept, added_from_baseline


def _playbook_case_key(row: dict[str, Any]) -> str:
    payload = row.get("payload")
    if isinstance(payload, dict) and str(payload.get("case_id") or "").strip():
        return str(payload["case_id"]).strip()
    metadata = row.get("filter_metadata")
    if isinstance(metadata, dict) and str(metadata.get("case_id") or "").strip():
        return str(metadata["case_id"]).strip()
    return ""


def _merge_playbooks_by_case(
    candidate_rows: list[dict[str, Any]],
    baseline_rows: list[dict[str, Any]],
    *,
    publish_version_id: str,
) -> tuple[list[dict[str, Any]], int, int]:
    """Merge prompt_a playbook rows keyed by case_id, not document id.

    Prompt A is contractually one playbook per incident. A regenerated
    candidate for a case (new playbook_candidate_id slug, e.g. after a
    Stage 5 rerun) must replace the prior playbook for that case_id, not
    accumulate alongside it under a different document id — _merge_by_key's
    exact-id union is what let stale per-case duplicates pile up across
    cumulative publishes.

    Rows without a resolvable case_id (should not happen for prompt_a) fall
    back to id-based merge so they are not silently dropped.
    """
    merged: dict[str, dict[str, Any]] = {}
    fallback_baseline: dict[str, dict[str, Any]] = {}
    for row in baseline_rows:
        case_key = _playbook_case_key(row)
        cloned = dict(row)
        cloned["publish_version_id"] = publish_version_id
        if case_key:
            merged[case_key] = cloned
        else:
            key = _row_key(row, "id")
            if key:
                fallback_baseline[key] = cloned

    candidate_case_keys: set[str] = set()
    for row in candidate_rows:
        case_key = _playbook_case_key(row)
        cloned = dict(row)
        cloned["publish_version_id"] = publish_version_id
        if case_key:
            merged[case_key] = cloned
            candidate_case_keys.add(case_key)
        else:
            key = _row_key(row, "id")
            if key:
                fallback_baseline[key] = cloned

    added_from_baseline = sum(1 for key in merged if key not in candidate_case_keys)
    kept = len(candidate_case_keys)
    result = list(merged.values()) + list(fallback_baseline.values())
    return result, kept, added_from_baseline


def _has_http_storage_uri(row: dict[str, Any]) -> bool:
    storage_uri = str(row.get("storage_uri") or "").strip()
    return storage_uri.startswith("http://") or storage_uri.startswith("https://")


def _merge_image_row(baseline: dict[str, Any] | None, candidate: dict[str, Any]) -> dict[str, Any]:
    """Prefer candidate metadata, but never drop a working HTTPS storage_uri."""
    merged = dict(candidate)
    if baseline is None:
        return merged
    if _has_http_storage_uri(candidate):
        return merged
    if _has_http_storage_uri(baseline):
        merged["storage_uri"] = baseline.get("storage_uri")
        if str(baseline.get("blob_path") or "").strip():
            merged["blob_path"] = baseline.get("blob_path")
        if str(baseline.get("content_type") or "").strip() and not str(
            merged.get("content_type") or ""
        ).strip():
            merged["content_type"] = baseline.get("content_type")
    return merged


def _merge_canonical_images(
    candidate_rows: list[dict[str, Any]],
    baseline_rows: list[dict[str, Any]],
    *,
    publish_version_id: str,
) -> tuple[list[dict[str, Any]], int, int]:
    merged: dict[str, dict[str, Any]] = {}
    baseline_by_key: dict[str, dict[str, Any]] = {}
    for row in baseline_rows:
        key = _row_key(row, "id")
        if not key:
            continue
        cloned = dict(row)
        cloned["publish_version_id"] = publish_version_id
        baseline_by_key[key] = cloned
        merged[key] = cloned
    for row in candidate_rows:
        key = _row_key(row, "id")
        if not key:
            continue
        cloned = dict(row)
        cloned["publish_version_id"] = publish_version_id
        merged[key] = _merge_image_row(baseline_by_key.get(key), cloned)
    candidate_keys = {_row_key(row, "id") for row in candidate_rows if _row_key(row, "id")}
    added_from_baseline = sum(1 for key in merged if key not in candidate_keys)
    kept = len(candidate_keys)
    return list(merged.values()), kept, added_from_baseline


def _row_key(row: dict[str, Any], id_key: str) -> str:
    value = row.get(id_key)
    if value:
        return str(value)
    for key in ("record_id", "source_record_id", "image_id", "id"):
        if row.get(key):
            return str(row.get(key))
    payload = row.get("payload")
    if isinstance(payload, dict):
        for key in ("playbook_id", "procedure_id"):
            if payload.get(key):
                return str(payload.get(key))
    return ""


def _merge_relationship_links(
    candidate_shards: list[dict[str, Any]],
    baseline_shards: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for shard in baseline_shards + candidate_shards:
        for link in shard.get("links") or []:
            if not isinstance(link, dict):
                continue
            key = "|".join(
                [
                    str(link.get("link_type") or ""),
                    str(link.get("source_record_id") or ""),
                    str(link.get("target_record_id") or ""),
                    str(link.get("link_rank") or ""),
                ]
            )
            merged[key] = link
    return list(merged.values())


def _shard_links(links: list[dict[str, Any]], *, publish_version_id: str) -> list[dict[str, Any]]:
    from datetime import UTC, datetime

    generated_at = datetime.now(UTC).isoformat()
    limit = 2000
    shards: list[dict[str, Any]] = []
    for index in range(0, max(len(links), 1), limit):
        batch = links[index : index + limit]
        if not batch and links:
            continue
        if not batch:
            break
        shard_index = len(shards)
        shards.append(
            {
                "id": f"relationship_graph_{publish_version_id}_{shard_index:03d}",
                "doc_type": "relationship_link_shard",
                "publish_version_id": publish_version_id,
                "generated_at": generated_at,
                "shard_index": shard_index,
                "shard_count": 0,
                "link_count": len(batch),
                "links": batch,
            }
        )
    for shard in shards:
        shard["shard_count"] = len(shards)
    return shards


def _load_relationship_shards(bundle_root: Path) -> list[dict[str, Any]]:
    links_dir = bundle_root / "relationship_links"
    if not links_dir.is_dir():
        return []
    shards: list[dict[str, Any]] = []
    for path in sorted(links_dir.glob("shard_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            shards.append(payload)
    return shards


def _load_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        return [payload]
    return []


def _write_rows(path: Path, rows: list[dict[str, Any]] | dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
