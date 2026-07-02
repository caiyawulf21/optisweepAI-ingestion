# Add AGV to zone when no empty AGV is available

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_add_agv_to_zone_when_no_empty_agv_is_available_v1` |
| Title | Add AGV to zone when no empty AGV is available |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Restore operation by stopping RMS, moving an AGV into the zone under the tote rack, adding the AGV through RMS using Tote API Controls, verifying the AGV turns blue and shows status/state "szonestaging" on the HMI, then resuming RMS.

## When To Use

Use this recovery procedure when an AGV must be added to a zone and no empty AGV is available, and the source directs recovery by placing an AGV into the zone under the tote rack and confirming the AGV reaches the expected state before restart.

## Do Not Use For

* Do not use this runbook for other AGV fault scenarios such as bump faults, faulted AGV with tote, AGV stuck, or power outage recovery; those are covered by other source sections.
* Do not resume/restart the system until the AGV status is verified as "szonestaging" on the HMI when restart is needed.

## Safety And Operational Notes

* The source instructs the user to E-stop RMS before moving and adding the AGV.
* If the system needs to be restarted, make sure the AGVs are in the "szonestaging" state.
* No lockout/tagout instruction is provided in the supplied source packet.

## Access Or Tools Needed

* RMS access
* Tote API Controls
* HMI access to view AGV state/status
* Ability to E-stop and resume RMS

## Related Operational Context

* ctx_manual_agv_status_screen_v1
* ctx_manual_agv_szonestaging_status_v1
* ctx_manual_agv_green_lights_status_v1

## Procedure Steps

### Step 1 — E-stop RMS

**Responsible role:** L1_support

**Instruction:**
E-stop RMS.

**Expected result:**
RMS is stopped and the recovery can proceed.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*System shut-down mode context relevant to stopping the system before recovery.*


**Stop or Escalate If:**

* RMS does not enter the stopped/E-stopped condition.

---

### Step 2 — Move an AGV into the zone under the tote rack

**Responsible role:** L1_support

**Instruction:**
Move an AGV into the zone under the tote rack.

**Expected result:**
An AGV is physically positioned in the zone under the tote rack.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Screen/figure associated with the Add AGV to Zone with No Empty AGV context and the zone under the tote rack.*


**Stop or Escalate If:**

* The AGV cannot be moved into the zone under the tote rack.
* The correct zone cannot be identified from available source material.

---

### Step 3 — Add the AGV in RMS using Tote API Controls

**Responsible role:** L1_support

**Instruction:**
Add the AGV in RMS using Tote API Controls.

**Expected result:**
The AGV is added in RMS.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Recovery screen context for adding an AGV when no empty AGV is available.*


**Stop or Escalate If:**

* Tote API Controls are not accessible.
* The AGV add action fails or does not appear to take effect.

---

### Step 4 — Wait for the AGV to turn blue

**Responsible role:** L1_support

**Instruction:**
Wait for the AGV to turn blue.

**Expected result:**
The AGV turns blue on the relevant display.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*AGV display state showing the AGV turning blue after add.*


**Stop or Escalate If:**

* The AGV does not turn blue.
* The AGV instead appears to be routing to the Hospital.

---

### Step 5 — Verify AGV status is szonestaging on the HMI

**Responsible role:** L1_support

**Instruction:**
Verify on the HMI that the AGV status/state is "szonestaging".

**Expected result:**
The HMI shows the AGV status/state as "szonestaging".

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Screen associated with the fault recovery procedure for adding an AGV to a zone when there is no empty AGV available.*


**Stop or Escalate If:**

* The AGV status is not "szonestaging".
* The HMI cannot be accessed to verify AGV state.

---

### Step 6 — If AGV is moving to the Hospital, remove and add it again

**Responsible role:** L1_support

**Instruction:**
If the AGV is moving to the Hospital, remove the AGV and add it again.

**Expected result:**
The AGV is removed and re-added so recovery can be retried.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Recovery screen context noting the Hospital-routing retry condition.*


**Stop or Escalate If:**

* The AGV continues moving to the Hospital after being removed and added again.
* The source provides no further escalation path beyond retry.

---

### Step 7 — Press E-stop again

**Responsible role:** L1_support

**Instruction:**
Press E-stop again.

**Expected result:**
The documented E-stop action is completed as part of the recovery sequence.

**Stop or Escalate If:**

* The E-stop action cannot be performed as documented.

---

### Step 8 — Resume RMS

**Responsible role:** L1_support

**Instruction:**
Resume RMS.

**Expected result:**
RMS resumes operation.

**Stop or Escalate If:**

* The AGV has not been verified as "szonestaging" before restart/resume.
* RMS does not resume normally.

---

## Success Criteria

* The AGV is added to the zone under the tote rack.
* The AGV turns blue.
* The HMI shows the AGV status/state as "szonestaging".
* RMS can be resumed.

## Failure Conditions

* RMS cannot be E-stopped or resumed.
* The AGV cannot be moved into the zone under the tote rack.
* The AGV cannot be added in RMS using Tote API Controls.
* The AGV does not turn blue.
* The AGV status/state does not become "szonestaging".
* The AGV moves to the Hospital and does not recover after remove/add retry.

## Escalation Guidance

* If the AGV is moving to the Hospital, remove the AGV and add it again.
* No further escalation path is provided in the source.

## Missing Details / Known Gaps

* The supplied packet does not include the full OCR text of section 5.8.2.2.
* Detailed Tote API Controls substeps are referenced but not reproduced in the packet.
* The exact HMI navigation path for verifying "szonestaging" is only partially supported through related context, not the section text itself.
* No estimated completion time is provided in the source packet.
* No explicit production stop or LOTO requirement is stated in the supplied source packet.
* No further escalation path is provided beyond removing and re-adding the AGV if it moves to the Hospital.

## Source Lineage

- Candidate IDs: add_agv_to_zone_with_no_empty_agv_recovery
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
