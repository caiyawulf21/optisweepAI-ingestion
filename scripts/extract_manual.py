"""Run deterministic Stage 1 manual extraction."""

from __future__ import annotations

from pathlib import Path

import typer

from optisweep_ingestion.tools.source_bundle_builder import build_source_bundle

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_pdf: Path = typer.Option(..., "--source-pdf", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    source_bundle_id: str | None = typer.Option(None, "--source-bundle-id"),
    source_document_id: str | None = typer.Option(None, "--source-document-id"),
) -> None:
    bundle = build_source_bundle(
        source_pdf=source_pdf,
        output_dir=output_dir,
        source_bundle_id=source_bundle_id,
        source_document_id=source_document_id,
    )
    output_path = output_dir / "source_bundle.json"
    typer.echo(f"Wrote: {output_path}")
    typer.echo(f"Pages: {len(bundle.pages)}")
    typer.echo(f"Sections: {len(bundle.sections)}")
    typer.echo(f"Figure refs: {len(bundle.figure_refs)}")
    typer.echo(f"Table refs: {len(bundle.table_refs)}")
    typer.echo("LLM used: false")


if __name__ == "__main__":
    app()
