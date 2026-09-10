from __future__ import annotations

from brain.schemas.common import RecordType
from brain_service.scripts.backfill_embeddings import backfill_embeddings
from brain_service.tests.conftest import make_entity


class _CountingFakeEmbedder:
    def __init__(self) -> None:
        self.call_count = 0
        self.embedded_texts: list[str] = []

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        self.call_count += 1
        self.embedded_texts.extend(texts)
        return [[float(len(text))] for text in texts]

    def embedding_model_id(self) -> str:
        return "fake-model"


def test_backfill_embeds_every_embeddable_record(storage) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:a"), make_entity("entity:system:b")], scope="operational_sources/test"
    )
    embedder = _CountingFakeEmbedder()

    counts = backfill_embeddings(embedder, storage)

    assert counts["entity"] == 2
    stored = storage.load_all_embeddings(record_type=RecordType.ENTITY)
    assert {row["record_id"] for row in stored} == {"entity:system:a", "entity:system:b"}


def test_backfill_is_idempotent_skips_already_embedded(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope="operational_sources/test")
    embedder = _CountingFakeEmbedder()

    backfill_embeddings(embedder, storage)
    first_call_count = embedder.call_count
    backfill_embeddings(embedder, storage)

    assert embedder.call_count == first_call_count  # no new calls, already embedded


def test_backfill_force_re_embeds_everything(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope="operational_sources/test")
    embedder = _CountingFakeEmbedder()

    backfill_embeddings(embedder, storage)
    first_call_count = embedder.call_count
    backfill_embeddings(embedder, storage, force=True)

    assert embedder.call_count > first_call_count


def test_backfill_dry_run_reports_counts_without_calling_embedder(storage) -> None:
    storage.save_brain_records([make_entity("entity:system:a")], scope="operational_sources/test")
    embedder = _CountingFakeEmbedder()

    counts = backfill_embeddings(embedder, storage, dry_run=True)

    assert counts["entity"] == 1
    assert embedder.call_count == 0
    assert storage.load_all_embeddings() == []


def test_backfill_only_processes_embeddable_record_types(storage) -> None:
    """BrainReview is deliberately excluded (working/pending material, not
    corpus content a semantic search over Brain's knowledge should
    surface)."""
    from brain_service.review import build_review
    from brain.schemas.review import ReviewKind

    storage.save_brain_records(
        [build_review(kind=ReviewKind.GAP, affected_record_ids=["entity:system:a"], proposed_change="x")],
        scope="reviews/test",
    )
    embedder = _CountingFakeEmbedder()

    counts = backfill_embeddings(embedder, storage)

    assert "review" not in counts
