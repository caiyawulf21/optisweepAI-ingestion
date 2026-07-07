from __future__ import annotations

from shared_pipeline_stages.stage_6_5.schemas import MergeCluster, PairwiseMatch


def split_oversized_cluster(
    cluster: MergeCluster,
    *,
    max_size: int = 3,
) -> list[list[str]]:
    members = list(cluster.finalized_runbook_ids)
    if len(members) <= max_size:
        return [sorted(members)]
    return _greedy_split(members, cluster.pairwise_matches, max_size=max_size)


def build_sub_clusters(
    cluster: MergeCluster,
    *,
    max_size: int = 3,
) -> list[MergeCluster]:
    member_groups = split_oversized_cluster(cluster, max_size=max_size)
    auto_split = len(member_groups) > 1
    sub_clusters: list[MergeCluster] = []
    for index, members in enumerate(member_groups, start=1):
        member_set = set(members)
        member_cards_ids = [member_id for member_id in members]
        cluster_matches = [
            match
            for match in cluster.pairwise_matches
            if match.source_id in member_set and match.target_id in member_set
        ]
        cluster_matches.sort(key=lambda item: (-item.combined_score, item.source_id, item.target_id))
        max_score = cluster_matches[0].combined_score if cluster_matches else cluster.similarity_score
        candidate_ids: list[str] = []
        source_types = sorted(set(cluster.source_types))
        sub_clusters.append(
            MergeCluster(
                merge_cluster_id=f"{cluster.merge_cluster_id}__sub_{index}",
                finalized_runbook_ids=sorted(member_cards_ids),
                candidate_ids=sorted(set(candidate_ids)),
                source_types=source_types,
                similarity_score=max_score,
                merge_hint=cluster.merge_hint,
                requires_stage_7_llm=cluster.requires_stage_7_llm,
                evidence_notes=_sub_cluster_notes(cluster, members, auto_split),
                pairwise_matches=cluster_matches,
            )
        )
    return sub_clusters


def _greedy_split(
    members: list[str],
    pairwise_matches: list[PairwiseMatch],
    *,
    max_size: int,
) -> list[list[str]]:
    remaining = set(members)
    subclusters: list[list[str]] = []
    while remaining:
        if len(remaining) <= max_size:
            subclusters.append(sorted(remaining))
            break
        seed_match = _best_internal_match(remaining, pairwise_matches)
        if seed_match is None:
            chunk = sorted(remaining)[:max_size]
            subclusters.append(chunk)
            remaining -= set(chunk)
            continue
        group = {seed_match.source_id, seed_match.target_id}
        while len(group) < max_size:
            next_member = _best_neighbor(group, remaining, pairwise_matches)
            if next_member is None:
                break
            group.add(next_member)
        subclusters.append(sorted(group))
        remaining -= group
    return subclusters


def _best_internal_match(
    remaining: set[str],
    pairwise_matches: list[PairwiseMatch],
) -> PairwiseMatch | None:
    best: PairwiseMatch | None = None
    for match in pairwise_matches:
        if match.source_id not in remaining or match.target_id not in remaining:
            continue
        if best is None or match.combined_score > best.combined_score:
            best = match
    return best


def _best_neighbor(
    group: set[str],
    remaining: set[str],
    pairwise_matches: list[PairwiseMatch],
) -> str | None:
    candidates: list[tuple[float, str]] = []
    for member_id in remaining:
        if member_id in group:
            continue
        score = _max_pair_score(member_id, group, pairwise_matches)
        if score >= 0:
            candidates.append((score, member_id))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (-item[0], item[1]))
    return candidates[0][1]


def _max_pair_score(
    member_id: str,
    group: set[str],
    pairwise_matches: list[PairwiseMatch],
) -> float:
    best = -1.0
    for match in pairwise_matches:
        if match.source_id == member_id and match.target_id in group:
            best = max(best, match.combined_score)
        elif match.target_id == member_id and match.source_id in group:
            best = max(best, match.combined_score)
    return best


def _sub_cluster_notes(cluster: MergeCluster, members: list[str], auto_split: bool) -> list[str]:
    notes = list(cluster.evidence_notes)
    if auto_split:
        notes.insert(
            0,
            f"Auto-split from parent cluster {cluster.merge_cluster_id} "
            f"({len(cluster.finalized_runbook_ids)} members) into sub-cluster of {len(members)}.",
        )
    return notes
