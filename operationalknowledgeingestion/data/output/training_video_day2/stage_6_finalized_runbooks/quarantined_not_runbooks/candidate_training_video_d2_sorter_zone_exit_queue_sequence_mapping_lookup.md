# Use sorter zone exit queue sequence ID and mapping file lookup to determine the target station/location

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_sorter_zone_exit_queue_sequence_id_and_mapping_lookup_v1` |
| Title | Use sorter zone exit queue sequence ID and mapping file lookup to determine the target station/location |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sorter_item_or_scan_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `mapping_abnormal`, `sort_lifecycle_stuck` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When an AGV is shut down and the system uses a zone + shutdown queue sequence number, it looks up a zone-to-sequence mapping (lookup table) to translate that zone/sequence into a specific sorter station/location. Use the observed zone and shutdown queue sequence ID to query the sorter-side mapping and read the mapped station/location.

## When To Use

Use this when you need to determine which sorter station/location an AGV should target based on a shutdown queue sequence ID tied to a specific zone (e.g., zone 4 with sequence 4).

## Do Not Use For

* Do not use this procedure to perform physical safety actions (e-stop).
* Do not use this procedure when the zone/sequence values are unknown or cannot be observed from the live system context.

## Access Or Tools Needed

* Sorter-side mapping file / lookup table (as referenced by the training segment)
* Ability to identify the relevant zone and shutdown queue sequence number from the live system context

## Related Operational Context

* ctx_training_video_sorter_zone_exit_queue_sequence_id_v1
* ctx_training_video_zone_sequence_mapping_file_v1
* ctx_training_video_sorter_entrance_queue_sequence_order_v1
* ctx_training_video_compression_preserves_order_v1

## Visual References

![artifact_training_video_training_video_day2_0012_the_sense_to_me_yeah_if_primary_00_34_18_500](assets/eedfe29104bb9440.jpg)

*RMS robotControl page frame with transcript describing: shutdown queue sequence number tied to zone; query for zone 4; mapping file lookup table; sequence 1–4 start from sorter entrance queue; compression keeps AGVs in order.*

## Procedure Steps

### Step 1 — Identify the current zone and the shutdown queue sequence number

**Responsible role:** L2_support

**Instruction:**
From the live shutdown queue context, identify the zone (example concept: zone 4) and the shutdown queue sequence number you are dealing with (example concept: sequence four).

**Expected result:**
You have a specific (zone, sequence) pair (e.g., zone 4 + sequence 4) that can be used as lookup keys.

**Stop or Escalate If:**

* If the zone/sequence pair cannot be identified reliably, stop and escalate for deeper investigation.

---

### Step 2 — Open/locate the sorter-side mapping file (lookup table)

**Responsible role:** L2_support

**Instruction:**
Locate the sorter-side mapping file/lookup table referenced by the segment and prepare to query it using the identified zone value.

**Expected result:**
You have access to the mapping/lookup table that supports querying by zone and sequence.

**Stop or Escalate If:**

* If the mapping file/lookup table cannot be found or does not support the required lookup keys, stop and escalate.

---

### Step 3 — Use the zone value in the mapping file

**Responsible role:** L2_support

**Instruction:**
In the mapping file/lookup table, select the entry for the identified zone value (example concept: use zone 4).

**Expected result:**
The mapping table context for the selected zone is active/selected so you can retrieve the sequence mapping for that zone.

**Stop or Escalate If:**

* If the zone value is not found in the mapping file/lookup table, stop and escalate for deeper investigation.

---

### Step 4 — Find the sequence entry for that zone

**Responsible role:** L2_support

**Instruction:**
Within the selected zone entry, locate the row/entry for the identified shutdown queue sequence number (example concept: “what is sequence four”).

**Expected result:**
You have identified the mapping row/entry corresponding to the (zone, sequence) pair.

**Stop or Escalate If:**

* If the (zone, sequence) combination is not found in the mapping file/lookup table, stop and escalate for deeper investigation.

---

### Step 5 — Read the mapped sorter station/location from the lookup table

**Responsible role:** L2_support

**Instruction:**
Read the mapped sorter station/location value from the mapping file/lookup table for the selected (zone, sequence) entry (examples from the segment include station 300; zone 3, station 301; zone 3, 2302).

**Expected result:**
You can state the mapped sorter station/location corresponding to the observed zone + sequence number using the mapping file/lookup table (example concept: zone 4 + sequence 4 → station/location as defined in the lookup table).

**Stop or Escalate If:**

* If the mapped station/location is inconsistent with the source’s sequence ordering/compression concept, stop and escalate for deeper investigation.

---

### Step 6 — Confirm mapping logic aligns with sequence ordering and compression behavior

**Responsible role:** L2_support

**Instruction:**
Verify that the mapping result you read is consistent with the concept that sequence values 1–4 start from the sorter entrance queue and that compression keeps AGVs in order by sequence (including the idea that AGVs need to move together when compressing).

**Expected result:**
The mapped station/location you report is consistent with the expected sequence ordering/compression logic described in the segment.

**Stop or Escalate If:**

* If the mapping logic does not align with the sequence ordering/compression concept, stop and escalate for deeper investigation.

---

## Success Criteria

* You can state the mapped sorter station/location corresponding to the observed zone + shutdown queue sequence number using the sorter-side mapping/lookup table.
* The mapping result is consistent with the sequence ordering/compression concept (sequence 1–4 starting from sorter entrance queue; compression preserves order by sequence).

## Failure Conditions

* Zone value not found in the mapping file/lookup table.
* Sequence entry for the selected zone not found (zone/sequence combination missing).
* Mapped station/location is inconsistent with the expected sequence ordering/compression concept.

## Escalation Guidance

* If the zone/sequence combination is not found in the mapping file/lookup table, or the mapped station/location is inconsistent with the sequence ordering/compression concept, stop and escalate for deeper investigation.

## Missing Details / Known Gaps

* The source does not name the exact mapping file name, table name, or the specific query mechanism/fields used to perform the lookup (it is described conceptually as a mapping file/lookup table).
* The source provides example station/location outputs (e.g., station 300; zone 3, station 301; zone 3, 2302) but does not provide the full mapping dataset needed to compute real station/location values without access to the actual mapping file.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_sorter_zone_exit_queue_sequence_mapping_lookup
- Source ID: `training_video_day2`
- Source Type: `training_video`
