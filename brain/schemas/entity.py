from __future__ import annotations

from enum import Enum
from typing import Any, Union

from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny, model_validator

from brain.id_generation import is_well_formed_id
from brain.schemas.common import BrainRecord, RecordType


class EntityType(str, Enum):
    SYSTEM = "system"
    COMPONENT = "component"
    SERVICE = "service"
    DATABASE = "database"
    DATABASE_TABLE = "database_table"
    UI_SCREEN = "ui_screen"
    METRIC = "metric"
    ALARM = "alarm"
    STATE = "state"
    SYMPTOM = "symptom"
    ROLE = "role"
    SYSTEM_ACTION = "system_action"


class KeyField(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    meaning: str


class VisibleField(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    meaning: str


class SystemPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operational_roles: list[str] = Field(default_factory=list)
    owned_domains: list[str] = Field(default_factory=list)
    health_surfaces: list[str] = Field(default_factory=list)


class DatabaseTablePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    database_name: str
    schema_name: str | None = None
    business_meanings: list[str] = Field(default_factory=list)
    key_fields: list[KeyField] = Field(default_factory=list)
    read_only: bool = True


class UiScreenPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    surface: str
    navigation_hint: list[str] = Field(default_factory=list)
    visible_fields: list[VisibleField] = Field(default_factory=list)
    artifact_ids: list[str] = Field(default_factory=list)


class SystemActionPayload(BaseModel):
    """A named thing the SYSTEM does when invoked — an API endpoint or
    command (GetAGVStatuses, OpenAllChutes) — never a human action
    (that's Capability) and never a persistent state (that's Entity
    state/symptom). See AGENT_DESIGN_NOTES.md §2's third-shape note and
    §11 for the boundary this payload encodes.

    invocation_kind stays a free string rather than an enum: the corpus's
    only source for it today (wcs_api_catalog.json's objects[].group —
    "system"/"agvs"/"totes") is a subject-matter grouping, not a stable
    technical taxonomy of invocation mechanisms, and forcing it into a
    small enum now would either lose real source vocabulary or invent
    categories the evidence doesn't support.
    """

    model_config = ConfigDict(extra="forbid")

    invocation_kind: str = ""
    access_surface_entity_ids: list[str] = Field(default_factory=list)
    mutates_state: bool | None = None

    @model_validator(mode="after")
    def _access_surface_entity_ids_well_formed(self) -> "SystemActionPayload":
        for entity_id in self.access_surface_entity_ids:
            if not is_well_formed_id(entity_id, expected_prefix="entity"):
                raise ValueError(f"access_surface_entity_ids contains a malformed entity ID: {entity_id!r}")
        return self


class EmptyPayload(BaseModel):
    """Placeholder payload for MVP entity types with no dedicated fields yet."""

    model_config = ConfigDict(extra="forbid")


# Entity types without a fully specified payload shape in Part 1 use EmptyPayload
# until a real need (and evidence) defines their fields.
PAYLOAD_MODEL_BY_ENTITY_TYPE: dict[EntityType, type[BaseModel]] = {
    EntityType.SYSTEM: SystemPayload,
    EntityType.DATABASE_TABLE: DatabaseTablePayload,
    EntityType.UI_SCREEN: UiScreenPayload,
    EntityType.COMPONENT: EmptyPayload,
    EntityType.SERVICE: EmptyPayload,
    EntityType.DATABASE: EmptyPayload,
    EntityType.METRIC: EmptyPayload,
    EntityType.ALARM: EmptyPayload,
    EntityType.STATE: EmptyPayload,
    EntityType.SYMPTOM: EmptyPayload,
    EntityType.ROLE: EmptyPayload,
    EntityType.SYSTEM_ACTION: SystemActionPayload,
}

EntityPayload = Union[
    SystemPayload,
    DatabaseTablePayload,
    UiScreenPayload,
    SystemActionPayload,
    EmptyPayload,
]


class Entity(BrainRecord):
    type: RecordType = RecordType.ENTITY

    entity_type: EntityType
    name: str
    description: str = ""
    aliases: list[str] = Field(default_factory=list)

    # SerializeAsAny: without it, pydantic's serializer tries each
    # EntityPayload Union member in declaration order against the runtime
    # object and warns when an earlier member (e.g. SystemPayload, whose
    # fields are all optional) "shape-matches" a DatabaseTablePayload/
    # UiScreenPayload instance before reaching the correct one — the dumped
    # data is unaffected, but the warning is real signal noise. SerializeAsAny
    # tells it to serialize using the object's actual runtime type instead of
    # walking the Union, which is what _validate_payload_against_declared_
    # entity_type below already guarantees is the correct one.
    payload: SerializeAsAny[EntityPayload] = Field(default_factory=EmptyPayload)

    @model_validator(mode="before")
    @classmethod
    def _validate_payload_against_declared_entity_type(cls, data: Any) -> Any:
        # pydantic's Union member selection would otherwise try each payload
        # model in declaration order and silently accept the first one whose
        # fields happen to fit (e.g. an empty dict validates against
        # SystemPayload, whose fields all have defaults) instead of the one
        # the record's own entity_type calls for. Resolving the payload model
        # from entity_type here, before Union validation ever runs, is what
        # makes a mismatched payload shape (Part 1 §5, §13) actually rejected.
        if isinstance(data, dict):
            entity_type = data.get("entity_type")
            payload = data.get("payload", {})
            if entity_type is not None and isinstance(payload, dict):
                try:
                    resolved_type = EntityType(entity_type)
                except ValueError:
                    return data
                expected_model = PAYLOAD_MODEL_BY_ENTITY_TYPE[resolved_type]
                data = {**data, "payload": expected_model.model_validate(payload)}
        return data
