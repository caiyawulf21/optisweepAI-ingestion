from __future__ import annotations

import shutil
from pathlib import Path

from orchestration.paths import (
    OUTPUT_COSMOS_PUBLISH,
    OUTPUT_ROOT,
    OUTPUT_SME_REVIEW,
    SHARED_OUTPUT,
    discover_source_roots,
    ensure_output_layout,
)

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}

SME_README = """# Delivery SME Review

Reviewable markdown mirror assembled by the ingestion orchestrator.

Shape matches `sme_review_runbooks/`:

```text
sme_review/
  <source_id>/                 # finalized runbook markdown + assets/
  <case_id>/
    assets/                    # finalized runbook + incident OCR images
    stage_5_runbook_candidates/
  stage_8_playbooks/
    prompt_a_one_per_incident/
    prompt_b_multi_flow/
```

Cosmos push uses the sibling folder `../cosmos_publish/`, not these markdown files.

Refresh:

```powershell
python orchestration/scripts/assemble_output.py
```
"""


def assemble_delivery_output(
    *,
    source_roots: list[Path] | None = None,
    stage11_dir: Path | None = None,
) -> dict[str, object]:
    ensure_output_layout()
    roots = source_roots or discover_source_roots()
    sme_summary = _assemble_sme_review(roots)
    cosmos_summary = _assemble_cosmos_publish(stage11_dir)
    (OUTPUT_ROOT / "README.md").write_text(
        _output_readme(sme_summary, cosmos_summary),
        encoding="utf-8",
    )
    return {
        "output_root": str(OUTPUT_ROOT),
        "sme_review": sme_summary,
        "cosmos_publish": cosmos_summary,
    }


def publish_cosmos_from_output(
    cosmos_publish_dir: Path | None = None,
    *,
    publish_scope: str | None = None,
    default_case_id: str | None = None,
) -> tuple[bool, str, list[str], dict[str, int]]:
    from shared_pipeline_stages.stage_11.cosmos_publisher import upload_existing_publish_bundle

    target = cosmos_publish_dir or OUTPUT_COSMOS_PUBLISH
    if not (target / "publish_bundle").is_dir() and not (target / "runbooks").is_dir():
        raise FileNotFoundError(
            f"No publish bundle at {target}. Run shared Stage 11 / assemble_output first."
        )
    return upload_existing_publish_bundle(
        target,
        publish_scope=publish_scope,
        default_case_id=default_case_id,
    )


def _assemble_sme_review(roots: list[Path]) -> dict[str, dict[str, int]]:
    if OUTPUT_SME_REVIEW.exists():
        shutil.rmtree(OUTPUT_SME_REVIEW)
    OUTPUT_SME_REVIEW.mkdir(parents=True)

    summary: dict[str, dict[str, int]] = {}
    for root in roots:
        name = root.name
        runbooks_dir = root / "stage_6_finalized_runbooks" / "review_markdown" / "runbooks"
        dest = OUTPUT_SME_REVIEW / name
        dest.mkdir(parents=True, exist_ok=True)
        markdown_count = 0
        if runbooks_dir.is_dir():
            for markdown in runbooks_dir.glob("*.md"):
                shutil.copy2(markdown, dest / markdown.name)
                markdown_count += 1
            assets_src = runbooks_dir / "assets"
            if assets_src.is_dir():
                shutil.copytree(assets_src, dest / "assets")
        _copy_incident_stage2_images(root, dest)

        candidate_review = (
            root / "stage_5_runbook_candidates" / "runbook_candidate_review.md"
        )
        if candidate_review.is_file():
            target = dest / "stage_5_runbook_candidates" / "runbook_candidate_review.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate_review, target)

        image_count = len(list((dest / "assets").glob("*"))) if (dest / "assets").is_dir() else 0
        summary[name] = {"markdown": markdown_count, "images": image_count}

    stage8_root = SHARED_OUTPUT / "stage_8_finalized_playbooks"
    playbooks_dest = OUTPUT_SME_REVIEW / "stage_8_playbooks"
    playbooks_dest.mkdir(parents=True, exist_ok=True)
    for variant in ("prompt_a_one_per_incident", "prompt_b_multi_flow"):
        src = stage8_root / variant / "review_markdown" / "playbooks"
        dest = playbooks_dest / variant
        dest.mkdir(parents=True, exist_ok=True)
        markdown_count = 0
        html_count = 0
        if src.is_dir():
            for markdown in src.glob("*.md"):
                shutil.copy2(markdown, dest / markdown.name)
                markdown_count += 1
            for html_file in src.glob("*.html"):
                shutil.copy2(html_file, dest / html_file.name)
                html_count += 1
            assets_src = src / "assets"
            if assets_src.is_dir():
                shutil.copytree(assets_src, dest / "assets")
        image_count = len(list((dest / "assets").glob("*"))) if (dest / "assets").is_dir() else 0
        summary[f"stage_8_playbooks/{variant}"] = {
            "markdown": markdown_count,
            "html": html_count,
            "images": image_count,
        }

    (OUTPUT_SME_REVIEW / "README.md").write_text(SME_README, encoding="utf-8")
    return summary


