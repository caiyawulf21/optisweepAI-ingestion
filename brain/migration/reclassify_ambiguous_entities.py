"""Reclassify a fixed, human-reviewed list of entities as Claims.

These entities were flagged AMBIGUOUS by the entity-vs-claim audit (see
brain/migration/BRAIN_BUILD_PROCESS.md) — short enough and structured
loosely enough that the migration-time is_claim_shaped() heuristic doesn't
catch them (tightening that heuristic to catch this pattern in general was
tested and produces 80 false positives against legitimately-named entities;
see the audit). The user reviewed the original 35 directly and confirmed
all are claims, not entities — this is a targeted reclassification of
exactly those records, not a change to the general migration logic.

**2 more added during the §6.12 re-judge pass** (`crash_example`,
`repeat_incident_avoidance_as_a_training_concept`): both typed `symptom`,
so they weren't in the original name-pattern review at all, but both fail
the Entity test on inspection — `crash_example`'s own description ("An
example of a crash is presented") describes a moment in a training video,
not a checkable system state, and `repeat_incident_avoidance` describes a
training/pedagogy theme ("recurrence avoidance is an operational concern"),
not a state of the system either. Both had the exact same applies_to-target
shape as the original 35, confirming they belong in this list, not that the
list-building method needs to change.

For each entity in the list:
1. Find its existing APPLIES_TO relationship(s) (created by the normal
   migration path before this entity was flagged) and use the target as the
   new Claim's subject.
2. Emit a Claim carrying the entity's description/any has_detail claim
   content, citing the same source_refs the entity had.
3. Remove the entity from the registry and rewrite every Relationship/Claim
   that referenced its id to point at the new claim's subject instead (for
   relationship endpoints) or drop the now-redundant APPLIES_TO edge itself.

Requires re-running the full rebuild afterward (see brain/migration/
BRAIN_BUILD_PROCESS.md's rebuild order) is NOT needed here — unlike
consolidate_entities.py, this script also directly rewrites the per-source
claims.json/relationships.json files it touches, since the entities being
removed are not going to be recreated by re-running Pass 1 (they were a
one-off audit finding, not a systematic bug affecting future runs).

Run: python -m brain.migration.reclassify_ambiguous_entities [--write]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from brain.id_generation import claim_id
from brain.migration.common import REPO_ROOT, dump_records, load_json
from brain.migration.entity_shape import strip_source_reference_leak
from brain.schemas.claim import Claim, LiteralValueObject, Polarity
from brain.schemas.entity import Entity
from brain.schemas.relationship import Relationship, RelationshipType

ENTITIES_PATH = REPO_ROOT / "brain" / "data" / "local" / "ontology_catalogs" / "entities.json"
OPERATIONAL_SOURCES_DIR = REPO_ROOT / "brain" / "data" / "local" / "operational_sources"
SOURCES = [
    "manual_optisweep_om_v3",
    "training_video_day1",
    "training_video_day2",
    "active_agv_error_query_1",
    "video_training_inspection",
]

# The 35 names, human-reviewed and confirmed as claims, not entities.
AMBIGUOUS_ENTITY_NAMES = [
    "OptiSweep as an automated consolidated bagging solution",
    "UPS Chat as the standard building communication layer",
    "Division of responsibilities between AGV hardware and RMS",
    "Task assignment flow from WCS into RMS queue",
    "Second Chat message and sorter-ready parcel data",
    "Tote fill thresholds: pretty full and full",
    "Full tote makes chute unavailable during exchange",
    "Parcel lifecycle messaging before and at sorter induction",
    "Potential destination as a sortable destination set",
    "Parcel lifecycle into chute and tote tracking",
    "Off-end sorter destinations remain visible through sort confirmations",
    "AGV zone designation and under-rack lift positioning",
    "AGV exchange command pairing and backfill exception",
    "Chute closure behavior and exchange timing targets",
    "Hospital as a reject station for operator handling",
    "RMS as the robot management system for AGVs",
    "RMS web application login and overview screen",
    "Special locations can represent different operational functions",
    "E-stop system control referenced in the message panel",
    "Map Overview right-side panel provides additional information",
    "Robot indicator color states mentioned during restart recovery",
    "Container Selection screen for totes and containers",
    "Blue indicator meaning on container or station display",
    "Container section supports tote lookup by tote number",
    "Robot Selection Go-to function for AGV repositioning",
    "Example recovery use of Go-to after tipper disruption",
    "Hospital location referenced as an AGV drop-off destination",
    "Low-battery thresholds affecting task acceptance and startup",
    "Charger Selection screen supports viewing and selecting chargers",
    "Cancel Bag Out Option for Manual Bag Out",
    "Indicator message reference for hot bin marking",
    "Referenced categories of API-related errors and exceptions",
    "Historical sort data is retained in the database",
    "Ignition tag application and real-time tag view",
    "SystemActiveErrorModel table used for active AGV error visibility",
    # Added in the §6.12 re-judge pass — see module docstring.
    "Crash example",
    "Repeat-incident avoidance as a training concept",
]


def load_entities() -> list[dict]:
    return load_json(ENTITIES_PATH)


def load_source_records(source: str, name: str) -> list[dict]:
    path = OPERATIONAL_SOURCES_DIR / source / f"{name}.json"
    return load_json(path) if path.exists() else []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    raw_entities = load_entities()
    entities_by_id = {e["id"]: e for e in raw_entities}
    entities_by_name = {e["name"]: e["id"] for e in raw_entities}

    target_ids = set()
    missing_names = []
    for name in AMBIGUOUS_ENTITY_NAMES:
        eid = entities_by_name.get(name)
        if eid is None:
            missing_names.append(name)
        else:
            target_ids.add(eid)

    if missing_names:
        print(f"WARNING: {len(missing_names)} name(s) not found in current entities.json (already resolved or renamed):")
        for n in missing_names:
            print(f"  - {n!r}")

    print(f"Targeting {len(target_ids)} entities for reclassification.")

    # Load every source's relationships/claims once, tagged by source, so
    # rewrites can be written back per-source at the end.
    per_source_relationships: dict[str, list[dict]] = {}
    per_source_claims: dict[str, list[dict]] = {}
    for source in SOURCES:
        per_source_relationships[source] = load_source_records(source, "relationships")
        per_source_claims[source] = load_source_records(source, "claims")

    new_claims: list[Claim] = []
    unresolved = []

    for eid in target_ids:
        entity = entities_by_id[eid]

        # Find this entity's own APPLIES_TO target across all sources.
        # Skip a self-referential edge (from_id == to_id) if one exists — a
        # separate, real bug in the live migration's applies_to handling
        # (an applies_to value matching the record's own alias, not just its
        # exact title, isn't caught by the self-skip check there) that
        # surfaced while building this script; noted, not fixed here, since
        # fixing it is a different change than reclassifying these 35
        # entities. Reclassifying THIS entity must not point its new claim's
        # subject at itself, since the entity is about to be deleted.
        subject_id = None
        for source, rels in per_source_relationships.items():
            for r in rels:
                if r["from_id"] == eid and r["relationship_type"] == "applies_to" and r["to_id"] != eid:
                    subject_id = r["to_id"]
                    break
            if subject_id:
                break

        if subject_id is None or subject_id not in entities_by_id:
            unresolved.append(entity["name"])
            continue

        claim_text = strip_source_reference_leak(entity.get("description", "")) or entity["name"]
        c_id = claim_id(eid.split(":", 2)[-1], "reclassified_from_entity")
        new_claims.append(
            Claim(
                id=c_id,
                subject_entity_id=subject_id,
                predicate="has_related_fact",
                object=LiteralValueObject(kind="literal", value=claim_text),
                polarity=Polarity.AFFIRMED,
                source_refs=entity.get("source_refs", []),
            )
        )

    if unresolved:
        print(f"\n{len(unresolved)} entities had no resolvable applies_to target — left as entities, not reclassified:")
        for n in unresolved:
            print(f"  - {n!r}")

    reclassified_entity_ids = set()
    for eid in target_ids:
        if eid in entities_by_id and entities_by_id[eid]["name"] not in unresolved:
            reclassified_entity_ids.add(eid)

    print(f"\n{len(new_claims)} entities will become Claims.")
    for c in new_claims:
        print(f"  {c.id} -> subject {c.subject_entity_id}")

    if not args.write:
        print("\nDRY RUN — nothing written. Pass --write to apply.")
        return

    # 1. Remove the reclassified entities from entities.json.
    remaining_entities = [e for e in raw_entities if e["id"] not in reclassified_entity_ids]
    dump_records([Entity.model_validate(e) for e in remaining_entities], ENTITIES_PATH)
    print(f"\nWrote {len(remaining_entities)} entities to {ENTITIES_PATH} ({len(reclassified_entity_ids)} removed)")

    # 2. For each source, drop relationships that reference a reclassified
    #    entity (its own applies_to edge is now redundant with the new
    #    Claim; any other relationship pointing at it becomes dangling and
    #    is dropped rather than repointed, since a reclassified entity's
    #    former id has no single correct replacement for an arbitrary
    #    relationship type).
    for source in SOURCES:
        rels = per_source_relationships[source]
        kept = [
            r for r in rels
            if r["from_id"] not in reclassified_entity_ids and r["to_id"] not in reclassified_entity_ids
        ]
        dropped = len(rels) - len(kept)
        if dropped:
            path = OPERATIONAL_SOURCES_DIR / source / "relationships.json"
            dump_records([Relationship.model_validate(r) for r in kept], path)
            print(f"{source}: dropped {dropped} relationship(s) referencing a reclassified entity")

        claims = per_source_claims[source]
        kept_claims = [c for c in claims if c["subject_entity_id"] not in reclassified_entity_ids]
        source_new_claims = [c for c in new_claims if any(
            r["to_id"] == c.subject_entity_id
            for r in per_source_relationships[source]
            if r["from_id"] in reclassified_entity_ids
        )]
        dropped_claims = len(claims) - len(kept_claims)
        if dropped_claims or source_new_claims:
            all_claims = kept_claims + [json.loads(c.model_dump_json()) for c in source_new_claims]
            path = OPERATIONAL_SOURCES_DIR / source / "claims.json"
            dump_records([Claim.model_validate(c) for c in all_claims], path)
            print(
                f"{source}: dropped {dropped_claims} claim(s) with a reclassified subject, "
                f"added {len(source_new_claims)} new claim(s)"
            )


if __name__ == "__main__":
    main()
