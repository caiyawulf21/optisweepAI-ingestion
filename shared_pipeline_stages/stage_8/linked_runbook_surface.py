from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_7.artifact_images import collect_image_refs, render_image_html, render_image_markdown
from shared_pipeline_stages.stage_8.schemas import EvidenceCollectionProcedure

_WORD_PATTERN = re.compile(r"[a-z0-9]+")


def _distribute_visual_references_to_steps(runbook: dict[str, Any]) -> list[dict[str, Any]]:
    """Assign runbook-level visual_references to their best-matching step.

    Some runbooks (e.g. case-local Stage 6 candidates) record images only in
    the runbook-level `visual_references` list and never populate individual
    `steps[].screens_or_images`, so no images render next to any step even
    though each reference's description names the exact step it belongs to
    (e.g. "Windows Administrator Command Prompt showing ... gwcmd -r").
    This is a rendering-time fallback only: if any step already carries its
    own screens_or_images, the runbook is left untouched, since that means
    per-step image data does exist and should not be second-guessed.
    """
    steps = [step for step in runbook.get("steps") or [] if isinstance(step, dict)]
    if not steps or any(step.get("screens_or_images") for step in steps):
        return steps
    references = [ref for ref in runbook.get("visual_references") or [] if isinstance(ref, dict)]
    if not references:
        return steps

    step_word_sets = []
    for step in steps:
        text = " ".join(
            str(step.get(key) or "") for key in ("title", "instruction", "expected_result")
        ).lower()
        step_word_sets.append(set(_WORD_PATTERN.findall(text)))

    assigned_steps = [dict(step) for step in steps]
    for step in assigned_steps:
        step["screens_or_images"] = []
    for ref in references:
        description = str(ref.get("description") or ref.get("what_to_look_at") or "").lower()
        ref_words = set(_WORD_PATTERN.findall(description))
        if not ref_words:
            continue
        best_index, best_overlap = -1, 0
        for index, step_words in enumerate(step_word_sets):
            overlap = len(ref_words & step_words)
            if overlap > best_overlap:
                best_index, best_overlap = index, overlap
        if best_index >= 0:
            assigned_steps[best_index]["screens_or_images"].append(ref)
    return assigned_steps


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
        linked.append(
            {
                "procedure_id": str(runbook.get("procedure_id") or procedure_id),
                "title": str(runbook.get("title") or ""),
                "procedure_type": str(runbook.get("procedure_type") or ""),
                "purpose": str(
                    runbook.get("purpose")
                    or runbook.get("summary")
                    or runbook.get("when_to_use")
                    or ""
                ),
                "role_required": str(runbook.get("role_required") or ""),
                "audience_roles": list(runbook.get("audience_roles") or []),
            }
        )
    node["linked_runbooks"] = linked
    node["evidence_collection_procedures"] = [
        EvidenceCollectionProcedure(
            procedure_id=item["procedure_id"],
            title=item["title"],
            purpose=item["purpose"],
            role_required=item["role_required"],
            audience_roles=item["audience_roles"],
        ).model_dump()
        for item in linked
    ]
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
    grouped = _group_runbooks_by_audience(node, runbooks_by_id=runbooks_by_id)
    operator = grouped.get("operator") or []
    support = grouped.get("support") or []
    if not operator and not support:
        return ["*No linked runbook content available.*", ""]
    if operator:
        lines.extend(
            [
                f"<details><summary><strong>Operator runbooks</strong> ({len(operator)})</summary>",
                "",
            ]
        )
        for runbook in operator:
            if not isinstance(runbook, dict):
                continue
            lines.append(
                f"<details><summary>{runbook.get('title') or 'Untitled'} "
                f"(`{runbook.get('procedure_id')}`)</summary>",
            )
            lines.append("")
            lines.extend(
                _render_single_runbook_markdown(
                    runbook,
                    artifact_index=artifact_index,
                    review_markdown_path=review_markdown_path,
                    repo_root=repo_root,
                    asset_link_cache=asset_link_cache,
                    heading_level=5,
                    audience_label="operator",
                )
            )
            lines.extend(["</details>", ""])
        lines.extend(["</details>", ""])
    if support:
        lines.extend(
            [
                f"<details><summary><strong>Support runbooks</strong> ({len(support)})</summary>",
                "",
            ]
        )
        for runbook in support:
            if not isinstance(runbook, dict):
                continue
            lines.append(
                f"<details><summary>{runbook.get('title') or 'Untitled'} "
                f"(`{runbook.get('procedure_id')}`)</summary>",
            )
            lines.append("")
            lines.extend(
                _render_single_runbook_markdown(
                    runbook,
                    artifact_index=artifact_index,
                    review_markdown_path=review_markdown_path,
                    repo_root=repo_root,
                    asset_link_cache=asset_link_cache,
                    heading_level=5,
                    audience_label="support",
                )
            )
            lines.extend(["</details>", ""])
        lines.extend(["</details>", ""])
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
    grouped = _group_runbooks_by_audience(node, runbooks_by_id=runbooks_by_id)
    operator = grouped.get("operator") or []
    support = grouped.get("support") or []
    if not operator and not support:
        return ["<p><em>No linked runbook content available.</em></p>"]
    if operator:
        parts.append(
            f'<details class="linked-runbook-group linked-runbook-operator" open>'
            f"<summary><strong>Operator runbooks</strong> ({len(operator)})</summary>"
        )
        for index, runbook in enumerate(operator):
            if not isinstance(runbook, dict):
                continue
            parts.extend(
                _render_single_runbook_html(
                    runbook,
                    node=node,
                    artifact_index=artifact_index,
                    review_html_path=review_html_path,
                    repo_root=repo_root,
                    asset_link_cache=asset_link_cache,
                    default_open=index == 0,
                    audience_label="operator",
                )
            )
        parts.append("</details>")
    if support:
        parts.append(
            f'<details class="linked-runbook-group linked-runbook-support" open>'
            f"<summary><strong>Support runbooks</strong> ({len(support)})</summary>"
        )
        for index, runbook in enumerate(support):
            if not isinstance(runbook, dict):
                continue
            parts.extend(
                _render_single_runbook_html(
                    runbook,
                    node=node,
                    artifact_index=artifact_index,
                    review_html_path=review_html_path,
                    repo_root=repo_root,
                    asset_link_cache=asset_link_cache,
                    default_open=index == 0 and not operator,
                    audience_label="support",
                )
            )
        parts.append("</details>")
    return parts


