# Copy VISU_MDS Machine Data Parameters From the Opposite Tipper to the Selected Axis

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_copy_visu_mds_machine_data_parameters_from_the_opposite_tipper_to_the_selected_axis_v1` |
| Title | Copy VISU_MDS Machine Data Parameters From the Opposite Tipper to the Selected Axis |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the VISU_MDS Machine Data screen to copy parameters from the other tipper to the selected axis. The source states the Machine Data screen contains parameters for axes Z1, A1, Z2, and A2, and that the COPY FROM OPPOSITE button copies parameters to the selected axis from the other tipper. The same source also states these parameters generally do not require changing unless a motor is replaced.

## When To Use

Use when a source-backed need exists to copy machine data parameters from one tipper to the selected axis on the opposite tipper using the VISU_MDS Machine Data screen.

## Do Not Use For

* Do not use for routine operator adjustments of machine parameters.
* Do not use when the reason for changing or copying parameters is unclear.
* Do not use as a procedure for manual parameter editing, because the source does not provide edit, save, or confirmation details.

## Safety And Operational Notes

* The source states these parameters do not require changing unless a motor is replaced.
* Treat this as a controlled machine-parameter action and stop if the source-backed reason for copying is not established.
* The source does not provide save, confirmation, or rollback details.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_MDS Machine Data screen
* COPY FROM OPPOSITE button

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1

## Procedure Steps

### Step 1 — Open the VISU_MDS Machine Data screen

**Responsible role:** L2_support

**Instruction:**
Open the VISU_MDS "Machine Data" screen on the operator station HMI.

**Expected result:**
The Machine Data screen is displayed.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*The VISU_MDS Machine Data view and its axis parameter layout for Z1, A1, Z2, and A2.*

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*Reference for operator station HMI access to the Visu_MDs screen during controller parameter work.*


**Stop or Escalate If:**

* The VISU_MDS Machine Data screen is not accessible.
* You cannot confirm you are on the Machine Data screen used for axis parameters.

---

### Step 2 — Identify the selected axis

**Responsible role:** L2_support

**Instruction:**
Identify the selected axis on the Machine Data screen from the available axes Z1, A1, Z2, and A2.

**Expected result:**
A single intended target axis is identified on the screen.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Axis parameter settings for Z1, A1, Z2, and A2 so the selected target axis can be identified.*


**Stop or Escalate If:**

* The intended target axis cannot be clearly identified.
* There is uncertainty about which axis should receive the copied parameters.

---

### Step 3 — Locate the COPY FROM OPPOSITE control

**Responsible role:** L2_support

**Instruction:**
Locate the COPY FROM OPPOSITE button on the VISU_MDS Machine Data screen.

**Expected result:**
The COPY FROM OPPOSITE button is visible and ready to be used for the selected axis.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*The COPY FROM OPPOSITE button on the Machine Data screen.*


**Stop or Escalate If:**

* The COPY FROM OPPOSITE button cannot be found on the Machine Data screen.

---

### Step 4 — Copy parameters from the opposite tipper

**Responsible role:** L2_support

**Instruction:**
Use COPY FROM OPPOSITE to copy parameters to the selected axis from the other tipper.

**Expected result:**
The selected axis receives parameters from the other tipper.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*The selected axis area and the COPY FROM OPPOSITE control during the parameter copy action.*


**Stop or Escalate If:**

* The reason for changing or copying parameters is unclear.
* You are being asked to manually edit parameters instead of using the documented copy function.
* The source-backed copy action cannot be completed or its effect is unclear.

---

### Step 5 — Verify the selected axis shows the copied parameters

**Responsible role:** L2_support

**Instruction:**
Verify on the Machine Data screen that the selected axis now shows the copied parameter set.

**Expected result:**
The selected axis displays the copied parameter set on the Machine Data screen.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*The selected axis parameter settings after using COPY FROM OPPOSITE.*


**Stop or Escalate If:**

* The selected axis does not show the expected copied parameter set.
* The source does not provide enough detail to confirm save, confirmation, or persistence behavior after the copy.

---

## Success Criteria

* The VISU_MDS Machine Data screen is opened.
* The intended target axis is identified as one of Z1, A1, Z2, or A2.
* COPY FROM OPPOSITE is used on the selected axis.
* The selected axis shows the copied parameter set from the other tipper on the Machine Data screen.

## Failure Conditions

* The VISU_MDS Machine Data screen cannot be accessed.
* The intended target axis cannot be confirmed.
* The COPY FROM OPPOSITE button cannot be identified or used.
* The selected axis does not show the copied parameter set after the action.
* The task requires manual parameter editing, save behavior, or confirmation behavior not documented in the source.

## Escalation Guidance

* Escalate if the required source-backed reason for changing or copying parameters is unclear.
* Escalate if the task appears to require manual parameter editing rather than the documented COPY FROM OPPOSITE action.
* Escalate if the result cannot be verified on the Machine Data screen.
* Escalate for SME review when save, confirmation, persistence, or rollback behavior is needed, because the source does not provide those details.

## Missing Details / Known Gaps

* The source does not provide explicit navigation steps to open the VISU_MDS Machine Data screen within this section.
* The source does not provide save, confirmation, or persistence details after using COPY FROM OPPOSITE.
* The source does not provide rollback or recovery steps if the wrong axis is selected.
* The source does not specify whether production must be stopped before performing this action.
* The source does not specify LOTO requirements for this action.
* The source does not provide a time estimate for completing this procedure.

## Source Lineage

- Candidate IDs: candidate_l2_copy_visu_mds_parameters_from_opposite_tipper_axis
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
