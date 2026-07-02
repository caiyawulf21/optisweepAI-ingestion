# Open the Visu_Dual_MCP screen and stop the automatic tipping cycle for manual axis positioning

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_visu_dual_mcp_and_stop_cycle_for_manual_axis_positioning_v1` |
| Title | Open the Visu_Dual_MCP screen and stop the automatic tipping cycle for manual axis positioning |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Source-specific preparation procedure for maintenance-related manual axis positioning. On the operator station HMI, navigate to the Visu_Dual_MCP screen using F3 and press CYCLE STOP to stop the automatic tipping cycle before any further manual positioning actions.

## When To Use

Use when preparing the operator station for maintenance procedures that require the end effector to be manually moved into position using the HMI.

## Do Not Use For

* Do not use this runbook as a complete manual referencing procedure; the source packet only supports the setup steps.
* Do not continue into manual movement or referencing actions unless additional source-backed instructions are available.

## Safety And Operational Notes

* This source only supports preparation steps for maintenance positioning.
* Stop after CYCLE STOP unless additional source-backed instructions are available for the intended maintenance task.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_Dual_MCP screen (F3)
* CYCLE STOP control

## Procedure Steps

### Step 1 — Open the Visu_Dual_MCP screen

**Responsible role:** L2_support

**Instruction:**
On the operator station HMI, navigate to the "Visu_Dual_MCP" screen using F3.

**Expected result:**
The Visu_Dual_MCP screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*The operator station HMI context for the manually referencing axes procedure and the Visu_Dual_MCP navigation reference.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*The operator station screen associated with manually referencing tipper axes during maintenance.*


**Stop or Escalate If:**

* The Visu_Dual_MCP screen cannot be opened from the operator station HMI.
* The displayed screen does not match the expected maintenance positioning context.

---

### Step 2 — Stop the automatic tipping cycle

**Responsible role:** L2_support

**Instruction:**
Press CYCLE STOP to stop the automatic tipping cycle.

**Expected result:**
The automatic tipping cycle is stopped.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*The operator station HMI context associated with pressing CYCLE STOP in the manually referencing axes procedure.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*The CYCLE STOP control on the operator station control panel.*


**Stop or Escalate If:**

* CYCLE STOP is not available on the displayed HMI screen.
* The automatic tipping cycle does not stop.
* Additional manual movement steps are needed but are not available from this source-backed procedure.

---

## Success Criteria

* The Visu_Dual_MCP screen is open on the operator station HMI.
* The automatic tipping cycle is stopped.
* The operator station is prepared for subsequent maintenance-specific manual positioning instructions, if separately available.

## Failure Conditions

* The Visu_Dual_MCP screen cannot be accessed.
* The automatic tipping cycle does not stop.
* The procedure requires additional manual movement or referencing steps that are not provided in this source.

## Escalation Guidance

* Stop after CYCLE STOP if the next required maintenance positioning steps are not available from an approved source-backed procedure.
* Escalate for SME review if the Visu_Dual_MCP screen cannot be reached or if CYCLE STOP does not stop the automatic tipping cycle.
* Escalate when full manual referencing or movement instructions are required, because this source packet is incomplete for those actions.

## Missing Details / Known Gaps

* The source packet does not provide the remaining manual movement or manual referencing steps after CYCLE STOP.
* The source packet does not provide explicit confirmation indicators for successful cycle stop on this specific page.
* The source packet does not specify whether production stop or LOTO is required for this preparation action.

## Source Lineage

- Candidate IDs: open_visu_dual_mcp_and_stop_cycle_for_manual_axis_positioning
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
