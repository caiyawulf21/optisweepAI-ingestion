from __future__ import annotations

import os

import pytest

from brain_service.pipeline_hook import brain_enabled, ingest_stage_output
from brain_service.tests.conftest import ScriptedLLM, make_entity
from brain_service.types import (
    ClassifiedCandidate,
    ClassifiedRecordKind,
    EvidenceCandidate,
    ExtractEvidenceResult,
    ReconciliationDecision,
    ReconciliationOutcome,
)


@pytest.fixture(autouse=True)
def _clean_gate_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BRAIN_INGESTION_ENABLED", raising=False)


def test_brain_enabled_defaults_on(monkeypatch: pytest.MonkeyPatch) -> None:
    # 2026-09-09: "brain ingestion should always be enabled" -- unset means
    # ON now, a deliberate reversal of the original default-off gate.
    monkeypatch.delenv("BRAIN_INGESTION_ENABLED", raising=False)
    assert brain_enabled() is True


@pytest.mark.parametrize("value", ["1", "true", "True", "yes", "YES"])
def test_brain_enabled_true_for_truthy_values(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("BRAIN_INGESTION_ENABLED", value)
    assert brain_enabled() is True


@pytest.mark.parametrize("value", ["0", "false", "no", ""])
def test_brain_enabled_false_for_falsy_values(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("BRAIN_INGESTION_ENABLED", value)
    assert brain_enabled() is False


def _happy_path_llm() -> ScriptedLLM:
    extraction = ExtractEvidenceResult(
        candidates=[
            EvidenceCandidate(
                evidence_kind="incident_timeline_event",
                content_text="bots stopped moving",
                is_verbatim=False,
                raw_claim_candidates=["bots stopped moving"],
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
        outcome=ReconciliationOutcome.REINFORCE,
        classified=classified,
        affected_record_ids=["entity:system:seed"],
        rationale="test",
        duplicate_check_performed=True,
    )
    return ScriptedLLM(
        {
            ExtractEvidenceResult: [extraction] * 5,
            ClassifiedCandidate: [classified] * 5,
            ReconciliationDecision: [decision] * 5,
        }
    )


def test_ingest_stage_output_succeeds_for_reinforce(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:seed")], scope="operational_sources/seed")

    result = ingest_stage_output(
        llm=_happy_path_llm(),
        storage=storage,
        pipeline="incidence",
        stage_name="stage4_canonical_incident_record",
        source_id="case:228086",
        scope="incidents/case_228086",
        records=[{"event_id": "evt_1", "text": "bots stopped moving"}],
        record_kind="incident_timeline_event",
    )

    assert result.succeeded_count == 1
    assert result.pipeline == "incidence"
    assert result.stage_name == "stage4_canonical_incident_record"


def test_ingest_stage_output_continues_past_single_record_failure(storage) -> None:
    # No seed entity -- "entity:system:seed" dangles, so the record fails,
    # but the hook must still process the remaining records rather than
    # aborting the whole stage's output.
    result = ingest_stage_output(
        llm=_happy_path_llm(),
        storage=storage,
        pipeline="incidence",
        stage_name="stage4_canonical_incident_record",
        source_id="case:228086",
        scope="incidents/case_228086",
        records=[{"event_id": "evt_1"}, {"event_id": "evt_2"}],
        record_kind="incident_timeline_event",
    )

    assert len(result.outcomes) == 2
    assert result.failed_count == 2


def test_ingest_stage_output_surfaces_systemic_failure() -> None:
    class AlwaysFailLLM:
        def generate_json(self, **kwargs):
            raise RuntimeError("simulated systemic failure")

        def generate_text(self, **kwargs):
            raise NotImplementedError

    from providers.local_storage import LocalStorageProvider
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        result = ingest_stage_output(
            llm=AlwaysFailLLM(),
            storage=LocalStorageProvider(root=Path(tmp)),
            pipeline="operational",
            stage_name="stage4_operational_context",
            source_id="manual_optisweep_om_v3",
            scope="operational_sources/manual_optisweep_om_v3",
            records=[{"i": i} for i in range(5)],
            record_kind="operational_context_record",
        )

    assert result.systemic_failure_detected is True
    assert len(result.outcomes) == 3