OPERATOR_AUDIENCE_ROLES = {"operator", "on_site"}
SUPPORT_AUDIENCE_ROLES = {
    "L1_support",
    "L2_support",
    "L3_support",
    "L4_support",
    "L2_L3_support",
    "remote",
}


def runbook_audience_bucket(runbook: dict[str, Any] | None) -> str:
    """Classify a runbook as operator (site/customer) or support (FORTNA L1–L4)."""
    if not isinstance(runbook, dict):
        return "support"
    primary = str(runbook.get("role_required") or runbook.get("responsible_role") or "").strip()
    if primary in OPERATOR_AUDIENCE_ROLES:
        return "operator"
    if primary in SUPPORT_AUDIENCE_ROLES or primary.startswith("L"):
        return "support"
    audience = {
        str(item).strip()
        for item in (runbook.get("audience_roles") or [])
        if str(item or "").strip()
    }
    if audience & OPERATOR_AUDIENCE_ROLES and not (audience & SUPPORT_AUDIENCE_ROLES):
        return "operator"
    if audience & SUPPORT_AUDIENCE_ROLES:
        return "support"
    if audience & OPERATOR_AUDIENCE_ROLES:
        return "operator"
    return "support"


def _group_runbooks_by_audience(
    node: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {"operator": [], "support": []}
    seen: set[str] = set()
    ordered_ids: list[str] = []
    for link in node.get("runbook_links") or []:
        if not isinstance(link, dict):
            continue
        procedure_id = str(link.get("procedure_id") or "")
        if procedure_id and procedure_id not in seen:
            seen.add(procedure_id)
            ordered_ids.append(procedure_id)
    for procedure_id in node.get("resolved_runbook_ids") or []:
        pid = str(procedure_id or "")
        if pid and pid not in seen:
            seen.add(pid)
            ordered_ids.append(pid)

    runbooks_by_proc: dict[str, dict[str, Any]] = {}
    for runbook in node.get("linked_runbooks") or []:
        if isinstance(runbook, dict) and runbook.get("procedure_id"):
            runbooks_by_proc[str(runbook.get("procedure_id"))] = runbook
    for procedure_id in ordered_ids:
        runbook = runbooks_by_id.get(procedure_id) or runbooks_by_proc.get(procedure_id)
        if not isinstance(runbook, dict):
            continue
        bucket = runbook_audience_bucket(runbook)
        grouped[bucket].append(runbook)
    return grouped


def _group_runbooks_by_link_role(
    node: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    return _group_runbooks_by_audience(node, runbooks_by_id=runbooks_by_id)


def _render_single_runbook_markdown(
    runbook: dict[str, Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None,
    review_markdown_path: Path | None,
    repo_root: Path,
    asset_link_cache: dict[str, str],
    heading_level: int = 4,
    audience_label: str = "",
) -> list[str]:
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    heading = "#" * max(2, min(heading_level, 6))
    step_heading = "#" * max(2, min(heading_level + 1, 6))
    audience = audience_label or runbook_audience_bucket(runbook)
    lines = [
        f"{heading} Runbook: {runbook.get('title') or 'Untitled'}",
        "",
        f"- **Procedure ID:** `{runbook.get('procedure_id')}`",
        f"- **Procedure Type:** `{runbook.get('procedure_type')}`",
        f"- **Role:** `{runbook.get('role_required')}`",
        f"- **Audience:** `{audience}`",
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
    for step in _distribute_visual_references_to_steps(runbook):
        if not isinstance(step, dict):
            continue
        step_number = step.get("step_number") or "?"
        lines.extend(
            [
                f"{step_heading} Step {step_number} — {step.get('title') or 'Untitled Step'}",
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
    default_open: bool = True,
    audience_label: str = "",
) -> list[str]:
    title = html.escape(str(runbook.get("title") or "Untitled"))
    procedure_id = html.escape(str(runbook.get("procedure_id") or ""))
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    audience = audience_label or runbook_audience_bucket(runbook)
    open_attr = " open" if default_open else ""
    parts = [
        f'<details class="linked-runbook linked-runbook-{html.escape(audience)}"{open_attr}>'
        f"<summary><strong>{html.escape(audience.title())} runbook:</strong> {title} "
        f'(<code>{procedure_id}</code>)</summary>',
        "<ul>",
        f"<li><strong>Procedure Type:</strong> {html.escape(str(runbook.get('procedure_type') or ''))}</li>",
        f"<li><strong>Role:</strong> {html.escape(str(runbook.get('role_required') or ''))}</li>",
        f"<li><strong>Audience:</strong> {html.escape(audience)}</li>",
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
    for step in _distribute_visual_references_to_steps(runbook):
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
