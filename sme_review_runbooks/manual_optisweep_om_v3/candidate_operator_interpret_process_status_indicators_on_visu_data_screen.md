# Interpret Process Status Indicators On The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_process_status_indicators_on_the_visu_data_screen_v1` |
| Title | Interpret Process Status Indicators On The VISU_DATA Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Process Status section on the VISU_DATA screen to determine the current documented operating and tote-handling state of the tipper based on the source-defined indicator meanings.

## When To Use

Use this reference when viewing the Operator Station HMI VISU_DATA screen and needing to interpret the documented meaning of the Process Status indicators: In Cycle, Tipper Ready, AGV Present, Tote RFID Pass, Tip in Process, Tipper Clear, and Tipper Faulted.

## Do Not Use For

* Do not use this runbook to infer meanings for colors or states not described in the source.
* Do not use this runbook as a fault recovery or control procedure.

## Safety And Operational Notes

* This is a reference procedure for HMI interpretation only.
* Do not infer meanings for colors or states not described in the source.
* Escalate if an observed indicator state does not match the documented labels or expected green-state meaning.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_operator_station_status_indication_v1
* ctx_manual_visu_data_screen_overview_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen and locate Process Status

**Responsible role:** operator

**Instruction:**
Open the VISU_DATA screen on the Operator Station HMI and locate the Process Status section.

**Expected result:**
The VISU_DATA screen is visible and the Process Status section can be identified.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen layout and the Process Status section.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Display controls and screen navigation reference for accessing VISU_DATA.*


**Stop or Escalate If:**

* The VISU_DATA screen cannot be accessed.
* The Process Status section is not visible or does not match the documented screen layout.

---

### Step 2 — Interpret In Cycle

**Responsible role:** operator

**Instruction:**
Observe whether the In Cycle indicator is green and interpret green as the tipper operating in Auto mode.

**Expected result:**
The operator understands whether the In Cycle indicator shows the documented green-state condition.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Process Status section and the In Cycle indicator.*


**Stop or Escalate If:**

* The In Cycle indicator label does not match the documented label.
* The observed state does not align with the documented green-state meaning.

---

### Step 3 — Interpret Tipper Ready

**Responsible role:** operator

**Instruction:**
Observe whether the Tipper Ready indicator is green and interpret green as the tipper being ready to receive a tote.

**Expected result:**
The operator understands whether the Tipper Ready indicator shows the documented green-state condition.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Process Status section and the Tipper Ready indicator.*


**Stop or Escalate If:**

* The Tipper Ready indicator label does not match the documented label.
* The observed state does not align with the documented green-state meaning.

---

### Step 4 — Interpret AGV Present

**Responsible role:** operator

**Instruction:**
Observe whether the AGV Present indicator is green and interpret green as a robot currently stationed at the tipper.

**Expected result:**
The operator understands whether the AGV Present indicator shows the documented green-state condition.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Process Status section and the AGV Present indicator.*


**Stop or Escalate If:**

* The AGV Present indicator label does not match the documented label.
* The observed state does not align with the documented green-state meaning.

---

### Step 5 — Interpret Tote RFID Pass

**Responsible role:** operator

**Instruction:**
Note the Tote RFID Pass indicator and record that the source states it is not used currently.

**Expected result:**
The operator understands that Tote RFID Pass is documented as not currently used.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Process Status section and the Tote RFID Pass indicator.*


**Stop or Escalate If:**

* A user attempts to interpret Tote RFID Pass beyond the source statement that it is not used currently.

---

### Step 6 — Interpret Tip in Process

**Responsible role:** operator

**Instruction:**
Observe whether the Tip in Process indicator is green and interpret green as the gripper having taken hold of a tote and remaining active until the tote is released.

**Expected result:**
The operator understands whether the Tip in Process indicator shows the documented green-state condition.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Process Status section and the Tip in Process indicator.*


**Stop or Escalate If:**

* The Tip in Process indicator label does not match the documented label.
* The observed state does not align with the documented green-state meaning.

---

### Step 7 — Interpret Tipper Clear

**Responsible role:** operator

**Instruction:**
Observe whether the Tipper Clear indicator is green and interpret green as the gripper being open.

**Expected result:**
The operator understands whether the Tipper Clear indicator shows the documented green-state condition.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Process Status section and the Tipper Clear indicator.*


**Stop or Escalate If:**

* The Tipper Clear indicator label does not match the documented label.
* The observed state does not align with the documented green-state meaning.

---

### Step 8 — Interpret Tipper Faulted

**Responsible role:** operator

**Instruction:**
Observe whether the Tipper Faulted indicator is green and interpret green as the tipper currently having a fault.

**Expected result:**
The operator understands whether the Tipper Faulted indicator shows the documented green-state condition.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Process Status section and the Tipper Faulted indicator.*


**Stop or Escalate If:**

* The Tipper Faulted indicator label does not match the documented label.
* The observed state does not align with the documented green-state meaning.

---

## Success Criteria

* The user can determine the documented meaning of each Process Status indicator shown on the VISU_DATA screen.
* Each listed Process Status indicator is interpreted only according to the source-supported meaning.

## Failure Conditions

* An observed indicator state does not match the documented labels or expected green-state meaning.
* The operator cannot locate the VISU_DATA screen or Process Status section.
* A user infers meanings for colors or states not described in the source.

## Escalation Guidance

* Escalate if an observed indicator state does not match the documented labels or expected green-state meaning.
* Escalate if the VISU_DATA screen layout or indicator labels differ from the documented source.
* Do not infer meanings for colors or states not described in the source.

## Missing Details / Known Gaps

* The packet does not provide the full verbatim Table 4-6 text for each individual indicator definition.
* The source packet supports green-state meanings but does not provide supported meanings for non-green states.
* No time estimate is provided in the source packet.
* No explicit production stop or LOTO requirement is stated in the source packet.

## Source Lineage

- Candidate IDs: candidate_operator_interpret_process_status_indicators_on_visu_data_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
