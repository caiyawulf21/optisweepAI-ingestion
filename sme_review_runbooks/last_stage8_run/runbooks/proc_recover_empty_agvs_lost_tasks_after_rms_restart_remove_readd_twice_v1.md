# Recover Empty AGVs That Lost Tasks After RMS Restart (Remove/Re-add AGVs Twice)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1` |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `rms_ui`, `hospital_hmi` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

If empty AGVs lose their tasks after an RMS restart, stop RMS, remove and re-add the affected empty AGVs without totes twice, verify each AGV is in the "szonestaging" state on the HMI, press E-stop again when ready, then resume RMS.

## When To Use

Use when empty AGVs have lost their tasks because the RMS was restarted, and the recovery guidance calls for removing and re-adding the AGVs twice and confirming "szonestaging" before resuming RMS.

## Source Procedure References

- proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1

## Safety And Operational Notes

- Do not resume RMS until the affected AGVs are confirmed in the "szonestaging" state on the HMI.

## Procedure Steps

### Step 1 — E-stop RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), press the E-stop for RMS.

**Expected result:**
RMS is in an E-stopped state on the RMS / fleet status UI.

---

### Step 2 — Remove and re-add empty AGVs without totes twice using Tote API Controls

**Responsible role:** L2_support

**Instruction:**
Using the Tote API Controls flow within the RMS / fleet status UI (rms_ui), remove and re-add the affected empty AGVs without totes twice.

**Expected result:**
Each affected empty AGV has been removed and re-added twice via the RMS Tote API Controls flow.

---

### Step 3 — Verify AGVs are in "szonestaging" on the HMI

**Responsible role:** L2_support

**Instruction:**
If the system needs to be restarted, verify on the HMI (hospital_hmi) that the affected AGVs are in the "szonestaging" state by referencing the AGV state/value on the HMI.

**Expected result:**
The affected empty AGVs show AGV status/state value "szonestaging" on the HMI.

---

### Step 4 — Press E-stop again when ready to resume

**Responsible role:** L2_support

**Instruction:**
When the affected empty AGVs are confirmed in "szonestaging" on the HMI, press the E-stop again on the RMS / fleet status UI (rms_ui) when ready to resume.

**Expected result:**
The RMS E-stop control is pressed again (as indicated by the RMS / fleet status UI).

---

### Step 5 — Resume RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), resume RMS.

**Expected result:**
RMS resumes/starts successfully on the RMS / fleet status UI.

---

## Success Criteria

- RMS is resumed on the RMS / fleet status UI.
- Affected empty AGVs are no longer in the lost-task condition after the remove/re-add cycle and "szonestaging" verification.

## Failure Conditions

- Any affected empty AGV cannot be brought to "szonestaging".
- Lost-task condition persists after the twice remove/re-add process and RMS resumption.

## Escalation Guidance

- Escalate if AGVs cannot be brought to "szonestaging" or if the lost-task condition persists after the twice remove/re-add process.

## Missing Details / Known Gaps

- The packet does not provide a specific HMI artifact that explicitly shows the "szonestaging" value for AGVs; step 3 relies on the manual instruction to reference AGV state on the HMI.
