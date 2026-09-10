from __future__ import annotations

import json

import pytest

from brain.schemas.common import ValidationStatus
from brain.schemas.playbook import Playbook
from brain.schemas.relationship import RelationshipType
from brain_service.playbook_drafting import (
    DanglingPlaybookReferenceError,
    SymptomNotFoundError,
    build_playbook_record,
    draft_playbook,
    write_drafted_playbook,
)
from brain_service.tests.conftest import (
    ScriptedLLM,
    make_capability,
    make_entity,
    make_procedure,
    make_relationship,
)
from brain_service.types import DraftedPlaybook, DraftedPlaybookBranch, DraftedPlaybookNode


def _seed_symptom_to_capability_graph(storage) -> None:
    storage.save_brain_records(
        [
            make_entity("entity:symptom:system_fault", description="AGV reports a system fault."),
            make_capability("capability:confirm_agv_active_error_state"),
            make_relationship(
                "entity:symptom:system_fault",
                RelationshipType.MAY_INDICATE,
                "capability:confirm_agv_active_error_state",
            ),
            make_procedure(
                "procedure:confirm_agv_active_error_state:seed_1",
                capability_id="capability:confirm_agv_active_error_state",
            ),
        ],
        scope="ontology_catalogs",
    )


def _drafted(**overrides) -> DraftedPlaybook:
    defaults = dict(
        title="Diagnose AGV system fault",
        playbook_goal="Route from a reported system fault to the right verification procedure.",
        entry_symptom_entity_ids=["entity:symptom:system_fault"],
        nodes=[
            DraftedPlaybookNode(
                node_id="check_active_error",
                node_order=1,
                node_type="diagnostic_decision",
                title="Check AGV active error state",
                capability_id="capability:confirm_agv_active_error_state",
                symptom_entity_id="entity:symptom:system_fault",
                branches=[
                    DraftedPlaybookBranch(
                        outcome="unhealthy",
                        condition="Active error present",
                        next_node_id="run_procedure",
                        source_refs=["evidence:test:seed"],
                    )
                ],
                source_refs=["evidence:test:seed"],
            ),
            DraftedPlaybookNode(
                node_id="run_procedure",
                node_order=2,
                node_type="procedure_reference",
                title="Run active error verification",
                procedure_id="procedure:confirm_agv_active_error_state:seed_1",
                source_refs=["evidence:test:seed"],
            ),
        ],
        entry_node_id="check_active_error",
        rationale="Derived from one MAY_INDICATE relationship and one existing procedure.",
        gaps=[],
    )
    defaults.update(overrides)
    return DraftedPlaybook(**defaults)


def test_draft_playbook_returns_llm_response(storage) -> None:
    _seed_symptom_to_capability_graph(storage)
    expected = _drafted()
    llm = ScriptedLLM({DraftedPlaybook: [expected]})

    result = draft_playbook(
        llm,
        storage,
        entry_symptom_entity_ids=["entity:symptom:system_fault"],
        distinguishing_token="test_cluster_1",
    )

    assert result == expected


def test_draft_playbook_raises_when_symptom_missing(storage) -> None:
    llm = ScriptedLLM({DraftedPlaybook: [_drafted()]})

    with pytest.raises(SymptomNotFoundError):
        draft_playbook(
            llm,
            storage,
            entry_symptom_entity_ids=["entity:symptom:does_not_exist"],
            distinguishing_token="test_cluster_1",
        )


def test_draft_playbook_passes_reachable_capabilities_and_procedures_to_llm(storage) -> None:
    _seed_symptom_to_capability_graph(storage)
    captured: dict = {}

    class CapturingLLM:
        def generate_json(self, *, system_prompt, user_content, schema, label, max_attempts=2):
            captured["user_content"] = user_content
            captured["label"] = label
            return _drafted()

        def generate_text(self, **kwargs):
            raise NotImplementedError

    draft_playbook(
        CapturingLLM(),
        storage,
        entry_symptom_entity_ids=["entity:symptom:system_fault"],
        distinguishing_token="test_cluster_1",
    )

    payload = json.loads(captured["user_content"])
    assert payload["reachable_capabilities"][0]["id"] == "capability:confirm_agv_active_error_state"
    assert payload["existing_procedures_for_reachable_capabilities"][0]["procedure_id"] == (
        "procedure:confirm_agv_active_error_state:seed_1"
    )
    assert payload["symptom_relationships"][0]["relationship_type"] == "may_indicate"
    assert captured["label"] == "draft_playbook"


def test_build_playbook_record_constructs_valid_playbook(storage) -> None:
    _seed_symptom_to_capability_graph(storage)

    record = build_playbook_record(
        _drafted(),
        storage,
        distinguishing_token="test_cluster_1",
        source_evidence_ids=["evidence:test:seed"],
    )

    assert isinstance(record, Playbook)
    assert record.id == "playbook:test_cluster_1"
    assert record.entry_node_id == "check_active_error"
    assert record.validation_status == ValidationStatus.OPERATIONAL_UNREVIEWED
    assert len(record.nodes) == 2


def test_build_playbook_record_raises_on_dangling_procedure_reference(storage) -> None:
    _seed_symptom_to_capability_graph(storage)
    drafted = _drafted(
        nodes=[
            DraftedPlaybookNode(
                node_id="run_procedure",
                node_order=1,
                node_type="procedure_reference",
                title="Run a procedure that does not exist",
                procedure_id="procedure:does_not_exist:v1",
                source_refs=["evidence:test:seed"],
            )
        ],
        entry_node_id="run_procedure",
    )

    with pytest.raises(DanglingPlaybookReferenceError) as exc_info:
        build_playbook_record(
            drafted,
            storage,
            distinguishing_token="test_cluster_1",
            source_evidence_ids=["evidence:test:seed"],
        )

    assert "procedure:does_not_exist:v1" in exc_info.value.dangling_ids


def test_build_playbook_record_raises_on_dangling_symptom_entity(storage) -> None:
    _seed_symptom_to_capability_graph(storage)
    drafted = _drafted(entry_symptom_entity_ids=["entity:symptom:does_not_exist"])

    with pytest.raises(DanglingPlaybookReferenceError) as exc_info:
        build_playbook_record(
            drafted,
            storage,
            distinguishing_token="test_cluster_1",
            source_evidence_ids=["evidence:test:seed"],
        )

    assert "entity:symptom:does_not_exist" in exc_info.value.dangling_ids


def test_write_drafted_playbook_writes_record_and_review(storage) -> None:
    _seed_symptom_to_capability_graph(storage)
    record = build_playbook_record(
        _drafted(),
        storage,
        distinguishing_token="test_cluster_1",
        source_evidence_ids=["evidence:test:seed"],
    )

    write_drafted_playbook(storage, record, scope="incidents/case_test")

    loaded = storage.load_brain_records(scope="incidents/case_test")
    loaded_ids = {r.id for r in loaded}
    assert record.id in loaded_ids
    assert any(r.type.value == "review" for r in loaded)
