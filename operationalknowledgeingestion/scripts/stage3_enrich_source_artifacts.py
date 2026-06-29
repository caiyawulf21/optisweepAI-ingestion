"""Run Stage 3 LLM source artifact enrichment."""

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

from optisweep_ingestion.stage_paths import stage_dir
from optisweep_ingestion.tools.artifact_enricher import AzureOpenAIArtifactClient, enrich_source_artifacts

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    artifact_report: Path = typer.Option(..., "--artifact-report", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    llm: bool = typer.Option(False, "--llm", help="Use Azure OpenAI for enrichment."),
    max_workers: int = typer.Option(4, "--max-workers", min=1, max=8, help="Concurrent LLM calls."),
) -> None:
    if not llm:
        raise typer.BadParameter("Stage 3 requires --llm. Fake enrichment is not supported.")
    output_dir = stage_dir(output_dir, "3")
    client = AzureOpenAIArtifactClient()
    artifacts, report = enrich_source_artifacts(source_artifacts, artifact_report, output_dir, client, llm_used=True, max_workers=max_workers)
    typer.echo(f"Source artifacts enriched: {output_dir / 'source_artifacts_enriched.json'}")
    typer.echo(f"Enrichment report written: {output_dir / 'artifact_enrichment_report.json'}")
    typer.echo(f"Input artifacts: {report['input_artifact_count']}")
    typer.echo(f"Enriched artifacts: {report['enriched_artifact_count']}")
    typer.echo(f"Failed artifacts: {report['failed_artifact_count']}")
    typer.echo(f"Heartbeat enriched: {str(report['heartbeat_check']['enriched']).lower()}")


if __name__ == "__main__":
    app()
