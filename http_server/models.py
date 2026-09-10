"""Request/response models for the four appcode-facing HTTP routes
(OPTISWEEP_APP_BRAIN_HTTP_BOUNDARY.md, agreed 2026-09-09). Thin
pydantic wrappers only -- no business logic lives here, matching
mcp_server/tools.py's own "thin wrapper" discipline.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from brain.schemas.relationship import RelationshipType


# -- /brain/v1/context/retrieve ---------------------------------------------


class ContextRetrieveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_text: str
    entity_ids: list[str] = Field(default_factory=list)
    relationship_types: list[RelationshipType] | None = None
    hops: int = 1


# -- /brain/v1/context/troubleshoot ------------------------------------------


class TroubleshootRequest(BaseModel):
    """Session/node/signal-aware context -- distinct from a bare search
    query. `current_node_id`/`playbook_id` seed retrieval from wherever a
    live troubleshooting session actually is (e.g. a Playbook node's own
    `capability_id`/`procedure_id`/`symptom_entity_id`), and
    `observed_signals` are free-text observations the app has collected in
    this session so far (e.g. "AGV active error confirmed", "RMS shows
    normal") -- folded into the semantic query text, not treated as
    structured facts, since Brain has no schema for "signal" as its own
    concept."""

    model_config = ConfigDict(extra="forbid")

    session_id: str
    playbook_id: str | None = None
    current_node_id: str | None = None
    observed_signals: list[str] = Field(default_factory=list)
    entity_ids: list[str] = Field(default_factory=list)
    hops: int = 2  # troubleshooting sessions default to the §14.4 2-hop worked example, not retrieve's 1-hop default


class HydratedExcerptResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: str
    label: str  # "approved" | "working" | "conflict"
    validation_status: str
    text: str
    truncated: bool


class ContextResponse(BaseModel):
    """Shared response shape for both /context/retrieve and
    /context/troubleshoot -- the critical-response-rule shape: the
    original ID-only packet (for audit/citation) PLUS real hydrated
    excerpts, never ID-only alone."""

    model_config = ConfigDict(extra="forbid")

    task: dict[str, Any]
    excerpts: list[HydratedExcerptResponse]
    excerpt_count: int
    truncated_excerpt_count: int
    entity_ids: list[str]
    approved_knowledge_ids: list[str]


# -- /brain/v1/feedback -------------------------------------------------------


class FeedbackEvent(BaseModel):
    """Matches the appcode-side FeedbackEvent shape named in the HTTP
    boundary doc: session/interaction/sentiment/text/targets/image
    summaries. `targets` names what the feedback is ABOUT (a node id, a
    procedure id, a capability id, ...) -- not validated against the
    corpus here; extract_evidence/classify_candidate do that judgment."""

    model_config = ConfigDict(extra="forbid")

    session_id: str
    interaction_id: str
    sentiment: str | None = None
    text: str
    targets: list[str] = Field(default_factory=list)
    image_summaries: list[str] = Field(default_factory=list)


class FeedbackResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str  # "succeeded" | "needs_human_review" | "failed"
    detail: str = ""
    review_ids: list[str] = Field(default_factory=list)
    written_record_ids: list[str] = Field(default_factory=list)


# -- /brain/v1/reviews --------------------------------------------------------


class ReviewSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    kind: str
    check_name: str | None
    affected_record_ids: list[str]
    proposed_change: str
    status: str
    resolution: str | None
    resolved_by: str | None


class ReviewListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reviews: list[ReviewSummary]
    open_count: int


class ReviewResolveRequest(BaseModel):
    """SME approves or overrides a resolution for one BrainReview.
    `resolution` defaults to whatever resolve_audit_candidate (Tool 6)
    already proposed on the review if the SME doesn't override it --
    callers approving an agent-proposed MERGE typically omit this.
    `winner_record_id` is required for MERGE; `new_entity_type` is
    required for RETYPE (2026-09-10) -- both name the one extra piece of
    judgment an SME (or the agent's own proposed resolution) supplies
    beyond "this resolution kind is correct.\""""

    model_config = ConfigDict(extra="forbid")

    resolution: str | None = None
    winner_record_id: str | None = None
    new_entity_type: str | None = None


class ReviewResolveResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    review_id: str
    resolution: str
    applied: bool
    mutated_record_ids: list[str] = Field(default_factory=list)
    detail: str = ""
