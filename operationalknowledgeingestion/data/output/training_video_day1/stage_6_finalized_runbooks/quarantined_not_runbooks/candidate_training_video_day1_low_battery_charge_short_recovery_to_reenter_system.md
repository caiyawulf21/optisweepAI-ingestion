# Charge a low-battery robot long enough to reach a level that allows it to start and be added back into the system

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_charge_low_battery_robot_short_charge_reenter_system_v1` |
| Title | Charge a low-battery robot long enough to reach a level that allows it to start and be added back into the system |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery`, `agv_charging_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `charging_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Recover a low-battery robot by charging it for a short period so it reaches a battery level sufficient to start and be added back into the system. The source provides example timing/levels: ~10 minutes to get enough juice to start, and charging from ~25% for ~15 minutes may bring the robot to ~40%, described as “good enough for the system” to cycle on its own.

## When To Use

Use when a robot is at a low battery level and needs a short charge to reach a level that allows it to start and be re-entered into the system so it can cycle on its own.

## Do Not Use For

* Do not use if the robot cannot reach the source-indicated sufficient battery level after the short charging period; escalate instead.

## Safety And Operational Notes

* The source indicates that at very low battery levels the robot may not accept new tasks and may turn off automatically (example thresholds mentioned: under 20% and at 15%). Avoid operating/attempting to start the robot when it is near these low thresholds; use the charger-based recovery approach.

## Access Or Tools Needed

* Access to robot battery percentage display
* Ability to place the robot on a charger and manage charging availability

## Related Operational Context

* ctx_training_video_low_battery_recovery_and_reentry_v1

## Procedure Steps

### Step 1 — Identify the robot’s current battery percentage

**Responsible role:** L1_support

**Instruction:**
Check the robot’s current battery percentage in the live system view you are using for robot status.

**Expected result:**
A current battery percentage value is identified for the robot (examples discussed in the source include ~25%, ~30%, and ~40%).

---

### Step 2 — Place the robot on a charger and charge for the short period

**Responsible role:** L1_support

**Instruction:**
Place the robot on a charger and allow charging for the short period described by the source examples (e.g., ~15 minutes when starting around ~25%). Ensure the charger is enabled/available for charging after any charger selection/disablement you perform.

**Expected result:**
The robot has been charged for the source-indicated short period (example: 15 minutes from ~25%).

---

### Step 3 — Verify battery percentage increased to a sufficient level

**Responsible role:** L1_support

**Instruction:**
After the short charging period, re-check the robot’s battery percentage and confirm it increased to the source-indicated sufficient level (example: ~40% described as 'good enough for the system').

**Expected result:**
Battery percentage is at/near the source-indicated sufficient level (example: ~40% after charging from ~25% for ~15 minutes).

**Stop or Escalate If:**

* Robot does not reach the source-indicated sufficient battery level after the short charging period

---

### Step 4 — Add the robot back into the system so it can start/cycle on its own

**Responsible role:** L1_support

**Instruction:**
Once the battery percentage is sufficient, add the robot back into the system so it can start/cycle on its own (source wording: 'add it back in the system' and 'to cycle it on its own').

**Expected result:**
The robot is added back into the system and is able to cycle on its own after the short charging period.

**Stop or Escalate If:**

* If the robot does not reach the source-indicated sufficient battery level after the short charging period, stop and escalate to support.

---

## Success Criteria

* Robot reaches the source-indicated sufficient battery level after a short charging period (example: ~40% after 25% + 15 minutes) and can be added back into the system to cycle on its own.

## Failure Conditions

* Robot does not reach the source-indicated sufficient battery level after the short charging period.
* Robot is at/near very low thresholds where it may not accept new tasks (source example: under 20%) or may turn off automatically (source example: at 15%).

## Escalation Guidance

* If the robot does not reach the source-indicated sufficient battery level after the short charging period, stop and escalate to support.

## Missing Details / Known Gaps

* The source provides example battery percentages and charging durations, but does not specify the exact live UI controls/workflow steps for 'add it back in the system' or the exact readiness indicators beyond battery percentage.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_low_battery_charge_short_recovery_to_reenter_system
- Source ID: `training_video_day1`
- Source Type: `training_video`
