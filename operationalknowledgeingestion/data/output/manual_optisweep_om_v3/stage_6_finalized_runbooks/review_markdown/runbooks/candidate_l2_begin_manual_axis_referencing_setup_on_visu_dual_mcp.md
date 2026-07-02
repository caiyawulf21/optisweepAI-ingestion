# Begin Manual Axis Referencing Setup on the Visu_Dual_MCP Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_begin_manual_axis_referencing_setup_on_the_visu_dual_mcp_screen_v1` |
| Title | Begin Manual Axis Referencing Setup on the Visu_Dual_MCP Screen |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Open the operator station HMI to the Visu_Dual_MCP screen using F3 and press CYCLE STOP to stop the automatic tipping cycle. This establishes the documented starting condition for manual axis referencing described in the source manual, but the remaining manual referencing steps are not present in the supplied source packet.

## When To Use

Use when preparing the OptiSweep operator station for the documented manual axis referencing procedure in section 7.3.1.2, where the source states the end effector can be manually moved into position for maintenance procedures using the HMI.

## Do Not Use For

* Do not use this as a complete manual axis referencing procedure because the supplied source excerpt only includes the initial setup steps.
* Do not continue into manual movement or referencing actions unless the missing source instructions are available and reviewed.

## Safety And Operational Notes

* The source states that the end effector can be manually moved into position for maintenance procedures using the HMI.
* Because the supplied source packet does not include the remaining manual referencing steps, stop after the documented setup actions.

## Access Or Tools Needed

* Operator station HMI
* Access to the "Visu_Dual_MCP" screen (F3)
* CYCLE STOP control

## Procedure Steps

### Step 1 — Open the Visu_Dual_MCP screen

**Responsible role:** L2_support

**Instruction:**
On the operator station HMI, navigate to the "Visu_Dual_MCP" screen using F3.

**Expected result:**
The operator station HMI displays the Visu_Dual_MCP screen.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI screen associated with manually referencing axes on page 103.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Operator station HMI artifact on page 103 showing the manual referencing context and the Visu_Dual_MCP navigation instruction.*


**Stop or Escalate If:**

* Stop if the Visu_Dual_MCP screen cannot be accessed from the operator station HMI.
* Stop if the displayed screen cannot be confirmed as the documented Visu_Dual_MCP screen.

---

### Step 2 — Stop the automatic tipping cycle

**Responsible role:** L2_support

**Instruction:**
Press CYCLE STOP to stop the automatic tipping cycle.

**Expected result:**
The automatic tipping cycle is stopped.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI context for manual axis referencing where CYCLE STOP is part of the documented setup.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Page 103 operator station artifact associated with the instruction to press CYCLE STOP.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*CYCLE STOP control on the operator station control panel reference.*


**Stop or Escalate If:**

* Stop if CYCLE STOP does not stop the automatic tipping cycle.
* Do not continue beyond this point because the remaining manual referencing procedure is not included in the supplied source packet.

---

## Success Criteria

* The operator station HMI is on the Visu_Dual_MCP screen.
* The automatic tipping cycle is stopped.
* The system matches the documented starting condition for manual axis referencing from the supplied source.

## Failure Conditions

* Unable to access the Visu_Dual_MCP screen.
* CYCLE STOP does not stop the automatic tipping cycle.
* Procedure cannot continue because the remaining manual axis referencing instructions are not present in the supplied source.

## Escalation Guidance

* Escalate for SME or maintenance review if the Visu_Dual_MCP screen cannot be accessed or confirmed.
* Escalate if the automatic tipping cycle does not stop when CYCLE STOP is pressed.
* Escalate before attempting any additional manual axis referencing or end effector movement not explicitly included in the supplied source packet.

## Missing Details / Known Gaps

* The supplied source packet does not include the remaining manual axis referencing steps after opening Visu_Dual_MCP and pressing CYCLE STOP.
* No source-supported completion criteria for the full manual referencing procedure are available in the packet.
* No source-supported production stop or LOTO requirement is explicitly stated in the supplied packet.

## Source Lineage

- Candidate IDs: candidate_l2_begin_manual_axis_referencing_setup_on_visu_dual_mcp
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
