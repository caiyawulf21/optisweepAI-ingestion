from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json
from shared_pipeline_stages.stage_6_5.schemas import MergeCluster, PassThroughRunbook
from shared_pipeline_stages.stage_7.artifact_loader import load_artifact_index_from_pool
from shared_pipeline_stages.stage_7.cluster_split import build_sub_clusters
from shared_pipeline_stages.stage_7.merge_comparison_review import write_merge_comparison_review
from shared_pipeline_stages.stage_7.merge_packet_builder import build_merge_packet, load_runbooks_by_procedure_id
from shared_pipeline_stages.stage_7.merge_runner import RunbookMergeClient
from shared_pipeline_stages.stage_7.normalize import normalize_merged_runbook, validate_canonical_runbook
from shared_pipeline_stages.stage_7.pass_through import promote_pass_through_runbook
from shared_pipeline_stages.stage_7.review_markdown import safe_review_filename, write_review_file
from shared_pipeline_stages.stage_7.schemas import (
    CandidateProcedureMapping,
    ClusterMergeResult,
    Stage7BuildResult,
)

STAGE7_DIR_NAME = "stage_7_merged_runbooks"


class Stage7BuildConfig:
    def __init__(
        self,
        *,
        max_cluster_size: int = 3,
        llm_used: bool = False,
        max_workers: int = 2,
    ) -> None:
        self.max_cluster_size = max_cluster_size
        self.llm_used = llm_used
        self.max_workers = max_workers


