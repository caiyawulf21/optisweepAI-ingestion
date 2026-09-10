"""Coverage for the in-tandem Brain hook wired into
create_stage4_canonical_incident_record_and_timeline (BRAIN_AGENT plan §5:
the hook lives inside each stage module's own function, gated by
BRAIN_INGESTION_ENABLED so every existing caller of this stage function --
including the rest of this test suite -- keeps working with zero network
dependency by default."""

from __future__ import annotations

import pytest

from optisweep_incidence_ingestion.stage4_canonical_incident_record import (
    _ingest_timeline_events_into_brain,
)


@pytest.fixture(autouse=True)
def _clean_gate_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BRAIN_INGESTION_ENABLED", raising=False)


def test_hook_is_a_noop_when_gate_is_explicitly_off(monkeypatch: pytest.MonkeyPatch) -> None:
    # 2026-09-09: the gate now defaults ON, so testing the off-path
    # requires explicitly disabling it. No providers/brain_service module
    # should be touched -- if the gate check didn't short-circuit first,
    # this would attempt a real Azure OpenAI provider construction and
    # raise RuntimeError for missing credentials (see
    # providers.azure_openai_llm.AzureOpenAILLMProvider), which is exactly
    # what must NOT happen when the gate is off.
    monkeypatch.setenv("BRAIN_INGESTION_ENABLED", "0")
    _ingest_timeline_events_into_brain(
        timeline_events={"events": [{"event_id": "evt_1", "details": "x"}]},
        package={"source_case_id": "228086"},
    )


def test_hook_calls_ingest_stage_output_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    # No BRAIN_INGESTION_ENABLED set at all -- confirms the new default-on
    # behavior, not just the explicit "1" path already covered below.
    monkeypatch.setattr("providers.azure_openai_llm.AzureOpenAILLMProvider", lambda: object())
    monkeypatch.setattr("providers.local_storage.LocalStorageProvider", lambda: object())
    calls = []
    monkeypatch.setattr(
        "brain_service.pipeline_hook.ingest_stage_output",
        lambda **kwargs: calls.append(kwargs),
    )

    _ingest_timeline_events_into_brain(
        timeline_events={"events": [{"event_id": "evt_1", "event_order": 1, "details": "x"}]},
        package={"source_case_id": "228086"},
    )

    assert len(calls) == 1


def test_hook_is_a_noop_with_no_case_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BRAIN_INGESTION_ENABLED", "1")
    calls = []
    monkeypatch.setattr(
        "brain_service.pipeline_hook.ingest_stage_output",
        lambda **kwargs: calls.append(kwargs),
    )

    _ingest_timeline_events_into_brain(
        timeline_events={"events": [{"event_id": "evt_1", "details": "x"}]},
        package={},  # no source_case_id
    )

    assert calls == []


def test_hook_calls_ingest_stage_output_with_expected_shape(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BRAIN_INGESTION_ENABLED", "1")
    monkeypatch.setattr("providers.azure_openai_llm.AzureOpenAILLMProvider", lambda: object())
    monkeypatch.setattr("providers.local_storage.LocalStorageProvider", lambda: object())

    calls = []
    monkeypatch.setattr(
        "brain_service.pipeline_hook.ingest_stage_output",
        lambda **kwargs: calls.append(kwargs),
    )

    _ingest_timeline_events_into_brain(
        timeline_events={"events": [{"event_id": "evt_1", "event_order": 1, "details": "x"}]},
        package={"source_case_id": "228086"},
    )

    assert len(calls) == 1
    call = calls[0]
    assert call["pipeline"] == "incidence"
    assert call["stage_name"] == "stage4_canonical_incident_record"
    assert call["source_id"] == "case:228086"
    assert call["scope"] == "incidents/case_228086"
    assert call["record_kind"] == "incident_timeline_event"
    assert len(call["records"]) == 1
    assert call["records"][0]["event_id"] == "evt_1"
