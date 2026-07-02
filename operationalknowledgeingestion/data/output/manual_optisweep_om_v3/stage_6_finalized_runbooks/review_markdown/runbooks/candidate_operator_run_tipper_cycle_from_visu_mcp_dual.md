# Run the Tipper Operation Cycle From the Visu_MCP_Dual Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_run_tipper_operation_cycle_from_visu_mcp_dual_screen_v1` |
| Title | Run the Tipper Operation Cycle From the Visu_MCP_Dual Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the primary operator station HMI screen, Visu_MCP_Dual, to place the tipper in Auto mode and start or stop the tipper operation cycle. The source identifies AUTO, CYCLE START, and CYCLE STOP as the normal operating controls and states that green illuminated bars above buttons indicate which controls are active.

## When To Use

Use this procedure during normal operator control of the tipper from the primary operator station HMI when you need to place the tipper in automatic mode and start or stop the tipper operation cycle from the Visu_MCP_Dual screen.

## Do Not Use For

* Do not use JOG as part of normal operator operation; the source states JOG is for manually controlling the end effector and gripper and the candidate notes it is not part of normal operator operation.
* Not for recovery or troubleshooting when the required control is not active or the tipper does not respond as expected; the supplied source section does not provide further recovery steps.

## Safety And Operational Notes

* Use the Visu_MCP_Dual screen as the primary operator screen for normal tipper operation.
* Green illuminated bars above buttons indicate which controls are active.
* Do not use JOG as part of normal operator operation in this runbook.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_MCP_Dual screen
* Figure 4-19 Operator Station Control Panel

## Related Operational Context

* ctx_manual_visu_mcp_dual_screen_overview_v1
* ctx_manual_tipper_control_modes_and_cycle_controls_v1

## Procedure Steps

### Step 1 — Open the Visu_MCP_Dual screen

**Responsible role:** operator

**Instruction:**
Open or navigate to the Tipper Machine Control Panel (Visu_MCP_Dual) screen on the operator station HMI.

**Expected result:**
The Visu_MCP_Dual control panel is displayed and available for operator use.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen-navigation controls and the mapping showing F3 to Visu_MCP_Dual.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The Operator Station Control Panel image showing the Visu_MCP_Dual primary screen and main control buttons.*


**Stop or Escalate If:**

* You cannot access the Visu_MCP_Dual screen from the operator station HMI.

---

### Step 2 — Verify active cycle controls

**Responsible role:** operator

**Instruction:**
Identify the AUTO, CYCLE START, and CYCLE STOP buttons on the Visu_MCP_Dual screen. Verify which controls are active by checking for green illuminated bars above the buttons.

**Expected result:**
The operator can identify the cycle control buttons and determine which ones are active.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*AUTO, CYCLE START, and CYCLE STOP buttons and the green bars above buttons that indicate active controls.*


**Stop or Escalate If:**

* The required control is not active.
* The tipper does not respond as expected and no further recovery steps are provided in this source section.

---

### Step 3 — Place the tipper in Auto mode

**Responsible role:** operator

**Instruction:**
Press AUTO to run the tipper in automatic mode.

**Expected result:**
The tipper is placed in automatic mode.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The AUTO button on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* AUTO is not active.
* Pressing AUTO does not place the tipper in automatic mode.

---

### Step 4 — Start the tipper cycle

**Responsible role:** operator

**Instruction:**
Press CYCLE START to start the tipper operation cycle when the system is in Auto mode.

**Expected result:**
The tipper operation cycle starts.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The CYCLE START button on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* The system is not in Auto mode.
* CYCLE START is not active.
* Pressing CYCLE START does not start the tipper operation cycle.

---

### Step 5 — Stop the tipper cycle

**Responsible role:** operator

**Instruction:**
Use CYCLE STOP to stop the tipper operation cycle when the system is in Auto mode.

**Expected result:**
The tipper operation cycle stops.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The CYCLE STOP button on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* The system is not in Auto mode.
* CYCLE STOP is not active.
* Pressing CYCLE STOP does not stop the tipper operation cycle.

---

### Step 6 — Review banner messages if needed

**Responsible role:** operator

**Instruction:**
If needed, review the informational banner for alarms or informational messages and use the arrows on the right side of the banner to navigate through messages.

**Expected result:**
The operator can view current banner messages and move through available messages.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The informational banner and the arrows on the right side of the banner.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The informational banner for alarms and informational messages with navigation arrows.*


**Stop or Escalate If:**

* Banner messages indicate a condition that prevents normal operation.
* The operator cannot review or navigate the displayed messages.

---

## Success Criteria

* The Visu_MCP_Dual screen is accessible from the operator station HMI.
* The operator can identify AUTO, CYCLE START, and CYCLE STOP on the primary operator screen.
* The tipper is placed in automatic mode using AUTO.
* The tipper operation cycle can be started using CYCLE START while in Auto mode.
* The tipper operation cycle can be stopped using CYCLE STOP while in Auto mode.
* The operator can review informational banner messages and navigate through them if needed.

## Failure Conditions

* The Visu_MCP_Dual screen cannot be accessed.
* The required control is not active.
* AUTO does not place the tipper in automatic mode.
* CYCLE START does not start the tipper operation cycle.
* CYCLE STOP does not stop the tipper operation cycle.
* The operator cannot review or navigate banner messages.
* The tipper does not respond as expected and the source section provides no further recovery steps.

## Escalation Guidance

* Stop and escalate if the required control is not active.
* Stop and escalate if the tipper does not respond as expected.
* Use a different source-backed recovery or maintenance procedure for troubleshooting; this source section does not provide recovery steps.

## Missing Details / Known Gaps

* The supplied source section does not provide a time estimate for completing this procedure.
* The supplied source section does not specify whether production stop is required.
* The supplied source section does not specify whether lockout/tagout is required.
* The supplied source section does not provide detailed recovery actions if a control is inactive or the tipper does not respond as expected.
* The supplied source section does not define explicit role boundaries beyond identifying station operators as the primary users of this screen.

## Source Lineage

- Candidate IDs: candidate_operator_run_tipper_cycle_from_visu_mcp_dual
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
