from __future__ import annotations

import json

import pytest

from brain.schemas.common import ValidationStatus
from brain.schemas.procedure import Procedure
from brain_service.procedure_drafting import (
    CapabilityNotFoundError,
    DanglingProcedureReferenceError,
    build_procedure_record,
    draft_procedure,
    write_drafted_procedure,
)
from brain_service.tests.conftest import ScriptedLLM, make_capability, make_entity
from brain_service.types import DraftedProcedure, DraftedProcedureStep


def _drafted(**overrides) -> DraftedProcedure:
    defaults = dict(
        title="Confirm AGV fleet health",
        summary="Checks the AGV fleet's reported state before escalating.",
        when_to_use=["AGV reported as stalled"],
        not_for=["Known network outage in progress"],
        allowed_role_entity_ids=["entity:role:l1_support"],
        steps=[
            DraftedProcedureStep(
                step_number=1,
                title="Check fleet status screen",
                instruction="Open the fleet status screen and note the AGV's reported state.",
                responsible_role_entity_id="entity:role:l1_support",
                source_refs=["evidence:test:seed"],
            )
        ],
        rationale="Derived from the capability's observables and one retrieved evidence excerpt.",
        gaps=[],
    )
    defaults.update(overrides)
    return DraftedProcedure(**defaults)


def test_draft_procedure_returns_llm_response(storage) -> None:
    capability = make_capability(
        "capability:confirm_agv_fleet_health",
        target_entity_ids=["entity:system:agv_fleet"],
        required_role_ids=["entity:role:l1_support"],
    )
    storage.save_brain_records(
        [capability, make_entity("entity:system:agv_fleet"), make_entity("entity:role:l1_support")],
        scope="ontology_catalogs",
    )
    expected = _drafted()
    llm = ScriptedLLM({DraftedProcedure: [expected]})

    result = draft_procedure(
        llm,
        storage,
        capability_id="capability:confirm_agv_fleet_health",
        distinguishing_token="case_999",
    )

    assert result == expected


def test_draft_procedure_raises_when_capability_missing(storage) -> None:
    llm = ScriptedLLM({DraftedProcedure: [_drafted()]})

    with pytest.raises(CapabilityNotFoundError):
        draft_procedure(
            llm,
            storage,
            capability_id="capability:does_not_exist",
            distinguishing_token="case_999",
        )


def test_draft_procedure_passes_capability_fields_to_llm(storage) -> None:
    capability = make_capability(
        "capability:confirm_agv_fleet_health",
        target_entity_ids=["entity:system:agv_fleet"],
    )
    storage.save_brain_records([capability, make_entity("entity:system:agv_fleet")], scope="ontology_catalogs")
    captured: dict = {}

    class CapturingLLM:
        def generate_json(self, *, system_prompt, user_content, schema, label, max_attempts=2):
            captured["user_content"] = user_content
            captured["label"] = label
            return _drafted()

        def generate_text(self, **kwargs):
            raise NotImplementedError

    draft_procedure(
        CapturingLLM(),
        storage,
        capability_id="capability:confirm_agv_fleet_health",
        distinguishing_token="case_999",
    )

    payload = json.loads(captured["user_content"])
    assert payload["capability"]["id"] == "capability:confirm_agv_fleet_health"
    assert "entity:system:agv_fleet" in payload["retrieved_context"]["entities"]
    assert captured["label"] == "draft_procedure"


def test_build_procedure_record_constructs_valid_procedure(storage) -> None:
    capability = make_capability("capability:confirm_agv_fleet_health")
    storage.save_brain_records(
        [capability, make_entity("entity:role:l1_support")], scope="ontology_catalogs"
    )

    record = build_procedure_record(
        _drafted(),
        storage,
        capability_id="capability:confirm_agv_fleet_health",
        distinguishing_token="case_999",
        source_evidence_ids=["evidence:test:seed"],
    )

    assert isinstance(record, Procedure)
    assert record.capability_id == "capability:confirm_agv_fleet_health"
    assert record.id == "procedure:confirm_agv_fleet_health:case_999"
    assert record.validation_status == ValidationStatus.OPERATIONAL_UNREVIEWED
    assert record.steps[0].step_number == 1


def test_build_procedure_record_raises_on_dangling_role_reference(storage) -> None:
    capability = make_capability("capability:confirm_agv_fleet_health")
    storage.save_brain_records([capability], scope="ontology_catalogs")

    with pytest.raises(DanglingProcedureReferenceError) as exc_info:
        build_procedure_record(
            _drafted(),
            storage,
            capability_id="capability:confirm_agv_fleet_health",
            distinguishing_token="case_999",
            source_evidence_ids=["evidence:test:seed"],
        )

    assert "entity:role:l1_support" in exc_info.value.dangling_ids


def test_build_procedure_record_raises_when_capability_missing(storage) -> None:
    with pytest.raises(CapabilityNotFoundError):
        build_procedure_record(
            _drafted(allowed_role_entity_ids=[], steps=[]),
            storage,
            capability_id="capability:does_not_exist",
            distinguishing_token="case_999",
            source_evidence_ids=["evidence:test:seed"],
        )


def test_write_drafted_procedure_writes_record_and_review(storage) -> None:
    capability = make_capability("capability:confirm_agv_fleet_health")
    storage.save_brain_records(
        [capability, make_entity("entity:role:l1_support")], scope="ontology_catalogs"
    )
    record = build_procedure_record(
        _drafted(),
        storage,
        capability_id="capability:confirm_agv_fleet_health",
        distinguishing_token="case_999",
        source_evidence_ids=["evidence:test:seed"],
    )

    write_drafted_procedure(storage, record, scope="incidents/case_999")

    loaded = storage.load_brain_records(scope="incidents/case_999")
    loaded_ids = {r.id for r in loaded}
    assert record.id in loaded_ids
    assert any(r.type.value == "review" for r in loaded)
