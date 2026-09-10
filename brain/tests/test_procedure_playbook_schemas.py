from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from brain.schemas.capability import Capability
from brain.schemas.entity import Entity
from brain.schemas.playbook import Playbook
from brain.schemas.procedure import Procedure
from brain.validators import validate_batch

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


# --- Fixture round-trips ---


def test_verify_tote_state_procedure_fixture_validates() -> None:
    proc = Procedure.model_validate(load_fixture("verify_tote_state_procedure.json"))
    assert proc.capability_id == "capability:verify_tote_state"
    assert proc.procedure_type.value == "diagnostic"
    assert len(proc.steps) == 1
    assert proc.steps[0].step_number == 1


def test_tote_state_playbook_fixture_validates() -> None:
    pb = Playbook.model_validate(load_fixture("tote_state_playbook.json"))
    assert pb.entry_node_id == "node_1"
    assert len(pb.nodes) == 2
    assert pb.nodes[0].branches[1].next_node_id == "node_2"


# --- Procedure: steps must be sequential (no gaps, no branching at this layer) ---


def test_procedure_rejects_non_sequential_step_numbers() -> None:
    data = load_fixture("verify_tote_state_procedure.json")
    data["steps"][0]["step_number"] = 2
    with pytest.raises(ValidationError):
        Procedure.model_validate(data)


def test_procedure_requires_capability_id() -> None:
    data = load_fixture("verify_tote_state_procedure.json")
    data["capability_id"] = "Verify Tote State"
    with pytest.raises(ValidationError):
        Procedure.model_validate(data)


def test_procedure_requires_source_refs() -> None:
    data = load_fixture("verify_tote_state_procedure.json")
    data["source_refs"] = []
    with pytest.raises(ValidationError):
        Procedure.model_validate(data)


def test_procedure_step_requires_source_refs() -> None:
    data = load_fixture("verify_tote_state_procedure.json")
    data["steps"][0]["source_refs"] = []
    with pytest.raises(ValidationError):
        Procedure.model_validate(data)


# --- Playbook: node/branch graph integrity ---


def test_playbook_rejects_branch_to_unknown_node_id() -> None:
    data = load_fixture("tote_state_playbook.json")
    data["nodes"][0]["branches"][1]["next_node_id"] = "node_99"
    with pytest.raises(ValidationError):
        Playbook.model_validate(data)


def test_playbook_rejects_duplicate_node_ids() -> None:
    data = load_fixture("tote_state_playbook.json")
    data["nodes"][1]["node_id"] = "node_1"
    with pytest.raises(ValidationError):
        Playbook.model_validate(data)


def test_playbook_rejects_entry_node_id_not_in_nodes() -> None:
    data = load_fixture("tote_state_playbook.json")
    data["entry_node_id"] = "node_99"
    with pytest.raises(ValidationError):
        Playbook.model_validate(data)


def test_playbook_procedure_reference_node_requires_procedure_id() -> None:
    data = load_fixture("tote_state_playbook.json")
    data["nodes"][0]["node_type"] = "procedure_reference"
    data["nodes"][0]["procedure_id"] = None
    with pytest.raises(ValidationError):
        Playbook.model_validate(data)


def test_playbook_branch_requires_source_refs() -> None:
    data = load_fixture("tote_state_playbook.json")
    data["nodes"][0]["branches"][0]["source_refs"] = []
    with pytest.raises(ValidationError):
        Playbook.model_validate(data)


def test_playbook_node_requires_source_refs() -> None:
    data = load_fixture("tote_state_playbook.json")
    data["nodes"][1]["source_refs"] = []
    with pytest.raises(ValidationError):
        Playbook.model_validate(data)


def test_playbook_requires_source_refs() -> None:
    data = load_fixture("tote_state_playbook.json")
    data["source_refs"] = []
    with pytest.raises(ValidationError):
        Playbook.model_validate(data)


# --- validate_batch: payload-embedded id references must resolve ---


def _symptom_entity() -> Entity:
    return Entity.model_validate(
        {
            "id": "entity:symptom:tote_state_inconsistent",
            "type": "entity",
            "schema_version": "1.0",
            "entity_type": "symptom",
            "name": "Tote state inconsistent between screen and backend",
            "description": "",
            "aliases": [],
            "payload": {},
            "source_refs": ["evidence:training_day2:segment_042"],
            "constraints": {},
        }
    )


def _l2_role_entity() -> Entity:
    return Entity.model_validate(
        {
            "id": "entity:role:l2",
            "type": "entity",
            "schema_version": "1.0",
            "entity_type": "role",
            "name": "L2 support",
            "description": "",
            "aliases": [],
            "payload": {},
            "source_refs": ["evidence:training_day2:segment_042"],
            "constraints": {},
        }
    )


def _wcs_system_entity() -> Entity:
    return Entity.model_validate(load_fixture("wcs_system_entity.json"))


def test_validate_batch_passes_when_procedure_playbook_references_resolve() -> None:
    capability = Capability.model_validate(load_fixture("verify_tote_state_capability.json"))
    procedure = Procedure.model_validate(load_fixture("verify_tote_state_procedure.json"))
    playbook = Playbook.model_validate(load_fixture("tote_state_playbook.json"))
    entities = [_symptom_entity(), _l2_role_entity(), _wcs_system_entity()]

    result = validate_batch(
        entities=entities,
        capabilities=[capability],
        procedures=[procedure],
        playbooks=[playbook],
    )
    assert result.valid, result.errors


def test_validate_batch_flags_procedure_with_unknown_capability_id() -> None:
    procedure = Procedure.model_validate(load_fixture("verify_tote_state_procedure.json"))
    # capability deliberately omitted from the batch
    result = validate_batch(procedures=[procedure])
    assert not result.valid
    assert any("capability_id" in e for e in result.errors)


def test_validate_batch_flags_playbook_node_with_unknown_procedure_id() -> None:
    capability = Capability.model_validate(load_fixture("verify_tote_state_capability.json"))
    playbook = Playbook.model_validate(load_fixture("tote_state_playbook.json"))
    entities = [_symptom_entity(), _l2_role_entity(), _wcs_system_entity()]

    # procedure deliberately omitted from the batch
    result = validate_batch(entities=entities, capabilities=[capability], playbooks=[playbook])
    assert not result.valid
    assert any("procedure_id" in e for e in result.errors)


def test_validate_batch_flags_playbook_with_unknown_entry_symptom_entity() -> None:
    capability = Capability.model_validate(load_fixture("verify_tote_state_capability.json"))
    procedure = Procedure.model_validate(load_fixture("verify_tote_state_procedure.json"))
    playbook = Playbook.model_validate(load_fixture("tote_state_playbook.json"))
    # symptom entity deliberately omitted from the batch
    entities = [_l2_role_entity(), _wcs_system_entity()]

    result = validate_batch(
        entities=entities,
        capabilities=[capability],
        procedures=[procedure],
        playbooks=[playbook],
    )
    assert not result.valid
    assert any("entity:symptom:tote_state_inconsistent" in e for e in result.errors)
