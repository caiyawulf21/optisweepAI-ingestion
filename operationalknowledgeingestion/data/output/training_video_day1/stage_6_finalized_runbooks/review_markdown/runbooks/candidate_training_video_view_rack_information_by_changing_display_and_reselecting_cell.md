# View Rack Information By Changing The Display And Reselecting The Same Cell

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_rack_information_by_changing_the_display_and_reselecting_the_same_cell_v1` |
| Title | View Rack Information By Changing The Display And Reselecting The Same Cell |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Change the display setting referenced in the training segment, then select the same cell again to show rack information for that cell.

## When To Use

Use when viewing a cell in the OptiSweep display and you need the interface to show rack information for that same cell, as described in the training segment.

## Do Not Use For

* Do not use as a fully specified control-navigation procedure when the exact display control or mode label must be known; the source does not identify that control.
* Do not use if you need a source-confirmed sequence beyond changing the display setting and reselecting the same cell.

## Safety And Operational Notes

* The source provides no physical safety hazards or lockout requirements for this display interaction.
* Use caution because the exact control being changed is not named in the source.

## Access Or Tools Needed

* Access to the display or screen where cells can be selected

## Related Operational Context

* ctx_training_video_selected_cell_context_display_v1

## Procedure Steps

### Step 1 — Change the display setting

**Responsible role:** operator

**Instruction:**
Change the displayed setting referred to in the training segment.

**Expected result:**
The display setting is changed from its prior state.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The training frame near the transcript statement about changing the display before selecting the same cell again.*


**Stop or Escalate If:**

* The exact control or mode label to change is not identifiable from the source.
* The display setting cannot be changed as expected.

---

### Step 2 — Reselect the same cell

**Responsible role:** operator

**Instruction:**
Select the same cell again after changing the display setting.

**Expected result:**
The same cell is reselected under the changed display setting.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*Use the frame as contextual support for the instruction to reselect the same cell after changing the display.*


**Stop or Escalate If:**

* The same cell cannot be identified with confidence.
* The interface does not register the repeated cell selection.

---

### Step 3 — Verify rack information is shown

**Responsible role:** operator

**Instruction:**
Observe whether the display shows the rack information for that cell.

**Expected result:**
The selected cell displays rack information.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*Reference the nearby training frame while verifying whether rack information appears after reselecting the cell.*


**Stop or Escalate If:**

* Rack information does not appear after changing the display and reselecting the same cell.
* Additional source guidance is needed because the source does not identify the exact control being changed.

---

## Success Criteria

* After changing the display setting and reselecting the same cell, the selected cell displays rack information.

## Failure Conditions

* The exact display control or mode label cannot be identified from the source.
* Changing the display and reselecting the same cell does not show rack information.
* The interface does not clearly indicate that the same cell was reselected.

## Escalation Guidance

* Seek additional source guidance or SME clarification if the exact display control being changed is unclear.
* Escalate if changing the display and reselecting the cell does not show rack information.

## Missing Details / Known Gaps

* The source does not name the exact control, button, or mode label that must be changed.
* The source does not provide a screenshot explicitly showing the rack-information result state for this action.
* The source does not define alternate troubleshooting steps if rack information does not appear.
* The source does not specify timing, permissions, or role boundaries beyond likely operator use.

## Source Lineage

- Candidate IDs: candidate_training_video_view_rack_information_by_changing_display_and_reselecting_cell
- Source ID: `training_video_day1`
- Source Type: `training_video`
