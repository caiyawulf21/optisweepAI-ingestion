# Recover A Stuck AGV By Using Go-to To Send It To The Hospital Drop-off Area

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_a_stuck_agv_by_using_go_to_to_send_it_to_the_hospital_drop_off_area_v1` |
| Title | Recover A Stuck AGV By Using Go-to To Send It To The Hospital Drop-off Area |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Source-specific recovery example from training: when a tipper goes down and an AGV will not leave, the slide instructs the user to remove and add the AGV, then use the Go-to function to send it to the hospital drop-off area. The AGV is expected to pick up a new task once its tote has been removed.

## When To Use

Use this source-described recovery example when a tipper disruption leaves an AGV stuck and the AGV will not leave, and the interface provides the AGV selection and Go-to controls needed to send the AGV to the hospital drop-off area.

## Do Not Use For

* Do not use as a complete remove-and-add procedure; the source references that action but does not define how to perform it.
* Do not use if the hospital drop-off square cannot be identified from the interface or local documentation.
* Do not use as a general AGV removal authorization; the source packet does not define permissions or approval requirements for remove/add.

## Safety And Operational Notes

* This runbook is based on a training example and is incomplete for the remove-and-add portion; use SME review before operational reliance.
* The source does not define the exact remove-and-add procedure for the AGV.
* Escalate if required controls are unavailable or unclear in the interface.

## Access Or Tools Needed

* Access to the robot or object selection interface
* Ability to select the AGV
* Go to function in the interface
* Knowledge of the hospital drop-off square
* Ability to remove the tote from the AGV

## Related Operational Context

* ctx_training_video_agv_object_selection_v1
* ctx_training_video_agv_recovery_hospital_dropoff_v1

## Procedure Steps

### Step 1 — Select the AGV in the object selection view

**Responsible role:** L1_support

**Instruction:**
In the robot or object selection view, select the AGV involved so its AGV information is displayed.

**Expected result:**
The selected AGV is highlighted or otherwise selected in the interface and AGV information is shown.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*AGV object selection behavior and AGV information shown after selecting the AGV.*


**Stop or Escalate If:**

* The AGV cannot be located in the robot or object selection view.
* Selecting the AGV does not display AGV information.

---

### Step 2 — Remove and add the AGV if following the recovery example

**Responsible role:** L1_support

**Instruction:**
If using the source example recovery, remove and add the AGV as stated on the slide before using Go-to.

**Expected result:**
The AGV has been removed and added back as required by the source example.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*Recovery example text stating to remove and add the AGV before using Go-to.*


**Stop or Escalate If:**

* The remove-and-add procedure is not already known or available in the interface.
* You do not have the required authorization to perform remove/add.

---

### Step 3 — Select the Go to function

**Responsible role:** L1_support

**Instruction:**
Select the Go to function for the AGV.

**Expected result:**
The Go to control is activated for the selected AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*Go to control in the robot selection workflow.*


**Stop or Escalate If:**

* The Go to function is not present for the selected AGV.
* The interface does not allow the Go to action.

---

### Step 4 — Select the hospital drop-off square

**Responsible role:** L1_support

**Instruction:**
Select the square used for the hospital drop-off location, as referenced by the slide example.

**Expected result:**
The hospital drop-off square is selected as the AGV destination.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*Step on the slide indicating square selection for the Go to destination.*


**Stop or Escalate If:**

* The hospital drop-off square is not identifiable from the interface or local documentation.
* The selected square does not appear to correspond to the hospital drop-off area.

---

### Step 5 — Confirm the Go to destination

**Responsible role:** L1_support

**Instruction:**
Select Confirm to send the AGV to the selected hospital drop-off square.

**Expected result:**
The Go to action is confirmed and the AGV is sent toward the selected hospital drop-off location.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*Confirm step in the Go to workflow.*


**Stop or Escalate If:**

* Confirm is unavailable.
* The AGV does not accept or begin the directed move after confirmation.

---

### Step 6 — Remove the tote so the AGV can resume tasking

**Responsible role:** L1_support

**Instruction:**
Remove the tote from the AGV, because the slide states the AGV will pick up a new task once its tote has been removed.

**Expected result:**
The tote is removed from the AGV and the AGV can pick up a new task.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*Recovery example text stating the AGV will pick up a new task once its tote has been removed.*


**Stop or Escalate If:**

* The tote cannot be removed.
* The AGV does not pick up a new task after tote removal.

---

## Success Criteria

* The affected AGV is selected and AGV information is displayed.
* The Go to function is used to send the AGV to the hospital drop-off square.
* The tote is removed from the AGV.
* The AGV picks up a new task after tote removal.

## Failure Conditions

* The AGV cannot be selected or AGV information does not display.
* The remove-and-add action is not known, available, or authorized.
* The Go to function is unavailable.
* The hospital drop-off square cannot be identified.
* The AGV does not move to the selected destination after confirmation.
* The AGV does not pick up a new task after tote removal.

## Escalation Guidance

* Escalate if the remove-and-add procedure is not already known or available in the interface.
* Escalate if the hospital drop-off square is not identifiable from the available interface or local documentation.
* Escalate if the AGV does not pick up a new task after tote removal.
* Escalate for SME review because the source provides an example recovery but not a complete operational procedure for all actions.

## Missing Details / Known Gaps

* The source does not define the exact procedure for removing and adding the AGV.
* The source does not identify the exact hospital drop-off square or how to determine it in the interface.
* The source does not provide explicit permissions, approvals, or role boundaries for remove/add actions.
* The source does not provide timing expectations for the AGV to arrive or pick up a new task.

## Source Lineage

- Candidate IDs: candidate_training_video_recover_agv_by_sending_to_hospital_dropoff
- Source ID: `training_video_day1`
- Source Type: `training_video`
