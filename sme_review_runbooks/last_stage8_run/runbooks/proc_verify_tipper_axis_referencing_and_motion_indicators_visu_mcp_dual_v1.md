# Verify Tipper Axis Referencing and Motion Indicators on Visu_MCP_Dual (A1/Z1/A2/Z2)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_tipper_axis_referencing_and_motion_indicators_visu_mcp_dual_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the tipper operator HMI screen Visu_MCP_Dual, verify that the left (A1/Z1) and right (A2/Z2) gripper axes show the correct referencing indicator (green 'R' circle) and determine whether an axis is currently moving (yellow data field). An axis that is out of reference may contribute to a tipper fault.

## When To Use

Use when investigating a tipper fault and you need to confirm whether the left/right tipper axes are referenced and whether an axis is currently moving based on the Visu_MCP_Dual indicators.

## Source Procedure References

- proc_verify_tipper_axis_referencing_and_motion_indicators_visu_mcp_dual_v1

## Safety And Operational Notes

- The Visu_MCP_Dual screen includes movement controls; the manual jog function is intended for maintenance personnel (do not jog unless you are authorized/qualified per site practice).

## Procedure Steps

### Step 1 — Open the primary tipper operator screen Visu_MCP_Dual

**Responsible role:** operator

**Instruction:**
On the operator station HMI, navigate to the primary screen labeled "Visu_MCP_Dual" (Tipper Machine Control Panel).

**Expected result:**
The Visu_MCP_Dual screen is visible with the axis position boxes labeled A1, Z1, A2, Z2 and the cycle referencing indicator labeled with the green 'R' circle rule.

---

### Step 2 — Read left gripper axis positions (A1 and Z1) in steps

**Responsible role:** operator

**Instruction:**
On Visu_MCP_Dual, read the numeric position values (in steps) shown in the "A1" and "Z1" boxes for the left gripper.

**Expected result:**
The "A1" and "Z1" boxes show current position values (in steps) for the left gripper.

---

### Step 3 — Read right gripper axis positions (A2 and Z2) in steps

**Responsible role:** operator

**Instruction:**
On Visu_MCP_Dual, read the numeric position values (in steps) shown in the "A2" and "Z2" boxes for the right gripper.

**Expected result:**
The "A2" and "Z2" boxes show current position values (in steps) for the right gripper.

---

### Step 4 — Check the cycle referencing indicator ('R' circle) for referenced status

**Responsible role:** operator

**Instruction:**
On Visu_MCP_Dual, check the cycle referencing indicator labeled with the green 'R' circle rule.

**Expected result:**
The cycle referencing indicator shows green 'R' when the axis has been referenced.

---

### Step 5 — Observe whether the axis data field is yellow (axis in motion)

**Responsible role:** operator

**Instruction:**
On Visu_MCP_Dual, observe the axis data field color; confirm whether it is yellow (indicating the axis is in motion).

**Expected result:**
The data field is yellow when the axis is in motion.

---

### Step 6 — Interpret out-of-reference condition as a potential contributor to tipper fault

**Responsible role:** operator

**Instruction:**
If the axis is out of reference (i.e., the green 'R' circle rule is not satisfied), note that an out-of-reference axis may cause a tipper fault.

**Expected result:**
You have identified whether the axis is out of reference based on the cycle 'R' indicator rule, and you can state that this condition may contribute to a tipper fault.

---

## Success Criteria

- A1/Z1 and A2/Z2 position values (in steps) are visible and readable on Visu_MCP_Dual.
- The cycle referencing indicator follows the rule: green 'R' indicates the axis has been referenced.
- The axis data field shows yellow when the axis is in motion.

## Failure Conditions

- Referencing indicator does not show referenced (green 'R' rule not satisfied) while the system is faulting.
- Screen behavior does not match expected referenced/motion indicators.

## Escalation Guidance

- If the axis is out of reference (green 'R' rule not satisfied) while the system is faulting, stop and escalate for further troubleshooting.

## Missing Details / Known Gaps

- The packet does not provide explicit per-axis mapping of the yellow motion indicator to A1 vs Z1 vs A2 vs Z2; it only states that the data field will be yellow when the axis is in motion.
- The packet does not provide explicit UI labels for the exact location/label of the yellow data field beyond the general rule; operators should rely on the visible color change on Visu_MCP_Dual.
