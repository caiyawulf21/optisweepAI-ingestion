# Perform Operator Station Lockout/Tagout Using Visu_Dual_MCP and Electrical Panel Power Switch

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_perform_operator_station_loto_visu_dual_mcp_electrical_panel_power_switch_v1` |
| Title | Perform Operator Station Lockout/Tagout Using Visu_Dual_MCP and Electrical Panel Power Switch |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `e_stop_or_safety_stop` |
| Access Surface | `tipper_hmi`, `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely stop the operator station for lockout/tagout by using the operator station HMI to navigate to the Visu_Dual_MCP screen, press CYCLE STOP, optionally jog the tipper carriages using the JOG controls (+/–) for the correct tipper axis, then turn OFF the operator station electrical panel power switch and apply LOTO.

## When To Use

Use when you need to place the operator station into a stopped state and then perform lockout/tagout at the operator station electrical panel.

## Safety And Operational Notes

* Risk of personal injury: Do not touch the tippers while the system is powered ON.
* Risk of personal injury: Be aware of the movement trajectory of the product and do not interfere with the line.
* Risk of personal injury: Ensure no one approaches or extends a hand into the lift connecting rod assembly before starting the robot when powered on.

## Access Or Tools Needed

* Operator station HMI access
* Operator station electrical panel access (power switch and LOTO capability)

## Related Operational Context

* ctx_manual_operator_station_loto_v1
* ctx_manual_visu_dual_mcp_screen_v1
* ctx_manual_lift_connecting_rod_safety_v1

## Visual References

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Operator station main screen showing the CYCLE STOP button (Stopping the Operator Station).*

![artifact_page_83_image_10](assets/acd8e7472a45f789.png)

*Visu_Dual_MCP jogging screen showing Z1/Z2/A1/A2 axis controls and +/– buttons (Jogging the Tipper).*

![artifact_page_103_image_2](assets/8caf84ff57cdad0a.jpeg)

*Visu_Dual_MCP screen reference used for manually referencing axes; includes instruction to press CYCLE STOP before jogging.*

![artifact_page_103_image_3](assets/8ec7e8899bc0ced7.png)

*Visu_Dual_MCP screen reference for manually referencing axes; includes instruction to press CYCLE STOP to stop the automatic tipping cycle.*

![artifact_fig_4_19_operator_station_control_panel](assets/02aaee46093b117e.png)

*Tipper Machine Control Panel (Visu_MCP_Dual) showing JOG and CYCLE STOP controls and note about active buttons.*

## Procedure Steps

### Step 1 — Navigate to the Visu_Dual_MCP screen on the operator station HMI

**Responsible role:** operator

**Instruction:**
At the operator station HMI, navigate to the "Visu_Dual_MCP" screen.

**Expected result:**
The "Visu_Dual_MCP" screen is displayed on the operator station HMI.

**Stop or Escalate If:**

* Stop and escalate if you cannot reach the "Visu_Dual_MCP" screen.

---

### Step 2 — Press CYCLE STOP to stop the operator station

**Responsible role:** operator

**Instruction:**
On the "Visu_Dual_MCP" screen, press "CYCLE STOP".

**Expected result:**
The operator station is in a stopped state after pressing CYCLE STOP.

**Stop or Escalate If:**

* Stop and escalate if you cannot press "CYCLE STOP".

---

### Step 3 — Optionally jog the carriages using JOG (+/–) for the correct tipper axis

**Responsible role:** operator

**Instruction:**
If you need to move the carriages to a different position: press "JOG", select the corresponding axis for the tipper, then use the "+" and "-" buttons to move the carriages.

**Expected result:**
The carriages move to the desired position using the selected tipper axis controls after pressing JOG.

---

### Step 4 — Turn OFF the operator station electrical panel power switch and apply LOTO

**Responsible role:** operator

**Instruction:**
At the operator station electrical panel, turn the power switch to "OFF" and apply LOTO.

**Expected result:**
The operator station electrical panel power switch is set to "OFF" and LOTO is applied.

**Stop or Escalate If:**

* Stop and escalate if the electrical panel power switch cannot be set to "OFF" or LOTO cannot be applied.

---

## Success Criteria

* Operator station is stopped after pressing CYCLE STOP.
* Operator station electrical panel power switch is set to "OFF" and LOTO is applied.

## Failure Conditions

* Cannot reach the "Visu_Dual_MCP" screen.
* Cannot press "CYCLE STOP".
* Cannot set the operator station electrical panel power switch to "OFF".
* LOTO cannot be applied.

## Escalation Guidance

* If you cannot reach the "Visu_Dual_MCP" screen or cannot press "CYCLE STOP", stop and escalate.
* If you cannot set the electrical panel power switch to "OFF" or cannot apply LOTO, stop and escalate.

## Missing Details / Known Gaps

* No explicit electrical panel power switch label text or LOTO point/lock location is provided in the packet evidence; only the instruction to turn the power switch to "OFF" and apply LOTO is supported.

## Source Lineage

- Candidate IDs: candidate_manual_operator_station_loto_visu_dual_mcp
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
