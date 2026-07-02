# Resend A Tote Task Command Using The Resend Tote Task API Function

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resend_a_tote_task_command_using_the_resend_tote_task_api_function_v1` |
| Title | Resend A Tote Task Command Using The Resend Tote Task API Function |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

This source documents that the Aveva API tote management page includes a function named "Resend Tote Task" and states that it resends a command to a tote that encountered an error or failed to execute. The source supports identification and intended use of the function, but does not provide execution parameters, confirmation workflow, or validation steps.

## When To Use

Use when working from the Aveva API tote management page and the documented need is to resend a command to a tote that encountered an error or failed to execute.

## Do Not Use For

* Do not use to invent tote identifiers, parameters, confirmation steps, or validation checks not provided by the source.
* Do not use when the tote state is unclear.
* Do not use if the Resend Tote Task function is unavailable.
* Do not use as a complete recovery procedure; the source documents function purpose only.

## Safety And Operational Notes

* This is a state-changing recovery action and the source does not provide detailed safeguards.
* Use only with authorized access to the Aveva API page.
* The source does not provide tote selection criteria, parameters, or post-action verification steps.

## Access Or Tools Needed

* Access to the Aveva API page showing tote management functions
* Authorized ability to use the Resend Tote Task function

## Related Operational Context

* ctx_training_video_tote_api_task_functions_v1

## Procedure Steps

### Step 1 — Open the tote management API page

**Responsible role:** L2_support

**Instruction:**
Open or view the Aveva API page that lists tote management functions.

**Expected result:**
The tote management API page is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0072_it_s_it_s_on_those_primary_02_24_58_500](assets/2c7bff1ff4ef9684.jpg)

*API Features for Tote Management list with Resend Tote Task visible among the tote functions.*


**Stop or Escalate If:**

* Escalate if the function is unavailable.

---

### Step 2 — Locate the Resend Tote Task function

**Responsible role:** L2_support

**Instruction:**
Locate the function named "Resend Tote Task."

**Expected result:**
The Resend Tote Task function is identified on the page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0072_it_s_it_s_on_those_primary_02_24_58_500](assets/2c7bff1ff4ef9684.jpg)

*The entry labeled Resend Tote Task in the API Features for Tote Management list.*


**Stop or Escalate If:**

* Escalate if the function is unavailable.

---

### Step 3 — Confirm the documented purpose of the function

**Responsible role:** L2_support

**Instruction:**
Verify from the displayed description that this function resends a command to a tote that encountered an error or failed to execute.

**Expected result:**
The displayed description matches the documented resend purpose.

**Screens / Images:**

![artifact_training_video_training_video_day1_0072_it_s_it_s_on_those_primary_02_24_58_500](assets/2c7bff1ff4ef9684.jpg)

*The Resend Tote Task entry and its surrounding tote management function context.*


**Stop or Escalate If:**

* Escalate if the tote state is unclear.

---

### Step 4 — Use the function only with authorized support access

**Responsible role:** L2_support

**Instruction:**
Use the Resend Tote Task function only if authorized access to the API page is available and the action is being performed by a support role.

**Expected result:**
The resend action is limited to an authorized support user.

**Stop or Escalate If:**

* Escalate if authorized access is not available.
* Stop if required parameters or controls are not documented in the source.

---

### Step 5 — Record the documented resend purpose

**Responsible role:** L2_support

**Instruction:**
Record that the resend action corresponds to the documented purpose shown on the page.

**Expected result:**
The action is documented as matching the source-described resend purpose.

**Stop or Escalate If:**

* Escalate if the resend action does not resolve the issue.

---

## Success Criteria

* The Aveva API tote management page is accessed.
* The Resend Tote Task function is identified.
* Its documented purpose is confirmed as resending a command to a tote that encountered an error or failed to execute.
* Any use of the function is limited to authorized support access.
* The action is recorded as matching the documented purpose from the source.

## Failure Conditions

* The tote management API page or function is unavailable.
* The tote state is unclear.
* Authorized access is not available.
* The resend action does not resolve the issue.
* Required execution details such as identifiers, parameters, confirmation steps, or validation checks are not provided by the source.

## Escalation Guidance

* Escalate if the function is unavailable.
* Escalate if the tote state is unclear.
* Escalate if the resend action does not resolve the issue.
* Escalate when execution requires identifiers, parameters, confirmation steps, or validation checks not documented in the source.

## Missing Details / Known Gaps

* The source does not provide the exact execution steps for invoking Resend Tote Task.
* The source does not provide required input fields or parameters for the resend action.
* The source does not provide tote identification or selection instructions.
* The source does not provide confirmation prompts, response handling, or validation checks.
* The source does not provide rollback or retry limits.
* The source does not provide explicit production-stop or LOTO requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_resend_tote_task_command_after_error
- Source ID: `training_video_day1`
- Source Type: `training_video`
