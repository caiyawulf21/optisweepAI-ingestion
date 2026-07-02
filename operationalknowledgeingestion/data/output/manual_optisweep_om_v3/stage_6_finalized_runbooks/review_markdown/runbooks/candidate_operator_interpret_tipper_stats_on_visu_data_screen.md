# Interpret Tipper Stats On The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_tipper_stats_on_the_visu_data_screen_v1` |
| Title | Interpret Tipper Stats On The VISU_DATA Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Tipper Stats section on the VISU_DATA screen to identify left and right tipper counts, fault totals, average cycle time, average totes per hour, and time starved values.

## When To Use

Use this reference when an operator needs to read and interpret the Tipper Stats section on the VISU_DATA screen for left and right tipper processed tote counts, hospital-station counts, fault totals since last reset, average cycle time, average totes per hour, and time starved values.

## Do Not Use For

* Do not use this runbook to infer undocumented thresholds, acceptable ranges, or corrective actions from the displayed values.

## Safety And Operational Notes

* This is a reference procedure for reading HMI values only.
* Do not infer undocumented thresholds or corrective actions from the displayed values.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1
* ctx_manual_agv_status_metrics_v1

## Procedure Steps

### Step 1 — Open VISU_DATA and locate Tipper Stats

**Responsible role:** operator

**Instruction:**
Open the VISU_DATA screen on the operator station HMI and locate the Tipper Stats section.

**Expected result:**
The VISU_DATA screen is open and the Tipper Stats section is visible.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The VISU_DATA screen layout and the Tipper Stats section with labeled fields.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*The screen-navigation controls showing access to Visu_Data.*


**Stop or Escalate If:**

* Expected Tipper Stats fields are missing.
* Tipper Stats labels or values are unreadable on the VISU_DATA screen.

---

### Step 2 — Read Totes Processed for the left tipper

**Responsible role:** operator

**Instruction:**
Read the Totes Processed (Left) fields and identify how many totes have been processed and how many have been sent to the Hospital Station for the left tipper.

**Expected result:**
The left tipper processed tote count and left Hospital Station count are identified from the display.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The left-side Tipper Stats fields for Totes Processed and the count sent to the Hospital Station.*


**Stop or Escalate If:**

* The left Totes Processed fields are missing or unreadable.

---

### Step 3 — Read Totes Processed for the right tipper

**Responsible role:** operator

**Instruction:**
Read the Totes Processed (Right) fields and identify how many totes have been processed and how many have been sent to the Hospital Station for the right tipper.

**Expected result:**
The right tipper processed tote count and right Hospital Station count are identified from the display.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The right-side Tipper Stats fields for Totes Processed and the count sent to the Hospital Station.*


**Stop or Escalate If:**

* The right Totes Processed fields are missing or unreadable.

---

### Step 4 — Read left and right fault totals

**Responsible role:** operator

**Instruction:**
Read the Faults (Left/Right) fields and identify how many faults have occurred on each tipper since the last reset.

**Expected result:**
Left and right fault totals since the last reset are identified from the display.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The Faults fields for the left and right tippers in the Tipper Stats section.*


**Stop or Escalate If:**

* The left or right fault totals are missing or unreadable.

---

### Step 5 — Interpret average cycle time

**Responsible role:** operator

**Instruction:**
Read the Avg Cycle Time value and interpret it as the average time from when the gripper takes hold of the tote until it releases it back to the AGV.

**Expected result:**
The Avg Cycle Time value is identified and interpreted using the documented definition.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The Avg Cycle Time field in the Tipper Stats section.*


**Stop or Escalate If:**

* The Avg Cycle Time field is missing or unreadable.

---

### Step 6 — Interpret average totes per hour

**Responsible role:** operator

**Instruction:**
Read the Avg Totes/Hour value and interpret it as the average number of totes processed at 15-minute intervals.

**Expected result:**
The Avg Totes/Hour value is identified and interpreted using the documented definition.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The Avg Totes/Hour field in the Tipper Stats section.*


**Stop or Escalate If:**

* The Avg Totes/Hour field is missing or unreadable.

---

### Step 7 — Interpret time starved

**Responsible role:** operator

**Instruction:**
Read the Time Starved value and interpret it as the length of time the tipper has been waiting for a tote, noting that it resets after each tote.

**Expected result:**
The Time Starved value is identified and interpreted using the documented definition.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The Time Starved field in the Tipper Stats section.*


**Stop or Escalate If:**

* The Time Starved field is missing or unreadable.

---

## Success Criteria

* The user can correctly identify and interpret the documented Tipper Stats values for both tippers.
* The user reads only source-defined meanings for Totes Processed, Hospital Station counts, Faults since last reset, Avg Cycle Time, Avg Totes/Hour, and Time Starved.

## Failure Conditions

* Expected Tipper Stats fields are missing or unreadable on the VISU_DATA screen.
* The operator cannot distinguish left and right tipper values.
* The operator attempts to apply undocumented thresholds, acceptable ranges, or corrective actions.

## Escalation Guidance

* Escalate if expected Tipper Stats fields are missing or unreadable on the VISU_DATA screen.
* Escalate for SME review if interpretation beyond the documented field meanings is required.

## Missing Details / Known Gaps

* The source packet does not provide acceptable ranges or thresholds for any Tipper Stats values.
* The source packet does not provide corrective actions based on Tipper Stats values.
* The source packet does not provide an estimated completion time.
* The source packet does not state whether production stop or LOTO is required, though this runbook is reference-only.
* The source packet references a DATA RESET button but does not define its use as part of this candidate procedure.

## Source Lineage

- Candidate IDs: candidate_operator_interpret_tipper_stats_on_visu_data_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
