from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_8.linked_runbook_surface import (
    render_linked_runbooks_html,
    render_linked_runbooks_markdown,
    runbook_audience_bucket,
)


def safe_playbook_review_filename(playbook_id: str, *, max_length: int = 80) -> str:
    raw = str(playbook_id or "playbook").strip()
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "_", raw).strip("._-") or "playbook"
    if len(slug) <= max_length:
        return f"{slug}.md"
    digest = __import__("hashlib").sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"pb_{digest}.md"


def write_playbook_review_markdown(
    playbook: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    artifact_index: dict[str, dict[str, Any]] | None = None,
    review_markdown_path: Path | None = None,
    repo_root: Path | None = None,
    asset_link_cache: dict[str, str] | None = None,
) -> str:
    lines: list[str] = [
        f"# {playbook.get('title') or 'Playbook'}",
        "",
        "## Playbook Header",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Playbook ID | `{playbook.get('playbook_id')}` |",
        f"| Case ID | `{playbook.get('case_id')}` |",
        f"| Extraction Mode | `{playbook.get('extraction_mode')}` |",
        f"| Confidence | `{playbook.get('confidence')}` |",
        f"| Validation Status | `{playbook.get('validation_status')}` |",
        "",
        "## Entry Symptoms",
        "",
        *_bullet_lines(playbook.get("observed_entry_symptoms") or []),
        "",
        "## Affected Systems",
        "",
        *_bullet_lines(playbook.get("affected_systems_or_components") or []),
        "",
        "## Nodes",
        "",
    ]
    cache = asset_link_cache if asset_link_cache is not None else {}
    root = repo_root or Path(__file__).resolve().parents[2]
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        lines.extend(_render_node_markdown(node, runbooks_by_id=runbooks_by_id))
        lines.extend(
            render_linked_runbooks_markdown(
                node,
                runbooks_by_id=runbooks_by_id,
                artifact_index=artifact_index,
                review_markdown_path=review_markdown_path,
                repo_root=root,
                asset_link_cache=cache,
            )
        )
        lines.extend(["---", ""])
    lines.extend(["## Branch Graph", "", *_render_branch_table(playbook), ""])
    return "\n".join(lines).rstrip() + "\n"


def write_playbook_review_html(
    playbook: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    artifact_index: dict[str, dict[str, Any]] | None = None,
    review_html_path: Path | None = None,
    repo_root: Path | None = None,
    asset_link_cache: dict[str, str] | None = None,
) -> str:
    title = html.escape(str(playbook.get("title") or "Playbook"))
    cache = asset_link_cache if asset_link_cache is not None else {}
    root = repo_root or Path(__file__).resolve().parents[2]
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>{title}</title>",
        "<style>",
        "body { font-family: Segoe UI, Arial, sans-serif; max-width: 960px; margin: 2rem auto; line-height: 1.5; }",
        "table { border-collapse: collapse; width: 100%; margin: 1rem 0; }",
        "th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; vertical-align: top; }",
        "figure { margin: 1rem 0; }",
        "img { max-width: 100%; height: auto; border: 1px solid #ddd; }",
        "figcaption { font-style: italic; color: #555; margin-top: 0.5rem; }",
        ".warn { color: #8a4b00; }",
        "details.linked-runbook { border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; margin: 1rem 0; }",
        "details.linked-runbook > summary { cursor: pointer; font-size: 1.05rem; margin-bottom: 0.5rem; }",
        "details.linked-runbook-group { border: 1px solid #e0e0e0; border-radius: 6px; padding: 0.75rem 1rem; margin: 1rem 0; background: #fafafa; }",
        "details.linked-runbook-group > summary { cursor: pointer; font-weight: 600; margin-bottom: 0.5rem; }",
        "details.linked-runbook-operator { border-left: 4px solid #2f6f4e; }",
        "details.linked-runbook-support { border-left: 4px solid #2f4f7f; }",
        ".missing-image { border: 1px dashed #bbb; padding: 1rem; background: #fafafa; }",
        ".missing-image-label { font-family: monospace; font-weight: 600; }",
        "hr { margin: 2rem 0; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>{title}</h1>",
        "<h2>Playbook Header</h2>",
        "<table>",
        f"<tr><th>Playbook ID</th><td>{html.escape(str(playbook.get('playbook_id') or ''))}</td></tr>",
        f"<tr><th>Case ID</th><td>{html.escape(str(playbook.get('case_id') or ''))}</td></tr>",
        f"<tr><th>Extraction Mode</th><td>{html.escape(str(playbook.get('extraction_mode') or ''))}</td></tr>",
        f"<tr><th>Confidence</th><td>{html.escape(str(playbook.get('confidence') or ''))}</td></tr>",
        f"<tr><th>Validation Status</th><td>{html.escape(str(playbook.get('validation_status') or ''))}</td></tr>",
        "</table>",
        "<h2>Entry Symptoms</h2>",
        "<ul>",
    ]
    for item in playbook.get("observed_entry_symptoms") or []:
        parts.append(f"<li>{html.escape(str(item))}</li>")
    parts.extend(["</ul>", "<h2>Nodes</h2>"])
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        parts.extend(_render_node_html(node, runbooks_by_id=runbooks_by_id))
        parts.extend(
            render_linked_runbooks_html(
                node,
                runbooks_by_id=runbooks_by_id,
                artifact_index=artifact_index,
                review_html_path=review_html_path,
                repo_root=root,
                asset_link_cache=cache,
            )
        )
        parts.append("<hr>")
    parts.extend(["<h2>Branch Graph</h2>", *_render_branch_table_html(playbook)])
    parts.extend(["</body>", "</html>"])
    return "\n".join(parts)


