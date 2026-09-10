# Stop Automatic Tipping Cycle on Operator Station HMI Before Manual Axes Referencing (Visu_Dual_MCP / CYCLE STOP)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_stop_automatic_tipping_cycle_visu_dual_mcp_cycle_stop_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the operator station HMI, navigate to the "Visu_Dual_MCP" screen (F3) and press CYCLE STOP to stop the automatic tipping cycle so the end effector can be moved into position for maintenance procedures.

## When To Use

Use when you need to stop the automatic tipping cycle on the operator station HMI before manually referencing/moving the end effector into position for maintenance procedures.

## Source Procedure References

- proc_stop_automatic_tipping_cycle_visu_dual_mcp_cycle_stop_v1

## Procedure Steps

### Step 1 — Navigate to the "Visu_Dual_MCP" screen (F3) on the operator station HMI

**Responsible role:** operator

**Instruction:**
On the operator station HMI, navigate to the "Visu_Dual_MCP" screen using the F3 key.

**Expected result:**
The operator station HMI is displaying the "Visu_Dual_MCP" screen.

---

### Step 2 — Press CYCLE STOP to stop the automatic tipping cycle

**Responsible role:** operator

**Instruction:**
On the "Visu_Dual_MCP" screen, press CYCLE STOP.

**Expected result:**
The automatic tipping cycle is stopped after pressing CYCLE STOP.

---

## Success Criteria

- Automatic tipping cycle is stopped after pressing CYCLE STOP on the "Visu_Dual_MCP" screen.

## Failure Conditions

- Cannot navigate to the "Visu_Dual_MCP" screen (F3).
- Automatic tipping cycle does not stop after pressing CYCLE STOP.

## Escalation Guidance

- If the automatic tipping cycle does not stop after pressing CYCLE STOP, stop and escalate for support.

## Missing Details / Known Gaps

- The manual excerpt provided does not specify the exact on-screen indication that confirms the automatic tipping cycle has stopped (e.g., a specific status label/value).
