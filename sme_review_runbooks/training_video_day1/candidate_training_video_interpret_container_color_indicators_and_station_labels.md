# Interpret Tote Presence Colors And Distinguish Stations On The Container Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_tote_presence_colors_and_distinguish_stations_on_the_container_selection_screen_v1` |
| Title | Interpret Tote Presence Colors And Distinguish Stations On The Container Selection Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen color and label conventions from the training source to determine whether a visible location shows a tote present, an empty rack, or a station. The source states that dark blue indicates a tote is present, light blue indicates an empty rack, and items without those blue indicators are stations with associated IDs.

## When To Use

Use this reference when viewing the Container Selection screen and you need to interpret whether a displayed location contains a tote, is empty, or is a station based on the documented color and label appearance.

## Do Not Use For

* Do not use this runbook to infer any color meaning beyond tote present, empty rack, and station identification stated in the source.
* Do not use this runbook as authority for operational actions such as removing items, changing system state, or performing recovery actions.

## Safety And Operational Notes

* Limit interpretation to the meanings explicitly stated in the source.
* Escalate if the observed color or label pattern does not match the documented dark blue, light blue, or station description.

## Access Or Tools Needed

* Access to the Container Selection screen

## Related Operational Context

* ctx_training_video_container_color_status_v1
* ctx_training_video_station_labels_and_ids_v1

## Procedure Steps

### Step 1 — View the Container Selection indicators

**Responsible role:** operator

**Instruction:**
Open or view the Container Selection screen and look at the rack or container indicators shown on the display.

**Expected result:**
The relevant rack, container, or labeled screen items are visible for interpretation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*Dark blue and light blue indicators and examples of items without those indicators on the Container Selection screen.*


**Stop or Escalate If:**

* The Container Selection screen is not available.
* The visible indicators do not match the documented screen example closely enough to interpret.

---

### Step 2 — Check whether the location is dark blue or light blue

**Responsible role:** operator

**Instruction:**
Observe whether the selected or visible location is marked dark blue or light blue.

**Expected result:**
The location is identified as either dark blue, light blue, or not one of those blue indicators.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*The blue color states used on the Container Selection screen.*


**Stop or Escalate If:**

* The observed color does not clearly appear dark blue or light blue.
* The observed color pattern does not match the documented training description.

---

### Step 3 — Interpret blue occupancy colors

**Responsible role:** operator

**Instruction:**
Interpret dark blue as indicating the presence of a tote and light blue as representing an empty rack.

**Expected result:**
The viewed location is correctly classified as tote present or empty rack when one of the documented blue colors is shown.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*Examples of dark blue and light blue occupancy indicators.*


**Stop or Escalate If:**

* The screen appears to use a different meaning than the documented dark blue or light blue definitions.
* Additional color meanings seem necessary to interpret the screen.

---

### Step 4 — Treat non-blue labeled items as stations

**Responsible role:** operator

**Instruction:**
If an item does not have the blue or dark blue tote indicators, compare it to the training note that such items are stations rather than standard tote locations.

**Expected result:**
Items without the documented blue occupancy indicators are recognized as stations.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*Items on the screen that do not use the blue occupancy indicators.*


**Stop or Escalate If:**

* A non-blue item cannot be confidently distinguished from a tote location.
* The label pattern does not match the documented station description.

---

### Step 5 — Note that stations have associated IDs

**Responsible role:** operator

**Instruction:**
When a station is identified, note that the training says stations have associated IDs.

**Expected result:**
The user recognizes that station items are associated with IDs.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*Station-like labeled items distinguished from blue occupancy indicators.*


**Stop or Escalate If:**

* A station appears without the expected associated ID information described in the source.
* The screen element cannot be reconciled with the training description of a station.

---

## Success Criteria

* The user can distinguish dark blue locations as tote present.
* The user can distinguish light blue locations as empty rack.
* The user can distinguish non-blue labeled items as stations.
* The user understands that stations have associated IDs.

## Failure Conditions

* The observed color or label pattern does not match the documented dark blue, light blue, or station description.
* Additional status meanings are inferred from colors without source support.
* A station is confused with a standard tote occupancy location.

## Escalation Guidance

* Escalate if the observed color or label pattern does not match the documented dark blue, light blue, or station description.
* Escalate if the screen cannot be interpreted using only the source-backed meanings in this runbook.

## Missing Details / Known Gaps

* The source packet does not provide a formal role boundary beyond operator-level use.
* The source packet does not provide a time estimate.
* The source packet does not provide explicit do-not-use cases beyond limiting interpretation to the documented meanings.
* The source packet does not provide additional screenshots specifically isolating station IDs.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_container_color_indicators_and_station_labels
- Source ID: `training_video_day1`
- Source Type: `training_video`
