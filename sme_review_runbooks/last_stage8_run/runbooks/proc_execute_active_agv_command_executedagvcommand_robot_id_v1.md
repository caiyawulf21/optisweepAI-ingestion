# Execute the active AGV command using ExecutedAgvCommand with robot ID

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_execute_active_agv_command_executedagvcommand_robot_id_v1` |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the OptiSweep / WCS API (via Apidog or equivalent) to trigger execution of the AGV’s currently active command for a specific robot ID. This is intended for unplanned restart recovery scenarios where OptiSweep may have missed callbacks from Geek Plus.

## When To Use

When recovering from an unplanned restart where OptiSweep missed callbacks from Geek Plus, and you need to execute the AGV’s currently active command for a specific robot ID.

## Source Procedure References

- proc_execute_active_agv_command_executedagvcommand_robot_id_v1

## Procedure Steps

### Step 1 — Identify the robot ID for the AGV whose active command should be executed

**Responsible role:** L2_support

**Instruction:**
Obtain the robot ID for the AGV that needs its currently active command executed.

**Expected result:**
You have a specific robot ID value to use in the ExecutedAgvCommand request.

---

### Step 2 — Select the ExecutedAgvCommand API action in the OptiSweep / WCS API client

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client surface (Apidog / WCS API), select the API action named ExecutedAgvCommand and confirm it is described as requiring the robot ID and executing the active command the AGV has.

**Expected result:**
The ExecutedAgvCommand action is selected in the API client and is ready to accept the robot ID parameter.

---

### Step 3 — Submit ExecutedAgvCommand with the robot ID

**Responsible role:** L2_support

**Instruction:**
Submit the ExecutedAgvCommand request using the robot ID you identified in Step 1.

**Expected result:**
The API request is sent successfully from the API client with the robot ID included.

---

### Step 4 — Verify observable API acceptance/success for ExecutedAgvCommand

**Responsible role:** L2_support

**Instruction:**
Check the API client response/result for the ExecutedAgvCommand request and verify it shows an observable success/acceptance indicator.

**Expected result:**
The API client shows an observable success/acceptance result for the ExecutedAgvCommand request.

---

## Success Criteria

- ExecutedAgvCommand request is accepted/successful in the API client for the specified robot ID.

## Failure Conditions

- API client response/result for ExecutedAgvCommand indicates failure/error.

## Escalation Guidance

- If ExecutedAgvCommand fails in the API client, stop and escalate for deeper API/robot command-state troubleshooting rather than repeating.

## Missing Details / Known Gaps

- The packet does not provide a live-system method/screenshot for where to obtain the robot ID (Step 1 image support was noted as needed in the candidate).
- The packet does not show a live Apidog request/response example for ExecutedAgvCommand success/error indicators (candidate noted image support needed).
- The packet does not provide an observable live-system confirmation that the AGV actually started executing the active command; the candidate limits expected_result to API acceptance/success.
