# Identify Tote Details After Selecting An Item On the Container Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_tote_details_after_selecting_an_item_on_the_container_selection_screen_v1` |
| Title | Identify Tote Details After Selecting An Item On the Container Selection Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Select an item on the Container Selection screen and verify that the selected item displays identifying details, specifically a box icon and tote number.

## When To Use

Use this procedure when viewing the Container Selection screen and you need to confirm which tote is associated with a selected item by checking the identifying details shown after selection.

## Do Not Use For

* Do not use this procedure to infer additional selection behavior not stated in the source.
* Do not use this procedure as guidance for navigation to the Container Selection screen, because the source packet does not provide those steps.
* Do not use this procedure for tote search, rack recovery, AGV removal, or other control actions not explicitly covered by this source evidence.

## Safety And Operational Notes

* Use only the documented observation behavior from the source.
* Do not assume additional interface actions or controls beyond what is stated in the source.

## Access Or Tools Needed

* Access to the Container Selection screen
* Ability to select an item on the screen

## Related Operational Context

* ctx_training_video_container_selection_item_selection_v1

## Procedure Steps

### Step 1 — View the Container Selection screen

**Responsible role:** operator

**Instruction:**
Open or view the Container Selection screen.

**Expected result:**
The Container Selection screen is visible and available for item selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Container Selection screen with selectable rack or tote entries.*


**Stop or Escalate If:**

* The Container Selection screen cannot be accessed or viewed.
* The visible screen does not match the documented Container Selection context.

---

### Step 2 — Select the item of interest

**Responsible role:** operator

**Instruction:**
Select the item of interest on the Container Selection screen.

**Expected result:**
The system recognizes the selected item and displays its associated identifying details.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Selectable item entries on the Container Selection screen.*


**Stop or Escalate If:**

* The item cannot be selected.
* Selecting the item does not show the documented box icon and tote number.

---

### Step 3 — Check for the box icon

**Responsible role:** operator

**Instruction:**
Check whether a box icon appears for the selected item.

**Expected result:**
A box icon is visible for the selected item.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Selected item area where the box icon is expected to appear.*


**Stop or Escalate If:**

* The selected item does not show a box icon.

---

### Step 4 — Verify the tote number

**Responsible role:** operator

**Instruction:**
Verify that the tote number is displayed with the selected item.

**Expected result:**
The tote number is visible for the selected item.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Selected item area where the tote number is expected to be displayed.*


**Stop or Escalate If:**

* The selected item does not show a tote number.

---

### Step 5 — Confirm the selected tote

**Responsible role:** operator

**Instruction:**
Use the displayed box icon and tote number to confirm which tote is selected.

**Expected result:**
The operator can identify the selected tote from the displayed box icon and tote number.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Displayed box icon and tote number associated with the selected item.*


**Stop or Escalate If:**

* The displayed details do not allow the operator to confirm which tote is selected.
* Selecting an item does not show the documented box icon and tote number.

---

## Success Criteria

* An item on the Container Selection screen is selected.
* A box icon appears for the selected item.
* The tote number is displayed for the selected item.
* The operator can confirm which tote is selected using the displayed identifiers.

## Failure Conditions

* The Container Selection screen cannot be viewed.
* The item cannot be selected.
* Selecting the item does not show a box icon.
* Selecting the item does not show a tote number.
* The displayed information does not clearly confirm the selected tote.

## Escalation Guidance

* Escalate or seek clarification if selecting an item does not show the documented box icon and tote number.
* Seek clarification if the screen behavior differs from the source-supported description.
* Do not assume additional selection behavior beyond what is stated in the source.

## Missing Details / Known Gaps

* The source does not provide exact navigation steps to reach the Container Selection screen.
* The source does not specify exact control names or selection target labels.
* The source does not define how selection is visually indicated beyond the appearance of the box icon and tote number.
* The source does not provide timing expectations or troubleshooting steps beyond escalation for missing displayed details.

## Source Lineage

- Candidate IDs: candidate_training_video_identify_selected_tote_details_on_container_selection
- Source ID: `training_video_day1`
- Source Type: `training_video`
