# Use Get tote task to view active tote state and resend a tote task to the robotics database model

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_get_tote_task_view_active_state_and_resend_to_robotics_database_model_v1` |
| Title | Use Get tote task to view active tote state and resend a tote task to the robotics database model |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tote_lifecycle_state`, `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `robot_task_or_command_stuck` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep/WCS “Get tote task” function to view which totes are currently active, then resend a tote task to the robotics database model when the active tote state needs to be re-issued.

## When To Use

When you need to check the active state of totes via “Get tote task,” and you need to re-issue (resend) a tote task to the robotics database model for a relevant tote.

## Access Or Tools Needed

* OptiSweep/WCS API access (tote-related functions are referenced in the source).
* Robotics database model (the resend action targets the robotics database model).

## Related Operational Context

* ctx_training_video_tote_task_state_and_resend_v1

## Visual References

![artifact_training_video_training_video_day2_0031_for_totes_we_have_exchange_sorter_primary_02_44_11_000](assets/54d41adfcf4b3f8f.jpg)

*Frame showing the tote-related API functions list including “GetToteTask” and the statement that you can resend a tote task to the robotics database model.*

## Procedure Steps

### Step 1 — Run or open the Get tote task function to view the active state of the totes

**Responsible role:** L1_support

**Instruction:**
Use the OptiSweep/WCS tote function labeled “GetToteTask” to view the active state of the totes.

**Expected result:**
The “GetToteTask” output indicates the active state of the totes.

---

### Step 2 — Identify the tote(s) whose active state indicates the task status you need to address

**Responsible role:** L1_support

**Instruction:**
From the “GetToteTask” results, identify the tote(s) whose active state indicates the tote task status you need to address.

**Expected result:**
You have identified the specific tote(s) that require a resend action.

---

### Step 3 — Resend a tote task to the robotics database model for the relevant tote task

**Responsible role:** L1_support

**Instruction:**
Use the resend capability described for tote tasks to resend the tote task to the robotics database model for the relevant tote task.

**Expected result:**
The resend action re-issues the tote task to the robotics database model for the selected tote task.

**Stop or Escalate If:**

* If resending does not change the active state as expected, stop and escalate for deeper robotics/database troubleshooting.

---

## Success Criteria

* Get tote task output shows the active state of the totes.
* Resend action re-issues the tote task to the robotics database model for the relevant tote task.

## Failure Conditions

* Get tote task does not provide the active state information needed for the tote(s) under investigation.
* Resending does not change the active state as expected.

## Escalation Guidance

* If resending does not change the active state as expected, stop and escalate for deeper robotics/database troubleshooting.

## Missing Details / Known Gaps

* The source does not provide the exact API method name or request parameters for the “resend tote task” action to the robotics database model (only that it can be resent).
* The source does not specify the exact fields/identifiers in the GetToteTask output needed to select the tote(s) for resend.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_get_tote_task_active_state_and_resend_to_robotics_database_model
- Source ID: `training_video_day2`
- Source Type: `training_video`
