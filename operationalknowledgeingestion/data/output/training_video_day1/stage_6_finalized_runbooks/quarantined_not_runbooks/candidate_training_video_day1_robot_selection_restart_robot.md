# Restart a robot using the Robot Selection / Restart Robot screen (robot ID + Restart button)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_restart_robot_robot_selection_restart_robot_v1` |
| Title | Restart a robot using the Robot Selection / Restart Robot screen (robot ID + Restart button) |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state`, `agv_physical_recovery` |
| Access Surface | `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Selection / Restart Robot screen to restart a specific robot by entering/selecting its robot ID, clicking “Restart,” and then verifying the restarted robot appears positioned at the restart point / QR code cell.

## When To Use

When you need to restart a specific robot from the Robot Selection / Restart Robot interface and then confirm it returns to the restart point / QR code cell.

## Safety And Operational Notes

* If the robot does not restart or does not appear at the restart point / QR code cell after clicking “Restart,” stop and escalate (no additional recovery steps are provided in the source).

## Access Or Tools Needed

* Robot Selection / Restart Robot screen
* Robot ID entry field (source example includes “IBGGGE0000”)
* “Restart” button
* On-screen visual confirmation area for the robot at the restart point / QR code cell

## Related Operational Context

* ctx_training_video_robot_restart_screen_reference_v1

## Procedure Steps

### Step 1 — Open the “Robot Selection / Restart Robot” screen

**Responsible role:** L2_support

**Instruction:**
Open the “Robot Selection / Restart Robot” screen.

**Expected result:**
The Robot Selection / Restart Robot screen is open and ready for robot ID selection/entry and restart action.

---

### Step 2 — Enter the corresponding robot ID (or select the robot)

**Responsible role:** L2_support

**Instruction:**
Enter the corresponding robot ID (example shown in the source: “IBGGGE0000”) or select the robot from the available selection.

**Expected result:**
The intended robot is selected/identified on the Robot Selection / Restart Robot screen using its robot ID.

---

### Step 3 — Click “Restart”

**Responsible role:** L2_support

**Instruction:**
Click the “Restart” button on the Robot Selection / Restart Robot screen.

**Expected result:**
The restart action is triggered for the selected robot.

**Stop or Escalate If:**

* If the robot does not restart after clicking “Restart,” stop and escalate.

---

### Step 4 — Wait for the robot to restart (restart point / QR code cell)

**Responsible role:** L2_support

**Instruction:**
Wait for the robot to restart; the source indicates it will be at the restart point or on the QR code cell.

**Expected result:**
The robot has restarted and is positioned at the restart point / QR code cell.

**Stop or Escalate If:**

* If the robot does not appear at the restart point / QR code cell after clicking “Restart,” stop and escalate.

---

### Step 5 — Confirm the restarted robot is displayed on the screen

**Responsible role:** L2_support

**Instruction:**
After starting, confirm the restarted robot that has been positioned is displayed on the Robot Selection / Restart Robot screen (the source references a display area, though the exact label is unclear).

**Expected result:**
The restarted robot is displayed on the screen as positioned at the restart point / QR code cell.

**Stop or Escalate If:**

* If the robot does not restart or does not appear at the restart point / QR code cell after clicking Restart, stop and escalate.

---

## Success Criteria

* Robot restarts after clicking “Restart.”
* Restarted robot is shown positioned at the restart point / QR code cell.
* Restarted robot is displayed on the Robot Selection / Restart Robot screen after starting.

## Failure Conditions

* Robot does not restart after clicking “Restart.”
* Robot does not appear at the restart point / QR code cell after restarting.
* Restarted robot is not displayed on the screen after starting.

## Escalation Guidance

* If the robot does not restart or does not appear at the restart point / QR code cell after clicking “Restart,” stop and escalate (the source does not provide further recovery steps).

## Missing Details / Known Gaps

* The source does not specify the exact navigation path to reach the Robot Selection / Restart Robot screen.
* The source references a post-restart display area on the screen, but the exact UI label text for that area is unclear due to garbled OCR.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_robot_selection_restart_robot
- Source ID: `training_video_day1`
- Source Type: `training_video`
