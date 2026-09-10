# Set Z-Axis Home Position (Tipper Commissioning)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_set_z_axis_home_position_tipper_commissioning_v1` |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the OptiSweep tipper HMI, use the "Visu_MDs" (F2) screen to enter the previously recorded Z-axis "Home Offset" values into the "New Value" column for each Z-axis, press UPDATE to apply, and repeat for the other Z-axis.

## When To Use

Use during tipper commissioning when you need to set each tipper Z-axis "Home Offset" to the previously recorded value and confirm the update on the "Visu_MDs" screen.

## Source Procedure References

- proc_set_z_axis_home_position_tipper_commissioning_v1

## Procedure Steps

### Step 1 — Navigate to the "Visu_MDs" (F2) screen

**Responsible role:** L2_support

**Instruction:**
On the OptiSweep HMI, navigate to the "Visu_MDs" screen using the F2 function key.

**Expected result:**
The "Visu_MDs" screen is displayed and ready for editing the Z-axis "Home Offset" settings.

---

### Step 2 — Enter recorded Z-axis "Home Offset" values into "New Value"

**Responsible role:** L2_support

**Instruction:**
For each Z-axis, locate the "Home Offset" setting and enter the previously recorded value into the "New Value" column.

**Expected result:**
Each Z-axis "Home Offset" field shows the entered value in the "New Value" column.

---

### Step 3 — Press UPDATE to confirm the change

**Responsible role:** L2_support

**Instruction:**
Press UPDATE to confirm the change for the Z-axis.

**Expected result:**
After pressing UPDATE, the "Home Offset" setting reflects the entered "New Value" for that Z-axis.

---

### Step 4 — Repeat for the other Z-axis

**Responsible role:** L2_support

**Instruction:**
Repeat the "Home Offset" "New Value" entry and UPDATE confirmation for the other Z-axis.

**Expected result:**
The other Z-axis "Home Offset" reflects its entered "New Value" after pressing UPDATE.

---

## Success Criteria

- After pressing UPDATE for each Z-axis, the "Home Offset" setting(s) on the "Visu_MDs" screen reflect the entered "New Value" values.

## Failure Conditions

- Pressing UPDATE does not change the "Home Offset" value to match the entered "New Value" for a Z-axis.

## Escalation Guidance

- If UPDATE does not apply the entered "New Value" (values do not change as expected), stop and escalate for support.

## Missing Details / Known Gaps

- The packet does not specify the exact on-screen confirmation behavior after pressing UPDATE (e.g., whether a pop-up appears or which field changes). Use the observable change in the "Home Offset" value on the "Visu_MDs" screen as the confirmation.
