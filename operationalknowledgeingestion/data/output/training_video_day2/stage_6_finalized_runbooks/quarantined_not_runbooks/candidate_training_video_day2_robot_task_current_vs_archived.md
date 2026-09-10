# Check Robot Task status and archival (current vs archived) for tote tasks from Sortter Sweeper

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_robot_task_status_archival_current_vs_archived_v1` |
| Title | Check Robot Task status and archival (current vs archived) for tote tasks from Sortter Sweeper |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robotics database Robot Task database model table to determine whether a tote task requested by the Sortter Sweeper module is still in the current set or has been archived to Robot Task Activity, based on the current-vs-archived table behavior described in the source.

## When To Use

When you need to verify whether a specific tote task requested by the Sortter Sweeper module is still present as a current Robot Task record or has moved into the archived Robot Task Activity dataset/table.

## Access Or Tools Needed

* Robotics database access (SSMS/Helix/WCS DB access implied by the source packet)

## Related Operational Context

* ctx_training_video_robot_task_table_archival_v1

## Visual References

![artifact_training_video_training_video_day2_0015_right_moving_on_excuse_me_the_primary_01_28_41_500](assets/0060f6132e5274b9.jpg)

*Training frame showing the Robot Task database model table archival relationship: current vs archived to Robot Task Activity (tote tasks requested by Sortter Sweeper).*

## Procedure Steps

### Step 1 — Open the Robotics database view for the Robot Task database model table

**Responsible role:** L2_support

**Instruction:**
In the Robotics database (via your available SSMS/Helix/WCS DB access), open the Robot Task database model table view/dataset that tracks tote task status for Sortter Sweeper requests.

**Expected result:**
You can view the Robot Task database model table rows/records that represent tote task status (the table that the source describes as having a current set).

**Stop or Escalate If:**

* If you cannot access/query the Robot Task database model table, stop and escalate for deeper database/model mapping support.

---

### Step 2 — Locate the tote task record associated with the Sortter Sweeper module request

**Responsible role:** L2_support

**Instruction:**
Within the Robot Task database model table, locate the record/row for the tote task associated with the Sortter Sweeper module request using the task identity fields/rows available in the table view you opened.

**Expected result:**
A specific tote task record is found in the Robot Task database model table for the Sortter Sweeper request under investigation.

**Stop or Escalate If:**

* If the task cannot be found in the current Robot Task model table, proceed to check the archived Robot Task Activity dataset/table as described by the source.

---

### Step 3 — Determine whether the record is in the current set or has been archived to robot task activity

**Responsible role:** L2_support

**Instruction:**
Using the source-described behavior (one current and one archived), determine whether the tote task record you located is part of the current Robot Task set or has moved to the archived Robot Task Activity.

**Expected result:**
You can identify whether the tote task is still current in the Robot Task database model table or has been archived to Robot Task Activity.

**Stop or Escalate If:**

* If the task cannot be found in either the current Robot Task model table or the archived Robot Task Activity, stop and escalate for deeper database/model mapping support.

---

### Step 4 — If archived, confirm it appears in the Robot Task Activity archive dataset/table

**Responsible role:** L2_support

**Instruction:**
If you determined the task is archived, open/query the Robot Task Activity archive dataset/table and confirm the tote task appears there.

**Expected result:**
The archived tote task appears in the Robot Task Activity archive dataset/table.

**Stop or Escalate If:**

* If the task cannot be found in either the current Robot Task model table or the archived Robot Task Activity, stop and escalate for deeper database/model mapping support.

---

## Success Criteria

* For the tote task requested by Sortter Sweeper, you can determine whether it is present as current in the Robot Task database model table or present as archived in Robot Task Activity.

## Failure Conditions

* The tote task cannot be found in either the current Robot Task model table or the archived Robot Task Activity dataset/table.
* The Robot Task database model table or Robot Task Activity archive dataset/table cannot be accessed/query-returned.

## Escalation Guidance

* If the task cannot be found in either the current Robot Task model table or the archived Robot Task Activity, stop and escalate for deeper database/model mapping support.

## Missing Details / Known Gaps

* The source packet does not provide exact SSMS/Helix/WCS navigation steps, nor specific table/column names for the Robot Task database model table and the Robot Task Activity archive dataset/table in this segment.
* The source packet does not specify which exact task identity fields/columns to use to locate a tote task record associated with a Sortter Sweeper request.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_robot_task_current_vs_archived
- Source ID: `training_video_day2`
- Source Type: `training_video`
