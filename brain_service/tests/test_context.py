from __future__ import annotations

from brain.schemas.common import ValidationStatus
from brain.schemas.relationship import Relationship, RelationshipType
from brain_service.context import get_brain_context
from brain_service.tests.conftest import make_entity


def test_get_brain_context_returns_only_requested_entities(storage) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:a"), make_entity("entity:system:b")], scope="incidents/case_1"
    )

    packet = get_brain_context(storage, task={"kind": "test"}, entity_ids=["entity:system:a"])

    assert packet.entities == ["entity:system:a"]


def test_get_brain_context_expands_one_hop_via_relationship(storage) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:a"), make_entity("entity:system:b")], scope="incidents/case_1"
    )
    rel = Relationship(
        id="relationship:a:controls:b",
        from_id="entity:system:a",
        relationship_type=RelationshipType.CONTROLS,
        to_id="entity:system:b",
        source_refs=["evidence:test:seed"],
    )
    storage.save_brain_records([rel], scope="incidents/case_1")

    packet = get_brain_context(storage, task={"kind": "test"}, entity_ids=["entity:system:a"], hops=1)

    assert set(packet.entities) == {"entity:system:a", "entity:system:b"}


def test_get_brain_context_zero_hops_does_not_expand(storage) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:a"), make_entity("entity:system:b")], scope="incidents/case_1"
    )
    rel = Relationship(
        id="relationship:a:controls:b",
        from_id="entity:system:a",
        relationship_type=RelationshipType.CONTROLS,
        to_id="entity:system:b",
        source_refs=["evidence:test:seed"],
    )
    storage.save_brain_records([rel], scope="incidents/case_1")

    packet = get_brain_context(storage, task={"kind": "test"}, entity_ids=["entity:system:a"], hops=0)

    assert packet.entities == ["entity:system:a"]


def test_get_brain_context_filters_by_relationship_type(storage) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:a"), make_entity("entity:system:b"), make_entity("entity:system:c")],
        scope="incidents/case_1",
    )
    storage.save_brain_records(
        [
            Relationship(
                id="relationship:a:controls:b",
                from_id="entity:system:a",
                relationship_type=RelationshipType.CONTROLS,
                to_id="entity:system:b",
                source_refs=["evidence:test:seed"],
            ),
            Relationship(
                id="relationship:a:observes:c",
                from_id="entity:system:a",
                relationship_type=RelationshipType.OBSERVES,
                to_id="entity:system:c",
                source_refs=["evidence:test:seed"],
            ),
        ],
        scope="incidents/case_1",
    )

    packet = get_brain_context(
        storage,
        task={"kind": "test"},
        entity_ids=["entity:system:a"],
        relationship_types=[RelationshipType.CONTROLS],
        hops=1,
    )

    assert set(packet.entities) == {"entity:system:a", "entity:system:b"}


def test_get_brain_context_only_approved_statuses_in_approved_knowledge(storage) -> None:
    approved = make_entity("entity:system:approved").model_copy(
        update={"validation_status": ValidationStatus.SME_APPROVED}
    )
    unreviewed = make_entity("entity:system:unreviewed").model_copy(
        update={"validation_status": ValidationStatus.OPERATIONAL_UNREVIEWED}
    )
    storage.save_brain_records([approved, unreviewed], scope="incidents/case_1")

    packet = get_brain_context(
        storage, task={"kind": "test"}, entity_ids=["entity:system:approved", "entity:system:unreviewed"]
    )

    assert packet.approved_knowledge == ["entity:system:approved"]
    assert set(packet.entities) == {"entity:system:approved", "entity:system:unreviewed"}


def test_get_brain_context_no_entity_ids_returns_empty_packet(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope="incidents/case_1")

    packet = get_brain_context(storage, task={"kind": "test"})

    assert packet.entities == []


class _FakeEmbeddingProvider:
    def __init__(self, query_vector: list[float]) -> None:
        self._query_vector = query_vector

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._query_vector for _ in texts]

    def embedding_model_id(self) -> str:
        return "fake-model"


def test_get_brain_context_query_text_finds_matching_entity_via_semantic_search(storage) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:a"), make_entity("entity:system:b")], scope="incidents/case_1"
    )
    storage.save_embeddings(
        [
            {"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "m", "vector": [1.0, 0.0]},
            {"record_id": "entity:system:b", "record_type": "entity", "embedding_model": "m", "vector": [0.0, 1.0]},
        ]
    )
    embeddings = _FakeEmbeddingProvider(query_vector=[1.0, 0.0])

    packet = get_brain_context(
        storage, task={"kind": "test"}, query_text="something about a",
        embeddings=embeddings, semantic_min_score=0.5,
    )

    assert packet.entities == ["entity:system:a"]


def test_get_brain_context_query_text_below_min_score_finds_nothing(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope="incidents/case_1")
    storage.save_embeddings(
        [{"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "m", "vector": [0.0, 1.0]}]
    )
    embeddings = _FakeEmbeddingProvider(query_vector=[1.0, 0.0])  # orthogonal -> score 0.0

    packet = get_brain_context(
        storage, task={"kind": "test"}, query_text="unrelated query",
        embeddings=embeddings, semantic_min_score=0.5,
    )

    assert packet.entities == []


def test_get_brain_context_combines_explicit_entity_ids_and_semantic_matches(storage) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:explicit"), make_entity("entity:system:semantic")], scope="incidents/case_1"
    )
    storage.save_embeddings(
        [{"record_id": "entity:system:semantic", "record_type": "entity", "embedding_model": "m", "vector": [1.0, 0.0]}]
    )
    embeddings = _FakeEmbeddingProvider(query_vector=[1.0, 0.0])

    packet = get_brain_context(
        storage, task={"kind": "test"}, entity_ids=["entity:system:explicit"],
        query_text="q", embeddings=embeddings, semantic_min_score=0.5,
    )

    assert set(packet.entities) == {"entity:system:explicit", "entity:system:semantic"}
