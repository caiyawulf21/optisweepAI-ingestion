from __future__ import annotations

import pytest

from brain.schemas.capability import Capability, CapabilityKind
from brain.schemas.claim import Claim, LiteralValueObject, Polarity
from brain.schemas.entity import Entity, EntityType
from brain.schemas.playbook import Playbook, PlaybookNode, PlaybookNodeType
from brain.schemas.relationship import Relationship, RelationshipType
from brain.schemas.review import BrainReview, ReviewKind
from providers.azure_cosmos_config import CONTAINER_BY_RECORD_TYPE, partition_key_value


def test_entity_partition_key_uses_value_not_str_repr() -> None:
    entity = Entity(
        id="entity:system:x", entity_type=EntityType.SYSTEM, name="X", description="y",
        source_refs=["evidence:test:seed"],
    )
    assert partition_key_value(entity) == "system"  # not "EntityType.SYSTEM"


def test_capability_partition_key_uses_value() -> None:
    capability = Capability(
        id="capability:do_x", name="Do X", description="d", capability_kind=CapabilityKind.DIAGNOSTIC,
        source_refs=["evidence:test:seed"],
    )
    assert partition_key_value(capability) == "diagnostic"


def test_claim_partition_key_is_subject_entity_id() -> None:
    claim = Claim(
        id="claim:x:has_fact", subject_entity_id="entity:system:x", predicate="has_fact",
        object=LiteralValueObject(value="v"), polarity=Polarity.AFFIRMED,
        source_refs=["evidence:test:seed"],
    )
    assert partition_key_value(claim) == "entity:system:x"


def test_relationship_partition_key_is_from_id() -> None:
    rel = Relationship(
        id="relationship:a:controls:b", from_id="entity:system:a",
        relationship_type=RelationshipType.CONTROLS, to_id="entity:system:b",
        source_refs=["evidence:test:seed"],
    )
    assert partition_key_value(rel) == "entity:system:a"


def test_review_partition_key_is_status() -> None:
    review = BrainReview(
        id="review:gap:x", kind=ReviewKind.GAP, affected_record_ids=["entity:system:x"],
        proposed_change="x",
    )
    assert partition_key_value(review) == "open"


def _minimal_node() -> PlaybookNode:
    return PlaybookNode(
        node_id="n1",
        node_order=1,
        node_type=PlaybookNodeType.DIAGNOSTIC_DECISION,
        title="Check X",
        capability_id="capability:do_x",
        source_refs=["evidence:test:seed"],
    )


def test_playbook_partition_key_uses_first_symptom_id() -> None:
    playbook = Playbook(
        id="playbook:x",
        title="X",
        entry_symptom_entity_ids=["entity:symptom:a", "entity:symptom:b"],
        nodes=[_minimal_node()],
        source_refs=["evidence:test:seed"],
    )
    assert partition_key_value(playbook) == "entity:symptom:a"


def test_playbook_partition_key_raises_on_empty_symptom_list() -> None:
    playbook = Playbook(
        id="playbook:x",
        title="X",
        entry_symptom_entity_ids=[],
        nodes=[_minimal_node()],
        source_refs=["evidence:test:seed"],
    )
    with pytest.raises(ValueError, match="empty list"):
        partition_key_value(playbook)


def test_every_record_type_has_a_container_mapping() -> None:
    from brain.schemas.common import RecordType

    for record_type in RecordType:
        if record_type == RecordType.REVIEW:
            continue
        assert record_type in CONTAINER_BY_RECORD_TYPE, f"{record_type} missing from CONTAINER_BY_RECORD_TYPE"
