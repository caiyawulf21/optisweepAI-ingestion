from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from shared_pipeline_stages.stage_6_5.retrieval_card import build_retrieval_text
from shared_pipeline_stages.stage_6_5.schemas import RetrievalCard
from shared_pipeline_stages.stage_6_5.similarity import SimilarityConfig, cosine_similarity, token_jaccard
from shared_pipeline_stages.stage_8.link_scoring import (
    anchor_overlap,
    boost_combined_score,
    build_retrieval_query_text,
    canonical_source_adjustment,
    normalize_placeholder_text,
    procedure_type_boost,
    runbook_match_text,
)
from shared_pipeline_stages.stage_8.normalize import procedure_type_compatible
from shared_pipeline_stages.stage_8.schemas import RunbookSearchMatch


@dataclass
class RunbookCatalogSearch:
    cards: list[RetrievalCard]
    vectors: dict[str, list[float]]
    runbooks_by_id: dict[str, dict[str, Any]]
    config: SimilarityConfig
    incident_preference_margin: float = 0.02

    @classmethod
    def from_pool_artifacts(
        cls,
        retrieval_cards: list[dict[str, Any] | RetrievalCard],
        retrieval_index: list[dict[str, Any]],
        runbooks: list[dict[str, Any]],
        *,
        config: SimilarityConfig | None = None,
        incident_preference_margin: float = 0.02,
    ) -> RunbookCatalogSearch:
        cards = [
            item if isinstance(item, RetrievalCard) else RetrievalCard.model_validate(item)
            for item in retrieval_cards
        ]
        vectors = {
            str(entry.get("finalized_runbook_id") or ""): list(entry.get("vector") or [])
            for entry in retrieval_index
            if isinstance(entry, dict)
        }
        runbooks_by_id = {
            str(runbook.get("procedure_id") or ""): runbook
            for runbook in runbooks
            if isinstance(runbook, dict) and str(runbook.get("procedure_id") or "").strip()
        }
        return cls(
            cards=cards,
            vectors=vectors,
            runbooks_by_id=runbooks_by_id,
            config=config or SimilarityConfig(),
            incident_preference_margin=incident_preference_margin,
        )

    def search(
        self,
        query_text: str,
        *,
        query_vector: list[float] | None = None,
        top_k: int = 10,
        min_score: float = 0.0,
        case_id: str = "",
        node_type: str = "",
    ) -> list[RunbookSearchMatch]:
        if query_vector is None:
            query_vector = []
        matches: list[RunbookSearchMatch] = []
        for card in self.cards:
            candidate_vector = self.vectors.get(card.finalized_runbook_id, [])
            cosine = cosine_similarity(query_vector, candidate_vector) if query_vector else 0.0
            jaccard = token_jaccard(query_text, card.retrieval_text or build_retrieval_text(card))
            combined = self.config.vector_weight * cosine + self.config.lexical_weight * jaccard
            combined += procedure_type_boost(node_type, card.procedure_type)
            runbook = self.runbooks_by_id.get(card.finalized_runbook_id, {})
            metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
            source_type = str(metadata.get("source_type") or card.source_type or "")
            combined += canonical_source_adjustment(
                RunbookSearchMatch(
                    procedure_id=card.finalized_runbook_id,
                    title=card.title,
                    procedure_type=card.procedure_type,
                    cosine_score=round(cosine, 4),
                    jaccard_score=round(jaccard, 4),
                    combined_score=round(combined, 4),
                    source_type=source_type,
                )
            )
            if combined < min_score and cosine == 0.0 and jaccard >= min_score:
                combined = jaccard + procedure_type_boost(node_type, card.procedure_type)
                combined += canonical_source_adjustment(
                    RunbookSearchMatch(
                        procedure_id=card.finalized_runbook_id,
                        title=card.title,
                        procedure_type=card.procedure_type,
                        cosine_score=round(cosine, 4),
                        jaccard_score=round(jaccard, 4),
                        combined_score=round(combined, 4),
                        source_type=source_type,
                    )
                )
            if combined < min_score:
                continue
            if node_type and not procedure_type_compatible(node_type, card.procedure_type):
                continue
            matches.append(
                RunbookSearchMatch(
                    procedure_id=card.finalized_runbook_id,
                    title=card.title,
                    procedure_type=card.procedure_type,
                    cosine_score=round(cosine, 4),
                    jaccard_score=round(jaccard, 4),
                    combined_score=round(combined, 4),
                    preferred_incident_source=_is_incident_source_for_case(metadata, card, case_id),
                    source_type=source_type,
                    source_id=str(metadata.get("source_id") or card.source_id or ""),
                )
            )
        matches.sort(key=lambda item: (-item.combined_score, item.procedure_id))
        filtered = [item for item in matches if item.procedure_id in self.runbooks_by_id]
        return self._apply_incident_preference(filtered[:top_k], case_id)

    def search_for_node(
        self,
        node: dict[str, Any],
        *,
        query_vector: list[float] | None = None,
        top_k: int = 10,
        min_score: float = 0.0,
        case_id: str = "",
        affected_systems: list[str] | None = None,
    ) -> list[RunbookSearchMatch]:
        query_text = build_retrieval_query_text(node, affected_systems=affected_systems)
        return self.search(
            query_text,
            query_vector=query_vector,
            top_k=top_k,
            min_score=min_score,
            case_id=case_id,
            node_type=str(node.get("node_type") or ""),
        )

    def _apply_incident_preference(
        self,
        matches: list[RunbookSearchMatch],
        case_id: str,
    ) -> list[RunbookSearchMatch]:
        if not matches or not case_id:
            return matches
        incident_matches = [item for item in matches if item.preferred_incident_source]
        if not incident_matches:
            return matches
        top_score = matches[0].combined_score
        best_incident = incident_matches[0]
        if top_score - best_incident.combined_score <= self.incident_preference_margin:
            reordered = [best_incident] + [item for item in matches if item.procedure_id != best_incident.procedure_id]
            return reordered
        return matches


def build_node_query_text(node: dict[str, Any], *, affected_systems: list[str] | None = None) -> str:
    return build_retrieval_query_text(node, affected_systems=affected_systems)


def _is_incident_source_for_case(metadata: dict[str, Any], card: RetrievalCard, case_id: str) -> bool:
    if not case_id:
        return False
    normalized_case = case_id.replace("case_", "")
    haystacks = [
        str(metadata.get("source_id") or ""),
        str(metadata.get("source_case_id") or ""),
        str(card.source_id or ""),
        str(card.source_path or ""),
    ]
    for lineage in metadata.get("source_lineage") or []:
        if isinstance(lineage, dict):
            haystacks.append(str(lineage.get("source_id") or ""))
            haystacks.append(str(lineage.get("source_case_id") or ""))
    joined = " ".join(haystacks).lower()
    return normalized_case in joined or f"case_{normalized_case}" in joined or "incident" in joined and normalized_case in joined
