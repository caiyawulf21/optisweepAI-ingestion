# Recover an AGV “BUMP” fault (Exception Codes 21057/21060) using RMS

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_agv_bump_fault_exception_21057_21060_using_rms_v1` |
| Title | Recover an AGV “BUMP” fault (Exception Codes 21057/21060) using RMS |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | `L2_support` |
| Support Safe | Yes |
| Capability Tags | None |
| Access Surface | `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When RMS shows an AGV “Bump” fault with Exception Code 21057 or 21060, stop RMS, remove the obstruction that caused the bump/obstacle trigger, hold the AGV RESET button for two seconds to clear the fault, press E-stop again, then resume RMS. Verify the Exception Code is cleared on the RMS “Bump” Fault Screen before resuming normal operation.

## When To Use

Use this procedure when the RMS interface displays an AGV “Bump” fault and the Exception Code shown is 21057 or 21060, indicating a collision bar trigger or obstacle-avoidance trigger that requires RMS-side fault recovery.

## Do Not Use For

* Do not use this procedure as a substitute for physical obstruction removal when the bump/obstacle trigger is caused by an on-grid obstruction; the obstruction must be physically cleared before attempting RESET.
* Do not proceed to resume RMS if the Exception Code remains after the two-second AGV RESET attempt.

## Safety And Operational Notes

* This procedure includes E-stopping RMS (not physical E-stop).

## Access Or Tools Needed

* RMS / fleet status UI (rms_ui)
* Physical access to remove the obstruction on the grid

## Related Operational Context

* ctx_manual_agv_bump_fault_codes_v1
* ctx_manual_agv_bump_fault_screen_v1
* ctx_manual_fault_recovery_prereqs_v1

## Visual References

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*RMS “Bump” Fault Screen showing Exception Code values 21057 and 21060 and the AGV RESET button.*

## Procedure Steps

### Step 1 — Open the RMS “Bump” Fault Screen

**Responsible role:** L2_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the AGV “Bump” Fault Screen (Figure 5-2).

**Expected result:**
The RMS “Bump” Fault Screen is visible with an Exception Code field and the AGV RESET button.

---

### Step 2 — Confirm the Exception Code is 21057 or 21060

**Responsible role:** L2_support

**Instruction:**
On the RMS “Bump” Fault Screen, confirm the displayed Exception Code is one of the following: 21057 or 21060.

**Expected result:**
Exception Code is either 21057 (Robot front collision bar triggers) or 21060 (The robot triggers the obstacle avoidance).

**Stop or Escalate If:**

* If the Exception Code is not 21057 or 21060, do not continue with this bump-fault recovery procedure.

---

### Step 3 — E-stop RMS

**Responsible role:** L2_support

**Instruction:**
On the RMS “Bump” Fault Screen / RMS UI, E-stop RMS.

**Expected result:**
RMS is in an E-stopped state as indicated by the RMS E-stop control/button state on the UI.

**Stop or Escalate If:**

* If RMS does not reflect an E-stopped state, do not proceed to obstruction removal/RESET.

---

### Step 4 — Remove the obstruction that caused the bump/obstacle trigger

**Responsible role:** L2_support

**Instruction:**
Physically clear the obstruction on the grid that caused the bump/collision/obstacle trigger.

**Expected result:**
The physical obstruction is removed from the AGV path/area that triggered the bump/obstacle avoidance event.

**Stop or Escalate If:**

* If the obstruction cannot be removed, do not proceed to AGV RESET and resuming RMS.

---

### Step 5 — Hold AGV RESET for two seconds to clear the fault

**Responsible role:** L2_support

**Instruction:**
On the RMS “Bump” Fault Screen, click/press the AGV RESET button and hold it for two (2) seconds.

**Expected result:**
The AGV bump fault clears after the two-second hold, reflected by the RMS fault/exception display updating.

**Stop or Escalate If:**

* If the Exception Code 21057/21060 remains after the two-second AGV RESET, stop and escalate for further fault recovery steps; do not proceed to resume operation if the fault persists.

---

### Step 6 — Press E-stop again

**Responsible role:** L2_support

**Instruction:**
Press E-stop again on the RMS UI.

**Expected result:**
RMS reflects the E-stop state again after the second E-stop press.

---

### Step 7 — Resume RMS

**Responsible role:** L2_support

**Instruction:**
Resume RMS (return RMS to normal operation) using the RMS controls on the same RMS UI.

**Expected result:**
RMS resumes normal operation after the resume action is taken.

**Stop or Escalate If:**

* If the bump Exception Code remains displayed, stop and escalate; do not continue normal operation with the fault still active.

---

### Step 8 — Verify the bump fault is cleared on the RMS interface

**Responsible role:** L2_support

**Instruction:**
Verify on the RMS “Bump” Fault Screen that the AGV no longer shows the bump fault/exception code (21057/21060).

**Expected result:**
The RMS “Bump” Fault Screen no longer displays Exception Code 21057 or 21060 for the faulted AGV.

**Stop or Escalate If:**

* If the Exception Code remains, stop and escalate for further fault recovery steps.

---

## Success Criteria

* On the RMS “Bump” Fault Screen, the Exception Code 21057 or 21060 is cleared after holding AGV RESET for two seconds.
* After resuming RMS, the RMS interface no longer shows the bump fault/exception code for the faulted AGV.

## Failure Conditions

* Exception Code 21057 or 21060 remains displayed after the two-second AGV RESET attempt.
* RMS resumes but the bump fault/exception code remains active on the RMS “Bump” Fault Screen.

## Escalation Guidance

* If the Exception Code 21057/21060 remains after the two-second AGV RESET, stop and escalate for further fault recovery steps; do not proceed to resume operation if the fault persists.

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_bump_fault_recovery_rms
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
