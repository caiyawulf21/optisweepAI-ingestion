from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DecisionOutcome(BaseModel):
    outcome_label: str
    descriptor: str = ""
    observable_signal: str = ""
    observer: str = ""
    tool_or_view: str = ""
    source: str = ""
    linked_runbook_id: str | None = None
    linked_step_number: int | None = None
    next_node_id: str | None = None


class NodeRetrievalSummary(BaseModel):
    node_id: str
    node_type: str
    title: str = ""
    intent: str = ""
    runbook_placeholder: str = ""
    expected_or_observed_result: str = ""
    allowed_roles: list[str] = Field(default_factory=list)
    required_evidence_concepts: list[str] = Field(default_factory=list)
    expects_capability: list[str] = Field(default_factory=list)
    expects_surface: list[str] = Field(default_factory=list)
    preferred_audience: list[str] = Field(default_factory=list)
    ontology_capabilities: list[dict[str, Any]] = Field(default_factory=list)
    backend_observability: list[dict[str, Any]] = Field(default_factory=list)
    ontology_gaps: list[str] = Field(default_factory=list)
    evidence_required: list[str] = Field(default_factory=list)
    healthy_indicators: list[str] = Field(default_factory=list)
    unhealthy_indicators: list[str] = Field(default_factory=list)
    inconclusive_indicators: list[str] = Field(default_factory=list)
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


class EvidenceCollectionProcedure(BaseModel):
    procedure_id: str
    title: str = ""
    purpose: str = ""
    role_required: str = ""
    audience_roles: list[str] = Field(default_factory=list)


class DiagnosticActionPlan(BaseModel):
    diagnostic_classification: str = "technical_diagnosis"
    primary_action: str = ""
    performed_by: str = ""
    primary_surface: str = ""
    optional_corroboration_surface: str = ""
    evidence_to_collect: list[str] = Field(default_factory=list)
    healthy_interpretation: str = ""
    unhealthy_interpretation: str = ""
    inconclusive_interpretation: str = ""
    optional_corroboration: list[dict[str, Any]] = Field(default_factory=list)
    linked_primary_procedure: dict[str, Any] | None = None
    generated_guidance: str = ""
    ontology_evidence: list[dict[str, Any]] = Field(default_factory=list)
    technical_field_mapping: dict[str, Any] = Field(default_factory=dict)
    runbook_execution_result: dict[str, Any] = Field(default_factory=dict)
    node_interpretation_mapping: dict[str, Any] = Field(default_factory=dict)
    confidence: str = "unresolved"
    requires_sme_review: bool = True
    query_mode: str = "none"
    evidence_retrieval_success: str = ""
    diagnostic_interpretation: str = ""


class PlaybookBranch(BaseModel):
    branch_id: str
    condition_label: str = ""
    condition_descriptor: str = ""
    outcome: str = ""
    next_node_id: str | None = None
    source_branch_hint_ids: list[str] = Field(default_factory=list)
    linked_runbook_step_ref: str | None = None
    source_refs: list[Any] = Field(default_factory=list)


class FinalizedNode(BaseModel):
    model_config = ConfigDict(extra="allow")

    node_id: str
    node_type: str
    purpose: str = ""
    diagnostic_reasoning: str = ""
    evidence_required: list[Any] = Field(default_factory=list)
    healthy_indicators: list[Any] = Field(default_factory=list)
    unhealthy_indicators: list[Any] = Field(default_factory=list)
    inconclusive_indicators: list[Any] = Field(default_factory=list)
    primary_action: str = ""
    performed_by: str = ""
    primary_surface: str = ""
    evidence_to_collect: list[str] = Field(default_factory=list)
    healthy_interpretation: str = ""
    unhealthy_interpretation: str = ""
    inconclusive_interpretation: str = ""
    diagnostic_classification: str = ""
    question: str = ""
    optional_corroboration_surface: str = ""
    optional_corroboration: list[dict[str, Any]] = Field(default_factory=list)
    linked_primary_procedure: dict[str, Any] | None = None
    generated_guidance: str = ""
    ontology_evidence: list[dict[str, Any]] = Field(default_factory=list)
    technical_field_mapping: dict[str, Any] = Field(default_factory=dict)
    runbook_execution_result: dict[str, Any] = Field(default_factory=dict)
    node_interpretation_mapping: dict[str, Any] = Field(default_factory=dict)
    trigger_condition: str = ""
    selected_procedure: dict[str, Any] | None = None
    selection_rationale: str = ""
    prerequisites: list[str] = Field(default_factory=list)
    safety_checks: list[str] = Field(default_factory=list)
    success_confirmation: str = ""
    failure_boundary: str = ""
    validation_checklist: list[str] = Field(default_factory=list)
    required_evidence_sources: list[str] = Field(default_factory=list)
    stable_operation_observation: str = ""
    escalation_reason: str = ""
    evidence_package: list[str] = Field(default_factory=list)
    actions_attempted: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    required_next_team: str = ""
    confidence: str = "unresolved"
    requires_sme_review: bool = True
    query_mode: str = "none"
    evidence_retrieval_success: str = ""
    diagnostic_interpretation: str = ""
    evidence_collection_procedures: list[EvidenceCollectionProcedure] = Field(default_factory=list)
    catalog_gaps: list[str] = Field(default_factory=list)
    resolved_runbook_ids: list[str] = Field(default_factory=list)
    runbook_links: list[RunbookLinkRecord] = Field(default_factory=list)
    decision_outcomes: list[DecisionOutcome] = Field(default_factory=list)
    branches: list[PlaybookBranch] = Field(default_factory=list)
    source_evidence: list[Any] = Field(default_factory=list)


class FinalizedPlaybook(BaseModel):
    model_config = ConfigDict(extra="allow")

    playbook_id: str
    case_id: str
    nodes: list[FinalizedNode] = Field(default_factory=list)
    branches: list[PlaybookBranch] = Field(default_factory=list)
    validation_status: str = "needs_sme_review"


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
    retrieval_mode: str = "semantic"
    embedding_model: str = ""
