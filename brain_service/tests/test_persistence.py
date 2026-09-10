from __future__ import annotations

from brain.schemas.common import ValidationStatus
from brain_service.persistence import apply_reconciliation
from brain_service.tests.conftest import make_entity
from brain_service.types import (
    ClassifiedCandidate,
    ClassifiedRecordKind,
    ReconciliationDecision,
    ReconciliationOutcome,
)

SCOPE = "operational_sources/test"


def _classified(record_kind: ClassifiedRecordKind, proposed_fields: dict | None = None) -> ClassifiedCandidate:
    return ClassifiedCandidate(
        record_kind=record_kind,
        proposed_fields=proposed_fields or {},
        confidence="medium",
        rationale="test",
        source_evidence_ids=["evidence:test:seed"],
    )


def test_reinforce_unions_source_refs_into_existing_record(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope=SCOPE)
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.REINFORCE,
        classified=_classified(ClassifiedRecordKind.ENTITY),
        affected_record_ids=["entity:system:a"],
        rationale="confirms existing fact",
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is not None
    assert "evidence:test:seed" in result.written_record.source_refs
    assert result.written_record.validation_status == ValidationStatus.OPERATIONAL_UNREVIEWED


def test_patch_applies_field_changes_to_existing_record(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope=SCOPE)
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.PATCH,
        classified=_classified(ClassifiedRecordKind.ENTITY),
        affected_record_ids=["entity:system:a"],
        patch_fields={"aliases": ["Alt Name"]},
        rationale="adds alias",
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record.aliases == ["Alt Name"]


def test_patch_fails_gracefully_when_target_does_not_exist(storage) -> None:
    # affected_record_ids naming an id that isn't in the corpus is caught by
    # validate_and_prepare_for_review's own dangling-reference check FIRST
    # (apply_reconciliation always validates before writing) -- this test
    # confirms that mechanical check, still surfacing as a clean
    # skipped_reason with no write attempted, not a crash inside the write
    # step itself.
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.PATCH,
        classified=_classified(ClassifiedRecordKind.ENTITY),
        affected_record_ids=["entity:system:does_not_exist"],
        patch_fields={"aliases": ["x"]},
        rationale="x",
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is None
    assert result.skipped_reason is not None
    assert "does not exist" in result.skipped_reason or "unknown record" in result.skipped_reason


def test_new_candidate_entity_is_created_with_unreviewed_status(storage) -> None:
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.ENTITY,
            {"entity_type": "symptom", "name": "Tote stuck", "description": "A tote fails to progress."},
        ),
        affected_record_ids=[],
        rationale="genuinely new",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is not None
    assert result.written_record.id == "entity:symptom:tote_stuck"
    assert result.written_record.validation_status == ValidationStatus.OPERATIONAL_UNREVIEWED
    loaded = storage.load_brain_records(scope=SCOPE)
    assert any(r.id == "entity:symptom:tote_stuck" for r in loaded)


def test_new_candidate_claim_is_created(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope=SCOPE)
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.CLAIM,
            {
                "subject_entity_id": "entity:system:a",
                "predicate": "has_fact",
                "object": {"kind": "literal", "value": "something happened"},
                "polarity": "affirmed",
            },
        ),
        affected_record_ids=[],
        rationale="new fact",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is not None
    assert result.written_record.subject_entity_id == "entity:system:a"


def test_new_candidate_refuses_to_overwrite_existing_id(storage) -> None:
    storage.save_brain_records([make_entity("entity:symptom:tote_stuck", entity_type=None)], scope=SCOPE)
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.ENTITY,
            {"entity_type": "symptom", "name": "Tote stuck", "description": "duplicate attempt"},
        ),
        affected_record_ids=[],
        rationale="x",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is None
    assert "already exists" in result.skipped_reason


def test_conflict_creates_new_claim_without_touching_original(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope=SCOPE)
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.CONFLICT,
        classified=_classified(
            ClassifiedRecordKind.CLAIM,
            {
                "subject_entity_id": "entity:system:a",
                "predicate": "resolved_by",
                "object": {"kind": "literal", "value": "restart fixed it"},
                "polarity": "affirmed",
            },
        ),
        affected_record_ids=["entity:system:a"],
        conflicts_with_claim_id="claim:existing:fact",
        rationale="disagrees",
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is not None
    assert result.written_record.validation_status == ValidationStatus.CONFLICTING
    assert "claim:existing:fact" in result.written_record.note
    # Original entity untouched.
    original = storage.load_brain_records(scope=SCOPE)
    assert any(r.id == "entity:system:a" for r in original)


