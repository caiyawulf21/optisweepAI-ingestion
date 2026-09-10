from __future__ import annotations

import pytest

from brain.schemas.common import ValidationStatus
from brain.schemas.entity import Entity, EntityType
from brain.schemas.review import BrainReview, ReviewKind, ReviewResolution
from brain_service.audit_execution import (
    NoWinnerRecordError,
    RetypeTargetError,
    UnresolvableRecordError,
    apply_audit_resolution,
)
from brain_service.tests.conftest import make_entity


def _review(*, affected_record_ids: list[str], resolution: ReviewResolution) -> BrainReview:
    return BrainReview(
        id="review:audit_finding:test",
        kind=ReviewKind.AUDIT_FINDING,
        affected_record_ids=affected_record_ids,
        check_name="normalized_name_collision",
        proposed_change="test finding",
        status="resolved",
        resolution=resolution,
        resolved_by="agent",
    )


def test_apply_merge_merges_loser_fields_into_winner(storage) -> None:
    winner = make_entity("entity:system:agv_fleet_a", description="Winner description.")
    loser = Entity(
        id="entity:system:agv_fleet_b",
        entity_type=winner.entity_type,
        name="AGV Fleet B",
        description="",
        aliases=["AGV Fleet"],
        source_refs=["evidence:test:loser_seed"],
    )
    storage.save_brain_records([winner, loser], scope="operational_sources/test")

    review = _review(affected_record_ids=[winner.id, loser.id], resolution=ReviewResolution.MERGE)
    result = apply_audit_resolution(storage, review, winner_record_id=winner.id)

    assert result.applied is True
    assert result.resolution == ReviewResolution.MERGE
    assert winner.id in result.mutated_record_ids
    assert loser.id in result.mutated_record_ids

    loaded = {r.id: r for r in storage.load_brain_records(scope="operational_sources/test")}
    merged_winner = loaded[winner.id]
    assert "AGV Fleet" in merged_winner.aliases
    assert "evidence:test:loser_seed" in merged_winner.source_refs
    assert merged_winner.description == "Winner description."  # never overwritten, only filled if empty

    deprecated_loser = loaded[loser.id]
    assert deprecated_loser.validation_status == ValidationStatus.DEPRECATED


def test_apply_merge_writes_winner_to_its_own_scope_not_a_default(storage) -> None:
    winner = make_entity("entity:system:agv_fleet_a")
    loser = make_entity("entity:system:agv_fleet_b")
    storage.save_brain_records([winner], scope="ontology_catalogs")
    storage.save_brain_records([loser], scope="incidents/case_test")

    review = _review(affected_record_ids=[winner.id, loser.id], resolution=ReviewResolution.MERGE)
    apply_audit_resolution(storage, review, winner_record_id=winner.id)

    assert any(r.id == winner.id for r in storage.load_brain_records(scope="ontology_catalogs"))


def test_apply_merge_is_idempotent_when_loser_already_deprecated(storage) -> None:
    winner = make_entity("entity:system:agv_fleet_a")
    loser = make_entity("entity:system:agv_fleet_b").model_copy(
        update={"validation_status": ValidationStatus.DEPRECATED}
    )
    storage.save_brain_records([winner, loser], scope="operational_sources/test")

    review = _review(affected_record_ids=[winner.id, loser.id], resolution=ReviewResolution.MERGE)
    result = apply_audit_resolution(storage, review, winner_record_id=winner.id)

    assert loser.id not in result.mutated_record_ids  # already deprecated -- not re-written


def test_apply_merge_raises_when_no_winner_given(storage) -> None:
    winner = make_entity("entity:system:agv_fleet_a")
    loser = make_entity("entity:system:agv_fleet_b")
    storage.save_brain_records([winner, loser], scope="operational_sources/test")

    review = _review(affected_record_ids=[winner.id, loser.id], resolution=ReviewResolution.MERGE)
    with pytest.raises(NoWinnerRecordError):
        apply_audit_resolution(storage, review, winner_record_id=None)


def test_apply_merge_raises_when_winner_not_in_affected_ids(storage) -> None:
    winner = make_entity("entity:system:agv_fleet_a")
    loser = make_entity("entity:system:agv_fleet_b")
    storage.save_brain_records([winner, loser], scope="operational_sources/test")

    review = _review(affected_record_ids=[winner.id, loser.id], resolution=ReviewResolution.MERGE)
    with pytest.raises(ValueError, match="not one of this review's own"):
        apply_audit_resolution(storage, review, winner_record_id="entity:system:not_in_review")


def test_apply_merge_raises_when_a_record_no_longer_exists(storage) -> None:
    winner = make_entity("entity:system:agv_fleet_a")
    storage.save_brain_records([winner], scope="operational_sources/test")

    review = _review(
        affected_record_ids=[winner.id, "entity:system:already_deleted"],
        resolution=ReviewResolution.MERGE,
    )
    with pytest.raises(UnresolvableRecordError):
        apply_audit_resolution(storage, review, winner_record_id=winner.id)


@pytest.mark.parametrize(
    "resolution",
    [ReviewResolution.RECLASSIFY, ReviewResolution.NOT_A_DUPLICATE, ReviewResolution.NEEDS_HUMAN],
)
def test_non_executable_resolutions_are_accepted_but_not_applied(storage, resolution) -> None:
    entity = make_entity("entity:system:agv_fleet_a")
    storage.save_brain_records([entity], scope="operational_sources/test")

    review = _review(affected_record_ids=[entity.id], resolution=resolution)
    result = apply_audit_resolution(storage, review)

    assert result.applied is False
    assert result.mutated_record_ids == []
    assert resolution.value in result.detail.lower()


