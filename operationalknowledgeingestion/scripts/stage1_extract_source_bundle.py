"""Run deterministic Stage 1 source knowledge extraction."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_ingestion.stage_paths import stage_dir
from optisweep_ingestion.stage1_source_bundle import build_source_bundle

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_pdf: Path = typer.Option(..., "--source-pdf", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    source_bundle_id: str | None = typer.Option(None, "--source-bundle-id"),
    source_document_id: str | None = typer.Option(None, "--source-document-id"),
    source_id: str | None = typer.Option(None, "--source-id"),
    source_type: str = typer.Option("manual", "--source-type"),
    source_title: str | None = typer.Option(None, "--source-title"),
    source_version: str | None = typer.Option(None, "--source-version"),
    ingestion_batch_id: str | None = typer.Option(None, "--ingestion-batch-id"),
) -> None:
    output_dir = stage_dir(output_dir, "1")
    bundle = build_source_bundle(
        source_pdf=source_pdf,
        output_dir=output_dir,
        source_bundle_id=source_bundle_id,
        source_document_id=source_document_id,
        source_id=source_id,
        source_type=source_type,
        source_title=source_title,
        source_version=source_version,
        ingestion_batch_id=ingestion_batch_id,
    )
    output_path = output_dir / "source_bundle.json"
    typer.echo(f"Wrote: {output_path}")
    typer.echo(f"Source ID: {bundle.source_metadata.source_id}")
    typer.echo(f"Source type: {bundle.source_metadata.source_type}")
    typer.echo(f"Ingestion batch: {bundle.source_metadata.ingestion_batch_id}")
    typer.echo(f"Pages: {len(bundle.pages)}")
    typer.echo(f"Sections: {len(bundle.sections)}")
    typer.echo(f"Figure refs: {len(bundle.figure_refs)}")
    typer.echo(f"Table refs: {len(bundle.table_refs)}")
    typer.echo("LLM used: false")


if __name__ == "__main__":
    app()