def test_gap_writes_only_the_review_no_record(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope=SCOPE)
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.GAP,
        classified=_classified(ClassifiedRecordKind.ENTITY),
        affected_record_ids=["entity:system:a"],
        rationale="something missing",
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is None
    assert result.skipped_reason == "GAP has no record to write"
    assert result.review.status == "open"


def test_missing_evidence_ids_still_only_writes_a_review(storage) -> None:
    classified = ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.ENTITY, proposed_fields={}, confidence="low", rationale="x",
        source_evidence_ids=[],
    )
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.PATCH,
        classified=classified,
        affected_record_ids=["entity:system:a"],
        rationale="x",
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is None
    assert "no source_evidence_ids" in result.skipped_reason


def test_new_candidate_claim_with_unresolved_subject_gets_a_clear_actionable_review(storage) -> None:
    """Regression test for a real bug found running this against live Azure
    OpenAI: the LLM correctly recognizes a claim's subject has no existing
    Entity yet and returns subject_entity_id=None with a proposed name --
    this must surface as a clear "create the Entity first" message, not a
    generic crash or WRITE FAILED."""
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.CLAIM,
            {
                "subject_entity_id": None,
                "subject_entity_name": "OptiSweep service",
                "predicate": "restart status",
                "object": "was restarted after a heartbeat failure",
                "polarity": "AFFIRMED",
            },
        ),
        affected_record_ids=[],
        rationale="new fact about an unresolved subject",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is None
    assert "NEEDS ENTITY FIRST" in result.review.proposed_change
    assert "OptiSweep service" in result.review.proposed_change


def test_new_candidate_claim_normalizes_uppercase_polarity_and_bare_string_object(storage) -> None:
    """Same real-world response shape as above, but with a resolvable
    subject -- confirms uppercase "AFFIRMED" and a bare-string object (both
    observed from a real Azure OpenAI response, not schema-conformant JSON)
    are normalized rather than rejected."""
    storage.save_brain_records([make_entity("entity:system:optisweep_service")], scope=SCOPE)
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.CLAIM,
            {
                "subject_entity_id": "entity:system:optisweep_service",
                "predicate": "restart status",
                "object": "was restarted after a heartbeat failure",  # bare string, not {"kind": ..., "value": ...}
                "polarity": "AFFIRMED",  # uppercase, not the schema's lowercase "affirmed"
            },
        ),
        affected_record_ids=[],
        rationale="new fact",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is not None
    assert result.written_record.polarity.value == "affirmed"
    assert result.written_record.object.value == "was restarted after a heartbeat failure"


def test_new_candidate_relationship_between_two_nonexistent_entities_refuses_to_write(storage) -> None:
    """Regression test for a real bug found by direct testing (not caught
    by any prior test): _build_relationship only checked from_id/to_id
    were WELL-FORMED strings (is_well_formed_id), never that they actually
    resolve to a real entity -- a relationship between two invented ids
    previously wrote silently, creating a dangling reference nothing else
    in the corpus would ever catch until a full validate_batch() run."""
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.RELATIONSHIP,
            {
                "from_id": "entity:system:not_created_yet",
                "to_id": "entity:system:also_not_created",
                "relationship_type": "controls",
            },
        ),
        affected_record_ids=[],
        rationale="new relationship",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is None
    assert "NEEDS ENTITY FIRST" in result.review.proposed_change
    assert "not_created_yet" in result.review.proposed_change
    assert storage.load_brain_records(scope=SCOPE, record_type=None) == [result.review]


def test_new_candidate_relationship_with_one_real_and_one_fake_entity_refuses_to_write(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope=SCOPE)
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.RELATIONSHIP,
            {"from_id": "entity:system:a", "to_id": "entity:system:invented", "relationship_type": "controls"},
        ),
        affected_record_ids=[],
        rationale="x",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is None
    assert "entity:system:invented" in result.review.proposed_change


