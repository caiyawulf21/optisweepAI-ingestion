from __future__ import annotations

import json
from pathlib import Path

from brain.schemas.capability import Capability
from brain.schemas.claim import Claim
from brain.schemas.entity import Entity
from brain.schemas.evidence_unit import EvidenceUnit
from brain.schemas.relationship import Relationship
from brain.validators import validate_batch

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def test_manual_and_incident_evidence_share_the_same_schema() -> None:
    """A manual source and an incident source must emit the same EvidenceUnit shape (Part 1 §9)."""
    manual = EvidenceUnit.model_validate(load_fixture("manual_evidence_unit.json"))
    incident = EvidenceUnit.model_validate(load_fixture("incident_evidence_unit.json"))

    assert type(manual) is type(incident) is EvidenceUnit
    assert manual.source_type != incident.source_type


def test_incident_derived_claim_can_reference_operational_entity_ids() -> None:
    """An incident-derived claim must be able to point at entities established by operational
    sources, proving both lanes converge on one shared entity namespace (Part 1 §1.1, §9)."""
    wcs_entity = Entity.model_validate(load_fixture("wcs_system_entity.json"))

    incident_claim = Claim.model_validate(
        {
            "id": "claim:wcs:diagnostically_useful_for_tote_mismatch",
            "type": "claim",
            "subject_entity_id": wcs_entity.id,
            "predicate": "supports_diagnosis_of",
            "object": {"kind": "literal", "value": "tote_state_mismatch"},
            "polarity": "affirmed",
            "note": "Backend verification via WCS was diagnostically useful for this symptom.",
            "source_refs": ["evidence:case_218550:event_007"],
        }
    )

    assert incident_claim.subject_entity_id == wcs_entity.id


def test_training_video_and_incident_can_both_reference_same_table_entity() -> None:
    """Mirrors Part 1 §9's worked example: a training video establishes a database_table entity
    and capability; an incident later adds a relationship and claim about the same table without
    requiring the operational contribution to exist first or vice versa."""
    table_entity = Entity.model_validate(load_fixture("tote_task_history_entity.json"))
    capability = Capability.model_validate(load_fixture("verify_tote_state_capability.json"))

    incident_relationship = Relationship.model_validate(
        {
            "id": "relationship:tote_task_history:supports:verify_tote_state",
            "type": "relationship",
            "from_id": table_entity.id,
            "relationship_type": "supports",
            "to_id": capability.id,
            "note": "Incident case_218550 confirmed this table supports the verify_tote_state capability.",
            "source_refs": ["evidence:case_218550:event_007"],
        }
    )

    incident_claim = Claim.model_validate(
        {
            "id": "claim:verify_tote_state:useful_for_tote_state_mismatch",
            "type": "claim",
            "subject_entity_id": table_entity.id,
            "predicate": "was_diagnostically_useful_for",
            "object": {"kind": "literal", "value": "tote_state_mismatch"},
            "polarity": "affirmed",
            "source_refs": ["evidence:case_218550:event_007"],
        }
    )

    result = validate_batch(
        entities=[table_entity],
        capabilities=[capability],
        relationships=[incident_relationship],
        claims=[incident_claim],
    )
    assert result.valid, result.errors


def test_evidence_units_are_never_overwritten_when_sources_conflict() -> None:
    """A source-backed conflict is represented as a new claim with polarity=conflicting,
    while both original EvidenceUnits remain intact and independently addressable
    (Part 1 §1.2, §13)."""
    manual = EvidenceUnit.model_validate(load_fixture("manual_evidence_unit.json"))
    incident = EvidenceUnit.model_validate(load_fixture("incident_evidence_unit.json"))

    conflicting_claim = Claim.model_validate(
        {
            "id": "claim:heartbeat_max:conflicting_incident_observation",
            "type": "claim",
            "subject_entity_id": "entity:metric:tipper_heartbeat_max",
            "predicate": "may_indicate",
            "object": {
                "kind": "entity_ref",
                "entity_id": "entity:state:tipper_wcs_synchronization_risk",
            },
            "polarity": "conflicting",
            "source_refs": [manual.id, incident.id],
        }
    )

    assert manual.content.text is not None
    assert incident.content.text is not None
    assert conflicting_claim.source_refs == [manual.id, incident.id]


def test_cross_source_batch_with_only_operational_or_only_incident_records_is_valid() -> None:
    """Neither lane requires the other to be present for its own contribution to validate
    (Part 1 §9: "Both contributions strengthen one Brain. Neither requires the other to be
    valid.")."""
    manual_only = validate_batch(
        evidence_units=[EvidenceUnit.model_validate(load_fixture("manual_evidence_unit.json"))],
        entities=[Entity.model_validate(load_fixture("wcs_system_entity.json"))],
    )
    incident_only = validate_batch(
        evidence_units=[EvidenceUnit.model_validate(load_fixture("incident_evidence_unit.json"))],
    )

    assert manual_only.valid, manual_only.errors
    assert incident_only.valid, incident_only.errors
