# Interpret Tote Presence And Tote Mismatch From Robot Selection Details

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_tote_presence_and_tote_mismatch_from_robot_selection_details_v1` |
| Title | Interpret Tote Presence And Tote Mismatch From Robot Selection Details |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep Robot selection detail panel to interpret whether a selected robot is carrying a tote, shows a tote mismatch indicated by a prefixed question mark, or has no tote indicated by the absence of the brown box and the text "layer_1".

## When To Use

Use this reference when viewing a robot in the OptiSweep Robot view and you need to determine the tote state from the robot selection details.

## Do Not Use For

* Do not use this runbook as a corrective or recovery procedure for removing or re-adding robots or totes.
* Do not invent corrective actions beyond the documented meaning that a '?' indicates the robot was removed but the tote was not.
* Do not use this runbook if the tote display does not match any of the documented patterns.

## Safety And Operational Notes

* Use only the documented display meanings from the source.
* Do not infer undocumented corrective actions from the tote indicators.
* Escalate if the display does not match the documented patterns.

## Access Or Tools Needed

* Access to the OptiSweep Robot view
* Robot selection detail panel
* Visual access to the robot selection display

## Related Operational Context

* ctx_training_video_tote_presence_indicators_v1
* ctx_training_video_robot_selection_panel_overview_v1

## Procedure Steps

### Step 1 — Select the robot in Robot view

**Responsible role:** operator

**Instruction:**
In the Robot view, select the robot you want to inspect so its details are shown. If the detail section is hidden, expand it using the small arrow.

**Expected result:**
The selected robot is highlighted and its detail panel is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*Selected robot outline/box and the expandable robot detail section.*


**Stop or Escalate If:**

* The robot detail panel is not available after selection.

---

### Step 2 — Check for tote text under the robot ID

**Responsible role:** operator

**Instruction:**
Look under the robot ID in the detail panel for a tote identifier.

**Expected result:**
You can see whether tote text is present under the robot ID.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*The text area under the robot ID where the tote identifier appears.*


**Stop or Escalate If:**

* The tote display does not match any documented pattern.

---

### Step 3 — Interpret a displayed tote ID as tote present

**Responsible role:** operator

**Instruction:**
If a tote ID is shown under the robot ID, interpret that as the robot having a tote on it.

**Expected result:**
The robot is classified as carrying a tote when a tote ID is displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*A tote identifier displayed under the robot ID.*


**Stop or Escalate If:**

* The displayed tote state conflicts with the documented visual indicators.

---

### Step 4 — Interpret a prefixed question mark as tote mismatch after robot removal

**Responsible role:** operator

**Instruction:**
Check whether the tote text has a '?' before it. If present, interpret this as the robot having been removed while the tote has not been removed.

**Expected result:**
A tote ID prefixed with '?' is recognized as the documented removed-robot/tote-not-removed condition.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*The tote text under the robot ID and whether a '?' appears before the tote identifier.*


**Stop or Escalate If:**

* The tote display does not match any documented pattern.
* A corrective action is needed beyond the documented interpretation.

---

### Step 5 — Use the brown box on the robot image as the tote-present visual cue

**Responsible role:** operator

**Instruction:**
Observe whether the robot image shows the small brown box on top. Use that as the visual cue that the AGV has a tote.

**Expected result:**
The brown box visual is used as a tote-present indicator.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*The robot image and the small brown box on top of the AGV indicating tote presence.*


**Stop or Escalate If:**

* The brown box visual does not match the documented tote text state.

---

### Step 6 — Interpret no tote from layer_1 and no brown box

**Responsible role:** operator

**Instruction:**
If no tote is being carried, verify that the brown box is not shown and the tote section says 'layer_1'.

**Expected result:**
The robot is classified as having no tote when 'layer_1' is shown and the brown box is absent.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*The tote section showing 'layer_1' and the robot image without the brown box.*


**Stop or Escalate If:**

* The display does not match the documented no-tote pattern.

---

### Step 7 — Record the observed tote state using documented meanings only

**Responsible role:** operator

**Instruction:**
Record the observed tote state using only the documented meanings from the source: tote present, '?' indicating robot removed but tote not removed, or no tote indicated by 'layer_1' and no brown box.

**Expected result:**
The tote state is documented using only source-supported meanings.

**Stop or Escalate If:**

* The tote display does not match any of the documented patterns.
* A corrective action is needed that is not provided by this source.

---

## Success Criteria

* The selected robot's tote state is interpreted as one of the documented conditions.
* A displayed tote ID is recognized as tote present.
* A '?' prefix is recognized as meaning the robot was removed but the tote was not.
* The combination of 'layer_1' and no brown box is recognized as no tote.

## Failure Conditions

* The robot detail panel cannot be viewed.
* The tote display does not match any documented pattern.
* The visual indicator and text indicator conflict.
* A corrective action is needed but is not provided by this source.

## Escalation Guidance

* Escalate if the tote display does not match any of the documented patterns.
* Escalate if the robot detail panel cannot be accessed or interpreted.
* Do not invent corrective actions beyond the documented meaning that a '?' indicates the robot was removed but the tote was not.

## Missing Details / Known Gaps

* The source does not provide a corrective or recovery procedure for the '?' tote mismatch condition.
* The source does not provide timing estimates.
* The source does not define additional role boundaries beyond operator use of the display.
* The source does not provide commands or system actions beyond visual interpretation.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_robot_tote_presence_and_mismatch
- Source ID: `training_video_day1`
- Source Type: `training_video`
