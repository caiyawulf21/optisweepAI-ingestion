# Remove A Faulted Motionless AGV From The Floor And Restore Operation

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_a_faulted_motionless_agv_from_the_floor_and_restore_operation_v1` |
| Title | Remove A Faulted Motionless AGV From The Floor And Restore Operation |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Recover from an AGV motionless-on-floor fault by locating the faulted AGV, identifying and stopping the correct E-stop zone, removing the AGV from the floor, then restoring operation with the documented E-stop release and blue RESET sequence.

## When To Use

Use when an AGV is faulted and motionless on the floor and the documented troubleshooting sequence calls for locating the AGV, stopping the appropriate E-stop zone, removing the AGV, and resetting the system.

## Do Not Use For

* Do not use when the faulted AGV cannot be identified from floor observation and RMS reference.
* Do not use as a detailed physical AGV removal method; the source does not describe how to physically remove the AGV.
* Do not continue this procedure if the AGV cannot be safely removed or if the system does not resume operation after the documented reset sequence.

## Safety And Operational Notes

* This procedure is not marked support-safe because the source does not describe the safe handling method for physically removing the AGV.
* Use site safety controls and local procedures for physical AGV removal; this source does not provide those details.
* Stop and escalate if the AGV cannot be safely removed.

## Access Or Tools Needed

* Access to RMS for AGV error reference
* Access to the E-stop zone map
* Access to the E-STOP control for the appropriate zone
* Access to the blue RESET button
* Physical access to the faulted AGV

## Related Operational Context

* ctx_manual_estop_reset_reference_v1
* ctx_manual_component_rms_agv_error_reference_v1

## Procedure Steps

### Step 1 — Locate the faulted AGV

**Responsible role:** L2_support

**Instruction:**
Locate the faulted AGV on the floor. If needed, reference RMS for AGV error information to help identify the AGV.

**Expected result:**
The faulted motionless AGV is identified.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Use as a visual example of a faulted AGV screen context during recovery.*


**Stop or Escalate If:**

* The faulted AGV cannot be identified from floor observation and RMS reference.

---

### Step 2 — Identify the appropriate E-stop zone

**Responsible role:** L2_support

**Instruction:**
Reference the E-stop zone map to identify the appropriate E-stop zone for the faulted AGV.

**Expected result:**
The correct E-stop zone is identified.

**Stop or Escalate If:**

* The correct E-stop zone cannot be determined.

---

### Step 3 — Stop the appropriate E-stop zone

**Responsible role:** L2_support

**Instruction:**
Press E-STOP to stop the appropriate E-stop zone.

**Expected result:**
The appropriate E-stop zone is stopped.

**Stop or Escalate If:**

* The zone does not stop as expected.
* There is uncertainty that the correct zone was stopped.

---

### Step 4 — Remove the faulted AGV from the floor

**Responsible role:** L2_support

**Instruction:**
Remove the faulted AGV from the floor.

**Expected result:**
The faulted AGV is removed from the floor.

**Stop or Escalate If:**

* The AGV cannot be safely removed.
* The source does not provide the physical removal method and site-approved handling guidance is unavailable.

---

### Step 5 — Release the E-stop

**Responsible role:** L2_support

**Instruction:**
Pull E-STOP.

**Expected result:**
The E-stop is released.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Reference ESTOP clearing and RESET context associated with pulling out ESTOP and clearing faults.*


**Stop or Escalate If:**

* The E-stop cannot be released.
* The E-stop remains faulted after release.

---

### Step 6 — Press the blue RESET button

**Responsible role:** L2_support

**Instruction:**
Press the blue RESET button.

**Expected result:**
The reset is accepted and the system clears the fault condition.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Candidate-provided image support for a faulted AGV screen during the fault recovery procedure.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Reference RESET-related HMI context associated with clearing faults after ESTOP is pulled out.*


**Stop or Escalate If:**

* The reset does not clear the fault.
* The system remains stopped after reset.

---

### Step 7 — Verify the system resumes operation

**Responsible role:** L2_support

**Instruction:**
Verify that the system resumes operation.

**Expected result:**
The system resumes operation.

**Stop or Escalate If:**

* The system does not resume operation after the documented reset sequence.

---

## Success Criteria

* The faulted AGV is identified.
* The appropriate E-stop zone is stopped.
* The faulted AGV is removed from the floor.
* The E-stop is released and the blue RESET button is pressed.
* The system resumes operation.

## Failure Conditions

* The faulted AGV cannot be identified from floor observation and RMS reference.
* The correct E-stop zone cannot be determined.
* The AGV cannot be safely removed.
* The reset sequence does not clear the fault.
* The system does not resume operation after the documented reset sequence.

## Escalation Guidance

* Escalate if the faulted AGV cannot be identified from floor observation and RMS reference.
* Escalate if the AGV cannot be safely removed.
* Escalate if the system does not resume operation after the documented reset sequence.
* Escalate for site safety review because the source does not describe how to physically remove the AGV.

## Missing Details / Known Gaps

* The source does not describe the physical method, tools, or safety controls for removing the faulted AGV from the floor.
* The source does not provide a time estimate.
* The source does not specify whether production stop is required beyond stopping the appropriate E-stop zone.
* The source does not specify whether LOTO is required.
* The source does not identify the exact location or interface of the blue RESET button for this procedure.

## Source Lineage

- Candidate IDs: candidate_remove_faulted_motionless_agv_using_estop_zone_and_reset
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
