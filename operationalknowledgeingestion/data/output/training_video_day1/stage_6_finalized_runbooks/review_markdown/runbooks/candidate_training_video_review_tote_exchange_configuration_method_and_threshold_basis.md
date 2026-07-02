# Review Whether Tote Exchange Configuration Uses Count, Cube, Or Cube And Count Threshold Basis

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_review_whether_tote_exchange_configuration_uses_count_cube_or_cube_and_count_threshold_basis_v1` |
| Title | Review Whether Tote Exchange Configuration Uses Count, Cube, Or Cube And Count Threshold Basis |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Tote Exchange Settings Aveva API page to identify which documented Method option is configured for tote exchange evaluation. The source supports reading the Method field and confirming that the screen includes count-based and cube-based threshold categories, but it does not define calculation logic beyond the listed options.

## When To Use

Use this runbook when you need to verify from the Tote Exchange Settings interface whether tote exchange is configured to use Count, Cube, or Cube and Count as the documented method basis.

## Do Not Use For

* Do not use this runbook to change Tote Exchange Settings.
* Do not use this runbook to infer undocumented calculation logic for the Cube and Count option.
* Do not use this runbook to determine save, edit, or update actions because the source does not provide them.

## Safety And Operational Notes

* This source-supported procedure is a view/reference activity only.
* Do not infer exact calculation behavior for the combined method because the source only states that it allows a mixture of both.

## Access Or Tools Needed

* Access to the Tote Exchange Settings interface
* Aveva API page view

## Related Operational Context

* ctx_training_video_tote_exchange_settings_interface_v1
* ctx_training_video_tote_exchange_method_options_v1
* ctx_training_video_tote_exchange_threshold_categories_v1

## Procedure Steps

### Step 1 — Open or view the Tote Exchange Settings interface

**Responsible role:** L1_support

**Instruction:**
Open or view the Tote Exchange Settings interface on the Aveva API page.

**Expected result:**
The Tote Exchange Settings screen is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*The Tote Exchange Settings page with the Method field and threshold entries visible.*


**Stop or Escalate If:**

* Escalate if the Tote Exchange Settings interface is not available for viewing.

---

### Step 2 — Locate the Method field

**Responsible role:** L1_support

**Instruction:**
Locate the Method field on the Tote Exchange Settings screen.

**Expected result:**
The Method field is identified on the interface.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*The Method field area listing the available method choices.*


**Stop or Escalate If:**

* Escalate if the Method field is missing.

---

### Step 3 — Read the configured Method option

**Responsible role:** L1_support

**Instruction:**
Read the displayed Method value and compare it to the documented choices: Count, Cube, or Cube and Count.

**Expected result:**
The configured method basis is identified as one of the documented options.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*The selected Method value and the listed options Count, Cube, and Cube and Count.*


**Stop or Escalate If:**

* Escalate if the Method field shows a value not documented in the source.

---

### Step 4 — Confirm the related threshold categories on the screen

**Responsible role:** L1_support

**Instruction:**
Use the surrounding threshold fields to confirm that the screen includes count-based and cube-based threshold entries referenced by the source.

**Expected result:**
The screen shows threshold categories for cube and count, including pickup, priority, and close entries.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*Threshold fields labeled for cube and count, including pickup, priority, and close.*


**Stop or Escalate If:**

* Escalate if the threshold categories shown on the screen do not include the documented count-based and cube-based entries.

---

### Step 5 — Record the configured threshold basis

**Responsible role:** L1_support

**Instruction:**
Record which threshold basis is configured without inferring any undocumented software behavior beyond the listed options.

**Expected result:**
The configured basis is recorded as Count, Cube, or Cube and Count.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*The Method field value used as the basis for the recorded result.*


**Stop or Escalate If:**

* Escalate if the Method field is missing or shows a value not documented in the source.
* Stop and avoid further interpretation if determining the result would require inferring exact combined-method calculation logic.

---

## Success Criteria

* The Tote Exchange Settings interface is viewed successfully.
* The Method field is located and read.
* The configured method is identified as Count, Cube, or Cube and Count.
* The surrounding threshold categories for cube-based and count-based entries are confirmed on the screen.
* The result is recorded without inferring undocumented behavior.

## Failure Conditions

* The Tote Exchange Settings interface cannot be accessed for viewing.
* The Method field is missing, unreadable, or not visible.
* The Method field shows a value not documented in the source.
* The threshold categories on the screen do not align with the documented cube and count threshold entries.
* Determining the result would require unsupported inference about software logic.

## Escalation Guidance

* Escalate if the Method field is missing or shows a value not documented in the source.
* Escalate if the Tote Exchange Settings screen does not show the documented threshold categories.
* Do not infer exact calculation logic for the combined method because the source only states that it allows a mixture of both.

## Missing Details / Known Gaps

* The source does not provide navigation steps to reach the Tote Exchange Settings page.
* The source does not provide edit, save, or update actions for the Method field.
* The source does not define exact calculation logic for the Cube and Count method.
* The source does not provide a time estimate for this review activity.
* The source does not specify production-stop or LOTO requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_review_tote_exchange_configuration_method_and_threshold_basis
- Source ID: `training_video_day1`
- Source Type: `training_video`
