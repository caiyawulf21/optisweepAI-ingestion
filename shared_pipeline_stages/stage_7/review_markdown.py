from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import re

from shared_pipeline_stages.stage_7.artifact_images import collect_image_refs, render_image_markdown


def safe_review_filename(procedure_id: str, *, max_length: int = 80) -> str:
    raw = str(procedure_id or "runbook").strip()
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "_", raw).strip("._-") or "runbook"
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    if len(slug) <= max_length:
        return f"{slug}.md"
    return f"rb_{digest}.md"


def write_runbook_review_markdown(
    runbook: dict[str, Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None = None,
    review_markdown_path: Path | None = None,
    asset_link_cache: dict[str, str] | None = None,
) -> str:
    lines: list[str] = []
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    lines.extend(
        [
            f"# {runbook.get('title') or 'Runbook'}",
            "",
            "## Runbook Header",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Procedure ID | `{runbook.get('procedure_id')}` |",
            f"| Procedure Type | `{runbook.get('procedure_type')}` |",
            f"| Primary Role | `{runbook.get('role_required')}` |",
            f"| Validation Status | `{runbook.get('validation_status')}` |",
            f"| Merge Status | `{metadata.get('merge_status')}` |",
            "",
            "## Summary",
            "",
            str(runbook.get("summary") or ""),
            "",
            "## When To Use",
            "",
            str(runbook.get("when_to_use") or ""),
            "",
        ]
    )
    if runbook.get("merged_from_procedure_ids"):
        lines.extend(
            [
                "## Source Procedure References",
                "",
                *_bullet_lines(runbook.get("merged_from_procedure_ids") or []),
                "",
            ]
        )
    if runbook.get("safety_notes"):
        lines.extend(["## Safety And Operational Notes", "", *_bullet_lines(runbook.get("safety_notes") or []), ""])
    image_lines: list[str] = []
    if artifact_index and review_markdown_path is not None:
        image_lines = render_image_markdown(
            collect_image_refs(runbook),
            artifact_index=artifact_index,
            review_markdown_path=review_markdown_path,
            asset_link_cache=asset_link_cache,
        )
    if image_lines:
        lines.extend(["## Visual References", "", *image_lines])
    lines.extend(["## Procedure Steps", ""])
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        step_number = step.get("step_number") or "?"
        lines.extend(
            [
                f"### Step {step_number} — {step.get('title') or 'Untitled Step'}",
                "",
                f"**Responsible role:** {step.get('responsible_role') or runbook.get('role_required')}",
                "",
                "**Instruction:**",
                str(step.get("instruction") or ""),
                "",
                "**Expected result:**",
                str(step.get("expected_result") or ""),
                "",
            ]
        )
        if artifact_index and review_markdown_path is not None:
            step_images = render_image_markdown(
                step.get("screens_or_images") or [],
                artifact_index=artifact_index,
                review_markdown_path=review_markdown_path,
                asset_link_cache=asset_link_cache,
            )
            if step_images:
                lines.extend(["**Screens / Images:**", "", *step_images])
        lines.extend(["---", ""])
    if runbook.get("success_criteria"):
        lines.extend(["## Success Criteria", "", *_bullet_lines(runbook.get("success_criteria") or []), ""])
    if runbook.get("failure_conditions"):
        lines.extend(["## Failure Conditions", "", *_bullet_lines(runbook.get("failure_conditions") or []), ""])
    if runbook.get("escalation_guidance"):
        lines.extend(["## Escalation Guidance", "", *_bullet_lines(runbook.get("escalation_guidance") or []), ""])
    if runbook.get("known_gaps") or runbook.get("missing_details"):
        gaps = _dedupe(
            list(runbook.get("known_gaps") or []) + list(runbook.get("missing_details") or [])
        )
        lines.extend(["## Missing Details / Known Gaps", "", *_bullet_lines(gaps), ""])
    if runbook.get("merge_history"):
        lines.extend(["## Merge History", "", "```json", _json_block(runbook.get("merge_history")), "```", ""])
    return "\n".join(lines).rstrip() + "\n"


def write_review_file(
    runbook: dict[str, Any],
    review_path: str | Path,
    *,
    artifact_index: dict[str, dict[str, Any]] | None = None,
    asset_link_cache: dict[str, str] | None = None,
) -> None:
    path = Path(review_path)
    path = path.parent / safe_review_filename(str(runbook.get("procedure_id") or path.stem))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        write_runbook_review_markdown(
            runbook,
            artifact_index=artifact_index,
            review_markdown_path=path,
            asset_link_cache=asset_link_cache,
        ),
        encoding="utf-8",
    )


def _bullet_lines(items: list[Any]) -> list[str]:
    return [f"- {item}" for item in items if str(item).strip()]


def _dedupe(items: list[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        text = str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _json_block(value: Any) -> str:
    import json

    return json.dumps(value, ensure_ascii=False, indent=2)
