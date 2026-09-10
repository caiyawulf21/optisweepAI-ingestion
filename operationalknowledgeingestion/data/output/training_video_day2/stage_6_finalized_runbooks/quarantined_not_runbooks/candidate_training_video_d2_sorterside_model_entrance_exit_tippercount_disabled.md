# Review SorterSideDatabaseModel entrance/exit queue IDs, tipper count, and disabled flag for a sorter side

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_review_sortersidedatabasemodel_entrance_exit_tippercount_disabled_v1` |
| Title | Review SorterSideDatabaseModel entrance/exit queue IDs, tipper count, and disabled flag for a sorter side |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `zone_config_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the SorterSideDatabaseModel field definitions to verify which entrance/exit queue location IDs a sorter side references, what tipper count represents (round-robin closest set), and whether that sorter side is marked disabled.

## When To Use

When you need to interpret how a specific sorter side is represented in the database model—specifically the EntranceId/ExitId queue-location references, the TipperCount meaning (round-robin closest set), and the Disabled flag.

## Access Or Tools Needed

* SSMS / Helix/WCS database access to view the SorterSideDatabaseModel table (exact access method not specified in the source).
* SorterSideDatabaseModel table fields: Name, EntranceId, ExitId, TipperCount, Disabled.
* Robot Location model understanding for the foreign-key relationship of EntranceId/ExitId to queue-location entries.

## Related Operational Context

* ctx_training_video_sorter_side_database_model_v1
* ctx_training_video_entrance_exit_queue_location_relationship_v1
* ctx_training_video_tipper_count_round_robin_concept_v1

## Visual References

![artifact_training_video_training_video_day2_0009_the_robot_location_database_model_table_primary_00_17_15_500](assets/e6b308f21a2ed402.jpg)

*Frame showing Robot Location database model location types/statuses and the SorterSideDatabaseModel field meaning (Entrance/Exit queue locations, TipperCount, Disabled).*

## Procedure Steps

### Step 1 — Open the SorterSideDatabaseModel table described in the training segment

**Responsible role:** L2_support

**Instruction:**
In SSMS / Helix/WCS database access, navigate to the SorterSideDatabaseModel table/view that contains the sorter-side model fields.

**Expected result:**
You can view the SorterSideDatabaseModel columns/fields including Name, EntranceId, ExitId, TipperCount, and Disabled.

---

### Step 2 — Identify the documented columns/fields: Name, EntranceId, ExitId, TipperCount, and Disabled

**Responsible role:** L2_support

**Instruction:**
Confirm the SorterSideDatabaseModel columns/fields you will use are: Name, EntranceId, ExitId, TipperCount, and Disabled.

**Expected result:**
You can map each required concept to the correct column: Name (sorter side identifier), EntranceId (entrance queue location ID), ExitId (exit-related queue location ID), TipperCount (round-robin closest set), Disabled (whether the sorter side is disabled).

---

### Step 3 — Review EntranceId and ExitId values as the queue-location references used by the sorter side

**Responsible role:** L2_support

**Instruction:**
For the sorter side record of interest, read EntranceId and ExitId and treat them as queue-location references for the entrance queue and exit-related queue, respectively.

**Expected result:**
For the sorter side record, EntranceId and ExitId are populated with queue-location IDs that correspond to the entrance and exit-related queue locations described by the model.

**Stop or Escalate If:**

* If EntranceId/ExitId do not correspond to queue-location entries in the Robot Location model (foreign-key relationship described in the segment), stop and escalate for deeper model/data integrity troubleshooting (L3/vendor).

---

### Step 4 — Review TipperCount and confirm it represents the 'round robin closest 4' concept

**Responsible role:** L2_support

**Instruction:**
For the sorter side record of interest, read TipperCount and interpret it as the round-robin closest set concept (the segment describes closest 4 as the tipper count).

**Expected result:**
TipperCount value can be described as the round-robin closest set size (e.g., closest 4 concept as described).

---

### Step 5 — Review Disabled to determine whether the sorter side is disabled or not

**Responsible role:** L2_support

**Instruction:**
For the sorter side record of interest, read the Disabled field and determine whether the sorter side is disabled or not based on the model’s Disabled indicator.

**Expected result:**
You can state whether the sorter side record is marked disabled (Disabled flag value) and describe it as 'disabled or not' per the model definition.

---

### Step 6 — If validating queue-location relationships, use the foreign-key relationship to the Robot Location model

**Responsible role:** L2_support

**Instruction:**
When you need to validate queue-location relationships, cross-check that the EntranceId and ExitId values correspond to queue-location entries in the Robot Location model (foreign keys to the location).

**Expected result:**
EntranceId and ExitId can be confirmed as references to queue-location entries in the Robot Location model.

**Stop or Escalate If:**

* If EntranceId/ExitId do not correspond to queue-location entries in the Robot Location model (foreign-key relationship described in the segment), stop and escalate for deeper model/data integrity troubleshooting (L3/vendor), since the source does not provide remediation steps.

---

## Success Criteria

* For the sorter side record of interest, EntranceId and ExitId can be described as the entrance queue and exit-related queue location IDs used by that sorter side.
* TipperCount can be described as the round-robin closest set concept (closest 4 described as the tipper count).
* Disabled can be described as whether the sorter side is disabled or not.
* If queue-location relationship validation is performed, EntranceId/ExitId correspond to queue-location entries in the Robot Location model.

## Failure Conditions

* EntranceId/ExitId do not correspond to queue-location entries in the Robot Location model.
* TipperCount cannot be interpreted as the round-robin closest set concept described in the source.
* Disabled flag is missing/uninterpretable for the sorter side record.

## Escalation Guidance

* If EntranceId/ExitId do not correspond to queue-location entries in the Robot Location model (foreign-key relationship described in the segment), stop and escalate for deeper model/data integrity troubleshooting (L3/vendor), since the source does not provide remediation steps.

## Missing Details / Known Gaps

* The source does not specify the exact SSMS/Helix/WCS query or how to select a specific sorter side record (e.g., by Name/SorterSideId).
* The source does not provide the exact data types/allowed values for Disabled or the exact mapping table name/columns for validating EntranceId/ExitId against Robot Location entries.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_sorterside_model_entrance_exit_tippercount_disabled
- Source ID: `training_video_day2`
- Source Type: `training_video`
