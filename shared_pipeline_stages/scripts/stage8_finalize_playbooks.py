"""Run Shared Stage 8 playbook finalization for pilot incidents."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import typer

from shared_pipeline_stages.stage_8.linking_runner import AzureOpenAIPlaybookLinkClient
from shared_pipeline_stages.stage_8.playbook_builder import (
    Stage8BuildConfig,
    build_stage8_finalized_playbooks,
    refresh_stage8_playbook_reviews,
)

app = typer.Typer(add_completion=False)


@app.command()
def main(
    pool_dir: Path = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool",
        "--pool-dir",
        exists=True,
        readable=True,
    ),
    stage7_dir: Path = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks",
        "--stage7-dir",
        exists=True,
        readable=True,
    ),
    incidents_root: Path = typer.Option(
        REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents",
        "--incidents-root",
        exists=True,
        readable=True,
    ),
    output_dir: Path = typer.Option(REPO_ROOT / "shared_pipeline_stages/data/output/shared", "--output-dir"),
    case_id: list[str] = typer.Option(["228086", "228723"], "--case-id"),
    llm: bool = typer.Option(False, "--llm", help="Run LLM link refinement calls."),
    mock_embedder: bool = typer.Option(False, "--mock-embedder", help="Use deterministic mock embeddings."),
    refresh_reviews: bool = typer.Option(
        False,
        "--refresh-reviews",
        help="Regenerate review markdown/HTML from existing canonical_playbooks.json without relinking.",
    ),
    top_k: int = typer.Option(10, "--top-k"),
    prompt_path: Path | None = typer.Option(None, "--prompt-path"),
) -> None:
    stage_dir = output_dir / "stage_8_finalized_playbooks" if output_dir.name != "stage_8_finalized_playbooks" else output_dir
    if refresh_reviews:
        count = refresh_stage8_playbook_reviews(
            stage_dir,
            pool_dir=pool_dir,
            stage7_dir=stage7_dir,
            repo_root=REPO_ROOT,
        )
        typer.echo(f"Review files refreshed:     {count}")
        typer.echo(f"Prompt A output:            {stage_dir / 'prompt_a_one_per_incident'}")
        typer.echo(f"Prompt B output:            {stage_dir / 'prompt_b_multi_flow'}")
        return
    config = Stage8BuildConfig(
        case_ids=list(case_id),
        top_k=top_k,
        llm_used=llm,
        use_mock_embedder=mock_embedder,
    )
    llm_client = AzureOpenAIPlaybookLinkClient(prompt_path=prompt_path) if llm else None
    result = build_stage8_finalized_playbooks(
        pool_dir=pool_dir,
        stage7_dir=stage7_dir,
        incidents_root=incidents_root,
        output_dir=output_dir,
        config=config,
        llm_client=llm_client,
    )
    stage_dir = output_dir / "stage_8_finalized_playbooks" if output_dir.name != "stage_8_finalized_playbooks" else output_dir
    typer.echo(f"Playbooks finalized:        {result.playbook_count}")
    typer.echo(f"Prompt A output:            {stage_dir / 'prompt_a_one_per_incident'}")
    typer.echo(f"Prompt B output:            {stage_dir / 'prompt_b_multi_flow'}")
    typer.echo(f"Comparison report:          {stage_dir / 'stage_8_comparison_report.json'}")


if __name__ == "__main__":
    app()
