# Run Lamp Test From VISU_MANCONTROL and Verify Red Flash + Audible Alarm

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_run_lamp_test_from_visu_mancontrol_verify_red_flash_audible_alarm_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the Operator Station HMI maintenance manual control screen VISU_MANCONTROL, use the LAMP TEST button to verify the audible alarm sounds and the stacklight flashes red.

## When To Use

Use to confirm the VISU_MANCONTROL LAMP TEST function triggers both the audible alarm and the stacklight red flashing behavior.

## Source Procedure References

- proc_run_lamp_test_from_visu_mancontrol_verify_red_flash_audible_alarm_v1

## Procedure Steps

### Step 1 — Open the VISU_MANCONTROL screen

**Responsible role:** L2_support

**Instruction:**
Open the Operator Station HMI maintenance manual control screen named VISU_MANCONTROL.

**Expected result:**
The VISU_MANCONTROL screen is displayed with the LAMP TEST button visible.

---

### Step 2 — Press LAMP TEST

**Responsible role:** L2_support

**Instruction:**
On the VISU_MANCONTROL screen, press the LAMP TEST button.

**Expected result:**
After pressing LAMP TEST, the audible alarm sounds and the stacklight flashes red.

---

## Success Criteria

- Audible alarm sounds after pressing LAMP TEST.
- Stacklight flashes red after pressing LAMP TEST.

## Failure Conditions

- Audible alarm does not sound after pressing LAMP TEST.
- Stacklight does not flash red after pressing LAMP TEST.

## Escalation Guidance

- If either the audible alarm does not sound or the stacklight does not flash red, stop the test and escalate.

## Missing Details / Known Gaps

- The source does not specify which stacklight (e.g., left vs right) is used for the lamp test; the procedure assumes the corresponding stacklight associated with the manual control station.
