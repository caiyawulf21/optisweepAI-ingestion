"""Tools 5 & 6 -- find_audit_candidates, resolve_audit_candidate
(AGENT_DESIGN_NOTES.md §10.2).

find_audit_candidates is a read-only, deliberately over-reporting corpus
scan; it never resolves anything. resolve_audit_candidate is the
expensive, high-context judgment call for exactly one candidate at a
time, and PROPOSES a resolution (MERGE/RETYPE/RECLASSIFY/NOT_A_DUPLICATE/
NEEDS_HUMAN) without executing it against the corpus (§10.2.1's
still-open item: a human/future step applies an approved MERGE by hand).
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pydantic import BaseModel, Field

from brain.migration.entity_shape import is_claim_shaped
from brain.schemas.claim import Claim
from brain.schemas.common import RecordType
from brain.schemas.entity import Entity
from brain.schemas.relationship import Relationship, RelationshipType
from brain.schemas.review import ReviewKind, ReviewResolution
from brain.validators import BrainRecordUnion
from brain_service.review import build_review
from providers.llm import LLMProvider
from providers.storage import StorageProvider

_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "resolve_audit_candidate.md"


class AuditResolutionResponse(BaseModel):
    """resolve_audit_candidate's (Tool 6) LLM response shape -- module-level
    so callers/tests can reference the exact same class the tool uses,
    rather than the tool constructing an equivalent-but-distinct class
    inline on every call."""

    resolution: ReviewResolution
    rationale: str
    winner_record_id: str | None = None
    fields_to_rewrite: dict = Field(default_factory=dict)

_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


def _normalize_name(name: str) -> str:
    return _NORMALIZE_RE.sub("", name.lower())


def find_audit_candidates(storage: StorageProvider, record_ids: list[str] | None = None) -> list:
    """Read-only scan implementing the checks named in §10.2. Every check
    needs the whole corpus loaded to detect a collision against something
    pre-existing (a duplicate is, by definition, a relationship between a
    candidate and something ELSE already in the corpus) -- so `record_ids`,
    when given, does not shrink what gets scanned; it filters the RETURNED
    findings down to only those naming at least one of the given ids. This
    is the "scoped to just the ids it created" behavior §10.3 describes for
    a New-candidate's mandatory duplicate check, without pretending a
    partial-corpus scan could ever detect a duplicate against unscanned
    records. None scans and returns everything.

    Returns a list of BrainReview(kind=AUDIT_FINDING) records -- these are
    RETURNED, not yet persisted, so a caller can inspect before writing
    (matching Tool 5's "never resolves anything" contract; persistence is
    the caller's choice, e.g. via storage.save_brain_records)."""
    entities = [
        r
        for r in storage.load_brain_context(record_type=RecordType.ENTITY)
        if isinstance(r, Entity)
    ]
    relationships = [
        r
        for r in storage.load_brain_context(record_type=RecordType.RELATIONSHIP)
        if isinstance(r, Relationship)
    ]
    findings: list = []

    findings.extend(_check_normalized_name_collisions(entities))
    findings.extend(_check_cross_type_same_name(entities))
    findings.extend(_check_applies_to_self_echo(entities, relationships))
    findings.extend(_check_claim_shaped_entities(entities))
    findings.extend(_check_dangling_references(storage))

    if record_ids is not None:
        wanted = set(record_ids)
        findings = [f for f in findings if wanted.intersection(f.affected_record_ids)]
    return findings


def _check_normalized_name_collisions(entities: list[Entity]) -> list:
    groups: dict[tuple, list[Entity]] = defaultdict(list)
    for entity in entities:
        groups[(entity.entity_type, _normalize_name(entity.name))].append(entity)
    findings = []
    for (_, normalized), group in groups.items():
        if len(group) > 1 and normalized:
            findings.append(
                build_review(
                    kind=ReviewKind.AUDIT_FINDING,
                    check_name="normalized_name_collision",
                    affected_record_ids=sorted(e.id for e in group),
                    proposed_change=(
                        f"{len(group)} entities of the same type normalize to the same name "
                        f"({normalized!r}) -- possible casing/spacing duplicate."
                    ),
                )
            )
    return findings


def _check_cross_type_same_name(entities: list[Entity]) -> list:
    groups: dict[str, list[Entity]] = defaultdict(list)
    for entity in entities:
        groups[_normalize_name(entity.name)].append(entity)
    findings = []
    for normalized, group in groups.items():
        distinct_types = {e.entity_type for e in group}
        if len(distinct_types) > 1 and normalized:
            findings.append(
                build_review(
                    kind=ReviewKind.AUDIT_FINDING,
                    check_name="cross_type_same_name",
                    affected_record_ids=sorted(e.id for e in group),
                    proposed_change=(
                        f"Entities with the same name {normalized!r} exist under different "
                        f"entity_types ({sorted(t.value for t in distinct_types)}) -- would "
                        "collide if one side is ever retyped to match the other."
                    ),
                )
            )
    return findings


def _check_applies_to_self_echo(entities: list[Entity], relationships: list[Relationship]) -> list:
    by_id = {e.id: e for e in entities}
    rels_by_from: dict[str, list[Relationship]] = defaultdict(list)
    for rel in relationships:
        rels_by_from[rel.from_id].append(rel)

    findings = []
    for entity in entities:
        own_rels = rels_by_from.get(entity.id, [])
        if len(own_rels) == 1 and own_rels[0].relationship_type == RelationshipType.APPLIES_TO:
            target_id = own_rels[0].to_id
            if target_id in by_id:
                findings.append(
                    build_review(
                        kind=ReviewKind.AUDIT_FINDING,
                        check_name="applies_to_self_echo",
                        affected_record_ids=sorted({entity.id, target_id}),
                        proposed_change=(
                            f"{entity.id}'s only relationship is a self-echoing APPLIES_TO "
                            f"back to {target_id} -- possible bare-echo duplicate with no "
                            "independent fact of its own."
                        ),
                    )
                )
    return findings


def _check_claim_shaped_entities(entities: list[Entity]) -> list:
    """is_claim_shaped() is a NAME check (see brain/migration/entity_shape.py
    and every existing caller in brain/migration/migrate_operational_source.py)
    -- it flags a title/name that reads as a sentence, not a description
    field, which is prose by design and will almost always contain claim-verb
    constructions without that being a category error. Calling it on
    `description` was tried during this tool's own smoke test and produced
    715/775 findings that were entity names sitting on well-formed,
    normal explanatory descriptions -- exactly the false-positive risk
    AGENT_DESIGN_NOTES.md §3 warns about for unverified heuristics."""
    findings = []
    for entity in entities:
        if is_claim_shaped(entity.name):
            findings.append(
                build_review(
                    kind=ReviewKind.AUDIT_FINDING,
                    check_name="claim_shaped_entity",
                    affected_record_ids=[entity.id],
                    proposed_change=(
                        f"{entity.id}'s name reads as an assertion/procedure title rather than "
                        "a lookup-able thing -- possible entity/claim category error."
                    ),
                )
            )
    return findings


def _check_dangling_references(storage: StorageProvider) -> list:
    from brain.validators import validate_batch

    all_records: dict[RecordType, list] = defaultdict(list)
    for record in storage.load_brain_context():
        all_records[record.type].append(record)

    result = validate_batch(
        evidence_units=all_records[RecordType.EVIDENCE_UNIT],
        entities=all_records[RecordType.ENTITY],
        claims=all_records[RecordType.CLAIM],
        relationships=all_records[RecordType.RELATIONSHIP],
        capabilities=all_records[RecordType.CAPABILITY],
        procedures=all_records[RecordType.PROCEDURE],
        playbooks=all_records[RecordType.PLAYBOOK],
    )
    if result.valid:
        return []
    # One finding per error rather than per record: validate_batch's errors
    # already name the offending record id in each message, and grouping
    # by record would require re-parsing that message's structure.
    return [
        build_review(
            kind=ReviewKind.AUDIT_FINDING,
            check_name="dangling_reference",
            affected_record_ids=_ids_referenced_in_error(error, all_records),
            proposed_change=error,
        )
        for error in result.errors
    ]


def _ids_referenced_in_error(error: str, all_records: dict[RecordType, list]) -> list[str]:
    known_ids = {record.id for records in all_records.values() for record in records}
    referenced = [record_id for record_id in known_ids if record_id in error]
    if referenced:
        return sorted(set(referenced))
    # validate_batch's messages always lead with "{record.id}: ...", even
    # when the referenced-but-unknown id itself isn't in known_ids.
    return [error.split(":", 1)[0]]


def _load_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def resolve_audit_candidate(llm: LLMProvider, storage: StorageProvider, review) -> object:
    """Loads full content of every record `review.affected_record_ids`
    names, asks the LLM to judge MERGE/RETYPE/RECLASSIFY/NOT_A_DUPLICATE/
    NEEDS_HUMAN, and returns the SAME review updated with `resolution` and
    `resolved_by="agent"`. Does not write a MERGE/RETYPE against the
    corpus itself."""
    affected_records: list[BrainRecordUnion] = [
        record
        for record in storage.load_brain_context()
        if record.id in review.affected_record_ids
    ]
    user_content = json.dumps(
        {
            "check_name": review.check_name,
            "proposed_change": review.proposed_change,
            "affected_records": [record.model_dump(mode="json") for record in affected_records],
        },
        ensure_ascii=False,
    )

    parsed = llm.generate_json(
        system_prompt=_load_prompt(),
        user_content=user_content,
        schema=AuditResolutionResponse,
        label="resolve_audit_candidate",
    )

    return build_review(
        kind=review.kind,
        affected_record_ids=review.affected_record_ids,
        proposed_change=review.proposed_change,
        check_name=review.check_name,
        status="resolved",
        resolution=parsed.resolution,
        resolved_by="agent",
        source_refs=review.source_refs,
        fields_to_rewrite=parsed.fields_to_rewrite,
    )
