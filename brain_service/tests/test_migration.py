from __future__ import annotations

from brain_service.migration import run_migration_batch
from brain_service.tests.conftest import ScriptedLLM, make_entity
from brain_service.types import (
    ClassifiedCandidate,
    ClassifiedRecordKind,
    EvidenceCandidate,
    ExtractEvidenceResult,
    ReconciliationDecision,
    ReconciliationOutcome,
)


def _happy_path_llm(outcome: ReconciliationOutcome) -> ScriptedLLM:
    extraction = ExtractEvidenceResult(
        candidates=[
            EvidenceCandidate(
                evidence_kind="incident_timeline_event",
                content_text="something happened",
                is_verbatim=False,
                raw_claim_candidates=["something happened"],
            )
        ]
    )
    classified = ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.CLAIM,
        proposed_fields={"subject_entity_id": "entity:system:seed"},
        confidence="medium",
        rationale="test",
        source_evidence_ids=["evidence:test:seed"],
    )
    decision = ReconciliationDecision(
        outcome=outcome,
        classified=classified,
        affected_record_ids=["entity:system:seed"],
        rationale="test decision",
        duplicate_check_performed=True,
    )
    return ScriptedLLM(
        {
            ExtractEvidenceResult: [extraction] * 10,
            ClassifiedCandidate: [classified] * 10,
            ReconciliationDecision: [decision] * 10,
        }
    )


def test_batch_marks_reinforce_items_succeeded(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:seed")], scope="operational_sources/seed")
    llm = _happy_path_llm(ReconciliationOutcome.REINFORCE)

    report = run_migration_batch(
        llm, storage, ["item_1", "item_2"], load_source_packet=lambda item: {"item": item}
    )

    assert report.succeeded_count == 2
    assert report.needs_human_review_count == 0
    assert report.failed_count == 0


def test_batch_marks_gap_items_needs_human_review(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:seed")], scope="operational_sources/seed")
    llm = _happy_path_llm(ReconciliationOutcome.GAP)

    report = run_migration_batch(
        llm, storage, ["item_1"], load_source_packet=lambda item: {"item": item}
    )

    assert report.needs_human_review_count == 1


def test_batch_marks_items_failed_when_affected_record_unknown(storage) -> None:
    # No entity seeded -- "entity:system:seed" will dangle.
    llm = _happy_path_llm(ReconciliationOutcome.PATCH)

    report = run_migration_batch(
        llm, storage, ["item_1"], load_source_packet=lambda item: {"item": item}
    )

    assert report.failed_count == 1


def test_batch_stops_after_three_consecutive_identical_failures(storage) -> None:
    class AlwaysFailLLM:
        def generate_json(self, **kwargs):
            raise RuntimeError("simulated persistent failure")

        def generate_text(self, **kwargs):
            raise NotImplementedError

    report = run_migration_batch(
        AlwaysFailLLM(),
        storage,
        ["a", "b", "c", "d", "e"],
        load_source_packet=lambda item: {"item": item},
    )

    assert len(report.outcomes) == 3
    assert report.systemic_failure_detected is True
    assert "simulated persistent failure" in report.systemic_failure_detail


def test_batch_does_not_stop_on_intermittent_different_failures(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:seed")], scope="operational_sources/seed")
    happy_llm = _happy_path_llm(ReconciliationOutcome.REINFORCE)

    call_count = {"n": 0}
    real_generate_json = happy_llm.generate_json

    def flaky_generate_json(*, system_prompt, user_content, schema, label, max_attempts=2):
        call_count["n"] += 1
        if call_count["n"] in (2, 4):  # fails on 2 different items, not 3 in a row
            raise RuntimeError(f"transient error #{call_count['n']}")
        return real_generate_json(
            system_prompt=system_prompt, user_content=user_content, schema=schema, label=label
        )

    happy_llm.generate_json = flaky_generate_json  # type: ignore[method-assign]

    report = run_migration_batch(
        happy_llm, storage, ["a", "b", "c", "d", "e"], load_source_packet=lambda item: {"item": item}
    )

    assert len(report.outcomes) == 5
    assert report.systemic_failure_detected is False
