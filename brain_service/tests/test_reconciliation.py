from __future__ import annotations

from brain_service.reconciliation import reconcile_candidate
from brain_service.tests.conftest import ScriptedLLM, make_entity
from brain_service.types import (
    ClassifiedCandidate,
    ClassifiedRecordKind,
    ReconciliationDecision,
    ReconciliationOutcome,
)


def _classified() -> ClassifiedCandidate:
    return ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.ENTITY,
        proposed_fields={"name": "Something New"},
        confidence="medium",
        rationale="test",
        source_evidence_ids=["evidence:test:seed"],
    )


def test_reconcile_candidate_returns_llm_decision(storage) -> None:
    expected = ReconciliationDecision(
        outcome=ReconciliationOutcome.REINFORCE,
        classified=_classified(),
        affected_record_ids=["entity:system:existing"],
        rationale="already known",
    )
    llm = ScriptedLLM({ReconciliationDecision: [expected]})

    result = reconcile_candidate(llm, storage, _classified())

    assert result.outcome == ReconciliationOutcome.REINFORCE
    assert result.affected_record_ids == ["entity:system:existing"]


def test_new_candidate_triggers_duplicate_check(storage, monkeypatch) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:geekagv", name="GeekAgv"), make_entity("entity:system:geek_agv", name="geek_agv")],
        scope="operational_sources/test",
    )
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.NEW_CANDIDATE,
        classified=_classified(),
        affected_record_ids=["entity:system:geekagv"],
        rationale="looks new",
        duplicate_check_performed=False,
    )
    llm = ScriptedLLM({ReconciliationDecision: [decision]})

    calls = []
    import brain_service.reconciliation as reconciliation_module

    original = reconciliation_module.find_audit_candidates

    def spy(storage_arg, record_ids=None):
        calls.append(record_ids)
        return original(storage_arg, record_ids=record_ids)

    monkeypatch.setattr(reconciliation_module, "find_audit_candidates", spy)

    result = reconcile_candidate(llm, storage, _classified())

    assert len(calls) == 1
    assert result.duplicate_check_performed is True


def test_non_new_candidate_does_not_trigger_duplicate_check(storage, monkeypatch) -> None:
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.PATCH,
        classified=_classified(),
        affected_record_ids=["entity:system:a"],
        rationale="patch",
    )
    llm = ScriptedLLM({ReconciliationDecision: [decision]})

    import brain_service.reconciliation as reconciliation_module

    calls = []
    monkeypatch.setattr(
        reconciliation_module,
        "find_audit_candidates",
        lambda *a, **k: calls.append(1) or [],
    )

    reconcile_candidate(llm, storage, _classified())

    assert calls == []
