# Check Axis Position, Reference State, and Motion Status on the Visu_MCP_Dual Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_axis_position_reference_state_and_motion_status_on_visu_mcp_dual_screen_v1` |
| Title | Check Axis Position, Reference State, and Motion Status on the Visu_MCP_Dual Screen |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | `operator` |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Visu_MCP_Dual axis display fields on the operator station HMI to verify left and right gripper axis positions, determine whether each axis is referenced, and identify whether an axis is currently in motion based on the documented field labels and color indicators.

## When To Use

Use this procedure when you need to interpret the Visu_MCP_Dual screen to confirm current A1, Z1, A2, and Z2 axis positions, verify whether each axis has been referenced, and determine whether an axis is in motion. This is appropriate for troubleshooting-oriented observation of tipper axis state on the HMI.

## Do Not Use For

* Do not use this procedure as a corrective action for restoring reference state or clearing faults; the source packet only supports observation and interpretation.
* Do not use this procedure to command motion, home axes, or change settings; those actions are not defined in this source-supported candidate.

## Safety And Operational Notes

* This candidate is limited to observation and interpretation on the HMI; no corrective actions are supported by the source packet.
* An axis being out of reference may cause a tipper fault.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_MCP_Dual screen
* Axis position and reference status display

## Related Operational Context

* ctx_manual_tipper_axis_position_and_reference_indicators_v1

## Procedure Steps

### Step 1 — Open the Visu_MCP_Dual screen and locate the axis fields

**Responsible role:** L1_support

**Instruction:**
Open the Tipper Machine Control Panel ("Visu_MCP_Dual") screen on the operator station HMI and locate the A1, Z1, A2, and Z2 boxes in the axis position area.

**Expected result:**
The Visu_MCP_Dual screen is visible and the A1, Z1, A2, and Z2 boxes can be identified.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Overall Visu_MCP_Dual operator station control panel view to orient to the primary screen and axis display area.*


**Stop or Escalate If:**

* Escalate if the displayed screen does not match the documented Visu_MCP_Dual control panel view.
* Escalate if the axis position area cannot be located on the HMI.

---

### Step 2 — Read left gripper axis positions

**Responsible role:** L1_support

**Instruction:**
Read A1 and Z1 on the screen as the current position in steps for the left gripper A-axis and Z-axis.

**Expected result:**
The current left gripper A-axis and Z-axis positions are identified from the displayed values.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Axis position boxes corresponding to A1 and Z1 for the left gripper.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Axis naming reference showing A1 and Z1 used for the left axis.*


**Stop or Escalate If:**

* Escalate if A1 or Z1 cannot be read from the HMI.
* Escalate if the left-axis labels do not match the documented A1/Z1 naming.

---

### Step 3 — Read right gripper axis positions

**Responsible role:** L1_support

**Instruction:**
Read A2 and Z2 on the screen as the current position in steps for the right gripper A-axis and Z-axis.

**Expected result:**
The current right gripper A-axis and Z-axis positions are identified from the displayed values.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Axis position boxes corresponding to A2 and Z2 for the right gripper.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Axis naming reference showing A2 and Z2 used for the right tipper.*


**Stop or Escalate If:**

* Escalate if A2 or Z2 cannot be read from the HMI.
* Escalate if the right-axis labels do not match the documented A2/Z2 naming.

---

### Step 4 — Check axis reference indicators

**Responsible role:** L1_support

**Instruction:**
Check the "R" indicator for each axis and verify whether the circle is green to confirm the axis has been referenced.

**Expected result:**
Each axis can be classified as referenced or not referenced based on the "R" indicator.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Reference-state indicator area associated with each axis on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* Escalate if an axis is not referenced and a fault is present or suspected.
* Escalate if the reference indicator behavior does not match the documented green-circle meaning.

---

### Step 5 — Check whether any axis is in motion

**Responsible role:** L1_support

**Instruction:**
Check whether any data field is yellow to determine whether that axis is in motion.

**Expected result:**
Any axis currently in motion is identified by a yellow data field.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Axis data fields to determine whether any field is yellow, indicating motion.*


**Stop or Escalate If:**

* Escalate if field color behavior does not match the documented yellow-means-motion indicator.
* Escalate if axis motion status cannot be determined from the HMI.

---

### Step 6 — Record out-of-reference axes and note fault relevance

**Responsible role:** L1_support

**Instruction:**
Record any axis that is not referenced, since the source states an axis being out of reference may cause a tipper fault.

**Expected result:**
Any out-of-reference axis is documented for follow-up or escalation.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Axis reference indicators and position fields for any axis identified as out of reference.*


**Stop or Escalate If:**

* Escalate if an out-of-reference axis is associated with a fault.
* Escalate if the displayed axis state does not match documented indicators.

---

## Success Criteria

* The user identifies the current A1, Z1, A2, and Z2 position values from the Visu_MCP_Dual screen.
* The user determines whether each axis is referenced using the green "R" indicator.
* The user determines whether any axis is in motion using the yellow data field indication.
* Any out-of-reference axis is documented for follow-up.

## Failure Conditions

* The Visu_MCP_Dual screen or axis fields cannot be located or interpreted.
* An axis reference indicator does not match the documented meaning.
* An axis is out of reference.
* Displayed axis state does not match documented indicators.
* An out-of-reference axis is associated with a tipper fault.

## Escalation Guidance

* Escalate if the displayed axis state does not match documented indicators or if an out-of-reference axis is associated with a fault.
* Escalate if the Visu_MCP_Dual screen cannot be accessed or the axis fields cannot be identified.
* This runbook does not include source-supported corrective actions; escalate rather than improvise unsupported recovery steps.

## Missing Details / Known Gaps

* The packet does not provide a source-backed time estimate for completing this check.
* The packet does not provide source-backed production stop or LOTO requirements.
* The packet does not provide a source-backed corrective procedure for restoring reference state or clearing related faults from this diagnostic check.
* The source section text body is empty in the packet; evidence is derived from supplied source refs and related artifacts only.

## Source Lineage

- Candidate IDs: candidate_l1_diagnose_axis_reference_and_motion_status_on_visu_mcp_dual
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
