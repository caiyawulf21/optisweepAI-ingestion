"""CLI for cumulative Stage 11 publish (used by LangGraph shared publish too)."""

from __future__ import annotations

from pathlib import Path
import sys

import typer

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared_pipeline_stages.stage_11.cumulative_publish import (
    DEFAULT_INCIDENTS_ROOT,
    DEFAULT_SOURCE_ROOTS,
    run_cumulative_stage11,
)

app = typer.Typer(add_completion=False)


@app.command()
def main(
    baseline_dir: Path | None = typer.Option(None, "--baseline-dir"),
    output_dir: Path = typer.Option(REPO_ROOT / "shared_pipeline_stages/data/output/shared", "--output-dir"),
    incidents_root: Path = typer.Option(DEFAULT_INCIDENTS_ROOT, "--incidents-root"),
    source_root: list[Path] = typer.Option(
        DEFAULT_SOURCE_ROOTS,
        "--source-root",
        exists=True,
        readable=True,
        help="Source roots to assemble into the candidate corpus before merging against the baseline.",
    ),
    deprecations: Path | None = typer.Option(None, "--deprecations"),
    publish: bool = typer.Option(False, "--publish"),
    skip_assemble: bool = typer.Option(False, "--skip-assemble"),
    publish_version_id: str | None = typer.Option(None, "--publish-version-id"),
    skip_smoke: bool = typer.Option(False, "--skip-smoke"),
) -> None:
    result = run_cumulative_stage11(
        output_dir=output_dir,
        baseline_dir=baseline_dir,
        incidents_root=incidents_root,
        source_roots=source_root,
        deprecations=deprecations,
        publish=publish,
        skip_assemble=skip_assemble,
        publish_version_id=publish_version_id,
        run_smoke=not skip_smoke,
        copy_to_delivery=True,
    )
    typer.echo(f"PUBLISH_VERSION_ID={result.publish_version_id}")
    typer.echo(f"cases={result.case_ids}")
    typer.echo(f"playbooks={len(result.playbook_ids)}")
    typer.echo(f"smoke_passed={result.smoke_passed}")
    typer.echo(f"uploaded={result.uploaded}")
    typer.echo(f"delivery={result.delivery_dir}")
    for warning in result.warnings[:20]:
        typer.echo(f"warning: {warning}")


if __name__ == "__main__":
    app()
