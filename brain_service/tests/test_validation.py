from __future__ import annotations

from brain_service.tests.conftest import make_entity
from brain_service.types import (
    ClassifiedCandidate,
    ClassifiedRecordKind,
    ReconciliationDecision,
    ReconciliationOutcome,
)
from brain_service.validation import validate_and_prepare_for_review, validate_records


def _classified(source_evidence_ids: list[str] | None = ["evidence:test:seed"]) -> ClassifiedCandidate:
    # A default MUTABLE-looking arg is safe here since it's never mutated,
    # and using `or` in the body would (as an earlier version of this
    # helper did) silently turn an explicit source_evidence_ids=[] into the
    # default list instead of an actually-empty one, which is exactly the
    # case test_missing_evidence_ids_fails_validation needs to construct.
    return ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.CLAIM,
        proposed_fields={},
        confidence="medium",
        rationale="test rationale",
        source_evidence_ids=list(source_evidence_ids) if source_evidence_ids is not None else [],
    )


def test_valid_decision_produces_open_review_with_evidence(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope="incidents/case_1")
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(),
        affected_record_ids=["entity:system:a"],
        rationale="new fact",
        duplicate_check_performed=True,
    )

    review = validate_and_prepare_for_review(storage, decision)

    assert review.status == "open"
    assert "VALIDATION FAILED" not in review.proposed_change
    assert review.source_refs == ["evidence:test:seed"]


def test_missing_evidence_ids_fails_validation(storage) -> None:
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.GAP,
        classified=_classified(source_evidence_ids=[]),
        affected_record_ids=["entity:system:a"],
        rationale="gap",
    )

    review = validate_and_prepare_for_review(storage, decision)

    assert "no source_evidence_ids" in review.proposed_change


def test_dangling_affected_record_id_fails_validation(storage) -> None:
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.PATCH,
        classified=_classified(),
        affected_record_ids=["entity:system:does_not_exist"],
        rationale="patch",
    )

    review = validate_and_prepare_for_review(storage, decision)

    assert "unknown record" in review.proposed_change


def test_patch_description_names_changed_fields(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope="incidents/case_1")
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.PATCH,
        classified=_classified(),
        affected_record_ids=["entity:system:a"],
        patch_fields={"aliases": ["Alpha"], "description": "richer text"},
        rationale="adds detail",
    )

    review = validate_and_prepare_for_review(storage, decision)

    assert "aliases" in review.proposed_change
    assert "description" in review.proposed_change


def test_conflict_description_names_the_conflicting_claim(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope="incidents/case_1")
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.CONFLICT,
        classified=_classified(),
        affected_record_ids=["entity:system:a"],
        conflicts_with_claim_id="claim:a:existing_fact",
        rationale="disagrees",
    )

    review = validate_and_prepare_for_review(storage, decision)

    assert "claim:a:existing_fact" in review.proposed_change
    assert "Both readings are kept" in review.proposed_change


def test_validate_records_bare_check_returns_valid_for_clean_batch() -> None:
    entity = make_entity("entity:system:a")
    result = validate_records({"entities": [entity]})
    assert result.valid is True
    assert result.errors == []
