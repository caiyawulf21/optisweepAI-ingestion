from __future__ import annotations

from enum import Enum

from pydantic import model_validator

from brain.schemas.common import BrainRecord, RecordType
from brain.id_generation import is_well_formed_id


class RelationshipType(str, Enum):
    CONTAINS = "contains"
    CONTROLS = "controls"
    COMMUNICATES_WITH = "communicates_with"
    DEPENDS_ON = "depends_on"
    DISPLAYS = "displays"
    OBSERVES = "observes"
    VERIFIES = "verifies"
    USES = "uses"
    SUPPORTS = "supports"
    AFFECTS = "affects"
    MAY_INDICATE = "may_indicate"
    CAUSES = "causes"
    CONTRIBUTES_TO = "contributes_to"
    REQUIRES = "requires"
    APPLIES_TO = "applies_to"


class Relationship(BrainRecord):
    type: RecordType = RecordType.RELATIONSHIP

    from_id: str
    relationship_type: RelationshipType
    to_id: str

    note: str = ""

    @model_validator(mode="after")
    def _endpoints_well_formed(self) -> "Relationship":
        for field_name in ("from_id", "to_id"):
            value = getattr(self, field_name)
            if not is_well_formed_id(value):
                raise ValueError(f"{field_name} is not a well-formed typed ID: {value!r}")
        return self

    @model_validator(mode="after")
    def _derived_record_requires_source_refs(self) -> "Relationship":
        if not self.source_refs:
            raise ValueError("relationship records require at least one source_refs entry (Part 1 §1.2)")
        return self
