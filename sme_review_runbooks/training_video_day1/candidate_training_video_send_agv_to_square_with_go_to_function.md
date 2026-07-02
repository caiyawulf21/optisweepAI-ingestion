# Send An AGV To A Selected Square Using The Go-to Function

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_send_an_agv_to_a_selected_square_using_the_go_to_function_v1` |
| Title | Send An AGV To A Selected Square Using The Go-to Function |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Selection Go-to function to send an AGV that is not in a task to a selected square. The training source presents this as a basic operator workflow and notes it can be helpful for quick recovery or repositioning.

## When To Use

Use when an AGV is not in a task and needs to be sent to a selected square using the Robot Selection Go-to function. The source also presents this as helpful for quick recovery, including a case where a tipper goes down and an AGV will not leave.

## Do Not Use For

* Do not use when the AGV is in a task.

## Safety And Operational Notes

* The source states the AGV must not be in a task before using the Go-to function.
* Do not invent alternate movement or recovery actions beyond the documented Go-to steps.

## Access Or Tools Needed

* Access to the Robot Selection Go-to function
* Ability to select an AGV and destination square

## Related Operational Context

* ctx_training_video_agv_go_to_recovery_use_case_v1

## Procedure Steps

### Step 1 — Open the Robot Selection Go-to function

**Responsible role:** operator

**Instruction:**
Open the Robot Selection Go-to function in the interface before attempting to select an AGV or destination square.

**Expected result:**
The Robot Selection Go-to function is visible and ready for AGV selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*Robot Selection Go-to function title and the listed workflow steps on the training slide.*


**Stop or Escalate If:**

* Stop or escalate if the Robot Selection Go-to function cannot be opened or accessed.

---

### Step 2 — Select an AGV

**Responsible role:** operator

**Instruction:**
Select an AGV in the Robot Selection Go-to function. Ensure the AGV is not in a task before proceeding.

**Expected result:**
The intended AGV is selected in the interface.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The slide step that instructs the user to select an AGV.*


**Stop or Escalate If:**

* Stop or escalate if the AGV cannot be selected.
* Stop or escalate if the AGV is in a task.

---

### Step 3 — Select Go to

**Responsible role:** operator

**Instruction:**
After selecting the AGV, select Go to.

**Expected result:**
The interface advances to destination selection for the selected AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The slide step that instructs the user to select Go to.*


**Stop or Escalate If:**

* Stop or escalate if the Go to option cannot be selected.

---

### Step 4 — Select the destination square

**Responsible role:** operator

**Instruction:**
Select which square you want the AGV to go to.

**Expected result:**
A destination square is selected for the AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The slide step that instructs the user to select which square the AGV should go to.*


**Stop or Escalate If:**

* Stop or escalate if the destination square cannot be selected.

---

### Step 5 — Confirm the move

**Responsible role:** operator

**Instruction:**
Select Confirm.

**Expected result:**
The selected AGV is sent to the chosen square.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The slide step that instructs the user to select Confirm.*


**Stop or Escalate If:**

* Stop or escalate if the AGV cannot be sent using the documented Go-to steps.

---

## Success Criteria

* The selected AGV is sent to the chosen square.
* The Go-to workflow is completed by selecting an AGV, selecting Go to, selecting a square, and selecting Confirm.

## Failure Conditions

* The Robot Selection Go-to function cannot be accessed.
* The AGV is in a task.
* The AGV cannot be selected.
* The destination square cannot be selected.
* The AGV cannot be sent using the documented Go-to steps.

## Escalation Guidance

* Escalate if the AGV cannot be selected.
* Escalate if the AGV cannot be sent using the documented Go-to steps.

## Missing Details / Known Gaps

* The source does not provide a time estimate.
* The source does not specify production stop requirements.
* The source does not specify LOTO requirements.
* The source does not document exact UI navigation beyond the Go-to workflow steps.
* The source does not provide explicit confirmation text or status indicators after the move is submitted.

## Source Lineage

- Candidate IDs: candidate_training_video_send_agv_to_square_with_go_to_function
- Source ID: `training_video_day1`
- Source Type: `training_video`
