"""Fix 3 claim-id collisions found while backfilling embeddings
(brain/AGENT_DESIGN_NOTES.md §15.4): training_video_day1 and
training_video_day2 each independently produced an operational_context
record with the SAME context_id for a topic both days' training covered
(AGV status fields, system state reference, zone configuration) --
claim_id(context_id, "details") (brain/id_generation.py) then faithfully
derived the identical claim id from that identical context_id for two
genuinely different claims (different subject_entity_id, different
asserted content, cited from different evidence).

This is a structural gap in claim_id() itself (no source-disambiguating
component), not a one-off migration-script bug -- but per
AGENT_DESIGN_NOTES.md §1's standing rule (no new source-shape-specific
migration script), the fix here is a small, targeted, one-time correction
of the 3 known-affected records, following the exact pattern
apply_entity_type_corrections.py already established for a rename: change
the id, verify no dangling reference exists (confirmed by grep before
writing this script -- these 3 ids appear nowhere else in the corpus),
write back.

Run: python -m brain.migration.fix_training_video_claim_id_collisions [--write]
"""

from __future__ import annotations

import argparse

from brain.migration.common import REPO_ROOT, dump_records, load_json
from brain.schemas.claim import Claim

OPERATIONAL_SOURCES_DIR = REPO_ROOT / "brain" / "data" / "local" / "operational_sources"

# Every claim id colliding between training_video_day1 and
# training_video_day2, confirmed by loading both sources' claims.json and
# grouping by id (see AGENT_DESIGN_NOTES.md §15.4 for the confirming
# investigation) -- day2's copy is renamed, day1's is left as-is, matching
# "the earlier-ingested source keeps the unqualified id" as the
# disambiguation rule (arbitrary but consistent; no other criterion
# distinguishes them, since both are equally real, evidence-backed claims).
COLLIDING_CLAIM_IDS = [
    "claim:ctx_training_video_agv_status_fields_v1:details",
    "claim:ctx_training_video_system_state_reference_v1:details",
    "claim:ctx_training_video_zone_configuration_reference_v1:details",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    day2_claims_path = OPERATIONAL_SOURCES_DIR / "training_video_day2" / "claims.json"
    raw_claims = load_json(day2_claims_path)

    renamed = 0
    for claim in raw_claims:
        if claim["id"] in COLLIDING_CLAIM_IDS:
            old_id = claim["id"]
            new_id = old_id.replace("claim:ctx_training_video_", "claim:ctx_training_video_day2_")
            print(f"  {old_id} -> {new_id}")
            claim["id"] = new_id
            renamed += 1

    print(f"\nRenamed {renamed} of {len(COLLIDING_CLAIM_IDS)} known-colliding claim ids in training_video_day2.")
    if renamed != len(COLLIDING_CLAIM_IDS):
        print("WARNING: not all expected collisions were found -- corpus may have changed since this script was written.")

    if not args.write:
        print("\nDRY RUN — nothing written. Pass --write to apply.")
        return

    claims = [Claim.model_validate(c) for c in raw_claims]
    dump_records(claims, day2_claims_path)
    print(f"Wrote {len(claims)} claims to {day2_claims_path}")


if __name__ == "__main__":
    main()
