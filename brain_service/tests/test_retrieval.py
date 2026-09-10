from __future__ import annotations

from brain.schemas.common import RecordType
from brain_service.retrieval import find_similar_records
from providers.embeddings import EmbeddingProvider


class FakeEmbeddingProvider(EmbeddingProvider):
    """Returns the query text's own pre-registered vector, so a test can
    control exactly which stored vector should rank closest without a real
    embedding call."""

    def __init__(self, vectors_by_text: dict[str, list[float]]) -> None:
        self._vectors_by_text = vectors_by_text

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._vectors_by_text[text] for text in texts]

    def embedding_model_id(self) -> str:
        return "fake-model"


def test_find_similar_records_ranks_by_cosine_similarity(storage) -> None:
    storage.save_embeddings(
        [
            {"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "fake", "vector": [1.0, 0.0]},
            {"record_id": "entity:system:b", "record_type": "entity", "embedding_model": "fake", "vector": [0.0, 1.0]},
            {"record_id": "entity:system:c", "record_type": "entity", "embedding_model": "fake", "vector": [0.9, 0.1]},
        ]
    )
    embeddings = FakeEmbeddingProvider({"query about a": [1.0, 0.0]})

    matches = find_similar_records(embeddings, storage, query_text="query about a", top_k=2)

    assert [m.record_id for m in matches] == ["entity:system:a", "entity:system:c"]
    assert matches[0].score > matches[1].score


def test_find_similar_records_filters_by_record_type(storage) -> None:
    storage.save_embeddings(
        [
            {"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "fake", "vector": [1.0, 0.0]},
            {"record_id": "claim:x:y", "record_type": "claim", "embedding_model": "fake", "vector": [1.0, 0.0]},
        ]
    )
    embeddings = FakeEmbeddingProvider({"q": [1.0, 0.0]})

    matches = find_similar_records(embeddings, storage, query_text="q", record_type=RecordType.CLAIM)

    assert [m.record_id for m in matches] == ["claim:x:y"]


def test_find_similar_records_respects_min_score(storage) -> None:
    storage.save_embeddings(
        [
            {"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "fake", "vector": [1.0, 0.0]},
            {"record_id": "entity:system:b", "record_type": "entity", "embedding_model": "fake", "vector": [-1.0, 0.0]},
        ]
    )
    embeddings = FakeEmbeddingProvider({"q": [1.0, 0.0]})

    matches = find_similar_records(embeddings, storage, query_text="q", min_score=0.5)

    assert [m.record_id for m in matches] == ["entity:system:a"]


def test_find_similar_records_returns_empty_for_no_embeddings(storage) -> None:
    embeddings = FakeEmbeddingProvider({"q": [1.0, 0.0]})
    matches = find_similar_records(embeddings, storage, query_text="q")
    assert matches == []


def test_find_similar_records_handles_zero_vector_without_crashing(storage) -> None:
    storage.save_embeddings(
        [{"record_id": "entity:system:zero", "record_type": "entity", "embedding_model": "fake", "vector": [0.0, 0.0]}]
    )
    embeddings = FakeEmbeddingProvider({"q": [1.0, 0.0]})

    matches = find_similar_records(embeddings, storage, query_text="q")

    assert matches[0].score == 0.0
