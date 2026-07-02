# Compare System Bag Out Close Out Versus System Purge On The API Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_compare_system_bag_out_close_out_versus_system_purge_on_the_api_page_v1` |
| Title | Compare System Bag Out Close Out Versus System Purge On The API Page |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Reference aid for distinguishing System Bag Out/close out from System Purge on the Overall System Aveva API page using source-backed differences in tote exchange scope and label printing behavior.

## When To Use

Use when reviewing the Overall System Aveva API page and needing to interpret the difference between System Bag Out/close out and System Purge based on the training source.

## Do Not Use For

* Not for executing Bag Out, close out, or Purge actions, because the source does not provide explicit execution steps.
* Not for assuming operational differences beyond tote scope and label printing behavior explicitly stated in the source.

## Safety And Operational Notes

* Do not assume additional operational differences beyond those explicitly stated in the source.
* Escalate if the displayed page labels or descriptions do not match the training source.

## Access Or Tools Needed

* Access to the Overall System Aveva API page
* Source-backed descriptions of Bag Out or close out and Purge

## Related Operational Context

* ctx_training_video_bag_out_close_out_reference_v1
* ctx_training_video_system_purge_reference_v1
* ctx_training_video_api_page_overview_v1

## Procedure Steps

### Step 1 — Locate System Bag Out and System Purge on the API page

**Responsible role:** operator

**Instruction:**
Open or view the Overall System Aveva API page and locate the System Bag Out and System Purge items on the page.

**Expected result:**
Both System Bag Out and System Purge are visible on the API page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*Left-side system items on the Overall System Aveva API page, including System Bag Out and System Purge.*


**Stop or Escalate If:**

* Displayed page labels do not match the training source.
* System Bag Out or System Purge cannot be identified on the page.

---

### Step 2 — Identify the Bag Out or close out description

**Responsible role:** operator

**Instruction:**
Identify the Bag Out or close out description as the end-of-sort function that closes all chutes and exchanges totes with items.

**Expected result:**
Bag Out or close out is recognized as an end-of-sort function tied to closing chutes and exchanging totes with items.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*System Bag Out area and associated training description on the Overall System Aveva API page.*


**Stop or Escalate If:**

* Displayed description does not match the training source.

---

### Step 3 — Confirm Bag Out or close out tote scope and label behavior

**Responsible role:** operator

**Instruction:**
Note from the transcript that close out only affects totes with items and prints labels.

**Expected result:**
The Bag Out or close out function is understood to apply only to totes with items and to print labels.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*Training frame and aligned description indicating close out affects totes with items and prints labels.*


**Stop or Escalate If:**

* The displayed or described behavior conflicts with the training source.
* There is pressure to assume additional close out behavior not stated in the source.

---

### Step 4 — Identify the Purge description

**Responsible role:** operator

**Instruction:**
Identify the Purge description as the function that exchanges all totes in the system.

**Expected result:**
Purge is recognized as the function that exchanges all totes in the system.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*System Purge area and associated training description on the Overall System Aveva API page.*


**Stop or Escalate If:**

* Displayed description does not match the training source.

---

### Step 5 — Confirm Purge label behavior

**Responsible role:** operator

**Instruction:**
Confirm from the source that Purge does not print a label at the tipper.

**Expected result:**
Purge is understood to exchange all totes without printing a label at the tipper.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*Training frame and aligned description indicating Purge does not print a label at the tipper.*


**Stop or Escalate If:**

* The displayed or described behavior conflicts with the training source.
* There is pressure to assume additional purge behavior not stated in the source.

---

### Step 6 — Record the Bag Out versus Purge distinction

**Responsible role:** operator

**Instruction:**
Record the distinction: close out is limited to totes with items and prints labels, while purge exchanges all totes and does not print a label.

**Expected result:**
A clear comparison is documented using only the source-backed differences.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*Overall API page context showing both System Bag Out and System Purge for side-by-side interpretation.*


**Stop or Escalate If:**

* Displayed page labels or descriptions do not match the training source.
* Additional operational differences are requested without source support.

---

## Success Criteria

* The user can correctly distinguish Bag Out/close out from Purge using the source-backed differences in tote scope and label printing.
* Bag Out/close out is understood as affecting totes with items and printing labels.
* Purge is understood as exchanging all totes and not printing a label at the tipper.

## Failure Conditions

* Displayed page labels or descriptions do not match the training source.
* The user assumes additional operational differences not explicitly stated in the source.
* Bag Out/close out and Purge are confused on tote scope or label printing behavior.

## Escalation Guidance

* Escalate if the displayed page labels or descriptions do not match the training source.
* Escalate if clarification is needed beyond the source-supported differences of tote scope and label printing behavior.

## Missing Details / Known Gaps

* The source explains the difference between Bag Out/close out and Purge but does not provide explicit execution steps for running either function.
* The source does not specify production stop requirements.
* The source does not specify LOTO requirements.
* The source does not provide a time estimate for this reference activity.
* The source does not define supporting role boundaries beyond operator use.

## Source Lineage

- Candidate IDs: candidate_training_video_compare_bag_out_close_out_and_purge_on_api_page
- Source ID: `training_video_day1`
- Source Type: `training_video`
