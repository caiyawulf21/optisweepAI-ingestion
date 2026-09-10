from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from brain.id_generation import is_well_formed_id
from brain.schemas.capability import Capability
from brain.schemas.claim import Claim
from brain.schemas.entity import Entity
from brain.schemas.evidence_unit import EvidenceUnit
from brain.schemas.playbook import Playbook
from brain.schemas.procedure import Procedure
from brain.schemas.relationship import Relationship
from brain.schemas.review import BrainReview

BrainRecordUnion = (
    EvidenceUnit | Entity | Claim | Relationship | Capability | Procedure | Playbook | BrainReview
)


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)


def validate_relationship_endpoints(
    relationships: Iterable[Relationship],
    known_ids: set[str],
) -> ValidationResult:
    """Reject relationships whose from_id/to_id do not resolve to a known typed ID.

    Part 1 §8: "Relationships must not be inferred from a title string or held
    only inside LLM prose" and §13: "A relationship cannot point to an unknown
    or malformed typed ID."
    """
    errors: list[str] = []
    for rel in relationships:
        for field_name in ("from_id", "to_id"):
            endpoint_id = getattr(rel, field_name)
            if not is_well_formed_id(endpoint_id):
                errors.append(f"{rel.id}: {field_name} {endpoint_id!r} is not a well-formed typed ID")
            elif endpoint_id not in known_ids:
                errors.append(f"{rel.id}: {field_name} {endpoint_id!r} does not reference a known record")
    return ValidationResult(valid=not errors, errors=errors)


def validate_source_refs_present(records: Iterable[BrainRecordUnion]) -> ValidationResult:
    """Derived records (claim, relationship, capability) should carry provenance.

    EvidenceUnit and Entity may originate with sparse source_refs during initial
    authoring; Claim and Relationship enforce this at the schema level already.
    This check gives a batch-level summary across a mixed set of records.
    """
    errors: list[str] = []
    for record in records:
        if isinstance(record, (Claim, Relationship)) and not record.source_refs:
            errors.append(f"{record.id}: derived record has no source_refs")
    return ValidationResult(valid=not errors, errors=errors)


def validate_claim_references(claims: Iterable[Claim], known_ids: set[str]) -> ValidationResult:
    """Check Claim.subject_entity_id and Claim.object (when kind ==
    entity_ref) resolve to known records — payload-embedded entity
    references, not Relationship records, so `validate_relationship_endpoints`
    never covered them.

    This exact gap caused real, live data corruption three times in one
    migration session before being closed here (2026-09-03):
    `apply_capability_state_pairings.py`'s Capability.support_contract
    references (BRAIN_BUILD_PROCESS.md §6.10), then
    `apply_entity_type_corrections.py`'s Claim.subject_entity_id
    references, then `apply_entity_duplicate_merges.py`'s
    Claim.subject_entity_id references (the same script, unfixed since
    the entity-duplicate-merge feature was first built) — each found only
    by an engineer explicitly grepping for dangling references after the
    fact, because `validate_batch() == 0 errors` gave false confidence
    every time. See AGENT_DESIGN_NOTES.md §4 for the standing lesson this
    keeps re-teaching: any corpus-wide id rename/merge must be treated as
    touching every kind of place another record could reference that id,
    not just Relationship.from_id/to_id.
    """
    errors: list[str] = []
    for claim in claims:
        if claim.subject_entity_id not in known_ids:
            errors.append(
                f"{claim.id}: subject_entity_id {claim.subject_entity_id!r} does not reference a known record"
            )
        obj = claim.object
        if getattr(obj, "kind", None) == "entity_ref":
            entity_ref_id = getattr(obj, "entity_id", None)
            if entity_ref_id not in known_ids:
                errors.append(f"{claim.id}: object.entity_id {entity_ref_id!r} does not reference a known record")
    return ValidationResult(valid=not errors, errors=errors)


def validate_capability_support_contract_references(
    capabilities: Iterable[Capability], known_ids: set[str]
) -> ValidationResult:
    """Check Capability.support_contract's capability-id lists resolve to
    known records — the exact gap found in BRAIN_BUILD_PROCESS.md §6.10
    (27 dangling references that `validate_batch()` silently reported 0
    errors on). Documented there as an open gap; closed here.
    """
    errors: list[str] = []
    for cap in capabilities:
        sc = cap.support_contract
        if sc is None:
            continue
        for field_name in ("required_evidence_capability_ids", "forbidden_capability_ids"):
            for cap_id in getattr(sc, field_name):
                if cap_id not in known_ids:
                    errors.append(
                        f"{cap.id}: support_contract.{field_name} contains unknown id {cap_id!r}"
                    )
        for field_name in ("diagnostic_surface_entity_ids", "control_surface_entity_ids"):
            for entity_ref in getattr(sc, field_name):
                if entity_ref not in known_ids:
                    errors.append(f"{cap.id}: support_contract.{field_name} contains unknown id {entity_ref!r}")
        if sc.preferred_surface_entity_id is not None and sc.preferred_surface_entity_id not in known_ids:
            errors.append(
                f"{cap.id}: support_contract.preferred_surface_entity_id "
                f"{sc.preferred_surface_entity_id!r} does not reference a known record"
            )
    return ValidationResult(valid=not errors, errors=errors)


