from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MergeSubCluster(BaseModel):
    sub_cluster_id: str
    parent_cluster_id: str
    finalized_runbook_ids: list[str]
    candidate_ids: list[str]
    source_types: list[str]
    similarity_score: float
    merge_hint: str
    auto_split: bool = False


class MergePacket(BaseModel):
    merge_cluster_id: str
    sub_cluster_id: str
    merge_hint: str
    similarity_score: float
    evidence_notes: list[str] = Field(default_factory=list)
    pairwise_matches: list[dict[str, Any]] = Field(default_factory=list)
    finalized_runbooks: list[dict[str, Any]] = Field(default_factory=list)
    existing_canonical_runbook: dict[str, Any] | None = None
    auto_split: bool = False
    parent_cluster_id: str = ""


class ClusterMergeResult(BaseModel):
    merge_cluster_id: str
    sub_cluster_id: str
    merge_decision: str
    canonical_procedure_ids: list[str] = Field(default_factory=list)
    merged_from_procedure_ids: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)
    known_gaps: list[str] = Field(default_factory=list)
    merge_notes: list[str] = Field(default_factory=list)
    llm_used: bool = False
    error: str = ""


class CandidateProcedureMapping(BaseModel):
    candidate_id: str
    canonical_procedure_id: str
    source_procedure_id: str
    merge_cluster_id: str = ""
    merge_action: str
    sub_cluster_id: str = ""


class Stage7BuildResult(BaseModel):
    stage_7_version: int = 1
    generated_at: str
    canonical_runbook_count: int
    pass_through_count: int
    merge_cluster_count: int
    sub_cluster_count: int
    llm_merge_count: int
