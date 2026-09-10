# Reset a LEFT/RIGHT Tipper Fault From the VISU_MANCONTROL Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_left_right_tipper_fault_from_visu_mancontrol_v1` |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the Operator Station HMI VISU_MANCONTROL screen, use the LEFT/RIGHT TIPPER FAULT RESET button to clear the corresponding left or right tipper fault. Then verify the VISU_MANCONTROL informational banner/message area updates to reflect the reset (fault-related message cleared or replaced with a normal informational state).

## When To Use

Use when a LEFT or RIGHT tipper fault is indicated on the Operator Station HMI VISU_MANCONTROL screen and you need to reset the corresponding tipper fault using the screen’s manual control.

## Source Procedure References

- proc_reset_left_right_tipper_fault_from_visu_mancontrol_v1

## Procedure Steps

### Step 1 — Open the VISU_MANCONTROL manual control screen

**Responsible role:** L2_support

**Instruction:**
Open the Operator Station HMI maintenance manual control screen named VISU_MANCONTROL.

**Expected result:**
The VISU_MANCONTROL screen is displayed with the informational banner (alarms/informational messages) and the LEFT/RIGHT TIPPER FAULT RESET buttons visible.

---

### Step 2 — Review the current banner message(s) for the active fault

**Responsible role:** L2_support

**Instruction:**
Use the informational banner arrows on the right side of the banner to review the current alarm/informational messages so you can confirm what fault is present.

**Expected result:**
The informational banner message(s) corresponding to the current tipper fault are visible/identifiable via the banner navigation arrows.

---

### Step 3 — Press the LEFT or RIGHT TIPPER FAULT RESET button for the indicated side

**Responsible role:** L2_support

**Instruction:**
Select the correct side (LEFT or RIGHT) and press the corresponding LEFT/RIGHT TIPPER FAULT RESET button.

**Expected result:**
The corresponding tipper fault reset action is triggered for the selected side (LEFT or RIGHT).

---

### Step 4 — Verify the banner message updates after reset

**Responsible role:** L2_support

**Instruction:**
After pressing reset, re-check the informational banner messages (use the arrows again if needed) to confirm the fault-related message is cleared/updated.

**Expected result:**
The informational banner messages update to reflect that the corresponding LEFT or RIGHT tipper fault has been reset (fault-related message cleared or replaced with a new/normal informational state).

---

## Success Criteria

- After pressing the corresponding LEFT/RIGHT TIPPER FAULT RESET button, the VISU_MANCONTROL informational banner message for that fault is cleared or updated to a normal informational state.

## Failure Conditions

- The same LEFT or RIGHT tipper fault message remains in the VISU_MANCONTROL informational banner after pressing the corresponding FAULT RESET button.

## Escalation Guidance

- Escalate if the same fault message remains after pressing the corresponding FAULT RESET button.
- Do not proceed with additional manual actions if the banner continues to show an active fault condition.

## Missing Details / Known Gaps

- The source does not specify the exact post-reset banner message text or a specific timing window for when the banner should update; expected_result is limited to observable banner/message change/clearing.
