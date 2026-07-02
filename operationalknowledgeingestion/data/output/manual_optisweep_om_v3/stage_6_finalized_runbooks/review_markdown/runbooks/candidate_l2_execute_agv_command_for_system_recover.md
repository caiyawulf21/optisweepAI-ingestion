# Use Execute AGV Command For System Recovery

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_execute_agv_command_for_system_recovery_v1` |
| Title | Use Execute AGV Command For System Recovery |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Execute AGV Command control in the AGVs section of the System HMI API screen for system recovery when the system has gone down and messages were missed. The source documents the control and its purpose, but does not provide the command inputs, parameters, or confirmation behavior.

## When To Use

Use this procedure during system recovery when the system went down and messages were missed, and the recovery action involves the Execute AGV Command control in the AGVs section of the API screen.

## Do Not Use For

* Do not use this runbook as a complete command-entry procedure when the required command inputs, parameters, or confirmation behavior are needed but not available from approved site documentation or support personnel.
* Do not use this runbook for non-recovery AGV operations not supported by the source.

## Safety And Operational Notes

* This is a recovery-related control with potential system-wide impact.
* The source does not provide command inputs, parameters, or confirmation behavior; do not improvise unsupported recovery commands.
* Escalate if approved site documentation or support personnel cannot provide the required recovery command details.

## Access Or Tools Needed

* Access to the System HMI API screen
* AGVs section of the API screen
* Execute AGV Command control

## Related Operational Context

* ctx_manual_tote_api_controls_overview_v1
* ctx_manual_agv_system_recovery_commands_v1

## Procedure Steps

### Step 1 — Open the AGVs section of the API screen

**Responsible role:** L2_support

**Instruction:**
Open the System HMI API screen and navigate to the AGVs section.

**Expected result:**
The AGVs section of the API screen is visible.

**Screens / Images:**

![artifact_fig_4_8_acb_api_screen](assets/artifact_fig_4_8_acb_api_screen.jpeg)

*The ACB API screen interface used to access AGV controls.*

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The AGV API Controls area within the AGVs section of the API screen.*


**Stop or Escalate If:**

* The System HMI API screen cannot be accessed.
* The AGVs section is not available on the API screen.

---

### Step 2 — Locate the Execute AGV Command control

**Responsible role:** L2_support

**Instruction:**
In the AGVs section, locate the Execute AGV Command control.

**Expected result:**
The Execute AGV Command control is identified on the AGV API Controls screen.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Execute AGV Command control listed among the AGV API Controls.*


**Stop or Escalate If:**

* The Execute AGV Command control is not present on the AGV API Controls screen.
* The displayed screen does not match the documented AGV API Controls layout.

---

### Step 3 — Use Execute AGV Command for documented recovery purpose

**Responsible role:** L2_support

**Instruction:**
Use Execute AGV Command as part of system recovery when the system went down and messages were missed. If the required command details are not available from approved site documentation or support personnel, stop and escalate.

**Expected result:**
The Execute AGV Command control is used for the documented system recovery purpose related to missed messages.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Execute AGV Command control used for system recovery in the AGV API Controls screen.*


**Stop or Escalate If:**

* The source does not provide the command inputs, parameters, or confirmation behavior for this control.
* Required recovery command details are not available from approved site documentation or support personnel.

---

## Success Criteria

* The AGVs section of the API screen is accessed.
* The Execute AGV Command control is identified.
* The control is used only for the documented recovery case where the system went down and messages were missed.

## Failure Conditions

* The API screen or AGVs section cannot be accessed.
* The Execute AGV Command control cannot be located.
* The source does not provide enough detail to safely determine command inputs, parameters, or confirmation behavior.

## Escalation Guidance

* Escalate if the required recovery command details are not available from approved site documentation or support personnel.
* Escalate if the Execute AGV Command control is unavailable or the screen does not match the documented AGV API Controls view.

## Missing Details / Known Gaps

* The source does not provide the exact command inputs for Execute AGV Command.
* The source does not provide required parameters or field values for the control.
* The source does not describe confirmation behavior, expected on-screen feedback, or completion indicators.
* The source does not define whether production must be stopped before using this control.
* The source does not define whether lockout/tagout is required.
* The source does not provide a time estimate for this recovery action.

## Source Lineage

- Candidate IDs: candidate_l2_execute_agv_command_for_system_recover
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
