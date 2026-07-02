# Recover a Restarted Robot That Does Not Reappear on the Map

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_a_restarted_robot_that_does_not_reappear_on_the_map_v1` |
| Title | Recover a Restarted Robot That Does Not Reappear on the Map |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Recover a robot that was restarted while stopped between labels and does not automatically reappear on the map because it cannot identify a label. The source describes confirming the condition, observing the flashing blue state, E-stopping the system, entering the floor, pushing the robot onto a label, waiting for the robot to lock onto the label, clearing the E-stop, and verifying the robot appears on the map and changes from flashing blue to solid blue.

## When To Use

Use when a robot has been restarted while stopped between two labels, does not snap back onto the map automatically, and the source-described condition indicates it cannot see a label.

## Do Not Use For

* Do not use before the restart cycle reaches the green state if the robot still has locked brakes; the source states to wait until it turns green before moving it because the brakes stay locked until then.
* Do not use as a general operator procedure without site-approved controls; this recovery includes E-stop use, floor entry, and physically moving the robot.
* Do not use for cases where the robot is already positioned at a restart point or QR code cell and displays normally on the map after restart.

## Safety And Operational Notes

* This procedure is not support-safe for general operator execution based on the source packet.
* The procedure includes use of the system E-stop before entering the floor.
* The procedure includes entering the floor and physically pushing the robot.
* The source states to wait until the robot turns green before moving it because the brakes stay locked until then.
* The source also notes the software E-stop pauses the system but is not a physical emergency stop and robots in motion may continue to the next label before stopping.

## Access Or Tools Needed

* System E-stop access
* Physical floor access
* Ability to physically push the robot
* Map display
* Visual access to robot color/state indication

## Related Operational Context

* ctx_training_video_robot_map_visibility_after_restart_v1
* ctx_training_video_robot_indicator_color_states_v1
* ctx_training_video_robot_brake_lock_restart_behavior_v1

## Procedure Steps

### Step 1 — Confirm the robot is not back on the map after restart

**Responsible role:** L2_support

**Instruction:**
Confirm that after the restart the robot is not showing on the map as expected and that it cannot see a label.

**Expected result:**
The affected robot is confirmed to have not snapped back onto the map automatically after restart because it cannot identify a label.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Restart guidance indicating the robot may not be displayed on the map after restart unless positioned at a restart point or QR code cell.*


**Stop or Escalate If:**

* Stop if the robot is already showing normally on the map.
* Escalate if the observed condition does not match the source-described restart-between-labels scenario.

---

### Step 2 — Observe the flashing blue robot indication

**Responsible role:** L2_support

**Instruction:**
Observe whether the robot shows the flashing blue indication mentioned in the source.

**Expected result:**
The robot shows the flashing blue indication associated with not seeing a label.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*The training segment describing the flashing blue sign when the robot cannot see a label after restart.*


**Stop or Escalate If:**

* Escalate if the robot state does not match the source-described flashing blue condition.

---

### Step 3 — E-stop the system before entering the floor

**Responsible role:** L2_support

**Instruction:**
E-stop the system before entering the floor, as described in the training segment.

**Expected result:**
The system is E-stopped before floor entry.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*Map monitor summary area showing the system E-stop control.*


**Stop or Escalate If:**

* Stop if floor entry would occur before the system is E-stopped.
* Escalate if site controls require additional authorization not provided in the source.

---

### Step 4 — Enter the floor and push the robot onto a label

**Responsible role:** L2_support

**Instruction:**
Walk into the floor and push the robot onto the label.

**Expected result:**
The robot is physically repositioned onto a label.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*The recovery description stating to walk into the floor and push the robot onto the label.*


**Stop or Escalate If:**

* Do not move the robot before the source-described restart cycle reaches the green state because the brakes stay locked until then.
* Escalate if the robot cannot be physically moved onto a label.

---

### Step 5 — Wait for the robot to identify and lock onto the label

**Responsible role:** L2_support

**Instruction:**
Watch for the robot to identify the label and lock itself on the label; the source states this brake-lock behavior is how you know it has identified the label.

**Expected result:**
The robot identifies the label and locks itself on the label.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*The transcript statement that the robot will lock itself on the label when it identifies it.*


**Stop or Escalate If:**

* Escalate if the robot does not lock onto the label after being pushed onto it.

---

### Step 6 — Exit the floor and clear the E-stop

**Responsible role:** L2_support

**Instruction:**
Exit the floor and clear the E-stop.

**Expected result:**
The floor is exited and the E-stop is cleared.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*System E-stop control in the map monitor summary area.*


**Stop or Escalate If:**

* Stop if the robot has not yet locked onto the label.
* Escalate if the E-stop cannot be cleared or the system does not resume as expected.

---

### Step 7 — Verify the robot appears successfully on the map

**Responsible role:** L2_support

**Instruction:**
Verify that the robot shows successfully on the map.

**Expected result:**
The robot appears successfully on the map.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*The restart guidance stating the robot will be shown successfully on the map after recovery.*


**Stop or Escalate If:**

* Escalate if the robot does not appear successfully on the map after the E-stop is cleared.

---

### Step 8 — Confirm the robot changes from flashing blue to solid blue

**Responsible role:** L2_support

**Instruction:**
Confirm the color change described in the source from flashing blue to solid blue after label pickup.

**Expected result:**
The robot changes from flashing blue to solid blue as described in the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*The training segment describing the robot going from flashing blue to solid blue after label pickup.*


**Stop or Escalate If:**

* Escalate if the robot does not change from flashing blue to solid blue after label pickup.

---

## Success Criteria

* The robot identifies a label.
* The robot locks itself on the label.
* The robot appears successfully on the map after the E-stop is cleared.
* The robot changes from flashing blue to solid blue as described in the source.

## Failure Conditions

* The robot does not lock onto the label after being pushed onto it.
* The robot does not appear successfully on the map after the E-stop is cleared.
* The robot does not change from flashing blue to solid blue.
* The robot is moved before the restart cycle reaches the green state while brakes are still locked.

## Escalation Guidance

* Escalate if the robot does not lock onto the label after being pushed onto it.
* Escalate if the robot does not appear successfully on the map after the E-stop is cleared.
* Escalate if the robot state does not match the source-described flashing blue / solid blue recovery pattern.
* Escalate if site-approved floor-entry or safety controls required for this action are not available in the source.

## Missing Details / Known Gaps

* The source does not provide a detailed guarded-area entry procedure or authorization workflow for entering the floor.
* The source does not specify whether a physical emergency stop, lockout/tagout, or additional site safety controls are required.
* The source does not provide a precise map-screen workflow for locating the affected robot during this recovery.
* The source does not provide a time estimate for completing the recovery.
* The source does not provide additional troubleshooting steps if the robot still fails to identify the label after repositioning.

## Source Lineage

- Candidate IDs: candidate_training_video_recover_robot_not_on_map_after_restart
- Source ID: `training_video_day1`
- Source Type: `training_video`
