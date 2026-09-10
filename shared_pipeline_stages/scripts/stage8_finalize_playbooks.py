"""Run Shared Stage 8 playbook finalization for pilot incidents."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import typer

from orchestration.paths import discover_source_roots
from orchestration.runners import run_python_script
from shared_pipeline_stages.stage_8.linking_runner import AzureOpenAIPlaybookLinkClient
from shared_pipeline_stages.stage_8.playbook_builder import (
    Stage8BuildConfig,
    build_stage8_finalized_playbooks,
    refresh_stage8_playbook_reviews,
)

app = typer.Typer(add_completion=False)
SHARED_SCRIPTS = REPO_ROOT / "shared_pipeline_stages" / "scripts"


@app.command()
def main(
    pool_dir: Path = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool",
        "--pool-dir",
    ),
    stage7_dir: Path = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks",
        "--stage7-dir",
    ),
    incidents_root: Path = typer.Option(
        REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents",
        "--incidents-root",
        exists=True,
        readable=True,
    ),
    output_dir: Path = typer.Option(REPO_ROOT / "shared_pipeline_stages/data/output/shared", "--output-dir"),
    case_id: list[str] = typer.Option(["228086", "228723"], "--case-id"),
    llm: bool = typer.Option(False, "--llm", help="Use Azure OpenAI for playbook link refinement."),
    mock_embedder: bool = typer.Option(False, "--mock-embedder", help="Use deterministic mock embeddings."),
    lexical_only: bool = typer.Option(
        False,
        "--lexical-only",
        help=(
            "Explicitly allow retrieval to fall back to lexical-only (jaccard) scoring when "
            "Azure OpenAI embedding credentials are unavailable. Without this flag, missing "
            "credentials cause the run to fail loudly instead of silently degrading."
        ),
    ),
    rebuild_pool: bool = typer.Option(
        True,
        "--rebuild-pool/--no-rebuild-pool",
        help="Rebuild Stage 6.5 runbook pool (and Stage 7) before linking. Default: always rebuild.",
    ),
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
    if not llm:
        raise typer.BadParameter(
            "Stage 8 requires --llm. Deterministic playbook finalization is not supported."
        )
    if rebuild_pool:
        roots = discover_source_roots()
        if not roots:
            raise typer.BadParameter("No Stage 6 source roots found to rebuild the runbook pool.")
        typer.echo(f"Rebuilding Stage 6.5 pool from {len(roots)} source roots...")
        args = ["--output-dir", str(output_dir)]
        for root in roots:
            args.extend(["--source-root", str(root)])
        run_python_script(SHARED_SCRIPTS / "stage6_5_build_runbook_pool.py", args)
        typer.echo("Rebuilding Stage 7 merged catalog...")
        run_python_script(
            SHARED_SCRIPTS / "stage7_merge_runbooks.py",
            ["--pool-dir", str(pool_dir), "--output-dir", str(output_dir), "--llm"],
        )
        pool_dir = output_dir / "stage_6_5_runbook_pool"
        stage7_dir = output_dir / "stage_7_merged_runbooks"
    if not pool_dir.exists() or not stage7_dir.exists():
        raise typer.BadParameter(
            f"Missing pool/stage7 outputs. Expected {pool_dir} and {stage7_dir}. "
            "Run with --rebuild-pool (default) or Shared Stages 6.5/7 first."
        )
    config = Stage8BuildConfig(
        case_ids=list(case_id),
        top_k=top_k,
        llm_used=True,
        use_mock_embedder=mock_embedder,
        allow_lexical_fallback=lexical_only,
    )
    llm_client = AzureOpenAIPlaybookLinkClient(prompt_path=prompt_path)
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
    typer.echo(f"Retrieval mode:             {result.retrieval_mode} ({result.embedding_model})")
    typer.echo(f"Prompt A output:            {stage_dir / 'prompt_a_one_per_incident'}")
    typer.echo(f"Prompt B output:            {stage_dir / 'prompt_b_multi_flow'}")
    typer.echo(f"Comparison report:          {stage_dir / 'stage_8_comparison_report.json'}")


if __name__ == "__main__":
    app()
