# Use battery percentage thresholds to predict task acceptance and automatic shutdown behavior

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_battery_thresholds_predict_task_acceptance_shutdown_v1` |
| Title | Use battery percentage thresholds to predict task acceptance and automatic shutdown behavior |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | `shutdown_or_dwell_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the robot’s current battery percentage to predict whether it will accept new tasks and whether it will turn off automatically. The guidance provided is: under 20% it will not accept new tasks; at 15% it turns off automatically and you cannot turn it on until it is taken to a charger.

## When To Use

Use when you need to decide whether a robot with a given battery percentage is likely to accept new tasks and whether it may shut off automatically (and therefore be unavailable) based on the battery threshold behavior described in the source.

## Do Not Use For

* Do not use this guidance as a substitute for troubleshooting when observed behavior does not match the documented thresholds; escalate instead.

## Safety And Operational Notes

* Avoid operating the robot anywhere close to 15% battery, because at 15% it turns off automatically and cannot be turned on until moved to a charger.

## Access Or Tools Needed

* Access to the robot battery percentage display (HMI/system view)

## Related Operational Context

* ctx_training_video_battery_task_acceptance_thresholds_v1

## Procedure Steps

### Step 1 — Check the robot’s current battery percentage (as shown in the system/HMI)

**Responsible role:** operator

**Instruction:**
On the system/HMI, locate the robot’s current battery percentage and note the value.

**Expected result:**
You have the robot’s current battery percentage value available to compare against the thresholds (20% and 15%).

---

### Step 2 — If battery is under 20%, expect the robot will not accept any new task

**Responsible role:** operator

**Instruction:**
If the robot’s battery percentage is below 20%, treat it as not accepting new tasks.

**Expected result:**
Based on the threshold guidance, you predict the robot will not accept any new task when battery is under 20%.

**Stop or Escalate If:**

* If the observed behavior does not match the documented thresholds, stop relying on the threshold guidance and escalate to support.

---

### Step 3 — If battery is at/near 15%, expect automatic turn-off and inability to turn it back on

**Responsible role:** operator

**Instruction:**
If the robot’s battery percentage is at or near 15%, expect it to turn off automatically and that you cannot turn it on; plan to move it to a charger (e.g., using a dolly or carrying it to the charger and pushing down, per the source guidance).

**Expected result:**
You predict the robot will turn off automatically at 15% and you cannot turn it on until it is taken to a charger.

**Stop or Escalate If:**

* If the observed behavior does not match the documented thresholds, stop relying on the threshold guidance and escalate to support.

---

### Step 4 — Avoid operating near 15% and monitor for charging instead of continuing to run

**Responsible role:** operator

**Instruction:**
When planning robot usage, avoid running the robot anywhere close to 15%. If you see low battery approaching the thresholds, prioritize conditions that allow it to charge rather than continuing to run.

**Expected result:**
Operational decisions reduce the likelihood of the robot turning off automatically (at 15%) or rejecting new tasks (under 20%).

**Stop or Escalate If:**

* If the observed behavior does not match the documented thresholds, stop relying on the threshold guidance and escalate to support.

---

## Success Criteria

* You can correctly predict task acceptance and shutdown behavior from the battery thresholds: under 20% = no new tasks; at 15% = automatic turn-off and cannot be turned on until taken to a charger.

## Failure Conditions

* Observed robot behavior does not match the documented thresholds (under 20% task acceptance behavior; at 15% automatic turn-off and inability to turn on without charging).

## Escalation Guidance

* If the observed behavior does not match the documented thresholds, stop relying on the threshold guidance and escalate to support.

## Missing Details / Known Gaps

* The source does not specify the exact HMI label/location for the battery percentage display; the runbook assumes the operator can view it on the system/HMI.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_battery_threshold_task_acceptance_and_shutdown
- Source ID: `training_video_day1`
- Source Type: `training_video`
