# Reset the Tipper After an E-Stop From the Visu_MCP_Dual Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_tipper_after_estop_from_visu_mcp_dual_screen_v1` |
| Title | Reset the Tipper After an E-Stop From the Visu_MCP_Dual Screen |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented HMI recovery sequence on the Tipper Machine Control Panel (Visu_MCP_Dual) after an emergency stop: press ESTOP RESET, then AUTO, then CYCLE START to restart the system.

## When To Use

Use this procedure when the tipper system has experienced an emergency stop and the operator is restoring operation from the Visu_MCP_Dual operator station HMI using the documented ESTOP RESET sequence.

## Do Not Use For

* Do not use this procedure for non-E-stop faults that require RESET or AUTO REF functions.
* Do not use this procedure when additional recovery beyond ESTOP RESET, AUTO, and CYCLE START is required, because the source does not provide further detail in this section.

## Safety And Operational Notes

* The source states that ESTOP RESET resets the system after an E-stop.
* Use only the documented HMI sequence provided by the source: ESTOP RESET, then AUTO, then CYCLE START.
* No additional E-stop safety checks or field reset actions are provided in the source section.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_MCP_Dual screen
* ESTOP RESET button
* AUTO button
* CYCLE START button

## Related Operational Context

* ctx_manual_tipper_reset_and_reference_functions_v1
* ctx_manual_tipper_control_modes_and_cycle_controls_v1
* ctx_manual_visu_mcp_dual_screen_overview_v1

## Procedure Steps

### Step 1 — Open the Visu_MCP_Dual screen and identify the reset and restart controls

**Responsible role:** operator

**Instruction:**
Open the Tipper Machine Control Panel ("Visu_MCP_Dual") screen and identify the ESTOP RESET, AUTO, and CYCLE START buttons on the operator station HMI.

**Expected result:**
The operator is on the primary tipper control screen and has identified the controls needed for the recovery sequence.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Main control buttons on the Operator Station Control Panel for the Visu_MCP_Dual screen, including AUTO and cycle controls; use this figure to orient to the primary HMI layout.*


**Stop or Escalate If:**

* The Visu_MCP_Dual screen is not available at the operator station.
* The required controls cannot be identified on the HMI.

---

### Step 2 — Press ESTOP RESET

**Responsible role:** operator

**Instruction:**
Press ESTOP RESET to reset the system after an E-stop.

**Expected result:**
The system is reset from the E-stop condition.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Use the operator station control panel figure to locate the reset-related controls on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* The system does not reset after pressing ESTOP RESET.

---

### Step 3 — Press AUTO

**Responsible role:** operator

**Instruction:**
Press AUTO.

**Expected result:**
The tipper is placed in automatic mode.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the AUTO button on the primary operator station control panel.*

![artifact_page_86_image_15](assets/artifact_page_86_image_15.png)

*Related operator station controls showing AUTO used to return to automatic operation.*


**Stop or Escalate If:**

* AUTO cannot be selected.
* The system does not enter automatic mode.

---

### Step 4 — Press CYCLE START

**Responsible role:** operator

**Instruction:**
Press CYCLE START to restart the system.

**Expected result:**
The system restarts from the operator station HMI.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the CYCLE START control on the primary operator station control panel.*

![artifact_page_86_image_15](assets/artifact_page_86_image_15.png)

*Related operator station controls showing CYCLE START used to return operation.*


**Stop or Escalate If:**

* The system does not restart after pressing CYCLE START.

---

## Success Criteria

* The system is reset after the E-stop.
* The tipper is placed in Auto mode.
* The system restarts from the operator station HMI after CYCLE START.

## Failure Conditions

* The Visu_MCP_Dual screen cannot be accessed or the required controls cannot be identified.
* The system does not reset after ESTOP RESET.
* The system does not enter Auto mode after pressing AUTO.
* The system does not restart after pressing CYCLE START.

## Escalation Guidance

* If the system does not restart after ESTOP RESET, AUTO, and CYCLE START, escalate because the source section does not provide additional recovery detail.
* If the operator cannot access the Visu_MCP_Dual screen or identify the required controls, stop and seek additional support.

## Missing Details / Known Gaps

* The source does not provide additional troubleshooting or alternate recovery steps if the system does not restart after ESTOP RESET, AUTO, and CYCLE START.
* The source does not provide an estimated completion time.
* The source does not specify whether production must be stopped before performing this procedure.
* The source does not specify LOTO requirements for this HMI recovery sequence.
* The source section does not provide explicit confirmation indicators for successful ESTOP RESET beyond restart behavior.

## Source Lineage

- Candidate IDs: candidate_operator_reset_tipper_after_estop_from_visu_mcp_dual
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
