# Set tipper to AUTO mode so it waits for WCS instructions

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_set_tipper_auto_mode_wait_for_wcs_v1` |
| Title | Set tipper to AUTO mode so it waits for WCS instructions |
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

Place the tipper in AUTO mode so it waits for the WCS to send instructions.

## When To Use

Use when starting/operating the tipper and you need the tipper to wait for WCS instructions by placing it into AUTO mode.

## Access Or Tools Needed

* Operator station HMI/control panel (tipper mode selection/status)

## Related Operational Context

* ctx_manual_tipper_auto_mode_v1

## Visual References

![artifact_fig_4_19_operator_station_control_panel](assets/02aaee46093b117e.png)

*Operator Station Control Panel (Visu_MCP_Dual screen) showing the AUTO button and CYCLE START/CYCLE STOP controls.*

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Operator station main screen showing the CYCLE STOP button (used on the operator station main screen).*

## Procedure Steps

### Step 1 — Locate the tipper mode control on the operator station HMI

**Responsible role:** operator

**Instruction:**
On the operator station control panel (Visu_MCP_Dual / operator station main screen), locate the tipper mode control, including the AUTO button.

**Expected result:**
The AUTO control/button is visible and ready to be selected on the operator station HMI/control panel.

---

### Step 2 — Place the tipper in AUTO mode

**Responsible role:** operator

**Instruction:**
Select AUTO on the operator station HMI/control panel to place the tipper in AUTO mode.

**Expected result:**
The tipper is in AUTO mode.

**Stop or Escalate If:**

* If the tipper does not reflect AUTO mode after selection, stop and escalate.

---

### Step 3 — Confirm the tipper is waiting for WCS instructions

**Responsible role:** operator

**Instruction:**
Verify on the operator station HMI/control panel that the tipper is in AUTO mode and is waiting for WCS instructions.

**Expected result:**
Tipper is in AUTO mode and waits for the WCS to send instructions.

**Stop or Escalate If:**

* If the tipper does not reflect AUTO mode after selection, stop and escalate.

---

## Success Criteria

* Tipper reflects AUTO mode on the operator station HMI/control panel.
* Tipper is in a state where it waits for WCS instructions.

## Failure Conditions

* Tipper does not reflect AUTO mode after selection.
* Tipper is not waiting for WCS instructions.

## Escalation Guidance

* Stop and escalate if the tipper does not reflect AUTO mode after selection.

## Missing Details / Known Gaps

* The packet does not provide the exact HMI indicator text/field name that explicitly shows the tipper is 'waiting for the WCS to send instructions' (only the manual statement that this is what AUTO mode does).

## Source Lineage

- Candidate IDs: candidate_manual_operator_station_set_tipper_auto_mode_wait_for_wcs
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
