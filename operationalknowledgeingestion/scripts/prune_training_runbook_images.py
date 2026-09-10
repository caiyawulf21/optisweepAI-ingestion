"""Prune weak/unrelated training-video images from finalized Stage 6 runbooks."""

from __future__ import annotations

from pathlib import Path
import sys

import typer

ROOT = Path(__file__).resolve().parents[1]
PROJECT_PARENT = ROOT.parent
SRC = ROOT / "src"
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optisweep_ingestion.stage6_runbook_finalization import (
    _write_text,
    write_runbook_review_html,
    write_runbook_review_markdown,
)
from optisweep_ingestion.tools.artifact_linker import (
    _is_strong_term,
    _score_artifact,
    collect_record_text,
    extract_search_terms,
    is_weak_evidence_artifact,
    is_weak_evidence_text,
    pages_from_source_refs,
)
from optisweep_ingestion.utils.json_utils import read_json, write_json

app = typer.Typer(add_completion=False)


def _artifact_id(ref: object) -> str:
    if isinstance(ref, str):
        return ref.strip()
    if isinstance(ref, dict):
        return str(ref.get("artifact_id") or "").strip()
    return ""


def _keep_ref(
    ref: dict,
    *,
    artifact_index: dict[str, dict],
    terms: list[str],
    pages: set[int],
    preferred_section_ids: set[str],
    min_score: int,
) -> bool:
    artifact_id = _artifact_id(ref)
    if not artifact_id:
        return False
    if is_weak_evidence_text(artifact_id):
        return False
    artifact = artifact_index.get(artifact_id)
    if not artifact:
        return False
    if is_weak_evidence_artifact(artifact):
        return False
    score = _score_artifact(
        artifact,
        terms=terms,
        pages=pages,
        figure_ids=set(),
        prefer_screen_types=True,
        preferred_section_ids=preferred_section_ids,
    )
    return score >= min_score


def prune_runbook(runbook: dict, artifact_index: dict[str, dict], *, max_visuals: int = 2) -> dict:
    updated = dict(runbook)
    terms = extract_search_terms(updated)
    strong_terms = [term for term in terms if _is_strong_term(term)]
    if not strong_terms:
        strong_terms = terms
    pages = pages_from_source_refs(updated.get("source_refs") or [])
    preferred_section_ids = {
        str(ref.get("section_id") or "").strip()
        for ref in updated.get("source_refs") or []
        if isinstance(ref, dict) and ref.get("section_id")
    }
    preferred_section_ids.discard("")

    scored_visuals: list[tuple[int, dict]] = []
    for field in ("visual_references", "screens_or_images"):
        for ref in updated.get(field) or []:
            if not isinstance(ref, dict):
                continue
            artifact_id = _artifact_id(ref)
            artifact = artifact_index.get(artifact_id)
            if not artifact or is_weak_evidence_artifact(artifact):
                continue
            if is_weak_evidence_text(artifact_id):
                continue
            score = _score_artifact(
                artifact,
                terms=strong_terms or terms,
                pages=pages,
                figure_ids=set(),
                prefer_screen_types=True,
                preferred_section_ids=preferred_section_ids,
            )
            if score > 0:
                scored_visuals.append((score, ref))

    scored_visuals.sort(key=lambda item: (-item[0], _artifact_id(item[1])))
    kept_ids: list[str] = []
    kept_refs: list[dict] = []
    for score, ref in scored_visuals:
        artifact_id = _artifact_id(ref)
        if not artifact_id or artifact_id in kept_ids:
            continue
        kept_ids.append(artifact_id)
        kept_refs.append(ref)
        if len(kept_refs) >= max_visuals:
            break

    updated["visual_references"] = kept_refs
    updated["screens_or_images"] = [
        ref
        for ref in (updated.get("screens_or_images") or [])
        if isinstance(ref, dict) and _artifact_id(ref) in set(kept_ids)
    ]
    for step in updated.get("steps") or []:
        if not isinstance(step, dict):
            continue
        step["screens_or_images"] = [
            ref
            for ref in (step.get("screens_or_images") or [])
            if isinstance(ref, dict)
            and _keep_ref(
                ref,
                artifact_index=artifact_index,
                terms=strong_terms or terms,
                pages=pages,
                preferred_section_ids=preferred_section_ids,
                min_score=24,
            )
        ]

    image_refs: list[dict] = []
    seen: set[str] = set()
    for ref in kept_refs:
        artifact_id = _artifact_id(ref)
        if artifact_id and artifact_id not in seen:
            seen.add(artifact_id)
            image_refs.append(
                {
                    "artifact_id": artifact_id,
                    "what_to_look_at": str(
                        ref.get("what_to_look_at") or ref.get("description") or ref.get("caption") or ""
                    ).strip(),
                }
            )
    for step in updated.get("steps") or []:
        if not isinstance(step, dict):
            continue
        for ref in step.get("screens_or_images") or []:
            artifact_id = _artifact_id(ref)
            if artifact_id and artifact_id not in seen:
                seen.add(artifact_id)
                image_refs.append({"artifact_id": artifact_id})
    updated["image_refs"] = image_refs

    missing = list(updated.get("missing_details") or [])
    text = collect_record_text(updated).lower()
    multi_surface = sum(
        token in text for token in ("database", "heartbeat", "restart", "rms")
    ) >= 3 and len(updated.get("steps") or []) >= 4
    if multi_surface and not kept_refs:
        note = (
            "Training Q&A/checklist with no grounded UI/table frames; prefer a concrete "
            "incident or services restart runbook (e.g. case 228086 Ignition/OptiSweep restart) "
            "instead of this high-level tip."
        )
        if note not in missing:
            missing.append(note)
    updated["missing_details"] = missing
    return updated