def test_reclassify_detail_explains_why_it_cannot_be_mechanically_applied(storage) -> None:
    # RECLASSIFY gets its OWN specific reason, not the generic
    # "not applied yet" message RETYPE used to share with it before
    # RETYPE became real (2026-09-10).
    entity = make_entity("entity:system:agv_fleet_a")
    storage.save_brain_records([entity], scope="operational_sources/test")

    review = _review(affected_record_ids=[entity.id], resolution=ReviewResolution.RECLASSIFY)
    result = apply_audit_resolution(storage, review)

    assert "no mechanical procedure" in result.detail


def test_retype_raises_when_no_new_entity_type_given(storage) -> None:
    entity = make_entity("entity:system:agv_fleet_a")
    storage.save_brain_records([entity], scope="operational_sources/test")

    review = _review(affected_record_ids=[entity.id], resolution=ReviewResolution.RETYPE)
    with pytest.raises(RetypeTargetError, match="new_entity_type"):
        apply_audit_resolution(storage, review)


def test_retype_renames_entity_id_and_cascades_references(storage) -> None:
    from brain.schemas.relationship import Relationship, RelationshipType

    old_entity = Entity(
        id="entity:state:bag_out_stuck", entity_type=EntityType.STATE, name="Bag Out Stuck",
        description="test", source_refs=["evidence:test:seed"],
    )
    other_entity = make_entity("entity:system:sorter")
    referencing_relationship = Relationship(
        id="relationship:entity_state_bag_out_stuck:contributes_to:entity_system_sorter",
        from_id=old_entity.id, relationship_type=RelationshipType.CONTRIBUTES_TO, to_id=other_entity.id,
        source_refs=["evidence:test:seed"],
    )
    storage.save_brain_records(
        [old_entity, other_entity, referencing_relationship], scope="operational_sources/test"
    )

    review = _review(affected_record_ids=[old_entity.id], resolution=ReviewResolution.RETYPE)
    result = apply_audit_resolution(storage, review, new_entity_type="symptom")

    assert result.applied is True
    new_id = "entity:symptom:bag_out_stuck"
    assert new_id in result.mutated_record_ids
    assert old_entity.id in result.mutated_record_ids
    assert referencing_relationship.id in result.mutated_record_ids

    loaded = {r.id: r for r in storage.load_brain_context()}
    assert loaded[new_id].entity_type == EntityType.SYMPTOM
    assert loaded[old_entity.id].validation_status == ValidationStatus.DEPRECATED
    assert loaded[referencing_relationship.id].from_id == new_id  # reference rewritten


def test_retype_refuses_when_payload_data_would_be_lost(storage) -> None:
    from brain.schemas.entity import SystemPayload

    entity_with_real_payload = Entity(
        id="entity:system:wcs", entity_type=EntityType.SYSTEM, name="WCS", description="test",
        source_refs=["evidence:test:seed"],
        payload=SystemPayload(operational_roles=["primary_control"]),
    )
    storage.save_brain_records([entity_with_real_payload], scope="operational_sources/test")

    review = _review(affected_record_ids=[entity_with_real_payload.id], resolution=ReviewResolution.RETYPE)
    with pytest.raises(RetypeTargetError, match="payload"):
        apply_audit_resolution(storage, review, new_entity_type="state")


def test_retype_refuses_unknown_entity_type(storage) -> None:
    entity = make_entity("entity:system:agv_fleet_a")
    storage.save_brain_records([entity], scope="operational_sources/test")

    review = _review(affected_record_ids=[entity.id], resolution=ReviewResolution.RETYPE)
    with pytest.raises(RetypeTargetError, match="not a recognized EntityType"):
        apply_audit_resolution(storage, review, new_entity_type="not_a_real_type")


def test_retype_refuses_non_entity_target(storage) -> None:
    from brain.schemas.capability import Capability, CapabilityKind

    capability = Capability(
        id="capability:x", name="x", capability_kind=CapabilityKind.DIAGNOSTIC,
        source_refs=["evidence:test:seed"],
    )
    storage.save_brain_records([capability], scope="ontology_catalogs")

    review = _review(affected_record_ids=[capability.id], resolution=ReviewResolution.RETYPE)
    with pytest.raises(RetypeTargetError, match="only applies to Entity"):
        apply_audit_resolution(storage, review, new_entity_type="symptom")


def test_retype_refuses_when_target_id_already_exists(storage) -> None:
    old_entity = Entity(
        id="entity:state:x", entity_type=EntityType.STATE, name="x", description="test",
        source_refs=["evidence:test:seed"],
    )
    colliding_entity = Entity(
        id="entity:symptom:x", entity_type=EntityType.SYMPTOM, name="x", description="test",
        source_refs=["evidence:test:seed"],
    )
    storage.save_brain_records([old_entity, colliding_entity], scope="operational_sources/test")

    review = _review(affected_record_ids=[old_entity.id], resolution=ReviewResolution.RETYPE)
    with pytest.raises(RetypeTargetError, match="already exists"):
        apply_audit_resolution(storage, review, new_entity_type="symptom")


def test_retype_raises_when_multiple_affected_ids(storage) -> None:
    entity_a = make_entity("entity:system:a")
    entity_b = make_entity("entity:system:b")
    storage.save_brain_records([entity_a, entity_b], scope="operational_sources/test")

    review = _review(affected_record_ids=[entity_a.id, entity_b.id], resolution=ReviewResolution.RETYPE)
    with pytest.raises(RetypeTargetError, match="exactly one"):
        apply_audit_resolution(storage, review, new_entity_type="symptom")
