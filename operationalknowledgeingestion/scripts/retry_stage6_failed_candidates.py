"""Retry Stage 6 finalization for specific failed candidate IDs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_PARENT = ROOT.parent
SRC = ROOT / "src"
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_ingestion.stage6_runbook_finalization import (
    AzureOpenAIRunbookFinalizationClient,
    finalize_operational_runbooks,
)

app = typer.Typer(add_completion=False)


@app.command()
def main(
    runbook_candidates: Path = typer.Option(..., "--runbook-candidates", exists=True, readable=True),
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    operational_context: Path = typer.Option(..., "--operational-context", exists=True, readable=True),
    source_bundle: Path = typer.Option(..., "--source-bundle", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    candidate_id: list[str] = typer.Option(..., "--candidate-id"),
    total_candidate_count: int | None = typer.Option(None, "--total-candidate-count"),
    max_workers: int = typer.Option(4, "--max-workers"),
) -> None:
    output_dir = Path(output_dir)
    report_path = output_dir / "runbook_finalization_report.json"
    if not report_path.exists():
        raise typer.BadParameter(f"Missing report: {report_path}")

    wanted = set(candidate_id)
    all_candidates = json.loads(Path(runbook_candidates).read_text(encoding="utf-8"))
    retry = [c for c in all_candidates if c.get("candidate_id") in wanted]
    if len(retry) != len(wanted):
        found = {c.get("candidate_id") for c in retry}
        missing = sorted(wanted - found)
        raise typer.BadParameter(f"Candidates not found in Stage 5 file: {missing}")

    retry_path = output_dir / "_retry_runbook_candidates.json"
    retry_path.write_text(json.dumps(retry, indent=2), encoding="utf-8")

    existing = json.loads(report_path.read_text(encoding="utf-8"))
    client = AzureOpenAIRunbookFinalizationClient()
    finalized, retry_report = finalize_operational_runbooks(
        runbook_candidates_path=retry_path,
        source_artifacts_path=source_artifacts,
        operational_context_path=operational_context,
        source_bundle_path=source_bundle,
        output_dir=output_dir,
        llm_client=client,
        llm_used=True,
        max_workers=max_workers,
    )

    prev_failed = {f["candidate_id"] for f in existing.get("failed_candidates", [])}
    still_failed = {f["candidate_id"] for f in retry_report.get("failed_candidates", [])}
    succeeded = prev_failed & (wanted - still_failed)

    finalized_count = existing["finalized_runbook_count"] + len(succeeded)
    merged_failed_by_id = {
        f["candidate_id"]: f
        for f in existing.get("failed_candidates", [])
        if f["candidate_id"] not in succeeded
    }
    for failure in retry_report.get("failed_candidates", []):
        merged_failed_by_id[failure["candidate_id"]] = failure
    merged_failed = list(merged_failed_by_id.values())

    existing["candidate_count"] = total_candidate_count or existing.get("candidate_count", len(all_candidates))
    existing["finalized_runbook_count"] = finalized_count
    existing["failed_candidate_count"] = len(merged_failed)
    existing["failed_candidates"] = merged_failed
    report_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    retry_path.unlink(missing_ok=True)

    typer.echo(f"Retry finalized: {len(finalized)}/{len(retry)}")
    typer.echo(f"Total finalized: {finalized_count}/{existing['candidate_count']}")
    typer.echo(f"Remaining failures: {len(merged_failed)}")


if __name__ == "__main__":
    app()
