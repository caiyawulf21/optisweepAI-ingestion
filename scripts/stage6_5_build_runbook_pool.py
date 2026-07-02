"""Run Shared Stage 6.5 runbook pool generation from Stage 6 finalized runbooks."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import typer

from shared_pipeline_stages.stage_6_5.pool_builder import PoolBuildConfig, build_runbook_pool

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_root: list[Path] = typer.Option(
        ...,
        "--source-root",
        exists=True,
        readable=True,
        help="Source output root containing stage_6_finalized_runbooks. Repeat for multiple sources.",
    ),
    output_dir: Path = typer.Option(..., "--output-dir"),
    min_merge_score: float = typer.Option(0.62, "--min-merge-score"),
    high_confidence_score: float = typer.Option(0.78, "--high-confidence-score"),
    vector_weight: float = typer.Option(0.7, "--vector-weight"),
    lexical_weight: float = typer.Option(0.3, "--lexical-weight"),
    opposing_action_penalty: float = typer.Option(0.5, "--opposing-action-penalty"),
    top_k: int = typer.Option(10, "--top-k"),
    skip_embed: bool = typer.Option(False, "--skip-embed", help="Use deterministic mock vectors for structural tests."),
    use_mock_embedder: bool = typer.Option(False, "--use-mock-embedder"),
) -> None:
    config = PoolBuildConfig(
        min_merge_score=min_merge_score,
        high_confidence_score=high_confidence_score,
        vector_weight=vector_weight,
        lexical_weight=lexical_weight,
        opposing_action_penalty=opposing_action_penalty,
        top_k=top_k,
        skip_embed=skip_embed,
        use_mock_embedder=use_mock_embedder,
    )
    result = build_runbook_pool(
        source_roots=source_root,
        output_dir=output_dir,
        config=config,
    )
    stage_dir = output_dir / "stage_6_5_runbook_pool"
    typer.echo(f"Runbook pool written:         {stage_dir / 'runbook_pool.json'}")
    typer.echo(f"Retrieval cards written:      {stage_dir / 'retrieval_cards.json'}")
    typer.echo(f"Retrieval index written:      {stage_dir / 'runbook_retrieval_index.json'}")
    typer.echo(f"Merge clusters written:       {stage_dir / 'merge_clusters.json'}")
    typer.echo(f"Pass-through runbooks written:{stage_dir / 'pass_through_runbooks.json'}")
    typer.echo(f"Pool report written:          {stage_dir / 'runbook_pool_report.json'}")
    typer.echo(f"Indexed runbooks:             {result.runbook_count}")
    typer.echo(f"Merge clusters:               {result.merge_cluster_count}")
    typer.echo(f"Pass-through runbooks:        {result.pass_through_count}")


if __name__ == "__main__":
    app()
