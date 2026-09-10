"""Merge 2 relationship-id collisions found while backfilling embeddings
(brain/AGENT_DESIGN_NOTES.md §15.4): two pairs of incidents each
independently produced a relationship record with the SAME id
(relationship_id() is deterministic by from_id/relationship_type/to_id,
with no source/incident component -- correct by design, since two
incidents observing the same real structural edge SHOULD get the same
id) but never went through a merge step to combine their evidence, so
each pair currently exists as two separate on-disk records under
different incident scopes that happen to collide on id when the corpus is
loaded as a whole:

  relationship:entity_system_rms_ui:observes:entity_system_optisweep_agv_fleet
    case_218550 (earlier) + case_228723 (later)
  relationship:entity_system_optisweep_agv_fleet:observes:entity_symptom_zone_agv_mismatch
    case_223554 (earlier) + case_228723 (later)

Unlike the claim-id collision (fix_training_video_claim_id_collisions.py),
this is NOT a naming bug -- both records correctly assert the same real
edge. The fix is the Reinforce merge design docs already specify (§4.1):
union source_refs (and notes, since a merged record should not silently
drop either side's citation-adjacent context) into the earlier-created
record, remove the later, duplicate on-disk copy.

Run: python -m brain.migration.merge_cross_incident_relationship_duplicates [--write]
"""

from __future__ import annotations

import argparse

from brain.migration.common import REPO_ROOT, dump_records, load_json
from brain.migration.merge import merge_record
from brain.schemas.relationship import Relationship

INCIDENTS_DIR = REPO_ROOT / "brain" / "data" / "local" / "incidents"

# (relationship_id, winner_case, loser_case) -- winner is the
# earlier-created record (kept, enriched with the loser's source_refs/note);
# loser's on-disk copy is removed after merging. Both pairs confirmed by
# loading every incidents/*/relationships.json and grouping by id (see
# AGENT_DESIGN_NOTES.md §15.4).
DUPLICATE_PAIRS = [
    (
        "relationship:entity_system_rms_ui:observes:entity_system_optisweep_agv_fleet",
        "case_218550",
        "case_228723",
    ),
    (
        "relationship:entity_system_optisweep_agv_fleet:observes:entity_symptom_zone_agv_mismatch",
        "case_223554",
        "case_228723",
    ),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    paths_by_case: dict[str, list] = {}

    def relationships_for(case: str) -> list[dict]:
        if case not in paths_by_case:
            path = INCIDENTS_DIR / case / "relationships.json"
            paths_by_case[case] = load_json(path)
        return paths_by_case[case]

    merged_count = 0
    for relationship_id, winner_case, loser_case in DUPLICATE_PAIRS:
        winner_records = relationships_for(winner_case)
        loser_records = relationships_for(loser_case)

        winner_raw = next((r for r in winner_records if r["id"] == relationship_id), None)
        loser_raw = next((r for r in loser_records if r["id"] == relationship_id), None)
        if winner_raw is None or loser_raw is None:
            print(f"SKIP {relationship_id}: not found in both {winner_case} and {loser_case} (already merged?)")
            continue

        winner = Relationship.model_validate(winner_raw)
        loser = Relationship.model_validate(loser_raw)
        merged = merge_record(winner, {"source_refs": loser.source_refs})

        # merge_record()'s merge_scalar_field only fills an EMPTY scalar
        # from incoming -- it never overwrites a populated one, so a plain
        # merge_record() call here would silently drop the loser's note
        # whenever the winner already has one, even though both notes are
        # independently meaningful (each describes a different incident's
        # own observation of the same structural edge). Concatenate both
        # instead of relying on scalar-fill semantics for this one field.
        if loser.note and loser.note != merged.note:
            combined_note = " | ".join(filter(None, [merged.note, loser.note]))
            merged = merged.model_copy(update={"note": combined_note})

        print(f"MERGE {relationship_id}")
        print(f"  {winner_case} source_refs: {winner.source_refs} -> {merged.source_refs}")
        print(f"  note: {winner.note!r} + {loser.note!r} -> {merged.note!r}")

        winner_records[:] = [merged.model_dump(mode="python") if r["id"] == relationship_id else r for r in winner_records]
        loser_records[:] = [r for r in loser_records if r["id"] != relationship_id]
        merged_count += 1

    print(f"\nMerged {merged_count} of {len(DUPLICATE_PAIRS)} known duplicate pairs.")

    if not args.write:
        print("\nDRY RUN — nothing written. Pass --write to apply.")
        return

    for case, raw_records in paths_by_case.items():
        path = INCIDENTS_DIR / case / "relationships.json"
        records = [Relationship.model_validate(r) for r in raw_records]
        dump_records(records, path)
        print(f"Wrote {len(records)} relationships to {path}")


if __name__ == "__main__":
    main()
