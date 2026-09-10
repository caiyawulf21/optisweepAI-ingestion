# Recover an AGV from a "Bump" fault (Exception Codes 21057/21060) using RMS E-stop and AGV RESET

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_agv_bump_fault_rms_estop_agv_reset_v1` |
| Title | Recover an AGV from a "Bump" fault (Exception Codes 21057/21060) using RMS E-stop and AGV RESET |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `bump_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When an AGV cannot be recovered by Geek+ and the RMS shows an AGV "Bump" fault (Exception Codes 21057 or 21060), stop RMS, remove the obstruction, hold the AGV RESET button for two seconds to clear the fault, press E-stop again, and resume RMS.

## When To Use

Use this procedure when the RMS / fleet status UI shows an AGV "Bump" fault and the exception code is 21057 or 21060, and the AGV needs on-site recovery by removing the obstruction and resetting the AGV.

## Safety And Operational Notes

* Stop RMS (E-stop) before removing the obstruction and performing the AGV RESET sequence.
* Do not proceed with reset/resume if you cannot safely remove the obstruction.

## Access Or Tools Needed

* RMS / fleet status UI (rms_ui)

## Related Operational Context

* ctx_manual_dance_floor_entry_info_v1
* ctx_manual_bump_fault_codes_v1
* ctx_manual_agv_reset_button_v1
* ctx_manual_rms_e_stop_v1

## Visual References

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*RMS screen figure showing the AGV "Bump" fault and Exception Code values (21057, 21060).*

## Procedure Steps

### Step 1 — Identify the AGV "Bump" fault and confirm the Exception Code (21057 or 21060)

**Responsible role:** L2_support

**Instruction:**
In the RMS / fleet status UI, locate the AGV "Bump" fault screen and confirm the Exception Code shown is 21057 or 21060.

**Expected result:**
The RMS "Bump" fault screen for the affected AGV shows Exception Code 21057 (Robot front collision bar triggers) or 21060 (robot triggers the obstacle avoidance).

**Stop or Escalate If:**

* If the exception code is not 21057 or 21060, stop and use the appropriate recovery procedure for that fault.

---

### Step 2 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI, activate the E-stop function.

**Expected result:**
RMS is in an E-stopped state (E-stop activated) while the "Bump" fault recovery sequence proceeds.

**Stop or Escalate If:**

* If you cannot reliably activate RMS E-stop, stop and escalate for further recovery steps.

---

### Step 3 — Remove the obstruction that caused the bump

**Responsible role:** L2_support

**Instruction:**
Remove the physical obstruction causing the bump (for example, at the AGV/robot front collision bar area).

**Expected result:**
The physical obstruction is removed so the AGV/robot front collision bar area is clear.

**Stop or Escalate If:**

* If you cannot safely remove the obstruction, do not proceed with reset/resume; escalate.

---

### Step 4 — Click and hold AGV RESET for two seconds to clear the fault

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI, click the AGV RESET button and hold it for two (2) seconds.

**Expected result:**
The AGV RESET action is held for two seconds to clear the fault.

**Stop or Escalate If:**

* If the "Bump" fault does not clear after the two-second AGV RESET, stop and escalate for further recovery steps.

---

### Step 5 — Press E-stop again

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI, press E-stop again.

**Expected result:**
RMS E-stop is pressed again as part of the recovery sequence.

---

### Step 6 — Resume RMS

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI, resume RMS to normal operation.

**Expected result:**
RMS is resumed to normal operation and the affected AGV is no longer showing the active "Bump" fault.

**Stop or Escalate If:**

* If the "Bump" fault does not clear after the two-second AGV RESET, stop and escalate for further recovery steps.

---

## Success Criteria

* Exception Code 21057/21060 "Bump" fault is cleared for the affected AGV after holding AGV RESET for two seconds.
* RMS is resumed to normal operation and the RMS no longer shows the active "Bump" fault for the affected AGV.

## Failure Conditions

* The "Bump" fault does not clear after holding AGV RESET for two seconds.
* The obstruction cannot be safely removed.

## Escalation Guidance

* If the "Bump" fault does not clear after the two-second AGV RESET, stop and escalate for further recovery steps (the source only specifies this sequence for clearing the fault).
* If you cannot safely remove the obstruction, do not proceed with reset/resume; escalate.

## Missing Details / Known Gaps

* The packet does not provide a specific RMS UI label/state for the E-stop control or the exact visual indicator that confirms RMS has resumed to normal operation; steps rely on the manual’s named sequence only.

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_bump_fault_recovery_rms_estop_reset
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
