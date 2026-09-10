# Pause All AGV Movement Through the OptiSweep WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_pause_all_agv_movement_through_optisweep_wcs_api_v1` |
| Title | Pause All AGV Movement Through the OptiSweep WCS API |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `robot_command_or_task_state` |
| Access Surface | `wcs_api`, `apidog`, `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API PauseAgvs operation in Apidog or an equivalent WCS API client to request that Geek pause movement for all AGVs. PauseAgvs is not an AE stop.

## When To Use

Use when support needs to request a pause of movement for all AGVs through the live OptiSweep / WCS API.

## Do Not Use For

* Do not use or describe PauseAgvs as an AE stop.
* Do not use this procedure as a physical E-stop procedure.

## Safety And Operational Notes

* PauseAgvs requests Geek to pause all AGV movement; the source explicitly distinguishes this operation from an AE stop.
* Treat the operation as a software request to Geek, not as a physical safety stop.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog or equivalent WCS API client
* AGVs API operation labeled PauseAgvs
* Live AGV fleet status UI or live movement observation

## Related Operational Context

* ctx_training_video_pause_resume_agv_movement_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep API overview showing the AGVs API group and PauseAgvs operation in Apidog.*

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*AGVs API screen identifying POST PauseAgvs and its effect of requesting Geek to pause all AGV movement; it also distinguishes the operation from AE.*

![artifact_training_video_training_video_day2_0030_get_agv_status_shows_the_current_primary_02_43_04_500](assets/30f5c770747ce298.jpg)

*AGVs status view showing live AGV state, current command, vitals, AGV errors, and system errors for post-request verification.*

## Procedure Steps

### Step 1 — Open the PauseAgvs operation in the OptiSweep / WCS API client

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent OptiSweep / WCS API client, open the AGVs API group and locate the operation labeled POST PauseAgvs.

**Expected result:**
The AGVs API group displays the POST PauseAgvs operation and it is available for submission.

**Stop or Escalate If:**

* The OptiSweep / WCS API client cannot be reached.
* POST PauseAgvs is not available.

---

### Step 2 — Submit POST PauseAgvs

**Responsible role:** L2_support

**Instruction:**
Submit the POST PauseAgvs request in the OptiSweep / WCS API client. Do not represent or handle this request as an AE stop.

**Expected result:**
The POST PauseAgvs request is submitted to request that Geek pause all AGV movement.

**Stop or Escalate If:**

* The POST PauseAgvs request cannot be submitted.
* The operation is being treated as an AE stop or another safety-stop function.

---

### Step 3 — Verify the live AGV movement state

**Responsible role:** L2_support

**Instruction:**
Observe the live AGV fleet status in the RMS / fleet status UI or equivalent live AGV status view after submitting PauseAgvs. Check the current AGV state, current command, vitals, and any AGV or system errors, and confirm that AGV movement is paused.

**Expected result:**
The live fleet observation shows that AGV movement is paused; the status view remains available for reviewing current AGV state, command, vitals, and errors.

**Stop or Escalate If:**

* AGV movement continues after the PauseAgvs request.
* The live AGV state cannot be observed or the pause cannot be verified.
* The status view shows an AGV error or system error associated with the request.

---

## Success Criteria

* POST PauseAgvs is submitted through the OptiSweep / WCS API.
* Geek receives a request to pause movement for all AGVs.
* Live AGV observation confirms that AGV movement is paused.
* The operation is recorded and communicated as a software pause request, not an AE stop.

## Failure Conditions

* The OptiSweep / WCS API or Apidog client is unavailable.
* POST PauseAgvs cannot be submitted.
* AGV movement continues after the request.
* The live AGV status view cannot confirm the paused state.
* The operation is incorrectly treated as an AE stop.

## Escalation Guidance

* Escalate if the request cannot be submitted through the OptiSweep / WCS API.
* Escalate if AGV movement continues after POST PauseAgvs.
* Escalate if live AGV or system errors prevent verification of the paused state.
* Use the appropriate physical safety response separately if an AE stop is required; PauseAgvs is not an AE stop.

## Missing Details / Known Gaps

* The source does not provide an API response code or response body for POST PauseAgvs.
* The source does not identify a specific paused-state field or status value in the live AGV status view.
* The source does not define a timeout for confirming that all AGV movement has paused.
* A specific RMS fleet-status screen or equivalent live movement screen for confirming the paused state is not supplied.

## Source Lineage

- Candidate IDs: candidate_training_video_pause_all_agvs_via_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
