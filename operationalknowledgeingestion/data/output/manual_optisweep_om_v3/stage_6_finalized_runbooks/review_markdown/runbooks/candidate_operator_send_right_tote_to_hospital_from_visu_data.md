# Send The Right Tipper Tote To Hospital From The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_send_the_right_tipper_tote_to_hospital_from_the_visu_data_screen_v1` |
| Title | Send The Right Tipper Tote To Hospital From The VISU_DATA Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the SEND RIGHT TO HOSPITAL control on the Operator Station HMI VISU_DATA screen to send the tote currently at the right tipper to the hospital.

## When To Use

Use this procedure when the operator needs to send the tote currently at the right tipper to the hospital using the documented VISU_DATA screen control.

## Do Not Use For

* Do not use this procedure for the left tipper; the source distinguishes SEND LEFT TO HOSPITAL from SEND RIGHT TO HOSPITAL.
* Do not use this procedure when confirmation prompts, detailed follow-up indicators, or alternate recovery logic are required; those details are not provided in the source packet.

## Safety And Operational Notes

* Use only the documented SEND RIGHT TO HOSPITAL control on the VISU_DATA screen.
* The source packet does not provide confirmation prompt behavior or detailed post-action verification indicators.
* If the documented button action does not occur, stop and escalate.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen

**Responsible role:** operator

**Instruction:**
Open the VISU_DATA screen on the operator station HMI.

**Expected result:**
The VISU_DATA screen is displayed on the Operator Station HMI.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen layout with login controls, message banner, and tipper statistics.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Display controls showing navigation to Visu_Data.*


**Stop or Escalate If:**

* VISU_DATA cannot be opened from the operator station HMI.
* The screen shown does not match the documented VISU_DATA screen.

---

### Step 2 — Locate the SEND RIGHT TO HOSPITAL button

**Responsible role:** operator

**Instruction:**
Locate the SEND RIGHT TO HOSPITAL button on the VISU_DATA screen.

**Expected result:**
The SEND RIGHT TO HOSPITAL button is visible on the VISU_DATA screen.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen area containing hospital-routing controls.*


**Stop or Escalate If:**

* The SEND RIGHT TO HOSPITAL button is not present on the VISU_DATA screen.
* The operator cannot identify the correct right-side hospital-send control.

---

### Step 3 — Confirm the action applies to the right tipper tote

**Responsible role:** operator

**Instruction:**
Confirm that the action applies to the tote currently at the right tipper.

**Expected result:**
The operator has confirmed that the documented button applies to the tote currently at the right tipper.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen context for the right-side hospital-send control and tipper-related information.*


**Stop or Escalate If:**

* The tote is not currently at the right tipper.
* The operator cannot confirm that the right-side control applies to the intended tote.

---

### Step 4 — Press SEND RIGHT TO HOSPITAL

**Responsible role:** operator

**Instruction:**
Press the SEND RIGHT TO HOSPITAL button on the VISU_DATA screen.

**Expected result:**
The documented hospital-send action is initiated for the tote currently at the right tipper.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen containing the SEND RIGHT TO HOSPITAL control.*


**Stop or Escalate If:**

* The button does not initiate the documented hospital-send action.

---

### Step 5 — Verify the tote was sent to the hospital

**Responsible role:** operator

**Instruction:**
Verify on the HMI or through system observation that the right-tipper tote has been sent to the hospital, if that result is visible from available source-backed indicators.

**Expected result:**
The tote currently at the right tipper has been sent to the hospital.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen elements that may reflect the result, if visible.*


**Stop or Escalate If:**

* The result cannot be verified from available source-backed indicators.
* Observed behavior suggests the tote was not sent to the hospital.

---

## Success Criteria

* The SEND RIGHT TO HOSPITAL action is performed from the VISU_DATA screen.
* The action applies to the tote currently at the right tipper.
* Available source-backed HMI or observable system behavior indicates the tote has been sent to the hospital.

## Failure Conditions

* The VISU_DATA screen cannot be opened.
* The SEND RIGHT TO HOSPITAL button cannot be found on the VISU_DATA screen.
* The tote is not confirmed to be at the right tipper.
* The button does not initiate the documented hospital-send action.
* The source packet does not provide detailed confirmation prompts or explicit follow-up indicators.

## Escalation Guidance

* Escalate if the button does not initiate the documented hospital-send action.
* Escalate if the operator cannot verify the result using available source-backed indicators.
* Escalate if the correct VISU_DATA control cannot be located or the screen does not match the documented layout.

## Missing Details / Known Gaps

* The source does not provide confirmation prompt behavior for pressing SEND RIGHT TO HOSPITAL.
* The source does not provide explicit post-action indicators that confirm successful hospital routing.
* The source does not specify whether login is required before using the SEND RIGHT TO HOSPITAL button.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_operator_send_right_tote_to_hospital_from_visu_data
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
