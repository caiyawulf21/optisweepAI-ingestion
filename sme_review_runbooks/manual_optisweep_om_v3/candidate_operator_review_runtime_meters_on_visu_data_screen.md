# Review RunTime Meters On The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_review_runtime_meters_on_the_visu_data_screen_v1` |
| Title | Review RunTime Meters On The VISU_DATA Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the RunTime Meters section on the VISU_DATA screen to view accumulated operating time values and interpret them as the length of time the item has been in operation since system start. The source also states these values are only reset if the control software is overwritten.

## When To Use

Use when an operator needs to review RunTime Meters on the VISU_DATA screen to understand accumulated operating time since system start, or to record the displayed values for operational tracking.

## Do Not Use For

* Do not use this runbook to reset runtime values.
* Do not use this runbook as a control software overwrite procedure.

## Safety And Operational Notes

* This source section is informational and does not provide a reset action for RunTime Meters.
* Do not attempt to reset runtime values based on this source section.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_system_metrics_reference_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen and locate the RunTime Meters section

**Responsible role:** operator

**Instruction:**
At the operator station HMI, navigate to the VISU_DATA screen and locate the RunTime Meters section.

**Expected result:**
The VISU_DATA screen is open and the RunTime Meters section is visible to the operator.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Use the VISU_DATA screen image as the primary reference for the data-screen layout while locating the RunTime Meters section.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Use the display controls reference for navigation to the VISU_DATA screen, including the F5 mapping to Visu_Data.*


**Stop or Escalate If:**

* Escalate if the VISU_DATA screen cannot be accessed from the operator station HMI.
* Escalate if the runtime values cannot be located on the VISU_DATA screen using the available source references.

---

### Step 2 — Read the displayed RunTime Meters values

**Responsible role:** operator

**Instruction:**
Read the displayed RunTime Meters values for the item or items shown on the VISU_DATA screen.

**Expected result:**
The operator has identified the current runtime values displayed in the RunTime Meters section.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Review the VISU_DATA screen layout while reading the displayed data fields.*


**Stop or Escalate If:**

* Escalate if runtime values are not visible or cannot be read.

---

### Step 3 — Interpret the RunTime Meters values

**Responsible role:** operator

**Instruction:**
Interpret the displayed RunTime Meters values as the length of time the item has been in operation since the start of the system.

**Expected result:**
The operator understands that the displayed values represent accumulated operating time since system start.

**Stop or Escalate If:**

* Escalate if runtime values appear inconsistent with expected accumulated operation time.

---

### Step 4 — Record the displayed runtime values if needed

**Responsible role:** operator

**Instruction:**
Record the displayed runtime values if needed for operational tracking.

**Expected result:**
The runtime values are documented if the operator needs them for tracking.

**Stop or Escalate If:**

* Escalate if runtime values appear to have reset unexpectedly during normal operation.

---

### Step 5 — Note the reset behavior of RunTime Meters

**Responsible role:** operator

**Instruction:**
Note that the source states the RunTime Meters values are only reset if the control software is overwritten.

**Expected result:**
The operator understands the documented reset condition for the RunTime Meters values.

**Stop or Escalate If:**

* Escalate if runtime values appear to have reset unexpectedly during normal operation.
* Stop and escalate if a reset action is being requested based on this source section.

---

## Success Criteria

* The operator can access the VISU_DATA screen.
* The operator can locate and read the RunTime Meters values.
* The operator correctly interprets the values as accumulated operating time since system start.
* The operator understands that the source states the values are only reset if the control software is overwritten.

## Failure Conditions

* The VISU_DATA screen cannot be accessed.
* The RunTime Meters section cannot be located or read.
* Runtime values appear to have reset unexpectedly during normal operation.
* A user attempts to use this source section as a reset procedure.

## Escalation Guidance

* Escalate if runtime values appear to have reset unexpectedly during normal operation.
* Escalate if the VISU_DATA screen or RunTime Meters section cannot be accessed or identified.
* Do not attempt to reset runtime values based on this source section.

## Missing Details / Known Gaps

* The packet does not provide the exact visual location or labels of the RunTime Meters section within the VISU_DATA screen image.
* The source does not provide a procedure to reset RunTime Meters values.
* The source does not provide numeric thresholds, expected ranges, or troubleshooting criteria for runtime values.
* The source does not provide an estimated completion time for this reference procedure.

## Source Lineage

- Candidate IDs: candidate_operator_review_runtime_meters_on_visu_data_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
