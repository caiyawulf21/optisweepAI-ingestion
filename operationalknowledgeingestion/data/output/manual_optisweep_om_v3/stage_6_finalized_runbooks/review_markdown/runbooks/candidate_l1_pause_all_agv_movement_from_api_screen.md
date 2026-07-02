# Pause All AGV Movement From The API Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_pause_all_agv_movement_from_the_api_screen_v1` |
| Title | Pause All AGV Movement From The API Screen |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Pause movement for all AGVs using the Pause All AGVs control in the AGVs section of the System HMI API screen.

## When To Use

Use this procedure when all AGV movement needs to be paused from the AGVs section of the API screen.

## Do Not Use For

* Do not use this procedure for removing an AGV from the system.
* Do not use this procedure for recovering an AGV back into the system.
* Do not use this procedure for resuming AGV movement.
* Do not use this procedure for executing or resending AGV commands.

## Safety And Operational Notes

* This is a fleet-wide control that pauses all AGV movement.
* The source does not provide confirmation indicators or status feedback for the pause action.

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
Open the API screen and go to the AGVs section.

**Expected result:**
The AGVs section of the API screen is visible.

**Screens / Images:**

![artifact_fig_4_8_acb_api_screen](assets/artifact_fig_4_8_acb_api_screen.jpeg)

*The API interface used to control the OptiSweep system, AGVs, and totes.*

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The AGV API Controls area within the AGVs section of the API screen.*


**Stop or Escalate If:**

* Stop or escalate if the API screen cannot be opened.
* Stop or escalate if the AGVs section is not accessible.

---

### Step 2 — Locate the Pause All AGVs control

**Responsible role:** L1_support

**Instruction:**
In the AGVs section, locate the control labeled Pause All AGVs.

**Expected result:**
The Pause All AGVs control is identified on the screen.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Pause All AGVs control among the AGV API Controls.*


**Stop or Escalate If:**

* Stop or escalate if the Pause All AGVs control is not present on the AGVs section.

---

### Step 3 — Pause all AGV movement

**Responsible role:** L1_support

**Instruction:**
Use the Pause All AGVs control to pause all AGV movement.

**Expected result:**
All AGV movement is paused.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Pause All AGVs control used to pause all AGV movement.*


**Stop or Escalate If:**

* Escalate if AGV movement does not pause after using the control.
* Escalate if no confirmation or status feedback is available and AGV movement status cannot be verified from the source-supported screen information.

---

## Success Criteria

* The Pause All AGVs control is used from the AGVs section of the API screen.
* All AGV movement is paused.

## Failure Conditions

* The API screen cannot be accessed.
* The AGVs section cannot be opened.
* The Pause All AGVs control cannot be located.
* AGV movement does not pause after using the control.
* The source does not provide confirmation indicators or status feedback for the pause action.

## Escalation Guidance

* Escalate if AGV movement does not pause after using the control.
* Escalate if the Pause All AGVs control is unavailable or cannot be accessed.
* Escalate if the operator cannot verify the result because the source does not provide confirmation indicators or status feedback.

## Missing Details / Known Gaps

* The source does not provide explicit confirmation indicators or status feedback for the pause action.
* The source does not provide an estimated completion time.
* The source does not specify whether production must be stopped before using this control.
* The source does not specify whether lockout/tagout is required.
* The source does not define a more detailed verification method for confirming that all AGV movement has paused.

## Source Lineage

- Candidate IDs: candidate_l1_pause_all_agv_movement_from_api_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