def build_stage7_merged_runbooks(
    pool_dir: str | Path,
    output_dir: str | Path,
    *,
    config: Stage7BuildConfig | None = None,
    llm_client: RunbookMergeClient | None = None,
    generated_at: str | None = None,
) -> Stage7BuildResult:
    build_config = config or Stage7BuildConfig()
    pool_path = Path(pool_dir)
    output_path = _resolve_output_path(Path(output_dir))
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = generated_at or datetime.now(UTC).isoformat().replace("+00:00", "Z")

    merge_clusters = [MergeCluster.model_validate(item) for item in read_json(pool_path / "merge_clusters.json")]
    pass_through_entries = [
        PassThroughRunbook.model_validate(item) for item in read_json(pool_path / "pass_through_runbooks.json")
    ]
    runbooks_by_id = load_runbooks_by_procedure_id(pool_path)
    artifact_index = load_artifact_index_from_pool(pool_path)
    asset_link_cache: dict[str, str] = {}
    review_base = output_path / "review_markdown" / "runbooks"

    canonical_runbooks: list[dict[str, Any]] = []
    candidate_mappings: list[CandidateProcedureMapping] = []
    cluster_results: list[ClusterMergeResult] = []
    merge_packets: list[dict[str, Any]] = []
    warnings: list[str] = []
    failed: list[dict[str, Any]] = []

    clustered_ids = {
        runbook_id
        for cluster in merge_clusters
        for runbook_id in cluster.finalized_runbook_ids
    }
    for entry in pass_through_entries:
        if entry.finalized_runbook_id in clustered_ids:
            continue
        source_runbook = runbooks_by_id.get(entry.finalized_runbook_id)
        if source_runbook is None:
            warnings.append(f"Missing pass-through runbook {entry.finalized_runbook_id}.")
            continue
        promoted = promote_pass_through_runbook(source_runbook)
        errors = validate_canonical_runbook(promoted)
        if errors:
            warnings.append(
                f"Pass-through validation warnings for {entry.finalized_runbook_id}: " + "; ".join(errors)
            )
        canonical_runbooks.append(promoted)
        candidate_mappings.append(
            CandidateProcedureMapping(
                candidate_id=entry.candidate_id,
                canonical_procedure_id=str(promoted.get("procedure_id") or ""),
                source_procedure_id=entry.finalized_runbook_id,
                merge_action="pass_through",
            )
        )
        write_review_file(
            promoted,
            review_base / safe_review_filename(str(promoted.get("procedure_id") or "")),
            artifact_index=artifact_index,
            asset_link_cache=asset_link_cache,
        )

    sub_clusters: list[tuple[MergeCluster, bool, str]] = []
    for cluster in merge_clusters:
        if not cluster.requires_stage_7_llm:
            warnings.append(f"Skipped cluster {cluster.merge_cluster_id}: requires_stage_7_llm=false.")
            continue
        split_clusters = build_sub_clusters(cluster, max_size=build_config.max_cluster_size)
        auto_split = len(split_clusters) > 1
        parent_id = cluster.merge_cluster_id if auto_split else ""
        for split_cluster in split_clusters:
            candidate_ids = sorted(
                {
                    str(runbooks_by_id[runbook_id].get("candidate_id") or "")
                    for runbook_id in split_cluster.finalized_runbook_ids
                    if runbook_id in runbooks_by_id
                    and str(runbooks_by_id[runbook_id].get("candidate_id") or "").strip()
                }
            )
            if candidate_ids:
                split_cluster = split_cluster.model_copy(update={"candidate_ids": candidate_ids})
            sub_clusters.append((split_cluster, auto_split, parent_id))

    llm_jobs: list[tuple[MergeCluster, bool, str, dict[str, Any]]] = []
    for split_cluster, auto_split, parent_id in sub_clusters:
        try:
            packet = build_merge_packet(
                split_cluster,
                runbooks_by_id,
                auto_split=auto_split,
                parent_cluster_id=parent_id,
            )
        except ValueError as exc:
            failed.append(
                {
                    "merge_cluster_id": split_cluster.merge_cluster_id,
                    "error": str(exc),
                }
            )
            continue
        merge_packets.append(packet.model_dump(mode="json"))
        llm_jobs.append((split_cluster, auto_split, parent_id, packet.model_dump(mode="json")))

    if build_config.llm_used:
        if llm_client is None:
            raise ValueError("Stage 7 requires an LLM client when --llm is enabled.")
        _run_llm_jobs(
            llm_jobs,
            llm_client=llm_client,
            max_workers=build_config.max_workers,
            canonical_runbooks=canonical_runbooks,
            candidate_mappings=candidate_mappings,
            cluster_results=cluster_results,
            failed=failed,
            output_path=output_path,
            artifact_index=artifact_index,
            asset_link_cache=asset_link_cache,
            review_base=review_base,
        )

    comparison_path = output_path / "review_markdown" / "merge_comparison_review.md"
    write_merge_comparison_review(
        comparison_path,
        cluster_results=cluster_results,
        source_runbooks_by_id=runbooks_by_id,
        canonical_by_id={str(item.get("procedure_id") or ""): item for item in canonical_runbooks},
        artifact_index=artifact_index,
        generated_at=timestamp,
    )

    result = Stage7BuildResult(
        generated_at=timestamp,
        canonical_runbook_count=len(canonical_runbooks),
        pass_through_count=len([item for item in candidate_mappings if item.merge_action == "pass_through"]),
        merge_cluster_count=len(merge_clusters),
        sub_cluster_count=len(sub_clusters),
        llm_merge_count=len([item for item in cluster_results if item.llm_used and item.merge_decision == "merged"]),
    )

    write_json(output_path / "canonical_runbooks.json", {"runbooks": canonical_runbooks, **result.model_dump()})
    write_json(
        output_path / "candidate_to_procedure_mapping.json",
        {"mappings": [item.model_dump(mode="json") for item in candidate_mappings]},
    )
    write_json(
        output_path / "runbook_merge_report.json",
        {
            "stage": "stage_7_cross_source_runbook_merge",
            "llm_used": build_config.llm_used,
            "max_cluster_size": build_config.max_cluster_size,
            "generated_at": timestamp,
            "merge_cluster_count": len(merge_clusters),
            "sub_cluster_count": len(sub_clusters),
            "llm_merge_count": result.llm_merge_count,
            "cluster_results": [item.model_dump(mode="json") for item in cluster_results],
            "failed": failed,
            "warnings": warnings,
        },
    )
    write_json(output_path / "merge_packets.json", merge_packets)
    write_json(
        output_path / "stage7_review_index.json",
        {
            "merge_comparison_review": str(comparison_path),
            "review_markdown_dir": str(output_path / "review_markdown" / "runbooks"),
            "assets_dir": str(output_path / "review_markdown" / "assets"),
            "artifact_count": len(artifact_index),
        },
    )
    return result


