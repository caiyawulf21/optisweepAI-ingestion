# Open the Current Errors Pop-Up From the Overall System Aveva API Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_the_current_errors_pop_up_from_the_overall_system_aveva_api_page_v1` |
| Title | Open the Current Errors Pop-Up From the Overall System Aveva API Page |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Overall System Aveva API page to open the Get errors pop-up and view the current errors displayed by the system.

## When To Use

Use this procedure when you need to display the current errors from the Overall System Aveva API page for review.

## Do Not Use For

* Interpreting the meaning of the displayed errors when the source segment does not provide error definitions
* Performing corrective actions for the displayed errors
* Using pages other than the Overall System Aveva API page to retrieve errors

## Safety And Operational Notes

* This source segment presents the action as a pop-up viewing function and does not describe a hazardous physical action.
* Do not infer corrective actions from this segment; it only covers opening and viewing the current errors pop-up.

## Access Or Tools Needed

* Access to the Overall System Aveva API page
* Get errors control

## Related Operational Context

* ctx_training_video_overall_system_aveva_api_page_v1
* ctx_training_video_metrics_and_errors_popups_v1

## Procedure Steps

### Step 1 — Open the Overall System Aveva API page

**Responsible role:** L1_support

**Instruction:**
Open the Overall System Aveva API page.

**Expected result:**
The Overall System Aveva API page is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*The Overall System Aveva API page and the list of options that includes Get errors.*


**Stop or Escalate If:**

* The Overall System Aveva API page cannot be opened
* The page does not show the expected API options including Get errors

---

### Step 2 — Locate the Get errors control

**Responsible role:** L1_support

**Instruction:**
On the Overall System Aveva API page, locate the Get errors control.

**Expected result:**
The Get errors control is identified on the page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*The Get errors entry on the Overall System Aveva API page.*


**Stop or Escalate If:**

* The Get errors control is missing from the page
* The page layout does not match the source-supported view

---

### Step 3 — Select Get errors

**Responsible role:** L1_support

**Instruction:**
Select Get errors to open the current errors pop-up.

**Expected result:**
A pop-up opens showing the current errors.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*The Get errors control used to launch the current errors pop-up.*


**Stop or Escalate If:**

* The current errors pop-up does not appear

---

### Step 4 — Review the current errors pop-up

**Responsible role:** L1_support

**Instruction:**
Review the current errors shown in the pop-up window.

**Expected result:**
The current errors are visible for review in the pop-up window.

**Stop or Escalate If:**

* The pop-up does not show current errors
* Error interpretation or corrective action is needed, because this source segment does not provide that guidance

---

## Success Criteria

* The Overall System Aveva API page is opened
* The Get errors control is located
* Selecting Get errors opens a pop-up
* The pop-up shows the current errors for review

## Failure Conditions

* The Overall System Aveva API page cannot be accessed
* The Get errors control cannot be found
* The current errors pop-up does not appear
* The source segment does not provide interpretation or corrective action for the displayed errors

## Escalation Guidance

* Escalate if the current errors pop-up does not appear.
* Escalate if interpretation of the displayed errors or corrective action is required, because this source segment does not provide that guidance.

## Missing Details / Known Gaps

* The source does not provide navigation steps for reaching the Overall System Aveva API page.
* The source does not provide the contents, fields, or layout of the current errors pop-up.
* The source does not provide error interpretation guidance.
* The source does not provide corrective actions for any displayed errors.
* The source does not provide an estimated completion time.

## Source Lineage

- Candidate IDs: candidate_training_video_open_current_errors_popup
- Source ID: `training_video_day1`
- Source Type: `training_video`
