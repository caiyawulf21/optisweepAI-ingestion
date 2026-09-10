# Disable a LEFT/RIGHT Tipper and Verify Solid Blue Stacklight on VISU_MANCONTROL

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_disable_left_right_tipper_verify_solid_blue_visu_mancontrol_v1` |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the Operator Station HMI screen VISU_MANCONTROL, disable the corresponding LEFT or RIGHT tipper using the LEFT/RIGHT TIPPER DISABLE button and verify the corresponding stacklight illuminates solid blue.

## When To Use

Use when you need to disable a specific LEFT or RIGHT tipper from the Operator Station HMI and confirm the expected stacklight indication (solid blue) on VISU_MANCONTROL.

## Source Procedure References

- proc_disable_left_right_tipper_verify_solid_blue_visu_mancontrol_v1

## Safety And Operational Notes

- If the stacklight does not illuminate solid blue after pressing the LEFT/RIGHT TIPPER DISABLE button, stop and escalate.

## Procedure Steps

### Step 1 — Open VISU_MANCONTROL (Operator Station HMI manual control screen)

**Responsible role:** L2_support

**Instruction:**
Open the Operator Station HMI maintenance manual control screen named VISU_MANCONTROL.

**Expected result:**
The VISU_MANCONTROL screen is displayed with the LEFT/RIGHT TIPPER DISABLE controls visible.

---

### Step 2 — Disable the correct LEFT or RIGHT tipper using the DISABLE button

**Responsible role:** L2_support

**Instruction:**
Select the correct side (LEFT or RIGHT) and press the corresponding LEFT/RIGHT TIPPER DISABLE button on VISU_MANCONTROL.

**Expected result:**
The corresponding tipper is disabled as indicated by the stacklight behavior described for the DISABLE button.

---

### Step 3 — Verify the corresponding tipper stacklight illuminates solid blue

**Responsible role:** L2_support

**Instruction:**
Observe the corresponding tipper stacklight and confirm it illuminates solid blue.

**Expected result:**
The corresponding tipper stacklight illuminates solid blue.

---

## Success Criteria

- After pressing the LEFT or RIGHT TIPPER DISABLE button, the corresponding tipper stacklight illuminates solid blue.

## Failure Conditions

- Corresponding tipper stacklight does not illuminate solid blue after pressing the LEFT/RIGHT TIPPER DISABLE button.

## Escalation Guidance

- Escalate if the stacklight does not turn solid blue after the disable action.

## Missing Details / Known Gaps

- The source does not specify whether the stacklight indication is shown only physically or also reflected on-screen; the procedure assumes visual observation of the physical stacklight as stated in the candidate.
