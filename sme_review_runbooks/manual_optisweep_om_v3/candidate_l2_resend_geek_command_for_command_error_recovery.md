# Resend A Geek+ Command From The API Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resend_a_geek_command_from_the_api_screen_v1` |
| Title | Resend A Geek+ Command From The API Screen |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Resend Geek Command control on the System HMI API screen AGVs section during documented system recovery handling when Geek+ has a command error and the command guide can be provided so the message is resent to Geek+.

## When To Use

Use this procedure during system recovery handling when Geek+ has a command error and the command guide can be provided, using the Resend Geek Command control in the AGVs section of the API screen.

## Do Not Use For

* Do not use when the command guide is unavailable.
* Do not use when the source does not support the exact command guide contents or entry method for the situation being handled.

## Safety And Operational Notes

* This is a recovery-related action and is not marked support-safe by the candidate.
* The source does not define the command guide format, contents, or entry method; use caution and escalate if those details are not known.

## Access Or Tools Needed

* Access to the System HMI API screen
* AGVs section of the API screen
* Resend Geek Command control
* Command guide

## Related Operational Context

* ctx_manual_tote_api_controls_overview_v1
* ctx_manual_agv_system_recovery_commands_v1

## Procedure Steps

### Step 1 — Open the AGVs section of the API screen

**Responsible role:** L2_support

**Instruction:**
Open the System HMI API screen and go to the AGVs section.

**Expected result:**
The AGVs section of the API screen is displayed.

**Screens / Images:**

![artifact_fig_4_8_acb_api_screen](assets/artifact_fig_4_8_acb_api_screen.jpeg)

*API interface context used to access system, AGV, and tote controls.*

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls screen showing the AGVs section where Resend Geek Command is located.*


**Stop or Escalate If:**

* Stop or escalate if the System HMI API screen cannot be accessed.
* Stop or escalate if the AGVs section is not available.

---

### Step 2 — Locate the Resend Geek Command control

**Responsible role:** L2_support

**Instruction:**
In the AGVs section of the API screen, locate the Resend Geek Command control.

**Expected result:**
The Resend Geek Command control is identified on the AGV API Controls screen.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Resend Geek Command control within the AGV API Controls screen.*


**Stop or Escalate If:**

* Stop or escalate if the Resend Geek Command control is not present.
* Stop or escalate if the displayed screen does not match the AGV API Controls view.

---

### Step 3 — Provide the command guide

**Responsible role:** L2_support

**Instruction:**
Provide the command guide as described by the source when handling a Geek+ command error.

**Expected result:**
The command guide is provided to the Resend Geek Command function.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The AGV API Controls screen where the Resend Geek Command function is documented; the source does not define the command guide entry field or method.*


**Stop or Escalate If:**

* Stop or escalate if the command guide is unavailable.
* Stop or escalate if the source-supported command guide format or entry method is not known.

---

### Step 4 — Resend the message to Geek+

**Responsible role:** L2_support

**Instruction:**
Use the Resend Geek Command control so the message is resent to Geek+.

**Expected result:**
The message is resent to Geek+ using the documented recovery-related control.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Resend Geek Command control used to resend the message to Geek+.*


**Stop or Escalate If:**

* Stop or escalate if the message cannot be resent successfully.
* Stop or escalate if the control does not produce the documented resend behavior.

---

## Success Criteria

* The AGVs section of the API screen is accessed.
* The Resend Geek Command control is located.
* The command guide is provided.
* The message is resent to Geek+.

## Failure Conditions

* The System HMI API screen or AGVs section cannot be accessed.
* The Resend Geek Command control cannot be located.
* The command guide is unavailable.
* The source does not define the command guide format or entry method.
* The message cannot be resent successfully.

## Escalation Guidance

* Escalate if the command guide is unavailable.
* Escalate if the message cannot be resent successfully.
* Escalate for SME review if the required command guide contents, format, or entry method are not known from the source.

## Missing Details / Known Gaps

* The source does not define the command guide contents.
* The source does not define how the command guide is entered or provided in the HMI.
* The source does not define confirmation indicators for a successful resend.
* The source does not define follow-up verification steps after the message is resent.
* The source does not state whether production must be stopped before performing this action.
* The source does not state whether lockout/tagout is required.

## Source Lineage

- Candidate IDs: candidate_l2_resend_geek_command_for_command_error_recovery
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
