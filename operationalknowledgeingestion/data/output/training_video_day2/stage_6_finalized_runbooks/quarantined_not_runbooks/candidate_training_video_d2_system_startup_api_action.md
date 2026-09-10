# Use System API action “System Startup” to start the system when in shutdown state

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_system_api_action_system_startup_to_start_when_shutdown_v1` |
| Title | Use System API action “System Startup” to start the system when in shutdown state |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the System API action labeled “System Startup” to start the OptiSweep system when the system is currently in a shutdown state, then confirm the system state has moved out of shutdown using “System State”.

## When To Use

When the system is in a shutdown state and you need to start it using the System API action “System Startup”.

## Access Or Tools Needed

* System API interface that exposes the “System Startup” action
* System API interface that exposes “System State” for confirmation

## Related Operational Context

* ctx_training_video_system_api_actions_overview_v1
* ctx_training_video_status_system_state_startup_shutdown_v1

## Visual References

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*Frame showing the System API actions list including “System Startup” and “System State”.*

## Procedure Steps

### Step 1 — Identify the System API action labeled “System Startup”

**Responsible role:** L1_support

**Instruction:**
In the System API interface, locate the action/control labeled “System Startup”.

**Expected result:**
The “System Startup” action/control is identified and ready to run in the System API interface.

**Stop or Escalate If:**

* If you cannot locate “System Startup”, stop and escalate (the source does not provide alternate recovery steps).

---

### Step 2 — Run “System Startup” to start the system if it is in a shutdown state

**Responsible role:** L1_support

**Instruction:**
Execute the System API action “System Startup”. Only run it when the system is in a shutdown state.

**Expected result:**
The system transitions from shutdown toward started/running operation (as implied by the conditional behavior of “System startup”).

**Stop or Escalate If:**

* If the system does not start as expected, stop and escalate (no additional recovery steps are provided in the source).

---

### Step 3 — Confirm the system is no longer in shutdown state using “System State”

**Responsible role:** L1_support

**Instruction:**
Use the System API interface to run “System State” and confirm the system state is no longer shutdown.

**Expected result:**
“System State” indicates the system is not in shutdown anymore.

**Stop or Escalate If:**

* If the system does not start as expected (System State still shows shutdown), stop and escalate (the source does not provide additional recovery steps).

---

## Success Criteria

* After executing “System Startup”, “System State” indicates the system is no longer in shutdown state.

## Failure Conditions

* “System State” still indicates shutdown after running “System Startup”.
* The system does not transition from shutdown toward started/running operation after “System Startup”.

## Escalation Guidance

* If the system does not start as expected, stop and escalate. The source does not provide additional recovery steps beyond using “System Startup” and confirming with “System State”.

## Missing Details / Known Gaps

* The source does not specify the exact “System State” value(s) that correspond to shutdown vs started/running, so the precise expected state string/enum cannot be stated from this packet.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_system_startup_api_action
- Source ID: `training_video_day2`
- Source Type: `training_video`
