"""Run Stage 6 source runbook finalization."""

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
from optisweep_ingestion.stage6_runbook_finalization import AzureOpenAIRunbookFinalizationClient, finalize_operational_runbooks

app = typer.Typer(add_completion=False)


@app.command()
def main(
    runbook_candidates: Path = typer.Option(..., "--runbook-candidates", exists=True, readable=True),
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    operational_context: Path = typer.Option(..., "--operational-context", exists=True, readable=True),
    source_bundle: Path = typer.Option(..., "--source-bundle", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    max_workers: int = typer.Option(4, "--max-workers"),
    prompt_path: Path | None = typer.Option(None, "--prompt-path"),
) -> None:
    output_dir = stage_dir(output_dir, "6")
    client = AzureOpenAIRunbookFinalizationClient(prompt_path=prompt_path)
    finalized, report = finalize_operational_runbooks(
        runbook_candidates_path=runbook_candidates,
        source_artifacts_path=source_artifacts,
        operational_context_path=operational_context,
        source_bundle_path=source_bundle,
        output_dir=output_dir,
        llm_client=client,
        llm_used=True,
        max_workers=max_workers,
    )
    typer.echo(f"Finalized runbooks written: {output_dir / 'finalized_runbooks'}")
    typer.echo(f"Review markdown written:     {output_dir / 'review_markdown' / 'runbooks'}")
    typer.echo(f"Review HTML written:         {output_dir / 'review_markdown' / 'runbooks'}")
    typer.echo(f"Finalization report written: {output_dir / 'runbook_finalization_report.json'}")
    typer.echo(f"Finalized runbook count:     {len(finalized)}")
    typer.echo(f"Failed candidates:           {report.get('failed_candidate_count', 0)}")


if __name__ == "__main__":
    app()
