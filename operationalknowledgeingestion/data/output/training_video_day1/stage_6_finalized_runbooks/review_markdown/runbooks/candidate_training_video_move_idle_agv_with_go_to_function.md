# Move An AGV To Another Map Location Using The Go-to Function

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_move_an_agv_to_another_map_location_using_the_go_to_function_v1` |
| Title | Move An AGV To Another Map Location Using The Go-to Function |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Go-to function in the robot selection interface to send an AGV that is not currently in a task to a selected square or map cell, avoiding the need to physically push the AGV.

## When To Use

Use when an AGV is not currently in a task and needs to be repositioned to another map location. The source describes a green AGV state as ready to execute something but not currently having a task, and identifies the Go-to function as useful for quick recovery and repositioning.

## Do Not Use For

* Do not use when the AGV is currently in a task.
* Do not use this procedure as a complete recovery workflow for cases where the AGV still does not pick up a new task after being moved, because the source does not provide further operator decision logic beyond the example described.

## Safety And Operational Notes

* Use only when the AGV is not in a task, as stated by the source.
* The source presents this function as a way to avoid physically pushing the AGV.

## Access Or Tools Needed

* Access to the AGV control interface with robot selection
* Go to function
* Map or target code destination selection

## Related Operational Context

* ctx_training_video_agv_go_to_function_v1
* ctx_training_video_agv_green_state_no_task_v1

## Procedure Steps

### Step 1 — Verify the AGV is idle and eligible for Go-to

**Responsible role:** operator

**Instruction:**
Identify an AGV that is not in a task. Confirm the AGV is in the green state described by the source as ready to execute something but not currently having a task.

**Expected result:**
An eligible AGV is identified for repositioning.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Robot Selection Go-to function slide and transcript note describing green state and no current task.*


**Stop or Escalate If:**

* Stop if the AGV is currently in a task.
* Stop if the AGV state does not indicate the ready/no-task condition described by the source.

---

### Step 2 — Select the AGV in robot selection

**Responsible role:** operator

**Instruction:**
Select the AGV in the robot selection area.

**Expected result:**
The intended AGV is selected in the interface.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Robot selection area showing the AGV selection step.*


**Stop or Escalate If:**

* Stop if you cannot identify or select the intended AGV.

---

### Step 3 — Select the Go to function

**Responsible role:** operator

**Instruction:**
Select the Go to function for the selected AGV.

**Expected result:**
The interface is ready for destination selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Go to function or button in the Robot Selection workflow.*


**Stop or Escalate If:**

* Stop if the Go to function cannot be selected for the AGV.

---

### Step 4 — Choose the destination location

**Responsible role:** operator

**Instruction:**
Choose the destination by either entering the target code or clicking a square or cell on the map.

**Expected result:**
A destination square, cell, or target code is selected for the AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Map or interface showing selectable destination squares or cells for the Go to action.*


**Stop or Escalate If:**

* Stop if the destination cannot be selected.
* Stop if you are not confident the selected square or cell is the intended target.

---

### Step 5 — Confirm the move

**Responsible role:** operator

**Instruction:**
Select Confirm to send the AGV to the chosen location.

**Expected result:**
The AGV is dispatched to the selected target location.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Confirm action after choosing the destination.*


**Stop or Escalate If:**

* Escalate if the AGV does not navigate to the selected target location after confirmation.
* Escalate if the AGV does not pick up a task after being moved and additional decision logic is needed, because the source does not provide further operator guidance.

---

## Success Criteria

* The intended AGV is selected and a destination square, cell, or target code is chosen.
* The operator confirms the Go-to action.
* The AGV navigates to the selected target location without needing to be physically pushed.

## Failure Conditions

* The AGV is currently in a task.
* The AGV cannot be selected or the Go-to function cannot be used.
* A destination cannot be selected.
* The AGV does not navigate to the selected target location after confirmation.
* The AGV does not pick up a task after being moved and further operator logic is required beyond what the source provides.

## Escalation Guidance

* Do not proceed with this procedure if the AGV is in a task.
* Escalate if the AGV does not move to the selected location after confirmation.
* Escalate if additional recovery logic is needed after repositioning, because the source only provides a limited recovery example and not a full decision tree.

## Missing Details / Known Gaps

* The source does not provide a time estimate for completing the Go-to procedure.
* The source does not define role boundaries beyond operator-facing actions.
* The source does not provide detailed troubleshooting steps if the AGV fails to move after confirmation.
* The source does not provide a complete decision process for what to do if the AGV does not pick up a new task after being moved.
* The source does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_move_idle_agv_with_go_to_function
- Source ID: `training_video_day1`
- Source Type: `training_video`