def write_playbook_review_files(
    playbook: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    review_dir: Path,
    artifact_index: dict[str, dict[str, Any]] | None = None,
    repo_root: Path | None = None,
) -> tuple[Path, Path]:
    review_dir.mkdir(parents=True, exist_ok=True)
    filename = safe_playbook_review_filename(str(playbook.get("playbook_id") or "playbook"))
    md_path = review_dir / filename
    html_path = review_dir / filename.replace(".md", ".html")
    cache: dict[str, str] = {}
    md_path.write_text(
        write_playbook_review_markdown(
            playbook,
            runbooks_by_id=runbooks_by_id,
            artifact_index=artifact_index,
            review_markdown_path=md_path,
            repo_root=repo_root,
            asset_link_cache=cache,
        ),
        encoding="utf-8",
    )
    html_path.write_text(
        write_playbook_review_html(
            playbook,
            runbooks_by_id=runbooks_by_id,
            artifact_index=artifact_index,
            review_html_path=html_path,
            repo_root=repo_root,
            asset_link_cache=cache,
        ),
        encoding="utf-8",
    )
    return md_path, html_path


def _render_node_markdown(node: dict[str, Any], *, runbooks_by_id: dict[str, dict[str, Any]]) -> list[str]:
    objective = str(node.get("purpose") or node.get("intent") or "").strip()
    node_type = str(node.get("node_type") or "")
    is_diagnostic = node_type in {"diagnostic_decision", "branching_condition"}
    is_validation = node_type == "validation_gate"
    lines = [
        f"### {node.get('node_order')} — {node.get('title')} (`{node.get('node_type')}`)",
        "",
        f"**Objective:** {objective}",
        "",
        f"**Why this check is next:** {node.get('diagnostic_reasoning') or ''}",
        "",
    ]
    if node.get("primary_action") or is_diagnostic or is_validation:
        action_label = "Validate" if is_validation else "Action"
        lines.extend(
            [
                f"**{action_label}:**",
                "",
                node.get("primary_action") or "Collect the required evidence and compare it with the conditions below.",
                "",
            ]
        )
        mapping = node.get("technical_field_mapping") or {}
        checks = mapping.get("suggested_database_checks") if isinstance(mapping, dict) else []
        if checks and is_diagnostic:
            lines.extend(["**Suggested database check:**", ""])
            for check in checks:
                lines.append(f"- **Database:** {check.get('database') or 'ontology-selected database'}")
                lines.append(f"  - **Model:** {check.get('entity') or 'ontology-selected model'}")
                fields = [
                    str(field.get("meaning") or field.get("name") or "")
                    for field in check.get("fields") or []
                    if isinstance(field, dict) and str(field.get("meaning") or field.get("name") or "").strip()
                ]
                lines.extend(f"  - **Inspect:** {field}" for field in fields)
                if check.get("correlation_keys"):
                    lines.append(f"  - **Relate by:** {', '.join(str(key) for key in check['correlation_keys'])}")
                if check.get("freshness_field"):
                    lines.append(f"  - **Freshness:** {check['freshness_field']}")
            lines.append("")
        status_labels = (("Success", "healthy"), ("Failure", "unhealthy"), ("Inconclusive", "inconclusive")) if is_validation else (("Healthy", "healthy"), ("Unhealthy", "unhealthy"), ("Inconclusive", "inconclusive"))
        for label, key in status_labels:
            lines.extend([f"**{label}:** {node.get(f'{key}_interpretation') or 'Required evidence is consistent with the expected state.'}", ""])
    if node_type == "procedure_reference":
        lines.extend(
            [
                "**Procedure Reference:**",
                "",
                f"- **Trigger condition:** {node.get('trigger_condition') or 'n/a'}",
                f"- **Selected procedure:** {_procedure_label(node.get('selected_procedure'))}",
                f"- **Selection rationale:** {node.get('selection_rationale') or 'n/a'}",
                f"- **Success confirmation:** {node.get('success_confirmation') or 'n/a'}",
                f"- **Failure boundary:** {node.get('failure_boundary') or 'n/a'}",
                "",
            ]
        )
        for label, key in (("Prerequisites", "prerequisites"), ("Safety checks", "safety_checks")):
            values = node.get(key) or []
            lines.extend([f"**{label}:**", "", *_bullet_lines(values), ""])
    elif node_type == "validation_gate":
        lines.extend(
            [
                "**Validation Gate:**",
                "",
                "**Validation checklist:**",
                "",
                *_bullet_lines(node.get("validation_checklist") or []),
                "",
                f"**Required evidence sources:** {', '.join(str(item) for item in node.get('required_evidence_sources') or [])}",
                "",
                f"**Stable-operation observation:** {node.get('stable_operation_observation') or 'n/a'}",
                "",
            ]
        )
    elif node_type == "escalation_gate":
        lines.extend(
            [
                "**Escalation Gate:**",
                "",
                f"- **Reason:** {node.get('escalation_reason') or 'n/a'}",
                f"- **Required next team:** {node.get('required_next_team') or 'n/a'}",
                "**Evidence package:**",
                "",
                *_bullet_lines(node.get("evidence_package") or []),
                "**Actions attempted:**",
                "",
                *_bullet_lines(node.get("actions_attempted") or []),
                "**Unresolved questions:**",
                "",
                *_bullet_lines(node.get("unresolved_questions") or []),
                "",
            ]
        )
    if is_diagnostic and node.get("evidence_required"):
        lines.extend(["**Evidence Required:**", "", *_bullet_lines(node.get("evidence_required") or []), ""])
    expects_capability = node.get("expects_capability") or []
    expects_surface = node.get("expects_surface") or []
    preferred_audience = node.get("preferred_audience") or []
    if expects_capability or expects_surface or preferred_audience:
        lines.extend(
            [
                f"**Expects capability:** {', '.join(str(item) for item in expects_capability) or 'n/a'}",
                f"**Expects surface:** {', '.join(str(item) for item in expects_surface) or 'n/a'}",
                f"**Preferred audience:** {', '.join(str(item) for item in preferred_audience) or 'n/a'}",
                "",
            ]
        )
    lines.extend(
        [
        "**Runbook Links:**",
        "",
        ]
    )
    links = node.get("runbook_links") or []
    if not links:
        lines.append("- No linked procedure; escalate if the required state cannot be confirmed using the available approved evidence sources.")
    for link in links:
        if not isinstance(link, dict):
            continue
        procedure_id = str(link.get("procedure_id") or "")
        runbook = runbooks_by_id.get(procedure_id, {})
        audience = runbook_audience_bucket(runbook) if runbook else "support"
        lines.append(
            f"- `{procedure_id}` ({link.get('link_confidence')}, {audience}, score={link.get('retrieval_combined_score', 'n/a')}, boosted={link.get('boosted_score', 'n/a')}) — {runbook.get('title') or link.get('link_rationale') or ''}"
        )
        gaps = link.get("match_gaps") or []
        if gaps:
            lines.extend([f"  - gaps: {'; '.join(str(item) for item in gaps)}"])
    procedures = node.get("evidence_collection_procedures") or []
    if procedures:
        lines.extend(["", "**Evidence Collection Procedures:**", ""])
        for procedure in procedures:
            if not isinstance(procedure, dict):
                continue
            lines.append(
                f"- `{procedure.get('procedure_id')}` — {procedure.get('title') or ''}"
                f" ({procedure.get('role_required') or 'role unspecified'}):"
                f" {procedure.get('purpose') or ''}"
            )
    source_evidence = node.get("source_evidence") or node.get("source_refs") or []
    if source_evidence:
        lines.extend(["", "**Source Evidence:**", ""])
        lines.extend(
            f"- {item.get('quote_or_summary') or item.get('page_ref') or item}"
            if isinstance(item, dict)
            else f"- {item}"
            for item in source_evidence
        )
    outcomes = node.get("decision_outcomes") or []
    if outcomes and not (is_diagnostic or is_validation):
        lines.extend(["", "**Decision Outcomes:**", ""])
        for outcome in outcomes:
            if not isinstance(outcome, dict):
                continue
            lines.append(
                f"- `{outcome.get('outcome_label')}`"
                f" (observer={outcome.get('observer') or 'n/a'};"
                f" tool={outcome.get('tool_or_view') or 'n/a'}):"
                f" {outcome.get('descriptor') or outcome.get('observable_signal') or ''}"
            )
    branches = node.get("branches") or []
    node_type = str(node.get("node_type") or "")
    if branches:
        lines.extend(["", "**Branches:**", ""])
        for branch in branches:
            if not isinstance(branch, dict):
                continue
            lines.append(
                f"- `{branch.get('outcome')}` → `{branch.get('next_node_id')}` when {branch.get('condition_label') or branch.get('condition_descriptor') or ''}"
            )
    elif node_type in {"procedure_reference", "escalation_gate", "exit"}:
        lines.extend(
            [
                "",
                "**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).",
                "",
            ]
        )
    lines.extend(["", "**Linked Runbook Procedures:**", ""])
    return lines


