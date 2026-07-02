# Reset Tipper Stats Data On The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_tipper_stats_data_on_the_visu_data_screen_v1` |
| Title | Reset Tipper Stats Data On The VISU_DATA Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Tipper Stats DATA RESET button on the VISU_DATA screen to reset the displayed tipper data to zero.

## When To Use

Use this procedure when an operator needs to reset the Tipper Stats values shown in the Tipper Stats section of the VISU_DATA screen to zero.

## Do Not Use For

* Do not use this procedure to reset data outside the Tipper Stats section.
* Do not assume this procedure covers heartbeat statistics, operator statistics, or other HMI reset functions not explicitly documented in this candidate.

## Safety And Operational Notes

* This candidate is marked support safe.
* The documented reset scope is limited to the Tipper Stats section as described by the source.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_agv_status_metrics_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen and locate Tipper Stats

**Responsible role:** operator

**Instruction:**
Open the VISU_DATA screen on the operator station HMI and locate the Tipper Stats section.

**Expected result:**
The VISU_DATA screen is open and the Tipper Stats section is visible.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen layout, login controls, message banner, and tipper statistics area.*


**Stop or Escalate If:**

* Escalate if the VISU_DATA screen cannot be accessed.
* Escalate if the Tipper Stats section is not visible on the VISU_DATA screen.

---

### Step 2 — Identify the DATA RESET button

**Responsible role:** operator

**Instruction:**
Identify the DATA RESET button within the Tipper Stats section.

**Expected result:**
The operator has located the DATA RESET button associated with Tipper Stats.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Tipper Stats section and the DATA RESET button.*


**Stop or Escalate If:**

* Escalate if the DATA RESET button is not present where expected in the Tipper Stats section.

---

### Step 3 — Review the displayed Tipper Stats values

**Responsible role:** operator

**Instruction:**
Review the displayed Tipper Stats values that will be reset, including processed tote counts, hospital counts, fault counts, and other listed metrics.

**Expected result:**
The operator has reviewed the currently displayed Tipper Stats values before resetting them.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Tipper Stats values such as totes processed, counts sent to the Hospital Station, fault totals since the last reset, and average cycle time.*


**Stop or Escalate If:**

* Escalate if the Tipper Stats values are not displayed or cannot be read.

---

### Step 4 — Press the DATA RESET button

**Responsible role:** operator

**Instruction:**
Press the DATA RESET button in the Tipper Stats section to reset the data to zero.

**Expected result:**
The Tipper Stats reset action is initiated from the VISU_DATA screen.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Tipper Stats section and DATA RESET button used to reset the displayed data.*


**Stop or Escalate If:**

* Escalate if the DATA RESET button does not reset the displayed Tipper Stats values to zero.
* Stop and seek clarification if a confirmation prompt appears, because the source does not state whether any confirmation prompt appears.

---

### Step 5 — Verify the values reset to zero

**Responsible role:** operator

**Instruction:**
Verify that the resettable Tipper Stats values display zero after the reset.

**Expected result:**
The resettable Tipper Stats values display zero.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Tipper Stats values after pressing DATA RESET to confirm they display zero.*


**Stop or Escalate If:**

* Escalate if the displayed Tipper Stats values do not reset to zero.

---

## Success Criteria

* The Tipper Stats data on the VISU_DATA screen is reset to zero.
* The resettable Tipper Stats values display zero after the reset.

## Failure Conditions

* The VISU_DATA screen or Tipper Stats section cannot be accessed or viewed.
* The DATA RESET button cannot be identified in the Tipper Stats section.
* Pressing the DATA RESET button does not reset the displayed Tipper Stats values to zero.
* A confirmation prompt may appear, but the source does not document its behavior.

## Escalation Guidance

* Escalate if the DATA RESET button does not reset the displayed Tipper Stats values to zero.
* Escalate if the VISU_DATA screen, Tipper Stats section, or DATA RESET button cannot be accessed or identified.
* Seek SME clarification if a confirmation prompt appears, because the source does not state whether any confirmation prompt appears.

## Missing Details / Known Gaps

* The source packet does not provide the exact navigation path used to open the VISU_DATA screen.
* The source packet does not state whether operator login is required before using the DATA RESET button.
* The source packet does not state whether a confirmation prompt appears after pressing DATA RESET.
* The source packet does not provide an estimated completion time.
* The source packet does not specify whether production must be stopped before performing this reset.
* The source packet does not specify whether all displayed Tipper Stats fields are resettable or identify any exceptions.

## Source Lineage

- Candidate IDs: candidate_operator_reset_tipper_stats_data_on_visu_data_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
