# Lock Out And Tag Out The Operator Station From The Visu_Dual_MCP Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_lock_out_and_tag_out_the_operator_station_from_the_visu_dual_mcp_screen_v1` |
| Title | Lock Out And Tag Out The Operator Station From The Visu_Dual_MCP Screen |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station HMI to open the Visu_Dual_MCP screen, stop the cycle with CYCLE STOP, optionally reposition the carriages using JOG and the axis +/- controls, then turn the operator station electrical panel power switch to OFF and apply lockout/tagout.

## When To Use

Use when the operator station must be placed into a stopped and locked/tagged out state from the Visu_Dual_MCP HMI workflow, including cases where carriage repositioning is needed before lockout/tagout.

## Do Not Use For

* Do not use as a basic operator procedure without site authorization.
* Do not use when safe lockout/tagout execution requires details not present in this source excerpt.
* Do not use this excerpt as the sole source for detailed jogging instructions; the source refers to "Jogging the Tipper" for those details.

## Safety And Operational Notes

* If the operator approaches or extends their hand into the lifting connecting rod assembly while the robot is lifting, it may cause serious personal injury.
* Be aware of the movement trajectory of this product, and make sure to not interfere with the line.
* Do not touch the tippers while the system is powered ON.
* This procedure includes hazardous energy isolation and powered equipment positioning.

## Access Or Tools Needed

* Access to the operator station HMI
* Access to the "Visu_Dual_MCP" screen
* Access to the operator station electrical panel
* Lockout/tagout equipment
* Authorization to perform lockout/tagout

## Related Operational Context

* ctx_manual_visu_dual_mcp_screen_reference_v1
* ctx_manual_lift_connecting_rod_safety_v1
* ctx_manual_movement_trajectory_line_interference_safety_v1
* ctx_manual_tippers_power_on_touch_hazard_v1

## Procedure Steps

### Step 1 — Open the Visu_Dual_MCP screen

**Responsible role:** L2_support

**Instruction:**
At the operator station HMI, navigate to the "Visu_Dual_MCP" screen.

**Expected result:**
The Visu_Dual_MCP screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Operator station HMI context showing navigation to the "Visu_Dual_MCP" screen using F3.*

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI context associated with Visu_Dual_MCP and maintenance positioning.*

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Operator station screen used for manual jogging after entering the Visu_Dual_MCP workflow.*


**Stop or Escalate If:**

* The Visu_Dual_MCP screen cannot be accessed.
* The HMI does not present the expected stop or jog controls.

---

### Step 2 — Stop the cycle

**Responsible role:** L2_support

**Instruction:**
Press CYCLE STOP.

**Expected result:**
The automatic tipping cycle is stopped from the operator station HMI.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the CYCLE STOP control on the operator station control panel screen.*

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Operator station screen context used before entering JOG/manual movement.*


**Stop or Escalate If:**

* CYCLE STOP is unavailable on the HMI.
* The automatic tipping cycle does not stop.

---

### Step 3 — Enter jog mode if repositioning is needed

**Responsible role:** L2_support

**Instruction:**
If carriage repositioning is needed before lockout/tagout, press JOG.

**Expected result:**
The jogging/manual positioning screen is opened when repositioning is required.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Manual mode/jogging screen with axis controls and plus/minus movement buttons.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the JOG button used for manual positioning of the end effector and gripper.*


**Stop or Escalate If:**

* Repositioning is required but JOG cannot be accessed.
* Safe repositioning requires details beyond those provided in this excerpt.

---

### Step 4 — Select the axis and reposition the carriages

**Responsible role:** L2_support

**Instruction:**
Select the corresponding axis for the tipper and use the + and - buttons to move the carriages. Refer to "Jogging the Tipper" for detailed jogging instructions.

**Expected result:**
The required carriage repositioning is completed using the documented axis selection and +/- controls.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Axis controls for Z1, A1, Z2, and A2 and the plus/minus buttons used to move the selected axis.*


**Stop or Escalate If:**

* Personnel would need to approach the lifting connecting rod assembly while the robot is lifting.
* Personnel would interfere with the movement trajectory of the product or line.
* Anyone would need to touch the tippers while the system is powered ON.
* Detailed jogging guidance is required beyond the source excerpt.

---

### Step 5 — Turn the operator station power switch off and apply lockout/tagout

**Responsible role:** L2_support

**Instruction:**
At the operator station electrical panel, turn the power switch to "OFF" and apply lockout/tagout.

**Expected result:**
The operator station power switch is OFF and lockout/tagout has been applied.

**Stop or Escalate If:**

* The operator station electrical panel cannot be accessed.
* The power switch cannot be turned to OFF.
* Site-required lockout/tagout execution details are not available in this excerpt.

---

## Success Criteria

* The Visu_Dual_MCP screen was used to stop the cycle with CYCLE STOP.
* Any required carriage repositioning was completed using JOG, axis selection, and the + / - controls.
* The operator station electrical panel power switch was turned to OFF.
* Lockout/tagout was applied at the operator station.

## Failure Conditions

* The Visu_Dual_MCP screen cannot be accessed.
* CYCLE STOP does not stop the cycle.
* JOG or axis movement controls are unavailable when repositioning is required.
* Safe repositioning cannot be completed using the available source guidance.
* The operator station power switch cannot be turned OFF or lockout/tagout cannot be applied.

## Escalation Guidance

* Escalate if safe lockout/tagout execution requires details not present in this excerpt.
* Escalate if detailed jogging instructions are needed beyond the source reference to "Jogging the Tipper."
* Escalate if any step would require personnel to enter the motion path, approach the lifting connecting rod assembly during lifting, or touch the tippers while powered on.

## Missing Details / Known Gaps

* The excerpt does not provide the detailed jogging instructions and instead refers to "Jogging the Tipper".
* The excerpt does not provide a detailed lockout/tagout subprocedure beyond turning the power switch to OFF and applying LOTO.
* No estimated completion time is provided in the source.
* No explicit verification method for confirming zero energy state is provided in the supplied source packet.

## Source Lineage

- Candidate IDs: candidate_l2_operator_station_lockout_tagout_from_visu_dual_mcp
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
