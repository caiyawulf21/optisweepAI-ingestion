# Check Lane Activity for missing dimension data (Scandata/Induct/SortConf) and identify AI01 not sending data

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_lane_activity_missing_dimension_data_ai01_v1` |
| Title | Check Lane Activity for missing dimension data (Scandata/Induct/SortConf) and identify AI01 not sending data |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `charging_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Lane Activity view/record that captures Scandata, Induct, and SortConf to determine whether missing dimension data is occurring. If AI01 is not sending any data, the system uses default dimensions, which the source ties to overfilling.

## When To Use

Use when you suspect missing dimension data is contributing to default dimensions being applied (e.g., symptoms consistent with overfilling) and you need to confirm whether AI01 is not sending data by checking Lane Activity evidence for Scandata, Induct, and SortConf.

## Do Not Use For

* Do not use this procedure to confirm the root cause beyond the AI01 no-data condition; if Lane Activity shows dimension data present for AI01, escalate to broader troubleshooting.

## Access Or Tools Needed

* Lane Activity view/record that captures Scandata, Induct, and SortConf
* Ability to view AI01-related Lane Activity records

## Related Operational Context

* ctx_training_video_lane_activity_dimension_data_v1

## Procedure Steps

### Step 1 — Open the Lane Activity view/record that records Scandata, Induct, and SortConf

**Responsible role:** L1_support

**Instruction:**
Open the Lane Activity view/record referenced by the source that records Scandata, Induct, and SortConf, and navigate to the area where AI01-related entries would be visible.

**Expected result:**
Lane Activity evidence is visible showing the sections/fields for Scandata, Induct, and SortConf for the relevant lane/work area.

---

### Step 2 — Locate dimension-data entries and confirm whether dimension data is missing

**Responsible role:** L1_support

**Instruction:**
In the Lane Activity view/record, locate the entries related to dimension data and confirm whether dimension data is missing (i.e., the evidence indicates missing dimension data for the relevant items/messages).

**Expected result:**
Lane Activity evidence indicates missing dimension data for the items/messages under investigation.

---

### Step 3 — Check whether AI01 is “not sending any data”

**Responsible role:** L1_support

**Instruction:**
Within the Lane Activity evidence, check the AI01-related entries and verify whether AI01 is “not sending any data” (i.e., there is no data being sent in the Lane Activity evidence for AI01).

**Expected result:**
AI01-related Lane Activity evidence shows a no-data condition consistent with “AI01 was not sending any data.”

---

### Step 4 — If AI01 is not sending data, confirm default dimensions are being used and tie to overfilling

**Responsible role:** L1_support

**Instruction:**
If the Lane Activity evidence confirms AI01 is not sending any data, interpret the impact as the system using default dimensions (default dims) and note that the source associates this with overfilling.

**Expected result:**
Your findings support the chain: AI01 no-data condition → missing dimension data → system uses default dimensions (default dims) → overfilling risk/occurrence as described by the source.

---

## Success Criteria

* Lane Activity evidence shows missing dimension data conditions.
* AI01-related Lane Activity evidence indicates AI01 is not sending any data.
* Findings align with the source-described impact: default dimensions are used and this is associated with overfilling.

## Failure Conditions

* Lane Activity indicates missing dimension data.
* AI01-related Lane Activity evidence indicates AI01 is not sending any data.
* If AI01 has dimension data present, do not conclude default-dims/overfilling cause from this procedure.

## Escalation Guidance

* If Lane Activity shows dimension data present for AI01, do not assume the default-dims/overfilling cause from this source; escalate to broader troubleshooting.

## Missing Details / Known Gaps

* The source does not name the exact live HMI/web screen or provide field labels beyond the named concepts: Scandata, Induct, SortConf, and AI01.
* The source does not provide explicit UI field names/values to use as a pass/fail indicator for “AI01 not sending any data” beyond the described no-data condition.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_check_lane_activity_missing_dimension_data_ai01
- Source ID: `training_video_day2`
- Source Type: `training_video`
