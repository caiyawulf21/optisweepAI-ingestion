# Check Robot Restart State and Brake Lock Before Moving the Robot

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_robot_restart_state_and_brake_lock_before_moving_v1` |
| Title | Check Robot Restart State and Brake Lock Before Moving the Robot |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the restart-state color indications described in the training source to determine whether a restarted robot is still brake-locked or has reached the solid green state required before physical movement for label reacquisition.

## When To Use

Use after a physical or remote robot restart when support personnel need to determine whether the robot is still in its restart cycle, whether brakes remain locked, and whether it is permissible to move the robot for label reacquisition.

## Do Not Use For

* Do not use this runbook to justify moving the robot before it reaches solid green.
* Do not use this runbook for robot states other than the flashing blue, solid blue, and solid green states named in the source.
* Do not use this runbook as authorization for operator handling if site guidance requires higher-support involvement for physical robot movement.

## Safety And Operational Notes

* The source states the robot brakes stay locked during the restart cycle until the robot turns green.
* Do not attempt to move the robot while brakes are still locked.
* Because this procedure informs physical movement of the robot, use a higher-support role unless site guidance explicitly allows operator handling.

## Access Or Tools Needed

* Visual access to the robot state indication
* Knowledge of the documented restart color states
* Physical access only if movement is authorized

## Related Operational Context

* ctx_training_video_robot_indicator_color_states_v1
* ctx_training_video_robot_brake_lock_restart_behavior_v1

## Procedure Steps

### Step 1 — Wait for the restart cycle to begin and continue

**Responsible role:** L2_support

**Instruction:**
After a physical or remote restart, wait for the robot to go through its restart cycle.

**Expected result:**
The robot is observed in the restart sequence described by the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Restart-related training frame and transcript describing the robot restart cycle and what to expect if the robot is not on a label.*


**Stop or Escalate If:**

* The robot does not appear to proceed through the restart cycle.
* The observed behavior cannot be matched to the source-described restart sequence.

---

### Step 2 — Observe the documented robot color state

**Responsible role:** L2_support

**Instruction:**
Observe the robot's indicated state and note whether it is flashing blue, solid blue, or solid green, using only the states named in the source.

**Expected result:**
The robot state is identified as one of the documented restart-related color states.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Source-backed restart recovery visual/transcript reference for flashing blue, solid blue, and solid green robot states.*


**Stop or Escalate If:**

* The observed state does not match the documented flashing blue, solid blue, or solid green states.

---

### Step 3 — Do not move the robot while brakes are locked

**Responsible role:** L2_support

**Instruction:**
Do not attempt to move the robot while the brakes are still locked during the restart cycle.

**Expected result:**
No movement is attempted while the robot remains brake-locked.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Transcript evidence stating that the brakes stay locked during restart until the robot turns green.*


**Stop or Escalate If:**

* The robot appears to remain brake-locked without progressing.
* There is uncertainty about whether the brakes are still locked.

---

### Step 4 — Wait for solid green before moving the robot

**Responsible role:** L2_support

**Instruction:**
Wait until the robot turns solid green before moving it, because the source states the brakes stay locked until it turns green.

**Expected result:**
The robot reaches solid green and is then eligible for movement under the source-described condition.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Evidence for the solid green state as the point at which movement may occur.*


**Stop or Escalate If:**

* The robot does not reach the green state after restart.

---

### Step 5 — Verify movement after label read

**Responsible role:** L2_support

**Instruction:**
If the robot then reads the label, verify that it moves on as described by the source.

**Expected result:**
After reading the label, the robot resumes movement as described in the training segment.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Transcript segment describing that once the robot reads the label, it moves on.*


**Stop or Escalate If:**

* The robot reads the label but does not move on.

---

### Step 6 — Confirm label lock-on and blue-state change

**Responsible role:** L2_support

**Instruction:**
If the robot identifies a label during recovery, confirm the source-described lock-on behavior and the blue-state change associated with label pickup.

**Expected result:**
The robot identifies the label, locks itself on the label, and shows the documented blue-state transition.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Transcript evidence for label identification causing lock-on and the change from flashing blue to solid blue.*


**Stop or Escalate If:**

* The robot does not identify a label during recovery.
* The robot does not lock itself on the label after identification.
* The observed blue-state change does not match the source-described behavior.

---

## Success Criteria

* The robot's restart state is correctly identified using the documented flashing blue, solid blue, and solid green indications.
* No movement is attempted before the robot reaches solid green.
* The robot reaches solid green before movement is attempted.
* If label reacquisition occurs, the robot locks onto the label and the observed behavior matches the source-described recovery sequence.

## Failure Conditions

* The robot does not reach the green state after restart.
* The observed state does not match the documented flashing blue, solid blue, or solid green states.
* The robot does not lock onto a label during recovery when label pickup is expected.
* The robot does not move on after reading the label.

## Escalation Guidance

* Escalate if the robot does not reach the green state after restart.
* Escalate if the observed state does not match the documented flashing blue, solid blue, or solid green states mentioned in the source.
* Escalate if there is uncertainty about physical movement authorization or role boundaries for handling the robot.

## Missing Details / Known Gaps

* The source does not provide a time estimate for the restart cycle.
* The source does not provide explicit production-stop or LOTO requirements for this check.
* The source does not provide a complete decision tree for what to do if the robot never reaches solid green.
* The source does not provide additional documented robot indicator states beyond flashing blue, solid blue, and solid green for this scenario.

## Source Lineage

- Candidate IDs: candidate_training_video_check_robot_restart_state_and_brake_lock_before_moving
- Source ID: `training_video_day1`
- Source Type: `training_video`
