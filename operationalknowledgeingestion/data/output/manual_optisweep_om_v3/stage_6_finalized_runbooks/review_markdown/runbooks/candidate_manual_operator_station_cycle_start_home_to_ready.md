# Move tipper from 'home' to 'ready' by pressing CYCLE START

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_move_tipper_home_to_ready_cycle_start_v1` |
| Title | Move tipper from 'home' to 'ready' by pressing CYCLE START |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

After the tipper axes are homed to the 'home' position, press CYCLE START on the operator station control panel to move the tipper motor from 'home' to 'ready'.

## When To Use

Use when the tipper axes have been homed (Z1/A1 and Z2/A2) and the system is at the 'home' position, and you need to start the tipper operation cycle to move the motor to 'ready'.

## Access Or Tools Needed

* Operator station HMI screen/control panel with CYCLE START and home/ready state indication

## Related Operational Context

* ctx_manual_tipper_cycle_start_ready_v1

## Visual References

![artifact_fig_4_19_operator_station_control_panel](assets/02aaee46093b117e.png)

*Operator Station Control Panel (Visu_MCP_Dual screen) showing the CYCLE START button and other tipper controls.*

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Operator station main screen image used in the startup procedure that includes the step to press CYCLE START and the expected 'home' to 'ready' movement.*

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

**Stop or Escalate If:**

* If pressing CYCLE START does not change the state from 'home' to 'ready', stop and escalate.

---

### Step 3 — Verify motor state changes from 'home' to 'ready'

**Responsible role:** operator

**Instruction:**
Observe the motor state indicator/state text on the operator station HMI to confirm it changes from 'home' to 'ready'.

**Expected result:**
The motor state changes from 'home' to 'ready' after CYCLE START.

**Stop or Escalate If:**

* If the state does not change from 'home' to 'ready', stop and escalate.

---

## Success Criteria

* After pressing CYCLE START, the tipper motor state changes from 'home' to 'ready'.

## Failure Conditions

* CYCLE START does not result in a state change from 'home' to 'ready'.

## Escalation Guidance

* If pressing CYCLE START does not change the state from 'home' to 'ready', stop and escalate.

## Missing Details / Known Gaps

* The packet does not provide the exact HMI label/field name for the 'home' vs 'ready' state indicator; operators should rely on the visible state indication on the operator station HMI.

## Source Lineage

- Candidate IDs: candidate_manual_operator_station_cycle_start_home_to_ready
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