def _run_llm_jobs(
    jobs: list[tuple[MergeCluster, bool, str, dict[str, Any]]],
    *,
    llm_client: RunbookMergeClient,
    max_workers: int,
    canonical_runbooks: list[dict[str, Any]],
    candidate_mappings: list[CandidateProcedureMapping],
    cluster_results: list[ClusterMergeResult],
    failed: list[dict[str, Any]],
    output_path: Path,
    artifact_index: dict[str, dict[str, Any]],
    asset_link_cache: dict[str, str],
    review_base: Path,
) -> None:
    def _process(job: tuple[MergeCluster, bool, str, dict[str, Any]]) -> ClusterMergeResult:
        split_cluster, _auto_split, parent_id, packet = job
        source_runbooks = packet.get("finalized_runbooks") or []
        try:
            response = llm_client.merge(packet)
            decision = str(response.get("merge_decision") or "merged").strip()
            raw_runbooks = response.get("canonical_runbooks") or []
            if decision == "rejected" or not raw_runbooks:
                return ClusterMergeResult(
                    merge_cluster_id=parent_id or split_cluster.merge_cluster_id,
                    sub_cluster_id=split_cluster.merge_cluster_id,
                    merge_decision=decision or "rejected",
                    merged_from_procedure_ids=sorted(
                        str(item.get("procedure_id") or "") for item in source_runbooks
                    ),
                    conflicts=_string_list(response.get("conflicts")),
                    known_gaps=_string_list(response.get("known_gaps")),
                    merge_notes=_string_list(response.get("merge_notes")),
                    llm_used=True,
                )
            canonical_ids: list[str] = []
            for raw_runbook in raw_runbooks:
                if not isinstance(raw_runbook, dict):
                    continue
                normalized = normalize_merged_runbook(
                    raw_runbook,
                    source_runbooks=source_runbooks,
                    merge_cluster_id=parent_id or split_cluster.merge_cluster_id,
                    sub_cluster_id=split_cluster.merge_cluster_id,
                    merge_decision=decision,
                )
                errors = validate_canonical_runbook(normalized)
                if errors:
                    raise ValueError("; ".join(errors))
                canonical_runbooks.append(normalized)
                canonical_ids.append(str(normalized.get("procedure_id") or ""))
                write_review_file(
                    normalized,
                    review_base / safe_review_filename(str(normalized.get("procedure_id") or "")),
                    artifact_index=artifact_index,
                    asset_link_cache=asset_link_cache,
                )
                source_lookup = {
                    str(item.get("procedure_id") or ""): item for item in source_runbooks if str(item.get("procedure_id") or "")
                }
                for source_procedure_id in normalized.get("merged_from_procedure_ids") or []:
                    source_runbook = source_lookup.get(str(source_procedure_id))
                    if source_runbook is None:
                        continue
                    candidate_mappings.append(
                        CandidateProcedureMapping(
                            candidate_id=str(source_runbook.get("candidate_id") or ""),
                            canonical_procedure_id=str(normalized.get("procedure_id") or ""),
                            source_procedure_id=str(source_runbook.get("procedure_id") or ""),
                            merge_cluster_id=parent_id or split_cluster.merge_cluster_id,
                            merge_action=decision,
                            sub_cluster_id=split_cluster.merge_cluster_id,
                        )
                    )
            return ClusterMergeResult(
                merge_cluster_id=parent_id or split_cluster.merge_cluster_id,
                sub_cluster_id=split_cluster.merge_cluster_id,
                merge_decision=decision,
                canonical_procedure_ids=canonical_ids,
                merged_from_procedure_ids=sorted(str(item.get("procedure_id") or "") for item in source_runbooks),
                conflicts=_string_list(response.get("conflicts")),
                known_gaps=_string_list(response.get("known_gaps")),
                merge_notes=_string_list(response.get("merge_notes")),
                llm_used=True,
            )
        except Exception as exc:
            failed.append(
                {
                    "merge_cluster_id": split_cluster.merge_cluster_id,
                    "error": str(exc),
                }
            )
            return ClusterMergeResult(
                merge_cluster_id=parent_id or split_cluster.merge_cluster_id,
                sub_cluster_id=split_cluster.merge_cluster_id,
                merge_decision="failed",
                merged_from_procedure_ids=sorted(str(item.get("procedure_id") or "") for item in source_runbooks),
                llm_used=True,
                error=str(exc),
            )

    if max_workers <= 1 or len(jobs) <= 1:
        for job in jobs:
            cluster_results.append(_process(job))
        return

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_process, job): job for job in jobs}
        for future in as_completed(futures):
            cluster_results.append(future.result())


def _resolve_output_path(output_dir: Path) -> Path:
    if output_dir.name == STAGE7_DIR_NAME:
        return output_dir
    return output_dir / STAGE7_DIR_NAME


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]
