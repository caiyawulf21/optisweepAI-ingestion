# Resume All AGV Movement Through the OptiSweep WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resume_all_agv_movement_through_optisweep_wcs_api_v1` |
| Title | Resume All AGV Movement Through the OptiSweep WCS API |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `rms_soft_stop` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | `api_unresponsive`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog or an equivalent WCS API client to submit the POST ResumeAgvs operation, which requests Geek to resume movement for all paused AGVs. Verify the resulting fleet state through the WCS API AGV status view.

## When To Use

Use when all AGV movement was paused through the OptiSweep / WCS API and movement needs to be resumed through the live WCS API surface.

## Do Not Use For

* Do not use ResumeAgvs as a physical E-stop reset.
* Do not use this procedure for physical AGV recovery or physical safety-stop reset.

## Safety And Operational Notes

* ResumeAgvs requests Geek to resume all AGV movement; it is not a physical E-stop reset.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog or equivalent WCS API client
* AGVs API operation labeled ResumeAgvs
* WCS API AGV status view, including Get Agv Statuses

## Related Operational Context

* ctx_training_video_pause_resume_agv_movement_v1

## Visual References

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*OptiSweep / WCS API AGVs view showing the POST ResumeAgvs operation and its description that it requests Geek to resume all AGV movement.*

![artifact_training_video_training_video_day2_0030_get_agv_status_shows_the_current_primary_02_43_04_500](assets/30f5c770747ce298.jpg)

*OptiSweep / WCS API AGV status view showing current AGV state, command, vitals, AGV errors, system errors, status, and errorAlert fields.*

## Procedure Steps

### Step 1 — Locate ResumeAgvs in the OptiSweep / WCS API

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent OptiSweep / WCS API client, open the AGVs API operations and locate the operation labeled POST ResumeAgvs.

**Expected result:**
The AGVs API list displays POST ResumeAgvs and identifies it as the operation that requests Geek to resume all AGV movement.

**Stop or Escalate If:**

* Stop and escalate if the WCS API client cannot display or locate POST ResumeAgvs.

---

### Step 2 — Submit the POST ResumeAgvs request

**Responsible role:** L2_support

**Instruction:**
Submit the POST ResumeAgvs request in Apidog or the equivalent OptiSweep / WCS API client.

**Expected result:**
The POST ResumeAgvs request is submitted to request that Geek resume all AGV movement.

**Stop or Escalate If:**

* Stop and escalate if the POST ResumeAgvs request cannot be submitted.

---

### Step 3 — Verify the live AGV fleet state

**Responsible role:** L2_support

**Instruction:**
Use the OptiSweep / WCS API AGV status view, including Get Agv Statuses, and observe the current AGV state, command, commandStatus, status, errorCode, errorDescription, errorCause, systemErrorDescription, systemErrorResolution, and errorAlert. Confirm through the available live fleet observation that AGV movement has resumed.

**Expected result:**
The live AGV status view reflects resumed movement for the previously paused fleet and provides current AGV state and error information for verification.

**Stop or Escalate If:**

* Stop and escalate if AGV movement remains paused after the ResumeAgvs request.
* Stop and escalate if current AGV status cannot be retrieved.
* Stop and escalate if the live status view shows an active AGV or system error preventing movement.

---

## Success Criteria

* POST ResumeAgvs is submitted successfully through the OptiSweep / WCS API.
* The request is intended to resume all paused AGV movement through Geek.
* The live WCS API AGV status view is available for verification.
* AGV movement resumes and no active AGV or system error is preventing movement.

## Failure Conditions

* POST ResumeAgvs cannot be located or submitted.
* Current AGV status cannot be retrieved through the WCS API.
* AGV movement remains paused after the request.
* The AGV status view shows an active AGV or system error preventing movement.

## Escalation Guidance

* Stop and escalate if the ResumeAgvs request cannot be submitted.
* Stop and escalate if AGV movement remains paused after the request.
* Stop and escalate if the live AGV status view cannot be retrieved or shows an active AGV or system error.

## Missing Details / Known Gaps

* The source does not provide an API response code or response-body confirmation for POST ResumeAgvs.
* The source does not identify a specific resumed-state field or exact movement-observation criterion beyond the live AGV status and movement observation.
* The source does not provide the API endpoint URL, authentication procedure, request body requirements, or timeout behavior.
* The source does not establish whether production movement must be stopped or whether LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_resume_all_agvs_via_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
