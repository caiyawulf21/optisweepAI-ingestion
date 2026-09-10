# Resume all AGV movement via Geek request (ResumeAgvs)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resume_all_agv_movement_via_geek_resumeagvs_v1` |
| Title | Resume all AGV movement via Geek request (ResumeAgvs) |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery`, `robot_command_or_task_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Send the fleet-level ResumeAgvs request to Geek to resume all paused AGV movement.

## When To Use

Use when AGV movement is paused at the fleet level and you need to resume all AGVs by issuing the ResumeAgvs request to Geek.

## Access Or Tools Needed

* OptiSweep APIs (AGVs) ResumeAgvs function
* Geek (Geek Plus) request capability
* API client capability to send the documented ResumeAgvs request

## Related Operational Context

* ctx_training_video_agv_api_pause_resume_v1

## Visual References

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*Frame listing AGVs API functions including PauseAGVs and ResumeAGVs and describing that ResumeAGVs sends a request to Geek to resume all AGV movement.*

## Procedure Steps

### Step 1 — Send the ResumeAgvs request to Geek to resume all AGV movement

**Responsible role:** L2_support

**Instruction:**
Using the OptiSweep APIs (AGVs) ResumeAgvs function, send the fleet-level ResumeAgvs request to Geek to resume all AGV movement.

**Expected result:**
A ResumeAgvs request is issued to Geek for resuming all AGV movement.

**Stop or Escalate If:**

* If you cannot access the ResumeAgvs request function, escalate to support.

---

### Step 2 — Verify the resume request was issued and movement resumes

**Responsible role:** L2_support

**Instruction:**
Confirm evidence shows the ResumeAgvs request being sent, and verify that AGV movement resumes after the request.

**Expected result:**
Geek receives the ResumeAgvs request and all AGV movement resumes.

**Stop or Escalate If:**

* If movement does not resume after the request, escalate for deeper troubleshooting of the Geek request/response path.

---

## Success Criteria

* Evidence shows the ResumeAgvs request was sent to Geek.
* All AGV movement resumes after the ResumeAgvs request.

## Failure Conditions

* ResumeAgvs request cannot be accessed/issued.
* Movement does not resume after the ResumeAgvs request.

## Escalation Guidance

* Escalate if you cannot access the ResumeAgvs request function.
* Escalate for deeper troubleshooting of the Geek request/response path if movement does not resume after the request.

## Missing Details / Known Gaps

* The source does not provide a specific on-screen indicator or verification surface for confirming that all AGV movement resumed after ResumeAgvs.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_resume_all_agvs_via_geek_resumeagvs
- Source ID: `training_video_day2`
- Source Type: `training_video`
