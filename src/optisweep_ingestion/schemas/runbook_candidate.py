"""Pydantic schema for Stage 5 runbook candidates."""

from __future__ import annotations

from pydantic import BaseModel, field_validator


ALLOWED_PROCEDURE_TYPES = {"operation", "diagnostic", "recovery", "reference"}
ALLOWED_ROLES = {"operator", "L1_support", "L2_support", "L3_support"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
FORBIDDEN_FIELDS = {
    "trigger_conditions",
    "candidate_input_signals",
    "produces_signals",
    "resolved_signals",
    "workflow_branch",
    "decision_node",
    "ml_label",
    "routing_key",
    "next_step_on_success",
    "next_step_on_failure",
    "workflow_id",
    "workflow_step_id",
}


class RunbookCandidate(BaseModel):
    candidate_id: str
    title: str
    candidate_goal: str
    likely_procedure_type: str
    likely_role_required: str
    support_safe: bool | None = None
    summary: str

    rough_steps: list[str] = []
    expected_result: str | None = None
    failure_or_escalation_notes: list[str] = []

    access_or_tools_needed: list[str] = []
    related_context_ids: list[str] = []
    related_artifact_ids: list[str] = []
    source_refs: list[dict] = []
    evidence_source_refs: list[dict] = []

    source_id: str
    source_type: str
    source_title: str | None = None
    source_version: str | None = None
    ingestion_batch_id: str

    confidence: str = "medium"
    candidate_status: str = "needs_review"
    extraction_notes: list[str] = []
    metadata: dict = {}

    @field_validator("likely_procedure_type")
    @classmethod
    def check_procedure_type(cls, value: str) -> str:
        if value not in ALLOWED_PROCEDURE_TYPES:
            raise ValueError(f"Unsupported likely_procedure_type: {value}")
        return value

    @field_validator("likely_role_required")
    @classmethod
    def check_role(cls, value: str) -> str:
        if value not in ALLOWED_ROLES:
            raise ValueError(f"Unsupported likely_role_required: {value}")
        return value

    @field_validator("confidence")
    @classmethod
    def check_confidence(cls, value: str) -> str:
        if value not in ALLOWED_CONFIDENCE:
            raise ValueError(f"Unsupported confidence: {value}")
        return value
