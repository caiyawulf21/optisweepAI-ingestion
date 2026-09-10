# Use System API action “Cancel Close Out” to cancel closeout exchanges not in progress

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_system_api_cancel_close_out_v1` |
| Title | Use System API action “Cancel Close Out” to cancel closeout exchanges not in progress |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `bag_out_or_closeout_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the System API action “Cancel Close Out” to cancel closeout exchanges that are not currently in progress. The source ties this to scenarios such as a manual bag out, where the system is back up and you want to cancel exchanges that were marked for exchange but are not actively in progress.

## When To Use

Use when the customer has performed a manual bag out and the system is back up/running, and you need to cancel closeout exchanges that are not in progress.

## Access Or Tools Needed

* System API interface that exposes the “Cancel Close Out” action (source mentions API Dog usage for API calls).

## Related Operational Context

* ctx_training_video_system_api_actions_overview_v1
* ctx_training_video_operation_chute_and_closeout_functions_v1

## Visual References

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*Frame showing the System API actions list including “Cancel close out” and its rule: “cancel all close out exchanges that are not in progress.”*

## Procedure Steps

### Step 1 — Identify the System API action labeled “Cancel Close Out”

**Responsible role:** L1_support

**Instruction:**
In the System API interface (API Dog / System API actions surface), locate the action/control labeled “Cancel Close Out”.

**Expected result:**
The “Cancel Close Out” action is identified and selected (not another closeout-related action such as CloseOut or Purge).

**Stop or Escalate If:**

* If you cannot find/confirm the “Cancel Close Out” action label, stop and escalate (no further steps are provided in the source).

---

### Step 2 — Run “Cancel Close Out” to cancel closeout exchanges not in progress

**Responsible role:** L1_support

**Instruction:**
Execute the System API action “Cancel Close Out”.

**Expected result:**
Closeout exchanges that were not in progress are canceled.

**Stop or Escalate If:**

* If closeout exchanges remain active or the system behavior does not match the expected cancellation scope, stop and escalate (no further steps are provided in the source).

---

### Step 3 — Verify cancellation scope: exchanges not in progress are canceled (do not expect in-progress cancellation)

**Responsible role:** L1_support

**Instruction:**
Verify that closeout exchanges that were not in progress are canceled, and that exchanges that are in progress are not expected to be canceled by this action.

**Expected result:**
Closeout exchanges that were not in progress show as canceled; in-progress closeout exchanges are not expected to be canceled by this action.

**Stop or Escalate If:**

* If closeout exchanges remain active or the system behavior does not match the expected cancellation scope, stop and escalate (no further steps are provided in the source).

---

## Success Criteria

* Closeout exchanges that were not in progress are canceled after running “Cancel Close Out”.

## Failure Conditions

* Closeout exchanges remain active when they should have been canceled.
* System behavior suggests the action is canceling exchanges beyond the “not in progress” scope.

## Escalation Guidance

* Stop and escalate if closeout exchanges remain active or the system behavior does not match the expected cancellation scope. The source provides no additional troubleshooting steps.

## Missing Details / Known Gaps

* The source does not provide a live-system method or named status field/model to observe whether a closeout exchange is “in progress” vs “not in progress.”
* The source does not provide the exact API Dog request/response fields or parameters for “Cancel Close Out,” nor how to confirm cancellation via a specific response payload.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_cancel_closeout_api_action
- Source ID: `training_video_day2`
- Source Type: `training_video`
