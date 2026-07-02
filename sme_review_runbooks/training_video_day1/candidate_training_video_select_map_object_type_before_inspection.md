# Choose the Correct Map Object Selection Mode Before Inspecting a Map Item

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_choose_correct_map_object_selection_mode_before_inspecting_map_item_v1` |
| Title | Choose the Correct Map Object Selection Mode Before Inspecting a Map Item |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Map Monitor left-side object selection controls to choose the intended inspection mode before clicking a clickable map item. Supported selection modes shown in the source are robot, container, cell, and charger.

## When To Use

Use when reviewing clickable items on the Map Monitor and you need the system to interpret the next map click as a specific object type for inspection, such as a robot, container, cell, or charger.

## Do Not Use For

* Do not use this runbook as guidance for the downstream inspection details shown after the map item is clicked; the source does not describe those results.
* Do not use this runbook for recovery, control, or movement actions; it only covers selecting the correct map object inspection mode before clicking.

## Safety And Operational Notes

* This source presents the task as an inspection aid and does not describe any physical intervention.
* If the clicked map item does not inspect as intended, verify the correct selection mode was chosen first.

## Access Or Tools Needed

* Access to the Map Monitor screen
* Left-side object selection controls

## Related Operational Context

* ctx_training_video_map_monitor_quick_select_overview_v1
* ctx_training_video_map_object_selection_modes_v1

## Procedure Steps

### Step 1 — Open Map Monitor and locate the object selection panel

**Responsible role:** L1_support

**Instruction:**
Open the Map Monitor screen and locate the left-side panel with the object selection icons.

**Expected result:**
The left-side selection controls are visible on the Map Monitor screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*Left-side panel showing Robot, Container, Cell, and Charger selection controls.*


**Stop or Escalate If:**

* Stop if the Map Monitor screen is not available.
* Escalate if the left-side object selection controls are missing or cannot be identified.

---

### Step 2 — Decide which object type you need to inspect

**Responsible role:** L1_support

**Instruction:**
Before clicking an item on the map, decide which object type you want to inspect.

**Expected result:**
The intended inspection target is identified as one of the supported object types.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*The object-type choices available on the left panel: robot, container, cell, and charger.*


**Stop or Escalate If:**

* Stop if it is unclear which object type should be inspected.
* Escalate if the available selection modes do not match the object the user needs to inspect.

---

### Step 3 — Select the matching object type icon

**Responsible role:** L1_support

**Instruction:**
Click the matching selection icon: robot, container, cell, or charger.

**Expected result:**
The correct object selection mode is set for the next map click.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*The left-side object selection icons used to choose robot, container, cell, or charger mode.*


**Stop or Escalate If:**

* Stop if the correct icon cannot be selected.
* Escalate if the interface does not allow choosing robot, container, cell, or charger selection mode.

---

### Step 4 — Click the corresponding map item to inspect it

**Responsible role:** L1_support

**Instruction:**
After selecting the object type, click the corresponding item on the map to inspect it.

**Expected result:**
The map click is interpreted using the selected object type, allowing inspection of the intended item.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*The map area used after selecting an object type, where the corresponding item is clicked for inspection.*


**Stop or Escalate If:**

* Stop if clicking the map item does not inspect the intended object.
* Verify the correct selection mode was chosen first if the wrong object behavior occurs.
* Escalate if repeated attempts with the correct selection mode still do not allow inspection.

---

## Success Criteria

* The correct object selection mode is chosen before clicking the map.
* The intended map item is inspected as the selected object type.
* The user can use the left-side controls to choose among robot, container, cell, or charger before inspection.

## Failure Conditions

* The left-side object selection controls cannot be located.
* The wrong object type is selected before clicking the map.
* Clicking a map item does not inspect the intended object.
* The source does not describe the resulting inspection details after the map item is clicked.

## Escalation Guidance

* If clicking a map item does not inspect the intended object, verify that the correct selection mode was chosen first.
* Escalate if the correct selection mode is chosen but the map still does not allow inspection of the intended object.
* Escalate when additional detail is needed about the inspection results after clicking, because the source does not provide that information.

## Missing Details / Known Gaps

* The source does not describe the detailed inspection output shown after clicking the selected map item.
* The source does not provide an estimated completion time.
* The source does not specify whether production stop or LOTO is required; none is stated.
* The source does not define supporting roles beyond the primary L1 support framing.

## Source Lineage

- Candidate IDs: candidate_training_video_select_map_object_type_before_inspection
- Source ID: `training_video_day1`
- Source Type: `training_video`
