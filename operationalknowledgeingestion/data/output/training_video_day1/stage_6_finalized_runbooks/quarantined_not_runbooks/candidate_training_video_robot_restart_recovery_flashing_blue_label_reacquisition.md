# Recover Robot Visibility After Restart When It Cannot See a Label (Flashing Blue to Solid Blue/Solid Green)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_robot_visibility_after_restart_cannot_see_label_v1` |
| Title | Recover Robot Visibility After Restart When It Cannot See a Label (Flashing Blue to Solid Blue/Solid Green) |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state`, `e_stop_or_safety_stop` |
| Access Surface | `physical_floor`, `rms_ui` |
| Audience Roles | `operator` |
| Failure Pattern Tags | `agv_tracking_or_path_lost` |
| Validation Status | `needs_smeme_review` |
| Merge Status | `source_finalized` |

## Summary

If a robot is restarted while stopped between two labels, it may not snap back onto the map because it cannot see a label. Use the source-described recovery: perform a system E stop, physically push the robot onto the label, then clear the E stop and verify the robot indicator transitions from flashing blue to solid blue and then to solid green, and that the robot becomes visible on the map.

## When To Use

Use when, after a robot restart, the robot does not snap back onto the map automatically because it cannot see a label, indicated by the robot showing a flashing blue sign/indicator.

## Safety And Operational Notes

* This procedure includes physical system E stop and walking into the floor area to push the robot onto the label; only perform if you can do so safely.

## Access Or Tools Needed

* Physical E stop access (as referenced by the source)
* Physical access to the robot on the floor
* Robot indicator/sign showing flashing blue / solid blue / solid green
* Map display to verify robot visibility

## Related Operational Context

* ctx_training_video_robot_map_visibility_after_restart_v1
* ctx_training_video_robot_indicator_color_states_v1
* ctx_training_video_robot_brake_lock_restart_behavior_v1

## Procedure Steps

### Step 1 — Check whether the robot snaps back onto the map after restart

**Responsible role:** operator

**Instruction:**
After restarting the robot, check the map display to see whether the robot snaps back onto the map automatically.

**Expected result:**
The robot is not positioned/visible on the map automatically after the restart (robot appears missing/not positioned).

---

### Step 2 — Identify the flashing blue indicator that means the robot cannot see a label

**Responsible role:** operator

**Instruction:**
Look for the robot indicator/sign state described by the source as flashing blue.

**Expected result:**
The robot shows a flashing blue sign/indicator.

---

### Step 3 — Perform the source-described recovery: E stop the system and push the robot onto the label

**Responsible role:** operator

**Instruction:**
If flashing blue is present, perform the source-described recovery: E stop the system, walk into the floor area, and push the robot onto the label.

**Expected result:**
After pushing the robot onto the label, the robot begins the label identification process (indicator should progress toward solid blue).

**Stop or Escalate If:**

* Stop and escalate if you cannot safely perform the source-described physical action (E stop + pushing the robot onto the label).

---

### Step 4 — Verify the robot locks onto the label (indicator transitions to solid blue)

**Responsible role:** operator

**Instruction:**
After pushing the robot onto the label, observe the robot indicator transition from flashing blue to solid blue.

**Expected result:**
The robot transitions from flashing blue to solid blue, indicating it has picked up the label.

**Stop or Escalate If:**

* If the indicator does not transition as described (flashing blue -> solid blue -> solid green) or the robot still does not appear on the map, escalate for further troubleshooting.

---

### Step 5 — Clear the E stop and confirm the robot is successfully showing on the map

**Responsible role:** operator

**Instruction:**
Clear the E stop and then check the map to confirm the robot is successfully showing on the map.

**Expected result:**
After clearing the E stop, the robot becomes visible successfully on the map.

**Stop or Escalate If:**

* If the indicator does not transition as described (flashing blue -> solid blue -> solid green) or the robot still does not appear on the map, escalate for further troubleshooting.

---

### Step 6 — Observe the full color transition to solid green and wait before moving if needed

**Responsible role:** operator

**Instruction:**
Observe the color transition: flashing blue -> solid blue -> solid green. If the robot is solid green but not on a label, wait until it turns green before moving it because the brakes stay locked.

**Expected result:**
The robot reaches solid green, and if it is solid green but not on a label, it is not moved until it turns green (brakes stay locked).

**Stop or Escalate If:**

* If the indicator does not transition as described (flashing blue -> solid blue -> solid green) or the robot still does not appear on the map, escalate for further troubleshooting.

---

## Success Criteria

* Robot reacquires a label and transitions from flashing blue to solid blue.
* Robot reaches solid green as part of the restart cycle.
* Robot becomes visible successfully on the map after clearing the E stop.

## Failure Conditions

* Robot does not snap back onto the map automatically after restart.
* Flashing blue is present and the robot does not transition to solid blue after being pushed onto the label.
* After clearing the E stop, the robot still does not appear on the map.
* Indicator sequence does not follow flashing blue -> solid blue -> solid green.

## Escalation Guidance

* Stop and escalate if you cannot safely perform the source-described physical action (E stop + pushing the robot onto the label).
* If the indicator does not transition as described (flashing blue -> solid blue -> solid green) or the robot still does not appear on the map, escalate for further troubleshooting.

## Missing Details / Known Gaps

* The source does not provide exact UI labels/buttons for the E stop action or the specific map UI element name used to verify robot visibility; it only references 'E stop the system' and 'you'll see the robot... on the map'.
* The source does not specify the exact robot indicator location (e.g., which side/LED) beyond 'flashing blue sign/indicator'.

## Source Lineage

- Candidate IDs: candidate_training_video_robot_restart_recovery_flashing_blue_label_reacquisition
- Source ID: `training_video_day1`
- Source Type: `training_video`
