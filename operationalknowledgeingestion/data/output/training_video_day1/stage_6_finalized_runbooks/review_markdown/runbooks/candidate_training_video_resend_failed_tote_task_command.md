# Resend a Tote Task Command After a Tote Error or Failed Execution

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resend_a_tote_task_command_after_a_tote_error_or_failed_execution_v1` |
| Title | Resend a Tote Task Command After a Tote Error or Failed Execution |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Resend Tote Task function in the tote management API page to resend a command to a tote that encountered an error or failed to execute, then review tote task status to confirm the resend outcome.

## When To Use

Use when a tote command encountered an error or failed to execute and support needs to resend the command using the Resend Tote Task function shown on the tote management API page.

## Do Not Use For

* Do not use for AGV command recovery; the source distinguishes tote management functions from AGV recovery functions.
* Do not use when deeper fault isolation, retry limits, or alternate recovery logic are required; the source does not provide those details.

## Safety And Operational Notes

* This source presents the action as a support recovery function for tote command errors or failed execution.
* Stop and escalate if the resend does not clear the failed condition or the tote continues to show an error after the resend.

## Access Or Tools Needed

* Access to tote management interface or API-backed Resend Tote Task function
* Tote identifier
* Ability to review tote task status

## Related Operational Context

* ctx_training_video_resend_tote_task_error_reference_v1
* ctx_training_video_get_tote_task_status_reference_v1
* ctx_training_video_tote_management_api_overview_v1

## Procedure Steps

### Step 1 — Identify the affected tote

**Responsible role:** L1_support

**Instruction:**
Identify the tote whose command encountered an error or failed to execute.

**Expected result:**
A specific affected tote is identified for the resend action.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*Tote management API features on the slide, especially Get Tote Task as the status lookup function for tote tasks.*


**Stop or Escalate If:**

* The affected tote cannot be identified.
* Available tote status information is insufficient to determine which tote failed.

---

### Step 2 — Open the Resend Tote Task function

**Responsible role:** L1_support

**Instruction:**
Open the tote management API page and locate the Resend Tote Task function.

**Expected result:**
The Resend Tote Task function is visible and ready for tote selection or entry.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*Aveva API page for tote management showing Resend Tote Task in the list of available functions.*


**Stop or Escalate If:**

* The tote management API page is inaccessible.
* The Resend Tote Task function is not present in the available interface.

---

### Step 3 — Enter or select the affected tote

**Responsible role:** L1_support

**Instruction:**
Enter or select the affected tote in the Resend Tote Task function.

**Expected result:**
The resend request is prepared for the intended tote.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management API page context where Resend Tote Task is available for tote-specific actions.*


**Stop or Escalate If:**

* The correct tote cannot be selected or entered.
* There is uncertainty that the selected tote is the one that failed.

---

### Step 4 — Submit the resend action

**Responsible role:** L1_support

**Instruction:**
Submit the resend action to resend the command to that tote.

**Expected result:**
The system issues a resent command for the selected tote.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*Resend Tote Task option on the tote management API page.*


**Stop or Escalate If:**

* The resend action does not clear the failed condition.
* The tote continues to show an error or failed execution after the resend.

---

### Step 5 — Verify tote task status after resend

**Responsible role:** L1_support

**Instruction:**
Check the tote task status afterward to verify whether the command was successfully resent and the tote state updated.

**Expected result:**
Tote task status reflects the resent command outcome and updated tote state if the resend succeeded.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*Get Tote Task function on the tote management API page for current tote status and task review.*


**Stop or Escalate If:**

* The resend action does not clear the failed condition.
* The tote continues to show an error or failed execution after the resend.

---

## Success Criteria

* The affected tote is identified and targeted with Resend Tote Task.
* The resend action is submitted for the selected tote.
* Tote task status afterward indicates the command was successfully resent and the tote state updated.

## Failure Conditions

* The affected tote cannot be identified.
* The Resend Tote Task function cannot be accessed or located.
* The resend action does not clear the failed condition.
* The tote continues to show an error or failed execution after the resend.

## Escalation Guidance

* Escalate if the resend action does not clear the failed condition.
* Escalate if the tote continues to show an error or failed execution after the resend.
* Escalate when deeper fault isolation is required because the source does not provide retry limits or additional troubleshooting steps.

## Missing Details / Known Gaps

* The source does not provide the exact UI fields or button labels used to submit Resend Tote Task.
* The source does not provide retry limits.
* The source does not provide deeper fault isolation steps if resend fails.
* The source does not provide explicit production stop or LOTO requirements.
* The source does not provide a time estimate for completing this procedure.

## Source Lineage

- Candidate IDs: candidate_training_video_resend_failed_tote_task_command
- Source ID: `training_video_day1`
- Source Type: `training_video`
