"""Run Shared Stage 9 corpus validation."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import typer

from shared_pipeline_stages.stage_9.corpus_validator import validate_corpus

app = typer.Typer(add_completion=False)


@app.command()
def main(
    stage7_dir: Path = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks",
        "--stage7-dir",
        exists=True,
        readable=True,
    ),
    stage8_dir: Path = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks",
        "--stage8-dir",
        exists=True,
        readable=True,
    ),
    stage85_dir: Path | None = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_8_5_relationship_linking",
        "--stage85-dir",
        exists=True,
        readable=True,
    ),
    output_dir: Path = typer.Option(REPO_ROOT / "shared_pipeline_stages/data/output/shared", "--output-dir"),
    source_root: list[Path] = typer.Option(
        [],
        "--source-root",
        exists=True,
        readable=True,
        help="Expected per-source roots that should appear in Stage 8.5 graph.",
    ),
) -> None:
    result = validate_corpus(
        stage7_dir=stage7_dir,
        stage8_dir=stage8_dir,
        stage85_dir=stage85_dir,
        output_dir=output_dir,
        expected_source_roots=source_root or None,
    )
    stage_dir = output_dir / "stage_9_validation" if output_dir.name != "stage_9_validation" else output_dir
    typer.echo(f"Validation report written:   {stage_dir / 'validation_report.json'}")
    typer.echo(f"Passed:                      {result.passed}")
    typer.echo(f"Errors:                      {result.error_count}")
    typer.echo(f"Warnings:                    {result.warning_count}")
    typer.echo(f"Runbooks:                    {result.runbook_count}")
    typer.echo(f"Playbooks:                   {result.playbook_count}")
    typer.echo(f"Relationship links:          {result.relationship_link_count}")
    if not result.passed:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
