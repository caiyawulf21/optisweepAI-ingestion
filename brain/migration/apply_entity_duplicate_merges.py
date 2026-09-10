"""Apply the hand-judged entity merges from entity_duplicate_merges.py:

For each (winner, [losers...]) pair:
1. Merge each loser's aliases/description/source_refs/payload into the
   winner via merge_record() (grow richer, never regress).
2. Drop the loser entity records.
3. Rewrite every Relationship reference elsewhere in the corpus (ontology
   catalogs' own relationships.json, and all 5 operational sources') from
   the loser id to the winner id. A relationship that would become a
   self-reference after rewriting (winner VERB winner) is dropped instead
   of kept, since "X applies_to X" is not a meaningful fact — this is the
   expected outcome for the applies_to self-echo relationships that created
   the loser in the first place.

Mirrors apply_capability_state_pairings.py's corpus-wide reference-rewrite
approach (see BRAIN_BUILD_PROCESS.md §6.10 for why a rename/merge must be
treated as a corpus-wide operation, not a local edit — the same lesson
applies here). Re-running this script is idempotent: a loser id that no
longer exists is skipped.

**Fixed 2026-09-03**: this script rewrote Relationship references to a
merged-away loser id but NOT Claim.subject_entity_id or
Claim.object.entity_id references — the exact same class of gap already
found and fixed once in apply_capability_state_pairings.py
(BRAIN_BUILD_PROCESS.md §6.10's support_contract lesson) and again in
apply_entity_type_corrections.py, now recurring a third time in this
script specifically. Found by explicitly checking for dangling Claim
references after a merge, not by validate_batch() (which does not check
Claim.subject_entity_id resolution at all — see brain/validators.py; this
is a distinct, still-open gap from the support_contract one). 5 claims
across 2 sources were already dangling from PRIOR runs of this script
before this fix (one from the database_walkthrough_training_slide merge in
BRAIN_BUILD_PROCESS.md §6.12) — cleaned up by re-running this fixed
version, not hand-patched.

Run: python -m brain.migration.apply_entity_duplicate_merges [--write]
"""

from __future__ import annotations

import argparse

from brain.migration.common import REPO_ROOT, dump_records, load_json
from brain.migration.entity_duplicate_merges import MERGES
from brain.migration.merge import merge_record
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    entities_path = CATALOGS_DIR / "entities.json"
    raw_entities = load_json(entities_path)
    entities_by_id = {e["id"]: e for e in raw_entities}

    id_remap: dict[str, str] = {}
    merged_count = 0
    skipped_missing = 0

    for winner_id, loser_ids in MERGES.items():
        if winner_id not in entities_by_id:
            print(f"WARNING: winner {winner_id} not found, skipping its group")
            continue
        winner = Entity.model_validate(entities_by_id[winner_id])
        for loser_id in loser_ids:
            if loser_id not in entities_by_id:
                skipped_missing += 1
                # Still register the remap in case an earlier, narrower run
                # already dropped the entity but left dangling relationship
                # references — same idempotency fix as the capability script.
                id_remap[loser_id] = winner_id
                continue
            loser = Entity.model_validate(entities_by_id[loser_id])
            winner = merge_record(
                winner,
                {
                    "aliases": [loser.name, *loser.aliases],
                    "description": loser.description,
                    "source_refs": loser.source_refs,
                    "payload": loser.payload,
                },
            )
            del entities_by_id[loser_id]
            id_remap[loser_id] = winner_id
            merged_count += 1
        entities_by_id[winner_id] = winner.model_dump(mode="python")

    print(f"Entities merged away: {merged_count}")
    print(f"Already merged (skipped): {skipped_missing}")
    print(f"Winners updated: {len({m for m in MERGES if m in entities_by_id})}")

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
        kept = []
        changed = 0
        dropped_self_refs = 0
        for r in rels:
            new_from = id_remap.get(r["from_id"], r["from_id"])
            new_to = id_remap.get(r["to_id"], r["to_id"])
            if new_from != r["from_id"] or new_to != r["to_id"]:
                changed += 1
            if new_from == new_to:
                dropped_self_refs += 1
                continue
            r["from_id"] = new_from
            r["to_id"] = new_to
            kept.append(r)
        if changed:
            dump_records([Relationship.model_validate(r) for r in kept], path)
            print(
                f"{path.parent.name}: updated {changed} relationship endpoint(s), "
                f"dropped {dropped_self_refs} self-reference(s) after remap"
            )

    def rewrite_claims(path):
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
