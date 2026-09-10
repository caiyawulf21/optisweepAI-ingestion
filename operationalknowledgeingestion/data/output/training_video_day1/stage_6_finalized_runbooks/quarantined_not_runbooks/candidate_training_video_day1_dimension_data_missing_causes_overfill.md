# Diagnose overfill indications caused by missing dimension data (no photo eyes)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_diagnose_overfill_indications_missing_dimension_data_no_photo_eyes_v1` |
| Title | Diagnose overfill indications caused by missing dimension data (no photo eyes) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `apidog`, `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `charging_abnormal`, `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this diagnostic when chute/tote fullness appears to be at/over thresholds (e.g., chutes closing or totes marked full) but the system does not have chute photo eyes/sensors. The source explains that fullness/closure decisions are driven by received weight and dimensions; if dimension data is missing or incomplete for sort induct/auto inducts, chutes can appear to overfill.

## When To Use

When support observes overfill/threshold behavior (e.g., chutes closing due to tote fullness) and the site/system is described as having no photo eyes/sensors at the chute, so fullness is based on weighted dimensions. Use to validate whether missing or incomplete dimension/weight data for the sort induct/auto inducts is the cause of the overfill indications.

## Do Not Use For

* Do not use this procedure as the only troubleshooting path when dimension data is confirmed complete; the source only provides the data-missing explanation and does not provide corrective steps beyond escalation.

## Access Or Tools Needed

* Access to the live system view/log/API area that shows whether dimension data is being received for the sort induct / auto inducts (the source references that the team can see they are 'not getting dim data' on their system).

## Related Operational Context

* ctx_training_video_weight_dimension_data_dependency_v1

## Procedure Steps

### Step 1 — Confirm the source constraint: chute fullness is based on weighted dimensions (no photo eyes/sensors)

**Responsible role:** L1_support

**Instruction:**
On the live system, treat chute/tote fullness and chute close behavior as driven by received weight and dimensions (not local chute photo eyes/sensors).

**Expected result:**
You can proceed with the diagnostic assumption that fullness/closure thresholds are computed from received weight/dimensions, consistent with the source statement that there are no photo eyes/sensors at the chute.

---

### Step 2 — Check whether dimension data is being received for the sort induct / auto inducts

**Responsible role:** L1_support

**Instruction:**
Using the live system view/log/API area referenced by the source (where the team can see they are 'not getting dim data'), check whether dimension data is being received for the relevant sort induct / auto inducts that feed the chute/tote fullness calculation.

**Expected result:**
You identify whether dimension data is missing entirely or partially (e.g., height/length present but a second length missing, and/or weight missing) for the affected induct(s).

---

### Step 3 — If dimension data is missing, link the overfill indication to missing/incomplete dimension/weight data

**Responsible role:** L1_support

**Instruction:**
When you confirm missing dimension data for the affected induct(s), document that the source explanation attributes the overfill indications to missing/incomplete dimension/weight data (not chute photo eyes/sensors).

**Expected result:**
Your diagnostic outcome states that the overfill/threshold behavior is consistent with missing dimension data for the sort induct/auto inducts.

**Stop or Escalate If:**

* Escalate if dimension data appears complete yet overfill behavior persists (source provides only the missing-data explanation and no further corrective steps).

---

### Step 4 — Handle partial dimension data: confirm which fields are missing (e.g., second length, weight)

**Responsible role:** L1_support

**Instruction:**
If dimension data is partially present, identify which specific dimension/weight components are missing (e.g., height/length present but second length missing; weight missing on other auto inducts).

**Expected result:**
You can describe the partial-data pattern that matches the source example and conclude it is consistent with overfill indications.

---

## Success Criteria

* You confirm that chute/tote fullness behavior is driven by received weight/dimensions (no photo eyes/sensors at the chute).
* You determine whether dimension data is missing or incomplete for the relevant sort induct/auto inducts feeding the overfill symptom.
* You produce a diagnostic conclusion linking overfill indications to missing/incomplete dimension/weight data, consistent with the source explanation.

## Failure Conditions

* Dimension data is missing or incomplete, and overfill indications occur (source-supported failure mode).
* Dimension data appears complete yet overfill behavior persists (candidate escalation trigger).

## Escalation Guidance

* Escalate if dimension data appears complete yet overfill behavior persists, because the source only provides the missing-data explanation and does not provide further corrective steps.

## Missing Details / Known Gaps

* The candidate notes that the source does not name the exact live dashboard/log where 'not getting dim data' is visible. This runbook therefore cannot specify the exact RMS/DB/API screen/table to check for dimension reception.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_dimension_data_missing_causes_overfill
- Source ID: `training_video_day1`
- Source Type: `training_video`
