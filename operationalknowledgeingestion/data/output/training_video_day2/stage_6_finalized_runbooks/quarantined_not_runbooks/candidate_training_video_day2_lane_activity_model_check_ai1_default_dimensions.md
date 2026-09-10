# Check Lane Activity Model for missing AI1 data causing default dimensions usage

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_lane_activity_model_missing_ai1_default_dimensions_v1` |
| Title | Check Lane Activity Model for missing AI1 data causing default dimensions usage |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Lane Activity Model to confirm whether AI1 is not sending data; the source example states this missing AI1 data can cause the system to use default dimensions.

## When To Use

When investigating a case where the system appears to be using default dimensions and you suspect AI1 is not providing recorded data, use the Lane Activity Model to verify AI1 data presence/absence.

## Access Or Tools Needed

* Lane Activity Model access (as referenced in the source)
* Ability to view AI1-related data/recording status and dimension outputs within the Lane Activity Model UI

## Related Operational Context

* ctx_training_video_lane_activity_model_ai1_data_v1

## Procedure Steps

### Step 1 — Open the Lane Activity Model view referenced by the source

**Responsible role:** L2_support

**Instruction:**
Open the Lane Activity Model view referenced in the source segment (Training Video Day 2, Segment 0058).

**Expected result:**
The Lane Activity Model view is open and ready for checking AI1-related data/recording status.

---

### Step 2 — Locate the AI1-related data/recording status within the Lane Activity Model

**Responsible role:** L2_support

**Instruction:**
Within the Lane Activity Model view, locate the AI1-related data/recording status area/indicator.

**Expected result:**
You have found the AI1-related indicator/recording status within the Lane Activity Model UI.

---

### Step 3 — Verify whether AI1 is sending data

**Responsible role:** L2_support

**Instruction:**
Check the AI1-related status/data in the Lane Activity Model to determine whether AI1 is sending any data (i.e., whether it is recording/sending data).

**Expected result:**
You determine whether AI1 is sending data or not sending data based on the Lane Activity Model AI1 status/data.

---

### Step 4 — Correlate missing AI1 data with default dimensions usage

**Responsible role:** L2_support

**Instruction:**
If the Lane Activity Model indicates AI1 is not sending data, confirm that the system behavior you are investigating aligns with default dimensions being used (as described in the source example).

**Expected result:**
When AI1 is not sending data, your investigation outcome matches the source example that default dimensions are used.

**Stop or Escalate If:**

* If AI1 data appears present in the Lane Activity Model but dimensions are still default, escalate for deeper investigation beyond the source-described check.

---

## Success Criteria

* You can determine from the Lane Activity Model whether AI1 is sending data or not sending data.
* In the AI1-missing case, your troubleshooting correlation supports that default dimensions are being used (per the source example).

## Failure Conditions

* AI1 status cannot be found or interpreted in the Lane Activity Model UI.
* AI1 appears to be sending data, yet dimensions are still default (requires escalation beyond this check).

## Escalation Guidance

* If AI1 data appears present in the Lane Activity Model but dimensions are still default, escalate for deeper investigation beyond the source-described check.

## Missing Details / Known Gaps

* The source does not provide concrete navigation steps or specific UI field/label names for the Lane Activity Model AI1 status indicator.
* The source does not provide a named UI location/label for where default dimensions usage is displayed/confirmed in the live Lane Activity Model or related UI.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_lane_activity_model_check_ai1_default_dimensions
- Source ID: `training_video_day2`
- Source Type: `training_video`
