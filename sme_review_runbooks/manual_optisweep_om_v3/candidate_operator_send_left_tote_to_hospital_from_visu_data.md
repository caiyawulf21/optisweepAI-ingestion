# Send The Left Tipper Tote To Hospital From The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_send_the_left_tipper_tote_to_hospital_from_the_visu_data_screen_v1` |
| Title | Send The Left Tipper Tote To Hospital From The VISU_DATA Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the SEND LEFT TO HOSPITAL control on the Operator Station HMI VISU_DATA screen to send the tote currently at the left tipper to the hospital.

## When To Use

Use when an operator needs to route the tote currently at the left tipper to the hospital using the documented VISU_DATA screen control.

## Do Not Use For

* Do not use for sending a tote from the right tipper to the hospital.
* Do not use when the tote is not currently at the left tipper.
* Do not use as a recovery procedure for AGV stuck or communication fault conditions; those are described in other source sections, not this procedure.

## Safety And Operational Notes

* This runbook is limited to the documented HMI action on the VISU_DATA screen.
* The source does not describe confirmation prompts, interlocks, or post-action confirmation indicators for this control.
* Do not assume additional system behavior beyond the source-stated function of the button.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen

**Responsible role:** operator

**Instruction:**
At the operator station HMI, open the VISU_DATA screen. The source indicates this screen can be reached through the operator station display controls and screen navigation.

**Expected result:**
The VISU_DATA screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Overall VISU_DATA screen layout including login controls, message banner, and tipper statistics.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Display controls and screen-navigation mapping showing access to Visu_Data.*


**Stop or Escalate If:**

* The operator station HMI is unavailable.
* The VISU_DATA screen cannot be accessed from the operator station controls.

---

### Step 2 — Locate the SEND LEFT TO HOSPITAL button

**Responsible role:** operator

**Instruction:**
On the VISU_DATA screen, locate the SEND LEFT TO HOSPITAL button.

**Expected result:**
The SEND LEFT TO HOSPITAL button is visible on the VISU_DATA screen.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen area containing hospital-routing controls, including SEND LEFT TO HOSPITAL.*


**Stop or Escalate If:**

* The SEND LEFT TO HOSPITAL button is not present on the VISU_DATA screen.
* The displayed screen does not match the documented VISU_DATA screen overview.

---

### Step 3 — Confirm the action applies to the left tipper tote

**Responsible role:** operator

**Instruction:**
Confirm that the tote to be sent is the tote currently at the left tipper, because the documented function of this button applies to that tote.

**Expected result:**
The operator has confirmed the action is intended for the tote currently at the left tipper.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen context while confirming the action is being applied from the left-tipper side.*


**Stop or Escalate If:**

* It is unclear whether the tote is currently at the left tipper.
* The operator intends to route a tote from the right tipper instead.

---

### Step 4 — Press SEND LEFT TO HOSPITAL

**Responsible role:** operator

**Instruction:**
Press the SEND LEFT TO HOSPITAL button on the VISU_DATA screen.

**Expected result:**
The documented hospital-send action is initiated for the tote currently at the left tipper.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The SEND LEFT TO HOSPITAL control on the VISU_DATA screen before and during button press.*


**Stop or Escalate If:**

* The button does not respond.
* The button does not initiate the documented hospital-send action.

---

### Step 5 — Verify the tote was sent if an indicator is available

**Responsible role:** operator

**Instruction:**
Verify on the HMI or through system observation that the tote at the left tipper has been sent to the hospital, but only if that result is visible from available source-backed indicators.

**Expected result:**
The operator observes source-supported indication or system behavior consistent with the tote being sent to the hospital, if such indication is available.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen elements such as tipper-related information or message banner that may provide visible indication, if present.*


**Stop or Escalate If:**

* The source provides no confirmation prompt or follow-up indicator and the operator cannot verify the result.
* Observed behavior suggests the tote was not sent to the hospital.
* The button press did not appear to initiate the documented action.

---

## Success Criteria

* The SEND LEFT TO HOSPITAL button is accessed from the VISU_DATA screen.
* The action is applied to the tote currently at the left tipper.
* The documented hospital-send action is initiated for that tote.
* If visible source-backed indicators are available, they are consistent with the tote being sent to the hospital.

## Failure Conditions

* VISU_DATA screen cannot be accessed.
* SEND LEFT TO HOSPITAL button is not visible or cannot be identified.
* The tote is not currently at the left tipper.
* Pressing the button does not initiate the documented hospital-send action.
* The source does not provide enough confirmation detail to verify completion from the HMI.

## Escalation Guidance

* Escalate if the SEND LEFT TO HOSPITAL button does not initiate the documented hospital-send action.
* Escalate if the operator cannot access the VISU_DATA screen or cannot locate the SEND LEFT TO HOSPITAL button.
* Escalate if the result cannot be verified and operational confirmation is required, because the source does not describe confirmation prompts or follow-up indicators for this action.

## Missing Details / Known Gaps

* The source does not provide a documented confirmation prompt for this action.
* The source does not provide explicit post-action indicators to verify completion.
* The source does not state whether login is required before using SEND LEFT TO HOSPITAL.
* The source does not provide an estimated completion time.
* The source does not specify whether production stop or LOTO is required for this action.

## Source Lineage

- Candidate IDs: candidate_operator_send_left_tote_to_hospital_from_visu_data
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
