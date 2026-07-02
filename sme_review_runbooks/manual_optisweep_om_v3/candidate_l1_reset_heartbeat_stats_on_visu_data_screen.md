# Reset Heartbeat Statistics On The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_heartbeat_statistics_on_the_visu_data_screen_v1` |
| Title | Reset Heartbeat Statistics On The VISU_DATA Screen |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Heartbeat RESET button on the VISU_DATA screen to reset heartbeat timing data to zero. The source describes the Heartbeat section as showing Last, Max, and Min values in milliseconds and states that the RESET button resets the data to zero.

## When To Use

Use this procedure when heartbeat timing statistics on the VISU_DATA screen need to be cleared to zero using the HMI RESET control.

## Do Not Use For

* Do not use if the displayed heartbeat values must be preserved as troubleshooting evidence before reset.

## Safety And Operational Notes

* Use caution if heartbeat values are needed as troubleshooting evidence before reset.
* The source notes that a heartbeat signal longer than 10 seconds can cause operation issues with the tipper due to mis-synchronization.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_hmi_agv_state_reference_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen and locate the Heartbeat section

**Responsible role:** L1_support

**Instruction:**
Open the operator station HMI VISU_DATA screen and locate the Heartbeat section that shows heartbeat signal statistics between the tipper and WCS.

**Expected result:**
The Heartbeat section is visible on the VISU_DATA screen.

**Screens / Images:**

![artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats](assets/artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats.jpeg)

*Heartbeat section showing heartbeat signal statistics between the tipper and WCS.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Overall VISU_DATA screen layout to help identify the correct screen.*


**Stop or Escalate If:**

* Stop or escalate if the VISU_DATA screen cannot be accessed.
* Stop or escalate if the Heartbeat section is not visible on the screen.

---

### Step 2 — Identify the RESET button in the Heartbeat section

**Responsible role:** L1_support

**Instruction:**
Within the Heartbeat section, identify the RESET button associated with the displayed heartbeat statistics.

**Expected result:**
The RESET button is identified in the Heartbeat section.

**Screens / Images:**

![artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats](assets/artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats.jpeg)

*Heartbeat section showing the RESET button.*


**Stop or Escalate If:**

* Stop or escalate if the RESET button is not present in the Heartbeat section.

---

### Step 3 — Review the displayed heartbeat values

**Responsible role:** L1_support

**Instruction:**
Review the displayed Last, Max, and Min heartbeat values in milliseconds before performing the reset.

**Expected result:**
The current Last, Max, and Min heartbeat values are reviewed before reset.

**Screens / Images:**

![artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats](assets/artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats.jpeg)

*Last, Max, and Min heartbeat values in milliseconds.*


**Stop or Escalate If:**

* Stop if the values need to be preserved as troubleshooting evidence before reset.
* Escalate if the heartbeat values cannot be read on the HMI.

---

### Step 4 — Press RESET to clear the heartbeat statistics

**Responsible role:** L1_support

**Instruction:**
Press the RESET button in the Heartbeat section to reset the displayed heartbeat data to zero.

**Expected result:**
The heartbeat statistics are reset by the HMI.

**Screens / Images:**

![artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats](assets/artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats.jpeg)

*Heartbeat section and RESET button used to clear the data.*


**Stop or Escalate If:**

* Escalate if the RESET button does not reset the displayed Heartbeat values to zero.

---

### Step 5 — Verify the heartbeat values display zero

**Responsible role:** L1_support

**Instruction:**
Verify that the Heartbeat values on the VISU_DATA screen display zero after the reset.

**Expected result:**
The Heartbeat values display zero.

**Screens / Images:**

![artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats](assets/artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats.jpeg)

*Heartbeat values after RESET to confirm they display zero.*


**Stop or Escalate If:**

* Escalate if the displayed Heartbeat values do not return to zero after RESET.

---

## Success Criteria

* The Heartbeat statistics on the VISU_DATA screen are reset to zero.
* Last, Max, and Min heartbeat values display zero after pressing RESET.

## Failure Conditions

* The VISU_DATA screen or Heartbeat section cannot be accessed.
* The RESET button is not visible in the Heartbeat section.
* The RESET button does not reset the displayed Heartbeat values to zero.
* Heartbeat values remain non-zero after reset.

## Escalation Guidance

* Escalate if the RESET button does not reset the displayed Heartbeat values to zero.
* Escalate if the Heartbeat section or RESET control is not available on the VISU_DATA screen.
* Preserve the displayed values before reset when they may be needed as troubleshooting evidence.

## Missing Details / Known Gaps

* The source packet does not provide a documented navigation path to open the VISU_DATA screen.
* The source packet does not specify whether production must be stopped before performing this reset.
* The source packet does not specify whether LOTO is required.
* The source packet does not provide an estimated completion time.
* The source packet does not define any additional role boundary beyond the candidate assignment to L1_support.

## Source Lineage

- Candidate IDs: candidate_l1_reset_heartbeat_stats_on_visu_data_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
