"""Intermediate shapes passed between the seven tools. These are NOT
BrainRecord types -- they are the LLM's structured proposals before a
record is actually constructed/validated/persisted. Keeping them loose
(dict payloads with a discriminator) rather than forcing the LLM to emit
a fully-typed Entity/Capability/etc. directly matches how AGENT_DESIGN_NOTES.md
§4.2 describes each tool: classify_candidate "proposes a record shape," it
does not have to emit the final validated record -- that happens once a
NEW_CANDIDATE decision is confirmed and validate_and_prepare_for_review
runs schema validation.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class EvidenceCandidate(BaseModel):
    """Tool 1 (extract_evidence) output: one bounded span plus a raw claim
    candidate. `evidence_unit` is a dict, not an EvidenceUnit instance,
    because the LLM does not have the corpus context to assign a final
    stable id (that happens once classify_candidate resolves it against
    existing entities) -- only content/locator/kind."""

    model_config = ConfigDict(extra="forbid")

    evidence_kind: str
    content_text: str
    is_verbatim: bool
    locator_hint: dict[str, Any] = Field(default_factory=dict)
    raw_claim_candidates: list[str] = Field(default_factory=list)


class ExtractEvidenceResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidates: list[EvidenceCandidate] = Field(default_factory=list)


class ClassifiedRecordKind(str, Enum):
    ENTITY = "entity"
    CAPABILITY = "capability"
    CLAIM = "claim"
    RELATIONSHIP = "relationship"
    ALREADY_EVIDENCE = "already_evidence"


class ClassifiedCandidate(BaseModel):
    """Tool 2 (classify_candidate) output. `proposed_fields` holds whatever
    fields the LLM judged for the target record type (e.g. entity_type/name/
    description for an Entity candidate, or subject_entity_id/predicate/
    object/polarity for a Claim candidate) -- validated into a real typed
    model only once reconcile_candidate confirms NEW_CANDIDATE and
    validate_and_prepare_for_review runs schema validation."""

    model_config = ConfigDict(extra="forbid")

    record_kind: ClassifiedRecordKind
    proposed_fields: dict[str, Any] = Field(default_factory=dict)
    confidence: Literal["low", "medium", "high"]
    rationale: str
    source_evidence_ids: list[str] = Field(default_factory=list)


class ReconciliationOutcome(str, Enum):
    REINFORCE = "reinforce"
    PATCH = "patch"
    CONFLICT = "conflict"
    GAP = "gap"
    NEW_CANDIDATE = "new_candidate"


class ReconciliationDecision(BaseModel):
    """Tool 3 (reconcile_candidate) output."""

    model_config = ConfigDict(extra="forbid")

    outcome: ReconciliationOutcome
    classified: ClassifiedCandidate
    affected_record_ids: list[str] = Field(default_factory=list)
    patch_fields: dict[str, Any] = Field(default_factory=dict)
    conflicts_with_claim_id: str | None = None
    rationale: str
    duplicate_check_performed: bool = False


class DraftedProcedureAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    exact_action: str
    role_entity_id: str | None = None


class DraftedProcedureStep(BaseModel):
    """Mirrors brain.schemas.procedure.ProcedureStep field-for-field --
    unlike ClassifiedCandidate's loose proposed_fields dict, a Procedure's
    target shape is already fully known (it is drafted FROM one specific
    Capability, not classified from an ambiguous raw candidate), so there
    is no benefit to a looser intermediate shape here. Kept as its own
    type rather than reusing ProcedureStep directly so a real LLM response
    that's missing/wrong on a field fails as a clear "drafted step" schema
    error, not a Procedure-construction error one layer removed from the
    LLM call that actually produced the bad value."""

    model_config = ConfigDict(extra="forbid")

    step_number: int
    title: str
    instruction: str
    responsible_role_entity_id: str | None = None
    supporting_role_entity_id: str | None = None
    purpose: str = ""
    expected_result: str = ""
    healthy_condition: str = ""
    failure_condition: str = ""
    stop_or_escalate_if: list[str] = Field(default_factory=list)
    actions: list[DraftedProcedureAction] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)


class DraftedProcedure(BaseModel):
    """draft_procedure's output -- the LLM's proposed Procedure content,
    before capability_id/role id existence is checked and the real,
    validated brain.schemas.procedure.Procedure is constructed (mirrors
    ClassifiedCandidate's proposed-then-validated-later split)."""

    model_config = ConfigDict(extra="forbid")

    title: str
    summary: str = ""
    when_to_use: list[str] = Field(default_factory=list)
    not_for: list[str] = Field(default_factory=list)
    allowed_role_entity_ids: list[str] = Field(default_factory=list)
    steps: list[DraftedProcedureStep] = Field(default_factory=list)
    rationale: str
    gaps: list[str] = Field(default_factory=list)


class DraftedPlaybookBranch(BaseModel):
    """Mirrors brain.schemas.playbook.PlaybookBranch field-for-field, same
    rationale as DraftedProcedureStep vs. ProcedureStep -- kept as its own
    type so a bad LLM response fails as a drafted-branch schema error, not
    a Playbook-construction error one layer removed."""

    model_config = ConfigDict(extra="forbid")

    outcome: str
    condition: str
    next_node_id: str | None = None
    source_refs: list[str] = Field(default_factory=list)


class DraftedPlaybookNode(BaseModel):
    """Mirrors brain.schemas.playbook.PlaybookNode field-for-field."""

    model_config = ConfigDict(extra="forbid")

    node_id: str
    node_order: int
    node_type: str
    title: str
    capability_id: str | None = None
    procedure_id: str | None = None
    symptom_entity_id: str | None = None
    intent: str = ""
    allowed_role_entity_ids: list[str] = Field(default_factory=list)
    stop_or_escalation_note: str = ""
    branches: list[DraftedPlaybookBranch] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)


class DraftedPlaybook(BaseModel):
    """draft_playbook's output -- the LLM's proposed Playbook content,
    before capability_id/procedure_id/symptom_entity_id existence is
    checked and the real, validated brain.schemas.playbook.Playbook is
    constructed. A Playbook never embeds a Procedure's steps -- nodes
    reference procedure_id only (schema docstring), so nothing here
    carries step content."""

    model_config = ConfigDict(extra="forbid")

    title: str
    playbook_goal: str = ""
    entry_symptom_entity_ids: list[str] = Field(default_factory=list)
    affected_entity_ids: list[str] = Field(default_factory=list)
    nodes: list[DraftedPlaybookNode] = Field(default_factory=list)
    entry_node_id: str | None = None
    confidence: str = "needs_review"
    rationale: str
    gaps: list[str] = Field(default_factory=list)
