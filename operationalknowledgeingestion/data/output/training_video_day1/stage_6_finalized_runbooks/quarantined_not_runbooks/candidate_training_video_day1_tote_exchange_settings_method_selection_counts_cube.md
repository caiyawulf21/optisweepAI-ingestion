# Confirm Tote Exchange Settings Method (Count vs Cube vs Cube and Count) for tote exchange evaluation

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_confirm_tote_exchange_settings_method_count_cube_v1` |
| Title | Confirm Tote Exchange Settings Method (Count vs Cube vs Cube and Count) for tote exchange evaluation |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sort_lifecycle_state` |
| Access Surface | None |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify the selected Tote Exchange Settings Method (Count, Cube, or Cube and Count) in the Aveva API Tote Exchange Settings interface, and confirm whether tote exchange evaluation is based on counts, cube, or a mixture of both.

## When To Use

Use when you need to confirm which tote exchange evaluation basis is configured in Tote Exchange Settings—counts, cube, or a mixture—because the Method selection determines how thresholds are applied.

## Access Or Tools Needed

* Aveva API access to the Tote Exchange Settings interface/page
* Method field on the Tote Exchange Settings page

## Related Operational Context

* ctx_training_video_tote_exchange_method_options_v1

## Procedure Steps

### Step 1 — Open the Tote Exchange Settings Aveva API page

**Responsible role:** L1_support

**Instruction:**
Open the Tote Exchange Settings Aveva API page/interface.

**Expected result:**
The Tote Exchange Settings page is visible with the Method field and the threshold fields grouped by Cube and Count.

---

### Step 2 — Read the selected Method option (Count, Cube, or Cube and Count)

**Responsible role:** L1_support

**Instruction:**
Find the Method field on the Tote Exchange Settings page and read the currently selected option.

**Expected result:**
You identify the selected Method as one of: Count, Cube, or Cube and Count.

**Stop or Escalate If:**

* If the Method field does not show one of the documented options (Count/Cube/Cube and Count), stop and escalate to the project team/UPS/UAT owner for clarification on the correct configuration interface.

---

### Step 3 — Interpret evaluation basis based on Method selection

**Responsible role:** L1_support

**Instruction:**
Based on the Method selection you observed, determine whether tote exchange evaluation is based on counts, cube, or a mixture of both.

**Expected result:**
You can state the evaluation basis consistent with the Method selection: Count => counts; Cube => cube; Cube and Count => mixture of both.

---

### Step 4 — Record Method selection and relevant threshold category fields

**Responsible role:** L1_support

**Instruction:**
Record the Method selection and the relevant threshold category fields shown on the Tote Exchange Settings page (Cube Threshold Pickup/Priority/Close and/or Count Threshold Pickup/Priority/Close) so the configuration matches the selected method.

**Expected result:**
You have documented the Method selection and the corresponding threshold fields visible on the page for Cube and/or Count.

---

## Success Criteria

* Method selection is identified as Count, Cube, or Cube and Count from the Tote Exchange Settings page.
* The evaluation basis (counts, cube, or mixture) is correctly stated based on the Method selection.
* The Method selection and the relevant threshold category fields (Cube and/or Count threshold Pickup/Priority/Close) are recorded.

## Failure Conditions

* Method field does not show one of the documented options (Count/Cube/Cube and Count).
* Threshold fields cannot be found/recorded in the expected Cube/Count grouped categories on the page.

## Escalation Guidance

* If the Method field does not show one of the documented options (Count/Cube/Cube and Count), stop and escalate to the project team/UPS/UAT owner for clarification on the correct configuration interface.

## Missing Details / Known Gaps

* The packet does not provide explicit navigation steps (menu path/URL) to reach the Tote Exchange Settings Aveva API page; it only states to open the page/interface.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_tote_exchange_method_options_v1
- Source ID: `training_video_day1`
- Source Type: `training_video`
