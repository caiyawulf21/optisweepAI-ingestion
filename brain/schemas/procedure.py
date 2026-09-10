from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from brain.schemas.capability import CapabilityKind
from brain.schemas.common import BrainRecord, RecordType
from brain.id_generation import is_well_formed_id


class ProcedureAction(BaseModel):
    """One concrete action within a step — the literal thing a person does
    (a button pressed, a command sent, a query run), not the step's prose
    description of it. Mirrors the pre-Brain pipeline's step.actions[]
    shape (see BRAIN_BUILD_PROCESS.md / AGENT_DESIGN_NOTES.md §5 audit)."""

    model_config = ConfigDict(extra="forbid")

    label: str
    exact_action: str
    role_entity_id: str | None = None

    @model_validator(mode="after")
    def _role_entity_id_well_formed(self) -> "ProcedureAction":
        if self.role_entity_id is not None and not is_well_formed_id(
            self.role_entity_id, expected_prefix="entity"
        ):
            raise ValueError(f"role_entity_id is not a well-formed entity ID: {self.role_entity_id!r}")
        return self


class ProcedureStep(BaseModel):
    """One step in a Procedure's linear sequence. No branching lives here —
    branching is a Playbook-level concept (Part 1 does not model runtime
    evaluation; a Procedure is a straight sequence a human works through).

    healthy_condition / failure_condition are the per-step observable
    outcome — the Procedure-level analog of a Capability's `observables`,
    scoped to this one step rather than the capability as a whole.
    """

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

    actions: list[ProcedureAction] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _role_entity_ids_well_formed(self) -> "ProcedureStep":
        for field_name in ("responsible_role_entity_id", "supporting_role_entity_id"):
            value = getattr(self, field_name)
            if value is not None and not is_well_formed_id(value, expected_prefix="entity"):
                raise ValueError(f"{field_name} is not a well-formed entity ID: {value!r}")
        return self

    @model_validator(mode="after")
    def _step_requires_source_refs(self) -> "ProcedureStep":
        if not self.source_refs:
            raise ValueError(
                f"step {self.step_number} ({self.title!r}) has no source_refs — "
                "every step must cite the evidence it was drafted from (Part 1 §1.2)"
            )
        return self


class Procedure(BrainRecord):
    """A linear, human-executable sequence for diagnosing, verifying, or
    acting on ONE Capability. The runbook/procedure half of the pre-Brain
    Stage 5-11 pipeline (shared_pipeline_stages/), rebuilt as a governed
    Brain record type per AGENT_DESIGN_NOTES.md §5.

    A Procedure exists to carry out its `capability_id` — it does not
    duplicate the Capability's own `observables`/`support_contract`/
    `sql_field_notes`; it REFERENCES that Capability and cites the specific
    evidence (source_refs, per-step) that grounds each concrete action.
    Multiple Procedures may exist for one Capability (e.g. drawn from
    different operational sources or incidents) — see AGENT_DESIGN_NOTES.md
    §5.2 on why runbooks are not incident-only, and §6's open question on
    whether/how those get reconciled into one canonical Procedure the way
    the pre-Brain pipeline's Stage 6.5/7 does today.
    """

    type: RecordType = RecordType.PROCEDURE

    capability_id: str
    procedure_type: CapabilityKind
    title: str
    summary: str = ""

    when_to_use: list[str] = Field(default_factory=list)
    not_for: list[str] = Field(default_factory=list)
    allowed_role_entity_ids: list[str] = Field(default_factory=list)

    steps: list[ProcedureStep] = Field(default_factory=list)

    # validation_status now lives on BrainRecord (brain/schemas/common.py),
    # covering every record type per AGENT_DESIGN_NOTES.md §14 — not
    # duplicated here as a bespoke field.

    @model_validator(mode="after")
    def _capability_id_well_formed(self) -> "Procedure":
        if not is_well_formed_id(self.capability_id, expected_prefix="capability"):
            raise ValueError(f"capability_id is not a well-formed capability ID: {self.capability_id!r}")
        return self

    @model_validator(mode="after")
    def _allowed_role_entity_ids_well_formed(self) -> "Procedure":
        for value in self.allowed_role_entity_ids:
            if not is_well_formed_id(value, expected_prefix="entity"):
                raise ValueError(f"allowed_role_entity_ids contains a malformed entity ID: {value!r}")
        return self

    @model_validator(mode="after")
    def _steps_numbered_sequentially(self) -> "Procedure":
        expected = list(range(1, len(self.steps) + 1))
        actual = [s.step_number for s in self.steps]
        if actual != expected:
            raise ValueError(f"steps must be numbered sequentially starting at 1, got {actual}")
        return self

    @model_validator(mode="after")
    def _derived_record_requires_source_refs(self) -> "Procedure":
        if not self.source_refs:
            raise ValueError("procedure records require at least one source_refs entry (Part 1 §1.2)")
        return self
