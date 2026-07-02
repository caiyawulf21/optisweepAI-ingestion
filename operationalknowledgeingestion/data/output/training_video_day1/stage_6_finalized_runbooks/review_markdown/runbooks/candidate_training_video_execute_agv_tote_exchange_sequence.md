# Execute The AGV Tote Exchange Sequence

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_execute_the_agv_tote_exchange_sequence_v1` |
| Title | Execute The AGV Tote Exchange Sequence |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Carry out the source-described AGV tote exchange sequence in which exchange staging occurs when a tote is imminently full or completely full, an AGV positions under the racking for lift, an empty-tote AGV positions behind the tote location under the sorter, and the two AGVs perform a simultaneous move-out/move-in so the empty tote is lowered into the rack and the AGV roles transition for the next pickup cycle.

## When To Use

Use when performing or understanding the documented AGV tote exchange sequence for a tote location where exchange staging has occurred because the tote is imminently full or completely full.

## Do Not Use For

* Do not use as a detailed control-level operating instruction for HMI actions, button presses, or commands, because the source provides only a conceptual training sequence.
* Do not use as a recovery procedure for AGV faults, failed positioning, or incomplete exchanges, because the source does not provide recovery actions.

## Safety And Operational Notes

* The source is a training explanation and does not provide explicit safety controls, lockout/tagout steps, or production-stop requirements.
* Do not infer or perform undocumented controls, commands, or manual interventions not stated in the source.
* Escalate if AGV movement or positioning does not match the documented exchange pattern.

## Access Or Tools Needed

* Access to the AGV exchange area
* Visibility of AGV movement under the racking and sorter
* Source training material describing the exchange sequence

## Related Operational Context

* ctx_training_video_tote_exchange_overview_v1
* ctx_training_video_exchange_staging_thresholds_v1
* ctx_training_video_agv_zone_and_lift_positioning_v1
* ctx_training_video_post_exchange_agv_role_transition_v1

## Procedure Steps

### Step 1 — Confirm exchange staging condition

**Responsible role:** operator

**Instruction:**
Identify that the tote exchange is being staged based on the documented fullness threshold, described as a tote being imminently full or completely full.

**Expected result:**
The tote location is recognized as being in an exchange staging condition supported by the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the training explanation that staging for an exchange can happen when a tote is imminently full or completely full.*


**Stop or Escalate If:**

* The exchange staging condition cannot be confirmed from the documented fullness threshold.
* Observed exchange activity does not align with the source-described staging concept.

---

### Step 2 — Position AGV with no tote under the racking

**Responsible role:** operator

**Instruction:**
Position an AGV with no tote that is designated to the tote zone under the racking for a lift.

**Expected result:**
The no-tote AGV is positioned under the racking in preparation for lifting the tote.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the training frame or explanation showing an AGV with no tote moving under the racking to position for lift.*


**Stop or Escalate If:**

* The AGV cannot position under the racking as described.
* The AGV assigned to the tote zone is not the AGV in position for the lift.

---

### Step 3 — Lift the tote in position

**Responsible role:** operator

**Instruction:**
Lift the tote into position as described in the source.

**Expected result:**
The tote is lifted in position for the exchange sequence.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the portion of the training material stating that the tote is lifted in position.*


**Stop or Escalate If:**

* The tote cannot be lifted into position.
* The observed lift state does not match the source-described sequence.

---

### Step 4 — Position empty-tote AGV behind the tote location

**Responsible role:** operator

**Instruction:**
Have an AGV with an empty tote travel under the sorter and position itself behind the tote location.

**Expected result:**
The empty-tote AGV is positioned behind the tote location under the sorter.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the training frame or explanation showing the empty-tote AGV positioned behind the tote under the sorter.*


**Stop or Escalate If:**

* The AGV with an empty tote cannot position behind the tote location.
* The observed AGV arrangement does not match the documented behind-the-tote positioning.

---

### Step 5 — Perform the simultaneous exchange movement

**Responsible role:** operator

**Instruction:**
Perform the exchange so the AGV with the full tote moves out into the aisle while the AGV with the empty tote moves into the rack location at the same time.

**Expected result:**
The full-tote AGV moves out into the aisle while the empty-tote AGV moves into the rack location simultaneously.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the explanation that one AGV comes behind and both move simultaneously, with one moving out and one moving in.*


**Stop or Escalate If:**

* Observed AGV movement does not match the documented simultaneous exchange pattern.
* The full-tote AGV does not move into the aisle while the empty-tote AGV moves into the rack location.

---

### Step 6 — Lower the empty tote into the rack

**Responsible role:** operator

**Instruction:**
Lower the empty tote into the rack location.

**Expected result:**
The empty tote is lowered into the rack location.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the portion of the training explanation stating that the AGV with the empty tote lowers its empty tote into the rack.*


**Stop or Escalate If:**

* The empty tote cannot be lowered into the rack location.
* The tote placement does not complete after the move-in portion of the exchange.

---

### Step 7 — Recognize post-exchange AGV role transition

**Responsible role:** operator

**Instruction:**
After the empty tote is dropped, recognize that this AGV becomes the AGV that will pick up the next tote in that zone.

**Expected result:**
The AGV that dropped the empty tote is understood to be the next AGV for pickup in that zone.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the training explanation stating that the AGV that just dropped its tote becomes the AGV that will pick up the next tote.*


**Stop or Escalate If:**

* The post-exchange AGV role transition does not match the documented source behavior.

---

## Success Criteria

* The tote exchange is staged at the documented fullness condition.
* An AGV with no tote positions under the racking for lift.
* An AGV with an empty tote positions behind the tote location under the sorter.
* The AGV with the full tote moves out into the aisle while the AGV with the empty tote moves into the rack location simultaneously.
* The empty tote is lowered into the rack location.
* The AGV that dropped the empty tote becomes the AGV that will pick up the next tote in that zone.

## Failure Conditions

* Observed AGV movement does not match the documented simultaneous exchange pattern.
* An AGV cannot position under the racking or behind the tote location as described.
* The tote cannot be lifted into position.
* The empty tote is not lowered into the rack location.
* The source does not provide detailed operator controls or recovery actions for abnormal conditions.

## Escalation Guidance

* Escalate if the observed AGV movement does not match the documented simultaneous exchange pattern.
* Escalate if the AGV cannot position under the racking or behind the tote location as described.
* Escalate for faults, failed backfill, or incomplete replacement scenarios because the source does not provide recovery actions in this runbook candidate.

## Missing Details / Known Gaps

* The source is a training explanation and does not provide explicit operator controls, HMI interactions, button presses, or commands.
* The source does not define permissions, role boundaries beyond operator-level use, or approval requirements.
* The source does not provide detailed recovery actions for failed positioning, failed lift, or incomplete exchange.
* The source does not provide a time estimate for completing the exchange.
* The source does not explicitly state production-stop or LOTO requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_execute_agv_tote_exchange_sequence
- Source ID: `training_video_day1`
- Source Type: `training_video`
