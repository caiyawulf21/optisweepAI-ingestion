"""Copy finalized runbook markdown and assets into sme_review_runbooks for SME review."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEST_ROOT = REPO_ROOT / "sme_review_runbooks"

README_TEXT = """# SME Review Runbooks

Copies of finalized runbook markdown files for easy SME review without navigating pipeline output folders.

Each source folder includes an `assets/` directory with the images referenced by the markdown files (`![](assets/...)`).

These files are snapshots copied from ingestion stage outputs. Edit and approve in the source pipeline outputs; refresh this folder when new runbooks are finalized.

## Sources

| Folder | Origin |
| --- | --- |
| `manual_optisweep_om_v3/` | Operational manual Stage 6 `review_markdown/runbooks/` |
| `training_video_day1/` | Training video Stage 6 `review_markdown/runbooks/` |
| `case_228086/` | Incident Case 228086 Stage 6 finalized runbook + Stage 5 candidate review |
| `case_228723/` | Incident Case 228723 Stage 5 runbook candidate review |

## File Types

- `*.md` in each source root (except `stage_5_runbook_candidates/`) are finalized runbook markdown from `review_markdown/runbooks/`.
- `stage_5_runbook_candidates/runbook_candidate_review.md` is the aggregated Stage 5 candidate review for incident cases.
- Do not use `*_review.md` wrapper files from stage output roots; those are review summaries, not the per-runbook markdown.

## Review Notes

- Each markdown file corresponds to one finalized runbook.
- Default validation status is `needs_sme_review` until explicitly approved.
- For full extraction reports and JSON records, see the source output paths documented in each ingestion area README.

## Refresh

From the repo root:

```powershell
python shared_pipeline_stages/scripts/sync_sme_review_runbooks.py
```
"""


@dataclass(frozen=True)
class SourceConfig:
    name: str
    runbooks_dir: Path
    extra_files: tuple[tuple[Path, Path], ...] = ()


def _source_configs() -> list[SourceConfig]:
    return [
        SourceConfig(
            name="manual_optisweep_om_v3",
            runbooks_dir=REPO_ROOT
            / "operationalknowledgeingestion/data/output/manual_optisweep_om_v3/stage_6_finalized_runbooks/review_markdown/runbooks",
        ),
        SourceConfig(
            name="training_video_day1",
            runbooks_dir=REPO_ROOT
            / "operationalknowledgeingestion/data/output/training_video_day1/stage_6_finalized_runbooks/review_markdown/runbooks",
        ),
        SourceConfig(
            name="case_228086",
            runbooks_dir=REPO_ROOT
            / "incidenceknowledgeingestion/data/output/incidents/case_228086/stage_6_finalized_runbooks/review_markdown/runbooks",
            extra_files=(
                (
                    REPO_ROOT
                    / "incidenceknowledgeingestion/data/output/incidents/case_228086/stage_5_runbook_candidates/runbook_candidate_review.md",
                    Path("case_228086/stage_5_runbook_candidates/runbook_candidate_review.md"),
                ),
            ),
        ),
        SourceConfig(
            name="case_228723",
            runbooks_dir=REPO_ROOT
            / "incidenceknowledgeingestion/data/output/incidents/case_228723/stage_6_finalized_runbooks/review_markdown/runbooks",
            extra_files=(
                (
                    REPO_ROOT
                    / "incidenceknowledgeingestion/data/output/incidents/case_228723/stage_5_runbook_candidates/runbook_candidate_review.md",
                    Path("case_228723/stage_5_runbook_candidates/runbook_candidate_review.md"),
                ),
            ),
        ),
    ]


def sync_sme_review_runbooks(dest_root: Path = DEST_ROOT) -> dict[str, dict[str, int]]:
    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True)

    summary: dict[str, dict[str, int]] = {}
    for config in _source_configs():
        dest = dest_root / config.name
        dest.mkdir(parents=True)

        markdown_count = 0
        if config.runbooks_dir.is_dir():
            for markdown in config.runbooks_dir.glob("*.md"):
                shutil.copy2(markdown, dest / markdown.name)
                markdown_count += 1

            assets_src = config.runbooks_dir / "assets"
            if assets_src.is_dir():
                shutil.copytree(assets_src, dest / "assets")

        for src, rel_dest in config.extra_files:
            target = dest_root / rel_dest
            target.parent.mkdir(parents=True, exist_ok=True)
            if src.is_file():
                shutil.copy2(src, target)

        image_count = len(list((dest / "assets").glob("*"))) if (dest / "assets").is_dir() else 0
        summary[config.name] = {"markdown": markdown_count, "images": image_count}

    (dest_root / "README.md").write_text(README_TEXT, encoding="utf-8")
    return summary


def main() -> None:
    summary = sync_sme_review_runbooks()
    for name, counts in summary.items():
        print(f"{name}: {counts['markdown']} markdown, {counts['images']} images")
    print(f"Wrote SME review runbooks under {DEST_ROOT}")


if __name__ == "__main__":
    main()
