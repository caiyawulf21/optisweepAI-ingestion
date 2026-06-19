"""Pydantic schemas for Stage 6 candidate pool output."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class CandidatePacket(BaseModel):
    candidate_id: str
    source_id: str
    source_type: str
    title: str
    candidate_goal: str
    likely_procedure_type: str = ""
    likely_role_required: str = ""
    ingestion_batch_id: str

    artifact_ids: list[str] = []
    related_context_ids: list[str] = []

    rough_steps: list[str] = []
    source_grounded_values: list[Any] = []

    source_refs: list[dict[str, Any]] = []
    evidence_source_refs: list[dict[str, Any]] = []


class CandidateCluster(BaseModel):
    candidate_cluster_id: str
    normalized_title: str
    candidate_count: int
    source_types: list[str]
    candidate_ids: list[str]
    candidate_packets: list[CandidatePacket]

    aggregate_artifact_ids: list[str]
    aggregate_context_ids: list[str]
    aggregate_source_refs: list[dict[str, Any]]

    stage7_notes: list[str]


class CandidatePool(BaseModel):
    candidate_pool_version: int = 1
    generated_at: str
    candidate_cluster_count: int
    candidate_clusters: list[CandidateCluster]
