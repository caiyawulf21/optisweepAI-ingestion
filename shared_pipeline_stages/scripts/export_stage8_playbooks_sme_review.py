"""Export Shared Stage 8 playbook review artifacts into an SME review subfolder."""

from __future__ import annotations

import shutil
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import typer

app = typer.Typer(add_completion=False)

STAGE8_ROOT = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks"
SME_ROOT = REPO_ROOT / "sme_review_runbooks"

VARIANTS = (
    ("prompt_a_one_per_incident", "prompt_a_one_per_incident"),
    ("prompt_b_multi_flow", "prompt_b_multi_flow"),
)


def export_stage8_playbooks(
    *,
    subfolder: str,
    stage8_root: Path = STAGE8_ROOT,
    sme_root: Path = SME_ROOT,
) -> dict[str, int]:
    dest_root = sme_root / subfolder
    dest_root.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for variant_key, dest_name in VARIANTS:
        source_playbooks = stage8_root / variant_key / "review_markdown" / "playbooks"
        dest = dest_root / dest_name
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        markdown_count = 0
        html_count = 0
        if source_playbooks.is_dir():
            for markdown in source_playbooks.glob("*.md"):
                if markdown.name == "README.md":
                    continue
                shutil.copy2(markdown, dest / markdown.name)
                markdown_count += 1
            for html_file in source_playbooks.glob("*.html"):
                shutil.copy2(html_file, dest / html_file.name)
                html_count += 1
            assets_src = source_playbooks / "assets"
            if assets_src.is_dir():
                shutil.copytree(assets_src, dest / "assets")
        variant_root = stage8_root / variant_key
        for artifact_name in ("canonical_playbooks.json", "playbook_runbook_links.json"):
            artifact = variant_root / artifact_name
            if artifact.is_file():
                shutil.copy2(artifact, dest / artifact_name)
        counts[dest_name] = markdown_count + html_count
    comparison = stage8_root / "stage_8_comparison_report.json"
    if comparison.is_file():
        shutil.copy2(comparison, dest_root / comparison.name)
    return counts


@app.command()
def main(
    subfolder: str = typer.Option(
        "stage_8_playbooks_linking_guards",
        "--subfolder",
        help="Destination folder under sme_review_runbooks/",
    ),
    stage8_root: Path = typer.Option(STAGE8_ROOT, "--stage8-root", exists=True, readable=True),
    sme_root: Path = typer.Option(SME_ROOT, "--sme-root", exists=True, readable=True),
) -> None:
    counts = export_stage8_playbooks(subfolder=subfolder, stage8_root=stage8_root, sme_root=sme_root)
    dest = sme_root / subfolder
    for name, total in counts.items():
        typer.echo(f"{name}: {total} review files")
    typer.echo(f"Exported Stage 8 playbooks to {dest}")


if __name__ == "__main__":
    app()
