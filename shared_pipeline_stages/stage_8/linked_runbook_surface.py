from __future__ import annotations

import html
from copy import deepcopy
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_7.artifact_images import collect_image_refs, render_image_html, render_image_markdown


def attach_linked_runbooks(
    node: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    linked: list[dict[str, Any]] = []
    for procedure_id in node.get("resolved_runbook_ids") or []:
        runbook = runbooks_by_id.get(str(procedure_id))
        if not isinstance(runbook, dict):
            continue
        linked.append(deepcopy(runbook))
    node["linked_runbooks"] = linked
    return linked


def render_linked_runbooks_markdown(
    node: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    artifact_index: dict[str, dict[str, Any]] | None,
    review_markdown_path: Path | None,
    repo_root: Path,
    asset_link_cache: dict[str, str],
) -> list[str]:
    lines: list[str] = []
    runbooks = node.get("linked_runbooks") or []
    if not runbooks:
        for procedure_id in node.get("resolved_runbook_ids") or []:
            runbook = runbooks_by_id.get(str(procedure_id))
            if isinstance(runbook, dict):
                runbooks.append(runbook)
    if not runbooks:
        return ["*No linked runbook content available.*", ""]
    for runbook in runbooks:
        if not isinstance(runbook, dict):
            continue
        lines.extend(
            _render_single_runbook_markdown(
                runbook,
                artifact_index=artifact_index,
                review_markdown_path=review_markdown_path,
                repo_root=repo_root,
                asset_link_cache=asset_link_cache,
            )
        )
    return lines


def render_linked_runbooks_html(
    node: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    artifact_index: dict[str, dict[str, Any]] | None,
    review_html_path: Path | None,
    repo_root: Path,
    asset_link_cache: dict[str, str],
) -> list[str]:
    parts: list[str] = []
    runbooks = node.get("linked_runbooks") or []
    if not runbooks:
        for procedure_id in node.get("resolved_runbook_ids") or []:
            runbook = runbooks_by_id.get(str(procedure_id))
            if isinstance(runbook, dict):
                runbooks.append(runbook)
    if not runbooks:
        return ["<p><em>No linked runbook content available.</em></p>"]
    for runbook in runbooks:
        if not isinstance(runbook, dict):
            continue
        procedure_id = str(runbook.get("procedure_id") or "")
        parts.extend(
            _render_single_runbook_html(
                runbook,
                node=node,
                artifact_index=artifact_index,
                review_html_path=review_html_path,
                repo_root=repo_root,
                asset_link_cache=asset_link_cache,
            )
        )
    return parts


def _render_single_runbook_markdown(
    runbook: dict[str, Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None,
    review_markdown_path: Path | None,
    repo_root: Path,
    asset_link_cache: dict[str, str],
) -> list[str]:
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    lines = [
        f"#### Runbook: {runbook.get('title') or 'Untitled'}",
        "",
        f"- **Procedure ID:** `{runbook.get('procedure_id')}`",
        f"- **Procedure Type:** `{runbook.get('procedure_type')}`",
        f"- **Role:** `{runbook.get('role_required')}`",
        f"- **Merge Status:** `{metadata.get('merge_status')}`",
        "",
        "**Summary:**",
        str(runbook.get("summary") or ""),
        "",
        "**When To Use:**",
        str(runbook.get("when_to_use") or ""),
        "",
    ]
    if runbook.get("safety_notes"):
        lines.extend(["**Safety Notes:**", "", *_bullet_lines(runbook.get("safety_notes") or []), ""])
    source_id = str(metadata.get("source_id") or "")
    source_type = str(metadata.get("source_type") or runbook.get("source_type") or "")
    if source_id or source_type:
        lines.extend([f"- **Source:** `{source_type}` / `{source_id}`", ""])
    lines.extend(["**Procedure Steps:**", ""])
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        step_number = step.get("step_number") or "?"
        lines.extend(
            [
                f"##### Step {step_number} — {step.get('title') or 'Untitled Step'}",
                "",
                f"**Responsible role:** {step.get('responsible_role') or runbook.get('role_required') or ''}",
                "",
                "**Instruction:**",
                str(step.get("instruction") or ""),
                "",
            ]
        )
        healthy = str(step.get("healthy_condition") or "").strip()
        expected = str(step.get("expected_result") or "").strip()
        if healthy:
            lines.extend(["**Healthy condition:**", healthy, ""])
        if expected:
            lines.extend(["**Expected result:**", expected, ""])
        if artifact_index and review_markdown_path is not None:
            step_images = render_image_markdown(
                step.get("screens_or_images") or [],
                artifact_index=artifact_index,
                review_markdown_path=review_markdown_path,
                repo_root=repo_root,
                asset_link_cache=asset_link_cache,
            )
            if step_images:
                lines.extend(["**Step Images:**", "", *step_images])
        lines.extend(["---", ""])
    if runbook.get("success_criteria"):
        lines.extend(["**Success Criteria:**", "", *_bullet_lines(runbook.get("success_criteria") or []), ""])
    if runbook.get("failure_conditions"):
        lines.extend(["**Failure Conditions:**", "", *_bullet_lines(runbook.get("failure_conditions") or []), ""])
    lines.append("")
    return lines


def _render_single_runbook_html(
    runbook: dict[str, Any],
    *,
    node: dict[str, Any] | None = None,
    artifact_index: dict[str, dict[str, Any]] | None,
    review_html_path: Path | None,
    repo_root: Path,
    asset_link_cache: dict[str, str],
) -> list[str]:
    title = html.escape(str(runbook.get("title") or "Untitled"))
    procedure_id = html.escape(str(runbook.get("procedure_id") or ""))
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    parts = [
        f'<details class="linked-runbook" open><summary><strong>Runbook:</strong> {title} '
        f'(<code>{procedure_id}</code>)</summary>',
        "<ul>",
        f"<li><strong>Procedure Type:</strong> {html.escape(str(runbook.get('procedure_type') or ''))}</li>",
        f"<li><strong>Role:</strong> {html.escape(str(runbook.get('role_required') or ''))}</li>",
        f"<li><strong>Merge Status:</strong> {html.escape(str(metadata.get('merge_status') or ''))}</li>",
        "</ul>",
        "<p><strong>Summary:</strong></p>",
        f"<p>{html.escape(str(runbook.get('summary') or ''))}</p>",
        "<p><strong>When To Use:</strong></p>",
        f"<p>{html.escape(str(runbook.get('when_to_use') or ''))}</p>",
    ]
    if runbook.get("safety_notes"):
        parts.append("<p><strong>Safety Notes:</strong></p><ul>")
        for item in runbook.get("safety_notes") or []:
            parts.append(f"<li>{html.escape(str(item))}</li>")
        parts.append("</ul>")
    parts.extend(_render_runbook_branches_html(runbook, node=node, procedure_id=str(runbook.get("procedure_id") or "")))
    source_id = str(metadata.get("source_id") or "")
    source_type = str(metadata.get("source_type") or runbook.get("source_type") or "")
    if source_id or source_type:
        parts.append(
            f"<p><strong>Source:</strong> {html.escape(source_type)} / {html.escape(source_id)}</p>"
        )
    parts.append("<p><strong>Procedure Steps:</strong></p>")
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        step_number = html.escape(str(step.get("step_number") or "?"))
        step_title = html.escape(str(step.get("title") or "Untitled Step"))
        parts.extend(
            [
                f"<h5>Step {step_number} — {step_title}</h5>",
                f"<p><strong>Responsible role:</strong> {html.escape(str(step.get('responsible_role') or runbook.get('role_required') or ''))}</p>",
                "<p><strong>Instruction:</strong></p>",
                f"<p>{html.escape(str(step.get('instruction') or ''))}</p>",
            ]
        )
        healthy = str(step.get("healthy_condition") or "").strip()
        expected = str(step.get("expected_result") or "").strip()
        if healthy:
            parts.extend(["<p><strong>Healthy condition:</strong></p>", f"<p>{html.escape(healthy)}</p>"])
        if expected:
            parts.extend(["<p><strong>Expected result:</strong></p>", f"<p>{html.escape(expected)}</p>"])
        step_images = step.get("screens_or_images") or []
        if step_images and review_html_path is not None:
            parts.append("<p><strong>Step Images:</strong></p>")
            parts.extend(
                render_image_html(
                    step_images,
                    artifact_index=artifact_index,
                    review_output_path=review_html_path,
                    repo_root=repo_root,
                    asset_link_cache=asset_link_cache,
                )
            )
        parts.append("<hr>")
    if runbook.get("success_criteria"):
        parts.append("<p><strong>Success Criteria:</strong></p><ul>")
        for item in runbook.get("success_criteria") or []:
            parts.append(f"<li>{html.escape(str(item))}</li>")
        parts.append("</ul>")
    if runbook.get("failure_conditions"):
        parts.append("<p><strong>Failure Conditions:</strong></p><ul>")
        for item in runbook.get("failure_conditions") or []:
            parts.append(f"<li>{html.escape(str(item))}</li>")
        parts.append("</ul>")
    parts.append("</details>")
    return parts


def _render_runbook_branches_html(
    runbook: dict[str, Any],
    *,
    node: dict[str, Any] | None,
    procedure_id: str,
) -> list[str]:
    branches = _runbook_branch_rows(runbook, node=node, procedure_id=procedure_id)
    parts = ["<p><strong>Runbook Branches:</strong></p>", "<table>", "<tr><th>Outcome</th><th>Descriptor</th><th>Next</th></tr>"]
    for outcome, descriptor, next_node in branches:
        parts.append(
            f"<tr><td><code>{html.escape(outcome)}</code></td>"
            f"<td>{html.escape(descriptor)}</td>"
            f"<td><code>{html.escape(next_node)}</code></td></tr>"
        )
    parts.append("</table>")
    return parts


def _runbook_branch_rows(
    runbook: dict[str, Any],
    *,
    node: dict[str, Any] | None,
    procedure_id: str,
) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    next_default = ""
    if node:
        for outcome in node.get("decision_outcomes") or []:
            if not isinstance(outcome, dict):
                continue
            linked_id = str(outcome.get("linked_runbook_id") or "")
            if linked_id and linked_id != procedure_id:
                continue
            label = str(outcome.get("outcome_label") or "")
            descriptor = str(outcome.get("descriptor") or outcome.get("observable_signal") or "")
            next_node = str(outcome.get("next_node_id") or "")
            if next_node:
                next_default = next_node
            key = (label, descriptor)
            if label and key not in seen:
                seen.add(key)
                rows.append((label, descriptor, next_node))
    if not any(row[0] == "healthy" for row in rows):
        for item in runbook.get("success_criteria") or []:
            text = str(item).strip()
            if text:
                rows.append(("healthy", text, next_default))
                break
        for condition in runbook.get("healthy_conditions") or []:
            if isinstance(condition, dict):
                text = str(condition.get("healthy_condition") or condition.get("description") or "").strip()
                if text:
                    rows.append(("healthy", text, next_default))
                    break
    if not any(row[0] == "unhealthy" for row in rows):
        for item in runbook.get("failure_conditions") or []:
            text = str(item).strip()
            if text:
                rows.append(("unhealthy", text, next_default))
                break
    if not any(row[0] in {"inconclusive", "unknown"} for row in rows):
        rows.append(("unknown", "State cannot be confirmed from available runbook evidence.", next_default))
    return rows


def _caption(ref: dict[str, Any]) -> str:
    for key in ("caption", "description", "label", "title"):
        value = str(ref.get(key) or "").strip()
        if value:
            return value
    return str(ref.get("artifact_id") or "").strip()


def _bullet_lines(values: list[Any]) -> list[str]:
    return [f"- {value}" for value in values if str(value).strip()]