def test_new_candidate_relationship_between_two_real_entities_writes_successfully(storage) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:a"), make_entity("entity:system:b")], scope=SCOPE
    )
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.RELATIONSHIP,
            {"from_id": "entity:system:a", "to_id": "entity:system:b", "relationship_type": "controls"},
        ),
        affected_record_ids=[],
        rationale="genuinely new relationship",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is not None
    assert result.written_record.from_id == "entity:system:a"
    assert result.written_record.to_id == "entity:system:b"
    assert result.written_record.relationship_type.value == "controls"


def test_new_candidate_claim_with_invented_but_well_formed_subject_id_refuses_to_write(storage) -> None:
    """Same class of bug as the relationship test above, for Claim.subject_entity_id
    specifically -- distinct from test_new_candidate_claim_with_unresolved_subject_gets_a_clear_actionable_review,
    which covers subject_entity_id=None (explicitly unresolved). This
    covers a NON-None id that merely looks valid but doesn't exist."""
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.CLAIM,
            {
                "subject_entity_id": "entity:system:invented_id_that_does_not_exist",
                "predicate": "has_fact",
                "object": {"kind": "literal", "value": "x"},
                "polarity": "affirmed",
            },
        ),
        affected_record_ids=[],
        rationale="x",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is None
    assert "NEEDS ENTITY FIRST" in result.review.proposed_change


def test_new_candidate_capability_with_invented_target_entity_refuses_to_write(storage) -> None:
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.CAPABILITY,
            {
                "name": "Do The Thing",
                "description": "x",
                "capability_kind": "diagnostic",
                "target_entity_ids": ["entity:system:invented"],
            },
        ),
        affected_record_ids=[],
        rationale="x",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is None
    assert "entity:system:invented" in result.review.proposed_change


def test_new_candidate_capability_with_real_target_entity_writes_successfully(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope=SCOPE)
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(
            ClassifiedRecordKind.CAPABILITY,
            {
                "name": "Verify System A",
                "description": "x",
                "capability_kind": "diagnostic",
                "target_entity_ids": ["entity:system:a"],
            },
        ),
        affected_record_ids=[],
        rationale="genuinely new capability",
        duplicate_check_performed=True,
    )

    result = apply_reconciliation(storage, decision, scope=SCOPE)

    assert result.written_record is not None
    assert result.written_record.target_entity_ids == ["entity:system:a"]
    assert result.written_record.capability_kind.value == "diagnostic"


def test_patch_writes_back_to_the_target_records_own_scope_not_the_caller_scope(storage) -> None:
    """Regression test for a real bug found testing this live (2026-09-09):
    a record living in "operational_sources/shared" was patched while
    ingesting an unrelated "incidents/case_new" scope -- the merge
    previously wrote a SECOND, divergent copy of the record into
    incidents/case_new instead of updating the original in
    operational_sources/shared, leaving the real record untouched. This
    verifies the fix: the merged record lands in its own original scope,
    and the ingestion scope receives only the BrainReview audit trail."""
    OWN_SCOPE = "operational_sources/shared"
    INGESTION_SCOPE = "incidents/case_new"
    storage.save_brain_records([make_entity("entity:system:shared_target")], scope=OWN_SCOPE)

    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.PATCH,
        classified=_classified(ClassifiedRecordKind.ENTITY),
        affected_record_ids=["entity:system:shared_target"],
        patch_fields={"aliases": ["New Alias From Incident"]},
        rationale="patched while ingesting an unrelated incident",
    )

    result = apply_reconciliation(storage, decision, scope=INGESTION_SCOPE)

    assert result.written_record is not None
    assert result.written_record.aliases == ["New Alias From Incident"]

    # The merged record must be in its OWN scope, not duplicated into the
    # ingestion scope.
    own_scope_records = storage.load_brain_records(scope=OWN_SCOPE)
    assert len(own_scope_records) == 1
    assert own_scope_records[0].aliases == ["New Alias From Incident"]

    ingestion_scope_records = storage.load_brain_records(scope=INGESTION_SCOPE)
    assert len(ingestion_scope_records) == 1
    assert ingestion_scope_records[0].type.value == "review"  # only the audit trail, not a duplicate entity