def _copy_incident_stage2_images(root: Path, dest: Path) -> None:
    stage2_dir = root / "stage_2_ocr_artifacts"
    if not stage2_dir.is_dir():
        return
    image_paths = sorted(
        path for path in stage2_dir.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )
    if not image_paths:
        return
    assets_dest = dest / "assets"
    assets_dest.mkdir(parents=True, exist_ok=True)
    for image_path in image_paths:
        shutil.copy2(image_path, _unique_asset_path(assets_dest, image_path))


def _unique_asset_path(assets_dest: Path, image_path: Path) -> Path:
    target = assets_dest / image_path.name
    if not target.exists() or target.stat().st_size == image_path.stat().st_size:
        return target
    stem = image_path.stem
    suffix = image_path.suffix
    index = 2
    while True:
        candidate = assets_dest / f"{stem}_{index}{suffix}"
        if not candidate.exists() or candidate.stat().st_size == image_path.stat().st_size:
            return candidate
        index += 1


def _assemble_cosmos_publish(stage11_dir: Path | None) -> dict[str, object]:
    base = stage11_dir or (SHARED_OUTPUT / "stage_11_cosmos_publish")
    # Prefer the cumulative (merged + operator-language enriched) bundle when present.
    cumulative = base / "cumulative_publish"
    source = cumulative if cumulative.is_dir() else base
    if OUTPUT_COSMOS_PUBLISH.exists():
        shutil.rmtree(OUTPUT_COSMOS_PUBLISH)
    OUTPUT_COSMOS_PUBLISH.mkdir(parents=True)

    if not source.is_dir():
        (OUTPUT_COSMOS_PUBLISH / "README.md").write_text(
            "# Cosmos publish\n\nNo Stage 11 bundle yet. Run shared publish (`--with-publish`) first.\n",
            encoding="utf-8",
        )
        return {"copied": False, "source": str(source), "files": 0}

    file_count = 0
    for path in source.rglob("*"):
        if path.is_file():
            rel = path.relative_to(source)
            target = OUTPUT_COSMOS_PUBLISH / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            file_count += 1

    (OUTPUT_COSMOS_PUBLISH / "README.md").write_text(
        (
            "# Cosmos publish handoff\n\n"
            "This folder is the cumulative Stage 11 publish bundle used for Cosmos upload.\n"
            "It must remain a superset of prior runtime cases (operator-language enriched).\n\n"
            "```powershell\n"
            "python orchestration/scripts/publish_cosmos_from_output.py --publish-scope all\n"
            "```\n"
        ),
        encoding="utf-8",
    )
    return {
        "copied": True,
        "source": str(source),
        "cumulative": source == cumulative,
        "files": file_count,
        "publish_bundle": str(OUTPUT_COSMOS_PUBLISH / "publish_bundle"),
    }


def _output_readme(
    sme_summary: dict[str, dict[str, int]],
    cosmos_summary: dict[str, object],
) -> str:
    sme_lines = "\n".join(
        f"- `{name}`: {counts.get('markdown', 0)} markdown, {counts.get('images', 0)} images"
        for name, counts in sme_summary.items()
    )
    return f"""# data/output delivery

Assembled handoff for SME review and Cosmos publish.

```text
data/output/
  sme_review/          # same shape as sme_review_runbooks/
  cosmos_publish/      # Stage 11 bundle — push to Cosmos from here
```

## SME review

{sme_lines or '- (empty)'}

## Cosmos publish

- Copied: `{cosmos_summary.get('copied')}`
- Source: `{cosmos_summary.get('source')}`
- Files: `{cosmos_summary.get('files')}`

```powershell
python orchestration/scripts/assemble_output.py
python orchestration/scripts/publish_cosmos_from_output.py
```
"""
