# Interpret Container Selection Screen Fields For Tote And Location Information

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_container_selection_screen_fields_for_tote_and_location_information_v1` |
| Title | Interpret Container Selection Screen Fields For Tote And Location Information |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen to identify the displayed container or tote ID, associated location information, and site-relevant meanings of fields shown in the training source. The training explains that the green number is the container or tote ID, the Location field shows associated rack or AGV location information when displayed, Layer Count reflects the rack configuration and is one at this site, Logic ID is present but not used in this deployment, and exception-related fields may appear as interface features that this site does not use.

## When To Use

Use when viewing the Container Selection screen and needing to interpret the displayed container or tote ID, location-related information, Layer Count, Logic ID, or exception-related fields according to this training source.

## Do Not Use For

* Do not use this runbook to assign operational meaning to Logic ID beyond the source statement that it is not used in this environment.
* Do not use this runbook to interpret exception box or abnormal-related fields as active site workflows beyond the source statement that these features are available in the interface but not used at this site.
* Do not use this runbook if the displayed fields do not match the documented training explanation.

## Safety And Operational Notes

* Use only the field meanings explicitly supported by the training source.
* Do not assign additional operational meaning to Logic ID or exception-related fields beyond what the source states.

## Access Or Tools Needed

* Access to the Container Selection screen
* Visual access to the tote label if cross-checking the tote ID

## Related Operational Context

* ctx_training_video_container_selection_screen_overview_v1
* ctx_training_video_layer_count_single_density_v1
* ctx_training_video_logic_id_usage_note_v1
* ctx_training_video_exception_box_feature_scope_v1

## Procedure Steps

### Step 1 — Open or view the Container Selection screen

**Responsible role:** operator

**Instruction:**
Open or view the Container Selection screen and visually confirm that the screen includes the container-related fields described in the training, including the container field and the location-related fields shown on the training slide.

**Expected result:**
The Container Selection screen is visible and the relevant fields can be reviewed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*Container Selection screen showing the container field, location field, Layer Count, Logic ID, and right-side interface fields.*


**Stop or Escalate If:**

* The displayed screen does not match the documented Container Selection training view.
* The fields needed for interpretation are not visible or cannot be identified from the source-backed screen.

---

### Step 2 — Identify the green number as the container or tote ID

**Responsible role:** operator

**Instruction:**
Identify the green number shown for the selected item and interpret it as the container or tote ID. If needed, cross-check it against the tote label, which the training says is also visible on the tote.

**Expected result:**
The displayed green number is recognized as the container or tote ID for the selected item.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*The green number on the Container Selection screen that the training identifies as the container or tote ID.*


**Stop or Escalate If:**

* The displayed identifier cannot be interpreted as the container or tote ID from the source-backed screen.
* The displayed identifier conflicts with the training explanation.

---

### Step 3 — Check the Location field for associated rack or AGV location

**Responsible role:** operator

**Instruction:**
Check the Location field for the associated rack or AGV location if it is displayed on the screen.

**Expected result:**
The associated location information is identified from the Location field when present.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*The Location field on the Container Selection screen.*


**Stop or Escalate If:**

* The Location field does not appear when expected.
* The displayed location information cannot be interpreted from the source-backed labels.

---

### Step 4 — Interpret Layer Count using the site single-layer note

**Responsible role:** operator

**Instruction:**
Review the Layer Count field and interpret it using the site note that this deployment uses single-density racks with one layer.

**Expected result:**
Layer Count is understood as reflecting the rack configuration and is interpreted as one for this site.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*The Layer Count field on the Container Selection screen.*


**Stop or Escalate If:**

* Layer Count does not align with the training statement that this site uses one layer.
* The field meaning cannot be confirmed from the source-backed explanation.

---

### Step 5 — Treat Logic ID as present but unused in this environment

**Responsible role:** operator

**Instruction:**
Note that the Logic ID field may appear on the screen, but interpret it only as a displayed field that the training states is not used in this environment.

**Expected result:**
Logic ID is recognized as present on the interface without assigning unsupported operational meaning to it.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*The Logic ID field on the Container Selection screen.*


**Stop or Escalate If:**

* The screen behavior suggests Logic ID is being used in a way that conflicts with the training explanation.
* The field cannot be matched to the source-backed screen.

---

### Step 6 — Recognize exception-related fields as available but not used at this site

**Responsible role:** operator

**Instruction:**
If exception-related fields such as exception box or abnormal-related fields appear on the right side, recognize them as available interface features that the training says this site does not use.

**Expected result:**
Exception-related fields are recognized as present interface features without being treated as active site workflow elements.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*Right-side exception box and abnormal-related fields on the Container Selection screen, if visible.*


**Stop or Escalate If:**

* The displayed fields do not match the training explanation of available but unused features.
* The interface presents exception-related fields that cannot be interpreted from the source-backed labels.

---

## Success Criteria

* The user can identify the Container Selection screen and its relevant fields.
* The green number is correctly interpreted as the container or tote ID.
* The Location field is correctly recognized as the associated rack or AGV location when displayed.
* Layer Count is interpreted according to the site note that the deployment uses one layer.
* Logic ID is recognized as present but not used in this environment.
* Exception-related fields are recognized as available interface features not used at this site.

## Failure Conditions

* The displayed fields do not match the documented training explanation.
* The screen cannot be interpreted from the source-backed labels.
* Logic ID or exception-related fields are given unsupported operational meaning.

## Escalation Guidance

* Escalate if the displayed fields do not match the documented training explanation.
* Escalate if the screen cannot be interpreted from the source-backed labels.
* Escalate if field behavior appears inconsistent with the training statements about Layer Count, Logic ID, or exception-related fields.

## Missing Details / Known Gaps

* The source does not provide a time estimate for using this reference procedure.
* The source does not define supporting roles beyond the operator-oriented training explanation.
* The source does not provide explicit commands or system navigation clicks for opening the Container Selection screen in this segment.
* The source transcript is partially noisy, so field meanings were limited to source-backed statements.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_container_selection_screen_fields
- Source ID: `training_video_day1`
- Source Type: `training_video`
