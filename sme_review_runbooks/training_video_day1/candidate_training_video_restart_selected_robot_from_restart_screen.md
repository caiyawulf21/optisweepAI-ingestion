# Restart A Selected Robot From The Robot Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_restart_a_selected_robot_from_the_robot_selection_screen_v1` |
| Title | Restart A Selected Robot From The Robot Selection Screen |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Selection / Restart Robot interface to select a robot and initiate a restart when the documented position requirement is met.

## When To Use

Use this procedure when a selected robot needs to be restarted through the Robot Selection / Restart Robot interface and the robot is at the documented restart point or on the QR code cell.

## Do Not Use For

* Do not use when the robot is not at the restart point or on the QR code cell.
* Do not use this runbook to add or remove robots.
* Do not add undocumented prerequisites or recovery branches beyond the OCR-supported steps.

## Safety And Operational Notes

* Only restart the robot when it is at the restart point or on the QR code cell, as stated in the source.
* Escalate if the robot is not at the required position before restart.
* This procedure is based on OCR-visible training slide content and should receive SME review before operational reliance.

## Access Or Tools Needed

* Access to the Robot Selection / Restart Robot screen
* Robot ID or ability to select the robot in the interface

## Related Operational Context

* ctx_training_video_robot_restart_screen_reference_v1

## Procedure Steps

### Step 1 — Open the Robot Selection / Restart Robot screen

**Responsible role:** L2_support

**Instruction:**
Open the Robot Selection / Restart Robot screen.

**Expected result:**
The Robot Selection / Restart Robot interface is visible and available for use.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*Robot Selection / Restart Robot interface shown on the training slide.*


**Stop or Escalate If:**

* The Robot Selection / Restart Robot screen cannot be accessed or is not available as shown in the source.

---

### Step 2 — Select the robot by ID or from the screen

**Responsible role:** L2_support

**Instruction:**
Enter the corresponding robot ID or select the robot from the screen.

**Expected result:**
The intended robot is selected in the interface for restart.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*Robot ID entry or robot selection area on the Robot Selection / Restart Robot slide.*


**Stop or Escalate If:**

* The correct robot cannot be identified or selected.

---

### Step 3 — Verify the robot is at the restart point or on the QR code cell

**Responsible role:** L2_support

**Instruction:**
Verify the documented position requirement that the robot is at the restart point or on the QR code cell before restart.

**Expected result:**
The robot is confirmed to be at the restart point or on the QR code cell.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*Slide text referencing the restart point or QR code cell requirement.*


**Stop or Escalate If:**

* The robot is not at the restart point.
* The robot is not on the QR code cell.
* The required position cannot be verified from available information.

---

### Step 4 — Click Restart

**Responsible role:** L2_support

**Instruction:**
Click Restart.

**Expected result:**
The restart action is issued for the selected robot.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*Restart control on the Robot Selection / Restart Robot slide.*


**Stop or Escalate If:**

* The Restart action is unavailable.
* The Restart action does not proceed as expected.

---

### Step 5 — Confirm the robot restarts and is displayed after starting

**Responsible role:** L2_support

**Instruction:**
Observe that the robot restarts and that the positioned robot is displayed after starting, as indicated by the slide OCR.

**Expected result:**
The selected robot restarts and the positioned robot is displayed after starting.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*Post-restart display expectation referenced by the training slide OCR.*


**Stop or Escalate If:**

* The robot does not restart.
* The robot is not displayed as expected after starting.

---

## Success Criteria

* The intended robot is selected in the Robot Selection / Restart Robot interface.
* The robot meets the documented position requirement of being at the restart point or on the QR code cell before restart.
* The Restart action is initiated successfully.
* The robot restarts and the positioned robot is displayed after starting.

## Failure Conditions

* The Robot Selection / Restart Robot screen cannot be accessed.
* The correct robot cannot be selected.
* The robot is not at the restart point or on the QR code cell.
* The Restart action cannot be completed.
* The robot does not restart or is not displayed as expected after starting.

## Escalation Guidance

* Escalate if the robot is not at the restart point or QR code cell, because the source ties restart to that position requirement.
* Escalate if the robot does not restart or is not displayed as expected after the restart action.
* Escalate if the required screen is unavailable or the correct robot cannot be selected.
* Do not add undocumented prerequisites or recovery branches beyond the OCR-supported steps.

## Missing Details / Known Gaps

* The source does not provide a documented navigation path to reach the Robot Selection / Restart Robot screen.
* The source does not specify exact confirmation text, status indicators, or messages after clicking Restart.
* The source does not provide a time estimate for the restart.
* The source does not define additional role boundaries beyond the inferred L2_support assignment.
* The source does not provide commands, system paths, or alternate recovery branches.
* The source section text is empty in the packet; the procedure is grounded primarily in OCR-derived slide evidence and artifact metadata.

## Source Lineage

- Candidate IDs: candidate_training_video_restart_selected_robot_from_restart_screen
- Source ID: `training_video_day1`
- Source Type: `training_video`
