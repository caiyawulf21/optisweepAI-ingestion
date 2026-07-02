# Check For Missing Dimension Or Weight Data When Chutes Appear To Overfill

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_for_missing_dimension_or_weight_data_when_chutes_appear_to_overfill_v1` |
| Title | Check For Missing Dimension Or Weight Data When Chutes Appear To Overfill |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-backed diagnostic to determine whether apparent chute overfilling is explained by missing or incomplete dimension or weight data on the affected sort induct path. The source states tote fullness and chute close behavior are based on weight and dimensions in software, not local chute sensors or photo eyes.

## When To Use

Use when chutes appear to be overfilling and you need to verify whether the behavior is consistent with missing or incomplete dimension or weight data rather than a chute-sensor issue.

## Do Not Use For

* Do not use this runbook to diagnose local chute sensor or photo-eye faults for tote fullness behavior, because the source states there are no chute sensors or photo eyes for this function.
* Do not use this runbook as a recovery procedure; the source supports diagnosis and escalation only, not corrective recovery steps.

## Safety And Operational Notes

* This source describes a diagnostic review only and does not provide physical intervention steps.
* Do not assume a local chute sensor fault from this source, because the source states tote fullness behavior is not driven by chute sensors or photo eyes.

## Access Or Tools Needed

* Access to system data or views showing received dimension and weight data
* Source-backed understanding of tote fullness dependency on dimension and weight data

## Related Operational Context

* ctx_training_video_weight_dimension_data_dependency_v1
* ctx_training_video_tote_fullness_volumetric_thresholds_v1

## Procedure Steps

### Step 1 — Identify the apparent overfill condition

**Responsible role:** L2_support

**Instruction:**
Identify the condition where chutes appear to be overfilling on the affected area or sort induct path.

**Expected result:**
A specific apparent chute overfill condition is identified for diagnostic review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0014_oh_so_parcel_was_sort_down_primary_00_23_58_000](assets/fa4202ba8c63f0d4.jpg)

*Review the slide context showing tote fullness calculation and chute unavailable behavior when a tote is considered full.*


**Stop or Escalate If:**

* The overfill symptom cannot be tied to a specific affected path or chute for review.

---

### Step 2 — Confirm fullness logic depends on weight and dimensions

**Responsible role:** L2_support

**Instruction:**
Verify from the source-backed system understanding that chute fullness decisions rely on dimension and weight data rather than photo eyes or other chute sensors.

**Expected result:**
You confirm that the source attributes tote fullness and chute close behavior to software using weight and dimensions, not local chute sensors.

**Screens / Images:**

![artifact_training_video_training_video_day1_0014_oh_so_parcel_was_sort_down_primary_00_23_58_000](assets/fa4202ba8c63f0d4.jpg)

*Look for the slide and transcript context describing software tote fullness calculation using weight and dimensions and the absence of chute sensors/photo eyes.*


**Stop or Escalate If:**

* Others are pursuing a local chute sensor or photo-eye fault theory based on this source alone.

---

### Step 3 — Check whether dimension and weight data are being received

**Responsible role:** L2_support

**Instruction:**
Check whether dimension data and weight data are being received for the affected sort induct path.

**Expected result:**
You determine whether both dimension and weight data are present for the affected path.

**Screens / Images:**

![artifact_training_video_training_video_day1_0011_so_before_a_parcel_reaches_our_primary_00_17_45_500](assets/970fceec39fd2c18.jpg)

*Review the parcel lifecycle context showing upstream messages and dimensional data before and at sorter induction.*

![artifact_training_video_training_video_day1_0013_so_why_is_this_potential_and_primary_00_20_02_000](assets/dea6e687312f24c7.jpg)

*Review the induction messaging context showing dimensions provided in upstream messages and dimensional data on the sorter.*

![artifact_training_video_training_video_day1_0014_oh_so_parcel_was_sort_down_primary_00_23_58_000](assets/fa4202ba8c63f0d4.jpg)

*Review the tote fullness context showing software updates tote cube/fullness using dimension and weight data from sort induct.*


**Stop or Escalate If:**

* Dimension data is missing for the affected path.
* Weight data is missing for the affected path.

---

### Step 4 — Identify specific missing or incomplete data elements

**Responsible role:** L2_support

**Instruction:**
If data is incomplete, note the specific missing elements described by the source example, such as missing weight or incomplete dimension values.

**Expected result:**
The missing or incomplete data elements are documented clearly enough for escalation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0014_oh_so_parcel_was_sort_down_primary_00_23_58_000](assets/fa4202ba8c63f0d4.jpg)

*Use the slide context on fullness calculation and nearby transcript discussing issues caused by missing dimension or weight data.*


**Stop or Escalate If:**

* Any required dimension data is missing.
* Weight data is missing.
* Dimension values appear incomplete for the affected path.

---

### Step 5 — Record findings and escalate if indicated

**Responsible role:** L2_support

**Instruction:**
Record that missing dimension or weight data may explain the overfill behavior and preserve the observed data gap for escalation.

**Expected result:**
A source-backed diagnostic finding is documented, including whether missing or incomplete data plausibly explains the symptom.

**Screens / Images:**

![artifact_training_video_training_video_day1_0014_oh_so_parcel_was_sort_down_primary_00_23_58_000](assets/fa4202ba8c63f0d4.jpg)

*Reference the source slide that ties tote fullness and chute closure behavior to weight and dimensions.*


**Stop or Escalate If:**

* Dimension or weight data is missing or incomplete for the affected path.
* Overfill behavior persists even though dimension and weight data appear present, because the source does not provide further recovery steps.

---

## Success Criteria

* You determine whether missing or incomplete dimension or weight data is a plausible source-backed explanation for the apparent chute overfill behavior.
* Any observed data gap is documented for escalation.

## Failure Conditions

* Dimension data is missing for the affected path.
* Weight data is missing for the affected path.
* Dimension values are incomplete for the affected path.
* Overfill behavior persists even though dimension and weight data appear present.

## Escalation Guidance

* Escalate if dimension or weight data is missing or incomplete for the affected path.
* Escalate if overfill behavior persists even though dimension and weight data appear present, because the source does not provide further recovery steps.
* Do not escalate this source finding as a chute-sensor or photo-eye fault based on this source alone, because the source states there are no chute sensors or photo eyes for this function.

## Missing Details / Known Gaps

* The source does not specify the exact system screen, query, or interface to use when checking received dimension and weight data.
* The source does not provide exact field names, acceptable value formats, or thresholds for determining incomplete data beyond the general examples of missing dimension or weight data.
* The source does not provide corrective recovery steps after identifying the data gap.
* The source does not provide a time estimate for completing this diagnostic.

## Source Lineage

- Candidate IDs: candidate_training_video_check_missing_dimension_weight_data_when_chutes_overfill
- Source ID: `training_video_day1`
- Source Type: `training_video`
