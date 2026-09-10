# Recover a Specified AGV Through the OptiSweep WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_specified_agv_through_optisweep_wcs_api_v1` |
| Title | Recover a Specified AGV Through the OptiSweep WCS API |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors`, `robot_command_or_task_state` |
| Access Surface | `apidog`, `wcs_api` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | `api_unresponsive`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog or an equivalent WCS API client to submit the POST RecoverAgv operation with a confirmed robot ID. RecoverAgv requests Geek to add the specified AGV back into the system. Verify the result with the Get Agv Statuses request.

## When To Use

Use when a specified AGV must be added back into the OptiSweep system through the Geek Plus recovery path and a confirmed robot ID is available.

## Do Not Use For

* Do not use without a confirmed robot ID.
* Do not use as a physical AGV recovery or E-stop procedure.
* Do not use to infer success from request submission alone; verify the AGV in Get Agv Statuses.

## Safety And Operational Notes

* Confirm the robot ID before submitting the RecoverAgv request.
* Stop and escalate if the API request cannot be submitted or the specified AGV does not reappear in the system state.

## Access Or Tools Needed

* Apidog or equivalent WCS API client on the primary server
* OptiSweep / WCS API access
* AGVs API operations
* POST RecoverAgv operation
* Confirmed robot ID
* GET Get Agv Statuses operation for verification

## Related Operational Context

* ctx_training_video_remove_recover_agv_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*Apidog / WCS API overview showing the AGVs API group and available operations, including POST RecoverAgv and GET Get Agv Statuses.*

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*AGVs API view showing POST RecoverAgv and the requirement for a robot ID to add the specified AGV to the system.*

![artifact_training_video_training_video_day2_0030_get_agv_status_shows_the_current_primary_02_43_04_500](assets/30f5c770747ce298.jpg)

*AGV status result showing the fields returned by Get Agv Statuses, including name, state, command status, battery, status, and error fields.*

## Procedure Steps

### Step 1 — Open the RecoverAgv operation in Apidog

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent OptiSweep / WCS API client, open the AGVs API group and locate the POST RecoverAgv operation.

**Expected result:**
The AGVs API list displays the POST RecoverAgv operation and it is available for submission.

**Stop or Escalate If:**

* The POST RecoverAgv operation is not available.
* The API client cannot open or submit the operation.

---

### Step 2 — Enter the confirmed robot ID

**Responsible role:** L2_support

**Instruction:**
In the POST RecoverAgv request in the Apidog / WCS API client, provide the confirmed robot ID for the specified AGV.

**Expected result:**
The RecoverAgv request contains the robot ID for the intended AGV and is ready for submission.

**Stop or Escalate If:**

* The robot ID cannot be confirmed.
* The request does not provide a way to specify the robot ID.

---

### Step 3 — Submit the POST RecoverAgv request

**Responsible role:** L2_support

**Instruction:**
Submit the POST RecoverAgv request in the Apidog / WCS API client after confirming that the intended robot ID is present.

**Expected result:**
The POST RecoverAgv request is submitted for the specified robot ID.

**Stop or Escalate If:**

* The request cannot be submitted.
* The robot ID is not confirmed before submission.

---

### Step 4 — Verify the AGV in Get Agv Statuses

**Responsible role:** L2_support

**Instruction:**
Use the GET Get Agv Statuses operation in the Apidog / WCS API client and inspect the returned AGV entries for the specified robot ID. Review the returned name, state, command status, battery, status, errorCode, errorDescription, errorCause, systemErrorDescription, systemErrorResolution, and errorAlert fields when present.

**Expected result:**
The returned AGV status data contains an entry for the specified robot ID, representing the AGV again in the system state.

**Stop or Escalate If:**

* The specified AGV does not reappear in the returned system state.
* The returned status shows an AGV error or system error that is not resolved by the recovery request.

---

## Success Criteria

* The POST RecoverAgv request is submitted with the confirmed robot ID.
* Get Agv Statuses returns an entry for the specified robot ID.
* The specified AGV is represented again in the OptiSweep system state.
* The returned AGV status does not show an unresolved error condition that prevents recovery confirmation.

## Failure Conditions

* The POST RecoverAgv operation is unavailable or cannot be submitted.
* The robot ID is missing or cannot be confirmed.
* The specified robot ID does not reappear in Get Agv Statuses.
* The returned AGV status indicates an unresolved error or system error.

## Escalation Guidance

* Escalate to L3_support if the POST RecoverAgv request cannot be submitted.
* Escalate to L3_support if the specified AGV does not reappear in Get Agv Statuses.
* Include the specified robot ID and the returned AGV status or error fields when escalating, if available.

## Missing Details / Known Gaps

* The source does not provide the exact RecoverAgv request body or parameter field syntax.
* The source does not provide the API endpoint URL, authentication procedure, or HTTP response code.
* The source does not define how long to wait before checking Get Agv Statuses.
* The source does not specify whether a returned AGV state must be a particular state to constitute successful recovery.
* The source does not define a detailed remediation path for an AGV that remains absent or reports an error after RecoverAgv.

## Source Lineage

- Candidate IDs: candidate_training_video_recover_agv_via_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
