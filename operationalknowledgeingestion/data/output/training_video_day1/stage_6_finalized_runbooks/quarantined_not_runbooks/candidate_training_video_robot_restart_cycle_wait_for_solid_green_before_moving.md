# Wait for Solid Green During Robot Restart Cycle Before Physically Moving (Brakes Stay Locked)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_wait_for_solid_green_during_robot_restart_cycle_before_moving_brakes_locked_v1` |
| Title | Wait for Solid Green During Robot Restart Cycle Before Physically Moving (Brakes Stay Locked) |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery`, `e_stop_or_safety_stop` |
| Access Surface | `rms_ui`, `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | `shutdown_or_dwell_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

After restarting a robot/AGV, it goes through a cycle. Do not physically move it until the robot indicator reaches the source-described green state. If it is solid green and not on a label, you must wait until it turns green for movement readiness because the brakes stay locked until that condition.

## When To Use

Use when you have initiated a robot/AGV restart and you need to determine when it is safe to physically move it based on the indicator color/state and label presence behavior described in the source.

## Safety And Operational Notes

* Do not attempt to move the robot while brakes are still locked; the source states brakes stay locked until the robot reaches the correct green readiness condition.

## Access Or Tools Needed

* Visual access to the robot indicator/sign showing flashing blue / solid blue / solid green
* Ability to observe whether the robot is on a label (source describes 'not on a label' vs label identification)

## Related Operational Context

* ctx_training_video_robot_brake_lock_restart_behavior_v1
* ctx_training_video_robot_indicator_color_states_v1

## Procedure Steps

### Step 1 — Observe the robot indicator color/state through the restart cycle

**Responsible role:** operator

**Instruction:**
After initiating the restart, visually observe the robot indicator color/state as it cycles (the source describes flashing blue, solid blue, and solid green).

**Expected result:**
The robot indicator transitions through the source-described restart-cycle states (including flashing blue and then solid blue) as the robot reacquires label status.

**Stop or Escalate If:**

* If the indicator does not reach the source-described green state, escalate for further troubleshooting.

---

### Step 2 — Wait until the robot reaches solid green

**Responsible role:** operator

**Instruction:**
Continue observing until the robot indicator reaches solid green.

**Expected result:**
The robot indicator is solid green.

**Stop or Escalate If:**

* If the indicator does not reach solid green/green as described, escalate for further troubleshooting.

---

### Step 3 — Do not move while brakes are locked; wait until it turns green for movement readiness (especially if solid green and not on a label)

**Responsible role:** operator

**Instruction:**
Before physically moving the robot, verify the source-described condition: if the robot is solid green and not on a label, wait until it turns green (movement readiness). The source states you must wait because brakes stay locked.

**Expected result:**
You only proceed to physical movement after the robot turns green for readiness (not merely solid green when not on a label).

**Stop or Escalate If:**

* Do not move the robot while brakes are still locked.
* If the robot does not reach the source-described 'turns green' readiness condition, escalate for further troubleshooting.

---

### Step 4 — Proceed with moving the robot only after the source-described green readiness condition is met

**Responsible role:** operator

**Instruction:**
Once the robot meets the source-described movement readiness condition (indicator turns green as required), proceed with moving the robot as allowed by your site process.

**Expected result:**
The robot is physically moved only after it reaches the source-described green readiness state indicating brakes are no longer locked for movement.

**Stop or Escalate If:**

* If you realize the robot was moved before it reached the source-described readiness condition, stop and escalate for further troubleshooting.

---

## Success Criteria

* Robot is physically moved only after the source-described green readiness condition is met (specifically, waiting until it turns green when solid green and not on a label).

## Failure Conditions

* Robot is moved while brakes are still locked (e.g., before it turns green readiness).
* Robot does not reach solid green/green as described.

## Escalation Guidance

* If the indicator does not reach the source-described solid green/green readiness condition, escalate for further troubleshooting.

## Missing Details / Known Gaps

* The source does not define the exact visual distinction between 'solid green' and 'turns green' beyond the wording; it is treated as an observable readiness transition.
* The source does not provide specific escalation contacts or additional troubleshooting steps beyond 'escalate for further troubleshooting' when the indicator does not reach the described green condition.

## Source Lineage

- Candidate IDs: candidate_training_video_robot_restart_cycle_wait_for_solid_green_before_moving
- Source ID: `training_video_day1`
- Source Type: `training_video`
