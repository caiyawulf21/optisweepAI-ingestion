from __future__ import annotations

from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_7.artifact_images import collect_image_refs, render_image_markdown
from shared_pipeline_stages.stage_7.review_markdown import write_runbook_review_markdown
from shared_pipeline_stages.stage_7.schemas import ClusterMergeResult


def write_merge_comparison_review(
    output_path: str | Path,
    *,
    cluster_results: list[ClusterMergeResult],
    source_runbooks_by_id: dict[str, dict[str, Any]],
    canonical_by_id: dict[str, dict[str, Any]],
    artifact_index: dict[str, dict[str, Any]] | None = None,
    generated_at: str = "",
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    asset_cache: dict[str, str] = {}
    lines = [
        "# Stage 7 Merge Comparison Review",
        "",
        "Before-and-after view for every LLM-processed merge sub-cluster.",
        "",
        f"- Generated at: `{generated_at}`",
        f"- LLM sub-clusters reviewed: {len(cluster_results)}",
        "",
        "## How to read this file",
        "",
        "Each section shows:",
        "",
        "1. **Before** — finalized source runbooks that entered the merge packet",
        "2. **After** — canonical runbook(s) produced by Stage 7",
        "3. Conflicts, gaps, and merge notes from the LLM",
        "",
        "Images are copied into `review_markdown/assets/` for inline preview.",
        "",
    ]
    llm_results = [item for item in cluster_results if item.llm_used]
    if not llm_results:
        lines.append("No LLM merge results were produced.")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    for index, result in enumerate(llm_results, start=1):
        lines.extend(
            _comparison_section(
                index,
                result,
                source_runbooks_by_id=source_runbooks_by_id,
                canonical_by_id=canonical_by_id,
                review_markdown_path=path,
                artifact_index=artifact_index,
                asset_cache=asset_cache,
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _comparison_section(
    index: int,
    result: ClusterMergeResult,
    *,
    source_runbooks_by_id: dict[str, dict[str, Any]],
    canonical_by_id: dict[str, dict[str, Any]],
    review_markdown_path: Path,
    artifact_index: dict[str, dict[str, Any]] | None,
    asset_cache: dict[str, str],
) -> list[str]:
    lines = [
        f"## {index}. `{result.sub_cluster_id}`",
        "",
        f"- **Parent cluster:** `{result.merge_cluster_id}`",
        f"- **Merge decision:** `{result.merge_decision}`",
        f"- **Source procedure IDs:** {', '.join(f'`{item}`' for item in result.merged_from_procedure_ids)}",
        f"- **Canonical procedure IDs:** {', '.join(f'`{item}`' for item in result.canonical_procedure_ids) or '_none_'}",
        "",
    ]
    if result.merge_notes:
        lines.extend(["### Merge notes", "", *_bullets(result.merge_notes), ""])
    if result.conflicts:
        lines.extend(["### Conflicts", "", *_bullets(result.conflicts), ""])
    if result.known_gaps:
        lines.extend(["### Known gaps", "", *_bullets(result.known_gaps), ""])
    if result.error:
        lines.extend([f"**Error:** {result.error}", ""])

    lines.extend(["### Before (source finalized runbooks)", ""])
    for procedure_id in result.merged_from_procedure_ids:
        runbook = source_runbooks_by_id.get(procedure_id)
        if runbook is None:
            lines.extend([f"#### Missing runbook `{procedure_id}`", ""])
            continue
        lines.extend(_runbook_subsection(runbook, heading_level=4, label="Before"))
        image_lines = render_image_markdown(
            collect_image_refs(runbook),
            artifact_index=artifact_index,
            review_markdown_path=review_markdown_path,
            asset_link_cache=asset_cache,
        )
        if image_lines:
            lines.extend(["**Images:**", "", *image_lines])

    lines.extend(["### After (canonical runbook(s))", ""])
    if not result.canonical_procedure_ids:
        lines.extend(["_No canonical runbooks were produced for this sub-cluster._", ""])
        return lines

    for procedure_id in result.canonical_procedure_ids:
        runbook = canonical_by_id.get(procedure_id)
        if runbook is None:
            lines.extend([f"#### Missing canonical `{procedure_id}`", ""])
            continue
        lines.extend(_runbook_subsection(runbook, heading_level=4, label="After"))
        image_lines = render_image_markdown(
            collect_image_refs(runbook),
            artifact_index=artifact_index,
            review_markdown_path=review_markdown_path,
            asset_link_cache=asset_cache,
        )
        if image_lines:
            lines.extend(["**Images:**", "", *image_lines])
        lines.extend(["<details>", "<summary>Full canonical markdown</summary>", "", "```markdown"])
        lines.extend(write_runbook_review_markdown(runbook).splitlines())
        lines.extend(["```", "</details>", ""])
    return lines


def _runbook_subsection(runbook: dict[str, Any], *, heading_level: int, label: str) -> list[str]:
    prefix = "#" * heading_level
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    return [
        f"{prefix} {label}: {runbook.get('title') or 'Untitled'}",
        "",
        f"- Procedure ID: `{runbook.get('procedure_id')}`",
        f"- Source type: `{metadata.get('source_type') or 'n/a'}`",
        f"- Procedure type: `{runbook.get('procedure_type')}`",
        f"- Role: `{runbook.get('role_required')}`",
        "",
        "**Summary:**",
        str(runbook.get("summary") or ""),
        "",
        "**When to use:**",
        str(runbook.get("when_to_use") or ""),
        "",
        "**Steps:**",
        "",
    ] + _step_summaries(runbook) + [""]


def _step_summaries(runbook: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        lines.append(
            f"- Step {step.get('step_number') or '?'} — {step.get('title') or 'Untitled'}: "
            f"{step.get('instruction') or ''}"
        )
    return lines or ["- _No steps_"]


def _bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items if str(item).strip()]
