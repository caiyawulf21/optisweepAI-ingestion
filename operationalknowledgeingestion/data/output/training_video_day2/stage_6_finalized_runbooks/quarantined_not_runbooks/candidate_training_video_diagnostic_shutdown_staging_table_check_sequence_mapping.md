# Verify Shutdown Staging Mapping Using ShutDownStaging Table (with tote vs without tote) and Sequence

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_shutdown_staging_mapping_shutdowntaging_sequence_v1` |
| Title | Verify Shutdown Staging Mapping Using ShutDownStaging Table (with tote vs without tote) and Sequence |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robotics database model’s ShutDownStaging mapping to verify where AGVs should stage during shutdown, including the difference between AGVs with totes (off-the-end queue + center queue staging) versus AGVs without totes (mapped to sorter locations). Confirm how the ShutDownStaging Sequence value is used to match an AGV’s zone/sequence to the correct shutdown queue destination.

## When To Use

When you need to diagnose/verify shutdown staging behavior by checking the ShutDownStaging table mapping logic (tote vs without tote) and confirming the Sequence-based mapping used to select the shutdown queue destination.

## Do Not Use For

* Do not use this procedure to make configuration changes or to attempt to correct staging behavior solely by editing the mapping; use it for diagnosis/verification only.

## Access Or Tools Needed

* Robotics database access to view the ShutDownStaging table (SSMS/Helix/WCS DB access as applicable in the environment)

## Related Operational Context

* ctx_training_video_shutdown_staging_table_v1
* ctx_training_video_shutdown_with_tote_vs_without_tote_v1

## Visual References

![artifact_training_video_training_video_day2_0011_so_all_right_we_ll_move_primary_00_26_58_500](assets/566cf64c9e45d275.jpg)

*Frame showing ShutDownStaging table fields/columns including ShutDownOffTheEndid, ShutDownQueueId, Sequence, SorterSide, DatabaseModelid and the tote vs without-tote mapping description.*

![artifact_training_video_training_video_day2_0012_the_sense_to_me_yeah_if_primary_00_34_18_500](assets/eedfe29104bb9440.jpg)

*Frame describing how an AGV in a zone uses Sequence to look up the shutdown queue mapping (e.g., zone 4 -> sequence 4 -> station mapping).*

## Procedure Steps

### Step 1 — Open the ShutDownStaging table in the Robotics database model

**Responsible role:** L2_support

**Instruction:**
In the Robotics database model (via SSMS/Helix/WCS DB access as applicable), open the ShutDownStaging table view that includes the mapping columns referenced in the source: ShutDownOffTheEndid, ShutDownQueueId, Sequence, SorterSide, and DatabaseModelid.

**Expected result:**
You can view ShutDownStaging rows with the mapping columns ShutDownOffTheEndid, ShutDownQueueId, Sequence, SorterSide, and DatabaseModelid visible in the table.

**Stop or Escalate If:**

* If ShutDownStaging does not show the expected mapping columns (including Sequence), stop and escalate to deeper database/config troubleshooting.

---

### Step 2 — Identify tote-carrying AGV staging entries (off-the-end queue + center queue staging)

**Responsible role:** L2_support

**Instruction:**
In the ShutDownStaging table, locate the rows/entries that correspond to AGVs with totes. Confirm that the mapping includes a ShutDownOffTheEndid (off-the-end queue) and a ShutDownQueueId (queue to stage at) for those tote-carrying entries.

**Expected result:**
You can point to ShutDownStaging entries for tote-carrying AGVs where ShutDownOffTheEndid is present (off-the-end queue) and ShutDownQueueId indicates the queue destination to stage at (center queue staging).

**Stop or Escalate If:**

* If the ShutDownStaging table does not show the expected tote vs without-tote mapping pattern, stop and escalate to deeper database/config troubleshooting.

---

### Step 3 — Identify without-tote AGV staging entries (mapped to sorter locations)

**Responsible role:** L2_support

**Instruction:**
In the ShutDownStaging table, locate the rows/entries that correspond to AGVs without totes. Confirm that the mapping indicates AGVs are mapped to sorter locations (i.e., the destination is based on sorter locations rather than the off-the-end queue path).

**Expected result:**
You can identify ShutDownStaging entries for AGVs without totes where the mapping pattern aligns with 'mapped to sorter locations' rather than the tote off-the-end queue staging path.

**Stop or Escalate If:**

* If the ShutDownStaging table does not show the expected tote vs without-tote mapping pattern, stop and escalate to deeper database/config troubleshooting.

---

### Step 4 — Locate and verify Sequence values used for shutdown queue selection

**Responsible role:** L2_support

**Instruction:**
In the ShutDownStaging table, locate the Sequence field values for the relevant tote and without-tote entries. Verify the source rule: Sequence is used as the order to match an AGV’s zone/sequence to the shutdown queue sequence.

**Expected result:**
You can identify Sequence values in ShutDownStaging entries and explain (from what is visible in the table) how those Sequence values correspond to the shutdown queue selection logic described by the source.

**Stop or Escalate If:**

* If the Sequence field is missing/unreadable, stop and escalate to deeper database/config troubleshooting.

---

### Step 5 — Cross-check the described zone/sequence -> shutdown queue mapping behavior

**Responsible role:** L2_support

**Instruction:**
Using the source-described logic, cross-check the ShutDownStaging entries you identified by Sequence: when an AGV in a given zone triggers shutdown, it looks up the shutdown queue destination using the matching sequence number (e.g., zone 4 uses sequence 4). Confirm that the Sequence value you see in ShutDownStaging maps to the expected shutdown queue destination (via the table’s mapping fields).

**Expected result:**
The ShutDownStaging entries you identified show a consistent mapping where the Sequence value used for zone/sequence matching corresponds to the shutdown queue destination selection described by the source.

**Stop or Escalate If:**

* If the ShutDownStaging table does not show the expected tote vs without-tote mapping pattern or the Sequence field is missing/unreadable, stop and escalate to deeper database/config troubleshooting.
* If the Sequence-based mapping does not align with the described zone/sequence lookup behavior, stop and escalate to deeper database/config troubleshooting.

---

## Success Criteria

* You can point to ShutDownStaging entries showing tote-carrying AGV staging includes ShutDownOffTheEndid (off-the-end queue) and ShutDownQueueId (center queue staging).
* You can point to ShutDownStaging entries showing without-tote AGV staging is mapped to sorter locations.
* Sequence values are visible/readable in ShutDownStaging and you can relate them to the zone/sequence -> shutdown queue selection behavior described by the source.

## Failure Conditions

* ShutDownStaging does not show the expected tote vs without-tote mapping pattern.
* Sequence field is missing/unreadable in ShutDownStaging.
* Sequence-based mapping does not align with the described zone/sequence lookup behavior.

## Escalation Guidance

* If the ShutDownStaging table does not show the expected tote vs without-tote mapping pattern or the Sequence field is missing/unreadable, stop and escalate to deeper database/config troubleshooting.

## Missing Details / Known Gaps

* The packet does not provide the exact SQL/SSMS query steps or the specific filter criteria to distinguish tote vs without-tote rows within ShutDownStaging (e.g., which column/value indicates tote presence).
* The packet does not provide the exact zone-to-sequence mapping values beyond the conceptual example (e.g., zone 4 -> sequence 4) and does not provide the specific station/destination IDs to validate against.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_shutdown_staging_table_check_sequence_mapping
- Source ID: `training_video_day2`
- Source Type: `training_video`
