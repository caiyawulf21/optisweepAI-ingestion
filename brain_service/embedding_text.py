"""Builds the text representation embedded per Brain record type, for
semantic retrieval (brain_service/retrieval.py). One function per type so
each record's most search-relevant fields are chosen deliberately rather
than dumping the whole model_dump() into the embedding call.
"""

from __future__ import annotations

from brain.schemas.capability import Capability
from brain.schemas.claim import Claim, EntityRefObject, LiteralValueObject
from brain.schemas.entity import Entity
from brain.schemas.evidence_unit import EvidenceUnit
from brain.schemas.playbook import Playbook
from brain.schemas.procedure import Procedure
from brain.schemas.relationship import Relationship
from brain.schemas.review import BrainReview
from brain.validators import BrainRecordUnion


def embedding_text_for(record: BrainRecordUnion) -> str:
    if isinstance(record, Entity):
        return " | ".join(filter(None, [record.name, *record.aliases, record.description]))
    if isinstance(record, Claim):
        if isinstance(record.object, LiteralValueObject):
            object_text = str(record.object.value)
        elif isinstance(record.object, EntityRefObject):
            object_text = record.object.entity_id
        else:
            object_text = ""
        return " | ".join(filter(None, [record.subject_entity_id, record.predicate, object_text, record.note]))
    if isinstance(record, EvidenceUnit):
        return record.content.text or ""
    if isinstance(record, Capability):
        return " | ".join(filter(None, [record.name, record.description]))
    if isinstance(record, Procedure):
        return " | ".join(filter(None, [record.title, record.summary, *record.when_to_use]))
    if isinstance(record, Playbook):
        return " | ".join(filter(None, [record.title, record.playbook_goal]))
    if isinstance(record, Relationship):
        return " | ".join(filter(None, [record.from_id, record.relationship_type.value, record.to_id, record.note]))
    if isinstance(record, BrainReview):
        return record.proposed_change or record.check_name or ""
    raise TypeError(f"No embedding text rule for record type {type(record)!r}")
