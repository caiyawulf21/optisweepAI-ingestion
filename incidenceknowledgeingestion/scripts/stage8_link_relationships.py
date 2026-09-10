"""Run incident Stage 8 source relationship linking."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
SRC = ROOT / "src"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_incidence_ingestion.stage8_relationship_linking import link_incident_relationships

app = typer.Typer(add_completion=False)


@app.command()
def main(
    output_dir: Path = typer.Option(..., "--output-dir"),
    source_artifacts: Path | None = typer.Option(None, "--source-artifacts", exists=True, readable=True),
    canonical_incident_record: Path | None = typer.Option(None, "--canonical-incident-record", exists=True, readable=True),
    timeline_events: Path | None = typer.Option(None, "--timeline-events", exists=True, readable=True),
    finalized_runbooks_dir: Path | None = typer.Option(None, "--finalized-runbooks-dir", exists=True, file_okay=False, dir_okay=True, readable=True),
    runbook_candidates: Path | None = typer.Option(None, "--runbook-candidates", exists=True, readable=True),
    no_shared_artifact_inference: bool = typer.Option(False, "--no-shared-artifact-inference"),
) -> None:
    report = link_incident_relationships(
        output_dir=output_dir,
        source_artifacts_path=source_artifacts,
        canonical_incident_record_path=canonical_incident_record,
        timeline_events_path=timeline_events,
        finalized_runbooks_dir=finalized_runbooks_dir,
        runbook_candidates_path=runbook_candidates,
        infer_shared_artifact_links=not no_shared_artifact_inference,
    )
    stage8_dir = output_dir / "stage_8_relationship_linking"
    typer.echo(f"Relationship links written:          {stage8_dir / 'relationship_links.json'}")
    typer.echo(f"Linked artifacts written:            {stage8_dir / 'source_artifacts_linked.json'}")
    typer.echo(f"Linked incident record written:      {stage8_dir / 'canonical_incident_record_linked.json'}")
    typer.echo(f"Linked timeline written:             {stage8_dir / 'timeline_events_linked.json'}")
    typer.echo(f"Linked runbooks written:               {stage8_dir / 'finalized_runbooks_linked'}")
    typer.echo(f"Relationship linking report written: {stage8_dir / 'relationship_linking_report.json'}")
    typer.echo(f"Link count:                          {report['link_stats']['link_count']}")
    typer.echo(f"Incident runbook links:              {report['link_stats']['incident_runbook_links']}")


if __name__ == "__main__":
    app()
