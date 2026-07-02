"""Run Shared Stage 6.5 runbook pool generation from finalized runbooks."""

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
from optisweep_ingestion.stage6_5_runbook_pool import build_candidate_pool

app = typer.Typer(add_completion=False)


@app.command()
def main(
    candidates: list[Path] = typer.Option(
        ...,
        "--candidates",
        exists=True,
        readable=True,
        help="Candidate JSON file. Repeat for multiple sources.",
    ),
    output_dir: Path = typer.Option(..., "--output-dir"),
) -> None:
    output_dir = stage_dir(output_dir, "6.5")
    pool = build_candidate_pool(candidate_paths=candidates, output_dir=output_dir)
    typer.echo(f"Runbook pool written:         {output_dir / 'candidate_pool.json'}")
    typer.echo(f"Candidate clusters generated: {pool.candidate_cluster_count}")


if __name__ == "__main__":
    app()
