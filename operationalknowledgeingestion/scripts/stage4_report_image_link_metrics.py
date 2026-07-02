"""Report image/artifact linkage metrics for Stage 4 and Stage 5 outputs."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT_PARENT = ROOT.parent
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))

from operationalknowledgeingestion.src.optisweep_ingestion.tools.artifact_linker import IMAGE_NOTE_MARKER


def load_json(path: Path) -> list | dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def stage4_metrics(contexts: list[dict]) -> dict[str, int | float]:
    total = len(contexts)
    with_art = sum(1 for item in contexts if item.get("related_artifact_ids"))
    with_image_refs = sum(1 for item in contexts if item.get("image_refs"))
    return {
        "total": total,
        "with_related_artifact_ids": with_art,
        "with_image_refs": with_image_refs,
        "empty_related_artifact_ids": total - with_art,
        "artifact_coverage_pct": round(100 * with_art / total, 1) if total else 0.0,
    }


def stage5_metrics(candidates: list[dict]) -> dict[str, int | float]:
    total = len(candidates)
    empty_art = sum(1 for item in candidates if not item.get("related_artifact_ids"))
    with_img_note = sum(
        1 for item in candidates if any(IMAGE_NOTE_MARKER in str(step) for step in (item.get("rough_steps") or []))
    )
    screen_kw = ["hmi", "screen", "visu_", "figure", "stacklight", "button"]
    screen_missing = 0
    for item in candidates:
        text = " ".join(item.get("rough_steps") or []) + " " + str(item.get("title") or "") + " " + str(item.get("summary") or "")
        if not any(k in text.lower() for k in screen_kw):
            continue
        has_note = any(IMAGE_NOTE_MARKER in str(step) for step in (item.get("rough_steps") or []))
        has_art = bool(item.get("related_artifact_ids"))
        if not has_note and not has_art:
            screen_missing += 1
    return {
        "total": total,
        "with_related_artifact_ids": total - empty_art,
        "empty_related_artifact_ids": empty_art,
        "with_image_notes": with_img_note,
        "screen_hmi_missing_both": screen_missing,
        "artifact_coverage_pct": round(100 * (total - empty_art) / total, 1) if total else 0.0,
    }


def main() -> None:
    base = ROOT / "data" / "output" / "manual_optisweep_om_v3"
    contexts = load_json(base / "stage_4_operational_context" / "operational_context.json")
    candidates = load_json(base / "stage_5_runbook_candidates" / "runbook_candidates.json")
    print("Stage 4:", json.dumps(stage4_metrics(contexts), indent=2))
    print("Stage 5:", json.dumps(stage5_metrics(candidates), indent=2))


if __name__ == "__main__":
    main()
