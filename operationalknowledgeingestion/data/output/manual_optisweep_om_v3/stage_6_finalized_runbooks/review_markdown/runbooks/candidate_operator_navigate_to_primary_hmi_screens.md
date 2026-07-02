# Navigate To The Primary Operator Station HMI Screens

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_navigate_to_the_primary_operator_station_hmi_screens_v1` |
| Title | Navigate To The Primary Operator Station HMI Screens |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station HMI on the right side of the tipper station to open the documented primary operator screens: Visu_MCP_Dual, Visu_Data, and Visu_Alarm, using the Next Screen drop-down menu, on-screen buttons, or the physical display buttons.

## When To Use

Use this procedure when a station operator needs to access the documented primary operator HMI screens at the tipper station: the main control panel screen (Visu_MCP_Dual), the data screen (Visu_Data), or the alarms screen (Visu_Alarm).

## Do Not Use For

* Do not use this runbook to operate or interpret screens beyond the source-identified operator screens unless supported elsewhere in the source material.
* Do not use this runbook for task-specific actions within the opened screens; the source only documents how to navigate to them.

## Safety And Operational Notes

* This source describes screen navigation only and does not specify lockout/tagout or production stop requirements.
* Use only the documented operator screens and navigation controls identified in the source.

## Access Or Tools Needed

* Physical access to the operator station HMI
* Operator station display controls
* Documented function key to screen mapping

## Related Operational Context

* ctx_manual_operator_station_hmi_overview_v1
* ctx_manual_operator_station_navigation_controls_v1
* ctx_manual_operator_station_primary_operator_screens_v1
* ctx_manual_visu_mcp_dual_screen_overview_v1

## Procedure Steps

### Step 1 — Go to the operator station HMI

**Responsible role:** operator

**Instruction:**
Go to the HMI screen located on the right side of the tipper station.

**Expected result:**
You are positioned at the correct operator station HMI.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*The operator station display location and right-side controls.*


**Stop or Escalate If:**

* The HMI screen cannot be located at the right side of the tipper station.
* The HMI is not available for operator use.

---

### Step 2 — Choose a documented navigation method

**Responsible role:** operator

**Instruction:**
Choose one documented navigation method: the Next Screen drop-down menu, the buttons on the right side of the screen, or the physical buttons on the right side of the display.

**Expected result:**
A valid navigation method is selected for opening the required HMI screen.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*The Next Screen drop-down menu, right-side on-screen buttons, and physical buttons on the right side of the display.*


**Stop or Escalate If:**

* The documented navigation controls do not respond.
* The available controls do not match the documented navigation methods.

---

### Step 3 — Open the main control panel screen

**Responsible role:** operator

**Instruction:**
To open the main control panel screen, use F3 and verify it navigates to "Visu_MCP_Dual."

**Expected result:**
The HMI opens the Visu_MCP_Dual screen.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*The F3 mapping on the operator station display controls.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The Visu_MCP_Dual control panel screen that should open after using F3.*


**Stop or Escalate If:**

* F3 does not open the named screen Visu_MCP_Dual.
* The opened screen does not match the documented main control panel screen.

---

### Step 4 — Open the data screen

**Responsible role:** operator

**Instruction:**
To open the data screen, use F5 and verify it navigates to "Visu_Data."

**Expected result:**
The HMI opens the Visu_Data screen.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*The F5 mapping on the operator station display controls.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The Visu_Data screen layout that should open after using F5.*


**Stop or Escalate If:**

* F5 does not open the named screen Visu_Data.
* The opened screen does not match the documented data screen.

---

### Step 5 — Open the alarms screen

**Responsible role:** operator

**Instruction:**
To open the alarms screen, use F6 and verify it navigates to "Visu_Alarm."

**Expected result:**
The HMI opens the Visu_Alarm screen.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*The F6 mapping on the operator station display controls.*


**Stop or Escalate If:**

* F6 does not open the named screen Visu_Alarm.
* The opened screen does not match the documented alarms screen.

---

### Step 6 — Use physical display selection controls when needed

**Responsible role:** operator

**Instruction:**
If using the physical display controls for selection, use the arrow buttons to move to the desired item and press the center button to select it.

**Expected result:**
The desired on-screen item is selected using the physical display controls.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*The arrow-based selection/navigation buttons and the center select button on the physical display controls.*


**Stop or Escalate If:**

* The arrow buttons do not move the selection.
* The center button does not select the highlighted item.

---

### Step 7 — Use the opened operator screen

**Responsible role:** operator

**Instruction:**
Use the opened screen needed for operator work, noting that the source identifies "Visu_MCP_Dual" as the primary screen operators need to use.

**Expected result:**
The operator is on the required documented screen for the intended operator task.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The primary Visu_MCP_Dual operator control panel screen.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The Visu_Data screen if data access is needed.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*The documented screen mappings and navigation controls used to reach the selected screen.*


**Stop or Escalate If:**

* The documented navigation controls do not open the named screens.
* The operator needs a screen or function not supported by this source material.

---

## Success Criteria

* The operator can reach the documented primary HMI screens used at the station: Visu_MCP_Dual, Visu_Data, and Visu_Alarm.
* F3 opens Visu_MCP_Dual, F5 opens Visu_Data, and F6 opens Visu_Alarm as documented.
* If physical display controls are used, the arrow buttons move selection and the center button selects the highlighted item.

## Failure Conditions

* The operator station HMI cannot be located or accessed.
* The documented navigation controls do not respond or do not open the named screens.
* F3 does not open Visu_MCP_Dual, F5 does not open Visu_Data, or F6 does not open Visu_Alarm.
* Physical arrow or center select buttons do not work as documented.
* The operator requires screens or functions not supported by this source material.

## Escalation Guidance

* Escalate if the documented navigation controls do not open the named screens.
* Escalate if the HMI or its physical display controls are unavailable or unresponsive.
* Do not assume use of other screens beyond the source-identified operator screens unless supported elsewhere in source material.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not specify whether production must be stopped before performing this navigation.
* The source does not specify lockout/tagout requirements for this navigation activity.
* The source does not provide detailed operating instructions for tasks performed within Visu_MCP_Dual, Visu_Data, or Visu_Alarm.
* No dedicated artifact for the Visu_Alarm screen was provided in this packet.

## Source Lineage

- Candidate IDs: candidate_operator_navigate_to_primary_hmi_screens
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
