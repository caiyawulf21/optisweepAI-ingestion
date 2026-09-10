"""Executes an approved audit resolution against the corpus -- the step
resolve_audit_candidate (Tool 6, brain_service/audit.py) deliberately
never performs itself ("proposes a resolution... does not write the
resolution to the corpus," per that module's own docstring; §10.2.1's
long-standing open item).

Scope (2026-09-09/2026-09-10, appcode HTTP boundary decisions):
- **MERGE** executes for real: collapses duplicate Entities/Capabilities/
  etc. that `find_audit_candidates` flagged, reusing the exact "grow
  richer, never regress" mechanic REINFORCE/PATCH already use.
- **RETYPE** executes for real (2026-09-10): an Entity's own
  `entity_type` was wrong (e.g. `state` should be `symptom`). Since an
  Entity's id embeds its type (`entity:<type>:<name>`), this means
  building the new id, walking every record in the corpus for any
  string-valued field that names the OLD id, and rewriting it to the NEW
  id -- then re-validating everything that changed. See
  `_apply_retype`'s own docstring for the payload-compatibility check
  that keeps this from silently dropping real data.
- **RECLASSIFY** is NOT executed -- unlike RETYPE (a same-record-kind id
  rename with a mechanical, generalizable procedure), RECLASSIFY means a
  record was created as the wrong RECORD KIND entirely (e.g. a Claim that
  should have been an Entity). There is no mechanical procedure for that:
  turning a Claim into an Entity is not a rename, it requires judgment
  about what fields survive, what new relationships/claims should exist
  in the new shape, and what should happen to whatever already cited the
  old Claim id -- none of which this module can safely infer. Accepting
  it without applying it -- rather than either silently no-op'ing or
  guessing at a conversion -- is the deliberate choice; a caller must
  never be told a corpus id changed when it didn't.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from brain.id_generation import entity_id
from brain.migration.merge import merge_record
from brain.schemas.common import ValidationStatus
from brain.schemas.entity import PAYLOAD_MODEL_BY_ENTITY_TYPE, Entity, EntityType
from brain.schemas.review import BrainReview, ReviewResolution
from brain.validators import BrainRecordUnion, validate_batch
from providers.storage import StorageProvider


class NoWinnerRecordError(ValueError):
    def __init__(self) -> None:
        super().__init__(
            "MERGE resolution requires winner_record_id -- resolve_audit_candidate's "
            "AuditResolutionResponse did not supply one, so there is no record to merge into."
        )


class UnresolvableRecordError(ValueError):
    def __init__(self, record_id: str) -> None:
        self.record_id = record_id
        super().__init__(f"record id {record_id!r} does not resolve to an existing record in the corpus")


class RetypeTargetError(ValueError):
    """Raised for any RETYPE request this module cannot safely execute --
    always BEFORE any write happens, so a caller never sees a partially
    -applied rename."""


@dataclass
class AuditExecutionResult:
    applied: bool
    resolution: ReviewResolution
    mutated_record_ids: list[str] = field(default_factory=list)
    detail: str = ""


def apply_audit_resolution(
    storage: StorageProvider,
    review: BrainReview,
    *,
    winner_record_id: str | None = None,
    new_entity_type: str | None = None,
) -> AuditExecutionResult:
    """Applies `review.resolution` (already set by resolve_audit_candidate
    or an SME's direct choice) against the corpus. Returns
    `applied=False` with an explanatory `detail` for anything this module
    does not execute -- never raises for an unsupported resolution kind,
    since NOT_A_DUPLICATE/NEEDS_HUMAN/RECLASSIFY are all real, valid
    outcomes that simply have nothing (or nothing safe yet) to execute.
    Does raise for a supported resolution given invalid/insufficient
    input (e.g. MERGE with no winner, RETYPE with no target type) --
    those are caller errors, not valid no-op outcomes."""
    if review.resolution == ReviewResolution.MERGE:
        return _apply_merge(storage, review, winner_record_id=winner_record_id)
    if review.resolution == ReviewResolution.RETYPE:
        return _apply_retype(storage, review, new_entity_type=new_entity_type)

    return AuditExecutionResult(
        applied=False,
        resolution=review.resolution,
        detail=_unsupported_resolution_detail(review.resolution),
    )


def _unsupported_resolution_detail(resolution: ReviewResolution) -> str:
    if resolution == ReviewResolution.RECLASSIFY:
        return (
            "RECLASSIFY is recorded but not auto-applied -- converting a record from one "
            "KIND to another (e.g. a Claim that should have been an Entity) has no mechanical "
            "procedure; it requires human judgment about what survives the conversion and how "
            "existing references should be re-pointed. The corpus is unchanged."
        )
    return (
        f"resolution {resolution.value!r} is recorded but not auto-applied -- "
        "only MERGE and RETYPE are executed against the corpus today. This resolution "
        "requires a manual follow-up action; the corpus is unchanged."
    )


def _apply_merge(
    storage: StorageProvider, review: BrainReview, *, winner_record_id: str | None
) -> AuditExecutionResult:
    if not winner_record_id:
        raise NoWinnerRecordError()
    if winner_record_id not in review.affected_record_ids:
        raise ValueError(
            f"winner_record_id {winner_record_id!r} is not one of this review's own "
            f"affected_record_ids {review.affected_record_ids!r}"
        )

    all_records = {r.id: r for r in storage.load_brain_context()}
    for record_id in review.affected_record_ids:
        if record_id not in all_records:
            raise UnresolvableRecordError(record_id)

    winner = all_records[winner_record_id]
    losers = [all_records[rid] for rid in review.affected_record_ids if rid != winner_record_id]

    merged_winner = winner
    for loser in losers:
        # merge_record expects a plain-dict incoming payload matching the
        # target model's own fields -- passing the loser's full dump lets
        # every unioned list (source_refs, aliases, etc.) and empty-scalar
        # fill happen the same way REINFORCE/PATCH already merge one
        # record's fields into another (brain_service/persistence.py's
        # _apply_merge), just with both sides being real existing records
        # here instead of an existing record + an LLM's proposed fields.
        merged_winner = merge_record(merged_winner, loser.model_dump(mode="python"))

    mutated: list[BrainRecordUnion] = []
    if merged_winner is not winner:
        winner_scope = storage.find_scope_for_record(winner_record_id) or "audit_resolutions"
        storage.save_brain_records([merged_winner], scope=winner_scope)
        mutated.append(merged_winner)

    deprecated_losers: list[BrainRecordUnion] = []
    for loser in losers:
        if loser.validation_status == ValidationStatus.DEPRECATED:
            continue
        deprecated = loser.model_copy(update={"validation_status": ValidationStatus.DEPRECATED})
        loser_scope = storage.find_scope_for_record(loser.id) or "audit_resolutions"
        storage.save_brain_records([deprecated], scope=loser_scope)
        deprecated_losers.append(deprecated)
    mutated.extend(deprecated_losers)

    return AuditExecutionResult(
        applied=True,
        resolution=ReviewResolution.MERGE,
        mutated_record_ids=[r.id for r in mutated],
        detail=(
            f"merged {len(losers)} record(s) into {winner_record_id!r}; "
            f"{len(deprecated_losers)} marked deprecated."
        ),
    )


def _apply_retype(
    storage: StorageProvider, review: BrainReview, *, new_entity_type: str | None
) -> AuditExecutionResult:
    """RETYPE renames one Entity's id (its type-segment changes, e.g.
    "entity:state:x" -> "entity:symptom:x") and cascades that rename into
    every OTHER record in the corpus that references the old id as a
    plain string anywhere in its own fields -- Relationship.from_id/to_id,
    Claim.subject_entity_id/object.entity_id, Procedure step role ids,
    Playbook node ids, Capability target/surface/role id lists, etc.
    Rather than hand-enumerating every one of those fields per schema
    (confirmed via grep: entity-id references appear in at least 9
    distinct nested locations across 5 record types), this walks each
    record's own raw dict form and replaces the exact old-id STRING
    wherever it appears -- a generic, schema-agnostic substitution that
    covers every current and future id-reference field the same way,
    verified correct afterward by re-validating every mutated record
    through its own pydantic model plus a corpus-wide validate_batch().

    The renamed record's OWN old id cannot be deleted (StorageProvider has
    no delete method anywhere) -- the old-id document is instead marked
    DEPRECATED, the same "flag, never destroy" mechanism MERGE's losers
    already use, so a stale reference that somehow survives the cascade
    at least resolves to a record correctly labeled as no longer current
    rather than silently vanishing.
    """
    if len(review.affected_record_ids) != 1:
        raise RetypeTargetError(
            f"RETYPE expects exactly one affected_record_id (the entity being retyped), "
            f"got {review.affected_record_ids!r}"
        )
    old_id = review.affected_record_ids[0]

    if not new_entity_type:
        raise RetypeTargetError(
            "RETYPE resolution requires new_entity_type -- resolve_audit_candidate's "
            "AuditResolutionResponse.fields_to_rewrite (or an SME's direct choice) must "
            "name the corrected entity_type."
        )
    try:
        resolved_new_type = EntityType(new_entity_type)
    except ValueError as exc:
        raise RetypeTargetError(f"{new_entity_type!r} is not a recognized EntityType") from exc

    all_records = {r.id: r for r in storage.load_brain_context()}
    if old_id not in all_records:
        raise UnresolvableRecordError(old_id)

    target = all_records[old_id]
    if not isinstance(target, Entity):
        raise RetypeTargetError(f"RETYPE only applies to Entity records; {old_id!r} is a {target.type.value}")
    if target.entity_type == resolved_new_type:
        raise RetypeTargetError(f"{old_id!r} already has entity_type {resolved_new_type.value!r} -- nothing to retype")

    # Payload compatibility, checked BEFORE any write: pydantic's own
    # before-validator (Entity._validate_payload_against_declared_entity_type)
    # would silently re-coerce the payload to the NEW type's model on
    # re-validation, dropping any field the new type's payload model
    # doesn't declare -- exactly the kind of silent data loss this module
    # exists to prevent. Only allow the retype when the old and new
    # types share the same payload model (structurally compatible), or
    # the old payload carries no real data to lose (an EmptyPayload
    # instance, or a populated model with every field still at its
    # default) -- anything else is refused with a clear reason rather
    # than either dropping data or guessing how to carry it over.
    old_payload_model = PAYLOAD_MODEL_BY_ENTITY_TYPE[target.entity_type]
    new_payload_model = PAYLOAD_MODEL_BY_ENTITY_TYPE[resolved_new_type]
    payload_is_empty = target.payload.model_dump() == old_payload_model().model_dump()
    if old_payload_model is not new_payload_model and not payload_is_empty:
        raise RetypeTargetError(
            f"cannot retype {old_id!r} from {target.entity_type.value!r} to "
            f"{resolved_new_type.value!r}: the current payload ({old_payload_model.__name__}) "
            f"carries real data not representable in the new type's payload "
            f"({new_payload_model.__name__}). Clear/migrate the payload data first, or use a "
            "manual follow-up rather than an automatic retype."
        )

    new_id = entity_id(resolved_new_type.value, target.name)
    if new_id in all_records:
        raise RetypeTargetError(
            f"cannot retype {old_id!r} to {new_id!r}: a record with that id already exists in the corpus"
        )

    renamed_target = target.model_copy(
        update={
            "id": new_id,
            "entity_type": resolved_new_type,
            "payload": new_payload_model() if old_payload_model is not new_payload_model else target.payload,
        }
    )

    # Known, deliberate limitation: Relationship.id and Claim.id are
    # DERIVED from their own from_id/subject_entity_id at creation time
    # (relationship_id()/claim_id()), but nothing in this schema enforces
    # that an id stays consistent with its own fields after creation --
    # validate_batch() checks that from_id/to_id/subject_entity_id RESOLVE
    # to real records, never that a record's own id matches what its
    # current field values would generate. So a Relationship/Claim whose
    # from_id/subject_entity_id gets rewritten below keeps its OLD id
    # string (now referencing the old entity's slug even though its own
    # field points at the new entity) -- cosmetically stale, but not a
    # functional break: every lookup still resolves correctly by id, and
    # validate_batch (run below) still passes. Regenerating those ids too
    # would itself cascade into anyone referencing THAT relationship/claim
    # by its own id -- a second-order cascade deliberately out of scope
    # here; flagged in the result's `detail` when it actually occurs.
    rewritten: list[BrainRecordUnion] = []
    id_now_stale: list[str] = []
    for record in all_records.values():
        if record.id == old_id:
            continue
        original_dump = record.model_dump(mode="python")
        new_data = _substitute_id_in_value(original_dump, old_id, new_id)
        if new_data == original_dump:
            continue  # this record never referenced old_id anywhere -- unchanged
        rewritten.append(type(record).model_validate(new_data))
        if record.type.value in ("relationship", "claim"):
            id_now_stale.append(record.id)

    deprecated_old = target.model_copy(update={"validation_status": ValidationStatus.DEPRECATED})

    # Verify the WHOLE affected set is internally consistent before writing
    # anything -- validate_batch() catches a cascade that missed a
    # reference (e.g. a field this walk didn't reach because it wasn't a
    # plain string) or introduced a dangling id, the same corpus-wide
    # check every other Create-path write already runs through
    # (brain_service/validation.py).
    all_after = {**all_records, new_id: renamed_target, old_id: deprecated_old}
    for record in rewritten:
        all_after[record.id] = record
    by_type: dict[str, list[Any]] = {}
    for record in all_after.values():
        by_type.setdefault(record.type.value, []).append(record)
    validation = validate_batch(
        evidence_units=by_type.get("evidence_unit", []),
        entities=by_type.get("entity", []),
        claims=by_type.get("claim", []),
        relationships=by_type.get("relationship", []),
        capabilities=by_type.get("capability", []),
        procedures=by_type.get("procedure", []),
        playbooks=by_type.get("playbook", []),
    )
    if not validation.valid:
        raise RetypeTargetError(
            f"retyping {old_id!r} to {new_id!r} would leave the corpus inconsistent: "
            f"{'; '.join(validation.errors[:5])}"
        )

    to_write = [renamed_target, deprecated_old, *rewritten]
    for record in to_write:
        scope = storage.find_scope_for_record(record.id) or storage.find_scope_for_record(old_id) or "audit_resolutions"
        storage.save_brain_records([record], scope=scope)

    detail = (
        f"retyped {old_id!r} to {new_id!r} ({target.entity_type.value} -> {resolved_new_type.value}); "
        f"rewrote {len(rewritten)} referencing record(s); old id marked deprecated."
    )
    if id_now_stale:
        detail += (
            f" Note: {len(id_now_stale)} Relationship/Claim record(s) had their referenced entity id "
            f"rewritten but kept their OWN id string (derived from the old entity at creation time) -- "
            f"still fully resolvable and valid, just cosmetically stale: {id_now_stale[:5]}"
            f"{'...' if len(id_now_stale) > 5 else ''}"
        )

    return AuditExecutionResult(
        applied=True,
        resolution=ReviewResolution.RETYPE,
        mutated_record_ids=[r.id for r in to_write],
        detail=detail,
    )


def _substitute_id_in_value(value: Any, old_id: str, new_id: str) -> Any:
    """Recursively walks a record's raw dict/list/scalar form, replacing
    any string value EQUAL to old_id with new_id. Deliberately exact-match
    only (never a substring/regex replace) -- Brain ids are never
    embedded inside a larger string field (Part 1's id convention), so an
    exact match is both sufficient and safe against accidentally
    rewriting unrelated text that happens to contain the old id as a
    substring."""
    if isinstance(value, str):
        return new_id if value == old_id else value
    if isinstance(value, list):
        return [_substitute_id_in_value(item, old_id, new_id) for item in value]
    if isinstance(value, dict):
        return {key: _substitute_id_in_value(item, old_id, new_id) for key, item in value.items()}
    return value
