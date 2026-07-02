# Resume All AGV Movement From The API Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resume_all_agv_movement_from_the_api_screen_v1` |
| Title | Resume All AGV Movement From The API Screen |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Resume movement for all AGVs using the Resume All AGVs control in the AGVs section of the System HMI API screen.

## When To Use

Use when AGV movement needs to be resumed from the AGVs section of the System HMI API screen and the Resume All AGVs control is available.

## Do Not Use For

* Do not use this runbook for AGV removal, AGV recovery, AGV command execution, or Geek+ command resend actions.
* Do not use this runbook when confirmation indicators or status feedback are required from the source, because the source does not provide them.

## Safety And Operational Notes

* This is a fleet-wide control that resumes movement for all AGVs.
* The source does not provide confirmation indicators or status feedback for the resume action.

## Access Or Tools Needed

* Access to the System HMI API screen
* AGVs section of the API screen

## Related Operational Context

* ctx_manual_tote_api_controls_overview_v1
* ctx_manual_optisweep_agv_reference_v1

## Procedure Steps

### Step 1 — Open the AGVs section of the API screen

**Responsible role:** L1_support

**Instruction:**
Open the System HMI API screen and go to the AGVs section.

**Expected result:**
The AGVs section of the API screen is visible.

**Screens / Images:**

![artifact_fig_4_8_acb_api_screen](assets/artifact_fig_4_8_acb_api_screen.jpeg)

*The API screen used to access AGV controls.*

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The AGVs section of the API screen where AGV API controls are shown.*


**Stop or Escalate If:**

* Stop or escalate if the System HMI API screen cannot be opened.
* Stop or escalate if the AGVs section is not available.

---

### Step 2 — Locate the Resume All AGVs control

**Responsible role:** L1_support

**Instruction:**
In the AGVs section of the API screen, locate the Resume All AGVs control.

**Expected result:**
The Resume All AGVs control is identified on the screen.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Resume All AGVs control within the AGV API Controls screen.*


**Stop or Escalate If:**

* Stop or escalate if the Resume All AGVs control is not present on the AGVs section.

---

### Step 3 — Use the Resume All AGVs control

**Responsible role:** L1_support

**Instruction:**
Use the Resume All AGVs control to resume all AGV movement.

**Expected result:**
All AGV movement resumes.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Resume All AGVs control used to resume fleet movement.*


**Stop or Escalate If:**

* Escalate if AGV movement does not resume after using the control.
* Escalate if no confirmation or status feedback is available and AGV movement remains unchanged.

---

## Success Criteria

* All AGV movement resumes.
* The Resume All AGVs control was accessed from the AGVs section of the API screen.

## Failure Conditions

* The API screen or AGVs section cannot be accessed.
* The Resume All AGVs control cannot be located.
* AGV movement does not resume after using the control.
* The source does not provide confirmation indicators or status feedback for the resume action.

## Escalation Guidance

* Escalate if AGV movement does not resume after using the Resume All AGVs control.
* Escalate if the required control is not available on the AGVs section.
* Escalate if confirmation of the resume action cannot be established from the available source-supported indicators.

## Missing Details / Known Gaps

* The source does not provide a detailed navigation sequence beyond access to the API screen and AGVs section.
* The source does not provide confirmation indicators, status feedback, or verification steps after using Resume All AGVs.
* The source does not provide timing expectations for the resume action.
* The source does not specify production stop or LOTO requirements for this action.

## Source Lineage

- Candidate IDs: candidate_l1_resume_all_agv_movement_from_api_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
