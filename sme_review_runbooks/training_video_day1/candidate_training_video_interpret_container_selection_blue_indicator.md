# Interpret Blue Status Indicators On The Container Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_blue_status_indicators_on_the_container_selection_screen_v1` |
| Title | Interpret Blue Status Indicators On The Container Selection Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen's blue visual indicators to determine whether a station or rack position has a tote present or is empty. The source states that dark blue indicates the presence of a tote and light blue represents an empty rack.

## When To Use

Use this reference when viewing the Container Selection screen and needing to interpret the meaning of the small blue indicator shown on a station or rack position.

## Do Not Use For

* Do not use this reference to infer any status meaning beyond the two documented values: tote present and empty rack.
* Do not use this reference when the displayed indicator does not appear as dark blue or light blue as described in the source.

## Safety And Operational Notes

* This source is a visual interpretation reference only and does not provide corrective actions.
* Do not infer additional status meanings beyond tote present and empty rack because the source only documents those values.

## Access Or Tools Needed

* Access to the Container Selection screen
* Visual view of the blue status indicator on the display

## Related Operational Context

* ctx_training_video_container_selection_screen_v1
* ctx_training_video_container_blue_indicator_status_v1

## Procedure Steps

### Step 1 — View the Container Selection screen

**Responsible role:** operator

**Instruction:**
Open or view the Container Selection screen for totes or containers.

**Expected result:**
The Container Selection screen is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Container Selection screen showing station or rack entries with blue indicators.*


**Stop or Escalate If:**

* Escalate if the Container Selection screen cannot be viewed.

---

### Step 2 — Locate the blue indicator

**Responsible role:** operator

**Instruction:**
Locate the small blue indicator shown on top of the relevant station or position as described in the source.

**Expected result:**
The relevant blue indicator is identified on the screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*The small blue indicator on top of some stations or positions.*


**Stop or Escalate If:**

* Escalate if the relevant indicator cannot be identified on the display.

---

### Step 3 — Observe the indicator color

**Responsible role:** operator

**Instruction:**
Observe whether the indicator is dark blue or light blue.

**Expected result:**
The operator identifies the indicator as dark blue or light blue.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Examples of dark blue versus light blue indicator states on the Container Selection screen.*


**Stop or Escalate If:**

* Escalate if the displayed indicator does not match the documented dark blue or light blue meanings.

---

### Step 4 — Interpret the documented meaning

**Responsible role:** operator

**Instruction:**
Compare the observed color to the documented meaning: dark blue indicates the presence of a tote, and light blue represents an empty rack.

**Expected result:**
The operator determines whether a tote is present or the rack is empty.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*The documented legend or visual example indicating dark blue means tote present and light blue means empty rack.*


**Stop or Escalate If:**

* Escalate if the displayed indicator does not match the documented dark blue or light blue meanings.
* Stop interpretation if additional status meanings would need to be inferred beyond tote present and empty rack.

---

### Step 5 — Communicate the interpreted status

**Responsible role:** operator

**Instruction:**
Record or communicate the interpreted status for the selected station or rack position.

**Expected result:**
The interpreted status is available for operational use.

**Stop or Escalate If:**

* Escalate if the interpreted status cannot be confidently determined from the documented dark blue and light blue meanings.

---

## Success Criteria

* The user can determine from the Container Selection display whether a tote is present or whether the rack position is empty.
* The observed indicator is interpreted using only the documented meanings: dark blue for tote present and light blue for empty rack.

## Failure Conditions

* The Container Selection screen cannot be viewed.
* The relevant blue indicator cannot be located.
* The indicator color is unclear or does not match dark blue or light blue.
* Additional status meaning would need to be inferred beyond what the source documents.

## Escalation Guidance

* Escalate if the displayed indicator does not match the documented dark blue or light blue meanings.
* Escalate if the indicator cannot be clearly seen or interpreted on the Container Selection screen.
* Do not infer additional status meanings beyond tote present and empty rack because the source only documents those values.

## Missing Details / Known Gaps

* The source does not provide a time estimate for using this reference.
* The source does not provide corrective actions beyond interpreting the indicator colors.
* The source does not define any additional blue indicator meanings beyond dark blue for tote present and light blue for empty rack.
* The source does not specify a formal recording method for communicating the interpreted status.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_container_selection_blue_indicator
- Source ID: `training_video_day1`
- Source Type: `training_video`
