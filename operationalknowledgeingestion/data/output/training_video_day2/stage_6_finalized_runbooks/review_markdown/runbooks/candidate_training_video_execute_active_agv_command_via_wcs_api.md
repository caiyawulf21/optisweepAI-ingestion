# Execute an AGV's Active Command Through the OptiSweep WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_execute_agv_active_command_via_wcs_api_v1` |
| Title | Execute an AGV's Active Command Through the OptiSweep WCS API |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | `robot_task_or_command_stuck`, `unplanned_restart` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API ExecutedAgvCommand operation with a confirmed robot ID to execute the active command currently held by an AGV. The source describes this as useful after an unplanned restart when OptiSweep missed callbacks from Geek Plus.

## When To Use

Use when an AGV has an active command but OptiSweep missed callbacks from Geek Plus, including the source-described unplanned-restart scenario.

## Do Not Use For

* Do not use without a confirmed robot ID.
* Do not use as a replacement-command or manual-command-entry procedure; the source does not define either.
* Do not use when the request cannot be submitted or the AGV does not execute its active command without escalating.

## Safety And Operational Notes

* Use only a confirmed robot ID.
* This procedure executes the active command already held by the AGV; it does not define a new command.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog or equivalent WCS API client
* ExecutedAgvCommand POST operation
* Confirmed robot ID
* Live AGV status or movement verification

## Related Operational Context

* ctx_training_video_execute_active_agv_command_v1

## Visual References

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*OptiSweep / WCS API AGVs operation list showing POST Executed Agv Command and the related robot-ID and active-command behavior.*

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep API overview showing Apidog on the primary server and the AGVs API operations.*

## Procedure Steps

### Step 1 — Open the ExecutedAgvCommand operation

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent OptiSweep / WCS API client, open the AGVs API group and locate the operation labeled ExecutedAgvCommand, shown as POST Executed Agv Command.

**Expected result:**
The POST Executed Agv Command operation is available for submission in the OptiSweep / WCS API client.

**Stop or Escalate If:**

* The API client cannot be opened.
* The ExecutedAgvCommand operation is not available.

---

### Step 2 — Enter the confirmed robot ID

**Responsible role:** L2_support

**Instruction:**
Provide the confirmed robot ID required by the ExecutedAgvCommand operation in the OptiSweep / WCS API client.

**Expected result:**
The request contains the robot ID for the intended AGV.

**Stop or Escalate If:**

* The robot ID cannot be confirmed.
* The intended AGV cannot be identified.

---

### Step 3 — Submit the active-command request

**Responsible role:** L2_support

**Instruction:**
Submit the POST ExecutedAgvCommand request in the OptiSweep / WCS API client with the confirmed robot ID.

**Expected result:**
The POST request is submitted for the selected AGV.

**Stop or Escalate If:**

* The request cannot be submitted.

---

### Step 4 — Verify active-command execution

**Responsible role:** L2_support

**Instruction:**
Use the live AGV status or movement view, including the OptiSweep / WCS API AGV status information when available, to verify that the selected AGV executes its active command.

**Expected result:**
The selected AGV's live status or movement shows execution or progression of the active command.

**Stop or Escalate If:**

* The AGV does not execute its active command.
* The live AGV status or movement view does not show execution or progression.

---

## Success Criteria

* The POST ExecutedAgvCommand request is submitted with a confirmed robot ID.
* The selected AGV executes or progresses its active command on the live AGV status or movement view.

## Failure Conditions

* The ExecutedAgvCommand operation is unavailable.
* The robot ID is missing or cannot be confirmed.
* The request cannot be submitted.
* The AGV does not execute or progress its active command.

## Escalation Guidance

* Escalate to L3_support if the request cannot be submitted.
* Escalate to L3_support if the AGV does not execute or progress its active command after the request.
* Do not substitute a manually entered or replacement command; no such procedure is provided by the source.

## Missing Details / Known Gaps

* The source does not provide the API request body schema beyond the required robot ID.
* The source does not provide response fields, response status values, or a defined command-state value for confirming execution.
* The source does not identify a specific live AGV status or movement screen for verification.
* The source does not define a retry, replacement-command, or manual-command-entry procedure.
* Production-stop and LOTO requirements are not specified.

## Source Lineage

- Candidate IDs: candidate_training_video_execute_active_agv_command_via_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
