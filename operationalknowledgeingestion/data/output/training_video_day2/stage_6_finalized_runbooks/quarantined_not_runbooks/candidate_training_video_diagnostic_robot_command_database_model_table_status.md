# Check Robot Command Database Model Table for Active Command Status (Sent → In Progress → Archived)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_robot_command_database_model_table_active_command_status_v1` |
| Title | Check Robot Command Database Model Table for Active Command Status (Sent → In Progress → Archived) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `robot_task_or_command_stuck` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robotics module’s transactional table, RobotCommandDatabaseModel, to determine whether a robot command is still active (sent/in-progress) or has completed and been archived to Robot Command Activity (historical status such as errored or cancelled).

## When To Use

When you need to verify whether a specific Robotics-module robot command for an AGV is still active (sent/in-progress) or has completed and moved into the archived Robot Command Activity record.

## Access Or Tools Needed

* Access to the Robot Command Database model table (RobotCommandDatabaseModel)
* Access to the Robot Command Activity archive view/table

## Related Operational Context

* ctx_training_video_robot_command_database_table_v1
* ctx_training_video_robot_command_activity_archive_v1
* ctx_training_video_command_status_and_queue_capacity_v1

## Visual References

![artifact_training_video_training_video_day2_0014_the_robot_command_database_model_table_primary_01_18_59_000](assets/bc80d134a7f69ff3.jpg)

*Training frame showing RobotCommandDatabaseModel command names and fields (including sent/in-progress indicators and command lifecycle context).*

## Procedure Steps

### Step 1 — Open the Robot Command Database model table view (RobotCommandDatabaseModel)

**Responsible role:** L2_support

**Instruction:**
Open the Robot Command Database model table view for RobotCommandDatabaseModel and display the columns/fields used to identify command lifecycle (including sent time and in-progress time) and command identity fields (command name, robot name, container, station/parameters).

**Expected result:**
RobotCommandDatabaseModel is visible with rows that include command identity fields and lifecycle timing fields (sent time and in-progress time).

---

### Step 2 — Locate the relevant active command row by command name and associated parameters

**Responsible role:** L2_support

**Instruction:**
In RobotCommandDatabaseModel, locate the row matching the command name (examples from the source include MoveTote, PickupTote, DropOffTote, EmptyGoTo, RemoveAgv, ReleaseAgv, GoCharge) and match the associated robot name/container/station parameters shown in the table.

**Expected result:**
A single RobotCommandDatabaseModel row is identified for the target command name and the associated robot/container/station parameters.

---

### Step 3 — Check lifecycle timestamps/fields (sent time and in-progress time)

**Responsible role:** L2_support

**Instruction:**
For the identified RobotCommandDatabaseModel row, confirm the row has a sent time and determine whether it is marked as in progress by checking the in-progress time field/indicator described in the source.

**Expected result:**
You can classify the command lifecycle state based on the presence/values of sent time and in-progress time (sent but not in-progress vs marked in-progress).

**Stop or Escalate If:**

* If the command appears stuck (e.g., not progressing from sent to in-progress as described), stop and escalate for deeper investigation.

---

### Step 4 — If not in active table, confirm archive in Robot Command Activity and review archived status

**Responsible role:** L2_support

**Instruction:**
If the command is no longer present in RobotCommandDatabaseModel, open the Robot Command Activity archive view/table and search for the historical record for the same command name and associated robot/container/station parameters. Review the archived status, noting that the source states it could be errored or cancelled.

**Expected result:**
A matching historical record is found in Robot Command Activity with an archived status (e.g., errored or cancelled) for the target command.

**Stop or Escalate If:**

* If the expected command is not present in RobotCommandDatabaseModel and also not found in Robot Command Activity, stop and escalate for deeper investigation.

---

### Step 5 — Interpret queue/capacity implication of in-progress vs not-yet in-progress

**Responsible role:** L2_support

**Instruction:**
Using the source’s described relationship between command lifecycle and queue/location capacity, interpret the observed lifecycle state: when the command is in-progress, it frees up the queue/location capacity; until then, the current destination location remains.

**Expected result:**
Your lifecycle classification (sent vs in-progress vs archived) aligns with the expected queue/location capacity behavior described by the source.

---

## Success Criteria

* For the target command, you determine whether it is still active in RobotCommandDatabaseModel (sent and/or in-progress) or has been archived to Robot Command Activity with an archived status (e.g., errored or cancelled).
* You can explain the observed lifecycle state using the source’s sent → in-progress → archived model and the described queue/location capacity implication.

## Failure Conditions

* Target command is missing from RobotCommandDatabaseModel and also missing from Robot Command Activity.
* Target command appears stuck (not progressing from sent to in-progress as described).
* Lifecycle state cannot be classified due to missing/unclear sent time or in-progress time fields.

## Escalation Guidance

* If the expected command is not present in RobotCommandDatabaseModel and also not found in Robot Command Activity, stop and escalate for deeper investigation (the source does not provide further database-only troubleshooting steps in this segment).
* If the command appears stuck (e.g., not progressing from sent to in-progress as described), stop and escalate; the source mentions operational recovery ideas elsewhere but does not provide a specific database-only recovery procedure in this segment.

## Missing Details / Known Gaps

* The packet does not provide explicit SSMS/WCS navigation steps (e.g., exact menu path) to open RobotCommandDatabaseModel and Robot Command Activity; steps are written to match the source’s described table/fields but without UI navigation specifics.
* The packet does not provide exact column names for sent time vs in-progress time vs archived status; it only states these fields exist and are used for lifecycle classification.
* The packet does not provide a specific database-only recovery procedure for a command stuck in sent/not-in-progress; it only instructs to stop and escalate.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_robot_command_database_model_table_status
- Source ID: `training_video_day2`
- Source Type: `training_video`
