"""Apply the hand-judged entity_type corrections from entity_type_corrections.py.

For each old_id -> new_entity_type entry:
1. Change the entity's entity_type and regenerate its id (entity_id() is
   type-prefixed, so a type change always means an id change).
2. Reset payload to the new type's default shape. For symptom/state ->
   component, both are EmptyPayload, so this is a no-op. For state ->
   database_table, a real DatabaseTablePayload is required
   (database_name is a mandatory field) — supplied via
   DATABASE_TABLE_PAYLOAD_OVERRIDES below rather than fabricated
   generically, since a wrong database_name would be worse than leaving
   the entity mistyped.
3. Rewrite every Relationship reference elsewhere in the corpus (both
   endpoints) from the old id to the new id, across ontology_catalogs and
   all 5 operational sources — same corpus-wide approach as
   apply_capability_state_pairings.py, for the same reason
   (BRAIN_BUILD_PROCESS.md §6.10: a rename that only rewrites some
   references silently dangles the rest).

This script must run BEFORE apply_entity_duplicate_merges.py in the
rebuild order: several of these corrections produce a same-name,
same-entity_type collision with an already-existing record once retyped
(see entity_type_corrections.py's docstring, "pattern 4") — those
collisions are then handled as ordinary merges by that later script, not
by this one.

Run: python -m brain.migration.apply_entity_type_corrections [--write]
"""

from __future__ import annotations

import argparse

from brain.id_generation import entity_id
from brain.migration.common import REPO_ROOT, dump_records, load_json
from brain.migration.entity_type_corrections import CORRECTIONS, SYSTEM_ACTION_PAYLOAD_OVERRIDES
from brain.migration.merge import merge_record

# The WCS API catalog's single access surface for every system_action
# correction below — see entity_type_corrections.py's docstring pattern 4;
# grounded in docs/ontology/catalogs/wcs_api_catalog.json's own top-level
# access_surface field ("wcs_api"), not guessed.
WCS_API_SURFACE_ENTITY_ID = "entity:system:wcs_api"
from brain.schemas.claim import Claim
from brain.schemas.entity import Entity
from brain.schemas.relationship import Relationship

CATALOGS_DIR = REPO_ROOT / "brain" / "data" / "local" / "ontology_catalogs"
OPERATIONAL_SOURCES_DIR = REPO_ROOT / "brain" / "data" / "local" / "operational_sources"
SOURCES = [
    "manual_optisweep_om_v3",
    "training_video_day1",
    "training_video_day2",
    "active_agv_error_query_1",
    "video_training_inspection",
]

