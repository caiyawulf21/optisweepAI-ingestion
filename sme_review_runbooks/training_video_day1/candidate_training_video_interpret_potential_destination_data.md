# Interpret Potential Destination Data For A Parcel On The Sorter

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_potential_destination_data_for_a_parcel_on_the_sorter_v1` |
| Title | Interpret Potential Destination Data For A Parcel On The Sorter |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-based reference procedure to interpret potential destination data for a parcel after the parcel is already on the sorter. The training source explains that the second message includes tracking ID, barcode data, dimensional data, and potential destination data, and that the destination values represent one or more sortable destinations rather than a ZIP code.

## When To Use

Use when reviewing parcel lifecycle evidence, training material, or message details to explain what potential destination data means for a parcel that is already on the sorter.

## Do Not Use For

* Do not use this procedure to infer ZIP-code resolution logic beyond the source statement that ZIP-to-destination mapping is handled upstream.
* Do not use this procedure as a control procedure for changing parcel routing or destination assignments.
* Do not use this procedure if the available parcel data does not match the source-described second message context.

## Safety And Operational Notes

* This is an interpretive reference procedure derived from training content, not a physical operating instruction.
* Do not infer additional routing, mapping, or destination resolution behavior beyond what the source states.

## Access Or Tools Needed

* Access to parcel lifecycle message details or training evidence
* Source-described second message field list
* Training slide or transcript describing potential destination meaning

## Related Operational Context

* ctx_training_video_parcel_lifecycle_messages_v1
* ctx_training_video_potential_destination_concept_v1
* ctx_training_video_zip_to_destination_mapping_v1

## Procedure Steps

### Step 1 — Identify the parcel lifecycle point

**Responsible role:** L1_support

**Instruction:**
Identify that the parcel is already on the sorter and that the second message in the parcel lifecycle has been triggered before interpreting potential destination data.

**Expected result:**
The parcel is placed in the source-described lifecycle context for the second message.

**Screens / Images:**

![artifact_training_video_training_video_day1_0013_so_why_is_this_potential_and_primary_00_20_02_000](assets/dea6e687312f24c7.jpg)

*Look for the lifecycle slide section describing the second message after the parcel is on the sorter.*


**Stop or Escalate If:**

* Escalate if the available parcel evidence does not support that the parcel is at the source-described second-message stage.

---

### Step 2 — Verify the second message fields

**Responsible role:** L1_support

**Instruction:**
Check that the available second-message data includes tracking ID, barcode data, dimensional data, and potential destination data.

**Expected result:**
The message data matches the source-described second message field list.

**Screens / Images:**

![artifact_training_video_training_video_day1_0013_so_why_is_this_potential_and_primary_00_20_02_000](assets/dea6e687312f24c7.jpg)

*Look for the slide or frame section listing the second message contents: tracking ID, barcode data, dimensional data on the sorter, and potential destination data.*


**Stop or Escalate If:**

* Escalate if the observed parcel data does not include the source-described second message fields.

---

### Step 3 — Determine whether one or multiple destinations are shown

**Responsible role:** L1_support

**Instruction:**
Observe whether the parcel is described as having one potential destination or multiple potential destinations.

**Expected result:**
The reviewed parcel evidence is categorized as showing either a single sortable destination or multiple sortable destinations.

**Screens / Images:**

![artifact_training_video_training_video_day1_0013_so_why_is_this_potential_and_primary_00_20_02_000](assets/dea6e687312f24c7.jpg)

*Look for the training explanation that UPS may give an order multiple destinations.*


**Stop or Escalate If:**

* Stop interpretation if destination count cannot be determined from the available source-aligned evidence.

---

### Step 4 — Interpret destination values as sortable destinations

**Responsible role:** L1_support

**Instruction:**
Interpret the listed destination values as sortable destinations, not as a ZIP code.

**Expected result:**
The destination data is explained as sorter-relevant destination information rather than postal ZIP information.

**Screens / Images:**

![artifact_training_video_training_video_day1_0013_so_why_is_this_potential_and_primary_00_20_02_000](assets/dea6e687312f24c7.jpg)

*Look for the explanation that destination is not a ZIP code and instead represents sorted destination information.*


**Stop or Escalate If:**

* Escalate if stakeholders require ZIP-code interpretation not supported by the source.

---

### Step 5 — Note that ZIP-to-destination mapping is upstream

**Responsible role:** L1_support

**Instruction:**
If ZIP code mapping is being discussed, note that the source says ZIP-to-destination mapping is handled upstream and the local system only knows the destination information it needs for sorting.

**Expected result:**
The explanation distinguishes upstream ZIP mapping from local destination usage.

**Stop or Escalate If:**

* Do not infer destination resolution logic beyond the source statement that mapping is handled upstream.

---

### Step 6 — Record why multiple potential destinations can exist

**Responsible role:** L1_support

**Instruction:**
Record that multiple potential destinations can exist for a single parcel because upstream mapping may associate one ZIP code with one or more sortable destinations.

**Expected result:**
The final explanation includes the source-supported reason that multiple sortable destinations may be associated with one parcel.

**Screens / Images:**

![artifact_training_video_training_video_day1_0013_so_why_is_this_potential_and_primary_00_20_02_000](assets/dea6e687312f24c7.jpg)

*Look for the training explanation that one ZIP code may map to one or multiple sortable destinations.*


**Stop or Escalate If:**

* Escalate if a more detailed mapping rule or resolution algorithm is requested, because the source does not provide it.

---

## Success Criteria

* The user can correctly explain that potential destination data represents one or more sortable destinations for the parcel on the sorter.
* The user distinguishes sortable destination information from ZIP code information.
* The explanation stays within the source boundary that ZIP-to-destination mapping is handled upstream.

## Failure Conditions

* The available parcel data does not include the source-described second message fields.
* The parcel is interpreted outside the source-described lifecycle point.
* Destination values are treated as ZIP codes rather than sortable destinations.
* The explanation invents local destination resolution logic not supported by the source.

## Escalation Guidance

* Escalate if the observed parcel data does not include the source-described second message fields.
* Escalate if a detailed ZIP-to-destination resolution rule is required, because the source only states that mapping is handled upstream.
* Escalate for SME review if stakeholders need operational or system-specific behavior beyond this training explanation.

## Missing Details / Known Gaps

* The source does not provide a named OptiSweep screen or exact UI workflow for viewing the second message fields.
* The source does not provide commands, APIs, or database queries for retrieving parcel message data.
* The source does not define escalation ownership beyond the need for further review when source-aligned evidence is missing or more detailed mapping logic is requested.
* The source is training content and does not provide a formal validation method beyond interpretive consistency with the transcript and slide.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_potential_destination_data
- Source ID: `training_video_day1`
- Source Type: `training_video`
