# Interpret Tote Presence And Empty Rack State On the Container Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_tote_presence_and_empty_rack_state_on_the_container_selection_screen_v1` |
| Title | Interpret Tote Presence And Empty Rack State On the Container Selection Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen color coding to determine whether a location contains a tote or is an empty rack.

## When To Use

Use this reference when viewing the Container Selection screen and needing to determine whether a displayed rack or location currently shows a tote present or an empty rack state based on the documented blue color coding.

## Do Not Use For

* Do not use this runbook to interpret colors other than the documented dark blue and light blue states.
* Do not infer additional location, alarm, or control meanings not documented in this source.

## Safety And Operational Notes

* Use only the documented color meanings from this source.
* If the displayed color does not match the documented dark blue or light blue states, stop interpretation and escalate for clarification.

## Access Or Tools Needed

* Access to the Container Selection screen
* Visual access to the screen color indicators

## Related Operational Context

* ctx_training_video_container_selection_color_coding_v1

## Procedure Steps

### Step 1 — Open or view the Container Selection screen

**Responsible role:** operator

**Instruction:**
Open or view the Container Selection screen before interpreting any rack or location color state.

**Expected result:**
The Container Selection screen is visible for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Container Selection screen showing the color-coded rack or location display.*


**Stop or Escalate If:**

* The Container Selection screen cannot be viewed.
* The screen does not show the rack or location display needed for color interpretation.

---

### Step 2 — Locate the rack or location entries

**Responsible role:** operator

**Instruction:**
Locate the rack or location entries shown on the Container Selection screen.

**Expected result:**
The relevant rack or location entries are identified on the screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Displayed rack or location entries on the Container Selection screen.*


**Stop or Escalate If:**

* The displayed entries cannot be identified clearly enough to interpret their state.

---

### Step 3 — Observe the displayed color

**Responsible role:** operator

**Instruction:**
Observe the color of the displayed location or container position.

**Expected result:**
The operator identifies whether the displayed state is dark blue or light blue.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*The blue color state shown for the displayed location or container position.*


**Stop or Escalate If:**

* The displayed color does not match the documented dark blue or light blue states.
* The displayed color cannot be determined confidently.

---

### Step 4 — Interpret dark blue as tote present

**Responsible role:** operator

**Instruction:**
Interpret dark blue as indicating the presence of a tote.

**Expected result:**
A dark blue displayed location is understood to contain a tote.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Dark blue location state on the Container Selection screen.*


**Stop or Escalate If:**

* The dark blue state appears to be used inconsistently with the documented meaning.
* The operator is unsure whether the displayed color is dark blue.

---

### Step 5 — Interpret light blue as empty rack

**Responsible role:** operator

**Instruction:**
Interpret light blue as representing an empty rack.

**Expected result:**
A light blue displayed location is understood to be an empty rack.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Light blue location state on the Container Selection screen.*


**Stop or Escalate If:**

* The light blue state appears to be used inconsistently with the documented meaning.
* The operator is unsure whether the displayed color is light blue.

---

### Step 6 — Record or communicate the observed state

**Responsible role:** operator

**Instruction:**
Record or communicate the observed state using the documented color meaning only.

**Expected result:**
The observed location is communicated as either tote present or empty rack based only on the documented color coding.

**Stop or Escalate If:**

* The displayed color does not match the documented dark blue or light blue states.
* Additional interpretation beyond tote present or empty rack is being requested without source support.

---

## Success Criteria

* The user can determine from the Container Selection screen whether a shown location has a tote present or is empty.
* Dark blue is interpreted as tote present.
* Light blue is interpreted as empty rack.

## Failure Conditions

* The Container Selection screen is not available for viewing.
* The displayed color is unclear or does not match the documented dark blue or light blue states.
* An undocumented color or state is interpreted without source support.

## Escalation Guidance

* Escalate or seek clarification if the displayed color does not match the documented dark blue or light blue states.
* Do not infer meanings for colors or states not documented in this source.

## Missing Details / Known Gaps

* The source does not provide a time estimate for performing this reference check.
* The source does not define additional roles beyond operator use.
* The source does not document any commands.
* The source does not provide documented meanings for colors other than dark blue and light blue in this specific reference.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_container_selection_colors
- Source ID: `training_video_day1`
- Source Type: `training_video`
