# Interpret System Faults Versus AGV System Faults On the Overall System RMS Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` |
| Title | Interpret System Faults Versus AGV System Faults On the Overall System RMS Page |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Overall System RMS page layout to determine whether a displayed fault is presented as a general system fault or an AGV system fault. The source states that system faults appear on the left side of the page and active AGV faults appear on the right side, with example interpretations for communication loss and an AGV commanded to move but not moving.

## When To Use

Use when reviewing the Overall System RMS page to categorize a displayed fault by where it appears on the page, or when explaining the source-backed distinction between system faults and AGV system faults.

## Do Not Use For

* Do not use to infer fault meanings beyond the source-provided page layout and examples.
* Do not use if the Overall System RMS page is unavailable or blank and the fault areas cannot be viewed.

## Safety And Operational Notes

* The source indicates the RMS page may appear blank if firewall access is not open.
* Do not infer additional fault meanings beyond the source-provided examples.

## Access Or Tools Needed

* Access to the Overall System RMS page or a source-backed view of it
* Source-backed understanding of the left-versus-right fault layout

## Related Operational Context

* ctx_training_video_system_faults_vs_agv_faults_v1

## Procedure Steps

### Step 1 — View the Overall System RMS page

**Responsible role:** L1_support

**Instruction:**
Open or view the Overall System RMS page if it is available.

**Expected result:**
The Overall System RMS page or a source-backed image of it is visible for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*Overall System RMS page layout showing that system faults are on the left and active AGV faults are on the right; note that the page may appear blank if firewall access is blocked.*


**Stop or Escalate If:**

* Escalate if the RMS page is unavailable or blank and the fault areas cannot be viewed.

---

### Step 2 — Check the left side for system faults

**Responsible role:** L1_support

**Instruction:**
Check the left side of the Overall System RMS page for system faults.

**Expected result:**
You determine whether the displayed fault appears in the system faults area on the left.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*Left side of the Overall System RMS page where the source says system faults are shown.*


**Stop or Escalate If:**

* Escalate if the left-side fault area cannot be viewed.

---

### Step 3 — Check the right side for active AGV faults

**Responsible role:** L1_support

**Instruction:**
Check the right side of the Overall System RMS page for active AGV faults.

**Expected result:**
You determine whether the displayed fault appears in the active AGV faults area on the right.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*Right side of the Overall System RMS page where the source says active AGV faults are shown.*


**Stop or Escalate If:**

* Escalate if the right-side fault area cannot be viewed.

---

### Step 4 — Interpret communication loss as a left-side system fault example

**Responsible role:** L1_support

**Instruction:**
If a communication loss with one of the carts is being discussed or displayed, interpret that as a system fault shown on the left based on the source explanation.

**Expected result:**
Communication-loss issues are categorized as left-side system faults when using this source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*Use the page layout while applying the source example that communication loss appears as a system fault on the left.*


**Stop or Escalate If:**

* Stop if the issue requires interpretation beyond the source-provided examples.

---

### Step 5 — Interpret AGV told to move but not moving as a right-side AGV fault example

**Responsible role:** L1_support

**Instruction:**
If an AGV was told to move but has not gone in progress, interpret that as an AGV system fault shown on the right based on the source explanation.

**Expected result:**
An AGV commanded to move but not moving is categorized as a right-side AGV system fault when using this source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*Use the page layout while applying the source example that an AGV told to move but not moving appears on the right.*


**Stop or Escalate If:**

* Stop if the issue requires interpretation beyond the source-provided examples.

---

### Step 6 — Record which side contains the fault

**Responsible role:** L1_support

**Instruction:**
Record which side of the page contains the fault so the observed issue is categorized using the source-backed page layout.

**Expected result:**
The issue is documented as a left-side system fault or right-side AGV system fault based on what was observed.

**Stop or Escalate If:**

* Stop if categorization would require unsupported interpretation beyond left-side system fault versus right-side AGV system fault.

---

## Success Criteria

* The user can distinguish whether the displayed issue is being presented as a system fault or an AGV system fault on the RMS page.
* The observed fault is categorized according to the source-backed left-versus-right page layout.

## Failure Conditions

* The Overall System RMS page is unavailable or blank and the fault areas cannot be viewed.
* The left or right fault areas cannot be reviewed.
* The user infers meanings beyond the source-provided examples and page layout.
* The issue cannot be categorized from the visible page layout.

## Escalation Guidance

* Escalate if the RMS page is unavailable or blank and the fault areas cannot be viewed.
* Escalate if the page layout cannot be confirmed from the available source-backed view.
* Do not extend interpretation beyond the source-provided examples without additional validated guidance.

## Missing Details / Known Gaps

* The source does not provide a navigation path for opening the Overall System RMS page.
* The source does not provide a formal documentation location or recording method for the categorized fault.
* The source does not define additional fault examples beyond communication loss and an AGV told to move but not moving.
* The source does not provide timing estimates for this reference procedure.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_overall_system_rms_fault_areas
- Source ID: `training_video_day1`
- Source Type: `training_video`
