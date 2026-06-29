"""Prepare training video bundle outputs for shared Stage 4/5 extraction."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_ingestion.tools.training_video_preparer import prepare_training_video_for_extraction
from optisweep_ingestion.stage_paths import stage_dir

app = typer.Typer(add_completion=False)


@app.command()
def main(
    training_segments: Path = typer.Option(..., "--training-segments", exists=True, readable=True),
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
) -> None:
    output_dir = stage_dir(output_dir, "2")
    bundle, artifacts, report = prepare_training_video_for_extraction(
        training_segments_path=training_segments,
        source_artifacts_path=source_artifacts,
        output_dir=output_dir,
    )
    typer.echo(f"Source bundle written:             {output_dir / 'source_bundle.json'}")
    typer.echo(f"Prepared artifacts written:        {output_dir / 'source_artifacts_enriched.json'}")
    typer.echo(f"Preparation report written:        {output_dir / 'training_video_preparation_report.json'}")
    typer.echo(f"Sections created:                  {len(bundle['sections'])}")
    typer.echo(f"Artifacts prepared:                {len(artifacts)}")
    typer.echo(f"Warnings:                          {len(report['warnings'])}")


if __name__ == "__main__":
    app()
