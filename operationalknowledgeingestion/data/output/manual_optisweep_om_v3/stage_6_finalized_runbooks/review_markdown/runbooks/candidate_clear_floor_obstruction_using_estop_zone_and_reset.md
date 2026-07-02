# Clear Floor Obstruction Or Dropped Parcel Using E-STOP Zone Isolation And Reset

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_clear_floor_obstruction_or_dropped_parcel_using_e_stop_zone_isolation_and_reset_v1` |
| Title | Clear Floor Obstruction Or Dropped Parcel Using E-STOP Zone Isolation And Reset |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented troubleshooting recovery sequence to isolate the affected E-stop zone, remove a dropped parcel or debris obstruction from the floor, reset the E-STOP condition, and restore system operation.

## When To Use

Use when there is an obstruction or parcel on the floor and the documented troubleshooting sequence calls for referencing the E-stop zone map, stopping the appropriate E-stop zone, removing the parcel or debris, pulling the E-STOP, and pressing the blue RESET button.

## Do Not Use For

* Do not use for recovery conditions beyond the documented obstruction/parcel on floor reset sequence.
* Do not proceed beyond the documented steps if the system does not resume operation after pressing the blue RESET button.

## Safety And Operational Notes

* Use the E-stop zone map to identify the appropriate zone before pressing E-STOP.
* Only the documented zone isolation and reset sequence is provided by the source.
* If the system does not resume operation after the blue RESET button is pressed, stop and escalate.

## Access Or Tools Needed

* Access to the E-stop zone map
* Access to the E-STOP control for the appropriate zone
* Access to the blue RESET button
* Physical access to remove the parcel or debris

## Related Operational Context

* ctx_manual_estop_reset_reference_v1

## Procedure Steps

### Step 1 — Identify the affected E-stop zone

**Responsible role:** operator

**Instruction:**
Reference the E-stop zone map to identify the appropriate E-stop zone for the obstruction.

**Expected result:**
The correct E-stop zone for the floor obstruction is identified.

**Stop or Escalate If:**

* The appropriate E-stop zone cannot be identified.

---

### Step 2 — Stop the appropriate E-stop zone

**Responsible role:** operator

**Instruction:**
Press E-STOP to stop the appropriate E-stop zone.

**Expected result:**
The appropriate E-stop zone is stopped.

**Stop or Escalate If:**

* The zone does not stop as expected.
* The wrong zone appears to have been selected.

---

### Step 3 — Remove the parcel or debris

**Responsible role:** operator

**Instruction:**
Remove the parcel or debris from the floor.

**Expected result:**
The obstruction is physically removed from the floor.

**Stop or Escalate If:**

* The obstruction cannot be safely removed.
* Debris or parcel material remains on the floor after removal attempt.

---

### Step 4 — Pull the E-STOP

**Responsible role:** operator

**Instruction:**
Pull E-STOP.

**Expected result:**
The E-STOP is pulled out and ready for reset completion.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Reference the ESTOP clearing context associated with pulling out the ESTOP before pressing RESET.*


**Stop or Escalate If:**

* The E-STOP cannot be reset to the pulled-out state.

---

### Step 5 — Press the blue RESET button

**Responsible role:** operator

**Instruction:**
Press the blue RESET button.

**Expected result:**
The reset is accepted and the system proceeds toward resumed operation.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Candidate-requested image support for the reset step; use as related fault recovery visual context from the packet.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*RESET-related HMI context associated with clearing faults after the ESTOP is pulled out.*


**Stop or Escalate If:**

* The system does not resume operation after pressing the blue RESET button.

---

### Step 6 — Verify system resumes operation

**Responsible role:** operator

**Instruction:**
Verify that the system resumes operation.

**Expected result:**
The system resumes operation.

**Stop or Escalate If:**

* The system does not resume operation after pressing the blue RESET button.

---

## Success Criteria

* The parcel or debris is removed from the floor.
* The E-stop zone is reset using the documented pull E-STOP and blue RESET sequence.
* The system resumes operation.

## Failure Conditions

* The appropriate E-stop zone cannot be identified.
* The zone does not stop as expected.
* The obstruction cannot be removed.
* The E-STOP cannot be pulled out or reset sequence cannot be completed.
* The system does not resume operation after pressing the blue RESET button.

## Escalation Guidance

* Stop and escalate if the system does not resume operation after pressing the blue RESET button.
* The source does not provide additional recovery steps beyond the reset sequence.

## Missing Details / Known Gaps

* The source does not specify exact physical location or format of the E-stop zone map.
* The source does not specify exact location of the blue RESET button.
* The source does not provide additional troubleshooting or alternate recovery steps if reset fails.
* The source does not provide a time estimate for completing this procedure.
* The packet does not include a dedicated artifact of the E-stop zone map.

## Source Lineage

- Candidate IDs: candidate_clear_floor_obstruction_using_estop_zone_and_reset
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
