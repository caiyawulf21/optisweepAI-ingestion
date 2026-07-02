# Interpret Shutdown Queue Behavior and AGV Movement During Shutdown and Startup

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_shutdown_queue_behavior_and_agv_movement_during_shutdown_and_startup_v1` |
| Title | Interpret Shutdown Queue Behavior and AGV Movement During Shutdown and Startup |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-based reference to interpret expected AGV position and movement during shutdown and startup. The training states that shutdown queues are where AGVs sit when the system is shut down, shutdown includes AGVs cycling through chargers, and on startup AGVs move into their assigned zones.

## When To Use

Use when a support user needs to understand or explain whether observed AGV locations and movement are consistent with the training description of shutdown and startup behavior.

## Do Not Use For

* Do not use as a control procedure for placing the system into shutdown or startup.
* Do not use as a corrective procedure for AGVs that fail to move as expected.
* Do not use to diagnose root cause beyond comparing observed behavior to the training description.

## Safety And Operational Notes

* This source provides interpretive guidance only and does not provide physical intervention steps.
* Do not infer unsupported corrective actions from this training segment.

## Access Or Tools Needed

* Visibility into AGV locations or system walkthrough access
* Knowledge of assigned zones
* Source-backed training description of shutdown queues and startup movement

## Related Operational Context

* ctx_training_video_shutdown_queue_reference_v1

## Procedure Steps

### Step 1 — Confirm the discussion or observation is about shutdown state

**Responsible role:** L1_support

**Instruction:**
Identify whether the system is being discussed or observed in shutdown rather than running.

**Expected result:**
The reviewer has established that the behavior under review is shutdown or startup related.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Transcript-aligned frame describing the distinction between shutdown and running states.*

![artifact_training_video_training_video_day1_0010_all_right_so_life_cycle_this_primary_00_15_09_500](assets/5959536fcd85fc0f.jpg)

*Lifecycle depiction showing startup, sorting, bag-out, and shutdown progression.*


**Stop or Escalate If:**

* Escalate if the system state cannot be determined from the available observation or discussion context.

---

### Step 2 — Interpret shutdown queues as AGV holding locations

**Responsible role:** L1_support

**Instruction:**
Check the shutdown queues and interpret them as the place where AGVs sit when the system is shut down.

**Expected result:**
AGVs located in shutdown queues during shutdown are understood as matching the documented training description.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Frame aligned to the statement that shutdown queues are where AGVs sit when shut down.*

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*Sorter layout frame showing shutdown queue locations.*


**Stop or Escalate If:**

* Escalate if AGV positions do not match the documented training description.

---

### Step 3 — Verify charger cycling expectation during shutdown

**Responsible role:** L1_support

**Instruction:**
Observe whether AGVs are cycling through charging while in shutdown logic, using only the source-backed expectation that shutdown includes charger cycling.

**Expected result:**
The reviewer recognizes charger cycling during shutdown as expected behavior when it matches the training description.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Transcript-aligned frame noting AGVs cycling through chargers during shutdown logic.*

![artifact_training_video_training_video_day1_0010_all_right_so_life_cycle_this_primary_00_15_09_500](assets/5959536fcd85fc0f.jpg)

*Lifecycle frame describing AGVs returning to shutdown and cycling back to chargers.*


**Stop or Escalate If:**

* Escalate if AGV positions or movement do not match the documented training description.
* Escalate if charger-related shutdown behavior cannot be reconciled with the source-backed expectation.

---

### Step 4 — Verify movement from shutdown queues into assigned zones on startup

**Responsible role:** L1_support

**Instruction:**
When startup begins, verify that AGVs move from shutdown queues into their own assigned zones.

**Expected result:**
Observed startup movement matches the training description of AGVs leaving shutdown queues and moving into assigned zones.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Frame aligned to the statement that when AGVs start up, they move into their own zones.*

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*Sorter layout frame describing shutdown queues and assigned zone behavior.*


**Stop or Escalate If:**

* Escalate if AGV positions or movement do not match the documented training description.
* The source does not provide corrective actions for AGVs that fail to move as expected.

---

### Step 5 — Compare observed behavior to the source description

**Responsible role:** L1_support

**Instruction:**
Compare the observed AGV location and movement to the source description: shutdown queues during shutdown, assigned zones after startup.

**Expected result:**
The reviewer can distinguish expected shutdown queue behavior from expected post-startup zone assignment.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Primary source frame summarizing shutdown queue behavior and startup movement into zones.*


**Stop or Escalate If:**

* Escalate if AGV positions or movement do not match the documented training description.
* Escalate if additional corrective guidance is needed, because the source does not provide corrective actions.

---

## Success Criteria

* Shutdown queues are correctly interpreted as the place AGVs sit when the system is shut down.
* Charger cycling during shutdown is recognized as part of the source-backed shutdown expectation.
* Startup behavior is correctly interpreted as AGVs moving into their assigned zones.
* The reviewer can distinguish shutdown queue behavior from normal zone assignment.

## Failure Conditions

* Observed AGV positions or movement do not match the documented training description.
* The operating state cannot be determined well enough to interpret shutdown queue behavior.
* AGVs do not appear to move into assigned zones on startup.
* The source does not provide corrective actions for the observed mismatch.

## Escalation Guidance

* Escalate if AGV positions or movement do not match the documented training description.
* Escalate when corrective action is needed, because this source provides interpretation only and does not provide a recovery procedure.
* Document the mismatch between observed behavior and the training description for further diagnosis.

## Missing Details / Known Gaps

* The source does not provide a direct control procedure for initiating shutdown or startup.
* The source does not provide corrective actions if AGVs fail to move as expected.
* The source does not define timing thresholds for how quickly AGVs should move into assigned zones.
* The source does not specify exact screens, commands, or system indicators to use for verification.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_shutdown_queue_and_agv_positioning
- Source ID: `training_video_day1`
- Source Type: `training_video`
