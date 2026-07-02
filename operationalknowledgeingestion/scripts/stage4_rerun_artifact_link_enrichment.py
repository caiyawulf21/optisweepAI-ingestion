"""Re-apply deterministic artifact/image linking to existing Stage 4 and Stage 5 outputs."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT_PARENT = ROOT.parent
SRC = ROOT / "src"
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from operationalknowledgeingestion.src.optisweep_ingestion.tools.artifact_linker import IMAGE_NOTE_MARKER, enrich_context_records, enrich_runbook_candidates
from optisweep_ingestion.stage4_operational_context import validate_context_record
from optisweep_ingestion.stage5_runbook_candidates import validate_candidate_record
from operationalknowledgeingestion.src.optisweep_ingestion.utils.json_utils import read_json, write_json
from optisweep_ingestion.stage_paths import stage_dir

app = typer.Typer(add_completion=False)


def _stage4_metrics(contexts: list[dict]) -> dict:
    total = len(contexts)
    with_art = sum(1 for item in contexts if item.get("related_artifact_ids"))
    with_image_refs = sum(1 for item in contexts if item.get("image_refs"))
    return {
        "total": total,
        "with_related_artifact_ids": with_art,
        "with_image_refs": with_image_refs,
        "empty_related_artifact_ids": total - with_art,
        "artifact_coverage_pct": round(100 * with_art / total, 1) if total else 0.0,
    }


def _stage5_metrics(candidates: list[dict]) -> dict:
    total = len(candidates)
    empty_art = sum(1 for item in candidates if not item.get("related_artifact_ids"))
    with_img_note = sum(
        1 for item in candidates if any(IMAGE_NOTE_MARKER in str(step) for step in (item.get("rough_steps") or []))
    )
    screen_kw = ["hmi", "screen", "visu_", "figure", "stacklight", "button"]
    screen_missing = 0
    for item in candidates:
        text = " ".join(item.get("rough_steps") or []) + " " + str(item.get("title") or "") + " " + str(item.get("summary") or "")
        if not any(k in text.lower() for k in screen_kw):
            continue
        has_note = any(IMAGE_NOTE_MARKER in str(step) for step in (item.get("rough_steps") or []))
        has_art = bool(item.get("related_artifact_ids"))
        if not has_note and not has_art:
            screen_missing += 1
    return {
        "total": total,
        "with_related_artifact_ids": total - empty_art,
        "empty_related_artifact_ids": empty_art,
        "with_image_notes": with_img_note,
        "screen_hmi_missing_both": screen_missing,
        "artifact_coverage_pct": round(100 * (total - empty_art) / total, 1) if total else 0.0,
    }


@app.command()
def main(
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    operational_context: Path = typer.Option(..., "--operational-context", exists=True, readable=True),
    runbook_candidates: Path = typer.Option(..., "--runbook-candidates", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
) -> None:
    artifacts = read_json(source_artifacts)
    contexts = read_json(operational_context)
    candidates = read_json(runbook_candidates)
    if not isinstance(artifacts, list):
        raise typer.BadParameter("source_artifacts must be a list.")
    if not isinstance(contexts, list):
        raise typer.BadParameter("operational_context must be a list.")
    if not isinstance(candidates, list):
        raise typer.BadParameter("runbook_candidates must be a list.")

    stage4_dir = stage_dir(output_dir, "4")
    stage5_dir = stage_dir(output_dir, "5")
    known_artifact_ids = {str(item["artifact_id"]) for item in artifacts if item.get("artifact_id")}
    known_context_ids = {str(item["context_id"]) for item in contexts if item.get("context_id")}

    before_stage4 = _stage4_metrics(contexts)
    before_stage5 = _stage5_metrics(candidates)

    enriched_contexts, context_notes = enrich_context_records(contexts, artifacts)
    validated_contexts: list[dict] = []
    context_warnings: list[str] = []
    for record in enriched_contexts:
        errors = validate_context_record(record, known_artifact_ids)
        if errors:
            context_warnings.append(
                f"Dropped context '{record.get('context_id', '?')}' after artifact linking: {'; '.join(errors)}"
            )
        else:
            validated_contexts.append(record)

    context_index = {str(item["context_id"]): item for item in validated_contexts if item.get("context_id")}
    enriched_candidates, candidate_notes = enrich_runbook_candidates(candidates, artifacts, list(context_index.values()))
    validated_candidates: list[dict] = []
    candidate_warnings: list[str] = []
    for candidate in enriched_candidates:
        errors = validate_candidate_record(candidate, known_artifact_ids, set(context_index))
        if errors:
            candidate_warnings.append(
                f"Dropped candidate '{candidate.get('candidate_id', '?')}' after artifact linking: {'; '.join(errors)}"
            )
        else:
            validated_candidates.append(candidate)

    after_stage4 = _stage4_metrics(validated_contexts)
    after_stage5 = _stage5_metrics(validated_candidates)

    write_json(stage4_dir / "operational_context.json", validated_contexts)
    context_report_path = stage4_dir / "operational_context_extraction_report.json"
    context_report = read_json(context_report_path) if context_report_path.exists() else {}
    context_report.update(
        {
            "artifact_link_rerun_at": datetime.now(UTC).isoformat(),
            "artifact_link_notes": context_notes,
            "artifact_link_warnings": context_warnings,
            "before_artifact_link_metrics": before_stage4,
            "after_artifact_link_metrics": after_stage4,
            "records_with_artifacts": after_stage4["with_related_artifact_ids"],
            "records_with_image_refs": after_stage4["with_image_refs"],
            "records_without_artifacts": after_stage4["empty_related_artifact_ids"],
        }
    )
    write_json(context_report_path, context_report)

    write_json(stage5_dir / "runbook_candidates.json", validated_candidates)
    candidate_report_path = stage5_dir / "runbook_candidate_extraction_report.json"
    candidate_report = read_json(candidate_report_path) if candidate_report_path.exists() else {}
    counts_by_type = Counter(str(item.get("likely_procedure_type") or "unknown") for item in validated_candidates)
    counts_by_role = Counter(str(item.get("likely_role_required") or "unknown") for item in validated_candidates)
    candidate_report.update(
        {
            "artifact_link_rerun_at": datetime.now(UTC).isoformat(),
            "artifact_link_notes": candidate_notes,
            "artifact_link_warnings": candidate_warnings,
            "before_artifact_link_metrics": before_stage5,
            "after_artifact_link_metrics": after_stage5,
            "candidate_count": len(validated_candidates),
            "candidate_counts_by_type": dict(sorted(counts_by_type.items())),
            "candidate_counts_by_role": dict(sorted(counts_by_role.items())),
            "candidates_with_artifacts": after_stage5["with_related_artifact_ids"],
            "candidates_with_image_notes": after_stage5["with_image_notes"],
        }
    )
    write_json(candidate_report_path, candidate_report)

    typer.echo("Stage 4 before: " + str(before_stage4))
    typer.echo("Stage 4 after:  " + str(after_stage4))
    typer.echo("Stage 5 before: " + str(before_stage5))
    typer.echo("Stage 5 after:  " + str(after_stage5))
    typer.echo(f"Stage 4 context notes:   {len(context_notes)}")
    typer.echo(f"Stage 5 candidate notes: {len(candidate_notes)}")
    typer.echo(f"Stage 4 warnings:          {len(context_warnings)}")
    typer.echo(f"Stage 5 warnings:          {len(candidate_warnings)}")


if __name__ == "__main__":
    app()
