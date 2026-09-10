# Use the Sort Confirmation support table to identify missing sort/dimension data (e.g., AIO one) by checking Length/Width/Height/Weight values

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_sort_confirmation_support_table_missing_dimension_data_v1` |
| Title | Use the Sort Confirmation support table to identify missing sort/dimension data (e.g., AIO one) by checking Length/Width/Height/Weight values |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Inspect the Sort Confirmation support table/view by filtering to “sort confirmation,” zooming in on the resulting rows, and checking the dimension-related fields (Length/Width/Height/Weight). A notable indicator called out in the source is when Width, Height, and Weight are all “1”; the source uses this pattern to identify that “AIO one” was not sending sort data or dimension data.

## When To Use

Use when you need to determine whether a specific source/package is not sending sort data or dimension data, using the dimension fields shown in the Sort Confirmation support table/view.

## Access Or Tools Needed

* Access to the sort confirmation support table/view shown in the source frame
* Ability to apply the “sort confirmation” filter in that view
* Ability to zoom in so the table columns (Length/Width/Height/Weight and related fields) are readable

## Related Operational Context

* ctx_training_video_sort_confirmation_dimension_data_view_v1
* ctx_training_video_dimension_fields_default_one_pattern_v1
* ctx_training_video_aio1_missing_sort_or_dimension_data_v1
* ctx_training_video_missing_dimension_data_flag_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0059_and_so_you_can_kind_of_primary_03_28_03_000](assets/a359db66d5e12322.jpg)

*Sort confirmation support table/view with columns including Zone, LaneName, PackageUid, TrackingNumber, Length, Width, Height, Weight, Cube, Toteld, Message, PackageClassification, MissingDimensionData, MissingInduct, ToteNotfound, Diverted, OffTheEnd, Recirc; includes the “every width, height and weight was 1” pattern and the AIO one callout.*

## Procedure Steps

### Step 1 — Open the Sort Confirmation support table/view and locate the dimension-related columns

**Responsible role:** L1_support

**Instruction:**
Open the support table/view shown in the source that displays Sort Confirmation records. Ensure the table includes the dimension-related columns: Length, Width, Height, and Weight (along with other package fields such as Zone, LaneName, PackageUid, TrackingNumber, Cube, Toteld, Message, PackageClassification, MissingDimensionData, MissingInduct, Diverted, OffTheEnd, and Recirc).

**Expected result:**
You can see the Sort Confirmation support table/view with the columns Length, Width, Height, and Weight visible for the displayed rows.

**Stop or Escalate If:**

* If the table does not show the dimension-related columns (Length/Width/Height/Weight), stop and escalate for further investigation rather than proceeding.

---

### Step 2 — Filter the table to show “sort confirmation” records

**Responsible role:** L1_support

**Instruction:**
Apply the filter used in the source to focus on “sort confirmation” records in the support table/view.

**Expected result:**
The table is filtered so that the visible rows correspond to “sort confirmation” records.

**Stop or Escalate If:**

* If you cannot apply the “sort confirmation” filter or the table does not reflect sort confirmation records, stop and escalate for further investigation.

---

### Step 3 — Zoom in so Length/Width/Height/Weight values are readable

**Responsible role:** L1_support

**Instruction:**
Zoom in on the filtered results so the dimension fields (Length, Width, Height, Weight) and the related package/source identifiers are readable.

**Expected result:**
You can clearly read Width, Height, and Weight values for the visible filtered rows.

**Stop or Escalate If:**

* If you cannot zoom enough to read Width/Height/Weight values, stop and escalate or request assistance to view the table clearly.

---

### Step 4 — Check for the “Width/Height/Weight all equal to 1” pattern

**Responsible role:** L1_support

**Instruction:**
On the filtered, zoomed-in rows, verify whether every Width, Height, and Weight value is “1” across the visible results.

**Expected result:**
You observe that Width, Height, and Weight are all “1” for the visible filtered rows (or you observe that this pattern is not present).

**Stop or Escalate If:**

* If the “all 1” pattern is not present in the filtered results, stop and escalate for further investigation rather than assuming missing data.

---

### Step 5 — Identify the specific source/package row (AIO one) associated with missing sort/dimension evidence

**Responsible role:** L1_support

**Instruction:**
Within the filtered results, locate the row identified as “AIO one” in the source and confirm it aligns with the missing sort/dimension evidence (the source states AIO one was “not sending sort data or dimension data”).

**Expected result:**
You identify the row/source labeled as “AIO one” in the filtered table and associate it with the missing sort/dimension evidence described by the source.

**Stop or Escalate If:**

* If you cannot identify the AIO one row in the filtered results, stop and escalate for further investigation.

---

### Step 6 — Communicate the finding that sort/dimension data is missing for the identified source/package

**Responsible role:** L1_support

**Instruction:**
Using the observed evidence (the “all 1” dimension pattern and the row identified as AIO one), communicate that sort/dimension data is missing for that source/package.

**Expected result:**
You can clearly state which source/package row (AIO one) is implicated and what observable dimension pattern supports the conclusion (Width/Height/Weight all “1” in the filtered sort confirmation records).

**Stop or Escalate If:**

* If the filtered results do not support the “all 1” pattern or the AIO one row cannot be identified, do not communicate missing-data as a conclusion; stop and escalate for further investigation.

---

## Success Criteria

* You can point to filtered Sort Confirmation records where Width, Height, and Weight are all “1.”
* You identify the specific row/source called out as “AIO one” in the filtered results as the implicated source for missing sort/dimension data.

## Failure Conditions

* The filtered Sort Confirmation view does not show the expected dimension columns/values (Length/Width/Height/Weight).
* The “all 1” pattern is not present in the filtered results.
* The AIO one row cannot be identified in the filtered results.

## Escalation Guidance

* If the filtered sort confirmation view does not show the expected dimension columns/values or the “all 1” pattern is not present, stop and escalate for further investigation rather than assuming missing data.
* If you cannot identify the AIO one row in the filtered results, stop and escalate for further investigation.

## Missing Details / Known Gaps

* The source does not name the exact application/module name or the specific UI control labels for applying the “sort confirmation” filter; steps are grounded only in the described filter behavior and visible table columns.

## Source Lineage

- Candidate IDs: candidate_training_video_sort_confirmation_filter_check_missing_dimension_data
- Source ID: `training_video_day2`
- Source Type: `training_video`
