# Add a Robot Using the Robot Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_add_a_robot_using_the_robot_selection_screen_v1` |
| Title | Add a Robot Using the Robot Selection Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Selection Add and Remove screen to add a robot by entering the corresponding robot ID, clicking Add, and confirming the system reports that the add was successful.

## When To Use

Use when a robot needs to be added through the Robot Selection Add and Remove interface and the operator has the corresponding robot ID.

## Access Or Tools Needed

* Access to the Robot Selection Add and Remove screen
* Corresponding robot ID

## Related Operational Context

* ctx_training_video_robot_selection_add_remove_screen_v1
* ctx_training_video_robot_id_reference_v1
* ctx_training_video_robot_add_remove_success_status_v1

## Procedure Steps

### Step 1 — Open or locate the Robot Selection Add and Remove screen

**Responsible role:** operator

**Instruction:**
Open or locate the "Robot Selection Add and Remove" screen.

**Expected result:**
The Robot Selection Add and Remove screen is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0030_all_right_we_re_continuing_with_primary_01_17_03_000](assets/07de2d052b490f62.jpg)

*Screen title "Robot Selection Add and Remove" and the Add Robot area with robot ID entry and Add button.*


**Stop or Escalate If:**

* Stop and escalate if the Robot Selection Add and Remove screen is not available or cannot be located.

---

### Step 2 — Enter the corresponding robot ID

**Responsible role:** operator

**Instruction:**
In the Add Robot section, enter the corresponding robot ID.

**Expected result:**
The robot ID is entered in the Add Robot input field.

**Screens / Images:**

![artifact_training_video_training_video_day1_0030_all_right_we_re_continuing_with_primary_01_17_03_000](assets/07de2d052b490f62.jpg)

*Add Robot section and robot ID entry field.*


**Stop or Escalate If:**

* Stop and escalate if the corresponding robot ID is not available.
* Stop and escalate if the robot ID field does not accept input.

---

### Step 3 — Click Add

**Responsible role:** operator

**Instruction:**
Click "Add."

**Expected result:**
The system processes the add request.

**Screens / Images:**

![artifact_training_video_training_video_day1_0030_all_right_we_re_continuing_with_primary_01_17_03_000](assets/07de2d052b490f62.jpg)

*Add button in the Add Robot section.*


**Stop or Escalate If:**

* Stop and escalate if the Add button is unavailable or does not respond.

---

### Step 4 — Verify the add was successful

**Responsible role:** operator

**Instruction:**
Verify that the system shows that the adding was successful.

**Expected result:**
The system shows a success indication for the add action.

**Screens / Images:**

![artifact_training_video_training_video_day1_0030_all_right_we_re_continuing_with_primary_01_17_03_000](assets/07de2d052b490f62.jpg)

*Success indication associated with the Add Robot action.*


**Stop or Escalate If:**

* Stop and escalate if the system does not show that the adding was successful, because the source does not provide additional recovery steps.

---

## Success Criteria

* The corresponding robot ID is entered in the Add Robot section.
* The Add action is performed.
* The system shows that the adding was successful.

## Failure Conditions

* The Robot Selection Add and Remove screen cannot be located.
* The corresponding robot ID cannot be entered.
* The Add action cannot be completed.
* The system does not show that the adding was successful.

## Escalation Guidance

* If the system does not show that the adding was successful, stop and escalate because the source does not provide additional recovery steps.

## Missing Details / Known Gaps

* The source segment does not provide explicit navigation steps for reaching the Robot Selection Add and Remove screen.
* The source does not define when to add a robot versus when not to use this procedure.
* The source does not specify the exact wording or location of the success indication.
* The source does not provide recovery steps if the add action fails.
* The source does not provide role boundaries beyond basic operator use.
* The source does not provide time estimates, production stop requirements, or LOTO requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_add_robot_by_robot_id
- Source ID: `training_video_day1`
- Source Type: `training_video`
