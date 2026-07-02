# Interpret Control Availability and Status Indicators on the Visu_MCP_Dual Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_control_availability_and_status_indicators_on_the_visu_mcp_dual_screen_v1` |
| Title | Interpret Control Availability and Status Indicators on the Visu_MCP_Dual Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented Visu_MCP_Dual screen indicators to determine which controls are active and to review alarms or informational messages shown on the primary operator screen.

## When To Use

Use when viewing the primary operator station HMI screen to determine which Visu_MCP_Dual controls are currently active and to read alarms or informational messages shown in the banner.

## Do Not Use For

* Do not use this runbook as a corrective action procedure.
* Do not use this runbook to perform fault recovery beyond interpreting the documented screen elements.

## Safety And Operational Notes

* This runbook supports interpretation only and does not provide corrective actions.
* Escalate if the observed control state or message display cannot be matched to the documented screen elements.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_MCP_Dual screen
* Informational banner
* Visual access to button status indicators

## Related Operational Context

* ctx_manual_visu_mcp_dual_screen_overview_v1

## Procedure Steps

### Step 1 — Open the Visu_MCP_Dual screen

**Responsible role:** operator

**Instruction:**
Open the Tipper Machine Control Panel ("Visu_MCP_Dual") screen on the operator station HMI.

**Expected result:**
The Visu_MCP_Dual screen is visible on the operator station HMI.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen-navigation controls showing access to F3 "Visu_MCP_Dual" as the primary screen operators need to use.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Overall layout of the Operator Station Control Panel for the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* The Visu_MCP_Dual screen cannot be located or opened.
* The displayed screen does not match the documented Operator Station Control Panel layout.

---

### Step 2 — Identify active controls using the green bars

**Responsible role:** operator

**Instruction:**
Look above each button and identify whether the bar above the button is illuminated green to determine which buttons are active.

**Expected result:**
The operator can distinguish active buttons from inactive buttons based on the green illuminated bars.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Buttons on the primary operator HMI screen and the bars above them that illuminate green when active.*


**Stop or Escalate If:**

* The observed control state cannot be matched to the documented screen elements.
* The green-bar indication is not visible or does not correspond to the displayed controls.

---

### Step 3 — Read the informational banner

**Responsible role:** operator

**Instruction:**
Locate the informational banner and read any displayed alarm or informational message.

**Expected result:**
The current banner message is identified and understood as an alarm or informational message.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Informational banner area used to display alarms or informational messages.*


**Stop or Escalate If:**

* The banner message cannot be read.
* The displayed message area does not match the documented informational banner.

---

### Step 4 — Navigate additional banner messages

**Responsible role:** operator

**Instruction:**
Use the arrows on the right side of the banner to navigate through additional messages if more than one message is present.

**Expected result:**
Additional banner messages can be viewed one at a time using the banner arrows.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Arrows on the right side of the informational banner used to move through messages.*


**Stop or Escalate If:**

* More than one message appears to be present but the arrows do not allow navigation.
* The message navigation controls cannot be matched to the documented banner arrows.

---

### Step 5 — Record the observed control and message state

**Responsible role:** operator

**Instruction:**
Record the active controls and the displayed message text for the current system state.

**Expected result:**
A record exists of which controls were active and what message text was displayed.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Control buttons, green active-status bars, and informational banner text to capture the current screen state.*


**Stop or Escalate If:**

* The observed control state or message display cannot be matched to the documented screen elements.

---

## Success Criteria

* The Visu_MCP_Dual screen is opened and identified correctly.
* Active controls are identified using the green illuminated bars above the buttons.
* The current alarm or informational banner message is read.
* Additional messages are reviewed using the banner arrows when present.
* The active controls and displayed message text are recorded for the current system state.

## Failure Conditions

* The Visu_MCP_Dual screen cannot be opened or confirmed.
* The control-state indicators cannot be interpreted from the screen.
* The informational banner or its message text cannot be read.
* The observed control state or message display cannot be matched to the documented screen elements.

## Escalation Guidance

* Escalate if the observed control state or message display cannot be matched to the documented screen elements.
* Escalate if the Visu_MCP_Dual screen cannot be accessed or does not match the documented layout.
* This runbook supports interpretation only and does not provide corrective actions beyond the source.

## Missing Details / Known Gaps

* The source packet does not provide a time estimate for this procedure.
* The source packet does not specify whether production stop is required.
* The source packet does not specify whether lockout/tagout is required.
* The source packet does not provide a prescribed recording location or format for documenting the observed state.

## Source Lineage

- Candidate IDs: candidate_operator_interpret_controls_and_status_on_visu_mcp_dual
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
