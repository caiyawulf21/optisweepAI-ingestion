# Open the manual referencing screen and stop the automatic tipping cycle

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_manual_referencing_screen_and_stop_cycle_v1` |
| Title | Open the manual referencing screen and stop the automatic tipping cycle |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Access the operator station HMI screen used for manual maintenance positioning and stop the automatic tipping cycle by navigating to the "Visu_Dual_MCP" screen with F3 and pressing CYCLE STOP.

## When To Use

Use when preparing to manually position the end effector for maintenance procedures from the operator station HMI, as described in the manual referencing context.

## Do Not Use For

* Do not use as a complete manual referencing procedure; the source text provided here is truncated and does not include the remaining manual referencing or manual movement steps.
* Do not use for commissioning parameter changes or other HMI procedures not explicitly covered by this source excerpt.

## Safety And Operational Notes

* This source excerpt is incomplete and only supports the opening HMI navigation and cycle stop actions.
* The procedure is associated with maintenance positioning of the end effector; additional safe movement instructions are not present in the supplied source packet.
* Escalate before attempting manual movement if further positioning instructions are required.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_Dual_MCP screen access via F3
* CYCLE STOP control on the HMI

## Procedure Steps

### Step 1 — Open the Visu_Dual_MCP screen

**Responsible role:** L2_support

**Instruction:**
On the operator station HMI, navigate to the "Visu_Dual_MCP" screen using F3.

**Expected result:**
The "Visu_Dual_MCP" screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI screen associated with manually referencing axes; use it to confirm the correct maintenance-related screen context.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Operator station HMI artifact on page 103 showing the manual referencing context and the Visu_Dual_MCP navigation reference.*


**Stop or Escalate If:**

* The HMI does not allow navigation to the "Visu_Dual_MCP" screen.
* The displayed screen does not match the maintenance/manual referencing context supported by the source.
* Additional manual movement steps are needed, since they are not included in the supplied source excerpt.

---

### Step 2 — Stop the automatic tipping cycle

**Responsible role:** L2_support

**Instruction:**
Press CYCLE STOP on the operator station HMI to stop the automatic tipping cycle.

**Expected result:**
The automatic tipping cycle is stopped.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the CYCLE STOP control on the operator station control panel figure.*

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Use the page 103 operator station HMI artifact to confirm the maintenance/manual referencing screen context where CYCLE STOP is used.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Use the page 103 operator station HMI artifact to confirm the same manual referencing context and expected HMI view.*


**Stop or Escalate If:**

* CYCLE STOP does not stop the automatic tipping cycle.
* The HMI does not show the expected control state after pressing CYCLE STOP.
* Further manual positioning instructions are required, because they are not present in the supplied source packet.

---

## Success Criteria

* The "Visu_Dual_MCP" screen is open on the operator station HMI.
* The automatic tipping cycle is stopped.
* The system is prepared for subsequent maintenance positioning actions supported elsewhere in the manual.

## Failure Conditions

* The "Visu_Dual_MCP" screen cannot be opened from the operator station HMI.
* CYCLE STOP does not stop the automatic tipping cycle.
* The source excerpt does not provide the remaining manual referencing or manual movement steps needed to continue.

## Escalation Guidance

* Escalate if the HMI does not display the expected "Visu_Dual_MCP" screen.
* Escalate if pressing CYCLE STOP does not stop the automatic tipping cycle.
* Escalate to obtain the complete maintenance/manual referencing procedure before attempting manual end effector movement.

## Missing Details / Known Gaps

* The supplied source packet does not include the remaining manual referencing steps after opening the screen and pressing CYCLE STOP.
* No explicit production stop requirement is stated in the supplied source packet.
* No explicit lockout/tagout requirement is stated in the supplied source packet.
* No time estimate is provided in the supplied source packet.
* No explicit role boundary beyond the candidate's selected L2_support role is stated in the source excerpt.

## Source Lineage

- Candidate IDs: open_manual_axis_reference_screen_and_stop_cycle
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
