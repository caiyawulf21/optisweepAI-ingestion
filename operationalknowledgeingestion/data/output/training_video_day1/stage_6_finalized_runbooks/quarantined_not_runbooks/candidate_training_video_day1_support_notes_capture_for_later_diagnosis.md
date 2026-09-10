# Capture enough observations during the incident to diagnose later while focusing on getting the system back running

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_capture_observations_for_later_diagnosis_restore_v1` |
| Title | Capture enough observations during the incident to diagnose later while focusing on getting the system back running |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `gateway_health`, `wcs_api_responsiveness` |
| Access Surface | `rms_ui`, `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

During a P1 incident, support should prioritize restoring operation and, in parallel, capture enough observable evidence for later diagnosis—rather than attempting full root-cause determination in real time.

## When To Use

Use during a high-severity (P1) incident when the system is not running and you need to both (1) restore operation quickly and (2) collect sufficient observations for later diagnosis.

## Access Or Tools Needed

* RMS screen access
* WCS/OptiSweep state visibility (as available via the supported surfaces mentioned in the source)
* Operator access for Aviva observations (when direct Aviva access is unavailable)
* Support note-taking/ticketing (implied by the source emphasis on capturing notes)

## Related Operational Context

* ctx_training_video_support_focus_notes_and_restore_v1

## Procedure Steps

### Step 1 — Prioritize restoring operation while preparing for later diagnosis

**Responsible role:** L1_support

**Instruction:**
During the call, keep the primary objective on restoring operation (how can we get the system back and running?), and in parallel capture enough observations for later diagnosis.

**Expected result:**
You have a running plan to restore operation and you are actively collecting incident observations (not attempting full 100% diagnosis in real time).

---

### Step 2 — Check RMS first for system faults

**Responsible role:** L1_support

**Instruction:**
On the phone call, go to the RMS screen first and check whether there are any system faults.

**Expected result:**
RMS is checked and you have an observable answer to whether RMS shows system faults.

---

### Step 3 — Use operator-provided Aviva observations when direct Aviva access is unavailable

**Responsible role:** L1_support

**Instruction:**
If you do not have access to Aviva, ask the operator to look in Aviva and tell you what they are seeing (so you can capture the Aviva-observable action/status for later diagnosis).

**Expected result:**
You have Aviva-observable information captured via the operator (since direct Aviva access is not available).

---

### Step 4 — Compare Aviva-reported action with WCS/OptiSweep system state

**Responsible role:** L1_support

**Instruction:**
When there is an issue between OPC and Aviva (or when Aviva triggers an action), check the WCS/OptiSweep state to see whether the system state matches the Aviva-reported action. If Aviva indicates a state change (e.g., startup) but WCS/OptiSweep does not show it, treat it as a communication issue and capture that mismatch as evidence.

**Expected result:**
Your notes include (a) what Aviva indicates and (b) what WCS/OptiSweep state shows, including whether the expected state change is present or missing.

---

## Success Criteria

* RMS system faults were checked and recorded as part of the call evidence.
* Aviva-observable information was captured via the operator when direct Aviva access was unavailable.
* A comparison was recorded between Aviva-indicated action/status and the observed WCS/OptiSweep system state (including any mismatch).
* The team focused on restoring operation while collecting sufficient evidence for later diagnosis (not full 100% diagnosis in real time).

## Failure Conditions

* RMS system faults were not checked or not recorded.
* Aviva observations were not captured (and direct Aviva access was unavailable).
* No Aviva vs WCS/OptiSweep state comparison was recorded, preventing later diagnosis.
* The incident response attempts full root-cause diagnosis in real time instead of restoring operation under P1 SLA pressure.

## Escalation Guidance

* If the system cannot be brought back running within the SLA pressure described for P1 incidents, escalate (the source frames this as a firefight due to UPS 4-hour SLA on P1s).
* If evidence capture is incomplete, later diagnosis may be delayed—ensure at minimum the source-backed evidence points (RMS faults, Aviva observations via operator, and Aviva vs WCS/OptiSweep state match/mismatch) are recorded.

## Missing Details / Known Gaps

* The packet does not provide a concrete checklist for what exact fields/labels to record from RMS, Aviva, or WCS/OptiSweep beyond the high-level evidence points (RMS system faults, Aviva observations via operator, and Aviva vs WCS/OptiSweep state match/mismatch).
* The packet does not provide explicit WCS/OptiSweep UI/API surface names or specific query steps to retrieve the 'state of the system'—only the instruction to check WCS or OptiSweep state.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_support_focus_notes_capture_for_later_diagnosis
- Source ID: `training_video_day1`
- Source Type: `training_video`
