# Check IgnitionLaneActivityModel in SSMS for MissingDimensionData after a power flicker

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_ignitionlanemodel_missingdimensiondata_after_power_flicker_v1` |
| Title | Check IgnitionLaneActivityModel in SSMS for MissingDimensionData after a power flicker |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_system_faults` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `charging_abnormal`, `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use SSMS to inspect the lane activity database model/view [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel] and confirm whether the MissingDimensionData field is flagged for lane activity rows in the affected time window after a power flicker. This provides database evidence that upstream dimension data did not reboot properly.

## When To Use

Use when a power flicker occurred and you need to verify whether upstream dimension data failed to reboot properly, by checking the lane activity dataset for MissingDimensionData.

## Access Or Tools Needed

* SSMS
* WCS/Helix database access sufficient to view [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel]
* Ability to view fields/columns including MissingDimensionData, MissingInduct, ToteNotFound, Length, Width, Height, Weight, Cube

## Related Operational Context

* ctx_training_video_dimension_data_after_power_flicker_v1
* ctx_training_video_optisweep_support_boundary_dimensioner_guidance_v1
* ctx_training_video_ignition_lane_activity_model_dimension_flags_v1
* ctx_training_video_missing_dimension_data_status_field_v1

## Visual References

![artifact_training_video_training_video_day2_0060_they_they_had_a_power_flicker_primary_03_28_33_000](assets/d3061ef3fe825a42.jpg)

*Frame showing SSMS-style results for [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel] including fields MissingDimensionData, MissingInduct, ToteNotFound, and dimension fields (Length, Width, Height, Weight, Cube), plus lane activity rows with timestamp-like values.*

## Procedure Steps

### Step 1 — Open SSMS and connect to the database containing IgnitionLaneActivityHodel / IgnitionLaneActivityModel

**Responsible role:** L2_support

**Instruction:**
In SSMS, connect to the WCS/Helix database that contains the lane activity model/view named [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel].

**Expected result:**
You are connected in SSMS and can access the [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel] object.

**Stop or Escalate If:**

* If you cannot access the database/model/view, stop and escalate for database access/permissions troubleshooting.

---

### Step 2 — Locate IgnitionLaneActivityHodel / IgnitionLaneActivityModel and identify dimension-data-related fields

**Responsible role:** L2_support

**Instruction:**
In SSMS, locate the lane activity model/view named [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel] and ensure the result set includes the fields shown in the source OCR: MissingDimensionData, MissingInduct, ToteNotFound, and dimension fields Length, Width, Height, Weight, Cube.

**Expected result:**
The SSMS results show the columns/fields MissingDimensionData, MissingInduct, ToteNotFound, and dimension fields Length, Width, Height, Weight, Cube.

**Stop or Escalate If:**

* If MissingDimensionData is not present in the result set for this model/view, stop and escalate for deeper investigation of the correct lane activity model/view or schema.

---

### Step 3 — Filter to the affected time window after the power flicker

**Responsible role:** L2_support

**Instruction:**
In the SSMS results for [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel], filter/identify the lane activity rows for the affected time window after the power flicker using the timestamp-like values visible in the results (as shown in the source OCR).

**Expected result:**
You have identified one or more lane activity rows in the SSMS results whose timestamp-like values fall within the affected time window after the power flicker.

**Stop or Escalate If:**

* If you cannot isolate the affected time window, stop and escalate for guidance on the correct time basis/filters for this model/view.

---

### Step 4 — Check MissingDimensionData for the identified lane activity rows

**Responsible role:** L2_support

**Instruction:**
For the lane activity rows you identified in the affected time window, check the MissingDimensionData field to see whether it is present/flagged in the results.

**Expected result:**
You can point to lane activity rows in [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel] where MissingDimensionData is present/flagged for the post-flicker time window.

**Stop or Escalate If:**

* If the database does not show MissingDimensionData for the affected lane activity/time window, stop and escalate for deeper investigation.

---

### Step 5 — Communicate the database evidence that upstream dimension data did not reboot properly

**Responsible role:** L2_support

**Instruction:**
Using the observed SSMS evidence (rows where MissingDimensionData is flagged), communicate that the system is supposed to get dimension data, but the database indicates it is not for the affected post-flicker lane activity rows.

**Expected result:**
You can reference the specific lane activity rows and the MissingDimensionData field values/flagging that support the claim of missing dimension data after the power flicker.

**Stop or Escalate If:**

* If the evidence is ambiguous (e.g., MissingDimensionData cannot be tied to the post-flicker rows), stop and escalate for deeper investigation.

---

## Success Criteria

* In SSMS, for lane activity rows in the affected time window after the power flicker, MissingDimensionData is present/flagged in [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel].

## Failure Conditions

* MissingDimensionData is not flagged/present for the affected post-flicker lane activity rows.
* The SSMS result set does not expose MissingDimensionData (or the expected dimension fields) for [dbo].[IgnitionLaneActivityHodel] / [dbo].[IgnitionLaneActivityModel].

## Escalation Guidance

* If the database does not show MissingDimensionData for the affected lane activity/time window, stop and escalate for deeper investigation (the source only states that the database is used to confirm missing dimension data).
* If you cannot access the database/model/view or cannot isolate the affected time window, escalate for database access/interpretation support.

## Missing Details / Known Gaps

* The packet does not include the exact SSMS query text, the exact database name/server, or the specific filter logic used to select the affected time window.
* The packet does not define the exact value semantics for MissingDimensionData (e.g., whether it is 0/1, NULL, or a specific string) beyond being 'present/flagged' in the results.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_check_ignition_lane_activity_missing_dimension_data
- Source ID: `training_video_day2`
- Source Type: `training_video`
