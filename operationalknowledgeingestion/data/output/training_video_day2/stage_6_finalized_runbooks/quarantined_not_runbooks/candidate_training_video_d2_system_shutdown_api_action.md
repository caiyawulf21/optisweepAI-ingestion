# Use System API action “System Shutdown” to shut down the system when in running state

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_system_api_action_system_shutdown_to_shut_down_v1` |
| Title | Use System API action “System Shutdown” to shut down the system when in running state |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the System API action labeled “System Shutdown” to shut down the system when the system is currently in a running state. Confirm the current system state using “System State”.

## When To Use

When the system is in a running state and you need to shut it down using the System API action “System Shutdown”.

## Access Or Tools Needed

* System API interface that exposes the “System Shutdown” action
* System API interface that exposes “System State”

## Related Operational Context

* ctx_training_video_system_api_actions_overview_v1
* ctx_training_video_status_system_state_startup_shutdown_v1

## Visual References

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*Frame showing the System API actions list including “System Shutdown” and “System State”.*

## Procedure Steps

### Step 1 — Identify the System API action labeled “System Shutdown”

**Responsible role:** L1_support

**Instruction:**
In the System API interface, locate the action control labeled “System Shutdown”.

**Expected result:**
You have located the “System Shutdown” action label/control in the System API interface.

---

### Step 2 — Run “System Shutdown” to shut down the system if it is in a running state

**Responsible role:** L1_support

**Instruction:**
Execute the System API action “System Shutdown”.

**Expected result:**
The system transitions from running toward shutdown as implied by the “System Shutdown” behavior being conditional on the system being in a running state.

**Stop or Escalate If:**

* If the system does not shut down as expected, stop and escalate.

---

### Step 3 — Confirm the system is in shutdown state by checking “System State”

**Responsible role:** L1_support

**Instruction:**
Use the System API action “System State” to retrieve the current system state and confirm it reflects shutdown (i.e., not running).

**Expected result:**
“System State” indicates the system is in shutdown state after “System Shutdown” is executed.

**Stop or Escalate If:**

* If the system does not shut down as expected, stop and escalate.

---

## Success Criteria

* After executing “System Shutdown”, “System State” indicates the system is in shutdown state (i.e., not running).

## Failure Conditions

* The system does not shut down as expected after executing “System Shutdown”.
* “System State” still indicates the system is in a running state after executing “System Shutdown”.

## Escalation Guidance

* If the system does not shut down as expected, stop and escalate (no additional recovery steps are provided in the source).

## Missing Details / Known Gaps

* The source does not specify the exact “System State” value/text that corresponds to shutdown (only that “System State” returns the current state and that “System Shutdown” is for a running state).
* The source does not provide the exact UI/API interaction steps (e.g., click/submit mechanics) beyond identifying the action labels.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_system_shutdown_api_action
- Source ID: `training_video_day2`
- Source Type: `training_video`
