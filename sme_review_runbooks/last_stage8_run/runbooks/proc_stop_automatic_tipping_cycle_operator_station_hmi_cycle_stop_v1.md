# Stop the Automatic Tipping Cycle From Operator Station HMI (Visu_Dual_MCP → CYCLE STOP)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_stop_automatic_tipping_cycle_operator_station_hmi_cycle_stop_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

From the operator station HMI, navigate to the "Visu_Dual_MCP" screen (F3) and press CYCLE STOP to stop the automatic tipping cycle so maintenance procedures and/or manual end-effector positioning can be performed.

## When To Use

Use when you need to halt the automatic tipping cycle from the operator station HMI to proceed with maintenance procedures and/or manual end-effector positioning.

## Source Procedure References

- proc_stop_automatic_tipping_cycle_operator_station_hmi_cycle_stop_v1

## Procedure Steps

### Step 1 — Navigate to the "Visu_Dual_MCP" screen (F3) on the operator station HMI

**Responsible role:** operator

**Instruction:**
On the operator station HMI, navigate to the "Visu_Dual_MCP" screen (F3).

**Expected result:**
The operator station HMI is displaying the "Visu_Dual_MCP" screen.

---

### Step 2 — Press CYCLE STOP to stop the automatic tipping cycle

**Responsible role:** operator

**Instruction:**
Press CYCLE STOP to stop the automatic tipping cycle.

**Expected result:**
The automatic tipping cycle is stopped after pressing CYCLE STOP.

---

## Success Criteria

- Automatic tipping cycle is stopped after pressing CYCLE STOP.

## Failure Conditions

- Automatic cycle does not stop after pressing CYCLE STOP.

## Escalation Guidance

- If the automatic cycle does not stop after pressing CYCLE STOP, stop attempting and escalate for support.
