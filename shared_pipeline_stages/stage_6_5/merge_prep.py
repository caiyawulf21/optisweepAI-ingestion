from __future__ import annotations

import re
from collections import defaultdict

from shared_pipeline_stages.stage_6_5.retriever import InMemoryRunbookRetriever
from shared_pipeline_stages.stage_6_5.schemas import MergeCluster, PairwiseMatch, PassThroughRunbook, RetrievalCard
from shared_pipeline_stages.stage_6_5.similarity import SimilarityConfig, merge_hint_for_score


class UnionFind:
    def __init__(self, ids: list[str]) -> None:
        self.parent = {item: item for item in ids}

    def find(self, item: str) -> str:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: str, right: str) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left != root_right:
            self.parent[root_right] = root_left

    def groups(self) -> dict[str, list[str]]:
        grouped: dict[str, list[str]] = defaultdict(list)
        for item in self.parent:
            grouped[self.find(item)].append(item)
        return grouped


def build_merge_clusters_and_pass_through(
    cards: list[RetrievalCard],
    retriever: InMemoryRunbookRetriever,
    config: SimilarityConfig,
    *,
    top_k: int = 10,
) -> tuple[list[MergeCluster], list[PassThroughRunbook], list[PairwiseMatch], dict[str, list[PairwiseMatch]]]:
    card_by_id = {card.finalized_runbook_id: card for card in cards}
    similarity_by_runbook: dict[str, list[PairwiseMatch]] = {}
    edge_matches: dict[frozenset[str], PairwiseMatch] = {}

    for card in cards:
        matches = retriever.search(
            card,
            top_k=top_k,
            min_score=config.min_merge_score,
            cross_source_only=True,
        )
        similarity_by_runbook[card.finalized_runbook_id] = matches
        for match in matches:
            key = frozenset({match.source_id, match.target_id})
            existing = edge_matches.get(key)
            if existing is None or match.combined_score > existing.combined_score:
                edge_matches[key] = match

    union_find = UnionFind([card.finalized_runbook_id for card in cards])
    for match in edge_matches.values():
        union_find.union(match.source_id, match.target_id)

    clustered_ids: set[str] = set()
    merge_clusters: list[MergeCluster] = []
    for members in union_find.groups().values():
        member_cards = [card_by_id[member_id] for member_id in members]
        source_types = sorted({card.source_type for card in member_cards if card.source_type})
        if len(source_types) < 2:
            continue
        clustered_ids.update(members)
        cluster_matches = [
            match
            for match in edge_matches.values()
            if match.source_id in members and match.target_id in members
        ]
        cluster_matches.sort(key=lambda item: (-item.combined_score, item.source_id, item.target_id))
        max_score = cluster_matches[0].combined_score if cluster_matches else 0.0
        merge_hint = merge_hint_for_score(max_score, config) or "needs_review"
        normalized_title = _choose_normalized_title(member_cards)
        merge_clusters.append(
            MergeCluster(
                merge_cluster_id=f"cluster_{_slug(normalized_title)}",
                finalized_runbook_ids=sorted(members),
                candidate_ids=sorted(card.candidate_id for card in member_cards),
                source_types=source_types,
                similarity_score=max_score,
                merge_hint=merge_hint,
                requires_stage_7_llm=True,
                evidence_notes=_cluster_evidence_notes(cluster_matches, member_cards),
                pairwise_matches=cluster_matches,
            )
        )

    merge_clusters.sort(key=lambda item: (-item.similarity_score, item.merge_cluster_id))
    pass_through = _build_pass_through(cards, clustered_ids, similarity_by_runbook, config)
    all_cross_source_pairs = sorted(
        edge_matches.values(),
        key=lambda item: (-item.combined_score, item.source_id, item.target_id),
    )
    return merge_clusters, pass_through, all_cross_source_pairs, similarity_by_runbook


def _build_pass_through(
    cards: list[RetrievalCard],
    clustered_ids: set[str],
    similarity_by_runbook: dict[str, list[PairwiseMatch]],
    config: SimilarityConfig,
) -> list[PassThroughRunbook]:
    pass_through: list[PassThroughRunbook] = []
    for card in cards:
        if card.finalized_runbook_id in clustered_ids:
            continue
        matches = similarity_by_runbook.get(card.finalized_runbook_id, [])
        cross_source_matches = [match for match in matches if match.combined_score >= config.min_merge_score]
        if cross_source_matches:
            reason = "below_threshold"
        else:
            reason = "singleton" if len(cards) == 1 else "no_match"
        pass_through.append(
            PassThroughRunbook(
                finalized_runbook_id=card.finalized_runbook_id,
                candidate_id=card.candidate_id,
                source_id=card.source_id,
                source_type=card.source_type,
                requires_stage_7_llm=False,
                pass_through_reason=reason,
            )
        )
    pass_through.sort(key=lambda item: item.finalized_runbook_id)
    return pass_through


def _cluster_evidence_notes(
    cluster_matches: list[PairwiseMatch],
    member_cards: list[RetrievalCard],
) -> list[str]:
    notes = [f"{len(member_cards)} finalized runbook(s) linked by cross-source similarity."]
    if cluster_matches:
        top = cluster_matches[0]
        notes.append(
            "Top pair score "
            f"{top.combined_score} (cosine {top.cosine_score}, jaccard {top.jaccard_score})."
        )
        if top.opposing_actions_detected:
            notes.append("Opposing actions detected in retrieval text; review carefully in Stage 7.")
        for warning in top.metadata_warnings:
            notes.append(f"Metadata warning: {warning}")
    source_types = sorted({card.source_type for card in member_cards if card.source_type})
    if len(source_types) > 1:
        notes.append("Source types represented: " + ", ".join(source_types) + ".")
    return notes


def _choose_normalized_title(cards: list[RetrievalCard]) -> str:
    ranked = sorted(
        cards,
        key=lambda card: (
            _source_title_rank(card.source_type),
            -len(card.title),
            card.title,
        ),
    )
    return ranked[0].title or "untitled"


def _source_title_rank(source_type: str) -> int:
    ranks = {
        "manual": 0,
        "sop": 1,
        "sme": 2,
        "training_slide": 3,
        "training_transcript": 4,
        "incident": 5,
    }
    return ranks.get(source_type, 10)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return re.sub(r"_+", "_", slug) or "untitled"
