"""Run Shared Stage 11 Cosmos publish bundle, SME review sheet, and optional upload."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import typer

from shared_pipeline_stages.stage_11.cosmos_publisher import publish_corpus_to_cosmos

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
    stage10_dir: Path = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_10_embeddings",
        "--stage10-dir",
        exists=True,
        readable=True,
    ),
    stage85_dir: Path | None = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_8_5_relationship_linking",
        "--stage85-dir",
        exists=True,
        readable=True,
    ),
    stage9_dir: Path | None = typer.Option(
        REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_9_validation",
        "--stage9-dir",
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
        help="Source roots used to resolve local artifact image files for Blob + Cosmos canonical_images.",
    ),
    output_dir: Path = typer.Option(REPO_ROOT / "shared_pipeline_stages/data/output/shared", "--output-dir"),
    publish: bool = typer.Option(False, "--publish", help="Upload publish bundle to Cosmos when COSMOS_* env vars are set."),
    publish_version_id: str | None = typer.Option(None, "--publish-version-id"),
    skip_image_blobs: bool = typer.Option(
        False,
        "--skip-image-blobs",
        help=(
            "Offline/local only: write canonical_images docs without Blob upload. "
            "Incompatible with --publish when images are present."
        ),
    ),
) -> None:
    if publish and skip_image_blobs:
        raise typer.BadParameter(
            "--skip-image-blobs cannot be combined with --publish; "
            "Cosmos image docs require HTTPS storage_uri values."
        )
    result = publish_corpus_to_cosmos(
        stage7_dir=stage7_dir,
        stage8_dir=stage8_dir,
        stage10_dir=stage10_dir,
        stage85_dir=stage85_dir,
        stage9_dir=stage9_dir,
        source_roots=source_root,
        output_dir=output_dir,
        publish=publish,
        publish_version_id=publish_version_id,
        upload_image_blobs=False if skip_image_blobs else None,
    )
    stage_dir = output_dir / "stage_11_cosmos_publish" if output_dir.name != "stage_11_cosmos_publish" else output_dir
    typer.echo(f"Publish manifest written:    {stage_dir / 'publish_manifest.json'}")
    typer.echo(f"Cosmos publish report:       {stage_dir / 'cosmos_publish_report.json'}")
    typer.echo(f"SME review sheet:            {stage_dir / 'sme_review_sheet.md'}")
    typer.echo(f"Publish bundle:              {stage_dir / 'publish_bundle'}")
    typer.echo(f"Publish version:             {result.publish_version_id}")
    typer.echo(f"Runbooks:                    {result.runbook_count}")
    typer.echo(f"Playbooks Prompt A:          {result.playbook_prompt_a_count}")
    typer.echo(f"Playbooks Prompt B:          {result.playbook_prompt_b_count}")
    typer.echo(f"Operational context RAG:     {result.operational_context_count}")
    typer.echo(f"Source artifact RAG:         {result.source_artifact_count}")
    typer.echo(f"Canonical images:            {result.canonical_image_count}")
    typer.echo(f"Embeddings total:            {result.embedding_count}")
    typer.echo(f"Relationship links:          {result.relationship_link_count}")
    typer.echo(f"Relationship shards:         {result.relationship_shard_count}")
    typer.echo(f"Uploaded to Cosmos:          {result.uploaded}")
    if result.warnings:
        typer.echo(f"Warnings:                    {len(result.warnings)}")
        for warning in result.warnings[:20]:
            typer.echo(f"  - {warning}")
        if len(result.warnings) > 20:
            typer.echo(f"  ... {len(result.warnings) - 20} more")
    if publish and not result.uploaded:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
