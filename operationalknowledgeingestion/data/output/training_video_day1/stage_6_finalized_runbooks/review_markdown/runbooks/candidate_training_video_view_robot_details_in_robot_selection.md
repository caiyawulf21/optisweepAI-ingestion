# View Robot Details In The Robot Selection Panel

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_robot_details_in_the_robot_selection_panel_v1` |
| Title | View Robot Details In The Robot Selection Panel |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot view in OptiSweep to select a robot, confirm the robot is highlighted, expand the robot detail section if it is hidden, and review the displayed robot information such as robot ID, location, and node code.

## When To Use

Use this procedure when you need to identify a robot in the OptiSweep Robot view and review its displayed details, including robot ID, location, and node code/cell code. This is appropriate for normal HMI usage and issue identification.

## Do Not Use For

* Do not use this procedure to assume robot identity without confirming the robot ID shown in the detail panel.
* Do not use this procedure for robot restart, robot movement, or recovery actions not described in this source.

## Safety And Operational Notes

* Do not assume robot identity without confirming the robot ID shown in the detail panel.
* If the detail section cannot be shown or the robot details are not visible, stop and escalate for support.

## Access Or Tools Needed

* Access to the OptiSweep Robot view
* Robot selection panel
* Robot detail panel

## Related Operational Context

* ctx_training_video_robot_selection_panel_overview_v1
* ctx_training_video_robot_detail_fields_v1

## Procedure Steps

### Step 1 — Open the Robot option

**Responsible role:** operator

**Instruction:**
Open the Robot option in the OptiSweep interface.

**Expected result:**
The Robot view is displayed and available for robot selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*Robot selection overview screen showing the Robot option context and robot selection panel.*


**Stop or Escalate If:**

* Stop and escalate if the Robot option cannot be opened.

---

### Step 2 — Select a robot

**Responsible role:** operator

**Instruction:**
Click on a robot in the Robot view.

**Expected result:**
The selected robot becomes the active robot for detail review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*A robot object in the Robot view that can be clicked to display details.*


**Stop or Escalate If:**

* Stop and escalate if clicking a robot does not allow the robot to be selected.

---

### Step 3 — Confirm the robot is highlighted as selected

**Responsible role:** operator

**Instruction:**
Verify the selected robot has a box around it showing it is selected.

**Expected result:**
A box appears around the selected robot.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*The selected robot should have a box around it indicating selection.*


**Stop or Escalate If:**

* Stop and escalate if the selected robot is not visibly boxed or selection cannot be confirmed.

---

### Step 4 — Expand the robot detail section if hidden

**Responsible role:** operator

**Instruction:**
If the detail section is hidden, click the small arrow to expand the robot detail information.

**Expected result:**
The robot detail section opens and the robot information becomes visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*The small arrow used to expand the hidden robot detail section.*


**Stop or Escalate If:**

* Stop and escalate if the detail section cannot be shown.
* Stop and escalate if robot details are not visible after using the expand control.

---

### Step 5 — Review the displayed robot details

**Responsible role:** operator

**Instruction:**
Review the displayed robot details, including robot ID, location, and node code.

**Expected result:**
The robot detail panel shows the selected robot's identifying and location-related fields.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*Robot detail fields including robot ID, location, node code/cell code, and tote ID when present.*


**Stop or Escalate If:**

* Stop and escalate if robot details are not visible.
* Stop and escalate if the expected identifying fields cannot be reviewed.

---

### Step 6 — Record robot ID and location if identifying an issue

**Responsible role:** operator

**Instruction:**
Record the robot ID and location if you are identifying which robot is associated with an issue.

**Expected result:**
The robot ID and location are documented for the issue being investigated.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*The robot ID and location fields in the robot detail panel before recording them.*


**Stop or Escalate If:**

* Stop and escalate if robot identity cannot be confirmed from the detail panel.
* Do not proceed if you would be assuming robot identity without confirming the robot ID shown.

---

## Success Criteria

* The Robot view is open.
* A robot is selected in the Robot view.
* The selected robot is shown with a box around it.
* The robot detail section is visible.
* Robot ID, location, and node code/cell code can be reviewed for the selected robot.

## Failure Conditions

* The Robot view cannot be opened.
* A robot cannot be selected.
* The selected robot is not visibly highlighted with a box.
* The detail section cannot be expanded or shown.
* Robot details are not visible or key fields cannot be reviewed.
* Robot identity would have to be assumed without confirmation from the detail panel.

## Escalation Guidance

* Escalate for support if the detail section cannot be shown.
* Escalate for support if robot details are not visible.
* Escalate if the interface does not clearly show which robot is selected.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not specify supporting roles beyond the operator.
* The source does not state whether production stop or LOTO is required.
* The source does not provide commands.
* The source section text is empty in the packet; evidence is derived from source refs, artifact retrieval text, and context records.

## Source Lineage

- Candidate IDs: candidate_training_video_view_robot_details_in_robot_selection
- Source ID: `training_video_day1`
- Source Type: `training_video`
