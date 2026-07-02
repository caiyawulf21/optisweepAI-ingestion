# Use the JOG Control on the Visu_MCP_Dual Screen for Manual Tipper Positioning

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_jog_control_on_visu_mcp_dual_for_manual_tipper_positioning_v1` |
| Title | Use the JOG Control on the Visu_MCP_Dual Screen for Manual Tipper Positioning |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the JOG button on the Visu_MCP_Dual operator station screen to access manual control of the end effector and gripper position. The source explicitly states that only maintenance personnel should jog the tipper, but this source section does not provide the detailed jogging sequence, limits, or recovery actions.

## When To Use

Use when maintenance personnel need to access the documented JOG function on the Visu_MCP_Dual screen to manually control the location and position of the end effector and gripper.

## Do Not Use For

* Do not use for non-maintenance personnel; the source notes that only maintenance personnel should jog the tipper.
* Do not use as a complete jogging procedure for axis movement, limits, or recovery because those details are not provided in this source section.

## Safety And Operational Notes

* Only maintenance personnel should jog the tipper.
* This source section documents the existence and purpose of the JOG control but does not provide detailed motion controls, limits, or recovery actions.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_MCP_Dual screen
* JOG control

## Related Operational Context

* ctx_manual_tipper_control_modes_and_cycle_controls_v1
* ctx_manual_tipper_parameter_access_roles_v1

## Procedure Steps

### Step 1 — Open the Visu_MCP_Dual screen and locate JOG

**Responsible role:** L2_support

**Instruction:**
At the operator station HMI, open the Tipper Machine Control Panel (Visu_MCP_Dual) screen and locate the JOG button on the screen.

**Expected result:**
The Visu_MCP_Dual screen is displayed and the JOG button is visible.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The JOG button on the Operator Station Control Panel (Figure 4-19).*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen navigation controls showing access to Visu_MCP_Dual, including F3.*


**Stop or Escalate If:**

* The Visu_MCP_Dual screen is not available on the operator station HMI.
* The JOG button cannot be located on the displayed control panel.
* The person performing the task is not maintenance personnel.

---

### Step 2 — Select JOG for manual positioning control

**Responsible role:** L2_support

**Instruction:**
Select JOG on the Visu_MCP_Dual screen to access manual control of the location and position of the end effector and gripper.

**Expected result:**
The documented JOG function is selected for manual positioning control.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The JOG control on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* JOG cannot be selected.
* The HMI does not present the documented manual control function after JOG is selected.
* The person performing the task is not maintenance personnel.

---

### Step 3 — Limit use to the documented JOG function

**Responsible role:** L2_support

**Instruction:**
Use only the source-documented JOG function for manual positioning. Do not assume additional movement controls, limits, or recovery actions from this section because they are not described here.

**Expected result:**
Manual positioning is limited to the documented JOG access described by the source.

**Stop or Escalate If:**

* Detailed jog controls, limits, or recovery actions are needed to continue.
* There is uncertainty about how to perform actual axis movement safely using only this section.
* A reviewer determines the procedure requires additional source-supported detail before use.

---

## Success Criteria

* The Visu_MCP_Dual screen is accessed on the operator station HMI.
* The JOG button is identified and selected.
* The documented manual-control mode for positioning the end effector and gripper is accessed.
* Use is limited to maintenance personnel.

## Failure Conditions

* The Visu_MCP_Dual screen cannot be accessed.
* The JOG button cannot be located or selected.
* A non-maintenance user attempts to jog the tipper.
* Detailed movement, limit, or recovery instructions are required but not available in this source section.

## Escalation Guidance

* Escalate if the person performing the task is not maintenance personnel.
* Escalate if the HMI does not match the documented Visu_MCP_Dual/JOG layout.
* Escalate for SME review before operational use because this source section does not provide the detailed jog sequence, limits, or recovery actions.

## Missing Details / Known Gaps

* This source section does not provide the detailed jog sequence after selecting JOG.
* This source section does not provide axis-specific controls, movement directions, limits, or stop conditions.
* This source section does not provide recovery actions if manual positioning fails.
* This source section does not state whether production must be stopped before using JOG.
* This source section does not state whether lockout/tagout is required.

## Source Lineage

- Candidate IDs: candidate_l2_use_jog_control_on_visu_mcp_dual_for_manual_tipper_positioning
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
