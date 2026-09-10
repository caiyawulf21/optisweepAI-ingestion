# Stop Automatic Tipping Cycle on Operator Station HMI Before Manual Axes Referencing (Visu_Dual_MCP / CYCLE STOP)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_stop_automatic_tipping_cycle_visu_dual_mcp_cycle_stop_v1` |
| Title | Stop Automatic Tipping Cycle on Operator Station HMI Before Manual Axes Referencing (Visu_Dual_MCP / CYCLE STOP) |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

On the operator station HMI, navigate to the "Visu_Dual_MCP" screen (F3) and press CYCLE STOP to stop the automatic tipping cycle so the end effector can be moved into position for maintenance procedures.

## When To Use

Use when you need to stop the automatic tipping cycle on the operator station HMI before manually referencing/moving the end effector into position for maintenance procedures.

## Access Or Tools Needed

* Tipper HMI / WebVisu / VISU (operator station HMI)

## Related Operational Context

* ctx_manual_manual_axes_referencing_v1

## Visual References

![artifact_page_103_image_3](assets/8ec7e8899bc0ced7.png)

*Operator station HMI screen for manually referencing tipper axes during maintenance; includes navigation to "Visu_Dual_MCP" (F3) and the CYCLE STOP step.*

![artifact_fig_4_19_operator_station_control_panel](assets/02aaee46093b117e.png)

*Operator Station Control Panel (Visu_MCP_Dual screen) showing the CYCLE STOP button and other operator controls.*

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

**Stop or Escalate If:**

* If the automatic tipping cycle does not stop after pressing CYCLE STOP, stop and escalate for support.

---

## Success Criteria

* Automatic tipping cycle is stopped after pressing CYCLE STOP on the "Visu_Dual_MCP" screen.

## Failure Conditions

* Cannot navigate to the "Visu_Dual_MCP" screen (F3).
* Automatic tipping cycle does not stop after pressing CYCLE STOP.

## Escalation Guidance

* If the automatic tipping cycle does not stop after pressing CYCLE STOP, stop and escalate for support.

## Missing Details / Known Gaps

* The manual excerpt provided does not specify the exact on-screen indication that confirms the automatic tipping cycle has stopped (e.g., a specific status label/value).

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_axes_referencing_manual_stop_cycle
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
