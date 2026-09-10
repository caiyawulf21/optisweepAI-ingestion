from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from brain.schemas.capability import Capability
from brain.schemas.claim import Claim
from brain.schemas.entity import Entity
from brain.schemas.evidence_unit import EvidenceUnit
from brain.schemas.relationship import Relationship

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


# --- Fixture round-trips: one per required record type (Part 1 §13) ---


def test_manual_evidence_unit_fixture_validates() -> None:
    unit = EvidenceUnit.model_validate(load_fixture("manual_evidence_unit.json"))
    assert unit.evidence_kind.value == "document_section"
    assert unit.source_type == "manual"


def test_incident_evidence_unit_fixture_validates() -> None:
    unit = EvidenceUnit.model_validate(load_fixture("incident_evidence_unit.json"))
    assert unit.evidence_kind.value == "incident_timeline_event"
    assert unit.locator.timeline_event_order == 7


def test_wcs_system_entity_fixture_validates() -> None:
    entity = Entity.model_validate(load_fixture("wcs_system_entity.json"))
    assert entity.entity_type.value == "system"
    assert "coordinates_agv_activity" in entity.payload.operational_roles


def test_tote_task_history_entity_fixture_validates() -> None:
    entity = Entity.model_validate(load_fixture("tote_task_history_entity.json"))
    assert entity.entity_type.value == "database_table"
    assert entity.payload.database_name == "OptiSweep"
    assert entity.payload.key_fields[0].name == "ToteId"


def test_verify_tote_state_capability_fixture_validates() -> None:
    capability = Capability.model_validate(load_fixture("verify_tote_state_capability.json"))
    assert capability.capability_kind.value == "diagnostic"
    assert "entity:system:wcs" in capability.target_entity_ids


def test_capability_role_paths_require_guidance_and_role_id() -> None:
    from brain.schemas.capability import RolePathGuidance

    path = RolePathGuidance(
        role_entity_id="entity:role:operator",
        guidance="Primary RMS overview on site; no SSMS",
    )
    assert path.role_entity_id.startswith("entity:role:")
    with pytest.raises(ValidationError):
        RolePathGuidance(role_entity_id="entity:role:operator", guidance="   ")
    with pytest.raises(ValidationError):
        RolePathGuidance(role_entity_id="operator", guidance="no SSMS")


def test_heartbeat_claim_fixture_validates() -> None:
    claim = Claim.model_validate(load_fixture("heartbeat_claim.json"))
    assert claim.polarity.value == "affirmed"
    assert claim.object.kind == "entity_ref"
    assert claim.object.entity_id == "entity:state:tipper_wcs_synchronization_risk"


def test_wcs_controls_agv_relationship_fixture_validates() -> None:
    relationship = Relationship.model_validate(load_fixture("wcs_controls_agv_relationship.json"))
    assert relationship.relationship_type.value == "controls"
    assert relationship.from_id == "entity:system:wcs"
    assert relationship.to_id == "entity:component:agv_fleet"


# --- Constraints: global by default (Part 1 §3.3, §13) ---


def test_record_with_no_constraints_is_globally_applicable() -> None:
    entity = Entity.model_validate(load_fixture("wcs_system_entity.json"))
    assert entity.constraints.sites == []
    assert entity.constraints.product_versions == []
    assert entity.constraints.environments == []


def test_constrained_record_retains_its_scope() -> None:
    data = load_fixture("wcs_system_entity.json")
    data["constraints"] = {
        "sites": ["ups_haslet"],
        "product_versions": ["v2"],
        "environments": ["production"],
    }
    entity = Entity.model_validate(data)
    assert entity.constraints.sites == ["ups_haslet"]
    assert entity.constraints.product_versions == ["v2"]
    assert entity.constraints.environments == ["production"]


# --- Polarity / conflicting claims without overwriting evidence (Part 1 §13) ---


def test_conflicting_claim_polarity_is_representable() -> None:
    data = load_fixture("heartbeat_claim.json")
    data["id"] = "claim:heartbeat_max:conflicting_variant"
    data["polarity"] = "conflicting"
    claim = Claim.model_validate(data)
    assert claim.polarity.value == "conflicting"


# --- Discriminated entity payload rejects mismatched fields (Part 1 §5, §13) ---


def test_invalid_entity_payload_fields_are_rejected_for_declared_entity_type() -> None:
    data = load_fixture("wcs_system_entity.json")
    data["payload"] = {"database_name": "OptiSweep", "key_fields": []}
    with pytest.raises(ValidationError):
        Entity.model_validate(data)


def test_entity_type_and_payload_shape_must_match() -> None:
    data = load_fixture("tote_task_history_entity.json")
    data["entity_type"] = "ui_screen"
    with pytest.raises(ValidationError):
        Entity.model_validate(data)


# --- Relationship endpoints must be well-formed typed IDs (Part 1 §8, §13) ---


def test_relationship_rejects_malformed_endpoint_id() -> None:
    data = load_fixture("wcs_controls_agv_relationship.json")
    data["to_id"] = "AGV Fleet"
    with pytest.raises(ValidationError):
        Relationship.model_validate(data)


def test_relationship_requires_source_refs() -> None:
    data = load_fixture("wcs_controls_agv_relationship.json")
    data["source_refs"] = []
    with pytest.raises(ValidationError):
        Relationship.model_validate(data)


def test_claim_requires_source_refs() -> None:
    data = load_fixture("heartbeat_claim.json")
    data["source_refs"] = []
    with pytest.raises(ValidationError):
        Claim.model_validate(data)


# --- Evidence text requirement for textual evidence kinds ---


def test_evidence_unit_requires_text_for_textual_kind() -> None:
    data = load_fixture("manual_evidence_unit.json")
    data["content"]["text"] = None
    with pytest.raises(ValidationError):
        EvidenceUnit.model_validate(data)


def test_evidence_unit_allows_missing_text_for_non_textual_kind() -> None:
    data = load_fixture("manual_evidence_unit.json")
    data["evidence_kind"] = "runtime_interaction_evidence"
    data["content"]["text"] = None
    data["content"]["structured_payload"] = {"outcome": "resolved"}
    unit = EvidenceUnit.model_validate(data)
    assert unit.content.text is None


# --- Extra fields are rejected (schema strictness) ---


def test_unknown_top_level_field_is_rejected() -> None:
    data = load_fixture("wcs_system_entity.json")
    data["unexpected_field"] = "nope"
    with pytest.raises(ValidationError):
        Entity.model_validate(data)
