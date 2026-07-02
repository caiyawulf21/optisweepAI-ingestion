# Select Another HMI Screen From The VISU_DATA Screen Drop-Down

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_select_another_hmi_screen_from_the_visu_data_screen_drop_down_v1` |
| Title | Select Another HMI Screen From The VISU_DATA Screen Drop-Down |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the VISU_DATA screen drop-down menu on the operator station HMI to directly select another screen to view.

## When To Use

Use this procedure when the operator is on the VISU_DATA screen and needs to directly navigate to another operator station HMI screen using the screen-selection drop-down menu.

## Do Not Use For

* Do not use this runbook to identify the full list of available screen names, because this source section does not enumerate the menu contents.

## Safety And Operational Notes

* This source-supported action is an HMI navigation task.
* No lockout/tagout requirement is stated in the supplied source packet.
* No production stop requirement is stated in the supplied source packet.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen

**Responsible role:** operator

**Instruction:**
Go to the VISU_DATA screen on the operator station HMI.

**Expected result:**
The VISU_DATA screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen layout, including login controls, message banner, and tipper statistics.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Display controls and navigation methods associated with operator station HMI screens, including access to VISU_DATA.*


**Stop or Escalate If:**

* The VISU_DATA screen cannot be reached or displayed.

---

### Step 2 — Locate the screen-selection drop-down

**Responsible role:** operator

**Instruction:**
On the VISU_DATA screen, find the drop-down menu used to directly select the screen to view.

**Expected result:**
The screen-selection drop-down is identified on the VISU_DATA screen.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen area containing the screen-selection drop-down.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Drop-down menu and related navigation controls used for direct screen selection.*


**Stop or Escalate If:**

* The drop-down menu is not visible or cannot be identified on the VISU_DATA screen.

---

### Step 3 — Open the drop-down menu

**Responsible role:** operator

**Instruction:**
Open the screen-selection drop-down menu on the VISU_DATA screen.

**Expected result:**
The drop-down menu opens and presents available screen choices.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Navigation controls and drop-down menu used to access HMI screens.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen location of the drop-down before selection.*


**Stop or Escalate If:**

* The drop-down menu does not open.

---

### Step 4 — Select the desired screen

**Responsible role:** operator

**Instruction:**
From the open drop-down menu, select the desired screen from the available list.

**Expected result:**
The selected screen is chosen from the drop-down menu.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen as the starting point for direct screen selection.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen-navigation controls and documented examples of available operator station screens.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Example destination screen: Visu_MCP_Dual / operator station control panel.*

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*Example destination screen: VISU_MANCONTROL.*

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Example destination screen: VISU_MDS.*

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Example destination screen: VISU_IO_DIAG.*


**Stop or Escalate If:**

* The desired screen cannot be selected.
* The source section does not provide the full list of screen names and the operator cannot determine the correct destination.

---

### Step 5 — Verify the selected screen displays

**Responsible role:** operator

**Instruction:**
Verify that the operator station HMI changes to the selected screen.

**Expected result:**
The operator station HMI displays the selected screen.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Example of a valid destination screen after navigation.*

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*Example of a valid destination screen after navigation.*

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Example of a valid destination screen after navigation.*

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Example of a valid destination screen after navigation.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Reference starting screen for comparison if the display does not change.*


**Stop or Escalate If:**

* The selected screen does not display.
* The HMI does not change screens after selection.

---

## Success Criteria

* The operator station HMI displays the screen selected from the VISU_DATA drop-down menu.

## Failure Conditions

* The VISU_DATA screen cannot be opened.
* The drop-down menu cannot be found.
* The drop-down menu does not open.
* The desired screen cannot be selected.
* The selected screen does not display after selection.

## Escalation Guidance

* Escalate if the drop-down menu does not open or the selected screen does not display.
* Escalate if the operator cannot determine the correct destination because the source section does not list the available screen names.

## Missing Details / Known Gaps

* The supplied source section does not enumerate the full list of screen names available in the VISU_DATA drop-down menu.
* The supplied source does not provide an estimated completion time.
* The supplied source does not state whether production must be stopped.
* The supplied source does not state any lockout/tagout requirement.
* The supplied source does not provide detailed troubleshooting beyond escalating if the drop-down does not open or the selected screen does not display.

## Source Lineage

- Candidate IDs: candidate_operator_navigate_to_another_hmi_screen_from_visu_data
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
