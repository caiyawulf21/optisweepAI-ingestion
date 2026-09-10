from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from brain.schemas.common import ValidationStatus

# The set of statuses a context packet's `approved_knowledge` field is
# allowed to draw from. Anything else (OPERATIONAL_UNREVIEWED,
# NEEDS_SME_REVIEW, CONFLICTING, DEPRECATED) is Reconciliation/curation
# working material, never runtime-eligible guidance — the concrete
# mechanism closing the "nothing distinguishes governed knowledge from raw
# extraction" gap named repeatedly in AGENT_DESIGN_NOTES.md §4/§6.
APPROVED_KNOWLEDGE_STATUSES = frozenset(
    {ValidationStatus.CATALOG_AUTHORITATIVE, ValidationStatus.SME_APPROVED}
)


class ContextPacket(BaseModel):
    """The LLM-accessible working-memory packet a retrieval/context-building
    service assembles for one bounded call (design doc §8).

    Schema only — deferred per architecture lock §14 ("retrieval chunks,
    embeddings, ranking, and ContextPacket schema"). No retrieval
    implementation, ranking, or Cosmos query code exists yet; this defines
    the shape a future context-builder service must produce and every
    runtime/ingestion LLM call must consume, so downstream agent design
    (AGENT_DESIGN_NOTES.md §4.2/§10) has a concrete contract to target.

    Every list field here holds Brain record IDs (never inlined record
    content) — the packet is a bounded, cited pointer set, not a copy of
    the corpus. A consuming service resolves IDs to content immediately
    before the LLM call, keeping the packet itself small and audit-friendly
    (design doc §8: "packet sizes should be budgeted").
    """

    model_config = ConfigDict(extra="forbid")

    task: dict[str, Any]
    current_state: dict[str, Any] = Field(default_factory=dict)

    entities: list[str] = Field(default_factory=list)
    approved_knowledge: list[str] = Field(default_factory=list)
    evidence_excerpts: list[str] = Field(default_factory=list)
    relevant_incidents: list[str] = Field(default_factory=list)
    policies: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)

    required_output_schema: dict[str, Any] | None = None
