# Recover An AGV From A BUMP Fault Code

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_an_agv_from_a_bump_fault_code_v1` |
| Title | Recover An AGV From A BUMP Fault Code |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Recover a documented AGV BUMP fault when Geek+ cannot recover the AGV by gathering required fault details, confirming the BUMP fault information on the AGV Bump Fault Screen, stopping RMS, removing the obstruction, resetting the AGV, and resuming RMS.

## When To Use

Use this procedure for the documented AGV BUMP fault recovery case in the OptiSweep manual when Geek+ cannot recover the AGV.

## Do Not Use For

* Do not use for AGV faults other than the documented BUMP fault case supported by this source.
* Do not use when the source-required BUMP fault information cannot be confirmed from RMS or the AGV Bump Fault Screen.

## Safety And Operational Notes

* The source states to gather information before going inside the grid (the Dance Floor).
* This procedure includes going inside the grid and physically removing an obstruction.
* Safety controls beyond the documented E-stop actions are not specified in the supplied source excerpt.

## Access Or Tools Needed

* Access to RMS
* Access to the AGV Bump Fault Screen
* Ability to use the E-stop
* Physical access to remove the obstruction
* Robot ID and RMS fault information

## Related Operational Context

* ctx_manual_fault_recovery_prereq_info_v1
* ctx_manual_bump_fault_overview_v1
* ctx_manual_bump_exception_codes_v1
* ctx_manual_agv_bump_fault_screen_v1

## Procedure Steps

### Step 1 — Gather required fault information before entering the grid

**Responsible role:** L2_support

**Instruction:**
Before going inside the grid (the Dance Floor), gather the Robot ID, the fault description from RMS, whether RMS indicates the faulted AGV is holding a bin and the tote ID if present, and if the faulted AGV is under a rack, determine whether that AGV is the empty AGV for that zone.

**Expected result:**
The responder has the AGV identity and required RMS fault context needed for the recovery.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*AGV identification and fault information relevant to the faulted robot.*


**Stop or Escalate If:**

* Robot ID cannot be determined.
* RMS fault description cannot be obtained.
* It cannot be determined whether the AGV is holding a bin or tote ID.
* It cannot be determined whether an under-rack AGV is the empty AGV for that zone.

---

### Step 2 — Confirm the documented BUMP fault case

**Responsible role:** L2_support

**Instruction:**
Identify that the AGV is in the documented BUMP fault case and check the exception information shown for code 21057 or 21060 if displayed on the AGV Bump Fault Screen.

**Expected result:**
The responder confirms the AGV fault matches the documented BUMP fault context and reviews the displayed exception information.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*Fault or exception display area, exception code area, and AGV identification on the AGV Bump Fault Screen.*


**Stop or Escalate If:**

* The AGV is not in the documented BUMP fault case.
* The exception information shown does not match the documented BUMP exceptions.
* The AGV Bump Fault Screen cannot be accessed or interpreted.

---

### Step 3 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
E-stop the RMS.

**Expected result:**
RMS is E-stopped.

**Stop or Escalate If:**

* RMS does not stop after E-stop is pressed.

---

### Step 4 — Remove the obstruction

**Responsible role:** L2_support

**Instruction:**
Remove the obstruction.

**Expected result:**
The obstruction is removed from the AGV path or contact point.

**Stop or Escalate If:**

* The obstruction cannot be safely removed.
* The obstruction is removed but the AGV remains in the faulted condition.

---

### Step 5 — Reset the AGV to clear the fault

**Responsible role:** L2_support

**Instruction:**
Click the AGV RESET button for two seconds to clear the fault.

**Expected result:**
The AGV fault is cleared.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*AGV RESET button location on the AGV Bump Fault Screen.*


**Stop or Escalate If:**

* The AGV RESET button cannot be located on the AGV Bump Fault Screen.
* The fault does not clear after the documented two-second reset action.

---

### Step 6 — Press E-stop again

**Responsible role:** L2_support

**Instruction:**
Press E-stop again.

**Expected result:**
The documented second E-stop action is completed.

**Stop or Escalate If:**

* The second E-stop action cannot be completed.
* System state does not allow continuation to resume RMS.

---

### Step 7 — Resume RMS

**Responsible role:** L2_support

**Instruction:**
Resume RMS.

**Expected result:**
RMS is resumed and the documented recovery sequence is complete.

**Stop or Escalate If:**

* RMS does not resume.
* The AGV fault is still present after resume.
* The AGV cannot be recovered by the documented sequence.

---

## Success Criteria

* The obstruction is removed.
* The AGV fault is cleared using the AGV RESET button.
* RMS is resumed.
* The documented BUMP recovery sequence completes without the fault persisting.

## Failure Conditions

* Required pre-entry fault information cannot be gathered.
* The fault does not match the documented BUMP fault case.
* RMS cannot be E-stopped or resumed as documented.
* The obstruction cannot be removed.
* The AGV fault does not clear after the documented reset sequence.

## Escalation Guidance

* Escalate if the fault does not clear after the documented reset sequence.
* Escalate if the AGV cannot be recovered by this documented BUMP fault procedure.
* Escalate if required fault identification information cannot be confirmed before entering the grid.

## Missing Details / Known Gaps

* The supplied source excerpt does not specify detailed safety controls for entering the grid beyond the documented E-stop actions and pre-entry information gathering.
* The supplied source excerpt does not define exact resume-RMS substeps; it only states to resume RMS.
* The supplied source excerpt does not provide an estimated completion time.
* The supplied source excerpt does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_l2_recover_agv_bump_fault_code
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
