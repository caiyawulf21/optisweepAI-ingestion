from __future__ import annotations

from brain.schemas.common import ValidationStatus
from brain.schemas.context_packet import ContextPacket
from brain_service.hydration import MAX_HYDRATED_EXCERPTS, hydrate_context_packet
from brain_service.tests.conftest import make_entity


def test_hydrate_returns_empty_when_packet_has_no_ids(storage) -> None:
    packet = ContextPacket(task={"kind": "test"})
    result = hydrate_context_packet(packet, storage=storage)
    assert result.excerpts == []
    assert result.truncated_excerpt_count == 0


def test_hydrate_labels_approved_status_as_approved(storage) -> None:
    entity = make_entity("entity:system:agv_fleet").model_copy(
        update={"validation_status": ValidationStatus.SME_APPROVED}
    )
    storage.save_brain_records([entity], scope="ontology_catalogs")
    packet = ContextPacket(task={"kind": "test"}, approved_knowledge=[entity.id])

    result = hydrate_context_packet(packet, storage=storage)

    assert len(result.excerpts) == 1
    assert result.excerpts[0].label == "approved"
    assert result.excerpts[0].id == entity.id


def test_hydrate_labels_unreviewed_status_as_working(storage) -> None:
    entity = make_entity("entity:system:agv_fleet").model_copy(
        update={"validation_status": ValidationStatus.OPERATIONAL_UNREVIEWED}
    )
    storage.save_brain_records([entity], scope="ontology_catalogs")
    packet = ContextPacket(task={"kind": "test"}, entities=[entity.id])

    result = hydrate_context_packet(packet, storage=storage)

    assert result.excerpts[0].label == "working"


def test_hydrate_labels_conflicting_status_as_conflict(storage) -> None:
    entity = make_entity("entity:system:agv_fleet").model_copy(
        update={"validation_status": ValidationStatus.CONFLICTING}
    )
    storage.save_brain_records([entity], scope="ontology_catalogs")
    packet = ContextPacket(task={"kind": "test"}, conflicts=[entity.id])

    result = hydrate_context_packet(packet, storage=storage)

    assert result.excerpts[0].label == "conflict"


def test_hydrate_truncates_long_text_and_flags_it(storage) -> None:
    entity = make_entity("entity:system:agv_fleet", description="x" * 5000)
    storage.save_brain_records([entity], scope="ontology_catalogs")
    packet = ContextPacket(task={"kind": "test"}, entities=[entity.id])

    result = hydrate_context_packet(packet, storage=storage, max_excerpt_chars=100)

    assert len(result.excerpts[0].text) == 100
    assert result.excerpts[0].truncated is True


def test_hydrate_deduplicates_ids_appearing_in_multiple_fields(storage) -> None:
    entity = make_entity("entity:system:agv_fleet")
    storage.save_brain_records([entity], scope="ontology_catalogs")
    packet = ContextPacket(
        task={"kind": "test"},
        approved_knowledge=[entity.id],
        entities=[entity.id],
    )

    result = hydrate_context_packet(packet, storage=storage)

    assert len(result.excerpts) == 1


def test_hydrate_prioritizes_approved_knowledge_ids_when_truncating(storage) -> None:
    approved = make_entity("entity:system:approved_one").model_copy(
        update={"validation_status": ValidationStatus.SME_APPROVED}
    )
    working_entities = [
        make_entity(f"entity:system:working_{i}") for i in range(MAX_HYDRATED_EXCERPTS)
    ]
    storage.save_brain_records([approved, *working_entities], scope="ontology_catalogs")
    packet = ContextPacket(
        task={"kind": "test"},
        entities=[e.id for e in working_entities],  # already at the cap
        approved_knowledge=[approved.id],  # must not be dropped
    )

    result = hydrate_context_packet(packet, storage=storage)

    assert len(result.excerpts) == MAX_HYDRATED_EXCERPTS
    assert any(e.id == approved.id and e.label == "approved" for e in result.excerpts)
    assert result.truncated_excerpt_count == 1


def test_hydrate_skips_ids_that_no_longer_resolve(storage) -> None:
    packet = ContextPacket(task={"kind": "test"}, entities=["entity:system:does_not_exist"])
    result = hydrate_context_packet(packet, storage=storage)
    assert result.excerpts == []


def test_hydrate_keeps_original_packet_on_result(storage) -> None:
    packet = ContextPacket(task={"kind": "test"}, entities=["entity:system:x"])
    result = hydrate_context_packet(packet, storage=storage)
    assert result.packet is packet
