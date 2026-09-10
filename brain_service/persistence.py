"""Applies a validated ReconciliationDecision to storage -- the write step
that was missing between validate_and_prepare_for_review (drafts a
BrainReview describing the proposed change) and an actual corpus update.

Write model (2026-09-09, user-directed): everything gets written, always.
`validation_status` -- not "written vs. not written" -- is the safety
signal. Every write from this module lands as
ValidationStatus.OPERATIONAL_UNREVIEWED (or CONFLICTING for the Conflict
branch), which already keeps it out of ContextPacket.approved_knowledge
(brain/schemas/context_packet.py's APPROVED_KNOWLEDGE_STATUSES) until an
SME flips it to SME_APPROVED. GAP is the one outcome with nothing to
write -- it names something missing, not a record to create.

This does NOT replace validate_and_prepare_for_review's BrainReview --
apply_reconciliation() calls it first and still saves the review (the
audit trail of what changed and why), then performs the actual write on
top of it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from brain.id_generation import claim_id, entity_id, is_well_formed_id, make_id
from brain.migration.merge import merge_record
from brain.schemas.capability import Capability, CapabilityKind
from brain.schemas.claim import Claim, EntityRefObject, LiteralValueObject, Polarity
from brain.schemas.common import ValidationStatus
from brain.schemas.entity import PAYLOAD_MODEL_BY_ENTITY_TYPE, Entity, EntityType
from brain.schemas.relationship import Relationship, RelationshipType
from brain.schemas.review import BrainReview
from brain.validators import BrainRecordUnion
from brain_service.types import ClassifiedRecordKind, ReconciliationDecision, ReconciliationOutcome
from brain_service.validation import validate_and_prepare_for_review
from providers.storage import StorageProvider


@dataclass
class ApplyResult:
    review: BrainReview
    written_record: BrainRecordUnion | None = None
    skipped_reason: str | None = None


def apply_reconciliation(
    storage: StorageProvider,
    reconciled: ReconciliationDecision,
    *,
    scope: str,
) -> ApplyResult:
    """Runs validate_and_prepare_for_review (always -- the audit trail is
    never skipped), then performs the actual write for every outcome
    except Gap. Returns the review plus whatever record was written (or
    None for Gap, or for a mechanical validation failure that blocked the
    write)."""
    review = validate_and_prepare_for_review(storage, reconciled)

    if "VALIDATION FAILED" in review.proposed_change:
        storage.save_brain_records([review], scope=scope)
        return ApplyResult(review=review, skipped_reason=review.proposed_change)

    if reconciled.outcome == ReconciliationOutcome.GAP:
        storage.save_brain_records([review], scope=scope)
        return ApplyResult(review=review, skipped_reason="GAP has no record to write")

    try:
        written = _write_for_outcome(storage, reconciled, scope=scope)
    except (UnresolvedClaimSubjectError, DanglingReferenceError) as exc:
        # Both are real, expected outcomes (the LLM proposed a record
        # referencing an entity that doesn't exist yet -- either
        # explicitly unresolved, per UnresolvedClaimSubjectError, or
        # merely well-formed-looking but nonexistent, per
        # DanglingReferenceError) -- surfaced as a clear next action for a
        # human ("create this Entity first"), not a generic write failure
        # that reads like a bug.
        needs_entity_review = review.model_copy(
            update={
                "proposed_change": (
                    f"{review.proposed_change} NEEDS ENTITY FIRST: {exc}"
                )
            }
        )
        storage.save_brain_records([needs_entity_review], scope=scope)
        return ApplyResult(review=needs_entity_review, skipped_reason=str(exc))
    except Exception as exc:  # noqa: BLE001 -- a construction/write failure must not be silent
        failure_review = review.model_copy(
            update={"proposed_change": f"{review.proposed_change} WRITE FAILED: {exc}"}
        )
        storage.save_brain_records([failure_review], scope=scope)
        return ApplyResult(review=failure_review, skipped_reason=str(exc))

    storage.save_brain_records([review], scope=scope)
    return ApplyResult(review=review, written_record=written)


def _write_for_outcome(
    storage: StorageProvider, reconciled: ReconciliationDecision, *, scope: str
) -> BrainRecordUnion:
    if reconciled.outcome in (ReconciliationOutcome.REINFORCE, ReconciliationOutcome.PATCH):
        return _apply_merge(storage, reconciled, scope=scope)
    if reconciled.outcome == ReconciliationOutcome.NEW_CANDIDATE:
        return _create_new_record(storage, reconciled, scope=scope)
    if reconciled.outcome == ReconciliationOutcome.CONFLICT:
        return _create_conflicting_claim(storage, reconciled, scope=scope)
    raise ValueError(f"No write rule for outcome {reconciled.outcome!r}")


def _apply_merge(storage: StorageProvider, reconciled: ReconciliationDecision, *, scope: str) -> BrainRecordUnion:
    if not reconciled.affected_record_ids:
        raise ValueError("REINFORCE/PATCH requires at least one affected_record_id to merge into")
    target_id = reconciled.affected_record_ids[0]
    existing_records = {r.id: r for r in storage.load_brain_context()}
    if target_id not in existing_records:
        # In practice apply_reconciliation() always runs
        # validate_and_prepare_for_review() first, which already rejects a
        # dangling affected_record_id before this function is ever called --
        # this check is deliberate defense-in-depth against a future caller
        # skipping that step, not a path exercised in the normal chain.
        raise ValueError(f"affected_record_id {target_id!r} does not resolve to an existing record")

    existing = existing_records[target_id]
    incoming_fields = dict(reconciled.patch_fields)
    # REINFORCE with no explicit patch_fields still adds the new citation --
    # that IS the reinforcement, even when nothing else about the record
    # changes.
    incoming_fields.setdefault("source_refs", list(reconciled.classified.source_evidence_ids))

    merged = merge_record(existing, incoming_fields)

    # A merge must write back to the TARGET record's own existing scope,
    # never the scope of whatever new material triggered the merge -- a
    # real bug found testing this live (2026-09-09): patching a shared
    # ontology_catalogs Capability while ingesting an unrelated incident
    # scope silently wrote a SECOND, divergent copy into the incident's
    # scope, leaving the real record in ontology_catalogs untouched. The
    # caller-supplied `scope` is only the right answer if the target
    # record happens to already live there; find_scope_for_record() is
    # the actual source of truth.
    home_scope = storage.find_scope_for_record(target_id) or scope
    storage.save_brain_records([merged], scope=home_scope)
    return merged


class DanglingReferenceError(ValueError):
    """Raised when a NEW_CANDIDATE record's own payload-embedded id
    reference(s) (Relationship.from_id/to_id, Claim.subject_entity_id or
    an entity_ref object, Capability.target_entity_ids/etc.) point at an
    entity id that is well-FORMED but does not actually exist in the
    corpus. _build_*()'s id-format checks (is_well_formed_id) only ever
    confirmed the id LOOKS like "entity:type:name" -- they never checked
    it resolves to a real record, so a plausible-but-invented id
    previously wrote silently. Found by direct testing (not caught by any
    prior test in this codebase): a Relationship between two nonexistent
    entities, and a Claim about a nonexistent subject, both wrote without
    error before this check existed. validate_batch() (brain/validators.py)
    already has the equivalent check for a full corpus; this applies the
    same check to one not-yet-written record before it's saved, since
    validate_and_prepare_for_review's own dangling check only covers
    `affected_record_ids`, which is empty for NEW_CANDIDATE by
    definition (nothing existing is "affected" by a brand-new record)."""

    def __init__(self, record_kind: str, dangling_ids: list[str]) -> None:
        self.dangling_ids = dangling_ids
        super().__init__(
            f"{record_kind} references entity id(s) not found in the corpus: {dangling_ids} -- "
            "create the referenced Entity/Entities first (as their own NEW_CANDIDATE)."
        )


def _referenced_entity_ids(record_kind: ClassifiedRecordKind, fields: dict[str, Any]) -> list[str]:
    """Every id-shaped field a NEW_CANDIDATE record of this kind embeds,
    that must resolve to an EXISTING entity (the record kind's own id is
    never included here -- that's the new record itself, not a reference)."""
    if record_kind == ClassifiedRecordKind.RELATIONSHIP:
        return [fields.get("from_id"), fields.get("to_id")]
    if record_kind == ClassifiedRecordKind.CLAIM:
        ids = [fields.get("subject_entity_id")]
        object_field = fields.get("object")
        if isinstance(object_field, dict) and object_field.get("kind") == "entity_ref":
            ids.append(object_field.get("entity_id"))
        return ids
    if record_kind == ClassifiedRecordKind.CAPABILITY:
        return [
            *fields.get("target_entity_ids", []),
            *fields.get("allowed_surface_entity_ids", []),
            *fields.get("required_role_ids", []),
        ]
    return []


def _create_new_record(
    storage: StorageProvider, reconciled: ReconciliationDecision, *, scope: str
) -> BrainRecordUnion:
    classified = reconciled.classified
    fields = dict(classified.proposed_fields)
    common = {
        "source_refs": list(classified.source_evidence_ids),
        "validation_status": ValidationStatus.OPERATIONAL_UNREVIEWED,
    }

    existing_ids = {r.id for r in storage.load_brain_context()}

    referenced_ids = [rid for rid in _referenced_entity_ids(classified.record_kind, fields) if rid]
    dangling = [rid for rid in referenced_ids if rid not in existing_ids]
    if dangling:
        raise DanglingReferenceError(classified.record_kind.value, dangling)

    if classified.record_kind == ClassifiedRecordKind.ENTITY:
        record = _build_entity(fields, common)
    elif classified.record_kind == ClassifiedRecordKind.CLAIM:
        record = _build_claim(fields, common)
    elif classified.record_kind == ClassifiedRecordKind.RELATIONSHIP:
        record = _build_relationship(fields, common)
    elif classified.record_kind == ClassifiedRecordKind.CAPABILITY:
        record = _build_capability(fields, common)
    else:
        raise ValueError(f"Cannot construct a new record for record_kind {classified.record_kind!r}")

    if record.id in existing_ids:
        raise ValueError(
            f"NEW_CANDIDATE id {record.id!r} already exists in the corpus -- "
            "the duplicate check should have caught this; refusing to silently overwrite"
        )
    storage.save_brain_records([record], scope=scope)
    return record


def _build_entity(fields: dict[str, Any], common: dict[str, Any]) -> Entity:
    entity_type = _normalize_enum(EntityType, fields.get("entity_type"), default=None)
    if entity_type is None:
        raise ValueError(f"entity_type {fields.get('entity_type')!r} is not a recognized EntityType")
    name = fields["name"]
    payload_model = PAYLOAD_MODEL_BY_ENTITY_TYPE[entity_type]
    payload_fields = fields.get("payload") or {}
    payload = payload_model.model_validate(payload_fields) if payload_fields else payload_model()

    return Entity(
        id=entity_id(entity_type.value, name),
        entity_type=entity_type,
        name=name,
        description=fields.get("description", ""),
        aliases=fields.get("aliases", []),
        payload=payload,
        **common,
    )


class UnresolvedClaimSubjectError(ValueError):
    """Raised when a Claim candidate's subject_entity_id is None/missing --
    a real, expected outcome (the LLM correctly recognized the subject has
    no existing Entity yet), not a malformed-response error. The caller
    (apply_reconciliation) surfaces this distinctly so a human sees "this
    needs an Entity created first for X," not a generic write failure."""

    def __init__(self, subject_entity_name: str | None) -> None:
        self.subject_entity_name = subject_entity_name
        super().__init__(
            f"Claim subject has no existing entity id (proposed name: {subject_entity_name!r}) -- "
            "an Entity for this subject must be created (as its own NEW_CANDIDATE) before a Claim "
            "about it can be written."
        )


def _build_claim(fields: dict[str, Any], common: dict[str, Any]) -> Claim:
    subject_entity_id = fields.get("subject_entity_id")
    if not subject_entity_id:
        raise UnresolvedClaimSubjectError(fields.get("subject_entity_name"))
    if not is_well_formed_id(subject_entity_id, expected_prefix="entity"):
        raise ValueError(f"subject_entity_id {subject_entity_id!r} is not a well-formed entity id")
    predicate = fields["predicate"]

    obj = _normalize_claim_object(fields["object"])

    return Claim(
        id=claim_id(subject_entity_id, predicate),
        subject_entity_id=subject_entity_id,
        predicate=predicate,
        object=obj,
        polarity=_normalize_enum(Polarity, fields.get("polarity"), default=Polarity.UNCERTAIN),
        condition=fields.get("condition"),
        note=fields.get("note", ""),
        **common,
    )


def _normalize_claim_object(object_field: Any) -> EntityRefObject | LiteralValueObject:
    # classify_candidate's schema documents `object` as {"kind": ...,
    # "value"|"entity_id": ...}, but a real LLM response has been observed
    # returning a bare string instead (proposed_fields is intentionally
    # loosely typed, see types.py's own docstring -- this is exactly the
    # kind of shape drift that's expected there, not a validation bug to
    # crash on).
    if isinstance(object_field, str):
        return LiteralValueObject(value=object_field)
    if isinstance(object_field, dict):
        if object_field.get("kind") == "entity_ref":
            return EntityRefObject(entity_id=object_field["entity_id"])
        if "value" in object_field:
            return LiteralValueObject(value=object_field["value"])
    raise ValueError(f"Cannot normalize claim object field: {object_field!r}")


def _normalize_enum(enum_cls: type, value: Any, *, default: Any) -> Any:
    """Case-insensitively resolve `value` against `enum_cls`'s values,
    falling back to `default` for None/empty/unrecognized input -- an LLM
    reliably gets the CONCEPT right (e.g. "affirmed") but not always the
    exact casing a str Enum's .value requires, and this is cheaper and
    more robust than teaching the prompt to never vary casing."""
    if not value:
        return default
    if isinstance(value, enum_cls):
        return value
    normalized = str(value).strip().lower()
    for member in enum_cls:
        if member.value.lower() == normalized:
            return member
    return default


def _build_relationship(fields: dict[str, Any], common: dict[str, Any]) -> Relationship:
    from_id = fields["from_id"]
    to_id = fields["to_id"]
    relationship_type = _normalize_enum(RelationshipType, fields.get("relationship_type"), default=None)
    if relationship_type is None:
        raise ValueError(f"relationship_type {fields.get('relationship_type')!r} is not a recognized RelationshipType")

    return Relationship(
        id=make_id("relationship", from_id, relationship_type.value, to_id),
        from_id=from_id,
        relationship_type=relationship_type,
        to_id=to_id,
        note=fields.get("note", ""),
        **common,
    )


def _build_capability(fields: dict[str, Any], common: dict[str, Any]) -> Capability:
    name = fields["name"]
    return Capability(
        id=make_id("capability", name),
        name=name,
        description=fields.get("description", ""),
        capability_kind=_normalize_enum(CapabilityKind, fields.get("capability_kind"), default=CapabilityKind.DIAGNOSTIC),
        target_entity_ids=fields.get("target_entity_ids", []),
        allowed_surface_entity_ids=fields.get("allowed_surface_entity_ids", []),
        required_role_ids=fields.get("required_role_ids", []),
        **common,
    )


def _create_conflicting_claim(
    storage: StorageProvider, reconciled: ReconciliationDecision, *, scope: str
) -> Claim:
    """A CONFLICT never edits the existing claim it disagrees with -- it
    creates a NEW Claim(polarity=conflicting) citing the new evidence,
    explicitly linked by shared subject_entity_id (design doc §12: "the
    existing claim is NOT deleted, edited, or silently overwritten. Both
    stand, flagged as contested, until a human resolves which is
    current")."""
    classified = reconciled.classified
    fields = dict(classified.proposed_fields)
    subject_entity_id = fields["subject_entity_id"]
    if not is_well_formed_id(subject_entity_id, expected_prefix="entity"):
        raise ValueError(f"subject_entity_id {subject_entity_id!r} is not a well-formed entity id")

    object_field = fields["object"]
    obj = (
        EntityRefObject(entity_id=object_field["entity_id"])
        if object_field.get("kind") == "entity_ref"
        else LiteralValueObject(value=object_field["value"])
    )

    note = fields.get("note", "")
    if reconciled.conflicts_with_claim_id:
        note = f"{note} (conflicts with {reconciled.conflicts_with_claim_id})".strip()

    conflicting_claim = Claim(
        id=claim_id(subject_entity_id, f"{fields['predicate']}_conflict_{reconciled.rationale[:20]}"),
        subject_entity_id=subject_entity_id,
        predicate=fields["predicate"],
        object=obj,
        polarity=Polarity.CONFLICTING,
        condition=fields.get("condition"),
        note=note,
        source_refs=list(classified.source_evidence_ids),
        validation_status=ValidationStatus.CONFLICTING,
    )
    storage.save_brain_records([conflicting_claim], scope=scope)
    return conflicting_claim
