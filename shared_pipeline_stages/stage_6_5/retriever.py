from __future__ import annotations

from typing import Protocol

from shared_pipeline_stages.stage_6_5.schemas import PairwiseMatch, RetrievalCard
from shared_pipeline_stages.stage_6_5.similarity import SimilarityConfig, score_pair


class RunbookRetriever(Protocol):
    def search(
        self,
        query: RetrievalCard,
        *,
        top_k: int = 10,
        exclude_source_types: list[str] | None = None,
        min_score: float = 0.0,
        cross_source_only: bool = True,
    ) -> list[PairwiseMatch]: ...


class InMemoryRunbookRetriever:
    def __init__(
        self,
        cards: list[RetrievalCard],
        vectors: dict[str, list[float]],
        config: SimilarityConfig,
    ) -> None:
        self.cards = cards
        self.card_by_id = {card.finalized_runbook_id: card for card in cards}
        self.vectors = vectors
        self.config = config

    def search(
        self,
        query: RetrievalCard,
        *,
        top_k: int = 10,
        exclude_source_types: list[str] | None = None,
        min_score: float = 0.0,
        cross_source_only: bool = True,
    ) -> list[PairwiseMatch]:
        excluded = set(exclude_source_types or [])
        query_vector = self.vectors.get(query.finalized_runbook_id, [])
        matches: list[PairwiseMatch] = []
        for candidate in self.cards:
            if candidate.finalized_runbook_id == query.finalized_runbook_id:
                continue
            if candidate.source_type in excluded:
                continue
            if cross_source_only and candidate.source_type == query.source_type:
                continue
            match = score_pair(
                query,
                candidate,
                query_vector,
                self.vectors.get(candidate.finalized_runbook_id, []),
                self.config,
            )
            if match.combined_score >= min_score:
                matches.append(match)
        matches.sort(
            key=lambda item: (
                -item.combined_score,
                item.target_id,
            )
        )
        return matches[:top_k]
