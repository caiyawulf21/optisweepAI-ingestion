"""Validation helpers for source knowledge extraction outputs."""

from __future__ import annotations

from typing import Any

from operationalknowledgeingestion.src.optisweep_ingestion.schemas.operational_context import ALLOWED_CONTEXT_TYPES, FORBIDDEN_FIELDS as CONTEXT_FORBIDDEN_FIELDS
from operationalknowledgeingestion.src.optisweep_ingestion.schemas.runbook_candidate import (
    ALLOWED_CONFIDENCE,
    ALLOWED_PROCEDURE_TYPES,
    ALLOWED_ROLES,
    FORBIDDEN_FIELDS as CANDIDATE_FORBIDDEN_FIELDS,
)
from operationalknowledgeingestion.src.optisweep_ingestion.services.source_ref_service import record_has_lineage, record_has_source_refs


def validate_source_knowledge_outputs(
    artifacts: list[dict[str, Any]] | None = None,
    contexts: list[dict[str, Any]] | None = None,
    candidates: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    artifacts = artifacts or []
    contexts = contexts or []
    candidates = candidates or []
    known_artifact_ids = {str(item.get("artifact_id")) for item in artifacts if item.get("artifact_id")}
    known_context_ids = {str(item.get("context_id")) for item in contexts if item.get("context_id")}

    failures: list[str] = []
    warnings: list[str] = []
    missing_artifact_reference_count = 0
    missing_context_reference_count = 0

    for index, artifact in enumerate(artifacts):
        prefix = f"artifact[{index}]"
        failures.extend(_validate_lineage(artifact, prefix))
        if not record_has_source_refs(artifact):
            failures.append(f"{prefix}: missing source_refs")

    for index, context in enumerate(contexts):
        prefix = f"context[{index}]"
        failures.extend(_validate_lineage(context, prefix))
        if not record_has_source_refs(context):
            failures.append(f"{prefix}: missing source_refs")
        context_type = str(context.get("context_type") or "")
        if context_type and context_type not in ALLOWED_CONTEXT_TYPES:
            failures.append(f"{prefix}: invalid context_type '{context_type}'")
        for forbidden in CONTEXT_FORBIDDEN_FIELDS:
            if forbidden in context:
                failures.append(f"{prefix}: forbidden field '{forbidden}'")
        for artifact_id in context.get("related_artifact_ids") or []:
            if artifact_id not in known_artifact_ids:
                missing_artifact_reference_count += 1
                failures.append(f"{prefix}: related_artifact_id not found '{artifact_id}'")
        for artifact_id in context.get("image_refs") or []:
            if artifact_id not in known_artifact_ids:
                missing_artifact_reference_count += 1
                failures.append(f"{prefix}: image_ref not found '{artifact_id}'")

    for index, candidate in enumerate(candidates):
        prefix = f"candidate[{index}]"
        failures.extend(_validate_lineage(candidate, prefix))
        if not record_has_source_refs(candidate):
            failures.append(f"{prefix}: missing source_refs")
        if candidate.get("likely_procedure_type") not in ALLOWED_PROCEDURE_TYPES:
            failures.append(f"{prefix}: invalid likely_procedure_type")
        if candidate.get("likely_role_required") not in ALLOWED_ROLES:
            failures.append(f"{prefix}: invalid likely_role_required")
        if candidate.get("confidence", "medium") not in ALLOWED_CONFIDENCE:
            failures.append(f"{prefix}: invalid confidence")
        for forbidden in CANDIDATE_FORBIDDEN_FIELDS:
            if forbidden in candidate:
                failures.append(f"{prefix}: forbidden field '{forbidden}'")
        for artifact_id in candidate.get("related_artifact_ids") or []:
            if artifact_id not in known_artifact_ids:
                missing_artifact_reference_count += 1
                failures.append(f"{prefix}: related_artifact_id not found '{artifact_id}'")
        for context_id in candidate.get("related_context_ids") or []:
            if context_id not in known_context_ids:
                missing_context_reference_count += 1
                failures.append(f"{prefix}: related_context_id not found '{context_id}'")

    return {
        "schema_validation_failures": failures,
        "warnings": warnings,
        "missing_artifact_reference_count": missing_artifact_reference_count,
        "missing_context_reference_count": missing_context_reference_count,
    }


def _validate_lineage(record: dict[str, Any], prefix: str) -> list[str]:
    errors: list[str] = []
    if not record_has_lineage(record):
        errors.append(f"{prefix}: missing source lineage fields")
    return errors
