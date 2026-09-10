"""Tool 4 -- validate_and_prepare_for_review (AGENT_DESIGN_NOTES.md §4.2),
plus validate_records() and validate_incident_pipeline_output() as bare
mechanical checks that don't produce a BrainReview.

validate_and_prepare_for_review never calls an LLM to approve -- it
mechanically verifies (pydantic schema + validate_batch() + non-empty
source_refs) and, on success, drafts a plain-language BrainReview for a
human to approve. Approval stays a human action outside this tool.
"""

from __future__ import annotations

from typing import Any

from brain.schemas.claim import Claim
from brain.schemas.common import RecordType
from brain.schemas.review import ReviewKind
from brain.validators import BrainRecordUnion, ValidationResult, validate_batch
from brain_service.review import build_review
from brain_service.types import ReconciliationDecision, ReconciliationOutcome
from providers.storage import StorageProvider

_OUTCOME_TO_REVIEW_KIND = {
    ReconciliationOutcome.REINFORCE: ReviewKind.REINFORCE,
    ReconciliationOutcome.PATCH: ReviewKind.PATCH,
    ReconciliationOutcome.CONFLICT: ReviewKind.CONFLICT,
    ReconciliationOutcome.GAP: ReviewKind.GAP,
    ReconciliationOutcome.NEW_CANDIDATE: ReviewKind.NEW_CANDIDATE,
}

_RECORD_TYPE_LISTS = (
    "evidence_units",
    "entities",
    "claims",
    "relationships",
    "capabilities",
    "procedures",
    "playbooks",
    "reviews",
)


def validate_records(records_by_type: dict[str, list[BrainRecordUnion]]) -> ValidationResult:
    """Bare schema + validate_batch() check with no review-drafting, for
    callers (e.g. run_migration_batch's own status checks) that need a
    yes/no rather than a review artifact."""
    kwargs = {key: records_by_type.get(key, []) for key in _RECORD_TYPE_LISTS}
    return validate_batch(**kwargs)


def validate_and_prepare_for_review(
    storage: StorageProvider,
    reconciled: ReconciliationDecision,
) -> Any:
    """Mechanically verifies the reconciled candidate, then drafts a
    BrainReview for human approval. On mechanical failure, returns a
    BrainReview whose status stays "open" with the validation errors
    attached in proposed_change -- never attempts to silently self-correct."""
    kind = _OUTCOME_TO_REVIEW_KIND[reconciled.outcome]
    affected_ids = reconciled.affected_record_ids or []
    evidence_ids = reconciled.classified.source_evidence_ids

    if not evidence_ids:
        return build_review(
            kind=kind,
            affected_record_ids=affected_ids or ["unknown"],
            proposed_change=(
                "VALIDATION FAILED: candidate carries no source_evidence_ids -- "
                "every derived record must cite provenance (Part 1 §1.2)."
            ),
        )

    existing_ids = {record.id for record in storage.load_brain_context()}
    dangling = [rid for rid in affected_ids if rid and rid not in existing_ids]
    if dangling:
        return build_review(
            kind=kind,
            affected_record_ids=affected_ids,
            proposed_change=(
                f"VALIDATION FAILED: affected_record_ids references unknown record(s): {dangling}."
            ),
            source_refs=evidence_ids,
        )

    proposed_change = _describe_change(reconciled)
    return build_review(
        kind=kind,
        affected_record_ids=affected_ids or evidence_ids,
        proposed_change=proposed_change,
        source_refs=evidence_ids,
    )


def _describe_change(reconciled: ReconciliationDecision) -> str:
    outcome = reconciled.outcome.value
    kind = reconciled.classified.record_kind.value
    if reconciled.outcome == ReconciliationOutcome.PATCH:
        fields = ", ".join(sorted(reconciled.patch_fields)) or "(no fields specified)"
        return f"PATCH ({kind}): {reconciled.rationale} Fields changed: {fields}."
    if reconciled.outcome == ReconciliationOutcome.CONFLICT:
        return (
            f"CONFLICT ({kind}) with {reconciled.conflicts_with_claim_id}: {reconciled.rationale} "
            "Both readings are kept; a human must resolve which is current."
        )
    return f"{outcome.upper()} ({kind}): {reconciled.rationale}"
