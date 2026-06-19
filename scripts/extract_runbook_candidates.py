"""Run Stage 5 LLM runbook candidate discovery."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_ingestion.tools.runbook_candidate_extractor import (
    AzureOpenAIRunbookCandidateClient,
    extract_runbook_candidates,
)

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_bundle: Path = typer.Option(..., "--source-bundle", exists=True, readable=True),
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    operational_context: Path = typer.Option(..., "--operational-context", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    llm: bool = typer.Option(False, "--llm", help="Use Azure OpenAI for candidate discovery."),
    max_workers: int = typer.Option(4, "--max-workers", min=1, max=8, help="Concurrent LLM calls."),
    backfill_missing_sections: bool = typer.Option(
        False,
        "--backfill-missing-sections",
        help="Create conservative candidates for procedural sections still missing after LLM repair.",
    ),
) -> None:
    if not llm:
        raise typer.BadParameter("Stage 5 requires --llm. Fake runbook candidate generation is not supported.")
    client = AzureOpenAIRunbookCandidateClient()
    candidates, report = extract_runbook_candidates(
        source_bundle_path=source_bundle,
        source_artifacts_path=source_artifacts,
        operational_context_path=operational_context,
        output_dir=output_dir,
        llm_client=client,
        llm_used=True,
        max_workers=max_workers,
        backfill_missing_sections=backfill_missing_sections,
    )
    typer.echo(f"Runbook candidates written: {output_dir / 'runbook_candidates.json'}")
    typer.echo(f"Extraction report written:  {output_dir / 'runbook_candidate_extraction_report.json'}")
    typer.echo(f"Coverage report written:    {output_dir / 'runbook_candidate_coverage_report.json'}")
    typer.echo(f"Candidates extracted:       {len(candidates)}")
    typer.echo(f"Failed packets:             {len(report['failed_packets'])}")
    typer.echo(f"Dropped candidates:         {report['dropped_candidate_count']}")
    typer.echo(f"Deduped candidates:         {report['deduped_candidate_count']}")
    typer.echo(f"Missing sections:           {len(report['missing_candidate_sections'])}")
    typer.echo(f"Missing priorities:         {len(report['missing_priority_candidates'])}")


if __name__ == "__main__":
    app()
