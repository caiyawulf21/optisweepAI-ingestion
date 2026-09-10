from __future__ import annotations

from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

from brain.schemas.common import BrainRecord, RecordType
from brain.id_generation import is_well_formed_id


class Polarity(str, Enum):
    AFFIRMED = "affirmed"
    NEGATED = "negated"
    UNCERTAIN = "uncertain"
    CONFLICTING = "conflicting"


class EntityRefObject(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["entity_ref"] = "entity_ref"
    entity_id: str

    @model_validator(mode="after")
    def _entity_id_well_formed(self) -> "EntityRefObject":
        if not is_well_formed_id(self.entity_id, expected_prefix="entity"):
            raise ValueError(f"object.entity_id is malformed: {self.entity_id!r}")
        return self


class LiteralValueObject(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["literal"] = "literal"
    value: str | float | int | bool


ClaimObject = Union[EntityRefObject, LiteralValueObject]


class Claim(BrainRecord):
    type: RecordType = RecordType.CLAIM

    subject_entity_id: str
    predicate: str
    object: ClaimObject
    polarity: Polarity

    condition: str | None = None
    note: str = ""

    @model_validator(mode="after")
    def _subject_entity_id_well_formed(self) -> "Claim":
        if not is_well_formed_id(self.subject_entity_id, expected_prefix="entity"):
            raise ValueError(f"subject_entity_id is malformed: {self.subject_entity_id!r}")
        return self

    @model_validator(mode="after")
    def _derived_record_requires_source_refs(self) -> "Claim":
        if not self.source_refs:
            raise ValueError("claim records require at least one source_refs entry (Part 1 §1.2)")
        return self
