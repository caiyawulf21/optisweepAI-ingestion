from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json

DEMO_PROMPTS = (
    {
        "id": "prompt_1",
        "label": "AGVs stopped",
        "query": "All AGVs stopped moving after ignition restart optisweep not responding nothing moving",
        "expected_case_id": "228086",
    },
    {
        "id": "prompt_2",
        "label": "Zone cannot pair",
        "query": "Zone cannot get a pair AMRs diverting to hospital after robot replacement",
        "expected_case_id": "228723",
    },
)


def build_sme_review_sheet(
    *,
    publish_version_id: str,
    manifest: dict[str, Any],
    bundle_dir: Path,
    stage9_validation_path: Path | None = None,
    stage85_links_path: Path | None = None,
    output_dir: Path,
) -> dict[str, Any]:
    generated_at = datetime.now(UTC).isoformat()
    embeddings = _load_embeddings(bundle_dir)
    playbook_links = _load_playbook_runbook_links(stage85_links_path)
    validation = _load_validation(stage9_validation_path)
    retrieval_checks = [_score_prompt(prompt, embeddings) for prompt in DEMO_PROMPTS]
    link_stats = _link_stats(stage85_links_path)

    sheet = {
        "generated_at": generated_at,
        "publish_version_id": publish_version_id,
        "manifest_summary": {
            "record_counts": manifest.get("record_counts") or {},
            "link_counts_by_type": manifest.get("link_counts_by_type") or {},
            "containers": manifest.get("containers") or {},
        },
        "retrieval_coverage": {
            "embedding_record_counts": _embedding_counts(embeddings),
            "demo_prompt_checks": retrieval_checks,
        },
        "playbook_runbook_links": playbook_links,
        "validation_summary": validation,
        "relationship_link_quality": link_stats,
        "review_checklist": [
            "Confirm Prompt A playbooks route demo prompts 1-2 better than Prompt B where expected.",
            "Review all playbook_runbook edges before trusting orchestration.",
            "Treat context_runbook_shared_artifact links as hints only unless confidence is high.",
            "Spot-check operational_context and source_artifact RAG text for noise before enabling broad retrieval.",
            "Sign off publish_version_id before app points at this corpus.",
        ],
    }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    write_json(output_path / "sme_review_sheet.json", sheet)
    (output_path / "sme_review_sheet.md").write_text(_render_markdown(sheet), encoding="utf-8")
    return sheet


