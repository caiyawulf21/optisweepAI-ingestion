# Force OUT W1 Value to Release an AGV Stuck Condition

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_force_out_w1_value_to_release_an_agv_stuck_condition_v1` |
| Title | Force OUT W1 Value to Release an AGV Stuck Condition |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented OUT W1 forced value entry on the operator station HMI to continue AGV operation or send the AGV to the hospital in the AGV Stuck recovery procedure.

## When To Use

Use this procedure for the documented AGV Stuck recovery action on the operator station HMI when an AGV remains at the tipper after tote-tipping is complete and the manual recovery requires forcing the OUT W1 value for the selected tipper.

## Do Not Use For

* Do not use if the correct tipper is not confirmed before entering a forced value.
* Do not use when the required AGV disposition is unclear between continuing work and going to the hospital.

## Safety And Operational Notes

* This procedure changes a forced output value on the HMI.
* Make sure the correct tipper is selected before changing any forced value.

## Access Or Tools Needed

* Operator station HMI
* Access to the "Visu_ManControl" and "CellIO Status" HMI area
* Ability to enter an "OUT W1" forced value and toggle the associated checkbox

## Related Operational Context

* ctx_manual_agv_stuck_fault_overview_v1
* ctx_manual_visu_mancontrol_cellio_status_screen_v1
* ctx_manual_out_w1_forced_values_agv_stuck_v1

## Procedure Steps

### Step 1 — Confirm the correct tipper on CellIO Status

**Responsible role:** L2_support

**Instruction:**
On the operator station HMI, make sure the correct tipper is selected on the CellIO Status view before changing any forced value.

**Expected result:**
The affected tipper is confirmed as the selected tipper on the CellIO Status view.

**Screens / Images:**

![artifact_page_87_image_2](assets/artifact_page_87_image_2.jpeg)

*CellIO Status view for the affected tipper selection in the AGV Stuck recovery context.*

![artifact_page_87_image_3](assets/artifact_page_87_image_3.jpeg)

*HMI area showing the selected tipper and the OUT W1 forced value area.*

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*Visu_ManControl screen and CellIO Status access path.*


**Stop or Escalate If:**

* Stop if the correct tipper is not confirmed before entering a forced value.

---

### Step 2 — Enter the documented OUT W1 forced value

**Responsible role:** L2_support

**Instruction:**
Enter a value of 3 in the "OUT W1" forced value box if the tote and AGV are ready to continue working, or enter 32771 if the AGV needs to go to the hospital.

**Expected result:**
The correct documented OUT W1 value is entered in the forced value box for the selected tipper.

**Screens / Images:**

![artifact_page_87_image_2](assets/artifact_page_87_image_2.jpeg)

*OUT W1 forced value field for the selected tipper in the AGV Stuck recovery screen.*

![artifact_page_87_image_3](assets/artifact_page_87_image_3.jpeg)

*Example location of the OUT W1 forced value entry area on the operator station screen.*


**Stop or Escalate If:**

* Escalate if the required AGV disposition is unclear because the source provides two different documented values for different outcomes.
* Escalate if the HMI does not allow the value to be entered as documented.

---

### Step 3 — Check the box next to the forced value

**Responsible role:** L2_support

**Instruction:**
Check the box next to the value entered in the forced value box.

**Expected result:**
The checkbox next to the entered OUT W1 forced value is checked.

**Screens / Images:**

![artifact_page_87_image_2](assets/artifact_page_87_image_2.jpeg)

*Checkbox next to the OUT W1 forced value field.*

![artifact_page_87_image_3](assets/artifact_page_87_image_3.jpeg)

*Forced value checkbox control associated with OUT W1.*


**Stop or Escalate If:**

* Escalate if the checkbox cannot be applied as documented.

---

### Step 4 — Wait 10 seconds

**Responsible role:** L2_support

**Instruction:**
Wait 10 seconds.

**Expected result:**
Ten seconds elapse after the OUT W1 forced value checkbox is checked.

---

### Step 5 — Uncheck the OUT W1 box

**Responsible role:** L2_support

**Instruction:**
Uncheck the box for value "OUT W1".

**Expected result:**
The OUT W1 checkbox is unchecked after the 10-second wait.

**Screens / Images:**

![artifact_page_87_image_2](assets/artifact_page_87_image_2.jpeg)

*OUT W1 checkbox state after the 10-second wait.*

![artifact_page_87_image_3](assets/artifact_page_87_image_3.jpeg)

*Checkbox next to OUT W1 being cleared after the forced value interval.*


**Stop or Escalate If:**

* Escalate if the checkbox cannot be removed as documented.

---

## Success Criteria

* The documented OUT W1 forced value is entered for the selected tipper.
* The checkbox next to the entered value is checked, held for 10 seconds, and then unchecked.
* The manual recovery action described for the AGV Stuck condition is completed as documented.

## Failure Conditions

* The correct tipper is not confirmed before entering a forced value.
* The required AGV disposition is unclear between continue working and hospital.
* The HMI does not allow the value to be entered.
* The checkbox cannot be applied or removed as documented.

## Escalation Guidance

* Stop if the correct tipper is not confirmed before entering a forced value.
* Escalate if the required AGV disposition is unclear because the source provides two different documented values for different outcomes.
* Escalate if the HMI does not allow the value to be entered or the checkbox cannot be applied or removed as documented.

## Missing Details / Known Gaps

* The source packet does not provide an explicit estimated completion time for the full procedure.
* The source packet does not explicitly state whether production stop or LOTO is required.
* The source packet does not provide explicit post-action confirmation criteria beyond applying and removing the forced value.
* The source packet references the broader AGV Stuck verification path on Visu_ManControl and CellIO Status, but this candidate begins at the forced-value action rather than restating the full verification sequence.

## Source Lineage

- Candidate IDs: candidate_l2_force_out_w1_value_for_agv_stuck_recovery
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
