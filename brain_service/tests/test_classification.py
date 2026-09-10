from __future__ import annotations

import json

from brain_service.classification import classify_candidate
from brain_service.tests.conftest import ScriptedLLM, make_entity
from brain_service.types import ClassifiedCandidate, ClassifiedRecordKind


def test_classify_candidate_returns_llm_response(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:agv_fleet")], scope="operational_sources/test")
    expected = ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.CLAIM,
        proposed_fields={"subject_entity_id": "entity:system:agv_fleet"},
        confidence="high",
        rationale="matches an existing entity",
        source_evidence_ids=["evidence:test:1"],
    )
    llm = ScriptedLLM({ClassifiedCandidate: [expected]})

    result = classify_candidate(
        llm,
        storage,
        candidate_text="AGVs stopped moving",
        evidence_id="evidence:test:1",
        likely_entity_ids=["entity:system:agv_fleet"],
    )

    assert result == expected


def test_classify_candidate_passes_retrieved_context_to_llm(storage, monkeypatch) -> None:
    storage.save_brain_records([make_entity("entity:system:agv_fleet")], scope="operational_sources/test")
    captured: dict = {}

    class CapturingLLM:
        def generate_json(self, *, system_prompt, user_content, schema, label, max_attempts=2):
            captured["user_content"] = user_content
            captured["label"] = label
            return ClassifiedCandidate(
                record_kind=ClassifiedRecordKind.ENTITY,
                proposed_fields={},
                confidence="low",
                rationale="x",
            )

        def generate_text(self, **kwargs):
            raise NotImplementedError

    classify_candidate(
        CapturingLLM(),
        storage,
        candidate_text="a new fact",
        evidence_id="evidence:test:2",
        likely_entity_ids=["entity:system:agv_fleet"],
    )

    payload = json.loads(captured["user_content"])
    assert payload["candidate_text"] == "a new fact"
    assert payload["evidence_id"] == "evidence:test:2"
    assert "entity:system:agv_fleet" in payload["retrieved_context"]["entities"]
    assert captured["label"] == "classify_candidate"
