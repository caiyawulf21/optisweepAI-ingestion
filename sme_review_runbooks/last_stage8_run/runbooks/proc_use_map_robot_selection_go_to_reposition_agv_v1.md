# Use Map Robot Selection “Go to” to reposition an AGV to a selected square

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_map_robot_selection_go_to_reposition_agv_v1` |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support`, `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS / fleet status UI map’s Robot Selection “Go to” workflow to send an AGV that is not currently in a task to a selected destination square. The source presents this as a quick recovery method for a stalled/blocked situation (example: a tipper goes down and an AGV will not leave; after the tote is removed, the AGV can pick up a new task).

## When To Use

When an AGV is not in a task and you need to recover quickly by sending it to a chosen map square using Robot Selection “Go to” (example use case described: a tipper goes down and an AGV will not leave; after the tote is removed, the AGV can resume by picking up a new task).

## Source Procedure References

- proc_use_map_robot_selection_go_to_reposition_agv_v1

## Procedure Steps

### Step 1 — Open the RMS map view that supports selecting operational objects

**Responsible role:** L1_support

**Instruction:**
In the RMS / fleet status UI, open the map view that allows selecting operational objects (AGVs/cells). Avoid clicking only on the map background.

**Expected result:**
You can select operational objects on the map (AGV/cell selection is recognized by the UI).

---

### Step 2 — Select the specific AGV object on the map

**Responsible role:** L1_support

**Instruction:**
On the RMS map, select the specific AGV object (do not select a generic map area).

**Expected result:**
The selected AGV is identified by the UI as the target for Robot Selection.

---

### Step 3 — Select the Robot Selection “Go to” function for the selected AGV

**Responsible role:** L1_support

**Instruction:**
After selecting the AGV on the RMS map, choose the Robot Selection “Go to” function for that AGV.

**Expected result:**
The UI enters the “Go to” flow for the selected AGV (ready to choose a destination square).

---

### Step 4 — Select the destination square on the map

**Responsible role:** L1_support

**Instruction:**
In the “Go to” flow, select the destination square on the RMS map where you want the AGV to go.

**Expected result:**
A destination square is selected as the target for the AGV “Go to” command.

---

### Step 5 — Select “Confirm” to send the AGV to the selected square

**Responsible role:** L1_support

**Instruction:**
Select “Confirm” to send the selected AGV to the selected destination square.

**Expected result:**
The “Go to” command is confirmed and issued for the selected AGV to the selected square.

---

### Step 6 — Verify AGV resumes tasking after the described recovery condition (e.g., tote removed)

**Responsible role:** L1_support

**Instruction:**
After issuing “Go to” and clearing the described blockage condition (example: tote removed), observe that the AGV resumes by picking up a new task.

**Expected result:**
The AGV picks up a new task after its tote has been removed (as described in the recovery example).

---

## Success Criteria

- The AGV is sent to the chosen map square via Robot Selection “Go to” + “Confirm”.
- In the described recovery scenario, after the tote is removed, the AGV picks up a new task.

## Failure Conditions

- Map action does not take effect (e.g., clicking the map background causes no action).
- AGV does not move / does not resume tasking after the recovery condition described.
- AGV remains unable to leave the area despite using “Go to.”

## Escalation Guidance

- Stop and escalate if the map action does not take effect or if the AGV does not resume tasking after the described recovery condition.
- If the AGV remains unable to leave the area despite using “Go to,” escalate for deeper troubleshooting of the underlying blockage.

## Missing Details / Known Gaps

- The source does not name the exact RMS screen name/menu path for the Robot Selection “Go to” controls; it only describes the workflow and that the map supports selecting operational objects.
