# Manually Reset Tipper Stats From the Overall System Aveva API Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_manually_reset_tipper_stats_from_the_overall_system_aveva_api_page_v1` |
| Title | Manually Reset Tipper Stats From the Overall System Aveva API Page |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Overall System Aveva API page to locate and activate the Reset Tipper Stats control. The source indicates tipper metrics are normally reset when a new sort plan is loaded, but they can also be manually reset from this page.

## When To Use

Use when tipper statistics need to be manually reset from the Overall System Aveva API page and the Reset Tipper Stats control is available.

## Do Not Use For

* Do not use as a validated post-reset verification procedure; the source does not provide validation steps after the reset.
* Do not use when the Reset Tipper Stats control is missing or non-responsive; escalate instead.

## Safety And Operational Notes

* The source does not identify special safety hazards for this page action.
* Do not assume production stop or lockout/tagout requirements from this source; they are not stated.

## Access Or Tools Needed

* Access to the Overall System Aveva API page
* Reset Tipper Stats control on the HMI page

## Related Operational Context

* ctx_training_video_overall_system_aveva_api_page_v1
* ctx_training_video_reset_tipper_stats_reference_v1

## Procedure Steps

### Step 1 — Open the Overall System Aveva API page

**Responsible role:** L1_support

**Instruction:**
Open the Overall System Aveva API page.

**Expected result:**
The Overall System Aveva API page is displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*Overall System Aveva API page with Reset Tipper Stats visible among the page options.*


**Stop or Escalate If:**

* The Overall System Aveva API page is not accessible.
* The displayed page does not match the expected Overall System Aveva API page.

---

### Step 2 — Locate the Reset Tipper Stats control

**Responsible role:** L1_support

**Instruction:**
Locate the Reset Tipper Stats control on the Overall System Aveva API page.

**Expected result:**
The Reset Tipper Stats control is visible and identifiable on the page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*The Reset Tipper Stats control on the Overall System Aveva API page.*


**Stop or Escalate If:**

* The Reset Tipper Stats control is missing.
* The control cannot be clearly identified on the page.

---

### Step 3 — Verify the page note about reset behavior

**Responsible role:** L1_support

**Instruction:**
Verify the page note indicating the metrics are reset when a new sort plan is loaded but can also be manually reset.

**Expected result:**
The page note or associated source evidence confirms the reset behavior.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*The page area and associated OCR-supported content indicating metrics are reset when a new sort plan is loaded but can also be manually reset.*


**Stop or Escalate If:**

* The reset behavior note cannot be confirmed from the page or source evidence.

---

### Step 4 — Use Reset Tipper Stats

**Responsible role:** L1_support

**Instruction:**
Use the Reset Tipper Stats control to perform the manual reset.

**Expected result:**
Tipper statistics are manually reset from the page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*The Reset Tipper Stats control used to initiate the manual reset.*


**Stop or Escalate If:**

* The Reset Tipper Stats control does not respond as expected.
* There is no observable indication that the manual reset action completed.
* Additional validation is required beyond what the source provides.

---

## Success Criteria

* The Overall System Aveva API page is opened.
* The Reset Tipper Stats control is located.
* The manual reset is initiated using the Reset Tipper Stats control.
* Tipper statistics are manually reset from the page.

## Failure Conditions

* The Overall System Aveva API page cannot be accessed.
* The Reset Tipper Stats control is missing.
* The Reset Tipper Stats control does not respond as expected.
* The source does not provide additional validation steps after the reset.

## Escalation Guidance

* Escalate if the Reset Tipper Stats control is missing or does not respond as expected.
* Escalate if additional post-reset validation is required, because the source does not provide validation steps after the reset.

## Missing Details / Known Gaps

* The source does not provide detailed navigation steps for reaching the Overall System Aveva API page.
* The source does not provide a confirmation dialog, button behavior, or exact UI response after selecting Reset Tipper Stats.
* The source does not provide explicit post-reset verification steps.
* The source does not explicitly assign the task to a named role; L1_support is a conservative candidate-derived assignment.
* The source does not state whether production must be stopped before performing this action.
* The source does not state whether lockout/tagout is required.

## Source Lineage

- Candidate IDs: candidate_training_video_manually_reset_tipper_stats
- Source ID: `training_video_day1`
- Source Type: `training_video`
