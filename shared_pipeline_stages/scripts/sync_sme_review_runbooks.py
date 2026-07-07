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
| `stage_8_playbooks/prompt_a_one_per_incident/` | Shared Stage 8 Prompt A finalized playbook review (MD + HTML) |
| `stage_8_playbooks/prompt_b_multi_flow/` | Shared Stage 8 Prompt B finalized playbook review (MD + HTML) |

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
    include_html: bool = False


@dataclass(frozen=True)
class PlaybookReviewConfig:
    variant_key: str
    playbooks_dir: Path


def _playbook_review_configs() -> list[PlaybookReviewConfig]:
    stage8_root = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks"
    return [
        PlaybookReviewConfig(
            variant_key="prompt_a_one_per_incident",
            playbooks_dir=stage8_root / "prompt_a_one_per_incident/review_markdown/playbooks",
        ),
        PlaybookReviewConfig(
            variant_key="prompt_b_multi_flow",
            playbooks_dir=stage8_root / "prompt_b_multi_flow/review_markdown/playbooks",
        ),
    ]


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
        html_count = 0
        if config.runbooks_dir.is_dir():
            for markdown in config.runbooks_dir.glob("*.md"):
                shutil.copy2(markdown, dest / markdown.name)
                markdown_count += 1
            if config.include_html:
                for html_file in config.runbooks_dir.glob("*.html"):
                    shutil.copy2(html_file, dest / html_file.name)
                    html_count += 1

            assets_src = config.runbooks_dir / "assets"
            if assets_src.is_dir():
                shutil.copytree(assets_src, dest / "assets")

        for src, rel_dest in config.extra_files:
            target = dest_root / rel_dest
            target.parent.mkdir(parents=True, exist_ok=True)
            if src.is_file():
                shutil.copy2(src, target)

        image_count = len(list((dest / "assets").glob("*"))) if (dest / "assets").is_dir() else 0
        summary[config.name] = {
            "markdown": markdown_count,
            "html": html_count,
            "images": image_count,
        }

    stage8_dest = dest_root / "stage_8_playbooks"
    stage8_dest.mkdir(parents=True, exist_ok=True)
    for config in _playbook_review_configs():
        dest = stage8_dest / config.variant_key
        dest.mkdir(parents=True, exist_ok=True)
        markdown_count = 0
        html_count = 0
        if not config.playbooks_dir.is_dir():
            summary[f"stage_8_playbooks/{config.variant_key}"] = {
                "markdown": 0,
                "html": 0,
                "images": 0,
            }
            continue
        for markdown in config.playbooks_dir.glob("*.md"):
            shutil.copy2(markdown, dest / markdown.name)
            markdown_count += 1
        for html_file in config.playbooks_dir.glob("*.html"):
            shutil.copy2(html_file, dest / html_file.name)
            html_count += 1
        assets_src = config.playbooks_dir / "assets"
        if assets_src.is_dir():
            shutil.copytree(assets_src, dest / "assets")
        image_count = len(list((dest / "assets").glob("*"))) if (dest / "assets").is_dir() else 0
        summary[f"stage_8_playbooks/{config.variant_key}"] = {
            "markdown": markdown_count,
            "html": html_count,
            "images": image_count,
        }

    (dest_root / "README.md").write_text(README_TEXT, encoding="utf-8")
    return summary


def main() -> None:
    summary = sync_sme_review_runbooks()
    for name, counts in summary.items():
        html_note = f", {counts.get('html', 0)} html" if counts.get("html") else ""
        print(f"{name}: {counts['markdown']} markdown{html_note}, {counts['images']} images")
    print(f"Wrote SME review runbooks under {DEST_ROOT}")


if __name__ == "__main__":
    main()