@app.command()
def main(
    stage6_dir: Path = typer.Option(..., "--stage6-dir", exists=True, file_okay=False),
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    max_visuals: int = typer.Option(2, "--max-visuals"),
    regenerate_reviews: bool = typer.Option(True, "--regenerate-reviews/--no-regenerate-reviews"),
) -> None:
    artifacts = read_json(source_artifacts)
    artifact_index = {
        str(item.get("artifact_id")): item
        for item in artifacts
        if isinstance(item, dict) and item.get("artifact_id")
    }
    finalized_dir = stage6_dir / "finalized_runbooks"
    review_dir = stage6_dir / "review_markdown" / "runbooks"
    pruned = 0
    visuals_before = 0
    visuals_after = 0
    for path in sorted(finalized_dir.glob("*.json")):
        runbook = read_json(path)
        before = len(runbook.get("visual_references") or []) + len(runbook.get("image_refs") or [])
        updated = prune_runbook(runbook, artifact_index, max_visuals=max_visuals)
        after = len(updated.get("visual_references") or []) + len(updated.get("image_refs") or [])
        visuals_before += before
        visuals_after += after
        if updated != runbook:
            write_json(path, updated)
            pruned += 1
        if regenerate_reviews:
            review_dir.mkdir(parents=True, exist_ok=True)
            review_path = review_dir / f"{path.stem}.md"
            html_path = review_dir / f"{path.stem}.html"
            _write_text(
                review_path,
                write_runbook_review_markdown(
                    updated,
                    artifact_index=artifact_index,
                    review_markdown_path=review_path,
                ),
            )
            _write_text(
                html_path,
                write_runbook_review_html(
                    updated,
                    artifact_index=artifact_index,
                    review_html_path=html_path,
                ),
            )
    typer.echo(f"Pruned runbooks changed: {pruned}")
    typer.echo(f"Visual/image ref counts: {visuals_before} -> {visuals_after}")
    if regenerate_reviews:
        typer.echo(f"Reviews regenerated under: {review_dir}")


if __name__ == "__main__":
    app()
