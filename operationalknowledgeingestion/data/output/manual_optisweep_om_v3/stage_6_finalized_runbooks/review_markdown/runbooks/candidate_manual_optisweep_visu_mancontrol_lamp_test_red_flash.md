# Run Lamp Test From VISU_MANCONTROL and Verify Red Flash + Audible Alarm

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_run_lamp_test_from_visu_mancontrol_verify_red_flash_audible_alarm_v1` |
| Title | Run Lamp Test From VISU_MANCONTROL and Verify Red Flash + Audible Alarm |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

On the Operator Station HMI maintenance manual control screen VISU_MANCONTROL, use the LAMP TEST button to verify the audible alarm sounds and the stacklight flashes red.

## When To Use

Use to confirm the VISU_MANCONTROL LAMP TEST function triggers both the audible alarm and the stacklight red flashing behavior.

## Access Or Tools Needed

* Tipper HMI / WebVisu / VISU access to the VISU_MANCONTROL screen
* Audible and visual access to the stacklight

## Related Operational Context

* ctx_manual_visu_mancontrol_screen_v1

## Visual References

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/4b97d803be8edafc.jpeg)

*VISU_MANCONTROL screen showing the LAMP TEST button and its item description (Item 5: audible alarm + stacklight flashes red).*

## Procedure Steps

### Step 1 — Open the VISU_MANCONTROL screen

**Responsible role:** L2_support

**Instruction:**
Open the Operator Station HMI maintenance manual control screen named VISU_MANCONTROL.

**Expected result:**
The VISU_MANCONTROL screen is displayed with the LAMP TEST button visible.

**Stop or Escalate If:**

* If VISU_MANCONTROL cannot be opened or the LAMP TEST button is not available, stop and escalate.

---

### Step 2 — Press LAMP TEST

**Responsible role:** L2_support

**Instruction:**
On the VISU_MANCONTROL screen, press the LAMP TEST button.

**Expected result:**
After pressing LAMP TEST, the audible alarm sounds and the stacklight flashes red.

**Stop or Escalate If:**

* Stop and escalate if the audible alarm does not sound.
* Stop and escalate if the stacklight does not flash red.

---

## Success Criteria

* Audible alarm sounds after pressing LAMP TEST.
* Stacklight flashes red after pressing LAMP TEST.

## Failure Conditions

* Audible alarm does not sound after pressing LAMP TEST.
* Stacklight does not flash red after pressing LAMP TEST.

## Escalation Guidance

* If either the audible alarm does not sound or the stacklight does not flash red, stop the test and escalate.

## Missing Details / Known Gaps

* The source does not specify which stacklight (e.g., left vs right) is used for the lamp test; the procedure assumes the corresponding stacklight associated with the manual control station.

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_visu_mancontrol_lamp_test_red_flash
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