def _load_embeddings(bundle_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    primary = (
        "runbooks/embeddings.json",
        "playbooks_prompt_a/embeddings.json",
        "playbooks_prompt_b/embeddings.json",
        "operational_context/embeddings.json",
        "source_artifacts/embeddings.json",
    )
    legacy_rag = (
        "operational_context/rag_records.json",
        "source_artifacts/rag_records.json",
    )
    for relative in primary:
        path = bundle_dir / relative
        if path.exists():
            payload = read_json(path)
            if isinstance(payload, list):
                records.extend(row for row in payload if isinstance(row, dict))
    if any((bundle_dir / relative).exists() for relative in ("operational_context/embeddings.json", "source_artifacts/embeddings.json")):
        return records
    for relative in legacy_rag:
        path = bundle_dir / relative
        if path.exists():
            payload = read_json(path)
            if isinstance(payload, list):
                records.extend(row for row in payload if isinstance(row, dict))
    return records


def _embedding_counts(embeddings: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in embeddings:
        record_type = str(record.get("record_type") or "unknown")
        counts[record_type] = counts.get(record_type, 0) + 1
    return counts


def _score_prompt(prompt: dict[str, str], embeddings: list[dict[str, Any]]) -> dict[str, Any]:
    query_words = set(prompt["query"].lower().split())
    scored: list[dict[str, Any]] = []
    for record in embeddings:
        record_type = str(record.get("record_type") or "")
        if not record_type.startswith("playbook_prompt"):
            continue
        text = str(record.get("embedded_text") or record.get("retrieval_text") or "").lower()
        words = set(text.split())
        overlap = len(query_words & words) / max(len(query_words), 1)
        scored.append(
            {
                "record_type": record_type,
                "source_record_id": record.get("source_record_id"),
                "case_id": (record.get("filter_metadata") or {}).get("case_id"),
                "keyword_overlap": round(overlap, 3),
                "preview": str(record.get("embedded_text") or record.get("retrieval_text") or "")[:220],
            }
        )
    scored.sort(key=lambda item: item["keyword_overlap"], reverse=True)
    top = scored[:5]
    expected = prompt["expected_case_id"]
    top_case_ids = [str(item.get("case_id") or "") for item in top[:3]]
    return {
        "prompt_id": prompt["id"],
        "label": prompt["label"],
        "query": prompt["query"],
        "expected_case_id": expected,
        "top_matches": top,
        "expected_case_in_top_3": expected in top_case_ids,
    }


def _load_playbook_runbook_links(stage85_links_path: Path | None) -> list[dict[str, Any]]:
    if stage85_links_path is None or not stage85_links_path.exists():
        return []
    links = read_json(stage85_links_path)
    if not isinstance(links, list):
        return []
    rows = [link for link in links if isinstance(link, dict) and link.get("link_type") == "playbook_runbook"]
    rows.sort(key=lambda item: (str(item.get("source_record_id") or ""), int(item.get("link_rank") or 0)))
    return [
        {
            "source_record_id": row.get("source_record_id"),
            "target_record_id": row.get("target_record_id"),
            "link_confidence": row.get("link_confidence"),
            "link_rank": row.get("link_rank"),
            "extraction_mode": row.get("extraction_mode"),
        }
        for row in rows
    ]


def _load_validation(stage9_validation_path: Path | None) -> dict[str, Any]:
    if stage9_validation_path is None or not stage9_validation_path.exists():
        return {"status": "missing"}
    report = read_json(stage9_validation_path)
    if not isinstance(report, dict):
        return {"status": "invalid"}
    return {
        "status": "passed" if report.get("passed") else "failed",
        "error_count": (report.get("summary") or {}).get("error_count"),
        "warning_count": (report.get("summary") or {}).get("warning_count"),
        "warnings": report.get("warnings") or [],
    }


def _link_stats(stage85_links_path: Path | None) -> dict[str, Any]:
    if stage85_links_path is None or not stage85_links_path.exists():
        return {}
    links = read_json(stage85_links_path)
    if not isinstance(links, list):
        return {}
    by_type: dict[str, int] = {}
    by_confidence: dict[str, int] = {}
    needs_review = 0
    shared_inference = 0
    for link in links:
        if not isinstance(link, dict):
            continue
        link_type = str(link.get("link_type") or "unknown")
        by_type[link_type] = by_type.get(link_type, 0) + 1
        confidence = str(link.get("confidence") or link.get("link_confidence") or "unknown")
        by_confidence[confidence] = by_confidence.get(confidence, 0) + 1
        if link.get("needs_sme_review"):
            needs_review += 1
        if link.get("link_method") == "shared_artifact_inference":
            shared_inference += 1
    return {
        "link_count": len(links),
        "by_type": by_type,
        "by_confidence": by_confidence,
        "needs_sme_review_count": needs_review,
        "shared_artifact_inference_count": shared_inference,
    }


def _render_markdown(sheet: dict[str, Any]) -> str:
    lines = [
        "# SME Review Sheet",
        "",
        f"**Publish version:** `{sheet['publish_version_id']}`  ",
        f"**Generated:** {sheet['generated_at']}",
        "",
        "## Corpus counts",
        "",
    ]
    for key, value in (sheet.get("manifest_summary") or {}).get("record_counts", {}).items():
        lines.append(f"- **{key}:** {value}")
    lines.extend(["", "## Cosmos containers", ""])
    for dataset, container in (sheet.get("manifest_summary") or {}).get("containers", {}).items():
        lines.append(f"- **{dataset}:** `{container or '(not configured)'}`")
    lines.extend(["", "## Demo prompt retrieval checks", ""])
    for check in sheet.get("retrieval_coverage", {}).get("demo_prompt_checks", []):
        lines.append(f"### {check['label']} ({check['prompt_id']})")
        lines.append(f"- Expected case: `{check['expected_case_id']}`")
        lines.append(f"- Expected case in top 3: **{check['expected_case_in_top_3']}**")
        for match in check.get("top_matches", [])[:3]:
            lines.append(
                f"- `{match['source_record_id']}` case={match.get('case_id')} "
                f"overlap={match.get('keyword_overlap')} mode={match.get('record_type')}"
            )
        lines.append("")
    lines.extend(["## Playbook → runbook links (orchestration)", ""])
    for row in sheet.get("playbook_runbook_links", []):
        lines.append(
            f"- `{row['source_record_id']}` → `{row['target_record_id']}` "
            f"(rank {row.get('link_rank')}, {row.get('link_confidence')})"
        )
    validation = sheet.get("validation_summary") or {}
    lines.extend(
        [
            "",
            "## Validation summary",
            "",
            f"- Stage 9 status: **{validation.get('status', 'unknown')}**",
            f"- Errors: {validation.get('error_count', 'n/a')}",
            f"- Warnings: {validation.get('warning_count', 'n/a')}",
            "",
            "## Relationship link quality",
            "",
        ]
    )
    link_stats = sheet.get("relationship_link_quality") or {}
    if link_stats:
        lines.append(f"- Total links: {link_stats.get('link_count')}")
        lines.append(f"- Shared-artifact inferred: {link_stats.get('shared_artifact_inference_count')}")
        lines.append(f"- Needs SME review: {link_stats.get('needs_sme_review_count')}")
    lines.extend(["", "## SME sign-off checklist", ""])
    for item in sheet.get("review_checklist", []):
        lines.append(f"- [ ] {item}")
    lines.append("")
    return "\n".join(lines)
