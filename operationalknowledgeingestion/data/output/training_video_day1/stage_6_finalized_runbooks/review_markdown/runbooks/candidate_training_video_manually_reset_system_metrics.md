# Manually Reset System Metrics From the Overall System Aveva API Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_manually_reset_system_metrics_from_the_overall_system_aveva_api_page_v1` |
| Title | Manually Reset System Metrics From the Overall System Aveva API Page |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Reset system metrics manually from the Overall System Aveva API page when a manual reset is needed. The source states that metrics are normally reset automatically when a new sort plan is loaded, but the page also provides a Reset Metrics control for manual reset.

## When To Use

Use this procedure when a manual reset of system metrics is needed from the Overall System Aveva API page.

## Do Not Use For

* Do not use this runbook for the UPSHMI A tag reset method, because the source mentions that method but does not provide a supported procedure.
* Do not use this runbook to infer confirmation prompts, post-reset indicators, or alternate reset workflows not shown in the source.

## Safety And Operational Notes

* Use only the Reset Metrics control described on the Overall System Aveva API page.
* Do not invent or perform unsupported steps for the UPSHMI A tag method from this source alone.

## Access Or Tools Needed

* Access to the Overall System Aveva API page
* Reset Metrics control on the HMI page

## Related Operational Context

* ctx_training_video_overall_system_aveva_api_page_v1
* ctx_training_video_reset_metrics_reference_v1

## Procedure Steps

### Step 1 — Open the Overall System Aveva API page

**Responsible role:** L1_support

**Instruction:**
Open the Overall System Aveva API page.

**Expected result:**
The Overall System Aveva API page is displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*Overall System Aveva API page with the Reset Metrics control.*


**Stop or Escalate If:**

* Escalate if the Overall System Aveva API page is not available.
* Escalate if the expected Reset Metrics control is not present on the page.

---

### Step 2 — Locate and verify the Reset Metrics control

**Responsible role:** L1_support

**Instruction:**
Locate the Reset Metrics control on the page and verify the page note that metrics are reset when a new sort plan is loaded but can also be manually reset.

**Expected result:**
The Reset Metrics control is identified and the page note confirms both automatic and manual reset behavior.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*Reset Metrics control and the page text indicating metrics are reset when a new sort plan is loaded but can also be manually reset.*


**Stop or Escalate If:**

* Escalate if the Reset Metrics control is not available.
* Escalate if the page content does not match the source-supported reset behavior.

---

### Step 3 — Use Reset Metrics to perform the manual reset

**Responsible role:** L1_support

**Instruction:**
Use the Reset Metrics control to perform the manual reset.

**Expected result:**
System metrics are manually reset from the page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*Reset Metrics control used for manual reset on the Overall System Aveva API page.*


**Stop or Escalate If:**

* Escalate if the Reset Metrics control does not perform the reset as expected.

---

### Step 4 — Do not use the unsupported UPSHMI A tag method from this source

**Responsible role:** L1_support

**Instruction:**
If applicable in the local setup, note that the speaker states UPSHMI can also reset the metric by hitting an A tag, but no further source-backed steps are provided for that method.

**Expected result:**
The operator recognizes that the UPSHMI A tag method is only mentioned as a reference and is not executed from this runbook.

**Stop or Escalate If:**

* Stop if the requested reset depends on the UPSHMI A tag method, because this source does not provide the procedure.
* Escalate if an alternate reset method is required beyond the page-based Reset Metrics control.

---

## Success Criteria

* The Overall System Aveva API page is accessed.
* The Reset Metrics control is identified on the page.
* The manual reset is performed using the Reset Metrics control.
* No unsupported UPSHMI A tag procedure is attempted from this runbook.

## Failure Conditions

* The Overall System Aveva API page is not available.
* The Reset Metrics control is not available.
* The Reset Metrics control does not perform the reset as expected.
* The procedure requires the UPSHMI A tag method, which is not provided by this source.

## Escalation Guidance

* Escalate if the Reset Metrics control is not available or does not perform the reset as expected.
* Escalate if an alternate reset method is required beyond the page-based Reset Metrics control.
* Do not invent steps for the UPSHMI A tag method because the source does not provide the procedure.

## Missing Details / Known Gaps

* The source does not provide confirmation prompts or post-reset indicators.
* The source does not provide a detailed navigation path to reach the Overall System Aveva API page.
* The source does not provide a procedural workflow for the UPSHMI A tag reset method.
* The source does not specify whether production stop or LOTO is required.
* The source does not provide an estimated completion time.

## Source Lineage

- Candidate IDs: candidate_training_video_manually_reset_system_metrics
- Source ID: `training_video_day1`
- Source Type: `training_video`
