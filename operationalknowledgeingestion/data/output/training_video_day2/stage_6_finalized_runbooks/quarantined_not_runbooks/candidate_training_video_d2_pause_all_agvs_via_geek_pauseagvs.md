# Pause all AGV movement via Geek request (PauseAgvs)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_pause_all_agv_movement_via_geek_pauseagvs_v1` |
| Title | Pause all AGV movement via Geek request (PauseAgvs) |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Send the fleet-level PauseAgvs request to Geek so all AGV movement is paused.

## When To Use

Use when you need to pause all AGV movement by issuing the documented PauseAgvs fleet request to Geek.

## Access Or Tools Needed

* OptiSweep APIs (AGVs) PauseAgvs function
* Geek (Geek Plus) request capability

## Related Operational Context

* ctx_training_video_agv_api_pause_resume_v1

## Visual References

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*Frame showing the AGV API list including PauseAgvs: 'Pause Agvs will make a request to Geek to pause all AGV movement.'*

## Procedure Steps

### Step 1 — Send PauseAgvs request to Geek to pause all AGV movement

**Responsible role:** L2_support

**Instruction:**
Using the OptiSweep AGVs API function named PauseAgvs, send the request to Geek to pause all AGV movement.

**Expected result:**
A PauseAgvs request is issued to Geek for fleet-level pausing of all AGV movement.

**Stop or Escalate If:**

* If you cannot access the PauseAgvs request function, escalate to support.
* If the pause request was not issued (no evidence the PauseAgvs request was sent), escalate for deeper troubleshooting of the Geek request/response path.

---

### Step 2 — Verify the pause request was issued and movement is paused

**Responsible role:** L2_support

**Instruction:**
Verify there is evidence that the PauseAgvs request was sent to Geek, and confirm that all AGV movement is paused after the request.

**Expected result:**
Geek receives the PauseAgvs request and all AGV movement is paused.

**Stop or Escalate If:**

* If movement is not paused after the request, escalate for deeper troubleshooting of the Geek request/response path.

---

## Success Criteria

* PauseAgvs request is issued to Geek.
* All AGV movement is paused after the request.

## Failure Conditions

* PauseAgvs request cannot be accessed or is not issued.
* AGV movement continues despite the PauseAgvs request.

## Escalation Guidance

* If you cannot access the PauseAgvs request function, escalate to support.
* If movement is not paused after the request, escalate for deeper troubleshooting of the Geek request/response path.

## Missing Details / Known Gaps

* The source does not specify a particular live UI/API response field or dashboard indicator to use as the observable verification that 'all AGV movement is paused' (only that evidence should show the PauseAgvs request being sent).

## Source Lineage

- Candidate IDs: candidate_training_video_d2_pause_all_agvs_via_geek_pauseagvs
- Source ID: `training_video_day2`
- Source Type: `training_video`
