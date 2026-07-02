# Check The Current Tote Task Using The Get Tote Task API Function

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_the_current_tote_task_using_the_get_tote_task_api_function_v1` |
| Title | Check The Current Tote Task Using The Get Tote Task API Function |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented Get Tote Task function shown on the Aveva API tote management page to identify the current tote task. The source supports the existence and purpose of the function, but does not provide execution details, parameters, or response fields.

## When To Use

Use when a support user needs to confirm that the Aveva API tote management page includes the Get Tote Task function and to verify from the source that it is intended to retrieve the current tote task. If access to the API page is available, use the documented function as shown by the page to check the current tote task.

## Do Not Use For

* Do not use this runbook to infer request fields, parameters, or response details for Get Tote Task.
* Do not use this runbook as a full API execution procedure because the source does not document how to execute the function.
* Do not use this runbook to perform tote recovery actions such as Resend Tote Task unless separately supported.

## Safety And Operational Notes

* This is a source-supported diagnostic/reference action and no hazardous physical action is described.
* Do not invent request fields, parameters, or response details because they are not provided in the source.

## Access Or Tools Needed

* Access to the Aveva API page showing tote management functions
* Ability to view or use the Get Tote Task function

## Related Operational Context

* ctx_training_video_tote_api_task_functions_v1

## Procedure Steps

### Step 1 — Open or view the tote management API page

**Responsible role:** L1_support

**Instruction:**
Open or view the Aveva API page that lists tote management functions.

**Expected result:**
The tote management API page is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0072_it_s_it_s_on_those_primary_02_24_58_500](assets/2c7bff1ff4ef9684.jpg)

*API Features for Tote Management list on the Aveva API page.*


**Stop or Escalate If:**

* Escalate if the displayed API page is not visible or accessible.

---

### Step 2 — Locate Get Tote Task

**Responsible role:** L1_support

**Instruction:**
Locate the function named "Get Tote Task."

**Expected result:**
The Get Tote Task function is found in the tote management function list.

**Screens / Images:**

![artifact_training_video_training_video_day1_0072_it_s_it_s_on_those_primary_02_24_58_500](assets/2c7bff1ff4ef9684.jpg)

*The Get Tote Task entry in the API Features for Tote Management list.*


**Stop or Escalate If:**

* Escalate if the Get Tote Task function is not visible or accessible on the displayed API page.

---

### Step 3 — Verify the function purpose

**Responsible role:** L1_support

**Instruction:**
Verify from the displayed description that this function retrieves the current tote task.

**Expected result:**
The function purpose is confirmed from the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0072_it_s_it_s_on_those_primary_02_24_58_500](assets/2c7bff1ff4ef9684.jpg)

*The Get Tote Task function on the tote management API page, together with the source statement describing its purpose.*


**Stop or Escalate If:**

* Escalate if the source-visible description does not support that Get Tote Task retrieves the current tote task.

---

### Step 4 — Use Get Tote Task if access is available

**Responsible role:** L1_support

**Instruction:**
Use the function as documented by the page to check the current tote task, if access to the API page is available.

**Expected result:**
The current tote task is identified or retrieved using the Get Tote Task function.

**Screens / Images:**

![artifact_training_video_training_video_day1_0072_it_s_it_s_on_those_primary_02_24_58_500](assets/2c7bff1ff4ef9684.jpg)

*The Get Tote Task function entry on the tote management API page.*


**Stop or Escalate If:**

* Escalate if the Get Tote Task function is not visible or accessible on the displayed API page.
* Stop and escalate if execution requires request fields, parameters, or response interpretation not provided in the source.

---

### Step 5 — Record the result

**Responsible role:** L1_support

**Instruction:**
Record that the current tote task was retrieved using the Get Tote Task function.

**Expected result:**
A record exists that the current tote task was retrieved using Get Tote Task.

**Stop or Escalate If:**

* Stop and escalate if documenting the result would require invented request fields, parameters, or response details.

---

## Success Criteria

* The Get Tote Task function is located on the Aveva API tote management page.
* The source-supported purpose of Get Tote Task is confirmed as retrieving the current tote task.
* If access is available, the current tote task is identified or retrieved using the documented function.
* The result is recorded without inventing unsupported API details.

## Failure Conditions

* The Aveva API tote management page is not visible or accessible.
* The Get Tote Task function is not visible or accessible on the displayed page.
* The source does not provide execution details, request fields, parameters, or response fields needed for deeper use.
* The user would need to invent unsupported technical details to continue.

## Escalation Guidance

* Escalate if the Get Tote Task function is not visible or accessible on the displayed API page.
* Escalate if additional API execution details are required, because the source does not provide request fields, parameters, or response details.
* Escalate if the function purpose cannot be confirmed from the displayed source material.

## Missing Details / Known Gaps

* The source does not provide the execution method for Get Tote Task.
* The source does not provide request fields or parameters for Get Tote Task.
* The source does not provide response fields or example output for Get Tote Task.
* The source does not define a recording location or format for documenting the result.
* The source does not specify role boundaries beyond support-oriented usage.

## Source Lineage

- Candidate IDs: candidate_training_video_check_current_tote_task_via_api_function
- Source ID: `training_video_day1`
- Source Type: `training_video`
