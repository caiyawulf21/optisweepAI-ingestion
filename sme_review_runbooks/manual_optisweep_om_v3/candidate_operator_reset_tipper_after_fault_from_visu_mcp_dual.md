# Reset the Tipper After a Fault From the Visu_MCP_Dual Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_tipper_after_fault_from_visu_mcp_dual_screen_v1` |
| Title | Reset the Tipper After a Fault From the Visu_MCP_Dual Screen |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station HMI Tipper Machine Control Panel (Visu_MCP_Dual) screen to review displayed alarm or informational messages, press RESET to reset the system after a fault, and press CYCLE START to restart the tipper operation cycle.

## When To Use

Use when a tipper fault has occurred and the operator is working from the primary operator station HMI screen (Visu_MCP_Dual) to reset the system and restart the tipper operation cycle.

## Do Not Use For

* Do not use for emergency stop reset; the source separately identifies ESTOP RESET as the control used after an E-stop.
* Do not assume AUTO REF is always required as part of this procedure; the source states AUTO REF is enabled after the cycle has been reset, but this candidate does not establish it as a mandatory step for this fault reset procedure.
* Do not use this runbook for maintenance-only manual control tasks on the Visu_ManControl screen.

## Safety And Operational Notes

* Use the primary operator station HMI screen intended for station operators.
* The source distinguishes fault reset from E-stop reset; use the appropriate control for the condition present.
* If the fault is not cleared after RESET, the supplied source section does not provide additional recovery steps.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_MCP_Dual screen
* RESET button
* CYCLE START button
* Informational banner

## Related Operational Context

* ctx_manual_tipper_reset_and_reference_functions_v1
* ctx_manual_visu_mcp_dual_screen_overview_v1

## Procedure Steps

### Step 1 — Open the Visu_MCP_Dual screen and identify reset controls

**Responsible role:** operator

**Instruction:**
Open the Tipper Machine Control Panel (Visu_MCP_Dual) screen on the operator station HMI and identify the RESET and CYCLE START buttons on the screen.

**Expected result:**
The Visu_MCP_Dual screen is displayed and the operator can locate the RESET and CYCLE START controls.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the RESET and CYCLE START controls on the operator station control panel screen.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Use the display controls mapping to access the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* Stop if the Visu_MCP_Dual screen cannot be accessed from the operator station HMI.
* Escalate if the required controls are not visible or cannot be identified on the screen.

---

### Step 2 — Review the informational banner messages

**Responsible role:** operator

**Instruction:**
Check the informational banner for alarms or informational messages. Use the arrows on the right side of the banner to review available messages.

**Expected result:**
The operator has reviewed the messages currently displayed in the informational banner.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Look at the informational banner and the arrows on the right side of the banner used to navigate messages.*


**Stop or Escalate If:**

* Escalate if the informational banner cannot be reviewed or message navigation is not functioning.

---

### Step 3 — Press RESET after the fault

**Responsible role:** operator

**Instruction:**
Press RESET to reset the system after a fault.

**Expected result:**
The system is reset after the fault.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate and press the RESET control on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* Escalate if the fault is not cleared after RESET.
* Do not continue with this runbook if the condition is an emergency stop requiring ESTOP RESET instead of RESET.

---

### Step 4 — Press CYCLE START to restart the tipper cycle

**Responsible role:** operator

**Instruction:**
Press CYCLE START to restart the tipper operation cycle.

**Expected result:**
The tipper operation cycle restarts from the HMI.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate and press the CYCLE START control on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* Escalate if the tipper operation cycle does not restart after CYCLE START.

---

## Success Criteria

* The system is reset after the fault.
* The tipper operation cycle can be restarted from the HMI using CYCLE START.

## Failure Conditions

* The Visu_MCP_Dual screen cannot be accessed.
* The informational banner cannot be reviewed.
* The fault is not cleared after RESET.
* The tipper operation cycle does not restart after CYCLE START.

## Escalation Guidance

* If the fault is not cleared after RESET, escalate because the supplied source section does not provide additional recovery steps.
* If the cycle does not restart after CYCLE START, escalate for further troubleshooting.
* If the condition is an emergency stop rather than a normal fault, use the documented ESTOP RESET path instead of this runbook.

## Missing Details / Known Gaps

* The source packet does not provide additional troubleshooting steps if RESET does not clear the fault.
* The source packet does not specify whether production must be stopped before performing this procedure.
* The source packet does not specify whether lockout/tagout is required for this procedure.
* The source packet does not provide an estimated completion time.
* The source packet does not define exact on-screen confirmation text indicating that the fault has cleared.

## Source Lineage

- Candidate IDs: candidate_operator_reset_tipper_after_fault_from_visu_mcp_dual
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
