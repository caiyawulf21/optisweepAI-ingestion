"""Quarantine finalized Stage 6 runbooks that fail live-runbook eligibility."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys

import typer

ROOT = Path(__file__).resolve().parents[1]
PROJECT_PARENT = ROOT.parent
SRC = ROOT / "src"
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from shared_pipeline_stages.runbook_eligibility import eligibility_errors_for_runbook
from optisweep_ingestion.utils.json_utils import read_json, write_json

app = typer.Typer(add_completion=False)


@app.command()
def main(
    stage6_dir: Path = typer.Option(..., "--stage6-dir", exists=True, file_okay=False),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    finalized_dir = stage6_dir / "finalized_runbooks"
    review_dir = stage6_dir / "review_markdown" / "runbooks"
    quarantine_dir = stage6_dir / "quarantined_not_runbooks"
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    moved = 0
    kept = 0
    for path in sorted(finalized_dir.glob("*.json")):
        runbook = read_json(path)
        errors = eligibility_errors_for_runbook(runbook)
        if not errors:
            kept += 1
            continue
        moved += 1
        typer.echo(f"QUARANTINE {path.name}: {'; '.join(errors)}")
        if dry_run:
            continue
        dest = quarantine_dir / path.name
        write_json(dest, {**runbook, "validation_status": "rejected_not_a_runbook", "quarantine_reasons": errors})
        path.unlink(missing_ok=True)
        for suffix in (".md", ".html"):
            review_path = review_dir / f"{path.stem}{suffix}"
            if review_path.exists():
                review_dest = quarantine_dir / review_path.name
                shutil.move(str(review_path), str(review_dest))
    typer.echo(f"Kept: {kept}")
    typer.echo(f"Quarantined: {moved}")
    typer.echo(f"Quarantine dir: {quarantine_dir}")


if __name__ == "__main__":
    app()
