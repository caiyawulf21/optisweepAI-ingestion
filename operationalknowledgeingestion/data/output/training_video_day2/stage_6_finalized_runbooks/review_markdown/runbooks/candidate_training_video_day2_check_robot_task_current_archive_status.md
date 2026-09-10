# Check Current and Archived Robot Task Records

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_current_and_archived_robot_task_records_v1` |
| Title | Check Current and Archived Robot Task Records |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use read-only SSMS access to the Robotics database to determine whether a tote task requested by the Sorter Sweeper module is present in the current Robot Task database model table or has been archived to Robot Task Activity.

## When To Use

Use SSMS against the WCS / Helix Robotics database when troubleshooting a tote task requested by the Sorter Sweeper module and determining whether the task is still current or has completed and been archived.

## Do Not Use For

* Do not use this procedure to modify Robot Task or Robot Task Activity records.
* Do not treat a completed task as current solely because it is no longer present in the current Robot Task database model table.

## Safety And Operational Notes

* This is a read-only database diagnostic. Do not alter Robot Task or Robot Task Activity records.

## Access Or Tools Needed

* WCS / Helix DB (SSMS)
* SSMS
* Robotics database
* Robot Task database model table
* Robot Task Activity

## Related Operational Context

* ctx_training_video_robot_task_current_archive_v1

## Procedure Steps

### Step 1 — Open the Robotics database in SSMS

**Responsible role:** L2_support

**Instruction:**
In SSMS, open the Robotics database and locate the Robot Task database model table.

**Expected result:**
The Robot Task database model table is available for read-only inspection in the Robotics database.

**Stop or Escalate If:**

* Escalate if the Robotics database or Robot Task database model table is unavailable.

---

### Step 2 — Check the current Robot Task record

**Responsible role:** L2_support

**Instruction:**
In the SSMS Robot Task database model table, inspect the record for the tote task requested by the Sorter Sweeper module and determine whether the task is present.

**Expected result:**
The requested tote task is either found as a row in the current Robot Task database model table or is not present there.

**Stop or Escalate If:**

* Continue to the archived-record check if the task is not present in the current table.
* Escalate if the task cannot be identified for lookup.

---

### Step 3 — Check Robot Task Activity for a completed task

**Responsible role:** L2_support

**Instruction:**
If the tote task is complete or is not present in the current Robot Task database model table, inspect Robot Task Activity in the Robotics database for the archived task record.

**Expected result:**
A completed tote task is found in Robot Task Activity rather than being treated as a current task.

**Stop or Escalate If:**

* Stop and escalate when the tote task cannot be found in either the current Robot Task table or Robot Task Activity.
* Escalate when the task status cannot be determined from the available records.

---

### Step 4 — Classify the task as current or archived

**Responsible role:** L2_support

**Instruction:**
Record the task as current when its row is present in the Robot Task database model table. Record it as archived when the completed task is present in Robot Task Activity and is no longer treated as current.

**Expected result:**
The task has one clear classification: current or archived, based on the corresponding Robotics database row.

**Stop or Escalate If:**

* Escalate when a task appears simultaneously current and archived.
* Escalate when the task status cannot be determined from the available records.
* Do not alter task or activity records.

---

## Success Criteria

* The requested tote task is located in either the current Robot Task database model table or Robot Task Activity.
* The task is classified as current or archived from its live Robotics database row.
* No Robot Task or Robot Task Activity records are modified.

## Failure Conditions

* The tote task cannot be found in either the current Robot Task database model table or Robot Task Activity.
* The task appears simultaneously in current and archived records.
* The task state cannot be determined from the available Robotics database records.

## Escalation Guidance

* Escalate to L3_support when the tote task is missing from both current and archived records.
* Escalate to L3_support when current and archived records conflict or the task state is indeterminate.
* Do not modify task or activity records while investigating.

## Missing Details / Known Gaps

* The packet does not provide the exact physical database table names beyond Robot Task database model table and Robot Task Activity.
* The packet does not provide a task identifier field or a query template; no SQL command is included.
* No matching live Robot Task table screenshot was supplied; the available artifact depicts AGV error information and is not attached as evidence.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_check_robot_task_current_archive_status
- Source ID: `training_video_day2`
- Source Type: `training_video`
