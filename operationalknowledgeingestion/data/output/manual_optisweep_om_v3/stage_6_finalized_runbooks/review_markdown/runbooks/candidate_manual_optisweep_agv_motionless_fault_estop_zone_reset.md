# Clear AGV Motionless on Floor Fault Using RMS (If Needed), E-Stop Zone Map, and Blue RESET

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1` |
| Title | Clear AGV Motionless on Floor Fault Using RMS (If Needed), E-Stop Zone Map, and Blue RESET |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors`, `agv_physical_recovery` |
| Access Surface | `rms_ui`, `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

For an AGV motionless on the floor (fault), locate the faulted AGV (optionally using RMS to identify the AGV error), stop the appropriate E-stop zone using the E-stop zone map, remove the faulted AGV, pull the E-STOP, and press the blue RESET button to resume operation.

## When To Use

Use when an AGV is motionless on the floor and the issue is identified as a fault, requiring physical removal of the faulted AGV and an E-stop zone reset to resume system operation.

## Access Or Tools Needed

* RMS / fleet status UI (if needed to identify the faulted AGV error)
* Physical access to the appropriate E-stop(s)
* E-stop zone map
* Blue RESET button

## Related Operational Context

* ctx_manual_agv_motionless_fault_v1
* ctx_manual_esop_zone_reset_procedure_v1

## Visual References

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*RMS screen showing the AGV “Bump” fault with exception codes 21057 and 21060 (used as an example of how RMS may display the AGV fault/error).*

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/d87070d22301b81d.jpeg)

*HMI screenshot showing a faulted AGV with tote state (used to support identifying the faulted AGV context).*

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*AGV API Controls screen (Remove AGV / Recover AGV / Pause/Resume / Execute/Resend commands) referenced by the manual for AGV management.*

## Procedure Steps

### Step 1 — Locate the faulted AGV (use RMS if needed)

**Responsible role:** operator

**Instruction:**
If the faulted AGV is not immediately obvious, use the RMS / fleet status UI to identify the AGV error/faulted unit.

**Expected result:**
You have identified the faulted AGV that is motionless on the floor.

**Stop or Escalate If:**

* If RMS does not clearly identify the faulted AGV, escalate for assistance locating the faulted unit.

---

### Step 2 — Stop the appropriate E-stop zone using the E-stop zone map

**Responsible role:** operator

**Instruction:**
Reference the E-stop zone map and press the E-STOP for the appropriate E-stop zone.

**Expected result:**
The appropriate E-stop zone is stopped.

---

### Step 3 — Remove the faulted AGV

**Responsible role:** operator

**Instruction:**
Remove the faulted AGV from the floor/system area.

**Expected result:**
The faulted AGV has been removed.

---

### Step 4 — Pull the E-STOP

**Responsible role:** operator

**Instruction:**
Pull the E-STOP.

**Expected result:**
The E-STOP has been pulled (reset sequence is ready for blue RESET).

---

### Step 5 — Press the blue RESET button

**Responsible role:** operator

**Instruction:**
Press the blue RESET button.

**Expected result:**
The system resumes operation after the reset.

**Stop or Escalate If:**

* If the system does not resume operation after pressing the blue RESET button, escalate.

---

### Step 6 — Confirm the system resumes operation

**Responsible role:** operator

**Instruction:**
Confirm that the system resumes operation following the blue RESET.

**Expected result:**
Operation resumes.

**Stop or Escalate If:**

* If the system does not resume operation after pressing the blue RESET button, escalate.

---

## Success Criteria

* After pulling the E-STOP and pressing the blue RESET button, the system resumes operation.

## Failure Conditions

* System does not resume operation after pressing the blue RESET button.
* RMS does not clearly identify the faulted AGV.

## Escalation Guidance

* Escalate if the system does not resume operation after pressing the blue RESET button.
* If RMS does not clearly identify the faulted AGV, escalate for assistance locating the faulted unit.

## Missing Details / Known Gaps

* The packet does not specify the exact RMS navigation path/buttons to identify the faulted AGV error; it only states that RMS may be referenced for AGV error.
* The packet does not provide the exact physical location/labeling of the blue RESET button or the specific E-stop zone map legend details.

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_agv_motionless_fault_estop_zone_reset
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
