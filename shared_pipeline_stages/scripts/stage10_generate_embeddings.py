"""Run Shared Stage 10 embedding generation."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import typer

from shared_pipeline_stages.stage_10.embedding_generator import generate_corpus_embeddings

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
    source_root: list[Path] = typer.Option(
        [
            REPO_ROOT / "operationalknowledgeingestion/data/output/manual_optisweep_om_v3",
            REPO_ROOT / "operationalknowledgeingestion/data/output/training_video_day1",
            REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents/case_228086",
            REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents/case_228723",
        ],
        "--source-root",
        exists=True,
        readable=True,
        help="Source output roots for operational context and source artifact RAG embeddings.",
    ),
    output_dir: Path = typer.Option(REPO_ROOT / "shared_pipeline_stages/data/output/shared", "--output-dir"),
    use_mock_embedder: bool = typer.Option(False, "--use-mock-embedder"),
) -> None:
    result = generate_corpus_embeddings(
        stage7_dir=stage7_dir,
        stage8_dir=stage8_dir,
        output_dir=output_dir,
        source_roots=source_root,
        use_mock_embedder=use_mock_embedder,
    )
    stage_dir = output_dir / "stage_10_embeddings" if output_dir.name != "stage_10_embeddings" else output_dir
    typer.echo(f"Embedding records written:   {stage_dir / 'embedding_records.json'}")
    typer.echo(f"Embedding report written:    {stage_dir / 'embedding_generation_report.json'}")
    typer.echo(f"Total records:               {result.record_count}")
    typer.echo(f"Runbook records:             {result.runbook_record_count}")
    typer.echo(f"Playbook Prompt A records:   {result.playbook_prompt_a_count}")
    typer.echo(f"Playbook Prompt B records:   {result.playbook_prompt_b_count}")
    typer.echo(f"Operational context records: {result.operational_context_count}")
    typer.echo(f"Source artifact records:     {result.source_artifact_count}")
    typer.echo(f"Embedding model:             {result.embedding_model}")
    if result.warnings:
        typer.echo(f"Warnings:                    {len(result.warnings)}")
        for warning in result.warnings:
            typer.echo(f"  - {warning}")
    missing_rag = (
        "No --source-root provided; operational_context and source_artifact embeddings will be skipped."
        in result.warnings
    )
    if missing_rag:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
