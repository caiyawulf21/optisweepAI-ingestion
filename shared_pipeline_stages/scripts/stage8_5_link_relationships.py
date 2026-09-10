"""Run Shared Stage 8.5 corpus relationship linking."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import typer

from shared_pipeline_stages.stage_8_5.link_aggregator import Stage85BuildConfig, build_stage8_5_corpus_relationship_links

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_root: list[Path] = typer.Option(
        ...,
        "--source-root",
        exists=True,
        readable=True,
        help="Source output root containing stage_8_relationship_linking/relationship_links.json. Repeat for multiple sources.",
    ),
    output_dir: Path = typer.Option(..., "--output-dir"),
    stage7_dir: Path | None = typer.Option(None, "--stage7-dir", exists=True, readable=True),
    stage8_dir: Path | None = typer.Option(None, "--stage8-dir", exists=True, readable=True),
    no_remap: bool = typer.Option(False, "--no-remap"),
    no_playbook_links: bool = typer.Option(False, "--no-playbook-links"),
) -> None:
    config = Stage85BuildConfig(
        remap_to_canonical_runbooks=not no_remap,
        include_playbook_links=not no_playbook_links,
    )
    result = build_stage8_5_corpus_relationship_links(
        source_roots=source_root,
        output_dir=output_dir,
        stage7_dir=stage7_dir,
        stage8_dir=stage8_dir,
        config=config,
    )
    stage_dir = output_dir / "stage_8_5_relationship_linking" if output_dir.name != "stage_8_5_relationship_linking" else output_dir
    typer.echo(f"Corpus relationship links written: {stage_dir / 'relationship_links.json'}")
    typer.echo(f"Relationship linking report written: {stage_dir / 'relationship_linking_report.json'}")
    typer.echo(f"Total link count:                  {result.link_count}")
    typer.echo(f"Per-source links included:         {result.per_source_link_count}")
    typer.echo(f"Playbook links included:           {result.playbook_link_count}")
    if result.warnings:
        typer.echo(f"Warnings:                          {len(result.warnings)}")


if __name__ == "__main__":
    app()
