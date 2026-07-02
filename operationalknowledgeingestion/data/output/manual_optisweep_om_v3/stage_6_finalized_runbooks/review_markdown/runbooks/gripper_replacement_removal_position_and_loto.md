# Position the gripper and lock out the tipper before gripper replacement removal

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_position_the_gripper_and_lock_out_the_tipper_before_gripper_replacement_removal_v1` |
| Title | Position the gripper and lock out the tipper before gripper replacement removal |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Prepare the selected gripper for removal by stopping the cycle, entering jog control, positioning the tipper, supporting the carriages if moved from home, locking out the tipper at the station e-panel, and confirming the correct left or right gripper selection.

## When To Use

Use this procedure when preparing for gripper replacement removal and the gripper must be positioned and the tipper locked out before further maintenance work.

## Do Not Use For

* Do not use this as the complete gripper replacement procedure; the supplied source excerpt only covers preparation and removal setup steps.
* Do not use this procedure to perform the remaining physical gripper removal steps, which are not provided in this packet.

## Safety And Operational Notes

* Use caution when lifting because components may be heavy.
* Failure to follow the caution can result in injury or equipment damage.
* Lock out the tipper at the station e-panel before continuing beyond positioning and setup.

## Access Or Tools Needed

* Operator station HMI
* Station e-panel access for lockout/tagout
* Replacement part: Gripper
* PPE: Safety glasses
* PPE: Gloves
* 2.5-mm hex wrench
* 3-mm hex wrench
* 5-mm hex wrench
* 6-mm hex wrench
* Loctite®

## Procedure Steps

### Step 1 — Open the tipper control screen at the operator station

**Responsible role:** L2_support

**Instruction:**
At the operator station HMI, navigate to the "Visu_MCP_Dual" screen.

**Expected result:**
The operator station displays the tipper control screen needed for manual control.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*The operator station screen used for manual jogging of the tipper axes; use it as visual support for the cycle stop and jog workflow.*

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*General maintenance positioning context referenced by the candidate for A-axis removal and re-assembly support.*


**Stop or Escalate If:**

* The HMI screen cannot be accessed.
* The expected tipper control interface is not present.

---

### Step 2 — Stop the cycle

**Responsible role:** L2_support

**Instruction:**
Press CYCLE STOP to stop the cycle.

**Expected result:**
The automatic tipping cycle stops.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*The HMI area used to stop the automatic tipping cycle before jogging.*


**Stop or Escalate If:**

* CYCLE STOP does not stop the cycle.
* The tipper remains in automatic operation.

---

### Step 3 — Enter jog mode

**Responsible role:** L2_support

**Instruction:**
Press JOG to manually control the tipper.

**Expected result:**
The jogging screen opens and manual axis controls are available.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*The jogging screen with axis controls for left and right tipper movement.*


**Stop or Escalate If:**

* JOG does not open the jogging screen.
* Axis controls are not available after entering jog mode.

---

### Step 4 — Move the selected tipper to the desired gripper position

**Responsible role:** L2_support

**Instruction:**
Use the axis buttons for the corresponding tipper to move the gripper to the desired location.

**Expected result:**
The selected gripper is moved to the desired removal position.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Z1/A1 controls for the left tipper and Z2/A2 controls for the right tipper, including plus/minus movement buttons.*


**Stop or Escalate If:**

* The selected axis does not respond.
* The wrong tipper or axis appears to be selected.
* The gripper cannot be positioned as needed for removal.

---

### Step 5 — Support the carriages if moved from home position

**Responsible role:** L2_support

**Instruction:**
If the gripper is moved from its home position, thread screws into the threaded holes in the column to support the carriages between the pair of holes.

**Expected result:**
Support screws are installed when required and the carriages are supported.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Support and positioning context for carriage retention during A-axis-related maintenance.*

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Example maintenance context showing positioning between threaded holes and use of support screws to prevent dropping.*

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Additional maintenance context for positioning between threaded holes and installing M6 support screws.*


**Stop or Escalate If:**

* The gripper has been moved from home position and support cannot be installed.
* There is any sign the carriages may drop or are not properly supported.

---

### Step 6 — Lock out the tipper at the station e-panel

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper at the station e-panel as referenced by "Operator Station Lockout/Tagout" on page 2.

**Expected result:**
The tipper is locked out at the station e-panel.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*General maintenance figure referenced by the candidate as image support for this preparation stage.*


**Stop or Escalate If:**

* Lockout/tagout cannot be completed at the station e-panel.
* There is any uncertainty that the tipper is fully locked out before continuing.

---

### Step 7 — Verify the correct gripper selection

**Responsible role:** L2_support

**Instruction:**
Verify the correct gripper has been selected, either the left gripper or the right gripper.

**Expected result:**
The intended gripper selection is confirmed before removal continues.

**Stop or Escalate If:**

* The left or right gripper selection cannot be confirmed.
* There is any doubt that the correct gripper is selected for removal.

---

## Success Criteria

* The cycle is stopped.
* The gripper is positioned as needed for removal.
* Carriage support is installed if the gripper was moved from home position.
* The tipper is locked out at the station e-panel.
* The correct left or right gripper selection is confirmed.

## Failure Conditions

* The required HMI screen cannot be accessed.
* The cycle does not stop.
* Jog mode or axis controls are unavailable.
* The gripper cannot be positioned as needed.
* Carriage support cannot be installed when required.
* The tipper cannot be locked out at the station e-panel.
* The correct gripper selection cannot be confirmed.
* The source excerpt does not provide the remaining physical removal steps.

## Escalation Guidance

* Stop and escalate if the HMI does not provide the expected cycle stop or jog controls.
* Stop and escalate if the gripper cannot be positioned safely or the correct axis cannot be controlled.
* Stop and escalate if carriage support cannot be installed after moving from home position.
* Do not continue with removal until lockout/tagout is completed at the station e-panel.
* Escalate for SME review because the supplied source excerpt appears truncated and does not include the full gripper replacement procedure.

## Missing Details / Known Gaps

* The source_sections text for the gripper replacement section is empty in this packet, so step wording is grounded primarily in the candidate and attached artifacts.
* The packet does not provide the full gripper replacement removal procedure beyond preparation and setup.
* The packet does not provide a direct image of the station e-panel or lockout/tagout points.
* The packet does not specify the exact screw type or size for the carriage support screws in this gripper replacement section.
* The packet does not provide an estimated completion time for this specific procedure.

## Source Lineage

- Candidate IDs: gripper_replacement_removal_position_and_loto
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
