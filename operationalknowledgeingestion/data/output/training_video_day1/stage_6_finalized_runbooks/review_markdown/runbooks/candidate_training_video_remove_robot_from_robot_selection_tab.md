# Remove a Robot From the Robot Selection Tab

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_a_robot_from_the_robot_selection_tab_v1` |
| Title | Remove a Robot From the Robot Selection Tab |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Selection tab to remove a robot from the system by entering the robot ID or selecting the robot on screen, then clicking Remove and confirming the system reports success. The source also warns that logical removal does not guarantee the robot is no longer physically present on the floor.

## When To Use

Use this procedure when a robot needs to be removed from the system through the Robot Selection tab and the operator has either the robot ID or can identify the robot directly on the screen.

## Do Not Use For

* Do not use this procedure as proof that the robot is no longer physically present on the floor.
* Do not assume logical removal is safe if physical robot presence is uncertain.

## Safety And Operational Notes

* The source warns that a robot can be removed logically while still remaining physically present on the floor.
* If a robot is physically present after logical removal, other robots may treat the pathway as free in the system model and then encounter that robot as an obstacle.
* The source states this condition should not result in a crash, but it still creates a mismatch between system state and floor state.

## Access Or Tools Needed

* Access to the Robot Selection tab
* Robot ID or ability to select the robot on screen
* Ability to click the Remove button
* Awareness of whether the robot is physically present on the floor

## Related Operational Context

* ctx_training_video_robot_selection_add_remove_tab_v1
* ctx_training_video_robot_add_remove_success_messages_v1
* ctx_training_video_robot_logical_vs_physical_presence_v1
* ctx_training_video_physical_robot_seen_as_obstacle_v1
* ctx_training_video_robot_right_of_way_space_on_map_v1

## Procedure Steps

### Step 1 — Open the Robot Selection tab

**Responsible role:** operator

**Instruction:**
Open the Robot Selection tab.

**Expected result:**
The Robot Selection tab is visible and ready for robot identification and removal.

**Screens / Images:**

![artifact_training_video_training_video_day1_0032_if_you_want_to_add_a_primary_01_17_55_500](assets/9f2665f3e5453b91.jpg)

*Robot Selection tab view showing the robot list or robot selection area, robot ID entry field, and Remove button.*


**Stop or Escalate If:**

* Stop if the Robot Selection tab cannot be accessed.

---

### Step 2 — Identify the robot to remove

**Responsible role:** operator

**Instruction:**
Identify the robot to remove either by entering the corresponding robot ID or by selecting the robot directly on the screen.

**Expected result:**
The intended robot is selected or identified for removal.

**Screens / Images:**

![artifact_training_video_training_video_day1_0032_if_you_want_to_add_a_primary_01_17_55_500](assets/9f2665f3e5453b91.jpg)

*Robot ID entry area and the robot selection area used to choose the robot for removal.*


**Stop or Escalate If:**

* Stop if the correct robot cannot be confidently identified.

---

### Step 3 — Click Remove

**Responsible role:** operator

**Instruction:**
Click the "Remove" button.

**Expected result:**
The system processes the robot removal request.

**Screens / Images:**

![artifact_training_video_training_video_day1_0032_if_you_want_to_add_a_primary_01_17_55_500](assets/9f2665f3e5453b91.jpg)

*Remove button in the Robot Selection tab.*


**Stop or Escalate If:**

* Stop if there is uncertainty that the selected robot is the intended robot before clicking Remove.

---

### Step 4 — Confirm removal success

**Responsible role:** operator

**Instruction:**
Check whether the system shows that the removal was successful.

**Expected result:**
The system displays a success indication for the removal.

**Screens / Images:**

![artifact_training_video_training_video_day1_0032_if_you_want_to_add_a_primary_01_17_55_500](assets/9f2665f3e5453b91.jpg)

*System feedback indicating that removal was successful.*


**Stop or Escalate If:**

* Stop if the system does not show that the removal was successful.

---

### Step 5 — Verify physical robot is not still on the floor

**Responsible role:** operator

**Instruction:**
Before treating the removal as complete, verify that the robot is not still physically present on the floor, because the source warns that a robot can be removed logically while still physically present.

**Expected result:**
The removed robot is not physically present on the floor, or the mismatch is recognized and escalated.

**Stop or Escalate If:**

* Stop and escalate if the robot is still physically present on the floor after being removed from the system.
* Stop and escalate if physical robot presence is uncertain.
* Stop and escalate if logical removal creates a mismatch between the system model and the floor state.

---

## Success Criteria

* The robot is removed from the system.
* The system shows that the removal was successful.
* The robot is confirmed not to remain physically present on the floor.

## Failure Conditions

* The Robot Selection tab cannot be accessed.
* The correct robot cannot be confidently identified.
* The system does not show that removal was successful.
* The robot remains physically present on the floor after logical removal.
* Physical robot presence is uncertain after logical removal.

## Escalation Guidance

* Escalate if the robot is still physically present on the floor after being removed from the system.
* Escalate if physical robot presence cannot be verified.
* Escalate if the system does not show that the removal was successful.
* Escalate if there is a mismatch between logical system state and physical floor state.

## Missing Details / Known Gaps

* The source does not specify exact navigation steps to reach the Robot Selection tab.
* The source does not specify the exact text or location of the success message beyond stating that removal success is shown.
* The source does not define a formal escalation contact or workflow.
* The source does not provide an estimated completion time.
* The source does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_remove_robot_from_robot_selection_tab
- Source ID: `training_video_day1`
- Source Type: `training_video`
