# Stop the Automatic Tipping Cycle From Operator Station HMI (Visu_Dual_MCP → CYCLE STOP)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_stop_automatic_tipping_cycle_operator_station_hmi_cycle_stop_v1` |
| Title | Stop the Automatic Tipping Cycle From Operator Station HMI (Visu_Dual_MCP → CYCLE STOP) |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

From the operator station HMI, navigate to the "Visu_Dual_MCP" screen (F3) and press CYCLE STOP to stop the automatic tipping cycle so maintenance procedures and/or manual end-effector positioning can be performed.

## When To Use

Use when you need to halt the automatic tipping cycle from the operator station HMI to proceed with maintenance procedures and/or manual end-effector positioning.

## Access Or Tools Needed

* tipper_hmi (Operator station HMI / WebVisu / VISU)

## Visual References

![artifact_fig_4_19_operator_station_control_panel](assets/02aaee46093b117e.png)

*Operator Station Control Panel (Visu_MCP_Dual screen) showing the CYCLE STOP button and that active buttons are indicated by illuminated green bars.*

![artifact_page_103_image_3](assets/8ec7e8899bc0ced7.png)

*Operator station HMI screen for manually referencing axes; includes navigation to "Visu_Dual_MCP" (F3) and the instruction to press CYCLE STOP to stop the automatic tipping cycle.*

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

**Stop or Escalate If:**

* If the automatic cycle does not stop after pressing CYCLE STOP, stop attempting and escalate for support.

---

## Success Criteria

* Automatic tipping cycle is stopped after pressing CYCLE STOP.

## Failure Conditions

* Automatic cycle does not stop after pressing CYCLE STOP.

## Escalation Guidance

* If the automatic cycle does not stop after pressing CYCLE STOP, stop attempting and escalate for support.

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_stop_automatic_tipping_cycle
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