def _render_node_html(node: dict[str, Any], *, runbooks_by_id: dict[str, dict[str, Any]]) -> list[str]:
    title = html.escape(str(node.get("title") or "Node"))
    objective = str(node.get("purpose") or node.get("intent") or "").strip()
    node_type = str(node.get("node_type") or "")
    is_diagnostic = node_type in {"diagnostic_decision", "branching_condition"}
    is_validation = node_type == "validation_gate"
    parts = [
        f"<h3>{html.escape(str(node.get('node_order') or ''))} — {title} ({html.escape(str(node.get('node_type') or ''))})</h3>",
        f"<p><strong>Objective:</strong> {html.escape(objective)}</p>",
        f"<p><strong>Why this check is next:</strong> {html.escape(str(node.get('diagnostic_reasoning') or ''))}</p>",
    ]
    if node.get("primary_action") or is_diagnostic or is_validation:
        action_label = "Validate" if is_validation else "Action"
        status_labels = (("Success", "healthy"), ("Failure", "unhealthy"), ("Inconclusive", "inconclusive")) if is_validation else (("Healthy", "healthy"), ("Unhealthy", "unhealthy"), ("Inconclusive", "inconclusive"))
        parts.extend(
            [
                f"<p><strong>{action_label}:</strong> "
                + html.escape(str(node.get("primary_action") or "Collect the required evidence and compare it with the conditions below."))
                + "</p>",
            ]
        )
        parts.extend(f"<p><strong>{label}:</strong> {html.escape(str(node.get(f'{key}_interpretation') or 'Required evidence is consistent with the expected state.'))}</p>" for label, key in status_labels)
        mapping = node.get("technical_field_mapping") or {}
        checks = mapping.get("suggested_database_checks") if isinstance(mapping, dict) else []
        if checks and is_diagnostic:
            parts.extend(["<p><strong>Suggested database check:</strong></p>", "<ul>"])
            for check in checks:
                parts.append(f"<li><strong>Database:</strong> {html.escape(str(check.get('database') or 'ontology-selected database'))}")
                parts.append(f"<ul><li><strong>Model:</strong> {html.escape(str(check.get('entity') or 'ontology-selected model'))}</li>")
                for field in check.get("fields") or []:
                    if isinstance(field, dict):
                        parts.append(
                            f"<li><strong>Inspect:</strong> {html.escape(str(field.get('meaning') or field.get('name') or ''))}</li>"
                        )
                parts.append("</ul></li>")
            parts.append("</ul>")
    if node_type == "procedure_reference":
        parts.extend(
            [
                "<p><strong>Procedure Reference:</strong></p>",
                "<ul>",
                f"<li><strong>Trigger condition:</strong> {html.escape(str(node.get('trigger_condition') or 'n/a'))}</li>",
                f"<li><strong>Selected procedure:</strong> {html.escape(_procedure_label(node.get('selected_procedure')))}</li>",
                f"<li><strong>Selection rationale:</strong> {html.escape(str(node.get('selection_rationale') or 'n/a'))}</li>",
                f"<li><strong>Success confirmation:</strong> {html.escape(str(node.get('success_confirmation') or 'n/a'))}</li>",
                f"<li><strong>Failure boundary:</strong> {html.escape(str(node.get('failure_boundary') or 'n/a'))}</li>",
                "</ul>",
            ]
        )
        for label, key in (("Prerequisites", "prerequisites"), ("Safety checks", "safety_checks")):
            parts.extend([f"<p><strong>{label}:</strong></p>", "<ul>"])
            parts.extend(f"<li>{html.escape(str(item))}</li>" for item in node.get(key) or [])
            parts.append("</ul>")
    elif node_type == "validation_gate":
        parts.extend(
            [
                "<p><strong>Validation Gate:</strong></p>",
                "<p><strong>Validation checklist:</strong></p>",
                "<ul>",
                *[f"<li>{html.escape(str(item))}</li>" for item in node.get("validation_checklist") or []],
                "</ul>",
                f"<p><strong>Required evidence sources:</strong> {html.escape(', '.join(str(item) for item in node.get('required_evidence_sources') or []))}</p>",
                f"<p><strong>Stable-operation observation:</strong> {html.escape(str(node.get('stable_operation_observation') or 'n/a'))}</p>",
            ]
        )
    elif node_type == "escalation_gate":
        parts.extend(
            [
                "<p><strong>Escalation Gate:</strong></p>",
                "<ul>",
                f"<li><strong>Reason:</strong> {html.escape(str(node.get('escalation_reason') or 'n/a'))}</li>",
                f"<li><strong>Required next team:</strong> {html.escape(str(node.get('required_next_team') or 'n/a'))}</li>",
                "</ul>",
            ]
        )
        for label, key in (
            ("Evidence package", "evidence_package"),
            ("Actions attempted", "actions_attempted"),
            ("Unresolved questions", "unresolved_questions"),
        ):
            parts.extend([f"<p><strong>{label}:</strong></p>", "<ul>"])
            parts.extend(f"<li>{html.escape(str(item))}</li>" for item in node.get(key) or [])
            parts.append("</ul>")
    if is_diagnostic and node.get("evidence_required"):
        parts.extend(["<p><strong>Evidence Required:</strong></p>", "<ul>"])
        parts.extend(f"<li>{html.escape(str(value))}</li>" for value in node.get("evidence_required") or [])
        parts.append("</ul>")
    expects_capability = node.get("expects_capability") or []
    expects_surface = node.get("expects_surface") or []
    preferred_audience = node.get("preferred_audience") or []
    if expects_capability or expects_surface or preferred_audience:
        parts.extend(
            [
                f"<p><strong>Expects capability:</strong> {html.escape(', '.join(str(item) for item in expects_capability) or 'n/a')}</p>",
                f"<p><strong>Expects surface:</strong> {html.escape(', '.join(str(item) for item in expects_surface) or 'n/a')}</p>",
                f"<p><strong>Preferred audience:</strong> {html.escape(', '.join(str(item) for item in preferred_audience) or 'n/a')}</p>",
            ]
        )
    parts.extend(
        [
            "<p><strong>Runbook Links:</strong></p>",
            "<ul>",
        ]
    )
    links = node.get("runbook_links") or []
    if not links:
        parts.append('<li>No linked procedure; escalate if the required state cannot be confirmed using the available approved evidence sources.</li>')
    for link in links:
        if not isinstance(link, dict):
            continue
        procedure_id = str(link.get("procedure_id") or "")
        runbook = runbooks_by_id.get(procedure_id, {})
        confidence = html.escape(str(link.get("link_confidence") or ""))
        audience = html.escape(runbook_audience_bucket(runbook) if runbook else "support")
        label = html.escape(str(runbook.get("title") or link.get("link_rationale") or ""))
        css = ' class="warn"' if confidence == "low" else ""
        score = link.get("retrieval_combined_score")
        score_label = f", score={score}" if score is not None else ""
        parts.append(
            f"<li{css}><code>{html.escape(procedure_id)}</code> ({confidence}, {audience}{score_label}) — {label}</li>"
        )
    parts.append("</ul>")
    procedures = node.get("evidence_collection_procedures") or []
    if procedures:
        parts.extend(["<p><strong>Evidence Collection Procedures:</strong></p>", "<ul>"])
        for procedure in procedures:
            if not isinstance(procedure, dict):
                continue
            parts.append(
                f"<li><code>{html.escape(str(procedure.get('procedure_id') or ''))}</code>"
                f" — {html.escape(str(procedure.get('title') or ''))}"
                f" ({html.escape(str(procedure.get('role_required') or 'role unspecified'))}): "
                f"{html.escape(str(procedure.get('purpose') or ''))}</li>"
            )
        parts.append("</ul>")
    source_evidence = node.get("source_evidence") or node.get("source_refs") or []
    if source_evidence:
        parts.extend(["<p><strong>Source Evidence:</strong></p>", "<ul>"])
        for item in source_evidence:
            value = item.get("quote_or_summary") or item.get("page_ref") or item if isinstance(item, dict) else item
            parts.append(f"<li>{html.escape(str(value))}</li>")
        parts.append("</ul>")
    parts.append("<p><strong>Linked Runbook Procedures:</strong></p>")
    outcomes = node.get("decision_outcomes") or []
    if outcomes and not (is_diagnostic or is_validation):
        parts.extend(["<p><strong>Decision Outcomes:</strong></p>", "<ul>"])
        for outcome in outcomes:
            if not isinstance(outcome, dict):
                continue
            parts.append(
                f"<li><code>{html.escape(str(outcome.get('outcome_label') or ''))}</code>"
                f" (observer={html.escape(str(outcome.get('observer') or 'n/a'))};"
                f" tool={html.escape(str(outcome.get('tool_or_view') or 'n/a'))}): "
                f"{html.escape(str(outcome.get('descriptor') or outcome.get('observable_signal') or ''))}</li>"
            )
        parts.append("</ul>")
    branches = node.get("branches") or []
    node_type = str(node.get("node_type") or "")
    if branches:
        parts.extend(["<p><strong>Branches:</strong></p>", "<ul>"])
        for branch in branches:
            if not isinstance(branch, dict):
                continue
            parts.append(
                f"<li><code>{html.escape(str(branch.get('outcome') or ''))}</code> → "
                f"<code>{html.escape(str(branch.get('next_node_id') or ''))}</code> when "
                f"{html.escape(str(branch.get('condition_label') or branch.get('condition_descriptor') or ''))}</li>"
            )
        parts.append("</ul>")
    elif node_type in {"procedure_reference", "escalation_gate", "exit"}:
        parts.append(
            "<p><strong>Branches:</strong> no branch outcomes — proceed / escalate (procedure or escalation node).</p>"
        )
    return parts


