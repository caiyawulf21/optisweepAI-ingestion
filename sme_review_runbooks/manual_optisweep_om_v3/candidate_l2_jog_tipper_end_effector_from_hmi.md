# Manually Jog The Tipper End Effector From The Operator Station HMI

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_manually_jog_the_tipper_end_effector_from_the_operator_station_hmi_v1` |
| Title | Manually Jog The Tipper End Effector From The Operator Station HMI |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station HMI jogging controls to manually move the left or right tipper end effector into position for maintenance procedures by stopping the automatic tipping cycle, opening the jogging screen, selecting the required axis, and using the plus or minus controls to move it in the documented direction.

## When To Use

Use this procedure when the tipper end effector must be manually moved into position from the operator station HMI during maintenance procedures.

## Safety And Operational Notes

* This procedure is used for maintenance procedures and involves manual axis movement from the HMI.
* Press CYCLE STOP to stop the automatic tipping cycle before opening the jogging screen.
* If you push an axis until it hits a hard stop, the axis will register a fault.

## Access Or Tools Needed

* Operator station HMI
* Access to the Visu_Dual_MCP screen
* HMI controls for CYCLE STOP and JOG
* Manual Mode jogging controls

## Related Operational Context

* ctx_manual_tipper_commissioning_overview_v1
* ctx_manual_visu_dual_mcp_jog_screen_v1
* ctx_manual_tipper_jog_direction_reference_v1
* ctx_manual_cycle_stop_control_reference_v1
* ctx_manual_tipper_hard_stop_fault_v1

## Procedure Steps

### Step 1 — Open the Visu_Dual_MCP screen

**Responsible role:** L2_support

**Instruction:**
On the operator station HMI, navigate to the "Visu_Dual_MCP" screen using F3.

**Expected result:**
The Visu_Dual_MCP screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Operator station HMI jogging screen context associated with the Visu_Dual_MCP access path.*

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI reference tied to navigating to the "Visu_Dual_MCP" screen using F3.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Operator station HMI reference associated with manual end effector positioning during maintenance.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Operator station control panel context showing the main HMI layout and control locations.*


**Stop or Escalate If:**

* The Visu_Dual_MCP screen cannot be opened from the operator station HMI.
* The expected operator station HMI controls are not visible after navigation.

---

### Step 2 — Stop the automatic tipping cycle

**Responsible role:** L2_support

**Instruction:**
Press CYCLE STOP to stop the automatic tipping cycle.

**Expected result:**
The automatic tipping cycle is stopped.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*CYCLE STOP control on the operator station control panel reference.*

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Operator station HMI jogging context associated with the documented CYCLE STOP then JOG sequence.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Related operator station context referencing use of CYCLE STOP on the main screen.*

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Related operator station HMI view associated with CYCLE STOP usage in maintenance/recovery context.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Related operator station HMI snippet associated with stopping the tipping cycle before manual actions.*


**Stop or Escalate If:**

* CYCLE STOP does not stop the automatic tipping cycle.
* The station remains in automatic motion or does not present the expected stopped state.

---

### Step 3 — Open the jogging screen

**Responsible role:** L2_support

**Instruction:**
Press JOG to open the jogging screen.

**Expected result:**
The jogging screen opens and Manual Mode jogging controls are available.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*JOG control on the operator station control panel reference.*

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Jogging screen used to manually move the tipper end effector.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Related manual jog mode interface reference showing jog mode context.*


**Stop or Escalate If:**

* The JOG control does not open the jogging screen.
* Manual Mode jogging controls are not visible after pressing JOG.

---

### Step 4 — Identify Manual Mode axis and jog controls

**Responsible role:** L2_support

**Instruction:**
On the jogging screen, identify the Manual Mode jogging controls for Z1 AXIS, Z2 AXIS, A1 AXIS, A2 AXIS, and the + and – buttons.

**Expected result:**
The operator can locate the axis selection buttons and the plus/minus movement controls.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Manual Mode jogging screen showing Z1 AXIS, Z2 AXIS, A1 AXIS, A2 AXIS, and plus/minus controls.*

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Related operator station HMI view showing Manual Mode axis controls.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Related operator station HMI snippet showing axis controls and Manual Mode elements.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Related manual jog mode reference showing axis names and jog controls.*


**Stop or Escalate If:**

* The Manual Mode controls are missing or unclear.
* The operator cannot positively identify the intended axis selection and movement controls.

---

### Step 5 — Select the axis for the required tipper movement

**Responsible role:** L2_support

**Instruction:**
Select the axis to move: use Z1 AXIS for left tipper vertical movement, A1 AXIS for left tipper gripper rotation, Z2 AXIS for right tipper vertical movement, or A2 AXIS for right tipper movement.

**Expected result:**
The correct axis is selected for the intended manual movement.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Axis selection controls for Z1, A1, Z2, and A2 on the jogging screen.*

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Related Manual Mode axis labels for Z1, Z2, A1, and A2.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Related axis control labels visible on the operator station HMI.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Related manual jog mode reference showing left/right axis naming.*


**Stop or Escalate If:**

* There is uncertainty about which axis corresponds to the intended tipper movement.
* The required axis cannot be selected from the jogging screen.

---

### Step 6 — Jog the selected axis with the plus or minus control

**Responsible role:** L2_support

**Instruction:**
Use the + or – button to move the selected axis.

**Expected result:**
The selected axis moves from the HMI jogging control input.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Plus and minus jog controls used to move the selected axis.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Related manual jog mode interface showing jog controls and axis context.*


**Stop or Escalate If:**

* The selected axis does not move when jog input is applied.
* The axis moves unexpectedly.
* The axis is pushed until it hits a hard stop.
* An axis fault registers during jogging.

---

### Step 7 — Verify Z-axis jog direction

**Responsible role:** L2_support

**Instruction:**
For Z-axis movement, verify that + moves the axis up and – moves the axis down.

**Expected result:**
Z-axis movement direction matches the documented behavior.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Z-axis selection and plus/minus controls on the jogging screen.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Related manual jog mode reference for axis direction context.*


**Stop or Escalate If:**

* Z-axis movement direction does not match the documented + up / – down behavior.
* Axis response is inconsistent with the selected jog input.

---

### Step 8 — Verify A-axis jog direction

**Responsible role:** L2_support

**Instruction:**
For A-axis movement, verify that + rotates the axis towards the operator and – rotates the axis away from the operator.

**Expected result:**
A-axis rotation direction matches the documented behavior.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*A-axis selection and plus/minus controls on the jogging screen.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Related manual jog mode reference for rotational direction context.*


**Stop or Escalate If:**

* A-axis rotation direction does not match the documented + toward operator / – away from operator behavior.
* Axis response is inconsistent with the selected jog input.

---

## Success Criteria

* The operator station HMI jogging screen is opened from Visu_Dual_MCP.
* The automatic tipping cycle is stopped before jogging.
* The correct left or right tipper axis is selected.
* The selected axis moves using the plus or minus controls.
* Z-axis movement follows the documented direction: + up, – down.
* A-axis movement follows the documented direction: + towards the operator, – away from the operator.
* The end effector is manually positioned as intended.

## Failure Conditions

* The Visu_Dual_MCP screen cannot be accessed.
* CYCLE STOP does not stop the automatic tipping cycle.
* JOG does not open the jogging screen.
* Manual Mode axis controls cannot be identified.
* The wrong axis is selected for the intended movement.
* The selected axis does not move or moves unexpectedly.
* Z-axis or A-axis movement direction does not match the documented behavior.
* An axis is pushed into a hard stop and registers a fault.

## Escalation Guidance

* Stop and escalate if the required HMI screen or controls are unavailable.
* Stop and escalate if the automatic tipping cycle cannot be stopped with CYCLE STOP.
* Stop and escalate if the selected axis does not respond correctly to jog input.
* Stop and escalate if motion direction does not match the documented behavior.
* Stop and escalate if an axis hits a hard stop or registers a fault.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not state whether production stop is formally required beyond stopping the automatic tipping cycle.
* The source does not state whether lockout/tagout is required.
* The source does not provide explicit completion confirmation beyond manual positioning and documented movement direction.
* The source does not provide explicit recovery steps if an axis fault occurs after hitting a hard stop within this section.

## Source Lineage

- Candidate IDs: candidate_l2_jog_tipper_end_effector_from_hmi
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
