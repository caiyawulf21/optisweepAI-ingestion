# Manually Open/Close Tipper Grippers Using VISU_MANCONTROL

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_manually_open_close_tipper_grippers_visu_mancontrol_v1` |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the Operator Station HMI maintenance manual control screen VISU_MANCONTROL, use the GRIPPERS OPEN/CLOSE button for the corresponding tipper (LEFT or RIGHT) to manually command the gripper to open or close, then verify the physical gripper state changes accordingly.

## When To Use

Use when you need to manually actuate a specific tipper gripper (LEFT or RIGHT) via the Operator Station HMI maintenance manual control screen VISU_MANCONTROL.

## Source Procedure References

- proc_manually_open_close_tipper_grippers_visu_mancontrol_v1

## Safety And Operational Notes

- If there is imminent danger to personnel or risk of equipment damage, use the appropriate safety response (the manual includes an emergency stop push-button on the operator station push-button panel).

## Procedure Steps

### Step 1 — Open the VISU_MANCONTROL manual control screen

**Responsible role:** L2_support

**Instruction:**
On the Operator Station HMI, navigate to the maintenance manual control screen named VISU_MANCONTROL.

**Expected result:**
The VISU_MANCONTROL screen is displayed with the GRIPPERS OPEN/CLOSE button for the corresponding tipper.

---

### Step 2 — Command the LEFT or RIGHT tipper gripper to open or close

**Responsible role:** L2_support

**Instruction:**
On VISU_MANCONTROL, select the corresponding tipper side (LEFT or RIGHT) and press the GRIPPERS OPEN/CLOSE button to command the gripper to open or close.

**Expected result:**
A manual open/close command is issued for the selected tipper gripper via the GRIPPERS OPEN/CLOSE button.

---

### Step 3 — Verify physical gripper state matches the command

**Responsible role:** L2_support

**Instruction:**
Physically observe the corresponding tipper and confirm the gripper changes state to match the command (open vs closed).

**Expected result:**
The corresponding tipper gripper opens or closes in response to the GRIPPERS OPEN/CLOSE button command.

---

### Step 4 — Escalate if the gripper does not respond

**Responsible role:** L2_support

**Instruction:**
If the gripper does not move to the commanded open/closed state, stop the attempt and escalate.

**Expected result:**
Escalation is initiated due to lack of physical response to the open/close command.

---

## Success Criteria

- After pressing GRIPPERS OPEN/CLOSE for the selected tipper side, the corresponding tipper gripper physically opens or closes to match the command.

## Failure Conditions

- Physical gripper does not move to the commanded open/closed state after pressing GRIPPERS OPEN/CLOSE.

## Escalation Guidance

- Escalate if the gripper does not respond to the open/close command.

## Missing Details / Known Gaps

- The manual evidence in this packet does not specify any on-screen gripper status field/indicator to use as an observable confirmation; verification is therefore based on physical observation only.
