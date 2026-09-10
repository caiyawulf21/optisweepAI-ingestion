# Use System API action “System State” to retrieve the current system state

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_system_api_action_system_state_v1` |
| Title | Use System API action “System State” to retrieve the current system state |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the System API action labeled “System State” to retrieve the current state of the OptiSweep system. The returned value(s) can be used to determine whether the system is in a shutdown state versus a running state.

## When To Use

When you need to check the current OptiSweep system state (e.g., to understand whether the system is in a shutdown state or a running state) using the System API action “System State”.

## Access Or Tools Needed

* System API interface that exposes the action labeled “System State”.

## Related Operational Context

* ctx_training_video_system_api_actions_overview_v1
* ctx_training_video_status_system_state_startup_shutdown_v1

## Visual References

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*Training video frame showing the System API actions list including “System State” and related actions (System Startup / System Shutdown).*

## Procedure Steps

### Step 1 — Identify the System API action labeled “System State”

**Responsible role:** L1_support

**Instruction:**
In the System API interface, locate the action labeled “System State”.

**Expected result:**
The “System State” action is identified and ready to be executed in the System API interface.

---

### Step 2 — Run “System State” to retrieve the current state of the system

**Responsible role:** L1_support

**Instruction:**
Execute the System API action labeled “System State” and capture the returned current system state value(s).

**Expected result:**
The API returns the current system state.

**Stop or Escalate If:**

* If the system state cannot be retrieved, stop and escalate (no troubleshooting steps are provided in the source).

---

### Step 3 — Interpret the returned system state as shutdown vs running

**Responsible role:** L1_support

**Instruction:**
Review the returned current system state value(s) from “System State” and classify the system as being in a shutdown state versus a running state.

**Expected result:**
You can determine whether the system is in a shutdown state or a running state based on the returned current system state value(s).

**Stop or Escalate If:**

* If the system state cannot be retrieved, stop and escalate (no troubleshooting steps are provided in the source).

---

## Success Criteria

* The “System State” API action returns the current system state.
* The returned current system state can be classified as shutdown vs running using the source’s described categories.

## Failure Conditions

* System state cannot be retrieved from the “System State” action.
* Returned system state value(s) are missing/blank or cannot be classified as shutdown vs running.

## Escalation Guidance

* If the system state cannot be retrieved, stop and escalate. The source provides no additional troubleshooting steps.

## Missing Details / Known Gaps

* The source does not provide the exact field names/values returned by “System State”, so the specific shutdown vs running mapping criteria are not enumerated.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_system_state_api_action
- Source ID: `training_video_day2`
- Source Type: `training_video`
