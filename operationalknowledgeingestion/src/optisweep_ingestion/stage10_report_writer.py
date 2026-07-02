"""Report writer for source knowledge extraction outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from operationalknowledgeingestion.src.optisweep_ingestion.schemas.extraction_report import LineageValidation, RecordsCreated, SourceExtractionReport
from operationalknowledgeingestion.src.optisweep_ingestion.services.source_ref_service import lineage_from_bundle, record_has_lineage, record_has_source_refs
from operationalknowledgeingestion.src.optisweep_ingestion.stage_paths import stage_dir
from optisweep_ingestion.stage9_validation_repair import validate_source_knowledge_outputs
from operationalknowledgeingestion.src.optisweep_ingestion.utils.json_utils import read_json, write_json


def write_source_extraction_report(
    output_dir: str | Path,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    output_path = Path(output_dir)
    bundle = read_json(
        _first_existing_path(
            output_path,
            [("1", "source_bundle.json"), ("2", "source_bundle.json")],
        )
    )
    lineage = lineage_from_bundle(bundle)

    artifacts = _read_list(_first_existing(output_path, "3", "source_artifacts_enriched.json", required=False))
    if not artifacts:
        artifacts = _read_list(_first_existing(output_path, "2", "source_artifacts_enriched.json", required=False))
    if not artifacts:
        artifacts = _read_list(_first_existing(output_path, "2", "source_artifacts.json", required=False))
    contexts = _read_list(_first_existing(output_path, "4", "operational_context.json", required=False))
    candidates = _read_list(_first_existing(output_path, "5", "runbook_candidates.json", required=False))

    validation = validate_source_knowledge_outputs(
        artifacts=artifacts,
        contexts=contexts,
        candidates=candidates,
    )

    placeholder_count = sum(
        1
        for candidate in candidates
        if candidate.get("metadata", {}).get("created_by") == "stage_5_candidate_coverage_backfill"
    )

    report = SourceExtractionReport(
        source_id=lineage.source_id,
        source_type=lineage.source_type,
        ingestion_batch_id=lineage.ingestion_batch_id,
        records_created=RecordsCreated(
            artifacts=len(artifacts),
            operational_context=len(contexts),
            runbook_candidates=len(candidates),
        ),
        lineage_validation=LineageValidation(
            missing_source_id_count=_count_missing_lineage(artifacts + contexts + candidates, record_has_lineage),
            missing_source_refs_count=_count_missing_lineage(artifacts + contexts + candidates, record_has_source_refs),
        ),
        duplicate_candidate_count=_count_duplicate_candidate_ids(candidates),
        placeholder_candidate_count=placeholder_count,
        missing_artifact_reference_count=validation["missing_artifact_reference_count"],
        missing_context_reference_count=validation["missing_context_reference_count"],
        schema_validation_failures=validation["schema_validation_failures"],
        warnings=[*(warnings or []), *validation["warnings"]],
    )
    payload = report.model_dump(mode="json")
    report_dir = stage_dir(output_path, "10")
    report_dir.mkdir(parents=True, exist_ok=True)
    write_json(report_dir / "extraction_report.json", payload)
    return payload


def _read_list(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    if not path.exists():
        return []
    data = read_json(path)
    return data if isinstance(data, list) else []


def _first_existing(output_path: Path, stage: str, filename: str, required: bool = True) -> Path | None:
    candidates = [stage_dir(output_path, stage) / filename, output_path / filename]
    for path in candidates:
        if path.exists():
            return path
    if required:
        raise FileNotFoundError(f"Missing {filename}. Checked: {', '.join(str(path) for path in candidates)}")
    return None


def _first_existing_path(output_path: Path, stage_files: list[tuple[str, str]]) -> Path:
    candidates = [
        candidate
        for stage, filename in stage_files
        for candidate in (stage_dir(output_path, stage) / filename, output_path / filename)
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError("Missing required file. Checked: " + ", ".join(str(path) for path in candidates))


def _count_missing_lineage(records: list[dict[str, Any]], check) -> int:
    return sum(1 for record in records if not check(record))


def _count_duplicate_candidate_ids(candidates: list[dict[str, Any]]) -> int:
    seen: set[str] = set()
    duplicates = 0
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id") or "")
        if not candidate_id:
            continue
        if candidate_id in seen:
            duplicates += 1
        else:
            seen.add(candidate_id)
    return duplicates
