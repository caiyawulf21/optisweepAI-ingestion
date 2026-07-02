# Verify That a Robot Resumes Its Transaction After Restart

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_that_a_robot_resumes_its_transaction_after_restart_v1` |
| Title | Verify That a Robot Resumes Its Transaction After Restart |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-based verification procedure to confirm the documented distinction between robot restart and robot removal. The source states that if a robot is in the middle of a transaction, it resumes that transaction after restart, and that task loss is associated with removing the robot from the system, after which it must go through initialization.

## When To Use

Use when reviewing the outcome of a robot restart and determining whether post-restart behavior matches the training source statement about transaction persistence.

## Do Not Use For

* Do not use this as a robot restart execution procedure; the source candidate is for verification of behavior, not for performing the restart.
* Do not use this to treat robot restart and robot removal as equivalent conditions.
* Do not use this as a detailed removal recovery procedure; the source only states that removal leads to initialization and task loss.

## Safety And Operational Notes

* Do not assume removal and restart have the same operational outcome; the source explicitly distinguishes them.
* If the robot was removed from the system, the source indicates it must go through initialization and that this is the case where the task is considered lost.

## Access Or Tools Needed

* Visibility into robot transaction status
* Knowledge of whether the robot was restarted or removed from the system

## Related Operational Context

* ctx_training_video_restart_task_persistence_v1

## Procedure Steps

### Step 1 — Identify the restarted robot and transaction state

**Responsible role:** L1_support

**Instruction:**
Identify a robot that was restarted while in the middle of a transaction, and confirm that the case under review is a restart outcome rather than another type of robot state change.

**Expected result:**
A specific robot and its pre-restart in-transaction condition are identified for verification.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Robot restart context and transcript note that tasks usually resume after restart unless the robot is removed from the system.*


**Stop or Escalate If:**

* Stop or escalate if you cannot determine whether the robot was restarted or removed from the system.

---

### Step 2 — Check whether the transaction resumes after restart

**Responsible role:** L1_support

**Instruction:**
After the restart completes, check whether the robot resumes the transaction, as stated in the source.

**Expected result:**
The robot resumes the in-progress transaction after restart.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Transcript statement that if the robot is in the middle of the transaction, it will resume the transaction after restart.*


**Stop or Escalate If:**

* Escalate if a restarted robot does not resume its transaction and there is no evidence that it was removed from the system.

---

### Step 3 — Distinguish restart behavior from removal behavior

**Responsible role:** L1_support

**Instruction:**
If reviewing the restart outcome, distinguish restart behavior from removal behavior using the source statement that tasks do not get lost for restarts.

**Expected result:**
The case is classified using the source distinction that restart preserves the task while removal is the loss case.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Transcript note that the task does not get lost for restarts.*


**Stop or Escalate If:**

* Stop or escalate if available evidence suggests the robot may have been removed rather than restarted.
* Do not treat restart and removal as equivalent; the source explicitly distinguishes them.

---

### Step 4 — Handle the case where the robot was removed from the system

**Responsible role:** L1_support

**Instruction:**
If the robot was removed from the system rather than restarted, note that the source says it must go through an initialization process and that this is when the task is considered lost.

**Expected result:**
The case is identified as a removal case, with initialization required and task loss understood as source-supported behavior.

**Screens / Images:**

![artifact_training_video_training_video_day1_0032_if_you_want_to_add_a_primary_01_17_55_500](assets/9f2665f3e5453b91.jpg)

*Robot Selection add/remove workflow showing removal as a distinct system action.*

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Transcript statement that task loss occurs when the robot is removed and must go through initialization.*


**Stop or Escalate If:**

* Stop or escalate if the robot was removed from the system and the review is still being evaluated as a restart persistence case.

---

### Step 5 — Record whether observed behavior matches the documented distinction

**Responsible role:** L1_support

**Instruction:**
Record whether the observed behavior matches the documented distinction between restart and removal.

**Expected result:**
A clear verification result is documented: either restart matched expected transaction resumption, or removal matched the documented initialization/task-loss case.

**Screens / Images:**

![artifact_training_video_training_video_day1_0034_restart_so_basically_the_process_to_primary_01_22_46_500](assets/432e4dd0da640fff.jpg)

*Source segment summarizing the expected distinction to use when recording the result.*


**Stop or Escalate If:**

* Escalate if observed behavior does not match the documented distinction and there is no evidence supporting removal from the system.

---

## Success Criteria

* The reviewer confirms whether a restarted robot resumed its in-progress transaction.
* The reviewer correctly distinguishes restart behavior from removal behavior using the source statement.
* The final record states whether the observed outcome matches the documented source expectation.

## Failure Conditions

* A restarted robot does not resume its transaction and there is no evidence that it was removed from the system.
* Restart and removal are treated as equivalent despite the source distinction.
* The observed case cannot be clearly classified as restart versus removal.

## Escalation Guidance

* Escalate if a restarted robot does not resume its transaction and there is no evidence that it was removed from the system.
* Escalate if the available evidence is insufficient to determine whether the robot was restarted or removed.
* Do not classify a removal case as a restart persistence failure.

## Missing Details / Known Gaps

* The source does not provide a detailed UI path or exact screen for checking transaction status.
* The source does not provide a formal logging location or documentation template for recording the verification result.
* The source does not provide a time expectation for restart completion or verification duration.
* The source does not provide a detailed removal recovery workflow beyond noting initialization and task loss.

## Source Lineage

- Candidate IDs: candidate_training_video_verify_transaction_resumes_after_robot_restart
- Source ID: `training_video_day1`
- Source Type: `training_video`
