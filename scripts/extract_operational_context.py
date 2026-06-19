"""Run Stage 4 LLM operational context extraction."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_ingestion.tools.operational_context_extractor import (
    AzureOpenAIContextClient,
    extract_operational_context,
)

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_bundle: Path = typer.Option(..., "--source-bundle", exists=True, readable=True),
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    llm: bool = typer.Option(False, "--llm", help="Use Azure OpenAI for extraction."),
) -> None:
    if not llm:
        raise typer.BadParameter(
            "Stage 4 requires --llm. Fake context generation is not supported."
        )
    client = AzureOpenAIContextClient()
    contexts, report = extract_operational_context(
        source_bundle_path=source_bundle,
        source_artifacts_path=source_artifacts,
        output_dir=output_dir,
        llm_client=client,
        llm_used=True,
    )
    typer.echo(f"Operational context written: {output_dir / 'operational_context.json'}")
    typer.echo(f"Extraction report written:   {output_dir / 'operational_context_extraction_report.json'}")
    typer.echo(f"Context records extracted:   {report['context_count']}")
    typer.echo(f"Failed packets:              {len(report['failed_packets'])}")
    if report["warnings"]:
        typer.echo(f"Warnings:                    {len(report['warnings'])}")
    heartbeat = report["priority_context_check"]["heartbeat_stats"]
    typer.echo(f"Heartbeat context found:     {str(heartbeat['found']).lower()}")
    typer.echo(f"Heartbeat has artifact ref:  {str(heartbeat['has_artifact_ref']).lower()}")


if __name__ == "__main__":
    app()
