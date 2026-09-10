"""Export the last Stage 8 corpus and Stage 5 candidates for SME review."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared_pipeline_stages.stage_7.review_markdown import safe_review_filename, write_runbook_review_markdown

REVIEW_ROOT = REPO_ROOT / "sme_review_runbooks" / "last_stage8_run"
RUNBOOK_DEST = REVIEW_ROOT / "runbooks"
STAGE5_DEST = REVIEW_ROOT / "stage5_playbook_outputs"
STAGE8_DEST = REVIEW_ROOT / "stage8_playbook_outputs"


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _stage5_markdown(candidate: dict, *, case_id: str, variant: str) -> str:
    lines = [
        f"# Stage 5 Playbook Candidate — Case {case_id}",
        "",
        f"- **Variant:** `{variant}`",
        f"- **Title:** {candidate.get('title') or ''}",
        f"- **Candidate ID:** `{candidate.get('playbook_candidate_id') or candidate.get('candidate_id') or ''}`",
        "",
        "## Playbook Context",
        "",
        str(candidate.get("playbook_goal") or candidate.get("user_facing_summary") or ""),
        "",
    ]
    for node in candidate.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        lines.extend(
            [
                f"## {node.get('node_id') or ''} — {node.get('title') or ''}",
                "",
                f"- **Node type:** `{node.get('node_type') or ''}`",
                f"- **Intent:** {node.get('intent') or node.get('goal') or ''}",
                f"- **Expected result:** {node.get('expected_or_observed_result') or ''}",
                f"- **Runbook placeholder:** {node.get('runbook_placeholder') or ''}",
                f"- **Expects capability:** {', '.join(node.get('expects_capability') or []) or 'None'}",
                f"- **Expects surface:** {', '.join(node.get('expects_surface') or []) or 'None'}",
                f"- **Preferred audience:** {', '.join(node.get('preferred_audience') or []) or 'None'}",
                "",
            ]
        )
        for key, heading in (
            ("source_supported_description", "Source-supported description"),
            ("stop_or_escalation_note", "Stop or escalation note"),
            ("source_refs", "Source references"),
            ("related_artifact_ids", "Related artifacts"),
            ("related_event_ids", "Related events"),
        ):
            value = node.get(key)
            if value:
                lines.extend([f"### {heading}", "", "```json", json.dumps(value, indent=2, ensure_ascii=False), "```", ""])
    return "\n".join(lines) + "\n"


def export() -> None:
    if REVIEW_ROOT.exists():
        shutil.rmtree(REVIEW_ROOT)
    RUNBOOK_DEST.mkdir(parents=True)
    STAGE5_DEST.mkdir(parents=True)
    STAGE8_DEST.mkdir(parents=True)

    pool = _read(REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool/runbook_pool.json")
    entries = pool.get("entries") if isinstance(pool, dict) else pool
    stage7 = _read(REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks/canonical_runbooks.json")
    runbooks = stage7.get("runbooks") if isinstance(stage7, dict) else stage7
    by_id = {str(item.get("procedure_id")): item for item in runbooks if isinstance(item, dict)}

    for entry in entries:
        procedure_id = str(entry.get("finalized_runbook_id") or "")
        runbook = by_id.get(procedure_id)
        if not runbook:
            continue
        path = RUNBOOK_DEST / safe_review_filename(procedure_id)
        path.write_text(write_runbook_review_markdown(runbook, review_markdown_path=path), encoding="utf-8")

    for case_id in ("228086", "228723", "223554", "218550"):
        for variant, subdir in (
            ("prompt_a_one_per_incident", "playbook_prompt_a_one_per_incident"),
            ("prompt_b_multi_flow", "playbook_prompt_b_multi_flow"),
        ):
            source = (
                REPO_ROOT
                / f"incidenceknowledgeingestion/data/output/incidents/case_{case_id}/stage_5_runbook_candidates/{subdir}/playbook_candidates.json"
            )
            if not source.is_file():
                continue
            candidates = _read(source)
            for index, candidate in enumerate(candidates, start=1):
                name = f"case_{case_id}_{variant}_{index:02d}.md"
                (STAGE5_DEST / name).write_text(
                    _stage5_markdown(candidate, case_id=case_id, variant=variant),
                    encoding="utf-8",
                )

    stage8_root = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks"
    for variant in ("prompt_a_one_per_incident", "prompt_b_multi_flow"):
        source_dir = stage8_root / variant / "review_markdown" / "playbooks"
        destination = STAGE8_DEST / variant
        destination.mkdir(parents=True, exist_ok=True)
        if source_dir.is_dir():
            for markdown in source_dir.glob("*.md"):
                shutil.copy2(markdown, destination / markdown.name)

    (REVIEW_ROOT / "README.md").write_text(
        "# Last Stage 8 SME Review Export\n\n"
        "This snapshot contains the 202 runbooks in the filtered Stage 6.5/7 corpus "
        "used by the last Stage 8 run, plus Stage 5 playbook candidates for all four "
        "cases and both Prompt A/B variants.\n\n"
        "- `runbooks/`: canonical runbook review Markdown\n"
        "- `stage5_playbook_outputs/`: Stage 5 candidate playbooks as Markdown\n"
        "- `stage8_playbook_outputs/`: final Stage 8 Prompt A/B playbook review Markdown\n",
        encoding="utf-8",
    )
    print(f"Exported {len(list(RUNBOOK_DEST.glob('*.md')))} runbooks")
    print(f"Exported {len(list(STAGE5_DEST.glob('*.md')))} Stage 5 playbooks")
    print(f"Exported {len(list(STAGE8_DEST.rglob('*.md')))} Stage 8 playbooks")


if __name__ == "__main__":
    export()
