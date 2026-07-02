from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RetrievalCard(BaseModel):
    finalized_runbook_id: str
    candidate_id: str
    title: str
    summary: str = ""
    when_to_use: str = ""
    procedure_type: str = ""
    role_required: str = ""
    systems: list[str] = Field(default_factory=list)
    components: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    action_verbs: list[str] = Field(default_factory=list)
    step_summaries: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    failure_conditions: list[str] = Field(default_factory=list)
    source_candidate_ids: list[str] = Field(default_factory=list)
    source_id: str = ""
    source_type: str = ""
    validation_status: str = ""
    retrieval_text: str = ""
    source_path: str = ""


class RetrievalIndexEntry(BaseModel):
    finalized_runbook_id: str
    embedding_model: str
    embedding_dimensions: int
    vector: list[float]
    retrieval_text_hash: str


class PairwiseMatch(BaseModel):
    source_id: str
    target_id: str
    cosine_score: float
    jaccard_score: float
    combined_score: float
    opposing_actions_detected: bool = False
    metadata_warnings: list[str] = Field(default_factory=list)


class RunbookSimilarityEntry(BaseModel):
    finalized_runbook_id: str
    top_cross_source_matches: list[PairwiseMatch] = Field(default_factory=list)


class MergeCluster(BaseModel):
    merge_cluster_id: str
    finalized_runbook_ids: list[str]
    candidate_ids: list[str]
    source_types: list[str]
    similarity_score: float
    merge_hint: str
    requires_stage_7_llm: bool = True
    evidence_notes: list[str] = Field(default_factory=list)
    pairwise_matches: list[PairwiseMatch] = Field(default_factory=list)


class PassThroughRunbook(BaseModel):
    finalized_runbook_id: str
    candidate_id: str
    source_id: str
    source_type: str
    requires_stage_7_llm: bool = False
    pass_through_reason: str


class RunbookPoolEntry(BaseModel):
    finalized_runbook_id: str
    candidate_id: str
    title: str
    source_id: str
    source_type: str
    procedure_type: str = ""
    role_required: str = ""
    validation_status: str = ""
    source_path: str = ""
    source_lineage: list[dict[str, Any]] = Field(default_factory=list)


class ScoreDistribution(BaseModel):
    count: int = 0
    min: float | None = None
    max: float | None = None
    mean: float | None = None
    p50: float | None = None
    p95: float | None = None


class RunbookPoolReport(BaseModel):
    generated_at: str
    input_runbook_count: int
    merge_cluster_count: int
    pass_through_count: int
    embedding_model: str = ""
    embeddings_generated: int = 0
    embeddings_cached: int = 0
    config: dict[str, Any] = Field(default_factory=dict)
    cosine_distribution: ScoreDistribution = Field(default_factory=ScoreDistribution)
    jaccard_distribution: ScoreDistribution = Field(default_factory=ScoreDistribution)
    combined_distribution: ScoreDistribution = Field(default_factory=ScoreDistribution)
    top_cross_source_pairs: list[PairwiseMatch] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class RunbookPoolResult(BaseModel):
    runbook_pool_version: int = 1
    generated_at: str
    runbook_count: int
    merge_cluster_count: int
    pass_through_count: int
