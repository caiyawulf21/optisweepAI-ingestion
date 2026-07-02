# Identify And Use Operator Station Display Controls To Select HMI Screens

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_and_use_operator_station_display_controls_to_select_hmi_screens_v1` |
| Title | Identify And Use Operator Station Display Controls To Select HMI Screens |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented operator station display controls to identify available HMI screen navigation methods, match function keys F1 through F6 to their named screens, and select screens using either the on-screen buttons, corresponding physical display buttons, or the Next Screen drop-down menu.

## When To Use

Use this runbook when an operator needs to identify the operator station display controls and use the documented navigation methods to select an HMI screen at the operator station.

## Do Not Use For

* Do not use this runbook to infer undocumented meanings or uses for controls beyond the mappings and behaviors stated in the source.
* Do not use this runbook as a detailed operating guide for the individual destination screens, because the source packet only supports control mapping and navigation behavior.

## Safety And Operational Notes

* Use only the documented control mappings and navigation behaviors from the source.
* If a physical button does not navigate to the same screen as the corresponding on-screen button, stop and escalate.

## Access Or Tools Needed

* Physical access to the operator station display
* Documented control mapping from Figure 4-18 and Table 4-4

## Related Operational Context

* ctx_manual_operator_station_navigation_controls_v1
* ctx_manual_operator_station_display_button_map_v1

## Procedure Steps

### Step 1 — Locate the operator station display controls

**Responsible role:** operator

**Instruction:**
Locate the operator station display controls on the right side of the screen and on the right side of the physical display. Identify the on-screen right-side buttons, the corresponding physical display buttons, the arrow navigation buttons, the center select button, and the Next Screen drop-down menu.

**Expected result:**
The operator can visually identify the documented navigation and selection controls.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Right-side on-screen buttons, physical function buttons, arrow buttons, center select button, and Next Screen drop-down menu.*


**Stop or Escalate If:**

* The documented controls cannot be located.
* The physical display control arrangement does not match the documented figure.

---

### Step 2 — Match function keys to the documented HMI screens

**Responsible role:** operator

**Instruction:**
Identify the function key labels and compare them to the documented screen mapping: F1 = Visu_ManControl, F2 = Visu_MDs, F3 = Visu_MCP_Dual, F4 = Visu_IO_Diag, F5 = Visu_Data, and F6 = Visu_Alarm.

**Expected result:**
The operator knows which function key corresponds to the intended HMI screen.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Function key labels and the screen-navigation buttons used to access HMI screens.*

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*Example destination screen for F1 / Visu_ManControl.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Example destination screen for F3 / Visu_MCP_Dual.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Example destination screen for F5 / Visu_Data.*

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Example destination screen for F4 / Visu_IO_Diag.*


**Stop or Escalate If:**

* The function key mapping does not match the documented source.

---

### Step 3 — Use arrow buttons to navigate to an on-screen item

**Responsible role:** operator

**Instruction:**
If navigating by physical selection controls, use the arrow buttons to move to the desired on-screen item.

**Expected result:**
The desired on-screen item is highlighted or navigated to for selection.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Arrow navigation buttons used to move to items on the screen.*


**Stop or Escalate If:**

* Arrow buttons do not navigate to items on the screen.

---

### Step 4 — Press the center button to select the navigated item

**Responsible role:** operator

**Instruction:**
Press the center button to select the item currently navigated to on the screen.

**Expected result:**
The currently navigated on-screen item is selected.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Center select button used after navigating with the arrows.*


**Stop or Escalate If:**

* The center button does not select the item navigated to on the screen.

---

### Step 5 — Use the Next Screen drop-down menu for direct screen selection

**Responsible role:** operator

**Instruction:**
If navigating by menu, use the Next Screen drop-down menu to directly select the next screen to view.

**Expected result:**
The selected HMI screen opens through the drop-down menu.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Next Screen drop-down menu used for direct screen selection.*


**Stop or Escalate If:**

* The Next Screen drop-down menu is not available.
* The selected screen does not open from the drop-down menu.

---

### Step 6 — Use either the on-screen button or corresponding physical button

**Responsible role:** operator

**Instruction:**
If navigating by buttons, use either the on-screen right-side button or the corresponding physical button, noting that both should navigate to the same screen.

**Expected result:**
The intended HMI screen opens whether the operator uses the on-screen button or the corresponding physical display button.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Right-side on-screen buttons and corresponding physical display buttons used for screen navigation.*


**Stop or Escalate If:**

* The physical button does not navigate to the same screen as the corresponding on-screen button.

---

## Success Criteria

* The operator can identify the documented operator station display controls.
* The operator can match function keys F1 through F6 to the documented HMI screen names.
* The operator can select the intended HMI screen using the arrow and center buttons, the Next Screen drop-down menu, or the right-side on-screen or physical buttons as documented.

## Failure Conditions

* The documented controls cannot be identified on the operator station display.
* Function key labels do not match the documented mapping.
* Arrow navigation does not move to items on the screen.
* The center button does not select the navigated item.
* The Next Screen drop-down menu does not allow direct screen selection.
* A physical display button does not navigate to the same screen as the corresponding on-screen button.

## Escalation Guidance

* Escalate if the physical button does not navigate to the same screen as the corresponding on-screen button.
* Escalate if the control layout or function key mapping does not match the documented source.
* Do not infer undocumented meanings or uses for controls beyond the mappings and behaviors stated in the source.

## Missing Details / Known Gaps

* The source packet does not provide an estimated completion time.
* The source packet does not specify whether production stop is required.
* The source packet does not specify whether lockout/tagout is required.
* The source packet does not provide detailed purposes or operating instructions for every destination screen named in the function key mapping.
* The source packet does not provide a dedicated artifact for the Visu_MDs screen.

## Source Lineage

- Candidate IDs: candidate_operator_interpret_operator_station_display_controls
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
