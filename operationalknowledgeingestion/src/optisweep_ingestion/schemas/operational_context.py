"""Pydantic schema for operational context records."""

from __future__ import annotations

from pydantic import BaseModel, field_validator

ALLOWED_CONTEXT_TYPES = {
    "system_overview",
    "component_reference",
    "hmi_screen_reference",
    "hmi_metric_reference",
    "alarm_reference",
    "status_reference",
    "role_or_access_reference",
    "safety_reference",
    "glossary",
    "troubleshooting_reference",
    "operation_reference",
    "maintenance_reference",
}

FORBIDDEN_FIELDS = {
    "trigger_conditions",
    "workflow_branch",
    "decision_node",
    "ml_label",
    "routing_key",
    "procedure_steps",
    "runbook_steps",
    "commands",
    "next_step_on_success",
    "next_step_on_failure",
}


class OperationalContext(BaseModel):
    context_id: str
    title: str
    context_type: str
    summary: str
    details: str
    applies_to: list[str] = []
    key_terms: list[str] = []
    related_artifact_ids: list[str] = []
    image_refs: list[str] = []
    related_runbook_candidate_ids: list[str] = []
    source_id: str
    source_type: str
    source_title: str | None = None
    ingestion_batch_id: str
    source_refs: list[dict] = []
    retrieval_text: str
    validation_status: str = "needs_review"
    metadata: dict = {}

    @field_validator("context_type")
    @classmethod
    def check_context_type(cls, v: str) -> str:
        if v not in ALLOWED_CONTEXT_TYPES:
            raise ValueError(f"context_type '{v}' is not allowed. Must be one of: {sorted(ALLOWED_CONTEXT_TYPES)}")
        return v

    @field_validator("context_id", "title", "summary", "details", "retrieval_text")
    @classmethod
    def check_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field must not be empty.")
        return v

    @field_validator("source_refs")
    @classmethod
    def check_source_refs_not_empty(cls, v: list[dict]) -> list[dict]:
        if not v:
            raise ValueError("source_refs must contain at least one entry.")
        return v
