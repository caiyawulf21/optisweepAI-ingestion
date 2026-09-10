"""Coverage for the in-tandem Brain hook wired into
extract_operational_context. Same gate pattern as the incidence pipeline's
stage hooks (see incidenceknowledgeingestion/tests/test_stage4_brain_hook.py)."""

from __future__ import annotations

import pytest

from optisweep_ingestion.stage4_operational_context import (
    _ingest_operational_context_into_brain,
)


@pytest.fixture(autouse=True)
def _clean_gate_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BRAIN_INGESTION_ENABLED", raising=False)


def test_hook_is_a_noop_when_gate_is_explicitly_off(monkeypatch: pytest.MonkeyPatch) -> None:
    # 2026-09-09: the gate now defaults ON, so testing the off-path
    # requires explicitly disabling it.
    monkeypatch.setenv("BRAIN_INGESTION_ENABLED", "0")
    _ingest_operational_context_into_brain(
        contexts=[{"context_id": "ctx_1", "summary": "x"}],
        source_id="manual_optisweep_om_v3",
    )


def test_hook_calls_ingest_stage_output_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("providers.azure_openai_llm.AzureOpenAILLMProvider", lambda: object())
    monkeypatch.setattr("providers.local_storage.LocalStorageProvider", lambda: object())
    calls = []
    monkeypatch.setattr(
        "brain_service.pipeline_hook.ingest_stage_output",
        lambda **kwargs: calls.append(kwargs),
    )

    _ingest_operational_context_into_brain(
        contexts=[{"context_id": "ctx_1", "summary": "x"}],
        source_id="manual_optisweep_om_v3",
    )

    assert len(calls) == 1


def test_hook_is_a_noop_with_no_source_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BRAIN_INGESTION_ENABLED", "1")
    calls = []
    monkeypatch.setattr(
        "brain_service.pipeline_hook.ingest_stage_output",
        lambda **kwargs: calls.append(kwargs),
    )

    _ingest_operational_context_into_brain(contexts=[{"context_id": "ctx_1"}], source_id="")

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

    _ingest_operational_context_into_brain(
        contexts=[{"context_id": "ctx_1", "summary": "x"}],
        source_id="manual_optisweep_om_v3",
    )

    assert len(calls) == 1
    call = calls[0]
    assert call["pipeline"] == "operational"
    assert call["stage_name"] == "stage4_operational_context"
    assert call["source_id"] == "manual_optisweep_om_v3"
    assert call["scope"] == "operational_sources/manual_optisweep_om_v3"
    assert call["record_kind"] == "operational_context_record"
    assert call["records"][0]["context_id"] == "ctx_1"
