# Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` |
| Title | Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state`, `wcs_api_responsiveness` |
| Access Surface | `apidog`, `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API client to send a Geek request to remove a specified AGV from the system (RemoveAgv) or re-add it (RecoverAGV). Both API actions require the target robot ID.

## When To Use

When you need to remove a specific AGV from the system roster (RemoveAgv) or re-add it (RecoverAGV) by sending the correct OptiSweep→Geek API request using the required robot ID.

## Do Not Use For

* Do not use this procedure as a substitute for identifying the correct robot ID; if the robot ID is incorrect/missing, the request cannot target the intended AGV.

## Access Or Tools Needed

* Apidog / WCS API client (or equivalent OptiSweep / WCS API client surface)

## Related Operational Context

* ctx_training_video_agv_api_remove_recover_v1

## Visual References

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*API action definitions: RemoveAgv requires robot ID and sends a request to Geek to remove the specified AGV; RecoverAGV requires robot ID and sends a request to Geek to add the specified AGV.*

## Procedure Steps

### Step 1 — Identify the target AGV robot ID for the API request

**Responsible role:** L2_support

**Instruction:**
Obtain the target AGV's robot ID that you will enter into the OptiSweep / WCS API request.

**Expected result:**
You have a specific robot ID value ready to use for the RemoveAgv and RecoverAGV requests.

**Stop or Escalate If:**

* If the robot ID is incorrect or missing, do not submit RemoveAgv/RecoverAGV; confirm the robot ID before retrying.

---

### Step 2 — Select RemoveAgv in the OptiSweep / WCS API client and confirm it targets Geek removal by robot ID

**Responsible role:** L2_support

**Instruction:**
In the Apidog / WCS API client, select the API action named RemoveAgv and confirm it is described as requiring the robot ID and sending a request to Geek to remove the specified AGV from the system.

**Expected result:**
The RemoveAgv action is selected in the API client and is associated with the robot ID input requirement.

**Stop or Escalate If:**

* If the selected API action is not RemoveAgv (or does not require robot ID as described), stop and correct the selection before submitting.

---

### Step 3 — Submit RemoveAgv request with the target robot ID

**Responsible role:** L2_support

**Instruction:**
Submit the RemoveAgv request in the Apidog / WCS API client using the target robot ID you identified.

**Expected result:**
The RemoveAgv request is submitted and you receive an observable API client response indicating acceptance/execution (success or error).

**Stop or Escalate If:**

* If the API client shows an error/failed request for RemoveAgv, stop and escalate to deeper API/roster troubleshooting rather than repeating blindly.

---

### Step 4 — Verify RemoveAgv request corresponds to intended action and response indicates acceptance/success

**Responsible role:** L2_support

**Instruction:**
Review the RemoveAgv request/response in the Apidog / WCS API client and verify the response indicates acceptance/execution (success vs error).

**Expected result:**
The API client response for RemoveAgv shows an observable success/acceptance indicator (or an error indicator if it failed).

**Stop or Escalate If:**

* If the API client shows an error/failed request for RemoveAgv, stop and escalate to deeper API/roster troubleshooting rather than repeating blindly.

---

### Step 5 — Select RecoverAGV in the OptiSweep / WCS API client and confirm it targets Geek add by robot ID

**Responsible role:** L2_support

**Instruction:**
In the Apidog / WCS API client, select the API action named RecoverAGV and confirm it is described as requiring the robot ID and sending a request to Geek to add the specified AGV to the system.

**Expected result:**
The RecoverAGV action is selected in the API client and is associated with the robot ID input requirement.

**Stop or Escalate If:**

* If the selected API action is not RecoverAGV (or does not require robot ID as described), stop and correct the selection before submitting.

---

### Step 6 — Submit RecoverAGV request with the same target robot ID

**Responsible role:** L2_support

**Instruction:**
Submit the RecoverAGV request in the Apidog / WCS API client using the same robot ID used for RemoveAgv.

**Expected result:**
The RecoverAGV request is submitted and you receive an observable API client response indicating acceptance/success (or error).

**Stop or Escalate If:**

* If the API client shows an error/failed request for RecoverAGV, stop and escalate to deeper API/roster troubleshooting rather than repeating blindly.

---

### Step 7 — Verify RecoverAGV request corresponds to intended action and response indicates acceptance/success

**Responsible role:** L2_support

**Instruction:**
Review the RecoverAGV request/response in the Apidog / WCS API client and verify the response indicates acceptance/execution (success vs error).

**Expected result:**
The API client response for RecoverAGV shows an observable success/acceptance indicator (or an error indicator if it failed).

**Stop or Escalate If:**

* If the API client shows an error/failed request for RecoverAGV, stop and escalate to deeper API/roster troubleshooting rather than repeating blindly.

---

## Success Criteria

* RemoveAgv request is accepted/executed for the specified robot ID (observable success/acceptance in the API client response).
* RecoverAGV request is accepted/executed for the same robot ID (observable success/acceptance in the API client response).

## Failure Conditions

* API client response indicates RemoveAgv failed/error.
* API client response indicates RecoverAGV failed/error.
* Robot ID is incorrect or missing (request cannot target intended AGV).

## Escalation Guidance

* If RemoveAgv or RecoverAGV fails in the API client, stop and escalate to deeper API/roster troubleshooting rather than repeating blindly.

## Missing Details / Known Gaps

* The packet does not include a live Apidog request/response screenshot showing the exact success/error fields or indicators to look for; steps 4 and 7 therefore rely on the general requirement to verify observable success/acceptance vs error in the API client response.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_agv_remove_recover_via_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
