# Reposition An AGV To The Hospital Using Go-to During A Tipper-Down Recovery Example

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reposition_an_agv_to_the_hospital_using_go_to_during_a_tipper_down_recovery_example_v1` |
| Title | Reposition An AGV To The Hospital Using Go-to During A Tipper-Down Recovery Example |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented Go-to recovery example to remove and add an AGV, send it to the hospital, and allow it to resume tasking after tote removal.

## When To Use

Use this source-described recovery example when a tipper goes down and an AGV will not leave, and the operator/support user needs to use the Robot Selection Go-to function to drop the AGV off at the hospital.

## Do Not Use For

* Do not use as a general-purpose AGV recovery procedure outside the specific source example of a tipper-down condition where an AGV will not leave.
* Do not use when the source-required remove-and-add action cannot be performed or is not permitted.
* Do not use as a substitute for procedures that define what to do if the AGV does not move to the selected square or does not pick up a new task after tote removal.

## Safety And Operational Notes

* The source presents this as a quick recovery example and does not define full risk boundaries or fallback controls.
* Do not assume additional movement, floor-entry, or manual handling steps beyond those explicitly stated in the source.
* Escalate if the AGV does not move to the selected square or does not pick up a new task after tote removal.

## Access Or Tools Needed

* Access to the Robot Selection Go-to function
* Ability to remove and add the AGV
* Ability to remove the tote from the AGV

## Related Operational Context

* ctx_training_video_agv_go_to_recovery_use_case_v1

## Procedure Steps

### Step 1 — Identify the AGV for the tipper-down recovery example

**Responsible role:** L1_support

**Instruction:**
Identify the AGV involved in the recovery example where a tipper goes down and the AGV will not leave.

**Expected result:**
The AGV to be recovered is identified for Go-to handling.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The slide text describing the recovery example: a tipper goes down and an AGV will not leave.*


**Stop or Escalate If:**

* The affected AGV cannot be confidently identified.
* The situation does not match the source example of a tipper-down condition where an AGV will not leave.

---

### Step 2 — Remove and add the AGV

**Responsible role:** L1_support

**Instruction:**
Remove and add the AGV, as stated on the training slide.

**Expected result:**
The AGV has been removed and added back in preparation for Go-to recovery.

**Stop or Escalate If:**

* Remove-and-add cannot be completed.
* The source does not provide a fallback if remove and add does not work.

---

### Step 3 — Select the AGV in Robot Selection Go-to

**Responsible role:** L1_support

**Instruction:**
Select the AGV in the Robot Selection Go-to function.

**Expected result:**
The target AGV is selected in Robot Selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The Robot Selection Go-to function and the listed step to select an AGV.*


**Stop or Escalate If:**

* The AGV cannot be selected in Robot Selection.
* There is uncertainty about whether the selected AGV is the affected AGV.

---

### Step 4 — Select Go to

**Responsible role:** L1_support

**Instruction:**
Select Go to.

**Expected result:**
The Go-to action is opened for the selected AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The Go-to step in the Robot Selection workflow.*


**Stop or Escalate If:**

* Go-to is unavailable for the selected AGV.

---

### Step 5 — Select the hospital square

**Responsible role:** L1_support

**Instruction:**
Select the square used to drop the AGV off at the hospital.

**Expected result:**
A hospital destination square is selected for the AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The step to select which square the AGV should go to, in the context of dropping it off at the hospital.*

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*The training frame describing hospital flow and hospital drop-off context.*


**Stop or Escalate If:**

* The correct hospital square is not known from the current source context.
* The AGV destination cannot be selected.

---

### Step 6 — Confirm the Go-to destination

**Responsible role:** L1_support

**Instruction:**
Select Confirm.

**Expected result:**
The Go-to request is confirmed for the selected hospital square.

**Screens / Images:**

![artifact_training_video_training_video_day1_0042_if_you_change_it_to_if_primary_01_35_45_500](assets/e3cc1b23b8636b92.jpg)

*The final Confirm step in the Go-to workflow.*


**Stop or Escalate If:**

* The AGV does not move to the selected square after confirmation.

---

### Step 7 — Remove the tote from the AGV

**Responsible role:** L1_support

**Instruction:**
Remove the tote from the AGV.

**Expected result:**
The tote is removed from the AGV.

**Stop or Escalate If:**

* The tote cannot be removed from the AGV.

---

### Step 8 — Verify the AGV picks up a new task

**Responsible role:** L1_support

**Instruction:**
Verify that the AGV picks up a new task once its tote has been removed.

**Expected result:**
The AGV picks up a new task after tote removal.

**Stop or Escalate If:**

* The AGV does not pick up a new task after tote removal.

---

## Success Criteria

* The AGV is removed and added as described in the source example.
* The AGV is sent to the selected hospital square using Go-to.
* The tote is removed from the AGV.
* The AGV picks up a new task after tote removal.

## Failure Conditions

* The AGV cannot be removed and added.
* The AGV cannot be selected in Robot Selection Go-to.
* The hospital square cannot be selected or confirmed.
* The AGV does not move to the selected square.
* The tote cannot be removed from the AGV.
* The AGV does not pick up a new task after tote removal.

## Escalation Guidance

* Escalate if remove and add does not work, because the source does not define the next action.
* Escalate if the AGV does not move to the selected square.
* Escalate if the AGV does not pick up a new task after tote removal.

## Missing Details / Known Gaps

* The source does not define the exact UI path or screen navigation for opening Robot Selection Go-to.
* The source does not define the exact method for identifying the correct hospital square beyond selecting a square.
* The source does not define what to do if remove and add does not work.
* The source does not define timing expectations for AGV movement or task pickup.
* The source does not define role boundaries, permissions, or safety controls for tote removal.

## Source Lineage

- Candidate IDs: candidate_training_video_reposition_agv_to_hospital_for_tipper_down_recovery
- Source ID: `training_video_day1`
- Source Type: `training_video`
