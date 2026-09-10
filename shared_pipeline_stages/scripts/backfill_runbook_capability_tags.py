"""Backfill capability / surface / audience / failure tags on existing finalized runbooks.

Heuristic by default (no LLM). Targets:
- operationalknowledgeingestion/data/output/**/stage_6_finalized_runbooks/finalized_runbooks/*.json
- shared Stage 7 canonical_runbooks.json (when present)

Example:

```powershell
python shared_pipeline_stages/scripts/backfill_runbook_capability_tags.py
python shared_pipeline_stages/scripts/backfill_runbook_capability_tags.py --regenerate-reviews
```
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared_pipeline_stages.runbook_tags import TAG_FIELDS, infer_runbook_tags, normalize_runbook_tags


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ops-output-root",
        type=Path,
        default=REPO_ROOT / "operationalknowledgeingestion" / "data" / "output",
        help="Root of operational source outputs",
    )
    parser.add_argument(
        "--stage7-canonical",
        type=Path,
        default=REPO_ROOT
        / "shared_pipeline_stages"
        / "data"
        / "output"
        / "shared"
        / "stage_7_merged_runbooks"
        / "canonical_runbooks.json",
        help="Optional Stage 7 canonical_runbooks.json",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing tag fields (default: fill only empty lists)",
    )
    parser.add_argument(
        "--regenerate-reviews",
        action="store_true",
        help="Rewrite Stage 6 review MD/HTML for updated ops runbooks",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report only; do not write files")
    args = parser.parse_args()

    updated_paths: list[Path] = []
    for path in _iter_stage6_runbook_paths(args.ops_output_root):
        if _backfill_file(path, force=args.force, dry_run=args.dry_run):
            updated_paths.append(path)

    if args.stage7_canonical.exists():
        if _backfill_canonical_bundle(args.stage7_canonical, force=args.force, dry_run=args.dry_run):
            updated_paths.append(args.stage7_canonical)

    print(f"Updated {len(updated_paths)} artifact(s)")
    for path in updated_paths[:30]:
        print(f"  - {path.relative_to(REPO_ROOT)}")
    if len(updated_paths) > 30:
        print(f"  ... and {len(updated_paths) - 30} more")

    if args.regenerate_reviews and not args.dry_run:
        _regenerate_reviews_for_paths(updated_paths)

    return 0


def _iter_stage6_runbook_paths(ops_root: Path) -> list[Path]:
    if not ops_root.exists():
        return []
    return sorted(ops_root.glob("*/stage_6_finalized_runbooks/finalized_runbooks/*.json"))


def _backfill_file(path: Path, *, force: bool, dry_run: bool) -> bool:
    runbook = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(runbook, dict):
        return False
    before = {field: list(runbook.get(field) or []) for field in TAG_FIELDS}
    if not force and all(before[field] for field in ("capability_tags", "access_surface")):
        return False
    if force:
        for field in TAG_FIELDS:
            runbook[field] = []
    infer_runbook_tags(runbook)
    after = {field: list(runbook.get(field) or []) for field in TAG_FIELDS}
    if before == after:
        return False
    if not dry_run:
        path.write_text(json.dumps(runbook, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def _backfill_canonical_bundle(path: Path, *, force: bool, dry_run: bool) -> bool:
    payload = json.loads(path.read_text(encoding="utf-8"))
    runbooks = payload.get("runbooks") if isinstance(payload, dict) else payload
    if not isinstance(runbooks, list):
        return False
    changed = False
    for runbook in runbooks:
        if not isinstance(runbook, dict):
            continue
        before = {field: list(runbook.get(field) or []) for field in TAG_FIELDS}
        if not force and all(before[field] for field in ("capability_tags", "access_surface")):
            continue
        if force:
            for field in TAG_FIELDS:
                runbook[field] = []
        infer_runbook_tags(runbook)
        after = {field: list(runbook.get(field) or []) for field in TAG_FIELDS}
        if before != after:
            changed = True
    if changed and not dry_run:
        if isinstance(payload, dict):
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            path.write_text(json.dumps(runbooks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def _regenerate_reviews_for_paths(paths: list[Path]) -> None:
    try:
        from operationalknowledgeingestion.src.optisweep_ingestion.stage6_runbook_finalization import (
            write_runbook_review_html,
            write_runbook_review_markdown,
        )
    except ImportError:
        print("Could not import Stage 6 review writers; skip --regenerate-reviews")
        return

    for path in paths:
        if "stage_6_finalized_runbooks" not in str(path):
            continue
        runbook = json.loads(path.read_text(encoding="utf-8"))
        review_dir = path.parents[1] / "review_markdown" / "runbooks"
        review_dir.mkdir(parents=True, exist_ok=True)
        stem = path.stem
        md_path = review_dir / f"{stem}.md"
        html_path = review_dir / f"{stem}.html"
        md_path.write_text(
            write_runbook_review_markdown(runbook, review_markdown_path=md_path, repo_root=REPO_ROOT),
            encoding="utf-8",
        )
        html_path.write_text(
            write_runbook_review_html(runbook, review_html_path=html_path, repo_root=REPO_ROOT),
            encoding="utf-8",
        )
        print(f"Regenerated review: {md_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    raise SystemExit(main())
