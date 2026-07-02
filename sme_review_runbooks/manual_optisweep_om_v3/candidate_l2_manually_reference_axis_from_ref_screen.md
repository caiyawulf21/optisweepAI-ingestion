# Manually Reference an Axis From the REF Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_manually_reference_an_axis_from_the_ref_screen_v1` |
| Title | Manually Reference an Axis From the REF Screen |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station HMI to navigate to the Visu_Dual_MCP screen, stop the automatic tipping cycle, open the REF screen, identify any axis whose circled R indicator is clear, and start movement of the selected axis for manual referencing.

## When To Use

Use this procedure during maintenance or recovery when an axis must be manually referenced from the operator station HMI and the REF screen indicates an axis needs referencing.

## Do Not Use For

* Do not use this runbook to complete undocumented referencing steps beyond starting axis movement.
* Do not use this runbook when site documentation requires a different authorized role.
* Do not use this runbook as a full automatic axis referencing procedure.

## Safety And Operational Notes

* This procedure is in a maintenance context and involves manual movement of the end effector into position using the HMI.
* The automatic tipping cycle is stopped as part of this procedure before opening the REF screen.
* The source excerpt does not provide full completion or confirmation criteria for the manual referencing movement.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_Dual_MCP screen
* REF screen
* Controls for CYCLE STOP, REF, axis selection, and the – button

## Procedure Steps

### Step 1 — Open the Visu_Dual_MCP screen

**Responsible role:** L2_support

**Instruction:**
On the operator station HMI, navigate to the "Visu_Dual_MCP" screen using F3.

**Expected result:**
The Visu_Dual_MCP screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI context for manually referencing axes and access to the Visu_Dual_MCP screen.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Operator station HMI view associated with the manual referencing procedure on page 103.*


**Stop or Escalate If:**

* The Visu_Dual_MCP screen cannot be accessed from the operator station HMI.
* The HMI does not match the documented maintenance procedure context.

---

### Step 2 — Stop the automatic tipping cycle

**Responsible role:** L2_support

**Instruction:**
Press CYCLE STOP to stop the automatic tipping cycle.

**Expected result:**
The automatic tipping cycle is stopped.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI context where CYCLE STOP is used before manual referencing.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Page 103 operator station screen associated with navigating to Visu_Dual_MCP and stopping the cycle.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*CYCLE STOP control on the operator station control panel.*


**Stop or Escalate If:**

* The automatic tipping cycle does not stop.
* The CYCLE STOP control is unavailable or inactive.

---

### Step 3 — Open the REF screen

**Responsible role:** L2_support

**Instruction:**
Press REF to open the reference screen.

**Expected result:**
The reference screen opens.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*REF control on the operator station control panel.*

![artifact_page_104_image_2](assets/artifact_page_104_image_2.jpeg)

*Reference screen context associated with manual axis referencing.*

![artifact_page_104_image_3](assets/artifact_page_104_image_3.jpeg)

*REF screen context used for manual axis referencing.*


**Stop or Escalate If:**

* The REF screen cannot be opened.
* The REF control is unavailable or inactive.

---

### Step 4 — Identify the axis that needs referencing

**Responsible role:** L2_support

**Instruction:**
Check the circled "R" next to the axis information. If the circled "R" is clear, that axis needs to be referenced.

**Expected result:**
The axis requiring reference is identified from the REF screen.

**Screens / Images:**

![artifact_page_104_image_2](assets/artifact_page_104_image_2.jpeg)

*Axis information and the circled R reference-status indicator.*

![artifact_page_104_image_3](assets/artifact_page_104_image_3.jpeg)

*Reference-status display showing how to identify an axis that needs referencing.*


**Stop or Escalate If:**

* The circled R indicator is not visible.
* The axis reference status cannot be determined from the REF screen.

---

### Step 5 — Start movement of the selected axis

**Responsible role:** L2_support

**Instruction:**
Select the axis to be referenced and press the – button to start movement of the axis.

**Expected result:**
The selected axis begins movement for manual referencing.

**Screens / Images:**

![artifact_page_104_image_2](assets/artifact_page_104_image_2.jpeg)

*Axis selection area and minus button used to start movement.*

![artifact_page_104_image_3](assets/artifact_page_104_image_3.jpeg)

*Manual-referencing controls for selecting an axis and pressing the minus button.*


**Stop or Escalate If:**

* The selected axis does not begin movement.
* The source excerpt does not provide completion criteria for the movement, so do not continue beyond the documented action without additional approved guidance.

---

## Success Criteria

* The operator reaches the Visu_Dual_MCP screen.
* The automatic tipping cycle is stopped.
* The REF screen is opened.
* An axis needing reference is identified by a clear circled R indicator.
* The selected axis begins movement after the – button is pressed.

## Failure Conditions

* The operator cannot access the Visu_Dual_MCP screen.
* The automatic tipping cycle does not stop.
* The REF screen does not open.
* The circled R indicator cannot be interpreted or the axis needing reference cannot be identified.
* The selected axis does not begin movement.
* The source does not provide completion criteria beyond starting movement.

## Escalation Guidance

* Escalate if the HMI screens or controls described in the source are unavailable.
* Escalate if the automatic tipping cycle cannot be stopped with CYCLE STOP.
* Escalate if the REF screen does not open or the circled R status cannot be determined.
* Escalate if the selected axis does not begin movement after pressing the – button.
* Stop short of inventing additional actions or confirmation checks because the source excerpt does not include completion criteria for the manual referencing movement.

## Missing Details / Known Gaps

* The source excerpt does not provide completion criteria for the manual referencing movement.
* The source excerpt does not state how to confirm that manual referencing is complete.
* The source excerpt does not provide recovery actions if the axis does not move.
* The source excerpt does not specify whether lockout/tagout is required.
* The source excerpt does not provide an estimated completion time.

## Source Lineage

- Candidate IDs: candidate_l2_manually_reference_axis_from_ref_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
