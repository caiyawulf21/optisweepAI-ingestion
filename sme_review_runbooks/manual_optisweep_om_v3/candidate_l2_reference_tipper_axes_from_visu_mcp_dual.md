# Reference Tipper Axes From the Visu_MCP_Dual Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reference_tipper_axes_from_the_visu_mcp_dual_screen_v1` |
| Title | Reference Tipper Axes From the Visu_MCP_Dual Screen |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Visu_MCP_Dual tipper machine control panel to move axes to the home position with REF or automatically reference both tippers with AUTO REF when enabled, then verify referenced status by checking the green 'R' indicators for A1, Z1, A2, and Z2.

## When To Use

Use when tipper axes need to be moved to the home position or referenced from the Visu_MCP_Dual screen. The source states REF typically only has to be done when the system is powered on, and AUTO REF is available after the cycle has been reset.

## Do Not Use For

* Do not use this runbook as a complete troubleshooting procedure when referencing does not complete; the source does not provide additional troubleshooting steps.
* Do not use AUTO REF unless the button is enabled; the source states it is enabled after the cycle has been reset (press RESET).

## Safety And Operational Notes

* This procedure causes axis movement.
* An axis being out of reference may cause a tipper fault.
* The source does not provide full safety boundaries or precondition detail for this action.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_MCP_Dual screen
* REF control
* AUTO REF control
* Axis position/reference display

## Related Operational Context

* ctx_manual_tipper_reset_and_reference_functions_v1
* ctx_manual_tipper_axis_position_and_reference_indicators_v1
* ctx_manual_visu_mcp_dual_screen_overview_v1

## Procedure Steps

### Step 1 — Open the Visu_MCP_Dual screen and identify REF and AUTO REF

**Responsible role:** L2_support

**Instruction:**
Open the Tipper Machine Control Panel (Visu_MCP_Dual) screen and identify the REF and AUTO REF controls on the operator station control panel.

**Expected result:**
The Visu_MCP_Dual screen is open and the REF and AUTO REF controls are visible.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the REF and AUTO REF buttons on the Operator Station Control Panel for the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* The required HMI screen cannot be accessed.
* The REF or AUTO REF controls are not visible on the screen.

---

### Step 2 — Use REF to move axes to the home position

**Responsible role:** L2_support

**Instruction:**
To move axes to the home position, select REF and press the "-" button to initiate movement.

**Expected result:**
The axes begin moving to the home position.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Use the REF control on the Visu_MCP_Dual screen and identify the associated "-" button used to initiate movement.*

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Reference-related HMI layout associated with manually referencing axes.*


**Stop or Escalate If:**

* Axis movement does not initiate after selecting REF and pressing the "-" button.
* Unexpected fault behavior is observed during or after the reference attempt.

---

### Step 3 — Use AUTO REF when enabled to reference both tippers

**Responsible role:** L2_support

**Instruction:**
If AUTO REF is enabled, use AUTO REF to automatically reference the axes of both tippers. The source states this button is enabled after the cycle has been reset (press RESET).

**Expected result:**
Automatic referencing of both tipper axes is initiated.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the AUTO REF button on the Visu_MCP_Dual screen and confirm whether it is enabled.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Reference-related HMI screen associated with manual and automatic axis referencing context.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup-related screen context mentioning AUTO REF for homing axes.*


**Stop or Escalate If:**

* AUTO REF is required but the button is not enabled.
* Automatic referencing does not complete after AUTO REF is used.
* A tipper fault remains or appears after the reference attempt.

---

### Step 4 — Check A1, Z1, A2, and Z2 reference indicators

**Responsible role:** L2_support

**Instruction:**
Verify axis reference status in the A1, Z1, A2, and Z2 display area by checking the 'R' indicator for each axis.

**Expected result:**
Each axis display shows an 'R' indicator that can be checked for referenced status.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Find the A1, Z1, A2, and Z2 display area on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* Any axis does not show referenced status after the documented controls are used.
* The axis status display cannot be interpreted from the HMI.

---

### Step 5 — Confirm the green 'R' status for referenced axes

**Responsible role:** L2_support

**Instruction:**
Confirm that the 'R' circle is green to indicate the axis has been referenced.

**Expected result:**
The 'R' indicator for referenced axes is green.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Review the axis status area and confirm the 'R' circle color for each axis.*


**Stop or Escalate If:**

* The 'R' circle does not turn green for one or more axes.
* A tipper fault is present or occurs because an axis remains out of reference.

---

## Success Criteria

* The axes are moved to home or referenced using REF or AUTO REF.
* The corresponding 'R' indicators for A1, Z1, A2, and Z2 show green for referenced axes.

## Failure Conditions

* REF does not initiate axis movement.
* AUTO REF is not enabled when expected or does not complete referencing.
* One or more axes remain out of reference.
* A tipper fault occurs or remains because an axis is out of reference.

## Escalation Guidance

* Escalate if axis reference status does not become indicated as referenced after the documented controls are used.
* Escalate if AUTO REF is needed but not enabled after the cycle has been reset.
* Escalate if a tipper fault is present or occurs due to an axis being out of reference.
* Escalate if referencing does not complete, because the source does not provide additional troubleshooting.

## Missing Details / Known Gaps

* The source does not clearly assign this action to a normal operator role; L2_support is retained from the candidate.
* The source does not provide a complete safety procedure or motion hazard controls for referencing.
* The source does not specify whether production must be stopped before performing this procedure.
* The source does not specify whether lockout/tagout is required.
* The source does not provide an estimated completion time.
* The source does not provide additional troubleshooting steps if referencing does not complete.

## Source Lineage

- Candidate IDs: candidate_l2_reference_tipper_axes_from_visu_mcp_dual
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
