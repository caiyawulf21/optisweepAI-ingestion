"""Regenerate Stage 6 review markdown and HTML from finalized runbook JSON."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT_PARENT = ROOT.parent
SRC = ROOT / "src"
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_ingestion.stage6_runbook_finalization import (
    write_runbook_review_html,
    write_runbook_review_markdown,
)
from optisweep_ingestion.utils.json_utils import read_json

app = typer.Typer(add_completion=False)


@app.command()
def main(
    stage6_dir: Path = typer.Option(..., "--stage6-dir", exists=True, file_okay=False),
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
) -> None:
    artifact_index = {
        str(item.get("artifact_id")): item
        for item in read_json(source_artifacts)
        if isinstance(item, dict) and item.get("artifact_id")
    }
    finalized_dir = stage6_dir / "finalized_runbooks"
    review_dir = stage6_dir / "review_markdown" / "runbooks"
    review_dir.mkdir(parents=True, exist_ok=True)
    runbook_paths = sorted(finalized_dir.glob("*.json"))
    regenerated = 0
    for runbook_path in runbook_paths:
        runbook = read_json(runbook_path)
        candidate_id = runbook_path.stem
        review_path = review_dir / f"{candidate_id}.md"
        html_path = review_dir / f"{candidate_id}.html"
        review_path.write_text(
            write_runbook_review_markdown(
                runbook,
                artifact_index=artifact_index,
                review_markdown_path=review_path,
            ),
            encoding="utf-8",
        )
        html_path.write_text(
            write_runbook_review_html(
                runbook,
                artifact_index=artifact_index,
                review_html_path=html_path,
            ),
            encoding="utf-8",
        )
        regenerated += 1
    assets_dir = review_dir / "assets"
    asset_count = len(list(assets_dir.glob("*"))) if assets_dir.exists() else 0
    typer.echo(f"Regenerated review outputs: {regenerated}")
    typer.echo(f"Review markdown/HTML dir:     {review_dir}")
    typer.echo(f"Shared assets copied:         {asset_count}")


if __name__ == "__main__":
    app()
