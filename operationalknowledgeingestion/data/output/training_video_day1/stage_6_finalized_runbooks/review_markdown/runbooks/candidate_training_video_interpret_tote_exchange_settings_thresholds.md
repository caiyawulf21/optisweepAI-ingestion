# Interpret Tote Exchange Settings Threshold Fields And Method Options

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_tote_exchange_settings_threshold_fields_and_method_options_v1` |
| Title | Interpret Tote Exchange Settings Threshold Fields And Method Options |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Tote Exchange Settings interface on the Aveva API page to identify the threshold field groups, method options, and weight-related parameters shown in the training source. This runbook is limited to viewing and documenting what is present on the screen.

## When To Use

Use when you need to verify or document which tote exchange threshold categories, method selections, and weight-related fields are shown on the Tote Exchange Settings screen in the source material.

## Do Not Use For

* Do not use this runbook to change Tote Exchange Settings.
* Do not use this runbook to infer undocumented threshold meanings, calculations, or corrective actions.
* Do not use this runbook as authority for queue threshold field names on the screen when those field names are not shown in the provided OCR evidence.

## Safety And Operational Notes

* This runbook is limited to screen interpretation and documentation from the source.
* Do not invent undocumented meanings, calculations, thresholds, or corrective actions from this source alone.

## Access Or Tools Needed

* Access to the Tote Exchange Settings interface
* Aveva API page view
* Source screenshot or training material for comparison

## Related Operational Context

* ctx_training_video_tote_exchange_settings_interface_v1
* ctx_training_video_tote_exchange_threshold_categories_v1
* ctx_training_video_tote_exchange_method_options_v1
* ctx_training_video_tote_exchange_weight_parameters_v1

## Procedure Steps

### Step 1 — Open or view the Tote Exchange Settings interface

**Responsible role:** L1_support

**Instruction:**
Open or view the Tote Exchange Settings interface on the Aveva API page, or use the referenced training screenshot if direct screen access is not being used.

**Expected result:**
The Tote Exchange Settings interface is visible for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*Overall Tote Exchange Settings interface and listed threshold, method, and weight fields.*


**Stop or Escalate If:**

* The screen does not show the documented Tote Exchange Settings interface.
* The available screen cannot be matched to the source screenshot.

---

### Step 2 — Identify the threshold categories discussed by the source

**Responsible role:** L1_support

**Instruction:**
Identify the tote exchange threshold categories shown or discussed by the source. Note pickup, priority, and close from the screen field names, and note that the transcript also mentions queue as part of the threshold discussion.

**Expected result:**
The threshold categories documented from the source are captured without adding unsupported interpretations.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*Threshold field labels showing Pickup, Priority, and Close; compare with transcript mention of queue.*


**Stop or Escalate If:**

* The screen does not show the documented threshold categories described in the source.
* There is pressure to treat queue as a confirmed screen field name without source screen evidence.

---

### Step 3 — Locate cube threshold fields

**Responsible role:** L1_support

**Instruction:**
Locate the cube-based threshold fields on the screen: Cube Threshold Pickup, Cube Threshold Priority, and Cube Threshold Close.

**Expected result:**
All documented cube threshold field names are identified from the source screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*Cube Threshold Pickup, Cube Threshold Priority, and Cube Threshold Close field labels.*


**Stop or Escalate If:**

* The screen does not show the documented cube threshold fields.

---

### Step 4 — Locate count threshold fields

**Responsible role:** L1_support

**Instruction:**
Locate the count-based threshold fields on the screen: Count Threshold Pickup, Count Threshold Priority, and Count Threshold Close.

**Expected result:**
All documented count threshold field names are identified from the source screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*Count Threshold Pickup, Count Threshold Priority, and Count Threshold Close field labels.*


**Stop or Escalate If:**

* The screen does not show the documented count threshold fields.

---

### Step 5 — Verify method field options

**Responsible role:** L1_support

**Instruction:**
Find the Method field and verify whether the documented options shown are Count, Cube, or Cube and Count.

**Expected result:**
The Method field and its documented options are identified from the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*Method field and the listed options Count, Cube, and Cube and Count.*


**Stop or Escalate If:**

* The Method field does not show the documented options described in the source.

---

### Step 6 — Check weight-related parameters

**Responsible role:** L1_support

**Instruction:**
Check whether Maximum Weight and Weight Threshold fields are present on the screen.

**Expected result:**
The documented weight-related parameters are confirmed from the source screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*Maximum Weight and Weight Threshold field labels.*


**Stop or Escalate If:**

* The screen does not show Maximum Weight or Weight Threshold as documented in the source.

---

### Step 7 — Record only the documented field names and options

**Responsible role:** L1_support

**Instruction:**
Record the displayed threshold field names and method option shown by the source without inventing undocumented meanings or actions.

**Expected result:**
A source-grounded record of the field names and method options is produced.

**Screens / Images:**

![artifact_training_video_training_video_day1_0076_our_exchange_settings_so_this_is_primary_02_27_29_000](assets/f1933105d45fe475.jpg)

*Use the screen as the authoritative reference for field names and visible options.*


**Stop or Escalate If:**

* You cannot document the fields without adding unsupported interpretation.
* The screen does not show the documented threshold, method, or weight fields described in the source.

---

## Success Criteria

* The Tote Exchange Settings interface is identified from the source.
* The documented cube threshold fields are identified: Cube Threshold Pickup, Cube Threshold Priority, and Cube Threshold Close.
* The documented count threshold fields are identified: Count Threshold Pickup, Count Threshold Priority, and Count Threshold Close.
* The Method field options are identified as Count, Cube, and Cube and Count.
* The weight-related parameters Maximum Weight and Weight Threshold are confirmed as present in the source.
* The resulting notes remain limited to source-supported field names and options.

## Failure Conditions

* The screen does not show the documented threshold, method, or weight fields described in the source.
* The interface cannot be matched to the provided training artifact.
* The reviewer attempts to infer undocumented threshold meanings, calculations, or corrective actions from this source alone.

## Escalation Guidance

* Escalate if the screen does not show the documented threshold, method, or weight fields described in the source.
* Escalate if the available screen cannot be matched to the provided source artifact.
* Escalate for SME review if interpretation would require undocumented meanings, calculations, or corrective actions.

## Missing Details / Known Gaps

* The source does not provide a navigation path to reach the Tote Exchange Settings interface.
* The source does not define exact role boundaries beyond the candidate's L1_support assumption.
* The source does not provide exact threshold values to use operationally in this runbook.
* The source does not define the meaning or calculation logic for each threshold field.
* The source does not provide corrective actions or change-control guidance for modifying these settings.
* The source transcript mentions queue as part of threshold discussion, but the provided OCR evidence does not confirm a queue threshold field label on the screen.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_tote_exchange_settings_thresholds
- Source ID: `training_video_day1`
- Source Type: `training_video`
