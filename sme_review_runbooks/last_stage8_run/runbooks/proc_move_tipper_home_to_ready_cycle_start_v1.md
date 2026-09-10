# Move tipper from 'home' to 'ready' by pressing CYCLE START

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_move_tipper_home_to_ready_cycle_start_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

After the tipper axes are homed to the 'home' position, press CYCLE START on the operator station control panel to move the tipper motor from 'home' to 'ready'.

## When To Use

Use when the tipper axes have been homed (Z1/A1 and Z2/A2) and the system is at the 'home' position, and you need to start the tipper operation cycle to move the motor to 'ready'.

## Source Procedure References

- proc_move_tipper_home_to_ready_cycle_start_v1

## Procedure Steps

### Step 1 — Confirm tipper axes are homed to the 'home' position

**Responsible role:** operator

**Instruction:**
Verify the tipper axes are homed so the system is at the 'home' position (Z1/A1 and Z2/A2).

**Expected result:**
The tipper is in the 'home' position state (ready to transition to 'ready' when CYCLE START is pressed).

---

### Step 2 — Press CYCLE START to start the tipper cycle

**Responsible role:** operator

**Instruction:**
On the operator station control panel (Visu_MCP_Dual), press the CYCLE START button.

**Expected result:**
The tipper motor transitions from 'home' to 'ready' after pressing CYCLE START.

---

### Step 3 — Verify motor state changes from 'home' to 'ready'

**Responsible role:** operator

**Instruction:**
Observe the motor state indicator/state text on the operator station HMI to confirm it changes from 'home' to 'ready'.

**Expected result:**
The motor state changes from 'home' to 'ready' after CYCLE START.

---

## Success Criteria

- After pressing CYCLE START, the tipper motor state changes from 'home' to 'ready'.

## Failure Conditions

- CYCLE START does not result in a state change from 'home' to 'ready'.

## Escalation Guidance

- If pressing CYCLE START does not change the state from 'home' to 'ready', stop and escalate.

## Missing Details / Known Gaps

- The packet does not provide the exact HMI label/field name for the 'home' vs 'ready' state indicator; operators should rely on the visible state indication on the operator station HMI.
