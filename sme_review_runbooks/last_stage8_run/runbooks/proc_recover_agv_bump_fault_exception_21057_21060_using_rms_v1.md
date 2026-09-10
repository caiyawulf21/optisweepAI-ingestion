# Recover an AGV “BUMP” fault (Exception Codes 21057/21060) using RMS

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_agv_bump_fault_exception_21057_21060_using_rms_v1` |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Capability Tags | None |
| Access Surface | `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

When RMS shows an AGV “Bump” fault with Exception Code 21057 or 21060, stop RMS, remove the obstruction that caused the bump/obstacle trigger, hold the AGV RESET button for two seconds to clear the fault, press E-stop again, then resume RMS. Verify the Exception Code is cleared on the RMS “Bump” Fault Screen before resuming normal operation.

## When To Use

Use this procedure when the RMS interface displays an AGV “Bump” fault and the Exception Code shown is 21057 or 21060, indicating a collision bar trigger or obstacle-avoidance trigger that requires RMS-side fault recovery.

## Source Procedure References

- proc_recover_agv_bump_fault_exception_21057_21060_using_rms_v1

## Safety And Operational Notes

- This procedure includes E-stopping RMS (not physical E-stop).

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

---

### Step 3 — E-stop RMS

**Responsible role:** L2_support

**Instruction:**
On the RMS “Bump” Fault Screen / RMS UI, E-stop RMS.

**Expected result:**
RMS is in an E-stopped state as indicated by the RMS E-stop control/button state on the UI.

---

### Step 4 — Remove the obstruction that caused the bump/obstacle trigger

**Responsible role:** L2_support

**Instruction:**
Physically clear the obstruction on the grid that caused the bump/collision/obstacle trigger.

**Expected result:**
The physical obstruction is removed from the AGV path/area that triggered the bump/obstacle avoidance event.

---

### Step 5 — Hold AGV RESET for two seconds to clear the fault

**Responsible role:** L2_support

**Instruction:**
On the RMS “Bump” Fault Screen, click/press the AGV RESET button and hold it for two (2) seconds.

**Expected result:**
The AGV bump fault clears after the two-second hold, reflected by the RMS fault/exception display updating.

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

---

### Step 8 — Verify the bump fault is cleared on the RMS interface

**Responsible role:** L2_support

**Instruction:**
Verify on the RMS “Bump” Fault Screen that the AGV no longer shows the bump fault/exception code (21057/21060).

**Expected result:**
The RMS “Bump” Fault Screen no longer displays Exception Code 21057 or 21060 for the faulted AGV.

---

## Success Criteria

- On the RMS “Bump” Fault Screen, the Exception Code 21057 or 21060 is cleared after holding AGV RESET for two seconds.
- After resuming RMS, the RMS interface no longer shows the bump fault/exception code for the faulted AGV.

## Failure Conditions

- Exception Code 21057 or 21060 remains displayed after the two-second AGV RESET attempt.
- RMS resumes but the bump fault/exception code remains active on the RMS “Bump” Fault Screen.

## Escalation Guidance

- If the Exception Code 21057/21060 remains after the two-second AGV RESET, stop and escalate for further fault recovery steps; do not proceed to resume operation if the fault persists.
