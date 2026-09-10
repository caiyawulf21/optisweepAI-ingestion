# Use IgnitionLaneActivityModel data in “MDI Support chat for Haslet” to troubleshoot lane/package activity

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_ignitionlaneactivitymodel_mdi_support_chat_haslet_v1` |
| Title | Use IgnitionLaneActivityModel data in “MDI Support chat for Haslet” to troubleshoot lane/package activity |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `tipper_hmi`, `wcs_sql` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Ignition-based “MDI Support chat for Haslet” screen to gather evidence from the lane activity table that references [dbo].[IgnitionLaneActivityModel]. Focus on which lane/package records are present and what the table shows for Message, PackageClassification, and MissingDimensionData (plus sorter-side and sort status fields such as SorterSide* and NewSort/SortConf/SortCont) to support troubleshooting.

## When To Use

When you need troubleshooting evidence about lane/package activity visible in the “MDI Support chat for Haslet” screen, specifically the lane activity table content backed by [dbo].[IgnitionLaneActivityModel].

## Do Not Use For

* Do not use this as a complete runbook to resolve the underlying issue end-to-end; the source frames this screen as troubleshooting/evidence gathering rather than a full resolution procedure.

## Access Or Tools Needed

* Access to the “MDI Support chat for Haslet” screen (Ignition-based UI as shown in the training frame).

## Related Operational Context

* ctx_training_video_mdi_support_chat_haslet_view_v1
* ctx_training_video_ignition_lane_activity_model_reference_v1
* ctx_training_video_lane_activity_table_columns_v1
* ctx_training_video_sorter_side_status_values_v1

## Visual References

![artifact_training_video_training_video_day2_0057_but_this_is_it_not_for_primary_03_23_52_500](assets/c02be26d0fda2a25.jpg)

*Frame showing the “MDI Support chat for Haslet” interface with the table referencing [dbo].[IgnitionLaneActivityModel] and visible column headers/row values (e.g., SorterSide2a/NewSort and SortConf/SortCont, plus Message, PackageClassification, MissingDimensionData).*

![artifact_training_video_training_video_day2_0059_and_so_you_can_kind_of_primary_03_28_03_000](assets/a359db66d5e12322.jpg)

*Frame showing the same “MDI Support chat for Haslet” table with additional visible columns including MissingDimensionData and related message/classification fields.*

## Procedure Steps

### Step 1 — Open the “MDI Support chat for Haslet” screen

**Responsible role:** L1_support

**Instruction:**
Open the “MDI Support chat for Haslet” screen in the Ignition-based UI.

**Expected result:**
The “MDI Support chat for Haslet” interface is displayed, including a table that references [dbo].[IgnitionLaneActivityModel].

---

### Step 2 — Locate the lane activity table that references [dbo].[IgnitionLaneActivityModel]

**Responsible role:** L1_support

**Instruction:**
On the “MDI Support chat for Haslet” screen, find the table content that includes the reference “[dbo].[IgnitionLaneActivityModel]”.

**Expected result:**
The table area is located and the “[dbo].[IgnitionLaneActivityModel]” reference is visible in the screen content.

---

### Step 3 — Review the table row fields for the relevant lane/package records

**Responsible role:** L1_support

**Instruction:**
In the lane activity table, review the row fields for the relevant record(s), focusing on the visible column headers/fields: date, SorterName, SortGuid, Zone, LaneName, Packaged/TrackingNumber, Length/Width/Height/Weight, Cube, Message, PackageClassification, and MissingDimensionData.

**Expected result:**
For the suspected lane/package, you can read the row values across the listed columns (including Message, PackageClassification, and MissingDimensionData).

**Stop or Escalate If:**

* If the expected lane/package records are not present in the table, stop and escalate to deeper support/troubleshooting beyond this screen.

---

### Step 4 — Check sorter-side and sort-related status fields for the suspected record(s)

**Responsible role:** L1_support

**Instruction:**
For the suspected lane/package record(s), read the sorter-side and sort-related fields shown in the rows, including SorterSide1a/SorterSide1b/SorterSide2a (as visible) and sort status-like values such as NewSort and SortConf/SortCont.

**Expected result:**
The suspected record(s) show sorter-side identifiers (SorterSide*) and sort status-like values (NewSort and/or SortConf/SortCont) that you can record for troubleshooting evidence.

---

### Step 5 — Record Message, PackageClassification, and MissingDimensionData for the relevant record(s)

**Responsible role:** L1_support

**Instruction:**
Record what the table shows for Message, PackageClassification, and MissingDimensionData for the relevant lane/package record(s) you identified.

**Expected result:**
You have captured the observable values from the table for Message, PackageClassification, and MissingDimensionData for the suspected record(s).

---

## Success Criteria

* The “MDI Support chat for Haslet” screen is opened and the lane activity table referencing [dbo].[IgnitionLaneActivityModel] is located.
* For the suspected lane/package record(s), the table row values for Message, PackageClassification, and MissingDimensionData are captured.
* For the same record(s), sorter-side and sort status-like fields (SorterSide* and NewSort/SortConf/SortCont as visible) are captured as additional evidence.

## Failure Conditions

* The expected lane/package record(s) are not present in the table.
* Message, PackageClassification, or MissingDimensionData values cannot be read/captured for the suspected record(s).

## Escalation Guidance

* If the expected lane/package records are not present in the table, stop and escalate to deeper support/troubleshooting beyond this screen (the source only indicates this is for troubleshooting, not a full runbook).

## Missing Details / Known Gaps

* The source packet does not provide explicit navigation steps (e.g., exact menu path) to reach the “MDI Support chat for Haslet” screen; it only states to open the named screen.
* The source packet does not specify how to filter/search within the table for a specific lane/package (no exact UI filter actions are provided).
* The source packet does not define the exact meaning/allowed values for Message, PackageClassification, or MissingDimensionData beyond their presence as fields in the table.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_mdi_support_chat_haslet_lane_activity_model
- Source ID: `training_video_day2`
- Source Type: `training_video`
