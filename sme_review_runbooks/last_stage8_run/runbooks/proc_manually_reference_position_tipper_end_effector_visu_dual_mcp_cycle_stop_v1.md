# Manually Reference/Position Tipper End Effector for Maintenance Using Visu_Dual_MCP (Navigate + CYCLE STOP)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_manually_reference_position_tipper_end_effector_visu_dual_mcp_cycle_stop_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Navigate to the Visu_Dual_MCP screen on the operator station HMI and press CYCLE STOP to stop the automatic tipping cycle so the end effector can be manually positioned for maintenance procedures.

## When To Use

Use when maintenance requires manually moving the tipper end effector into position, and you need to stop the automatic tipping cycle first.

## Source Procedure References

- proc_manually_reference_position_tipper_end_effector_visu_dual_mcp_cycle_stop_v1

## Safety And Operational Notes

- Only maintenance personnel should jog the tipper (JOG is described as maintenance personnel use only in the operator station control panel figure).

## Procedure Steps

### Step 1 — Navigate to the Visu_Dual_MCP screen (F3) on the operator station HMI

**Responsible role:** operator

**Instruction:**
On the operator station HMI, navigate to the "Visu_Dual_MCP" screen (F3).

**Expected result:**
The operator station HMI is displaying the "Visu_Dual_MCP" screen (F3).

---

### Step 2 — Press CYCLE STOP to stop the automatic tipping cycle

**Responsible role:** operator

**Instruction:**
Press CYCLE STOP on the Visu_Dual_MCP screen to stop the automatic tipping cycle.

**Expected result:**
The automatic tipping cycle is stopped after pressing CYCLE STOP.

---

## Success Criteria

- Visu_Dual_MCP screen (F3) is displayed on the operator station HMI.
- Automatic tipping cycle is stopped after pressing CYCLE STOP.

## Failure Conditions

- Automatic tipping cycle continues running after pressing CYCLE STOP.

## Escalation Guidance

- If CYCLE STOP does not stop the automatic tipping cycle, stop and escalate for support rather than attempting manual movement.

## Missing Details / Known Gaps

- The provided excerpt and evidence for this candidate cover only navigating to "Visu_Dual_MCP" (F3) and pressing CYCLE STOP. The manual end-effector movement/jogging actions themselves are not included in the provided excerpt for this specific candidate.