def validate_procedure_playbook_references(
    procedures: Iterable[Procedure],
    playbooks: Iterable[Playbook],
    known_ids: set[str],
) -> ValidationResult:
    """Check every id a Procedure/Playbook references by field (not by
    Relationship) actually resolves to a known record in the batch.

    This is exactly the class of check `validate_relationship_endpoints`
    does for `Relationship.from_id`/`to_id` — but Procedure.capability_id
    and PlaybookNode.capability_id/procedure_id/symptom_entity_id are
    payload-embedded id references, not Relationship records, so they were
    NOT covered by the existing check. Added deliberately at the same time
    these two record types were introduced, per the gap documented in
    AGENT_DESIGN_NOTES.md (found during the capability re-identification in
    BRAIN_BUILD_PROCESS.md §6.10: a corpus-wide id rename silently produced
    27 dangling `support_contract` references that `validate_batch()`
    reported as 0 errors on, because nothing walked that field). Rather
    than let Procedure/Playbook repeat that exact mistake, their
    payload-embedded references are checked from the start.
    """
    errors: list[str] = []
    for proc in procedures:
        if proc.capability_id not in known_ids:
            errors.append(f"{proc.id}: capability_id {proc.capability_id!r} does not reference a known record")
        for role_id in proc.allowed_role_entity_ids:
            if role_id not in known_ids:
                errors.append(f"{proc.id}: allowed_role_entity_ids contains unknown id {role_id!r}")
        for step in proc.steps:
            for role_field in ("responsible_role_entity_id", "supporting_role_entity_id"):
                value = getattr(step, role_field)
                if value is not None and value not in known_ids:
                    errors.append(
                        f"{proc.id}: step {step.step_number} {role_field} {value!r} does not reference a known record"
                    )
            for action in step.actions:
                if action.role_entity_id is not None and action.role_entity_id not in known_ids:
                    errors.append(
                        f"{proc.id}: step {step.step_number} action {action.label!r} "
                        f"role_entity_id {action.role_entity_id!r} does not reference a known record"
                    )

    for pb in playbooks:
        for entity_id in [*pb.entry_symptom_entity_ids, *pb.affected_entity_ids]:
            if entity_id not in known_ids:
                errors.append(f"{pb.id}: references unknown entity id {entity_id!r}")
        for node in pb.nodes:
            if node.capability_id is not None and node.capability_id not in known_ids:
                errors.append(f"{pb.id}: node {node.node_id!r} capability_id {node.capability_id!r} does not reference a known record")
            if node.procedure_id is not None and node.procedure_id not in known_ids:
                errors.append(f"{pb.id}: node {node.node_id!r} procedure_id {node.procedure_id!r} does not reference a known record")
            if node.symptom_entity_id is not None and node.symptom_entity_id not in known_ids:
                errors.append(f"{pb.id}: node {node.node_id!r} symptom_entity_id {node.symptom_entity_id!r} does not reference a known record")
            for role_id in node.allowed_role_entity_ids:
                if role_id not in known_ids:
                    errors.append(f"{pb.id}: node {node.node_id!r} allowed_role_entity_ids contains unknown id {role_id!r}")

    return ValidationResult(valid=not errors, errors=errors)


def validate_review_references(reviews: Iterable[BrainReview], known_ids: set[str]) -> ValidationResult:
    """Check BrainReview.affected_record_ids resolves to known records —
    the same payload-embedded-id-reference class of check every other
    record type gets (see validate_claim_references' docstring for why
    this class of gap recurred three times before being made a standing
    practice for every new id-shaped field, AGENT_DESIGN_NOTES.md §4).
    """
    errors: list[str] = []
    for review in reviews:
        for record_id in review.affected_record_ids:
            if record_id not in known_ids:
                errors.append(
                    f"{review.id}: affected_record_ids contains unknown id {record_id!r}"
                )
    return ValidationResult(valid=not errors, errors=errors)


def validate_batch(
    evidence_units: Iterable[EvidenceUnit] = (),
    entities: Iterable[Entity] = (),
    claims: Iterable[Claim] = (),
    relationships: Iterable[Relationship] = (),
    capabilities: Iterable[Capability] = (),
    procedures: Iterable[Procedure] = (),
    playbooks: Iterable[Playbook] = (),
    reviews: Iterable[BrainReview] = (),
) -> ValidationResult:
    """Validate a set of already-schema-valid Brain records against cross-record rules.

    Individual pydantic models already enforce their own field-level rules on
    construction; this function checks relationships between records in the batch,
    such as relationship endpoints resolving to a record actually present.
    """
    evidence_units = list(evidence_units)
    entities = list(entities)
    claims = list(claims)
    relationships = list(relationships)
    capabilities = list(capabilities)
    procedures = list(procedures)
    playbooks = list(playbooks)
    reviews = list(reviews)

    known_ids: set[str] = set()
    known_ids.update(e.id for e in evidence_units)
    known_ids.update(e.id for e in entities)
    known_ids.update(c.id for c in claims)
    known_ids.update(r.id for r in relationships)
    known_ids.update(c.id for c in capabilities)
    known_ids.update(p.id for p in procedures)
    known_ids.update(p.id for p in playbooks)
    known_ids.update(r.id for r in reviews)

    errors: list[str] = []
    errors.extend(validate_relationship_endpoints(relationships, known_ids).errors)
    errors.extend(
        validate_source_refs_present([*claims, *relationships]).errors
    )
    errors.extend(validate_claim_references(claims, known_ids).errors)
    errors.extend(validate_capability_support_contract_references(capabilities, known_ids).errors)
    errors.extend(validate_procedure_playbook_references(procedures, playbooks, known_ids).errors)
    errors.extend(validate_review_references(reviews, known_ids).errors)
    return ValidationResult(valid=not errors, errors=errors)
