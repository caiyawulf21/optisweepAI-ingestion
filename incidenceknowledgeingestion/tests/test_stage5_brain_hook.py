"""Coverage for the in-tandem Brain hook wired into
create_stage5_incident_candidates. Same gate pattern as Stage 4's hook --
see test_stage4_brain_hook.py."""

from __future__ import annotations

import pytest

from optisweep_incidence_ingestion.stage5_runbook_candidates import (
    _ingest_runbook_candidates_into_brain,
)


@pytest.fixture(autouse=True)
def _clean_gate_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BRAIN_INGESTION_ENABLED", raising=False)


def test_hook_is_a_noop_when_gate_is_explicitly_off(monkeypatch: pytest.MonkeyPatch) -> None:
    # 2026-09-09: the gate now defaults ON, so testing the off-path
    # requires explicitly disabling it.
    monkeypatch.setenv("BRAIN_INGESTION_ENABLED", "0")
    _ingest_runbook_candidates_into_brain(
        runbook_candidates=[{"candidate_id": "c1", "candidate_goal": "x"}],
        package={"source_case_id": "228086"},
    )


def test_hook_calls_ingest_stage_output_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("providers.azure_openai_llm.AzureOpenAILLMProvider", lambda: object())
    monkeypatch.setattr("providers.local_storage.LocalStorageProvider", lambda: object())
    calls = []
    monkeypatch.setattr(
        "brain_service.pipeline_hook.ingest_stage_output",
        lambda **kwargs: calls.append(kwargs),
    )

    _ingest_runbook_candidates_into_brain(
        runbook_candidates=[{"candidate_id": "c1", "candidate_goal": "x"}],
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

    _ingest_runbook_candidates_into_brain(
        runbook_candidates=[{"candidate_id": "c1", "candidate_goal": "x"}],
        package={},
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

    _ingest_runbook_candidates_into_brain(
        runbook_candidates=[{"candidate_id": "c1", "candidate_goal": "x"}],
        package={"source_case_id": "228086"},
    )

    assert len(calls) == 1
    call = calls[0]
    assert call["stage_name"] == "stage5_runbook_candidates"
    assert call["source_id"] == "case:228086"
    assert call["record_kind"] == "runbook_candidate"
    assert call["records"][0]["candidate_id"] == "c1"
