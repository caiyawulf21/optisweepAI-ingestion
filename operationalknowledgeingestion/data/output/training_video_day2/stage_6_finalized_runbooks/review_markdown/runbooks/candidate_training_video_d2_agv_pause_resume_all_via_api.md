# Pause and resume all AGV movement using PauseAGVs / ResumeAGVs API requests

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_pause_resume_all_agv_movement_pauseagvs_resumeagvs_v1` |
| Title | Pause and resume all AGV movement using PauseAGVs / ResumeAGVs API requests |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API client (Apidog / WCS API) to send fleet-level PauseAGVs and ResumeAGVs requests to Geek. PauseAGVs pauses all AGV movement; ResumeAGVs resumes the paused AGVs. Confirm each request shows an observable success/acceptance result in the API client.

## When To Use

When you need to pause all AGV movement fleet-wide (PauseAGVs) or resume the paused fleet (ResumeAGVs) by sending the correct API request to Geek, and you can observe the request/response outcome in the OptiSweep / WCS API client.

## Safety And Operational Notes

* This procedure is a fleet-level movement pause/resume action via API requests to Geek.

## Access Or Tools Needed

* Apidog / WCS API client (or equivalent OptiSweep / WCS API client surface)

## Related Operational Context

* ctx_training_video_agv_api_pause_resume_v1

## Visual References

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*Frame showing the API function behavior text: PauseAGVs makes a request to Geek to pause all AGV movement; ResumeAGVs makes a request to Geek to resume all AGV movement.*

## Procedure Steps

### Step 1 — Select the PauseAGVs API action and confirm it pauses all AGV movement

**Responsible role:** L2_support

**Instruction:**
On the OptiSweep / WCS API client surface (Apidog / WCS API), select the API action named PauseAGVs and confirm it is described as making a request to Geek to pause all AGV movement.

**Expected result:**
The API client is set to the PauseAGVs action, and the action description indicates it will make a request to Geek to pause all AGV movement.

---

### Step 2 — Submit the PauseAGVs request

**Responsible role:** L2_support

**Instruction:**
Submit the PauseAGVs request from the OptiSweep / WCS API client (Apidog / WCS API).

**Expected result:**
The PauseAGVs request is sent from the API client and a request/response result is displayed.

**Stop or Escalate If:**

* If PauseAGVs fails in the API client, stop and escalate for deeper API/Geek-side troubleshooting rather than repeating.

---

### Step 3 — Verify PauseAGVs request success/acceptance in the API client

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client (Apidog / WCS API), verify the PauseAGVs request shows an observable success/acceptance result for the request.

**Expected result:**
The API client displays an observable success/acceptance result for the PauseAGVs request.

**Stop or Escalate If:**

* If PauseAGVs fails in the API client, stop and escalate for deeper API/Geek-side troubleshooting rather than repeating.

---

### Step 4 — Select the ResumeAGVs API action and confirm it resumes all paused AGV movement

**Responsible role:** L2_support

**Instruction:**
On the OptiSweep / WCS API client surface (Apidog / WCS API), select the API action named ResumeAGVs and confirm it is described as making a request to Geek to resume all AGV movement.

**Expected result:**
The API client is set to the ResumeAGVs action, and the action description indicates it will make a request to Geek to resume all AGV movement.

---

### Step 5 — Submit the ResumeAGVs request

**Responsible role:** L2_support

**Instruction:**
Submit the ResumeAGVs request from the OptiSweep / WCS API client (Apidog / WCS API).

**Expected result:**
The ResumeAGVs request is sent from the API client and a request/response result is displayed.

**Stop or Escalate If:**

* If ResumeAGVs fails in the API client, stop and escalate for deeper API/Geek-side troubleshooting rather than repeating.

---

### Step 6 — Verify ResumeAGVs request success/acceptance in the API client

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client (Apidog / WCS API), verify the ResumeAGVs request shows an observable success/acceptance result for the request.

**Expected result:**
The API client displays an observable success/acceptance result for the ResumeAGVs request.

**Stop or Escalate If:**

* If ResumeAGVs fails in the API client, stop and escalate for deeper API/Geek-side troubleshooting rather than repeating.

---

## Success Criteria

* PauseAGVs request is executed and the API client shows an observable success/acceptance result for the request.
* ResumeAGVs request is executed and the API client shows an observable success/acceptance result for the request.

## Failure Conditions

* API client shows an error/failed outcome for PauseAGVs.
* API client shows an error/failed outcome for ResumeAGVs.

## Escalation Guidance

* If PauseAGVs or ResumeAGVs fails in the API client, stop and escalate for deeper API/Geek-side troubleshooting rather than repeating.

## Missing Details / Known Gaps

* The packet does not include a captured Apidog request/response screen showing the exact success/error indicators to look for; step verification is therefore limited to confirming that the API client shows an observable success/acceptance result.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_agv_pause_resume_all_via_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
