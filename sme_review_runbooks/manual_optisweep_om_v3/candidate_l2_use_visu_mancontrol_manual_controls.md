# Use VISU_MANCONTROL Screen Manual Controls For Tipper Functions

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_visu_mancontrol_screen_manual_controls_for_tipper_functions_v1` |
| Title | Use VISU_MANCONTROL Screen Manual Controls For Tipper Functions |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Operator Station HMI VISU_MANCONTROL screen, as seen by personnel logged in as maintenance, to perform documented manual control actions for the corresponding tipper. The source documents GRIPPERS OPEN/CLOSE, LAMP TEST, LEFT/RIGHT TIPPER FAULT RESET, and LEFT/RIGHT TIPPER DISABLE, and states that AIR BLOWOFF is not currently used.

## When To Use

Use when maintenance-level personnel need to access the VISU_MANCONTROL screen and perform one of the documented manual control actions for a tipper: manually open or close the gripper, run a lamp test, reset a tipper after a fault, or disable a tipper.

## Do Not Use For

* Do not use AIR BLOWOFF from this screen because the source states this button is not currently used.
* Do not use this runbook as a complete safety or recovery procedure; the source does not provide safety prerequisites, interlocks, or recovery detail for these manual controls.

## Safety And Operational Notes

* This runbook is not support-safe based on the source packet; the controls can directly affect tipper behavior.
* The source does not provide prerequisites, constraints, interlocks, or safe-use boundaries for manual actuation on this screen.
* Review by an SME is needed before exposing this procedure for routine support use.

## Access Or Tools Needed

* Operator Station HMI access
* Maintenance login
* VISU_MANCONTROL screen
* Visual and audible access to the corresponding stacklight and alarm

## Related Operational Context

* ctx_manual_visu_mancontrol_screen_overview_v1
* ctx_manual_system_api_control_functions_v1

## Procedure Steps

### Step 1 — Log in and open the VISU_MANCONTROL screen

**Responsible role:** L2_support

**Instruction:**
Log in on the Operator Station HMI with maintenance-level access and open the VISU_MANCONTROL screen.

**Expected result:**
The VISU_MANCONTROL screen is displayed for a maintenance-level user.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The maintenance-user VISU_MANCONTROL screen layout and manual control buttons.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen navigation controls showing F1 mapped to Visu_ManControl.*


**Stop or Escalate If:**

* Maintenance-level access is not available.
* The VISU_MANCONTROL screen cannot be reached from the Operator Station HMI.

---

### Step 2 — Identify the required manual control

**Responsible role:** L2_support

**Instruction:**
On the VISU_MANCONTROL screen, identify the corresponding manual control for the intended action: GRIPPERS OPEN/CLOSE, LAMP TEST, LEFT TIPPER FAULT RESET, RIGHT TIPPER FAULT RESET, LEFT TIPPER DISABLE, or RIGHT TIPPER DISABLE.

**Expected result:**
The correct manual control for the intended tipper action is identified before actuation.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The manual control buttons for GRIPPERS OPEN/CLOSE, LAMP TEST, LEFT/RIGHT TIPPER FAULT RESET, LEFT/RIGHT TIPPER DISABLE, and AIR BLOWOFF.*


**Stop or Escalate If:**

* The intended action is not one of the documented VISU_MANCONTROL functions.
* There is uncertainty about which tipper control should be used.

---

### Step 3 — Use GRIPPERS OPEN/CLOSE if manual gripper actuation is needed

**Responsible role:** L2_support

**Instruction:**
If the intended action is gripper actuation, press GRIPPERS OPEN/CLOSE for the corresponding tipper to manually open or close the gripper.

**Expected result:**
The corresponding tipper gripper manually opens or closes.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The GRIPPERS OPEN/CLOSE control on the maintenance manual control screen.*


**Stop or Escalate If:**

* The gripper does not manually open or close after pressing GRIPPERS OPEN/CLOSE.

---

### Step 4 — Use LAMP TEST and verify alarm indications

**Responsible role:** L2_support

**Instruction:**
If the intended action is a lamp test, press LAMP TEST and verify that the audible alarm sounds and the stacklight flashes red.

**Expected result:**
The audible alarm sounds and the stacklight flashes red.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The LAMP TEST control on the maintenance manual control screen.*


**Stop or Escalate If:**

* The audible alarm does not sound after pressing LAMP TEST.
* The stacklight does not flash red after pressing LAMP TEST.
* The documented effect does not occur.

---

### Step 5 — Use LEFT or RIGHT TIPPER FAULT RESET after a fault

**Responsible role:** L2_support

**Instruction:**
If the intended action is fault reset, press LEFT TIPPER FAULT RESET or RIGHT TIPPER FAULT RESET for the corresponding tipper after a fault.

**Expected result:**
The corresponding tipper is reset after a fault.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The LEFT/RIGHT TIPPER FAULT RESET controls on the maintenance manual control screen.*


**Stop or Escalate If:**

* The corresponding tipper does not reset after pressing the fault reset control.
* The source does not provide additional recovery detail for the fault condition.

---

### Step 6 — Use LEFT or RIGHT TIPPER DISABLE and verify blue stacklight

**Responsible role:** L2_support

**Instruction:**
If the intended action is tipper disable, press LEFT TIPPER DISABLE or RIGHT TIPPER DISABLE for the corresponding tipper and verify that the stacklight illuminates solid blue.

**Expected result:**
The corresponding tipper is disabled and the stacklight illuminates solid blue.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The LEFT/RIGHT TIPPER DISABLE controls on the maintenance manual control screen.*


**Stop or Escalate If:**

* The corresponding tipper does not disable after pressing the disable control.
* The stacklight does not illuminate solid blue.
* The documented effect does not occur.

---

### Step 7 — Do not use AIR BLOWOFF from this screen

**Responsible role:** L2_support

**Instruction:**
Do not use the AIR BLOWOFF button on the VISU_MANCONTROL screen.

**Expected result:**
AIR BLOWOFF is not actuated from this procedure.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The AIR BLOWOFF button on the maintenance manual control screen.*


**Stop or Escalate If:**

* There is a request to use AIR BLOWOFF from this screen despite the source stating it is not currently used.

---

## Success Criteria

* The VISU_MANCONTROL screen is accessed with maintenance-level login.
* The intended documented control is selected and actuated.
* The selected control produces the documented effect: gripper opens/closes, lamp test sounds the audible alarm and flashes the stacklight red, fault reset resets the corresponding tipper after a fault, or tipper disable illuminates the stacklight solid blue.

## Failure Conditions

* Maintenance-level access is unavailable.
* VISU_MANCONTROL cannot be opened.
* The selected control does not produce the documented effect.
* The audible alarm or stacklight behavior does not match the documented lamp test or disable indication.
* AIR BLOWOFF is considered for use even though the source states it is not currently used.

## Escalation Guidance

* Escalate if maintenance-level access is not available.
* Escalate if the documented effect does not occur after pressing the selected control.
* Escalate for SME review because the source does not provide safety prerequisites, interlocks, or recovery detail for these manual controls.

## Missing Details / Known Gaps

* The source does not provide explicit safety prerequisites or interlocks for using these manual controls.
* The source does not state whether production must be stopped before using these controls.
* The source does not state whether lockout/tagout is required.
* The source does not provide estimated execution time.
* The source does not provide detailed recovery actions if a control does not produce the documented effect.
* The source does not describe confirmation details beyond the documented effects for gripper open/close and fault reset.

## Source Lineage

- Candidate IDs: candidate_l2_use_visu_mancontrol_manual_controls
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
