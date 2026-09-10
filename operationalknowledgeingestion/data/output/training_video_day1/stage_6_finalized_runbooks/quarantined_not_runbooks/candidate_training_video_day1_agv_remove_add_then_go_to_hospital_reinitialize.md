# Recover an AGV by removing and adding it, then sending it to the hospital using Go-to so it drops, reinitializes, and picks up a new tote

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_agv_remove_add_go_to_hospital_v1` |
| Title | Recover an AGV by removing and adding it, then sending it to the hospital using Go-to so it drops, reinitializes, and picks up a new tote |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery`, `robot_command_or_task_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `operator` |
| Failure Pattern Tags | `mapping_abnormal`, `robot_task_or_command_stuck` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

If an AGV is in a green/ready state but not picking up a task, use the Robot Selection remove-and-add sequence so the tote enters the “question mark” state. Then use the Robot Selection Go-to function to send the AGV to the hospital drop-off location. After you remove the tote at the hospital, the AGV drops, reinitializes, and returns to pick up a new tote. The source also notes that WCS may not reinitialize the AGV if the tote remains in an improper binding state after remove/add; sending to the hospital and removing the tote is the recovery path.

## When To Use

Use when an AGV is not picking up a task and is described as being in a green state (ready to execute something but without a task). The recovery sequence is specifically described as: remove and add the AGV so totes enter the “question mark” state, then use Go-to to send the AGV to the hospital so it can drop, reinitialize, and pick up a new tote.

## Access Or Tools Needed

* OptiSweep Robot Selection screen
* Remove and add controls for the AGV (as referenced by the segment)
* Go-to function controls
* Map/cell selection for the hospital destination
* Ability to remove the tote at the hospital location

## Related Operational Context

* ctx_training_video_hospital_dropoff_recovery_context_v1
* ctx_training_video_wcs_reinitialize_binding_context_v1

## Procedure Steps

### Step 1 — Identify the AGV that is in the documented green state but not picking up a task

**Responsible role:** operator

**Instruction:**
On the OptiSweep Robot Selection screen, select the AGV and verify it is in the described green state (robot not in a task).

**Expected result:**
The selected AGV shows the described “Green: robot not in a task” condition, indicating it is ready to execute something but currently has no task.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*Robot status color legend: Green = robot not in a task; also use the robot selection details panel to confirm you selected the correct robot ID/location.*


---

### Step 2 — Remove and add the AGV so the totes enter the “question mark” state

**Responsible role:** operator

**Instruction:**
Perform the source-described remove-and-add action for the selected AGV so the totes enter the “question mark” state.

**Expected result:**
After remove/add, the tote associated with the AGV shows a “?” (question mark) before it, indicating the robot was removed but the tote has not (as described by the source).

---

### Step 3 — Use Go-to to send the AGV to the hospital drop-off location

**Responsible role:** operator

**Instruction:**
On the OptiSweep Robot Selection screen, use the Go-to function: select the AGV, select Go to, select the hospital destination square by clicking on the map/cell, then select Confirm.

**Expected result:**
The Go-to action is confirmed for the selected AGV with a hospital destination selected on the map, so the AGV navigates to the hospital drop-off area.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*Go-to UI steps: Select AGV -> Select Go to -> Select which square -> Select Confirm.*


---

### Step 4 — At the hospital, remove the tote from the AGV

**Responsible role:** operator

**Instruction:**
Once the AGV arrives at the hospital, remove the tote from the AGV at the hospital location.

**Expected result:**
The tote is removed from the AGV at the hospital.

**Stop or Escalate If:**

* Escalate if you cannot get the tote removed at the hospital.

---

### Step 5 — Observe the AGV: it should drop, reinitialize, and return to pick up a new tote

**Responsible role:** operator

**Instruction:**
After tote removal at the hospital, observe the AGV behavior/state until it drops, reinitializes, and comes back to pick up a new tote.

**Expected result:**
The AGV drops, reinitializes, and returns to pick up a new tote.

**Stop or Escalate If:**

* Escalate if the AGV does not drop/reinitialize after tote removal.

---

## Success Criteria

* After sending to the hospital and removing the tote there, the AGV drops, reinitializes, and returns to pick up a new tote.

## Failure Conditions

* WCS does not reinitialize the AGV after remove/add because the tote remains in an improper binding state.
* You cannot remove the tote at the hospital.
* AGV does not drop/reinitialize after tote removal.

## Escalation Guidance

* If you cannot get the tote removed at the hospital, escalate.
* If the AGV does not drop/reinitialize after tote removal, escalate.
* If remove/add alone does not lead to proper reinitialization, follow the source’s hospital-based recovery path (hospital drop-off + tote removal) because WCS will not reinitialize until the tote is removed and added again.

## Missing Details / Known Gaps

* The packet does not provide exact UI label text for the remove/add controls on the Robot Selection screen; steps therefore use source-described remove/add actions without exact button names.
* The packet does not provide the exact map/cell label text for the hospital destination square; steps therefore instruct selecting the hospital destination square by clicking on the map/cell.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_agv_remove_add_then_go_to_hospital_reinitialize
- Source ID: `training_video_day1`
- Source Type: `training_video`
