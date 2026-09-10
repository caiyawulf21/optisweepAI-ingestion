# Walk Through Database Tables Using the 'Database Walkthrough' Slide Reference

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_walk_through_database_tables_database_walkthrough_v1` |
| Title | Walk Through Database Tables Using the 'Database Walkthrough' Slide Reference |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep Day 2 “Database Walkthrough” segment to compile a table-by-table list of the database tables that are covered, and capture the walkthrough’s stated associations/purpose for each table (only when the table names/purpose are readable in the provided video frames).

## When To Use

When you need to identify which database tables are covered in the OptiSweep Training Day 2 “Database Walkthrough” segment and you have the relevant video frames available to read the table names and any stated purpose/associations.

## Do Not Use For

* Do not use this procedure as a live troubleshooting guide for database connectivity or runtime failures (the provided packet does not include a live SSMS/Helix DB workflow or query steps).
* Do not use this procedure to infer table names/purpose when the video frames are not readable; stop and request higher-resolution frames or the next segment that shows the specific table names.

## Access Or Tools Needed

* Training video playback for FORTNA OptiSweep Training Day 2
* The 'Database Walkthrough' slide frame as a reference

## Related Operational Context

* ctx_training_video_database_tables_training_scope_v1
* ctx_training_video_database_walkthrough_slide_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0008_we_use_for_this_database_when_primary_00_11_14_000](assets/f7783ed9b4087772.jpg)

*Frame with the walkthrough overview of WCS-created databases and the stated table associations/purpose (e.g., EntityLogs used for logging; Audit tracks AGDID/current geek task ID/command GUID; Geek AGV action logging; lattice code model; OPC configuration; OPC tags).*

## Procedure Steps

### Step 1 — Locate the 'Database Walkthrough' slide frame referenced in the Day 2 training segment

**Responsible role:** L1_support

**Instruction:**
Open/play the FORTNA OptiSweep Training Day 2 video and navigate to the “Database Walkthrough” segment where the presenter says “All right, we're gonna walk through all the tables”. Use the captured frame titled “Database Walkthrough” as your reference point.

**Expected result:**
You can identify the “Database Walkthrough” segment reference frame in the video (the frame where the presenter states the walkthrough will cover all tables).

**Stop or Escalate If:**

* If you cannot find the “Database Walkthrough” frame, stop and request the correct segment timestamp/frame set.

---

### Step 2 — Follow the presenter’s table-by-table walkthrough and note each table name as it appears

**Responsible role:** L1_support

**Instruction:**
During the walkthrough segment, follow along as the presenter names tables. For each table name that is readable in the available frames, record the table name exactly as it appears.

**Expected result:**
You have a list of the database table names that are readable from the provided walkthrough frames.

**Stop or Escalate If:**

* If table names are not readable from the available frames, stop and request a higher-resolution capture or the next segment that shows the specific table names.

---

### Step 3 — Record each table’s walkthrough association/purpose (only what is visible/said)

**Responsible role:** L1_support

**Instruction:**
For each table you recorded in Step 2, record what the walkthrough associates it with (purpose/what it stores) using only what is visible/said in the available frames. Do not guess beyond what is readable in the frames.

**Expected result:**
For each readable table name, you have a corresponding walkthrough association/purpose statement that is limited to what is visible/readable in the provided frames.

**Stop or Escalate If:**

* If table names/purpose are not readable from the available frames, stop and request a higher-resolution capture or the next segment that shows the specific table names and explanations.

---

## Success Criteria

* A list of database table names covered by the “Database Walkthrough” segment is produced from readable frames.
* For each recorded table name, a purpose/association statement is captured that is limited to what is visible/readable in the provided frames.

## Failure Conditions

* Table names or purposes cannot be confirmed due to unreadable/low-resolution frames.
* Recorded purposes include assumptions not supported by the visible/readable walkthrough text.

## Escalation Guidance

* If table names/purpose are not readable from the available frames, stop and request a higher-resolution capture or the next segment that shows the specific table names and explanations.

## Missing Details / Known Gaps

* The packet does not provide a live database surface/workflow (e.g., SSMS/Helix DB) to verify table names/fields directly; this runbook is limited to extracting readable table names/purpose from the provided video frames.
* The packet does not include additional frames that show the full table-by-table list; only an overview frame (00:11:14.000) is provided with multiple table/model concepts.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_database_walkthrough_tables
- Source ID: `training_video_day2`
- Source Type: `training_video`
