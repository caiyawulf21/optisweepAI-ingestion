"""Real semantic retrieval: embed a free-text query, brute-force cosine
search over stored embeddings, return the closest record ids. Correct and
simple at the current corpus scale (~20K records, confirmed fast enough --
see brain_service/tests/test_retrieval.py's timing note); no vector
DB/ANN index needed yet. This is the piece AGENT_DESIGN_NOTES.md §14.4
explicitly deferred ("embeddings, ranking... explicitly NOT implemented"),
now built.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from brain.schemas.common import RecordType
from providers.embeddings import EmbeddingProvider
from providers.storage import StorageProvider


@dataclass(frozen=True)
class SimilarityMatch:
    record_id: str
    record_type: RecordType
    score: float


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def find_similar_records(
    embeddings: EmbeddingProvider,
    storage: StorageProvider,
    *,
    query_text: str | None = None,
    query_vector: list[float] | None = None,
    record_type: RecordType | None = None,
    top_k: int = 10,
    min_score: float = 0.0,
) -> list[SimilarityMatch]:
    """Ranks every stored embedding (optionally filtered to one record
    type) by cosine similarity against the query, returning at most
    `top_k` matches scoring at least `min_score`, highest first.

    Pass `query_vector` directly when the caller already embedded the
    query text once and is calling this multiple times for different
    record types (e.g. get_brain_context searching entities/claims/
    evidence for the same query) -- embedding is a real network call
    (AzureOpenAIEmbeddingProvider), and re-embedding identical text once
    per record type was a real, measured cost in production (2026-09-10:
    get_brain_context previously called this 3x per request, each
    re-embedding the same query_text from scratch). `query_text` alone
    still works for a single-call site (e.g. brain_ontology_bridge.py)
    that has no reason to precompute a vector itself. Exactly one of
    `query_text`/`query_vector` must be given.

    Brute force: loads every stored vector and compares in Python. At the
    current corpus size this is fast in itself (confirmed against the
    real corpus, see test_retrieval.py) -- the real production latency
    problem turned out to be uncached network fetches (embeddings +
    load_brain_context), not this comparison step; revisit with an ANN
    index only if the comparison itself becomes the bottleneck, not
    before."""
    if (query_text is None) == (query_vector is None):
        raise ValueError("find_similar_records requires exactly one of query_text or query_vector")
    resolved_vector = query_vector if query_vector is not None else embeddings.embed_texts([query_text])[0]
    stored = storage.load_all_embeddings(record_type=record_type)

    scored = [
        SimilarityMatch(
            record_id=row["record_id"],
            record_type=RecordType(row["record_type"]),
            score=_cosine_similarity(resolved_vector, row["vector"]),
        )
        for row in stored
    ]
    scored = [match for match in scored if match.score >= min_score]
    scored.sort(key=lambda match: match.score, reverse=True)
    return scored[:top_k]
