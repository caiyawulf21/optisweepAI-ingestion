from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class NodeRetrievalSummary(BaseModel):
    node_id: str
    node_type: str
    title: str = ""
    intent: str = ""
    runbook_placeholder: str = ""
    expected_or_observed_result: str = ""
    allowed_roles: list[str] = Field(default_factory=list)
    retrieval_text: str = ""


class PlaybookRetrievalCard(BaseModel):
    playbook_id: str
    playbook_candidate_id: str
    case_id: str
    extraction_mode: str
    title: str = ""
    user_facing_summary: str = ""
    observed_entry_symptoms: list[str] = Field(default_factory=list)
    support_user_language_examples: list[str] = Field(default_factory=list)
    affected_systems_or_components: list[str] = Field(default_factory=list)
    node_retrieval_summaries: list[NodeRetrievalSummary] = Field(default_factory=list)
    retrieval_text: str = ""
    validation_status: str = "needs_sme_review"


class PlaybookRetrievalIndexEntry(BaseModel):
    entry_id: str
    entry_kind: str
    playbook_id: str
    node_id: str = ""
    embedding_model: str
    embedding_dimensions: int
    vector: list[float]
    retrieval_text_hash: str


class RunbookSearchMatch(BaseModel):
    procedure_id: str
    title: str = ""
    procedure_type: str = ""
    cosine_score: float
    jaccard_score: float
    combined_score: float
    preferred_incident_source: bool = False
    source_type: str = ""
    source_id: str = ""


class RunbookLinkRecord(BaseModel):
    procedure_id: str
    link_confidence: str
    link_rationale: str = ""
    match_gaps: list[str] = Field(default_factory=list)
    preferred_incident_source: bool = False
    link_rank: int = 1


class DecisionOutcome(BaseModel):
    outcome_label: str
    descriptor: str = ""
    observable_signal: str = ""
    source: str = ""
    linked_runbook_id: str = ""
    linked_step_number: int | None = None
    next_node_id: str = ""


class PlaybookBranch(BaseModel):
    branch_id: str
    condition_label: str = ""
    condition_descriptor: str = ""
    outcome: str = ""
    next_node_id: str = ""
    source_branch_hint_ids: list[str] = Field(default_factory=list)
    linked_runbook_step_ref: str = ""
    source_refs: list[Any] = Field(default_factory=list)


class PlaybookRunbookLinkRow(BaseModel):
    case_id: str
    playbook_id: str
    node_id: str
    procedure_id: str
    link_confidence: str
    link_rank: int
    extraction_mode: str


class VariantFinalizationReport(BaseModel):
    extraction_mode: str
    case_ids: list[str] = Field(default_factory=list)
    playbook_count: int = 0
    node_count: int = 0
    high_confidence_link_rate: float = 0.0
    high_confidence_link_count: int = 0
    medium_confidence_link_count: int = 0
    low_confidence_link_count: int = 0
    unresolved_link_count: int = 0
    multi_runbook_node_count: int = 0
    diagnostic_outcome_coverage: float = 0.0
    branch_graph_completeness: float = 0.0
    incident_source_preference_applied_count: int = 0
    duplicate_runbook_ref_count: int = 0
    warnings: list[str] = Field(default_factory=list)
    needs_graph_repair_playbook_ids: list[str] = Field(default_factory=list)


class Stage8BuildResult(BaseModel):
    stage: str = "stage_8_playbook_finalization"
    generated_at: str
    llm_used: bool = False
    case_ids: list[str] = Field(default_factory=list)
    playbook_count: int = 0
    variant_reports: list[VariantFinalizationReport] = Field(default_factory=list)
