# Check the Tote Error Field In the Tote Task Interface

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_the_tote_error_field_in_the_tote_task_interface_v1` |
| Title | Check the Tote Error Field In the Tote Task Interface |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Tote Task interface to determine whether a tote-related error is shown for a tote and capture the associated tote and task identifiers displayed on the same record.

## When To Use

Use when investigating a tote and you need to verify whether the Tote Task interface shows a tote-related error and identify the associated Tote ID, Task Name, Task ID, and sorter task UID if shown.

## Do Not Use For

* Interpreting the meaning of a tote error when the source does not define the error.
* Resolving or correcting tote errors; this source only supports checking and recording what is displayed.
* Using fields not shown or supported by the Tote Task interface evidence in this source.

## Safety And Operational Notes

* This source supports a diagnostic information-gathering check only.
* Do not infer corrective actions, error meanings, or system changes from this source alone.

## Access Or Tools Needed

* Access to the Tote Task interface
* Visibility of the Tote Error, Tote ID, Task ID, and Task Name fields

## Related Operational Context

* ctx_training_video_tote_task_data_fields_v1
* ctx_training_video_tote_error_field_reference_v1

## Procedure Steps

### Step 1 — Open or view the Tote Task interface

**Responsible role:** L1_support

**Instruction:**
Open or view the Tote Task interface for the tote being investigated.

**Expected result:**
The Tote Task interface is visible for the tote record under investigation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Tote Tasks Aveva API page showing the tote task detail fields, including Tote Error.*


**Stop or Escalate If:**

* The Tote Task interface is unavailable.
* The tote being investigated cannot be matched to a visible record.

---

### Step 2 — Locate the Tote Error field

**Responsible role:** L1_support

**Instruction:**
Locate the Tote Error field on the interface.

**Expected result:**
The Tote Error field is identified on the displayed Tote Task record.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*The Tote Error field listed among the Tote Task interface data fields.*


**Stop or Escalate If:**

* The Tote Error field is missing.
* The Tote Error field is unreadable.
* The displayed fields do not align with the expected Tote Task record.

---

### Step 3 — Check whether an error is shown

**Responsible role:** L1_support

**Instruction:**
Check whether any error is shown in the Tote Error field.

**Expected result:**
You can confirm whether the Tote Error field shows an error indication or not.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*The Tote Error field value for the displayed tote task record.*


**Stop or Escalate If:**

* An error is shown but the source does not provide enough information to interpret or resolve it.
* The Tote Error field is unreadable.
* The Tote Error field does not align with the displayed tote record.

---

### Step 4 — Read the Tote ID

**Responsible role:** L1_support

**Instruction:**
Read the Tote ID shown for the same record.

**Expected result:**
The Tote ID for the displayed record is identified.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*The Tote ID field on the same Tote Task record as the Tote Error field.*


**Stop or Escalate If:**

* The Tote ID is missing or unreadable.
* The Tote ID cannot be confidently tied to the same record as the Tote Error field.

---

### Step 5 — Review task identifiers

**Responsible role:** L1_support

**Instruction:**
Review the Task Name and Task ID fields, and sorter task UID if shown, to associate the error with the displayed task.

**Expected result:**
The task identifiers associated with the displayed tote record are identified.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Task ID, Task Name, and any sorter task UID information shown with the Tote Task record.*


**Stop or Escalate If:**

* Task Name or Task ID is missing or unreadable.
* Sorter task UID is expected by the workflow but is not shown.
* The task fields do not appear to match the displayed tote record.

---

### Step 6 — Record the displayed values exactly as shown

**Responsible role:** L1_support

**Instruction:**
Record the displayed error indication and the related tote and task identifiers exactly as shown.

**Expected result:**
A complete record of the displayed Tote Error state and associated identifiers is captured.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*All displayed Tote Task fields needed to document the error indication and associated identifiers.*


**Stop or Escalate If:**

* An error is shown but the source does not provide enough information to interpret or resolve it.
* The displayed values cannot be read clearly enough to document exactly.
* The Tote Error field is missing, unreadable, or does not align with the displayed tote record.

---

## Success Criteria

* The Tote Task interface is viewed for the tote under investigation.
* The Tote Error field is located and checked.
* The user confirms whether an error is shown.
* The displayed Tote ID, Task Name, Task ID, and sorter task UID if shown are captured exactly as displayed.

## Failure Conditions

* The Tote Task interface cannot be accessed or the relevant record cannot be viewed.
* The Tote Error field is missing or unreadable.
* The Tote Error field does not align with the displayed tote record.
* The tote or task identifiers are missing, unreadable, or cannot be associated with the same record.
* An error is shown but the source does not provide enough information to interpret or resolve it.

## Escalation Guidance

* Escalate if an error is shown but the source does not provide enough information to interpret or resolve it.
* Escalate if the Tote Error field is missing, unreadable, or does not align with the displayed tote record.

## Missing Details / Known Gaps

* The source does not define the meaning of specific Tote Error values.
* The source does not provide corrective actions or resolution steps for tote errors.
* The source does not provide a time estimate for this check.
* The source does not specify production stop or LOTO requirements.
* The source does not provide exact navigation steps to reach the Tote Task interface.

## Source Lineage

- Candidate IDs: candidate_training_video_check_tote_error_on_tote_task_interface
- Source ID: `training_video_day1`
- Source Type: `training_video`
