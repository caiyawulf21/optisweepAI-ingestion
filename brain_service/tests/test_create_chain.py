from __future__ import annotations

from brain_service.create_chain import run_create_chain
from brain_service.tests.conftest import ScriptedLLM, make_entity
from brain_service.types import (
    ClassifiedCandidate,
    ClassifiedRecordKind,
    EvidenceCandidate,
    ExtractEvidenceResult,
    ReconciliationDecision,
    ReconciliationOutcome,
)

SCOPE = "operational_sources/test"


def _llm_for(
    outcome: ReconciliationOutcome,
    proposed_fields: dict | None = None,
    affected_record_ids: list[str] | None = None,
) -> ScriptedLLM:
    extraction = ExtractEvidenceResult(
        candidates=[
            EvidenceCandidate(
                evidence_kind="sme_note", content_text="something happened", is_verbatim=False,
                raw_claim_candidates=["something happened"],
            )
        ]
    )
    classified = ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.ENTITY,
        proposed_fields=proposed_fields or {},
        confidence="medium", rationale="test", source_evidence_ids=["evidence:test:seed"],
    )
    # NEW_CANDIDATE affects nothing yet (the record doesn't exist until this
    # chain creates it) -- affected_record_ids defaults to empty for that
    # case, non-empty ["entity:system:seed"] for the others, matching what
    # a real decision of each shape actually looks like.
    default_affected = [] if outcome == ReconciliationOutcome.NEW_CANDIDATE else ["entity:system:seed"]
    decision = ReconciliationDecision(
        outcome=outcome, classified=classified,
        affected_record_ids=affected_record_ids if affected_record_ids is not None else default_affected,
        rationale="test", duplicate_check_performed=True,
    )
    return ScriptedLLM(
        {ExtractEvidenceResult: [extraction], ClassifiedCandidate: [classified], ReconciliationDecision: [decision]}
    )


def test_run_create_chain_reinforce_actually_writes_to_storage(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:seed")], scope=SCOPE)
    llm = _llm_for(ReconciliationOutcome.REINFORCE)

    result = run_create_chain(llm, storage, source_packet={"text": "x"}, evidence_id_prefix="test", scope=SCOPE)

    assert result.status == "succeeded"
    assert len(result.written_record_ids) == 1
    updated = storage.load_brain_records(scope=SCOPE)
    seed = next(r for r in updated if r.id == "entity:system:seed")
    assert "evidence:test:seed" in seed.source_refs


def test_run_create_chain_gap_marks_needs_human_review_with_no_write(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:seed")], scope=SCOPE)
    llm = _llm_for(ReconciliationOutcome.GAP)

    result = run_create_chain(llm, storage, source_packet={"text": "x"}, evidence_id_prefix="test", scope=SCOPE)

    assert result.status == "needs_human_review"
    assert result.written_record_ids == []


def test_run_create_chain_new_candidate_writes_and_flags_review(storage) -> None:
    llm = _llm_for(
        ReconciliationOutcome.NEW_CANDIDATE,
        proposed_fields={"entity_type": "symptom", "name": "New Symptom", "description": "x"},
    )

    result = run_create_chain(llm, storage, source_packet={"text": "x"}, evidence_id_prefix="test", scope=SCOPE)

    assert result.status == "needs_human_review"
    assert len(result.written_record_ids) == 1
    written = storage.load_brain_records(scope=SCOPE)
    assert any(r.id == "entity:symptom:new_symptom" for r in written)
