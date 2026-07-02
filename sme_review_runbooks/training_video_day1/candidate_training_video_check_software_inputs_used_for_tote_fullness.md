# Check What Inputs Software Uses To Assess Tote Fullness

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_what_inputs_software_uses_to_assess_tote_fullness_v1` |
| Title | Check What Inputs Software Uses To Assess Tote Fullness |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training source to identify the documented inputs software uses to determine how full a tote or location is as items accumulate. The source supports weight and dimensions as referenced inputs and notes that dimensions are scaled up by software based on package type.

## When To Use

Use this reference procedure when you need to explain or verify, from the training source only, what inputs the software considers when assessing tote or location fullness as parcels accumulate.

## Do Not Use For

* Do not use this runbook to derive exact fullness formulas or calculation logic.
* Do not use this runbook to determine exact thresholds beyond what the source explicitly states.
* Do not use this runbook to invent package-type scaling rules, system fields, or unsupported controls.

## Safety And Operational Notes

* This is a reference and interpretation procedure based on training material, not a physical intervention.
* Do not invent formulas, package-type rules, or system fields not present in the source.

## Access Or Tools Needed

* Access to the training slide or transcript describing tote fullness assessment

## Related Operational Context

* ctx_training_video_weight_dimensions_fill_assessment_v1

## Procedure Steps

### Step 1 — Locate the parcel lifecycle fullness material

**Responsible role:** L1_support

**Instruction:**
Open the parcel lifecycle training material and locate the slide or segment stating that software determines how full the location or tote is as items sort into it.

**Expected result:**
The relevant lifecycle slide or segment is identified for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0012_one_question_previous_like_the_two_primary_00_19_06_000](assets/c436919ae7797e5f.jpg)

*Slide titled "Lifecycle of a parcel" showing software determination of tote or location fullness.*


**Stop or Escalate If:**

* Escalate if the referenced training slide or segment is unavailable.

---

### Step 2 — Identify the documented fullness inputs

**Responsible role:** L1_support

**Instruction:**
Identify the inputs explicitly referenced by the source for fullness assessment. Record that the source references weight and dimensions as inputs used by software as items accumulate in the tote or location.

**Expected result:**
The documented inputs are captured as weight and dimensions.

**Screens / Images:**

![artifact_training_video_training_video_day1_0012_one_question_previous_like_the_two_primary_00_19_06_000](assets/c436919ae7797e5f.jpg)

*Text on the lifecycle slide referencing weight and dimensions in software fullness determination.*


**Stop or Escalate If:**

* Escalate if more detailed calculation logic is requested, because the source does not provide it.

---

### Step 3 — Capture the package-type scaling note

**Responsible role:** L1_support

**Instruction:**
Record that the source states dimensions are scaled up by software based on package type. Do not add any package-type rules beyond that statement.

**Expected result:**
The package-type scaling note is documented exactly at the level supported by the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0012_one_question_previous_like_the_two_primary_00_19_06_000](assets/c436919ae7797e5f.jpg)

*Source text indicating that dimensions are scaled up by software based on package type.*


**Stop or Escalate If:**

* Escalate if exact scaling rules or package-type logic are needed, because the source does not provide them.

---

### Step 4 — Compare the assessment to documented factors only

**Responsible role:** L1_support

**Instruction:**
When discussing or reviewing tote fullness assessment, compare it only to the documented source factors: software-determined accumulation using weight and dimensions, with the source note that dimensions are scaled by package type.

**Expected result:**
The explanation or comparison remains limited to source-supported factors.

**Stop or Escalate If:**

* Stop and escalate if exact thresholds, formulas, or system field mappings are requested.
* Stop and escalate if unsupported package-type rules would be required to continue.

---

### Step 5 — Record that fullness is software-determined

**Responsible role:** L1_support

**Instruction:**
Record that the source describes fullness assessment as software-determined as items sort into the tote or location and accumulate. Do not describe it as a manual estimate unless another source explicitly supports that, which this runbook does not use.

**Expected result:**
The final reference statement reflects software-determined fullness assessment using the documented inputs.

**Screens / Images:**

![artifact_training_video_training_video_day1_0012_one_question_previous_like_the_two_primary_00_19_06_000](assets/c436919ae7797e5f.jpg)

*Lifecycle slide statement that software determines how full the location or tote is as items sort into it.*


**Stop or Escalate If:**

* Escalate if a user needs exact calculation logic or exact thresholds not provided by the source.

---

## Success Criteria

* The user can state that the documented fullness assessment is software-determined as items accumulate.
* The user can identify weight and dimensions as the source-supported inputs.
* The user can state that dimensions are scaled up by software based on package type.
* No unsupported formulas, thresholds, or system fields are introduced.

## Failure Conditions

* Exact calculation logic or thresholds are required but not available in the source.
* Unsupported formulas, package-type rules, or system fields are introduced.
* The source material cannot be located or interpreted confidently from the packet evidence.

## Escalation Guidance

* Escalate if more detailed calculation logic or exact thresholds are needed, because the source does not provide them.
* Escalate for SME review if a user needs package-type scaling details beyond the source statement.
* Escalate if the training evidence is insufficient to answer a site-specific or system-field-specific question.

## Missing Details / Known Gaps

* The source does not provide exact fullness formulas.
* The source does not provide exact thresholds for fullness calculation in this candidate evidence.
* The source does not provide detailed package-type scaling rules.
* The source does not identify specific system fields or UI elements for viewing the calculation.

## Source Lineage

- Candidate IDs: candidate_training_video_check_software_inputs_used_for_tote_fullness
- Source ID: `training_video_day1`
- Source Type: `training_video`