def _render_branch_table(playbook: dict[str, Any]) -> list[str]:
    rows = _branch_rows(playbook)
    if not rows:
        return ["No branches emitted."]
    lines = [
        "| From Node | Outcome | Condition | Next Node |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| `{row[0]}` | `{row[1]}` | {row[2]} | `{row[3]}` |")
    return lines


def _render_branch_table_html(playbook: dict[str, Any]) -> list[str]:
    rows = _branch_rows(playbook)
    if not rows:
        return ["<p>No branches emitted.</p>"]
    parts = [
        "<table>",
        "<tr><th>From Node</th><th>Outcome</th><th>Condition</th><th>Next Node</th></tr>",
    ]
    for row in rows:
        parts.append(
            f"<tr><td><code>{html.escape(row[0])}</code></td>"
            f"<td><code>{html.escape(row[1])}</code></td>"
            f"<td>{html.escape(row[2])}</td>"
            f"<td><code>{html.escape(row[3])}</code></td></tr>"
        )
    parts.append("</table>")
    return parts


def _branch_rows(playbook: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    seen: set[tuple[str, str, str, str]] = set()

    def _add(from_id: str, outcome: str, condition: str, next_id: str) -> None:
        from_id = str(from_id or "").strip()
        if not from_id:
            return
        key = (from_id, outcome, next_id, condition.strip().lower())
        if key in seen:
            return
        seen.add(key)
        rows.append((from_id, outcome, condition, next_id))

    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("node_id") or "")
        for branch in node.get("branches") or []:
            if not isinstance(branch, dict):
                continue
            _add(
                node_id,
                str(branch.get("outcome") or ""),
                str(branch.get("condition_label") or branch.get("condition_descriptor") or ""),
                str(branch.get("next_node_id") or ""),
            )
    for branch in playbook.get("branches") or []:
        if not isinstance(branch, dict):
            continue
        _add(
            str(branch.get("from_node_id") or ""),
            str(branch.get("outcome") or ""),
            str(branch.get("condition_label") or branch.get("condition_descriptor") or ""),
            str(branch.get("next_node_id") or ""),
        )
    return rows


def _unresolved_nodes(playbook: dict[str, Any]) -> list[str]:
    unresolved: list[str] = []
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        links = node.get("runbook_links") or []
        if not links:
            unresolved.append(f"{node.get('node_id')}: unresolved")
            continue
        for link in links:
            if not isinstance(link, dict):
                continue
            if str(link.get("link_confidence") or "") in {"low", "unresolved"}:
                unresolved.append(
                    f"{node.get('node_id')}: {link.get('procedure_id') or 'unresolved'} ({link.get('link_confidence')})"
                )
    return unresolved


def _bullet_lines(values: list[Any]) -> list[str]:
    return [f"- {value}" for value in values if str(value).strip()]


def _procedure_label(value: Any) -> str:
    if not isinstance(value, dict):
        return str(value or "unresolved")
    procedure_id = str(value.get("procedure_id") or "").strip()
    title = str(value.get("title") or "").strip()
    if procedure_id and title:
        return f"{title} (`{procedure_id}`)"
    return procedure_id or title or "unresolved"
