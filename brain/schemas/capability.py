from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from brain.schemas.common import BrainRecord, RecordType
from brain.id_generation import is_well_formed_id


class CapabilityKind(str, Enum):
    DIAGNOSTIC = "diagnostic"
    VERIFICATION = "verification"
    RECOVERY = "recovery"
    OPERATION = "operation"
    REFERENCE = "reference"


class SqlFieldNote(BaseModel):
    """One SQL field this capability reads, and why it matters.

    Mirrors docs/ontology/catalogs capability cards' field_highlights /
    sql_model_links[].purpose — the field-level "why", not just which table.
    """

    model_config = ConfigDict(extra="forbid")

    database_entity_id: str | None = None
    table_entity_id: str | None = None
    field: str
    purpose: str = ""

    @model_validator(mode="after")
    def _entity_ids_well_formed(self) -> "SqlFieldNote":
        for field_name in ("database_entity_id", "table_entity_id"):
            value = getattr(self, field_name)
            if value is not None and not is_well_formed_id(value, expected_prefix="entity"):
                raise ValueError(f"{field_name} is not a well-formed entity ID: {value!r}")
        return self


class Observables(BaseModel):
    """Signals that indicate whether the checked state is healthy, degraded,
    or requires escalation. Free text, since these are read off a screen or
    query result by a human, not a machine-checkable predicate (Part 1 does
    not model runtime evaluation)."""

    model_config = ConfigDict(extra="forbid")

    healthy: list[str] = Field(default_factory=list)
    degraded: list[str] = Field(default_factory=list)
    escalate: list[str] = Field(default_factory=list)


class SupportContract(BaseModel):
    """The ground-truth diagnostic/control boundary for this capability —
    which surfaces are read-only diagnostic sources vs. which can take
    action, and which other capabilities are explicitly off-limits here.
    This is exactly the "SQL required for state verification" /
    "no restart before health checks" kind of policy the architecture lock
    (Part 1, and the OptiSweep Brain design doc §11) says must be governed
    knowledge rather than a recurring prompt instruction.
    """

    model_config = ConfigDict(extra="forbid")

    diagnostic_surface_entity_ids: list[str] = Field(default_factory=list)
    control_surface_entity_ids: list[str] = Field(default_factory=list)
    required_evidence_capability_ids: list[str] = Field(default_factory=list)
    forbidden_capability_ids: list[str] = Field(default_factory=list)
    preferred_surface_entity_id: str | None = None

    @model_validator(mode="after")
    def _ids_well_formed(self) -> "SupportContract":
        for field_name in ("diagnostic_surface_entity_ids", "control_surface_entity_ids"):
            for value in getattr(self, field_name):
                if not is_well_formed_id(value, expected_prefix="entity"):
                    raise ValueError(f"{field_name} contains a malformed entity ID: {value!r}")
        for field_name in ("required_evidence_capability_ids", "forbidden_capability_ids"):
            for value in getattr(self, field_name):
                if not is_well_formed_id(value, expected_prefix="capability"):
                    raise ValueError(f"{field_name} contains a malformed capability ID: {value!r}")
        if self.preferred_surface_entity_id is not None and not is_well_formed_id(
            self.preferred_surface_entity_id, expected_prefix="entity"
        ):
            raise ValueError(
                f"preferred_surface_entity_id is not a well-formed entity ID: {self.preferred_surface_entity_id!r}"
            )
        return self


class RolePathGuidance(BaseModel):
    """Per-role how this capability is used — the catalog role_paths text.

    required_role_ids only answers *who may* touch the capability. role_paths
    answers *how each role is expected to act* (e.g. operator uses RMS only;
    L2 may open SSMS). Executable SSMS/query steps stay on Procedure records;
    this field carries the policy/guidance sentence itself.
    """

    model_config = ConfigDict(extra="forbid")

    role_entity_id: str
    guidance: str

    @model_validator(mode="after")
    def _role_entity_id_well_formed(self) -> "RolePathGuidance":
        if not is_well_formed_id(self.role_entity_id, expected_prefix="entity"):
            raise ValueError(f"role_entity_id is not a well-formed entity ID: {self.role_entity_id!r}")
        if not self.guidance.strip():
            raise ValueError("role path guidance must be non-empty")
        return self


class Capability(BrainRecord):
    type: RecordType = RecordType.CAPABILITY

    name: str
    description: str = ""
    capability_kind: CapabilityKind

    # When to reach for this capability vs. a similar one — dropping this
    # was the single biggest loss found migrating docs/ontology/catalogs/
    # capability cards; it is the operational judgment call a capability
    # exists to support, not incidental detail.
    when_to_use: list[str] = Field(default_factory=list)
    not_for: list[str] = Field(default_factory=list)

    target_entity_ids: list[str] = Field(default_factory=list)
    allowed_surface_entity_ids: list[str] = Field(default_factory=list)
    required_role_ids: list[str] = Field(default_factory=list)
    role_paths: list[RolePathGuidance] = Field(default_factory=list)

    sql_field_notes: list[SqlFieldNote] = Field(default_factory=list)
    api_checks: list[str] = Field(default_factory=list)
    observables: Observables = Field(default_factory=Observables)
    support_contract: SupportContract | None = None

    @model_validator(mode="after")
    def _entity_ids_well_formed(self) -> "Capability":
        for field_name in ("target_entity_ids", "allowed_surface_entity_ids", "required_role_ids"):
            for entity_id in getattr(self, field_name):
                if not is_well_formed_id(entity_id, expected_prefix="entity"):
                    raise ValueError(f"{field_name} contains a malformed entity ID: {entity_id!r}")
        return self