# Hand-supplied DatabaseTablePayload content for the state -> database_table
# corrections, grounded in the entity's own description/evidence and the
# already-correctly-typed sibling database_table entities' database_name
# values (entity:database_table:systemactiveerrormodel and
# entity:database_table:ignitionlaneactivitymodel) — not fabricated.
DATABASE_TABLE_PAYLOAD_OVERRIDES: dict[str, dict] = {
    "entity:state:system_database_model_status_values": {"database_name": "robotics"},
    "entity:state:system_database_status_values": {"database_name": "robotics"},
    "entity:state:status_alarm_and_safety_related_database_fields": {"database_name": "robotics"},
    "entity:state:lane_activity_status_and_classification_labels": {"database_name": "sorter_sweeper"},
    "entity:state:lane_activity_status_and_classification_indicators": {"database_name": "sorter_sweeper"},
    # system_active_error_model / system_error_activity_model both belong to
    # the "robotics" database too — same grounding as the two entries above,
    # confirmed against their own evidence text. Both are merged into an
    # already-existing, already-populated database_table sibling by
    # apply_entity_duplicate_merges.py immediately after this script runs
    # (see entity_duplicate_merges.py), so this payload only needs to be
    # valid, not complete — merge_record() picks up the richer sibling's
    # key_fields regardless.
    "entity:state:system_active_error_model": {"database_name": "robotics"},
    "entity:state:system_error_activity_model": {"database_name": "robotics"},
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    entities_path = CATALOGS_DIR / "entities.json"
    raw_entities = load_json(entities_path)
    entities_by_id = {e["id"]: e for e in raw_entities}

    id_remap: dict[str, str] = {}
    corrected_count = 0
    merged_into_existing_count = 0
    skipped_missing = 0

    for old_id, new_type in CORRECTIONS.items():
        if old_id not in entities_by_id:
            skipped_missing += 1
            continue

        entity = dict(entities_by_id[old_id])
        old_name = entity["name"]
        new_id = entity_id(new_type, old_name)

        if new_id == old_id:
            continue  # already corrected in a prior run

        entity["id"] = new_id
        entity["entity_type"] = new_type

        if new_type == "database_table":
            override = DATABASE_TABLE_PAYLOAD_OVERRIDES.get(old_id)
            if override is None:
                print(f"WARNING: {old_id} -> database_table has no payload override, skipping")
                continue
            entity["payload"] = {
                "database_name": override["database_name"],
                "schema_name": None,
                "business_meanings": [],
                "key_fields": [],
                "read_only": True,
            }
        elif new_type == "system_action":
            override = SYSTEM_ACTION_PAYLOAD_OVERRIDES.get(old_id)
            if override is None:
                print(f"WARNING: {old_id} -> system_action has no payload override, skipping")
                continue
            entity["payload"] = {
                "invocation_kind": override["invocation_kind"],
                "access_surface_entity_ids": [WCS_API_SURFACE_ENTITY_ID],
                "mutates_state": override["mutates_state"],
            }
        else:
            entity["payload"] = {}

        del entities_by_id[old_id]

        if new_id in entities_by_id:
            # Retyping produced a same-id collision with an entity that
            # already existed (entity_type_corrections.py's "pattern 4":
            # two independently-created records with the identical name,
            # different entity_type, now colliding once retyped). This
            # MUST merge, never silently overwrite — an earlier version of
            # this script did exactly that and clobbered an
            # already-correct, already-hand-rewritten sibling record
            # (entity:component:agv_fault_during_exchange_recovery_concept)
            # before this fix; caught by re-reading the written output, not
            # by any test, which is itself the lesson: a retype/rename
            # script's collision path needs the same "grow richer, never
            # regress" treatment as an explicit merge does, not a bare
            # dict assignment.
            existing = Entity.model_validate(entities_by_id[new_id])
            retyped = Entity.model_validate(entity)
            merged = merge_record(
                existing,
                {
                    "aliases": [retyped.name, *retyped.aliases],
                    "description": retyped.description,
                    "source_refs": retyped.source_refs,
                    "payload": retyped.payload,
                },
            )
            entities_by_id[new_id] = merged.model_dump(mode="python")
            merged_into_existing_count += 1
        else:
            entities_by_id[new_id] = entity

        id_remap[old_id] = new_id
        corrected_count += 1

    print(f"Entities re-typed: {corrected_count}")
    print(f"  of which merged into an already-existing same-id entity: {merged_into_existing_count}")
    print(f"Already corrected (skipped): {len(CORRECTIONS) - corrected_count - skipped_missing}")
    print(f"Not found (skipped): {skipped_missing}")

    if not args.write:
        print("\nDRY RUN — nothing written. Pass --write to apply.")
        for old, new in id_remap.items():
            print(f"  {old} -> {new}")
        return

    all_entities = [Entity.model_validate(e) for e in entities_by_id.values()]
    dump_records(all_entities, entities_path)
    print(f"Wrote {len(all_entities)} entities to {entities_path}")

    def rewrite_relationships(path):
        if not path.exists():
            return
        rels = load_json(path)
        changed = 0
        for r in rels:
            if r["from_id"] in id_remap:
                r["from_id"] = id_remap[r["from_id"]]
                changed += 1
            if r["to_id"] in id_remap:
                r["to_id"] = id_remap[r["to_id"]]
                changed += 1
        if changed:
            dump_records([Relationship.model_validate(r) for r in rels], path)
            print(f"{path.parent.name}: updated {changed} relationship endpoint(s) to new entity ids")

    def rewrite_claims(path):
        # Claim.subject_entity_id and Claim.object (when kind == entity_ref)
        # are payload-embedded entity references, not Relationship records —
        # the same class of reference apply_capability_state_pairings.py's
        # support_contract gap taught us not to skip (BRAIN_BUILD_PROCESS.md
        # §6.10).
        if not path.exists():
            return
        claims = load_json(path)
        changed = 0
        for c in claims:
            if c.get("subject_entity_id") in id_remap:
                c["subject_entity_id"] = id_remap[c["subject_entity_id"]]
                changed += 1
            obj = c.get("object") or {}
            if obj.get("kind") == "entity_ref" and obj.get("entity_id") in id_remap:
                obj["entity_id"] = id_remap[obj["entity_id"]]
                changed += 1
        if changed:
            dump_records([Claim.model_validate(c) for c in claims], path)
            print(f"{path.parent.name}: updated {changed} claim entity reference(s) to new entity ids")

    rewrite_relationships(CATALOGS_DIR / "relationships.json")
    rewrite_claims(CATALOGS_DIR / "claims.json")
    for source in SOURCES:
        rewrite_relationships(OPERATIONAL_SOURCES_DIR / source / "relationships.json")
        rewrite_claims(OPERATIONAL_SOURCES_DIR / source / "claims.json")


if __name__ == "__main__":
    main()
