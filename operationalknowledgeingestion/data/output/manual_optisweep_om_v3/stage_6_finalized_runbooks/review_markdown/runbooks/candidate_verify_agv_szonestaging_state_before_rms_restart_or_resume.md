# Verify AGVs Are in the "szonestaging" State on the HMI

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_agvs_are_in_the_szonestaging_state_on_the_hmi_v1` |
| Title | Verify AGVs Are in the "szonestaging" State on the HMI |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Confirm on the HMI that the AGVs being checked are displayed in the documented "szonestaging" state before restart or resume actions in AGV fault recovery.

## When To Use

Use this check when AGV fault recovery or restart guidance requires confirmation that AGVs are in the documented ready state before restarting or resuming the system.

## Do Not Use For

* Do not use this procedure to infer readiness from AGV states other than "szonestaging".
* Do not use this procedure if the HMI does not display AGV state; escalate instead of guessing the state.

## Safety And Operational Notes

* Stop and escalate if the HMI does not show AGV state or if the AGVs are not shown as "szonestaging" when this verification is required.
* Do not infer equivalent AGV states that are not explicitly documented in the source.

## Access Or Tools Needed

* Access to the HMI showing AGV state

## Related Operational Context

* ctx_manual_agv_szonestaging_status_v1

## Procedure Steps

### Step 1 — Open the HMI view showing AGV state

**Responsible role:** L1_support

**Instruction:**
Open or view the HMI area where AGV state is displayed for the AGVs being checked.

**Expected result:**
The HMI view showing AGV state is visible.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Use the nearby page 90 AGV recovery screen as contextual visual support for the HMI-based AGV status verification; review the AGV status area referenced by the source.*


**Stop or Escalate If:**

* The HMI does not show AGV state.
* The relevant AGVs cannot be identified on the HMI.

---

### Step 2 — Identify the AGV state value

**Responsible role:** L1_support

**Instruction:**
Identify the AGV state value shown on the HMI for the AGVs being checked.

**Expected result:**
A visible AGV state value is identified for each AGV being checked.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Look for the AGV status/state information referenced by the page 90 recovery guidance.*


**Stop or Escalate If:**

* The AGV state value is not displayed.
* The AGV state value cannot be read clearly.

---

### Step 3 — Verify the state is "szonestaging"

**Responsible role:** L1_support

**Instruction:**
Verify that the displayed AGV state is exactly "szonestaging" for the AGVs being checked.

**Expected result:**
The AGVs are confirmed either to be in "szonestaging" or not in the required state.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Confirm the AGV status/state matches the documented value "szonestaging" referenced by the source.*


**Stop or Escalate If:**

* The displayed AGV state is not "szonestaging".
* The state appears similar but is not explicitly documented as "szonestaging".

---

### Step 4 — Confirm readiness before restart or resume

**Responsible role:** L1_support

**Instruction:**
Record or confirm that the AGVs are in the documented ready state before proceeding with restart or resume actions.

**Expected result:**
A clear confirmation is made that the AGVs are in the documented ready state, or escalation is initiated if they are not.

**Stop or Escalate If:**

* The AGVs cannot be confirmed in "szonestaging".
* Restart or resume would require proceeding without the documented state verification.

---

## Success Criteria

* The HMI displays AGV state for the AGVs being checked.
* The displayed AGV state is confirmed as exactly "szonestaging".
* The AGVs are confirmed in the documented ready state before restart or resume actions.

## Failure Conditions

* The HMI does not show AGV state.
* The AGV state cannot be identified or read.
* The AGV state is not "szonestaging" when this verification is required.
* Proceeding would require inferring an undocumented equivalent state.

## Escalation Guidance

* Stop and escalate if the HMI does not show AGV state.
* Stop and escalate if the AGVs are not shown as "szonestaging" when this verification is required.
* Do not infer equivalent AGV states that are not explicitly documented in the source.

## Missing Details / Known Gaps

* The source packet does not identify the exact HMI screen name or navigation path used to view AGV state for this check.
* The source packet does not provide a required recording method, log location, or confirmation field for documenting the result.
* The supplied figure support is noted as indirect and should be reviewed for exact screen applicability.
* The source does not specify whether all AGVs or only affected AGVs must be checked in this sub-procedure.
* The source does not provide a time estimate for completing this verification.

## Source Lineage

- Candidate IDs: candidate_verify_agv_szonestaging_state_before_rms_restart_or_resume
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
