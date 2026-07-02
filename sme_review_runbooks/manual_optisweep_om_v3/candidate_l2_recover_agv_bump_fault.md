# Clear an AGV Bump Fault When Geek+ Cannot Recover the AGV

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_clear_an_agv_bump_fault_when_geek_cannot_recover_the_agv_v1` |
| Title | Clear an AGV Bump Fault When Geek+ Cannot Recover the AGV |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Manual recovery sequence for an AGV Bump fault when Geek+ cannot recover the AGV. The documented process is to E-stop the RMS, remove the obstruction, press and hold the AGV RESET button for two seconds to clear the fault, press E-stop again, and resume RMS.

## When To Use

Use this procedure for a documented AGV Bump fault recovery when Geek+ cannot recover the AGV.

## Do Not Use For

* Do not use for AGV faults other than the documented Bump fault unless the source explicitly directs this same recovery.
* Do not use when Geek+ can recover the AGV automatically.

## Safety And Operational Notes

* This procedure is not marked support-safe in the candidate.
* The source context states fault recovery may involve going inside the grid (the Dance Floor). Before going inside the grid, make sure to have Robot ID, fault description from RMS, bin/tote status, and whether an AGV under a rack is the empty AGV for that zone.
* The source instructs the operator to remove the obstruction before resetting the AGV fault.

## Access Or Tools Needed

* Access to RMS E-stop control
* Access to the obstruction area
* Access to the AGV RESET button
* Access to resume RMS

## Related Operational Context

* ctx_manual_agv_bump_fault_screen_v1
* ctx_manual_bump_exception_codes_v1
* ctx_manual_fault_recovery_prereq_info_v1

## Procedure Steps

### Step 1 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
E-stop the RMS.

**Expected result:**
RMS is stopped and the system is in a state that allows the documented manual recovery sequence to continue.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*Use the AGV Bump Fault Screen context to confirm the recovery is being performed for the documented bump fault.*


**Stop or Escalate If:**

* The RMS cannot be E-stopped.
* The fault condition does not match the documented AGV Bump fault recovery context.

---

### Step 2 — Remove the obstruction

**Responsible role:** L2_support

**Instruction:**
Remove the obstruction.

**Expected result:**
The obstruction causing the bump or obstacle-triggered AGV exception is removed.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*Review the AGV Bump Fault Screen associated with collision bar trigger or obstacle avoidance trigger conditions.*


**Stop or Escalate If:**

* The obstruction cannot be removed.
* The area cannot be safely accessed.
* The observed condition does not align with the documented bump fault context.

---

### Step 3 — Reset the AGV bump fault

**Responsible role:** L2_support

**Instruction:**
Click the AGV RESET button for two (2) seconds to clear the fault.

**Expected result:**
The AGV bump fault is cleared.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*AGV 'Bump' Fault Screen and the AGV RESET button used to clear the fault.*


**Stop or Escalate If:**

* The AGV RESET button is not available on the documented screen.
* The fault does not clear after the documented two-second reset action.

---

### Step 4 — Press E-stop again

**Responsible role:** L2_support

**Instruction:**
Press E-stop again.

**Expected result:**
The documented second E-stop action is completed.

**Stop or Escalate If:**

* The E-stop control cannot be actuated as required.

---

### Step 5 — Resume RMS

**Responsible role:** L2_support

**Instruction:**
Resume RMS. See "Starting the System" on page 65.

**Expected result:**
RMS is resumed and AGV operation is restored.

**Stop or Escalate If:**

* RMS cannot be resumed.
* AGV operation is not restored after resuming RMS.

---

## Success Criteria

* The obstruction is removed.
* The AGV fault is cleared using the AGV RESET button.
* RMS is resumed.
* AGV operation is restored.

## Failure Conditions

* Geek+ cannot recover the AGV and the documented manual sequence does not clear the fault.
* The obstruction cannot be removed.
* The AGV fault does not clear after pressing the AGV RESET button for two seconds.
* RMS cannot be resumed.

## Escalation Guidance

* Use this procedure when Geek+ cannot recover the AGV.
* If the fault does not clear after the documented reset sequence, the source does not provide additional escalation steps.

## Missing Details / Known Gaps

* The source does not specify the exact location of the AGV RESET button.
* The source does not provide additional escalation steps if the fault does not clear after the documented reset sequence.
* The source does not provide an estimated completion time.
* The source does not explicitly state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_l2_recover_agv_bump_fault
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
