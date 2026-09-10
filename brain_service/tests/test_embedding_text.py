from __future__ import annotations

import pytest

from brain.schemas.capability import Capability, CapabilityKind
from brain.schemas.claim import Claim, EntityRefObject, LiteralValueObject, Polarity
from brain.schemas.entity import Entity, EntityType
from brain.schemas.evidence_unit import EvidenceContent, EvidenceKind, EvidenceUnit
from brain.schemas.playbook import Playbook, PlaybookNode, PlaybookNodeType
from brain.schemas.procedure import Procedure
from brain.schemas.relationship import Relationship, RelationshipType
from brain_service.embedding_text import embedding_text_for


def test_entity_text_includes_name_aliases_and_description() -> None:
    entity = Entity(
        id="entity:system:x", entity_type=EntityType.SYSTEM, name="WCS", aliases=["Warehouse Control"],
        description="Coordinates AGV activity.", source_refs=["evidence:test:seed"],
    )
    text = embedding_text_for(entity)
    assert "WCS" in text
    assert "Warehouse Control" in text
    assert "Coordinates AGV activity." in text


def test_claim_text_with_literal_object() -> None:
    claim = Claim(
        id="claim:x:has_fact", subject_entity_id="entity:system:x", predicate="has_fact",
        object=LiteralValueObject(value="something happened"), polarity=Polarity.AFFIRMED,
        note="a note", source_refs=["evidence:test:seed"],
    )
    text = embedding_text_for(claim)
    assert "entity:system:x" in text
    assert "has_fact" in text
    assert "something happened" in text
    assert "a note" in text


def test_claim_text_with_entity_ref_object() -> None:
    claim = Claim(
        id="claim:x:may_indicate", subject_entity_id="entity:metric:x", predicate="may_indicate",
        object=EntityRefObject(entity_id="entity:state:y"), polarity=Polarity.UNCERTAIN,
        source_refs=["evidence:test:seed"],
    )
    text = embedding_text_for(claim)
    assert "entity:state:y" in text


def test_evidence_unit_text_is_content_text() -> None:
    evidence = EvidenceUnit(
        id="evidence:test:1", evidence_kind=EvidenceKind.SME_NOTE, source_type="test", source_id="source:test",
        content=EvidenceContent(text="the bots stopped moving", is_verbatim=True, content_hash="sha256:x"),
    )
    assert embedding_text_for(evidence) == "the bots stopped moving"


def test_capability_text_includes_name_and_description() -> None:
    capability = Capability(
        id="capability:do_x", name="Do X", description="Does the X thing.",
        capability_kind=CapabilityKind.DIAGNOSTIC, source_refs=["evidence:test:seed"],
    )
    text = embedding_text_for(capability)
    assert "Do X" in text
    assert "Does the X thing." in text


def test_procedure_text_includes_title_summary_and_when_to_use() -> None:
    procedure = Procedure(
        id="procedure:capability:do_x:v1", capability_id="capability:do_x",
        procedure_type=CapabilityKind.DIAGNOSTIC, title="Check X", summary="A summary.",
        when_to_use=["Use when X is broken."], source_refs=["evidence:test:seed"],
    )
    text = embedding_text_for(procedure)
    assert "Check X" in text
    assert "A summary." in text
    assert "Use when X is broken." in text


def test_relationship_text_includes_endpoints_and_type() -> None:
    rel = Relationship(
        id="relationship:a:controls:b", from_id="entity:system:a",
        relationship_type=RelationshipType.CONTROLS, to_id="entity:system:b",
        note="controls it", source_refs=["evidence:test:seed"],
    )
    text = embedding_text_for(rel)
    assert "entity:system:a" in text
    assert "controls" in text
    assert "entity:system:b" in text


def test_playbook_text_includes_title_and_goal() -> None:
    playbook = Playbook(
        id="playbook:x", title="Bag-out stoppage", playbook_goal="Determine root cause.",
        entry_symptom_entity_ids=["entity:symptom:a"],
        nodes=[
            PlaybookNode(
                node_id="n1", node_order=1, node_type=PlaybookNodeType.DIAGNOSTIC_DECISION, title="Check",
                capability_id="capability:do_x", source_refs=["evidence:test:seed"],
            )
        ],
        source_refs=["evidence:test:seed"],
    )
    text = embedding_text_for(playbook)
    assert "Bag-out stoppage" in text
    assert "Determine root cause." in text
