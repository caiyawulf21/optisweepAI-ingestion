"""Run Stage 8 source relationship linking."""

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

from optisweep_ingestion.stage8_relationship_linking import link_source_relationships
from optisweep_ingestion.stage_paths import stage_dir

app = typer.Typer(add_completion=False)


@app.command()
def main(
    output_dir: Path = typer.Option(..., "--output-dir"),
    source_artifacts: Path | None = typer.Option(None, "--source-artifacts", exists=True, readable=True),
    operational_context: Path | None = typer.Option(None, "--operational-context", exists=True, readable=True),
    finalized_runbooks_dir: Path | None = typer.Option(None, "--finalized-runbooks-dir", exists=True, file_okay=False, dir_okay=True, readable=True),
    runbook_candidates: Path | None = typer.Option(None, "--runbook-candidates", exists=True, readable=True),
    no_shared_artifact_inference: bool = typer.Option(False, "--no-shared-artifact-inference"),
) -> None:
    report = link_source_relationships(
        output_dir=output_dir,
        source_artifacts_path=source_artifacts,
        operational_context_path=operational_context,
        finalized_runbooks_dir=finalized_runbooks_dir,
        runbook_candidates_path=runbook_candidates,
        infer_shared_artifact_links=not no_shared_artifact_inference,
    )
    stage8_dir = stage_dir(output_dir, "8")
    typer.echo(f"Relationship links written:          {stage8_dir / 'relationship_links.json'}")
    typer.echo(f"Linked artifacts written:            {stage8_dir / 'source_artifacts_linked.json'}")
    typer.echo(f"Linked context written:              {stage8_dir / 'operational_context_linked.json'}")
    typer.echo(f"Linked runbooks written:               {stage8_dir / 'finalized_runbooks_linked'}")
    typer.echo(f"Relationship linking report written: {stage8_dir / 'relationship_linking_report.json'}")
    typer.echo(f"Link count:                          {report['link_stats']['link_count']}")
    typer.echo(f"Contexts with runbook links:         {report['link_stats']['contexts_with_runbook_links']}")


if __name__ == "__main__":
    app()
