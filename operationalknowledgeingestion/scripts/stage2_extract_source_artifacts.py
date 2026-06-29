"""Run deterministic Stage 2 manual artifact extraction."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_ingestion.stage_paths import stage_dir
from optisweep_ingestion.tools.artifact_extractor import extract_source_artifacts

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_bundle: Path = typer.Option(..., "--source-bundle", exists=True, readable=True),
    source_pdf: Path = typer.Option(..., "--source-pdf", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
) -> None:
    output_dir = stage_dir(output_dir, "2")
    artifacts, report = extract_source_artifacts(source_bundle, source_pdf, output_dir)
    typer.echo(f"Source artifacts written: {output_dir / 'source_artifacts.json'}")
    typer.echo(f"Artifact report written: {output_dir / 'artifact_extraction_report.json'}")
    typer.echo(f"Artifacts created: {len(artifacts)}")
    typer.echo(f"Images saved: {report['total_images_saved']}")
    typer.echo(f"Missing figure images: {len(report['missing_figure_images'])}")
    typer.echo(f"Heartbeat artifact found: {str(report['heartbeat_artifact_check']['artifact_found']).lower()}")


if __name__ == "__main__":
    app()
