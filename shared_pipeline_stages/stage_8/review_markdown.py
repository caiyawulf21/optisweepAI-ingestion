from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_8.linked_runbook_surface import (
    render_linked_runbooks_html,
    render_linked_runbooks_markdown,
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
    unresolved = _unresolved_nodes(playbook)
    if unresolved:
        lines.extend(["## Unresolved / Low-Confidence Links", "", *_bullet_lines(unresolved), ""])
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
    unresolved = _unresolved_nodes(playbook)
    if unresolved:
        parts.extend(["<h2>Unresolved / Low-Confidence Links</h2>", "<ul>"])
        for item in unresolved:
            parts.append(f"<li>{html.escape(item)}</li>")
        parts.append("</ul>")
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
    lines = [
        f"### {node.get('node_order')} — {node.get('title')} (`{node.get('node_type')}`)",
        "",
        f"**Intent:** {node.get('intent') or node.get('goal') or ''}",
        "",
        "**Runbook Links:**",
        "",
    ]
    links = node.get("runbook_links") or []
    if not links:
        lines.append("- unresolved")
    for link in links:
        if not isinstance(link, dict):
            continue
        procedure_id = str(link.get("procedure_id") or "")
        runbook = runbooks_by_id.get(procedure_id, {})
        lines.append(
            f"- `{procedure_id}` ({link.get('link_confidence')}, score={link.get('retrieval_combined_score', 'n/a')}, boosted={link.get('boosted_score', 'n/a')}) — {runbook.get('title') or link.get('link_rationale') or ''}"
        )
        gaps = link.get("match_gaps") or []
        if gaps:
            lines.extend([f"  - gaps: {'; '.join(str(item) for item in gaps)}"])
    outcomes = node.get("decision_outcomes") or []
    if outcomes:
        lines.extend(["", "**Decision Outcomes:**", ""])
        for outcome in outcomes:
            if not isinstance(outcome, dict):
                continue
            lines.append(
                f"- `{outcome.get('outcome_label')}`: {outcome.get('descriptor') or outcome.get('observable_signal') or ''}"
            )
    branches = node.get("branches") or []
    if branches:
        lines.extend(["", "**Branches:**", ""])
        for branch in branches:
            if not isinstance(branch, dict):
                continue
            lines.append(
                f"- `{branch.get('outcome')}` → `{branch.get('next_node_id')}` when {branch.get('condition_label') or branch.get('condition_descriptor') or ''}"
            )
    lines.extend(["", "**Linked Runbook Procedures:**", ""])
    return lines


def _render_node_html(node: dict[str, Any], *, runbooks_by_id: dict[str, dict[str, Any]]) -> list[str]:
    title = html.escape(str(node.get("title") or "Node"))
    parts = [
        f"<h3>{html.escape(str(node.get('node_order') or ''))} — {title} ({html.escape(str(node.get('node_type') or ''))})</h3>",
        f"<p><strong>Intent:</strong> {html.escape(str(node.get('intent') or node.get('goal') or ''))}</p>",
        "<p><strong>Runbook Links:</strong></p>",
        "<ul>",
    ]
    links = node.get("runbook_links") or []
    if not links:
        parts.append('<li class="warn">unresolved</li>')
    for link in links:
        if not isinstance(link, dict):
            continue
        procedure_id = str(link.get("procedure_id") or "")
        runbook = runbooks_by_id.get(procedure_id, {})
        confidence = html.escape(str(link.get("link_confidence") or ""))
        label = html.escape(str(runbook.get("title") or link.get("link_rationale") or ""))
        css = ' class="warn"' if confidence == "low" else ""
        score = link.get("retrieval_combined_score")
        score_label = f", score={score}" if score is not None else ""
        parts.append(f"<li{css}><code>{html.escape(procedure_id)}</code> ({confidence}{score_label}) — {label}</li>")
    parts.append("</ul>")
    parts.append("<p><strong>Linked Runbook Procedures:</strong></p>")
    outcomes = node.get("decision_outcomes") or []
    if outcomes:
        parts.extend(["<p><strong>Decision Outcomes:</strong></p>", "<ul>"])
        for outcome in outcomes:
            if not isinstance(outcome, dict):
                continue
            parts.append(
                f"<li><code>{html.escape(str(outcome.get('outcome_label') or ''))}</code>: "
                f"{html.escape(str(outcome.get('descriptor') or outcome.get('observable_signal') or ''))}</li>"
            )
        parts.append("</ul>")
    branches = node.get("branches") or []
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
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("node_id") or "")
        for branch in node.get("branches") or []:
            if not isinstance(branch, dict):
                continue
            rows.append(
                (
                    node_id,
                    str(branch.get("outcome") or ""),
                    str(branch.get("condition_label") or branch.get("condition_descriptor") or ""),
                    str(branch.get("next_node_id") or ""),
                )
            )
    for branch in playbook.get("branches") or []:
        if not isinstance(branch, dict):
            continue
        rows.append(
            (
                str(branch.get("from_node_id") or ""),
                str(branch.get("outcome") or ""),
                str(branch.get("condition_label") or branch.get("condition_descriptor") or ""),
                str(branch.get("next_node_id") or ""),
            )
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
