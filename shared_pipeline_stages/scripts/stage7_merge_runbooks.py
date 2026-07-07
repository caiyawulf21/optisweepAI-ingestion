"""Run Shared Stage 7 cross-source runbook merge from Stage 6.5 outputs."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import typer

from shared_pipeline_stages.stage_7.merge_builder import Stage7BuildConfig, build_stage7_merged_runbooks
from shared_pipeline_stages.stage_7.merge_runner import AzureOpenAIRunbookMergeClient

app = typer.Typer(add_completion=False)


@app.command()
def main(
    pool_dir: Path = typer.Option(..., "--pool-dir", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    max_cluster_size: int = typer.Option(3, "--max-cluster-size"),
    llm: bool = typer.Option(False, "--llm", help="Run LLM merge calls for merge clusters."),
    max_workers: int = typer.Option(2, "--max-workers"),
    prompt_path: Path | None = typer.Option(None, "--prompt-path"),
) -> None:
    config = Stage7BuildConfig(
        max_cluster_size=max_cluster_size,
        llm_used=llm,
        max_workers=max_workers,
    )
    llm_client = AzureOpenAIRunbookMergeClient(prompt_path=prompt_path) if llm else None
    result = build_stage7_merged_runbooks(
        pool_dir=pool_dir,
        output_dir=output_dir,
        config=config,
        llm_client=llm_client,
    )
    stage_dir = output_dir / "stage_7_merged_runbooks" if output_dir.name != "stage_7_merged_runbooks" else output_dir
    typer.echo(f"Canonical runbooks written: {stage_dir / 'canonical_runbooks.json'}")
    typer.echo(f"Merge report written:       {stage_dir / 'runbook_merge_report.json'}")
    typer.echo(f"Mapping written:            {stage_dir / 'candidate_to_procedure_mapping.json'}")
    typer.echo(f"Merge packets written:      {stage_dir / 'merge_packets.json'}")
    typer.echo(f"Canonical runbooks:         {result.canonical_runbook_count}")
    typer.echo(f"Pass-through promoted:      {result.pass_through_count}")
    typer.echo(f"Parent merge clusters:      {result.merge_cluster_count}")
    typer.echo(f"Sub-clusters prepared:      {result.sub_cluster_count}")
    typer.echo(f"Comparison review written: {stage_dir / 'review_markdown' / 'merge_comparison_review.md'}")


if __name__ == "__main__":
    app()
