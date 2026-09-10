from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from brain.schemas.common import BrainRecord, RecordType
from brain.id_generation import is_well_formed_id


class PlaybookNodeType(str, Enum):
    DIAGNOSTIC_DECISION = "diagnostic_decision"
    PROCEDURE_REFERENCE = "procedure_reference"
    VALIDATION_GATE = "validation_gate"
    ESCALATION_GATE = "escalation_gate"
    RECOVERY_PHASE_MARKER = "recovery_phase_marker"


class BranchOutcome(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    INCONCLUSIVE = "inconclusive"
    ESCALATE = "escalate"


class PlaybookBranch(BaseModel):
    """One edge out of a node: a named outcome routes to the next node (or
    ends the playbook, if next_node_id is None — e.g. a terminal escalate).

    Mirrors shared_pipeline_stages/stage_8's FinalizedNode.branches[] shape
    (see the "Runbook Pipeline Audit" artifact, 2026-09-02), governed as a
    Brain record field instead of per-incident LLM output: the condition
    must cite the evidence that supports it, the same way a Relationship or
    Claim must.
    """

    model_config = ConfigDict(extra="forbid")

    outcome: BranchOutcome
    condition: str
    next_node_id: str | None = None
    source_refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _branch_requires_source_refs(self) -> "PlaybookBranch":
        if not self.source_refs:
            raise ValueError(
                f"branch to outcome {self.outcome.value!r} has no source_refs — "
                "a branch condition must cite the evidence it was drafted from (Part 1 §1.2)"
            )
        return self


class PlaybookNode(BaseModel):
    """One node in a Playbook's decision graph.

    Deliberately thin on its own: a node does not carry its own
    observables/sql_field_notes/support_contract — those live on the
    Capability the node's `capability_id` points at (AGENT_DESIGN_NOTES.md
    §2's locked Entity/Capability boundary, and §5.1's correction that a
    Capability's own fields are the reusable, LLM-grounded source of truth,
    not something redrafted fresh per playbook node the way the pre-Brain
    pipeline's `technical_field_mapping` was). A diagnostic_decision node
    points at the Capability it invokes; that Capability's own VERIFIES/
    CONTROLS relationship (§2) is what names the state/symptom entity being
    branched on.
    """

    model_config = ConfigDict(extra="forbid")

    node_id: str
    node_order: int
    node_type: PlaybookNodeType
    title: str

    capability_id: str | None = None
    procedure_id: str | None = None
    symptom_entity_id: str | None = None

    intent: str = ""
    allowed_role_entity_ids: list[str] = Field(default_factory=list)
    stop_or_escalation_note: str = ""

    branches: list[PlaybookBranch] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _referenced_ids_well_formed(self) -> "PlaybookNode":
        if self.capability_id is not None and not is_well_formed_id(
            self.capability_id, expected_prefix="capability"
        ):
            raise ValueError(f"capability_id is not a well-formed capability ID: {self.capability_id!r}")
        if self.procedure_id is not None and not is_well_formed_id(
            self.procedure_id, expected_prefix="procedure"
        ):
            raise ValueError(f"procedure_id is not a well-formed procedure ID: {self.procedure_id!r}")
        if self.symptom_entity_id is not None and not is_well_formed_id(
            self.symptom_entity_id, expected_prefix="entity"
        ):
            raise ValueError(f"symptom_entity_id is not a well-formed entity ID: {self.symptom_entity_id!r}")
        for value in self.allowed_role_entity_ids:
            if not is_well_formed_id(value, expected_prefix="entity"):
                raise ValueError(f"allowed_role_entity_ids contains a malformed entity ID: {value!r}")
        return self

    @model_validator(mode="after")
    def _node_requires_source_refs(self) -> "PlaybookNode":
        if not self.source_refs:
            raise ValueError(
                f"node {self.node_id!r} has no source_refs — "
                "every node must cite the evidence it was drafted from (Part 1 §1.2)"
            )
        return self

    @model_validator(mode="after")
    def _procedure_reference_requires_procedure_id(self) -> "PlaybookNode":
        if self.node_type == PlaybookNodeType.PROCEDURE_REFERENCE and self.procedure_id is None:
            raise ValueError(f"node {self.node_id!r} is procedure_reference but has no procedure_id")
        return self


class Playbook(BrainRecord):
    """Symptom-driven branching logic that routes between Procedures. The
    playbook half of the pre-Brain Stage 5-11 pipeline
    (shared_pipeline_stages/stage_8, "playbook finalization"), rebuilt as a
    governed Brain record type per AGENT_DESIGN_NOTES.md §5.

    A Playbook never embeds a Procedure's steps — nodes reference
    Procedures by `procedure_id` only, matching the pre-Brain pipeline's own
    deliberate choice (shared_pipeline_stages/README.md: "Full runbook
    steps are resolved from the catalog... and are not embedded in the
    canonical playbook artifact").
    """

    type: RecordType = RecordType.PLAYBOOK

    title: str
    playbook_goal: str = ""

    entry_symptom_entity_ids: list[str] = Field(default_factory=list)
    affected_entity_ids: list[str] = Field(default_factory=list)

    nodes: list[PlaybookNode] = Field(default_factory=list)
    entry_node_id: str | None = None

    confidence: str = "needs_review"

    # validation_status now lives on BrainRecord (brain/schemas/common.py),
    # covering every record type per AGENT_DESIGN_NOTES.md §14 — not
    # duplicated here as a bespoke field.

    @model_validator(mode="after")
    def _entity_id_lists_well_formed(self) -> "Playbook":
        for field_name in ("entry_symptom_entity_ids", "affected_entity_ids"):
            for value in getattr(self, field_name):
                if not is_well_formed_id(value, expected_prefix="entity"):
                    raise ValueError(f"{field_name} contains a malformed entity ID: {value!r}")
        return self

    @model_validator(mode="after")
    def _entry_node_id_resolves(self) -> "Playbook":
        if self.entry_node_id is not None:
            node_ids = {n.node_id for n in self.nodes}
            if self.entry_node_id not in node_ids:
                raise ValueError(f"entry_node_id {self.entry_node_id!r} does not match any node in nodes[]")
        return self

    @model_validator(mode="after")
    def _node_ids_unique(self) -> "Playbook":
        node_ids = [n.node_id for n in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            dupes = {n for n in node_ids if node_ids.count(n) > 1}
            raise ValueError(f"duplicate node_id(s) within playbook: {sorted(dupes)}")
        return self

    @model_validator(mode="after")
    def _branch_targets_resolve_within_playbook(self) -> "Playbook":
        node_ids = {n.node_id for n in self.nodes}
        for node in self.nodes:
            for branch in node.branches:
                if branch.next_node_id is not None and branch.next_node_id not in node_ids:
                    raise ValueError(
                        f"node {node.node_id!r} has a branch to {branch.next_node_id!r}, "
                        "which is not a node_id in this playbook's nodes[]"
                    )
        return self

    @model_validator(mode="after")
    def _derived_record_requires_source_refs(self) -> "Playbook":
        if not self.source_refs:
            raise ValueError("playbook records require at least one source_refs entry (Part 1 §1.2)")
        return self
