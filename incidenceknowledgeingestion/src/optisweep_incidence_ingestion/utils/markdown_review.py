"""Human review Markdown writers for incident ingestion stage outputs."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any
import os


def write_stage3_review_markdown(
    path: str | Path,
    enriched_artifacts: list[dict[str, Any]],
    report: dict[str, Any],
) -> None:
    output_path = Path(path)
    lines: list[str] = []
    case_id = _first_value(enriched_artifacts, "source_case_id") or "unknown"
    role_counts = Counter(str(item.get("evidence_role") or "unknown") for item in enriched_artifacts)
    quality_counts = Counter(str(item.get("ocr_quality") or "unknown") for item in enriched_artifacts)
    uncertain = [
        item
        for item in enriched_artifacts
        if item.get("review_uncertainty") or item.get("quality_notes") or item.get("validation_status") != "needs_sme_review"
    ]

    lines.extend(
        [
            f"# Stage 3 Artifact Enrichment Review - Case {case_id}",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | --- |",
            f"| Artifacts | {len(enriched_artifacts)} |",
            f"| Enriched | {report.get('enriched_artifact_count', len(enriched_artifacts))} |",
            f"| Failed | {report.get('failed_artifact_count', 0)} |",
            f"| Validation errors | {len(report.get('validation_errors') or [])} |",
            f"| Warnings | {len(report.get('warnings') or [])} |",
            f"| Artifacts with uncertainty or quality notes | {len(uncertain)} |",
            "",
            "## Counts",
            "",
            "### Evidence Roles",
            "",
            _counter_table(role_counts, "Role"),
            "",
            "### OCR Quality",
            "",
            _counter_table(quality_counts, "Quality"),
            "",
        ]
    )

    if report.get("validation_errors"):
        lines.extend(["## Validation Errors", "", *_bullet_lines(report.get("validation_errors") or []), ""])
    if report.get("warnings"):
        lines.extend(["## Warnings", "", *_bullet_lines(report.get("warnings") or []), ""])

    lines.extend(
        [
            "## Artifact Index",
            "",
            "| Page | Artifact | Role | OCR | Summary | Review flags |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for artifact in sorted(enriched_artifacts, key=lambda item: (item.get("page_number") or 0, item.get("artifact_id") or "")):
        flags = _artifact_review_flags(artifact)
        lines.append(
            "| "
            + " | ".join(
                [
                    _md_cell(artifact.get("page_number")),
                    _md_cell(artifact.get("artifact_id")),
                    _md_cell(artifact.get("evidence_role")),
                    _md_cell(artifact.get("ocr_quality")),
                    _md_cell(_truncate(artifact.get("short_description") or artifact.get("summary") or "", 180)),
                    _md_cell(", ".join(flags) if flags else ""),
                ]
            )
            + " |"
        )
    lines.append("")

    lines.extend(["## Artifact Details", ""])
    for artifact in sorted(enriched_artifacts, key=lambda item: (item.get("page_number") or 0, item.get("artifact_id") or "")):
        lines.extend(_artifact_detail_lines(artifact, output_path.parent))

    _write_markdown(output_path, lines)


def write_stage4_review_markdown(
    path: str | Path,
    canonical_record: dict[str, Any],
    canonical_report: dict[str, Any],
    timeline_events: dict[str, Any],
    timeline_report: dict[str, Any],
) -> None:
    output_path = Path(path)
    events = timeline_events.get("events") or []
    kpi = canonical_record.get("kpi_tracking") if isinstance(canonical_record.get("kpi_tracking"), dict) else {}
    lines: list[str] = [
        f"# Stage 4 Incident Review - Case {canonical_record.get('source_case_id') or 'unknown'}",
        "",
        "## Canonical Summary",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Incident | {_md_cell(canonical_record.get('title'))} |",
        f"| Status | {_md_cell(canonical_record.get('status'))} |",
        f"| Validation status | {_md_cell(canonical_record.get('validation_status'))} |",
        f"| Site | {_md_cell(_site_label(canonical_record.get('site')))} |",
        f"| Reported at | {_md_cell(canonical_record.get('reported_at'))} |",
        f"| Resolved at | {_md_cell(canonical_record.get('resolved_at'))} |",
        f"| Resolution time | {_md_cell(canonical_record.get('resolution_time'))} |",
        f"| Downtime minutes | {_md_cell(canonical_record.get('downtime_minutes'))} |",
        f"| KPI confidence | {_md_cell(canonical_record.get('kpi_confidence') or kpi.get('confidence'))} |",
        f"| Timeline events | {len(events)} |",
        f"| Canonical validation errors | {len(canonical_report.get('validation_errors') or [])} |",
        f"| Timeline validation errors | {len(timeline_report.get('validation_errors') or [])} |",
        "",
    ]

    lines.extend(
        [
            "## KPI Tracking",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Start | {_md_cell(kpi.get('tracking_start_at'))} |",
            f"| End | {_md_cell(kpi.get('tracking_end_at'))} |",
            f"| Elapsed minutes | {_md_cell(kpi.get('elapsed_minutes'))} |",
            f"| Basis | {_md_cell(kpi.get('basis'))} |",
            f"| Confidence | {_md_cell(kpi.get('confidence'))} |",
            "",
        ]
    )
    if kpi.get("notes"):
        lines.extend(["### KPI Notes", "", *_bullet_lines(kpi.get("notes") or []), ""])

    lines.extend(
        [
            "## Incident Narrative",
            "",
            f"**Description:** {_md_text(canonical_record.get('incident_description'))}",
            "",
            f"**Operational impact:** {_md_text(canonical_record.get('customer_operational_impact'))}",
            "",
            f"**Resolution:** {_md_text(canonical_record.get('what_resolved_it'))}",
            "",
        ]
    )
    _extend_named_list(lines, "Symptoms", canonical_record.get("symptoms") or [])
    _extend_named_list(lines, "Systems Involved", canonical_record.get("systems_involved") or [])
    _extend_named_list(lines, "Follow Up Required", canonical_record.get("follow_up_required") or [])

    if canonical_report.get("validation_errors") or timeline_report.get("validation_errors"):
        lines.extend(["## Validation Errors", ""])
        lines.extend(_bullet_lines(canonical_report.get("validation_errors") or []))
        lines.extend(_bullet_lines(timeline_report.get("validation_errors") or []))
        lines.append("")
    if canonical_report.get("warnings") or timeline_report.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend(_bullet_lines(canonical_report.get("warnings") or []))
        lines.extend(_bullet_lines(timeline_report.get("warnings") or []))
        lines.append("")

    lines.extend(
        [
            "## Timeline",
            "",
            "| # | Timestamp | Type | Summary | Systems | Confidence | Source |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for event in events:
        source_refs = event.get("source_refs") or []
        source_text = "; ".join(_source_ref_label(ref) for ref in source_refs[:3])
        lines.append(
            "| "
            + " | ".join(
                [
                    _md_cell(event.get("event_order")),
                    _md_cell(event.get("timestamp") or event.get("timestamp_status")),
                    _md_cell(event.get("event_type")),
                    _md_cell(_truncate(event.get("summary") or "", 200)),
                    _md_cell(", ".join(event.get("systems") or [])),
                    _md_cell(event.get("confidence")),
                    _md_cell(source_text),
                ]
            )
            + " |"
        )
    lines.append("")

    uncertain_events = [event for event in events if event.get("uncertainties")]
    if uncertain_events:
        lines.extend(["## Timeline Review Notes", ""])
        for event in uncertain_events[:20]:
            lines.append(f"### Event {event.get('event_order')}: {_md_text(event.get('summary'))}")
            lines.extend(_bullet_lines(event.get("uncertainties") or []))
            lines.append("")
        if len(uncertain_events) > 20:
            lines.append(f"_Additional events with uncertainties omitted from Markdown: {len(uncertain_events) - 20}._")
            lines.append("")

    _write_markdown(output_path, lines)


def write_stage5_runbook_candidate_review_markdown(
    path: str | Path,
    candidates: list[dict[str, Any]],
    report: dict[str, Any],
    canonical_record: dict[str, Any],
) -> None:
    output_path = Path(path)
    type_counts = Counter(str(item.get("likely_procedure_type") or "unknown") for item in candidates)
    role_counts = Counter(str(item.get("likely_role_required") or "unknown") for item in candidates)
    lines: list[str] = [
        f"# Stage 5 Runbook Candidate Review - Case {canonical_record.get('source_case_id') or report.get('source_case_id') or 'unknown'}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Candidates | {len(candidates)} |",
        f"| Validation errors | {len(report.get('validation_errors') or [])} |",
        f"| Warnings | {len(report.get('warnings') or [])} |",
        f"| Dropped candidates | {report.get('dropped_candidate_count', 0)} |",
        f"| Deduped candidates | {report.get('deduped_candidate_count', 0)} |",
        f"| Candidates with artifacts | {report.get('candidates_with_artifacts', 0)} |",
        f"| Candidates with events | {report.get('candidates_with_events', 0)} |",
        "",
        "## Counts",
        "",
        "### Procedure Types",
        "",
        _counter_table(type_counts, "Type"),
        "",
        "### Roles",
        "",
        _counter_table(role_counts, "Role"),
        "",
    ]
    if report.get("validation_errors"):
        lines.extend(["## Validation Errors", "", *_bullet_lines(report.get("validation_errors") or []), ""])
    if report.get("warnings"):
        lines.extend(["## Warnings", "", *_bullet_lines(report.get("warnings") or []), ""])

    lines.extend(
        [
            "## Candidate Index",
            "",
            "| Candidate | Type | Role | Confidence | Artifacts | Events | Summary |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for candidate in candidates:
        lines.append(
            "| "
            + " | ".join(
                [
                    _md_cell(candidate.get("candidate_id")),
                    _md_cell(candidate.get("likely_procedure_type")),
                    _md_cell(candidate.get("likely_role_required")),
                    _md_cell(candidate.get("confidence")),
                    _md_cell(", ".join(candidate.get("related_artifact_ids") or [])),
                    _md_cell(", ".join(candidate.get("related_event_ids") or [])),
                    _md_cell(_truncate(candidate.get("summary") or "", 180)),
                ]
            )
            + " |"
        )
    lines.append("")

    lines.extend(["## Candidate Details", ""])
    for candidate in candidates:
        lines.extend(
            [
                f"### {_md_text(candidate.get('title') or candidate.get('candidate_id'))}",
                "",
                "| Field | Value |",
                "| --- | --- |",
                f"| Candidate ID | {_md_cell(candidate.get('candidate_id'))} |",
                f"| Goal | {_md_cell(candidate.get('candidate_goal'))} |",
                f"| Type | {_md_cell(candidate.get('likely_procedure_type'))} |",
                f"| Role | {_md_cell(candidate.get('likely_role_required'))} |",
                f"| Confidence | {_md_cell(candidate.get('confidence'))} |",
                f"| Status | {_md_cell(candidate.get('candidate_status'))} |",
                "",
                f"**Summary:** {_md_text(candidate.get('summary'))}",
                "",
            ]
        )
        _extend_named_list(lines, "Rough Steps", candidate.get("rough_steps") or [], heading_level=4)
        if candidate.get("expected_result"):
            lines.extend([f"**Expected result:** {_md_text(candidate.get('expected_result'))}", ""])
        _extend_named_list(lines, "Failure Or Escalation Notes", candidate.get("failure_or_escalation_notes") or [], heading_level=4)
        _extend_named_list(lines, "Access Or Tools Needed", candidate.get("access_or_tools_needed") or [], heading_level=4)
        _extend_named_list(lines, "Extraction Notes", candidate.get("extraction_notes") or [], heading_level=4)

    _write_markdown(output_path, lines)


def write_stage5_playbook_candidate_review_markdown(
    path: str | Path,
    candidates: list[dict[str, Any]],
    report: dict[str, Any],
    canonical_record: dict[str, Any],
) -> None:
    output_path = Path(path)
    confidence_counts = Counter(str(item.get("confidence") or "unknown") for item in candidates)
    lines: list[str] = [
        f"# Stage 5 Playbook Candidate Review - Case {canonical_record.get('source_case_id') or report.get('source_case_id') or 'unknown'}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Playbook candidates | {len(candidates)} |",
        f"| Nodes | {report.get('nodes_count', 0)} |",
        f"| Nodes missing runbook placeholder | {report.get('nodes_missing_runbook_placeholder', 0)} |",
        f"| Validation errors | {len(report.get('validation_errors') or [])} |",
        f"| Warnings | {len(report.get('warnings') or [])} |",
        f"| Dropped candidates | {report.get('dropped_candidate_count', 0)} |",
        f"| Deduped candidates | {report.get('deduped_candidate_count', 0)} |",
        f"| Candidates with artifacts | {report.get('candidates_with_artifacts', 0)} |",
        f"| Candidates with events | {report.get('candidates_with_events', 0)} |",
        "",
        "## Confidence",
        "",
        _counter_table(confidence_counts, "Confidence"),
        "",
    ]
    if report.get("validation_errors"):
        lines.extend(["## Validation Errors", "", *_bullet_lines(report.get("validation_errors") or []), ""])
    if report.get("warnings"):
        lines.extend(["## Warnings", "", *_bullet_lines(report.get("warnings") or []), ""])

    lines.extend(
        [
            "## Candidate Index",
            "",
            "| Candidate | Confidence | Nodes | Events | Summary |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for candidate in candidates:
        summary = candidate.get("user_facing_summary") or candidate.get("summary") or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    _md_cell(candidate.get("playbook_candidate_id")),
                    _md_cell(candidate.get("confidence")),
                    _md_cell(len(candidate.get("nodes") or [])),
                    _md_cell(", ".join(candidate.get("related_event_ids") or [])),
                    _md_cell(_truncate(summary, 180)),
                ]
            )
            + " |"
        )
    lines.append("")

    lines.extend(["## Candidate Details", ""])
    for candidate in candidates:
        summary = candidate.get("user_facing_summary") or candidate.get("summary") or ""
        lines.extend(
            [
                f"### {_md_text(candidate.get('title') or candidate.get('playbook_candidate_id'))}",
                "",
                "| Field | Value |",
                "| --- | --- |",
                f"| Candidate ID | {_md_cell(candidate.get('playbook_candidate_id'))} |",
                f"| Goal | {_md_cell(candidate.get('playbook_goal'))} |",
                f"| Entry symptoms | {_md_cell('; '.join(candidate.get('observed_entry_symptoms') or []))} |",
                f"| Tentative internal patterns | {_md_cell('; '.join(candidate.get('tentative_internal_patterns') or []))} |",
                f"| Affected systems/components | {_md_cell('; '.join(candidate.get('affected_systems_or_components') or []))} |",
                f"| Roles | {_md_cell(', '.join(candidate.get('likely_roles') or []))} |",
                f"| Confidence | {_md_cell(candidate.get('confidence'))} |",
                f"| Confidence reason | {_md_cell(candidate.get('confidence_reason'))} |",
                "",
                f"**Summary:** {_md_text(summary)}",
                "",
            ]
        )
        _extend_named_list(lines, "Support User Language Examples", candidate.get("support_user_language_examples") or [], heading_level=4)
        _extend_named_list(lines, "Negative Or Absent Signals", candidate.get("negative_or_absent_signals") or [], heading_level=4)
        nodes = sorted(candidate.get("nodes") or [], key=lambda node: node.get("node_order") or 0)
        if nodes:
            lines.extend(
                [
                    "#### Nodes",
                    "",
                    "| # | Type | Title | Intent | Runbook placeholder | Source-supported description |",
                    "| --- | --- | --- | --- | --- | --- |",
                ]
            )
            for node in nodes:
                intent = node.get("intent") or node.get("goal") or ""
                runbook_placeholder = node.get("runbook_placeholder") or node.get("needed_runbook_capability") or ""
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            _md_cell(node.get("node_order")),
                            _md_cell(node.get("node_type")),
                            _md_cell(node.get("title")),
                            _md_cell(intent),
                            _md_cell(runbook_placeholder),
                            _md_cell(_truncate(node.get("source_supported_description") or "", 180)),
                        ]
                    )
                    + " |"
                )
            lines.append("")
        _extend_named_list(lines, "Extraction Notes", candidate.get("extraction_notes") or [], heading_level=4)

    _write_markdown(output_path, lines)


def _artifact_detail_lines(artifact: dict[str, Any], markdown_dir: Path) -> list[str]:
    artifact_id = str(artifact.get("artifact_id") or "unknown_artifact")
    lines = [
        f"### {artifact_id}",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Page | {_md_cell(artifact.get('page_number'))} |",
        f"| Image type | {_md_cell(artifact.get('image_type'))} |",
        f"| Evidence role | {_md_cell(artifact.get('evidence_role'))} |",
        f"| OCR quality | {_md_cell(artifact.get('ocr_quality'))} |",
        f"| Duplicate group | {_md_cell(artifact.get('duplicate_group_id'))} |",
        f"| Validation status | {_md_cell(artifact.get('validation_status'))} |",
        "",
    ]
    image_link = _relative_link(markdown_dir, artifact.get("storage_path"))
    if image_link:
        lines.extend([f"![{_md_alt(artifact_id)}]({image_link})", ""])
    lines.extend(
        [
            f"**Short description:** {_md_text(artifact.get('short_description'))}",
            "",
            f"**Detailed description:** {_md_text(artifact.get('detailed_description'))}",
            "",
        ]
    )
    _extend_named_list(lines, "What To Look At", artifact.get("what_to_look_at") or [], heading_level=4)
    _extend_named_list(
        lines,
        "Source Supported Claims",
        [_claim_text(claim) for claim in artifact.get("source_supported_claims") or []],
        heading_level=4,
    )
    _extend_named_list(lines, "Review Uncertainty", artifact.get("review_uncertainty") or [], heading_level=4)
    _extend_named_list(lines, "Quality Notes", artifact.get("quality_notes") or [], heading_level=4)
    return lines


def _artifact_review_flags(artifact: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    if artifact.get("review_uncertainty"):
        flags.append("uncertainty")
    if artifact.get("quality_notes"):
        flags.append("quality")
    if artifact.get("ocr_quality") in {"low", "garbled", "missing"}:
        flags.append(f"ocr:{artifact.get('ocr_quality')}")
    if artifact.get("duplicate_role") and artifact.get("duplicate_role") != "primary":
        flags.append(f"duplicate:{artifact.get('duplicate_role')}")
    return flags


def _write_markdown(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines).rstrip() + "\n"
    path.write_text(text, encoding="utf-8")


def _counter_table(counter: Counter[str], label: str) -> str:
    lines = [f"| {label} | Count |", "| --- | --- |"]
    for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {_md_cell(key)} | {count} |")
    return "\n".join(lines)


def _extend_named_list(lines: list[str], title: str, values: list[Any], heading_level: int = 2) -> None:
    if not values:
        return
    heading = "#" * max(1, min(6, heading_level))
    lines.extend([f"{heading} {title}", ""])
    lines.extend(_bullet_lines(values))
    lines.append("")


def _bullet_lines(values: list[Any]) -> list[str]:
    return [f"- {_md_text(value)}" for value in values if _md_text(value)]


def _claim_text(claim: Any) -> str:
    if not isinstance(claim, dict):
        return str(claim)
    claim_text = claim.get("claim") or claim.get("summary") or claim.get("text") or ""
    support = claim.get("support_type") or claim.get("confidence") or ""
    if support:
        return f"{claim_text} ({support})"
    return str(claim_text)


def _source_ref_label(ref: Any) -> str:
    if not isinstance(ref, dict):
        return str(ref)
    parts = [str(ref.get("page_ref") or "").strip(), str(ref.get("artifact_id") or "").strip(), str(ref.get("chunk_id") or "").strip()]
    return " / ".join(part for part in parts if part)


def _site_label(site: Any) -> str:
    if isinstance(site, dict):
        return str(site.get("primary_label") or site.get("observed_location_text") or "")
    return str(site or "")


def _relative_link(markdown_dir: Path, raw_path: Any) -> str:
    if not raw_path:
        return ""
    candidate = Path(str(raw_path))
    if not candidate.is_absolute():
        candidate = (Path.cwd() / candidate).resolve()
    try:
        relative = os.path.relpath(candidate, markdown_dir.resolve())
    except ValueError:
        relative = str(candidate)
    return relative.replace("\\", "/").replace(" ", "%20")


def _first_value(items: list[dict[str, Any]], key: str) -> Any:
    for item in items:
        if item.get(key):
            return item.get(key)
    return None


def _md_cell(value: Any) -> str:
    text = _md_text(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def _md_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(_md_text(item) for item in value)
    if isinstance(value, dict):
        return ", ".join(f"{key}: {_md_text(item)}" for key, item in value.items())
    return str(value).strip()


def _md_alt(value: Any) -> str:
    return _md_text(value).replace("[", "(").replace("]", ")")


def _truncate(text: str, limit: int) -> str:
    stripped = str(text or "").strip()
    if len(stripped) <= limit:
        return stripped
    return stripped[: max(0, limit - 3)].rstrip() + "..."
