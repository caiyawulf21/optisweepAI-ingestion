# Send an AGV to a selected square using Robot Selection → Go-to (Confirm) and verify AGV info updates

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_send_agv_to_selected_square_robot_selection_goto_confirm_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the live OptiSweep interface object selection to select an AGV (cell phone/object icon) so the AGV information panel updates, then use Go-to → select a destination square → Confirm to send an AGV that is not in a task to the selected square (example recovery: drop it off at the hospital).

## When To Use

When you need to recover an AGV quickly by sending it to a chosen square using Go-to, specifically described for an AGV that is “not in a task.”

## Source Procedure References

- proc_send_agv_to_selected_square_robot_selection_goto_confirm_v1

## Procedure Steps

### Step 1 — Open the live interface and use Robot Selection to select an AGV object

**Responsible role:** operator

**Instruction:**
Open the live OptiSweep interface that supports “Robot Selection.” Under the AGV view, select the AGV object (the segment references selecting a “cell phone” icon).

**Expected result:**
After selecting the AGV object (cell phone), the interface shows the AGV information.

---

### Step 2 — Select Go-to for the selected AGV

**Responsible role:** operator

**Instruction:**
With the AGV selected, select the “Go to” function for that AGV.

**Expected result:**
The Go-to function is selected/active for the selected AGV (ready for destination square selection).

---

### Step 3 — Select the destination square on the map/grid

**Responsible role:** operator

**Instruction:**
Select the destination square on the map/grid for where you want the AGV to go.

**Expected result:**
The destination square selection is made (the chosen square is the target for the Go-to request).

---

### Step 4 — Confirm the Go-to request

**Responsible role:** operator

**Instruction:**
Select “Confirm” to submit the Go-to request.

**Expected result:**
The Go-to request is submitted via Confirm.

---

### Step 5 — Verify the AGV is routed to the selected square (recovery example: hospital drop-off)

**Responsible role:** operator

**Instruction:**
Observe that the AGV is now being routed to the selected square (example recovery use: drop it off at the hospital).

**Expected result:**
The interface/system reflects that the AGV is being routed to the selected square; example: hospital drop-off use case.

---

## Success Criteria

- After selecting the AGV object (cell phone), the AGV information panel updates/shows AGV information.
- After Go-to → destination square → Confirm, the system reflects that the AGV is being routed to the selected square.

## Failure Conditions

- Selecting the AGV object does not display AGV information.
- Go-to cannot be confirmed.
- After Confirm, the AGV does not reflect movement/routing toward the selected square.

## Escalation Guidance

- If AGV information does not display after selecting the AGV object, stop and escalate for assistance.
- If Go-to cannot be confirmed or the AGV does not reflect movement/routing toward the selected square, stop and escalate for assistance.

## Missing Details / Known Gaps

- The packet does not explicitly name the exact live UI surface (e.g., RMS vs another HMI) that contains “Robot Selection” and “Go to”; it only references the UI labels in the training segment.
- The packet does not specify the exact observable routing indicator (e.g., map highlight, status text, or AGV icon behavior) beyond the general expectation that the AGV is routed toward the selected square.
