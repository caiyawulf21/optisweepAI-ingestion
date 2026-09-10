"""Remove Stage 6/8 outputs whose candidate_id is not in current Stage 5."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OP_OUT = ROOT / "operationalknowledgeingestion" / "data" / "output"
SOURCES = ["training_video_day1", "training_video_day2"]


def candidate_ids(source_dir: Path) -> set[str]:
    payload = json.loads((source_dir / "stage_5_runbook_candidates" / "runbook_candidates.json").read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        candidates = payload.get("candidates") or payload.get("runbook_candidates") or []
    else:
        candidates = payload
    return {
        str(item.get("candidate_id"))
        for item in candidates
        if isinstance(item, dict) and item.get("candidate_id")
    }


def clean_source(name: str) -> None:
    source_dir = OP_OUT / name
    ids = candidate_ids(source_dir)
    removed = 0
    dirs = [
        source_dir / "stage_6_finalized_runbooks" / "finalized_runbooks",
        source_dir / "stage_6_finalized_runbooks" / "review_markdown" / "runbooks",
        source_dir / "stage_8_relationship_linking" / "finalized_runbooks_linked",
    ]
    for directory in dirs:
        if not directory.exists():
            continue
        for path in directory.iterdir():
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".json", ".md", ".html"}:
                continue
            if path.stem not in ids:
                path.unlink()
                removed += 1
    kept = len(list((source_dir / "stage_6_finalized_runbooks" / "finalized_runbooks").glob("*.json")))
    print(f"{name}: kept={kept} expected={len(ids)} removed={removed}")


def main() -> None:
    for name in SOURCES:
        clean_source(name)


if __name__ == "__main__":
    main()
