# Interpret Robot Battery Thresholds For Task Acceptance And Startup Risk

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_robot_battery_thresholds_for_task_acceptance_and_startup_risk_v1` |
| Title | Interpret Robot Battery Thresholds For Task Acceptance And Startup Risk |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training guidance on battery percentage thresholds to judge whether a robot is suitable for new tasking, is approaching shutdown risk, or may require manual charging handling.

## When To Use

Use when an operator needs to interpret a robot battery percentage against the training guidance for task acceptance, continued powered operation, or low-battery recovery risk.

## Do Not Use For

* Do not use as a precise charging or recovery procedure when the battery reading method is not defined in the source.
* Do not use to infer exact robot behavior beyond the source-stated thresholds and conversational guidance.
* Do not use as a substitute for manual charging handling instructions beyond what is explicitly stated in the source.

## Safety And Operational Notes

* Use only the source-stated battery thresholds and guidance.
* Avoid letting the robot get close to 15% when possible, because the source states it may turn off automatically and cannot be turned on until taken to a charger.
* If the robot is already too low to move or power on, stop normal operation and prepare for manual charging handling as described in the source.

## Access Or Tools Needed

* Access to the robot battery percentage indication
* Training guidance describing the 30%, 20%, and 15% thresholds

## Related Operational Context

* ctx_training_video_battery_task_acceptance_thresholds_v1
* ctx_training_video_low_battery_recovery_and_reentry_v1

## Procedure Steps

### Step 1 — Check the robot battery percentage

**Responsible role:** operator

**Instruction:**
Check the robot battery percentage using the available system indication or source-provided battery reading method if available in context.

**Expected result:**
A current battery percentage is observed for the robot.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*Nearby transcript reference to checking the power section and HV charge percentage during troubleshooting.*

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Battery-threshold discussion associated with low-battery behavior and manual charging context.*


**Stop or Escalate If:**

* Battery percentage cannot be determined from the available indication.
* The observed battery behavior cannot be matched to the source guidance.

---

### Step 2 — Compare the battery percentage to the documented thresholds

**Responsible role:** operator

**Instruction:**
Compare the observed battery percentage to the documented thresholds discussed in the training: around 30% is a point where charging should be considered when possible, under 20% the robot may not accept any new task, and at about 15% it may turn off automatically.

**Expected result:**
The operator classifies the robot as charge-soon, may-not-accept-new-tasks, or shutdown-risk based on the source guidance.

**Screens / Images:**

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Transcript-supported threshold guidance: around 30% consider charging, under 20% no new task acceptance, around 15% automatic shutdown.*


**Stop or Escalate If:**

* Observed behavior does not match the training guidance for the battery range.
* The operator is being asked to apply a stricter threshold or behavior not supported by the source.

---

### Step 3 — Record low-battery operational risk

**Responsible role:** operator

**Instruction:**
If the robot is near the lower thresholds, record that the robot may not take new work or may not stay powered on.

**Expected result:**
The robot is flagged as a low-battery operational risk based on the source guidance.

**Screens / Images:**

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Low-battery discussion tying threshold levels to task acceptance and automatic shutdown risk.*


**Stop or Escalate If:**

* The robot is under 20% and is still expected to accept new tasks contrary to the source guidance.
* The robot is near 15% and normal operation is still being attempted without charging attention.

---

### Step 4 — Avoid letting the robot approach 15% when possible

**Responsible role:** operator

**Instruction:**
Use the source guidance to avoid letting the robot get close to 15% when possible.

**Expected result:**
Charging attention is considered earlier so the robot does not reach the automatic shutdown threshold.

**Screens / Images:**

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Guidance that charging earlier, such as around 30%, can save time and help avoid very low battery states.*


**Stop or Escalate If:**

* The robot is repeatedly being allowed to drop near 15% during normal operation.
* Site behavior or system behavior conflicts with the training guidance.

---

### Step 5 — Stop normal operation and prepare for manual charging handling if battery is too low

**Responsible role:** operator

**Instruction:**
If the robot has already dropped too low to move or power on, stop normal operation and prepare for manual charging handling as described in the source.

**Expected result:**
The operator recognizes that normal tasking is no longer appropriate and that charger-based recovery handling is needed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Slide and transcript describing charger selection/disable context for manually charging a low-battery robot and the note that the robot cannot be turned on until taken to a charger.*


**Stop or Escalate If:**

* The robot cannot be turned on and manual charging handling is required.
* The observed battery behavior does not match the training guidance.
* Additional support is needed to perform the manual charging handling described in the source.

---

## Success Criteria

* The operator can classify the robot battery state using the source thresholds.
* The operator recognizes that under 20% the robot may not accept new tasks.
* The operator recognizes that around 15% the robot may turn off automatically and cannot be turned on until taken to a charger.
* The operator uses earlier charging judgment, such as around 30% when charging is available, to avoid time loss.

## Failure Conditions

* Battery percentage cannot be determined from the available indication.
* The robot is under 20% and may not accept new tasks.
* The robot is around 15% and may turn off automatically.
* The robot cannot be turned on until taken to a charger.
* Observed battery behavior does not match the training guidance.

## Escalation Guidance

* Escalate or seek additional support if the observed battery behavior does not match the training guidance.
* Stop normal operation and prepare for manual charging handling if the robot is too low to move or power on.
* Seek additional support if the battery reading method or recovery handling details needed are not defined in the source.

## Missing Details / Known Gaps

* The source packet does not define an exact screen, menu path, or standard method for reading battery percentage.
* The source packet does not provide a formal logging or recording location for documenting low-battery risk.
* The 30% guidance is conversational and not presented as a strict enforced threshold.
* The packet references manual charging handling context but does not provide a complete step-by-step charging procedure in this candidate.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_low_battery_task_and_start_thresholds
- Source ID: `training_video_day1`
- Source Type: `training_video`
