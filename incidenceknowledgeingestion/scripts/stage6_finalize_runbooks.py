"""Run Stage 6 incident source runbook finalization."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
SRC = ROOT / "src"
OPERATIONAL_SRC = REPO_ROOT / "operationalknowledgeingestion" / "src"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(OPERATIONAL_SRC) not in sys.path:
    sys.path.insert(0, str(OPERATIONAL_SRC))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_incidence_ingestion.stage6_runbook_finalization import (
    AzureOpenAIStage6RunbookFinalizationClient,
    create_stage6_incident_runbooks,
)

app = typer.Typer(add_completion=False)


@app.command()
def main(
    runbook_candidates: Path = typer.Option(..., "--runbook-candidates", exists=True, readable=True),
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    canonical_incident_record: Path = typer.Option(..., "--canonical-incident-record", exists=True, readable=True),
    timeline_events: Path = typer.Option(..., "--timeline-events", exists=True, readable=True),
    stage4_evidence_chunks: Path = typer.Option(..., "--stage4-evidence-chunks", exists=True, readable=True),
    source_package: Path = typer.Option(..., "--source-package", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    max_workers: int = typer.Option(4, "--max-workers"),
    prompt_path: Path | None = typer.Option(None, "--prompt-path"),
) -> None:
    output_dir = output_dir / "stage_6_finalized_runbooks"
    client = AzureOpenAIStage6RunbookFinalizationClient(prompt_path=prompt_path)
    finalized, report = create_stage6_incident_runbooks(
        runbook_candidates_path=runbook_candidates,
        source_artifacts_enriched_path=source_artifacts,
        canonical_incident_record_path=canonical_incident_record,
        timeline_events_path=timeline_events,
        stage4_evidence_chunks_path=stage4_evidence_chunks,
        source_package_path=source_package,
        output_dir=output_dir,
        llm_client=client,
        max_workers=max_workers,
    )
    typer.echo(f"Finalized runbooks written: {output_dir / 'finalized_runbooks'}")
    typer.echo(f"Review markdown written:     {output_dir}/*_review.md")
    typer.echo(f"Review HTML written:         {output_dir}/*_review.html")
    typer.echo(f"Legacy review markdown:    {output_dir / 'review_markdown' / 'runbooks'}")
    typer.echo(f"Finalization report written: {output_dir / 'runbook_finalization_report.json'}")
    typer.echo(f"Finalized runbook count:     {len(finalized)}")
    typer.echo(f"Failed candidates:           {report.get('failed_candidate_count', 0)}")


if __name__ == "__main__":
    app()
