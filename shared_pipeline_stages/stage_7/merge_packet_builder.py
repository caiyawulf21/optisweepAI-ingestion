from __future__ import annotations

from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.json_utils import read_json
from shared_pipeline_stages.stage_6_5.schemas import MergeCluster, RunbookPoolEntry
from shared_pipeline_stages.stage_7.schemas import MergePacket


def load_runbooks_by_procedure_id(pool_dir: str | Path) -> dict[str, dict[str, Any]]:
    pool_path = Path(pool_dir) / "runbook_pool.json"
    payload = read_json(pool_path)
    entries = payload.get("entries") if isinstance(payload, dict) else payload
    if not isinstance(entries, list):
        raise ValueError("runbook_pool.json must contain an entries list.")
    runbooks: dict[str, dict[str, Any]] = {}
    for item in entries:
        entry = RunbookPoolEntry.model_validate(item)
        if not entry.source_path:
            raise ValueError(
                f"Missing source_path for finalized runbook {entry.finalized_runbook_id} in runbook_pool.json."
            )
        runbook = read_json(entry.source_path)
        if not isinstance(runbook, dict):
            raise ValueError(f"Finalized runbook must be a JSON object: {entry.source_path}")
        runbook["_source_path"] = entry.source_path
        runbooks[entry.finalized_runbook_id] = runbook
    return runbooks


def build_merge_packet(
    cluster: MergeCluster,
    runbooks_by_id: dict[str, dict[str, Any]],
    *,
    existing_canonical_runbook: dict[str, Any] | None = None,
    auto_split: bool = False,
    parent_cluster_id: str = "",
) -> MergePacket:
    finalized_runbooks: list[dict[str, Any]] = []
    missing: list[str] = []
    for runbook_id in cluster.finalized_runbook_ids:
        runbook = runbooks_by_id.get(runbook_id)
        if runbook is None:
            missing.append(runbook_id)
            continue
        finalized_runbooks.append(runbook)
    if missing:
        raise ValueError(f"Missing finalized runbooks for merge cluster {cluster.merge_cluster_id}: {missing}")
    if len(finalized_runbooks) < 2:
        raise ValueError(
            f"Merge cluster {cluster.merge_cluster_id} must contain at least two finalized runbooks."
        )
    _assert_cross_source(cluster)
    return MergePacket(
        merge_cluster_id=parent_cluster_id or cluster.merge_cluster_id,
        sub_cluster_id=cluster.merge_cluster_id,
        merge_hint=cluster.merge_hint,
        similarity_score=cluster.similarity_score,
        evidence_notes=cluster.evidence_notes,
        pairwise_matches=[match.model_dump(mode="json") for match in cluster.pairwise_matches],
        finalized_runbooks=finalized_runbooks,
        existing_canonical_runbook=existing_canonical_runbook,
        auto_split=auto_split,
        parent_cluster_id=parent_cluster_id,
    )


def _assert_cross_source(cluster: MergeCluster) -> None:
    if len(cluster.source_types) < 2:
        raise ValueError(
            f"Merge cluster {cluster.merge_cluster_id} must span multiple source types; "
            f"got {cluster.source_types}."
        )
