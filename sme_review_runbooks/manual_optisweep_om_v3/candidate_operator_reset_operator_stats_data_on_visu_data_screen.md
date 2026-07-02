# Reset Operator Stats Data On The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_operator_stats_data_on_the_visu_data_screen_v1` |
| Title | Reset Operator Stats Data On The VISU_DATA Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Operator Stats DATA RESET button on the VISU_DATA screen to reset the displayed operator response-time data to zero.

## When To Use

Use this procedure when the operator needs to clear the Operator Stats values shown on the VISU_DATA screen so the displayed response-time data is reset to zero.

## Do Not Use For

* Do not use this procedure to reset data outside the Operator Stats section.

## Safety And Operational Notes

* This runbook is limited to an HMI data reset action documented for the Operator Stats section.
* Reset scope is limited to the Operator Stats section as documented.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_agv_status_metrics_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen and locate Operator Stats

**Responsible role:** operator

**Instruction:**
Open the VISU_DATA screen on the operator station HMI and locate the Operator Stats section.

**Expected result:**
The VISU_DATA screen is open and the Operator Stats section is visible.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Overall VISU_DATA screen layout on the operator station HMI.*

![artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats](assets/artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats.jpeg)

*Operator Stats section showing operator performance statistics for left and right tippers.*


**Stop or Escalate If:**

* Stop or escalate if the VISU_DATA screen cannot be accessed.
* Stop or escalate if the Operator Stats section is not visible on the VISU_DATA screen.

---

### Step 2 — Identify the DATA RESET button

**Responsible role:** operator

**Instruction:**
Identify the DATA RESET button within the Operator Stats section.

**Expected result:**
The DATA RESET button for Operator Stats is identified.

**Screens / Images:**

![artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats](assets/artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats.jpeg)

*Operator Stats section showing the DATA RESET button.*


**Stop or Escalate If:**

* Stop or escalate if the DATA RESET button is not present in the Operator Stats section.

---

### Step 3 — Review the displayed response-time values

**Responsible role:** operator

**Instruction:**
Review the displayed response-time values in the Operator Stats section that will be reset.

**Expected result:**
The operator has confirmed the currently displayed response-time values before reset.

**Screens / Images:**

![artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats](assets/artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats.jpeg)

*Resp Time Max, Resp Time Min, and Resp Time Avg values for left and right tippers.*


**Stop or Escalate If:**

* Stop or escalate if the Operator Stats values are not displayed.

---

### Step 4 — Press the DATA RESET button

**Responsible role:** operator

**Instruction:**
Press the DATA RESET button in the Operator Stats section to reset the data to zero.

**Expected result:**
The Operator Stats data is reset to zero.

**Screens / Images:**

![artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats](assets/artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats.jpeg)

*Operator Stats section and DATA RESET button used to clear the displayed values.*


**Stop or Escalate If:**

* Escalate if the DATA RESET button does not reset the displayed Operator Stats values to zero.

---

### Step 5 — Verify the values display zero

**Responsible role:** operator

**Instruction:**
Verify that the Operator Stats values display zero after the reset.

**Expected result:**
The Operator Stats values display zero.

**Screens / Images:**

![artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats](assets/artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats.jpeg)

*Operator Stats values after reset to confirm they display zero.*


**Stop or Escalate If:**

* Escalate if the DATA RESET button does not reset the displayed Operator Stats values to zero.
* Stop or escalate if the Operator Stats values do not display zero after reset.

---

## Success Criteria

* The Operator Stats data on the VISU_DATA screen is reset to zero.
* The displayed Operator Stats values show zero after the reset.

## Failure Conditions

* The VISU_DATA screen cannot be accessed.
* The Operator Stats section cannot be located.
* The DATA RESET button cannot be identified.
* The DATA RESET button does not reset the displayed Operator Stats values to zero.
* The Operator Stats values do not display zero after reset.

## Escalation Guidance

* Escalate if the DATA RESET button does not reset the displayed Operator Stats values to zero.

## Missing Details / Known Gaps

* The source packet does not provide explicit navigation steps for opening the VISU_DATA screen.
* The source packet does not provide an estimated completion time.
* The source packet does not state whether production stop or LOTO is required.
* The supplied related context record appears unrelated to this Operator Stats reset procedure.

## Source Lineage

- Candidate IDs: candidate_operator_reset_operator_stats_data_on_visu_data_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
