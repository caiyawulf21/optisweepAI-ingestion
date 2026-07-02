# Locate the Map Overview Right-Side Information Panel

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_locate_map_overview_right_side_information_panel_v1` |
| Title | Locate the Map Overview Right-Side Information Panel |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Identify the right-side panel on the Map Overview screen as the area that provides additional information beyond the main map display.

## When To Use

Use this reference when orienting a user to the Map Overview screen layout and when identifying where additional information is displayed on the right side of the screen.

## Do Not Use For

* Do not use this runbook to interpret specific fields, values, statuses, or controls within the right-side panel, because the source does not describe them.
* Do not use this runbook if the displayed screen does not clearly match the Map Overview layout described in the source.

## Safety And Operational Notes

* This is a screen-identification reference only.
* The source does not describe any control interaction or operational changes from this panel segment.

## Access Or Tools Needed

* Access to the Map Overview screen
* Visual access to the HMI or training slide showing the screen layout

## Related Operational Context

* ctx_training_video_map_overview_right_panel_v1
* ctx_training_video_map_overview_screen_presence_v1
* ctx_training_video_right_panel_information_area_v1

## Procedure Steps

### Step 1 — Open or view the Map Overview screen

**Responsible role:** operator

**Instruction:**
Open or view the Map Overview screen shown in the training material.

**Expected result:**
The Map Overview screen is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0026_so_you_see_that_right_panel_primary_00_58_00_500](assets/253fc9bcc505febb.jpg)

*Overall Map Overview layout showing a map-style interface and a right-side panel.*


**Stop or Escalate If:**

* The screen shown does not clearly match the Map Overview layout described in the source.

---

### Step 2 — Identify the right-side panel

**Responsible role:** operator

**Instruction:**
Look to the right side of the screen and identify the right-side panel referenced by the presenter.

**Expected result:**
The right-side panel is visually identified on the screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0026_so_you_see_that_right_panel_primary_00_58_00_500](assets/253fc9bcc505febb.jpg)

*The right side of the Map Overview screen where the presenter indicates a panel.*


**Stop or Escalate If:**

* The right-side panel is not visually clear on the displayed screen.
* The screen does not match the training layout closely enough to identify the panel confidently.

---

### Step 3 — Use the panel as the information area

**Responsible role:** operator

**Instruction:**
Use the identified right-side panel as the information area that provides additional details beyond the main map display.

**Expected result:**
The user understands that the right-side panel is where additional information is presented.

**Screens / Images:**

![artifact_training_video_training_video_day1_0026_so_you_see_that_right_panel_primary_00_58_00_500](assets/253fc9bcc505febb.jpg)

*The right-side panel as the area described as providing more information.*


**Stop or Escalate If:**

* Specific fields, values, or controls are needed, because the source does not provide that detail.

---

### Step 4 — Compare the map area and the right-side panel

**Responsible role:** operator

**Instruction:**
If needed, compare the overall map area to the right-side panel to distinguish the map-style interface from the information panel.

**Expected result:**
The user can distinguish the main map display from the right-side information panel.

**Screens / Images:**

![artifact_training_video_training_video_day1_0026_so_you_see_that_right_panel_primary_00_58_00_500](assets/253fc9bcc505febb.jpg)

*The main map-style area versus the separate right-side panel.*


**Stop or Escalate If:**

* The screen layout remains unclear after comparison.
* A more detailed panel breakdown is required, because this source segment does not provide it.

---

## Success Criteria

* The Map Overview screen is identified.
* The right-side panel is located on the screen.
* The right-side panel is understood to be the area that provides additional information beyond the main map display.

## Failure Conditions

* The displayed screen does not clearly match the Map Overview layout described in the source.
* The right-side panel cannot be clearly identified.
* Specific panel contents or controls are needed but are not provided by this source segment.

## Escalation Guidance

* Stop and seek clarification if the visible screen does not clearly match the Map Overview layout described in the source.
* Escalate to SME review if specific panel fields, values, statuses, or controls must be identified, because this source does not define them.

## Missing Details / Known Gaps

* The source does not specify the exact fields, values, or controls shown in the right-side panel.
* The source does not provide a detailed interaction workflow for the panel.
* The source does not provide timing, role boundaries beyond operator-level viewing, or validation steps beyond visual identification.

## Source Lineage

- Candidate IDs: candidate_training_video_locate_map_overview_right_information_panel
- Source ID: `training_video_day1`
- Source Type: `training_video`
