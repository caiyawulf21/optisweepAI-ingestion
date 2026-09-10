"""Regression coverage for the two real, pre-existing corpus id-collision
findings surfaced while backfilling embeddings
(brain/AGENT_DESIGN_NOTES.md §15.4). These tests assert against the ACTUAL
local corpus on disk, not synthetic fixtures -- the whole point is
confirming the fix scripts already applied (fix_training_video_claim_id_collisions.py,
merge_cross_incident_relationship_duplicates.py) actually fixed the real
data, and stay fixed.
"""

from __future__ import annotations

from collections import Counter

from brain.schemas.common import RecordType
from providers.local_storage import LocalStorageProvider


def test_no_duplicate_claim_ids_in_corpus() -> None:
    storage = LocalStorageProvider()
    claims = storage.load_brain_context(record_type=RecordType.CLAIM)
    counts = Counter(c.id for c in claims)
    dupes = {claim_id: count for claim_id, count in counts.items() if count > 1}
    assert dupes == {}


def test_no_duplicate_relationship_ids_in_corpus() -> None:
    storage = LocalStorageProvider()
    relationships = storage.load_brain_context(record_type=RecordType.RELATIONSHIP)
    counts = Counter(r.id for r in relationships)
    dupes = {rel_id: count for rel_id, count in counts.items() if count > 1}
    assert dupes == {}


def test_training_video_day2_claims_have_disambiguated_ids() -> None:
    """The 3 claims that used to collide with training_video_day1 now carry
    a day2-specific id -- confirms fix_training_video_claim_id_collisions.py's
    rename actually landed, not just that no OTHER collision exists."""
    storage = LocalStorageProvider()
    day2_claims = storage.load_brain_records(scope="operational_sources/training_video_day2", record_type=RecordType.CLAIM)
    day2_ids = {c.id for c in day2_claims}

    expected_renamed_ids = {
        "claim:ctx_training_video_day2_agv_status_fields_v1:details",
        "claim:ctx_training_video_day2_system_state_reference_v1:details",
        "claim:ctx_training_video_day2_zone_configuration_reference_v1:details",
    }
    assert expected_renamed_ids.issubset(day2_ids)

    # And the OLD, colliding ids must no longer appear in day2's own file.
    old_colliding_ids = {
        "claim:ctx_training_video_agv_status_fields_v1:details",
        "claim:ctx_training_video_system_state_reference_v1:details",
        "claim:ctx_training_video_zone_configuration_reference_v1:details",
    }
    assert old_colliding_ids.isdisjoint(day2_ids)


def test_merged_cross_incident_relationships_retain_both_source_refs() -> None:
    """The 2 merged relationship records must carry BOTH incidents'
    evidence citations, not just the winner's -- confirms
    merge_cross_incident_relationship_duplicates.py's union actually
    happened, not a silent overwrite."""
    storage = LocalStorageProvider()
    relationships = storage.load_brain_context(record_type=RecordType.RELATIONSHIP)
    by_id = {r.id: r for r in relationships}

    merged_1 = by_id["relationship:entity_system_rms_ui:observes:entity_system_optisweep_agv_fleet"]
    assert "evidence:case_218550:event_023" in merged_1.source_refs
    assert "evidence:case_228723:event_008" in merged_1.source_refs

    merged_2 = by_id["relationship:entity_system_optisweep_agv_fleet:observes:entity_symptom_zone_agv_mismatch"]
    assert "evidence:case_223554:event_023" in merged_2.source_refs
    assert "evidence:case_228723:event_022" in merged_2.source_refs
