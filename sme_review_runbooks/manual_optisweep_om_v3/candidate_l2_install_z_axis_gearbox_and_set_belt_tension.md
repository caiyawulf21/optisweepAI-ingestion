# Install the Z-Axis Gearbox and Set Belt Tension

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_the_z_axis_gearbox_and_set_belt_tension_v1` |
| Title | Install the Z-Axis Gearbox and Set Belt Tension |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Reinstall the Z-axis gearbox, reconnect the timing pulley, belt, motor, and idler assembly, set belt tension to the documented specification, reattach belt clamps, reinstall panels, and restart the operator station using the referenced source procedures.

## When To Use

Use when restoring the machine after Z-axis gearbox replacement or removal and the source procedure section 7.3.7.2 Z-Axis Gearbox Installation applies.

## Do Not Use For

* Do not use if the gearbox cannot be fully seated in the pilot hole.
* Do not use if the clamp collar access hole cannot be oriented up as documented.
* Do not use if the motor electrical connectors cannot be oriented down as documented.
* Do not use if equal adjustment of the two tension screws cannot be maintained.
* Do not use if belt tension cannot be brought into the documented 448 N to 494 N range.
* Do not use if three acceptable belt tension readings in a row cannot be obtained.
* Do not use if the belt clamp cannot align with the belt teeth or if the belt is being pinched.

## Safety And Operational Notes

* This procedure is not marked support-safe in the candidate.
* Be aware that excessive area noise can interfere with sonic meter readings.
* The source section is installation-only and assumes prior removal steps from the larger gearbox replacement procedure.

## Access Or Tools Needed

* Access to the Z-axis gearbox assembly
* Four M6x20 socket-head screws
* M8x25 screws
* Two M6x35 tension screws
* M6 socket-head screws
* Six M6 screws for the A-axis belt clamp
* Six M6 screws for the counterbalance belt clamp
* Loctite®
* Torque tool capable of 7 Nm and 21.2 Nm
* Gates 508c Sonic Tension Meter if used
* Access to the referenced Installation procedure on page 168
* Access to the referenced Motor Installation procedure on page 108
* Access to the referenced Starting The Operator Station procedure on page 66

## Procedure Steps

### Step 1 — Insert the gearbox into the pilot hole

**Responsible role:** L2_support

**Instruction:**
Insert the gearbox into the pilot hole.

**Expected result:**
The gearbox enters the pilot hole and is positioned for further installation.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Gearbox visual reference for the component being inserted into the pilot hole.*


**Stop or Escalate If:**

* Stop if the gearbox cannot be inserted into the pilot hole.

---

### Step 2 — Mount the timing pulley on the gearbox

**Responsible role:** L2_support

**Instruction:**
Mount a timing pulley on the gearbox using the referenced Installation procedure on page 168.

**Expected result:**
The timing pulley is mounted on the gearbox per the referenced procedure.

**Stop or Escalate If:**

* Stop if the timing pulley cannot be mounted using the referenced installation procedure.

---

### Step 3 — Loop the belt over the pulley

**Responsible role:** L2_support

**Instruction:**
Loop the belt over the pulley.

**Expected result:**
The belt is placed over the pulley.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Timing belt visual reference for belt routing over the pulley.*


**Stop or Escalate If:**

* Stop if the belt cannot be looped over the pulley.

---

### Step 4 — Seat the gearbox and orient the clamp collar access hole up

**Responsible role:** L2_support

**Instruction:**
Fully seat the gearbox into the pilot hole and verify the clamp collar access hole is oriented up.

**Expected result:**
The gearbox is fully seated and the clamp collar access hole is oriented up.

**Screens / Images:**

![artifact_page_125_image_2](assets/artifact_page_125_image_2.jpeg)

*Clamp collar connection point context that may help identify the access hole orientation.*


**Stop or Escalate If:**

* Stop if the gearbox cannot be fully seated in the pilot hole.
* Stop if the clamp collar access hole cannot be oriented up as documented.

---

### Step 5 — Fasten the gearbox with M6x20 screws

**Responsible role:** L2_support

**Instruction:**
Mount the gearbox with four M6x20 socket-head screws with Loctite® and tighten to 7 Nm (62 in-lb).

**Expected result:**
The gearbox is secured with four M6x20 socket-head screws tightened to the documented torque.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Gearbox mounting context for the installed gearbox.*


**Stop or Escalate If:**

* Stop if the gearbox cannot be secured with four M6x20 socket-head screws and Loctite®.
* Stop if the specified 7 Nm (62 in-lb) torque cannot be applied.

---

### Step 6 — Mount the Z-axis motor with connectors oriented down

**Responsible role:** L2_support

**Instruction:**
Mount the Z-axis motor using the referenced Motor Installation procedure on page 108 and verify the motor electrical connectors are oriented down.

**Expected result:**
The Z-axis motor is mounted and the electrical connectors are oriented down.

**Screens / Images:**

![artifact_page_125_image_2](assets/artifact_page_125_image_2.jpeg)

*Motor mounting and connector orientation; verify electrical connections face down.*


**Stop or Escalate If:**

* Stop if the motor electrical connectors cannot be oriented down as documented.

---

### Step 7 — Lower the counter-balance carriage onto the lower hard stop

**Responsible role:** L2_support

**Instruction:**
Slightly lift the counter-balance carriage, remove the M6 fasteners supporting it, and lower the counter-balance carriage so it rests on the lower hard stop.

**Expected result:**
The counter-balance carriage rests on the lower hard stop.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Counter-balance assembly context while positioning the carriage.*


**Stop or Escalate If:**

* Stop if the counter-balance carriage cannot be safely supported or lowered.

---

### Step 8 — Loosen the idler pulley assembly for adjustment

**Responsible role:** L2_support

**Instruction:**
Very lightly tighten the M8x25 screws holding the idler pulley assembly so the assembly is not loose but can still slide under the fasteners.

**Expected result:**
The idler pulley assembly is retained but still able to slide for adjustment.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly location and adjustment context.*


**Stop or Escalate If:**

* Stop if the idler pulley assembly cannot be set so it is not loose but can still slide.

---

### Step 9 — Thread the tension screws to firm contact

**Responsible role:** L2_support

**Instruction:**
Thread the two M6x35 tension screws until they make firm contact with the actuator base.

**Expected result:**
Both tension screws make firm contact with the actuator base.

**Stop or Escalate If:**

* Stop if either tension screw cannot make firm contact with the actuator base.

---

### Step 10 — Tighten both tension screws equally

**Responsible role:** L2_support

**Instruction:**
Continue to equally tighten the two tension screws, turning both screws the exact same amount so they apply the same amount of force.

**Expected result:**
Both tension screws are advanced equally and apply the same amount of force.

**Stop or Escalate If:**

* Stop if equal adjustment of the two tension screws cannot be maintained.

---

### Step 11 — Measure belt tension on the counter-balance leg

**Responsible role:** L2_support

**Instruction:**
Measure belt tension only on the counter-balance leg of the belt and gradually increase tension until 471 N is reached, with an acceptable range of 448 N to 494 N.

**Expected result:**
Belt tension reaches the documented target within the acceptable range.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Timing belt context to identify the counter-balance leg of the belt.*


**Stop or Escalate If:**

* Stop if belt tension cannot be brought into the documented 448 N to 494 N range.

---

### Step 12 — Set sonic tension meter values if using a Gates 508c

**Responsible role:** L2_support

**Instruction:**
If using a Gates 508c Sonic Tension Meter, use Mass = 4.86 g/m, Width = 20 mm, and Span = 1200 mm.

**Expected result:**
The Gates 508c Sonic Tension Meter is configured with the documented values.

**Stop or Escalate If:**

* Stop if the sonic tension meter cannot be configured as documented when used.

---

### Step 13 — Verify three acceptable tension readings in a row

**Responsible role:** L2_support

**Instruction:**
Adjust and check the tension until three acceptable readings in a row are received, noting that excessive area noise can interfere with sonic meter readings.

**Expected result:**
Three acceptable belt tension readings in a row are obtained.

**Stop or Escalate If:**

* Stop if three acceptable readings in a row cannot be obtained.
* Escalate if excessive area noise prevents reliable sonic meter readings.

---

### Step 14 — Lock the idler assembly in place

**Responsible role:** L2_support

**Instruction:**
Tighten the M8x25 fasteners to 21.2 Nm (188 in-lbs) to lock the idler assembly in place.

**Expected result:**
The idler assembly is locked in place at the documented torque.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly being locked in place after tensioning.*


**Stop or Escalate If:**

* Stop if the idler assembly cannot be locked in place at 21.2 Nm (188 in-lbs).

---

### Step 15 — Raise the counter-balance carriage to mid-travel and reinstall support screws

**Responsible role:** L2_support

**Instruction:**
Raise the counter-balance carriage back to mid-travel and insert the M6 socket-head screws for the carriage to rest against.

**Expected result:**
The counter-balance carriage is at mid-travel and the M6 socket-head screws are inserted.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Counter-balance assembly context while raising the carriage to mid-travel.*


**Stop or Escalate If:**

* Stop if the counter-balance carriage cannot be raised to mid-travel or supported as described.

---

### Step 16 — Reattach the A-axis belt clamp

**Responsible role:** L2_support

**Instruction:**
Re-attach the A-axis belt clamp using six M6 screws and Loctite®, making sure the belt clamp aligns with the belt teeth and does not pinch the belt. Move the belt slightly if needed for alignment.

**Expected result:**
The A-axis belt clamp is reattached and aligned with the belt teeth without pinching the belt.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Belt tooth alignment context while reattaching the A-axis belt clamp.*


**Stop or Escalate If:**

* Stop if the belt clamp cannot align with the belt teeth.
* Stop if the belt is being pinched.

---

### Step 17 — Reattach the counterbalance belt clamp

**Responsible role:** L2_support

**Instruction:**
Re-attach the counterbalance belt clamp using six M6 screws and Loctite®, making sure the belt clamp aligns with the belt teeth and does not pinch the belt. Lift the counterbalance slightly if needed for alignment.

**Expected result:**
The counterbalance belt clamp is reattached and aligned with the belt teeth without pinching the belt.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Belt tooth alignment context while reattaching the counterbalance belt clamp.*


**Stop or Escalate If:**

* Stop if the belt clamp cannot align with the belt teeth.
* Stop if the belt is being pinched.

---

### Step 18 — Remove the support screws from the A-axis and counter-balance

**Responsible role:** L2_support

**Instruction:**
Remove the M6 socket-head screws supporting the A-axis and counter-balance.

**Expected result:**
The temporary support screws are removed from the A-axis and counter-balance.

**Stop or Escalate If:**

* Stop if the support screws cannot be removed safely.

---

### Step 19 — Reinstall the top and bottom side panels

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and bottom side panels.

**Expected result:**
The top and bottom side panels are reinstalled.

**Stop or Escalate If:**

* Stop if the top and bottom side panels cannot be reinstalled.

---

### Step 20 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced Starting The Operator Station procedure on page 66.

**Expected result:**
The operator station is restarted using the referenced procedure.

**Stop or Escalate If:**

* Stop if the operator station cannot be restarted using the referenced procedure.

---

## Success Criteria

* The Z-axis gearbox is installed.
* The gearbox is fully seated in the pilot hole.
* The clamp collar access hole is oriented up as documented.
* The timing pulley and belt are installed.
* The Z-axis motor is installed with electrical connectors oriented down.
* Belt tension is set to 471 N target with an acceptable range of 448 N to 494 N.
* Three acceptable belt tension readings in a row are obtained.
* The idler assembly is locked in place.
* The A-axis belt clamp and counterbalance belt clamp are reattached without pinching the belt and aligned with the belt teeth.
* The top and bottom side panels are reinstalled.
* The operator station is restarted.

## Failure Conditions

* Gearbox cannot be fully seated in the pilot hole.
* Clamp collar access hole cannot be oriented up as documented.
* Motor electrical connectors cannot be oriented down as documented.
* Equal adjustment of the two tension screws cannot be maintained.
* Belt tension cannot be brought into the documented 448 N to 494 N range.
* Three acceptable readings in a row cannot be obtained.
* Excessive area noise interferes with sonic meter readings.
* The belt clamp cannot align with the belt teeth.
* The belt is being pinched.

## Escalation Guidance

* Stop and escalate if the gearbox cannot be fully seated in the pilot hole.
* Stop and escalate if the clamp collar access hole cannot be oriented up as documented.
* Stop and escalate if the motor electrical connectors cannot be oriented down as documented.
* Stop and escalate if equal adjustment of the two tension screws cannot be maintained.
* Stop and escalate if belt tension cannot be brought into the documented 448 N to 494 N range.
* Stop and escalate if three acceptable readings in a row cannot be obtained.
* Account for excessive area noise if sonic meter readings are unreliable.
* Stop and escalate if either belt clamp cannot align with the belt teeth or if the belt is pinched.

## Missing Details / Known Gaps

* The packet does not provide the full source section text for pages 134-139, so step-level quotations could not be added beyond candidate wording and artifact summaries.
* The packet does not explicitly state whether production stop is required.
* The packet does not explicitly state whether LOTO is required for this installation section.
* No source-supported estimated time is provided for this procedure.
* No directly matching artifact for the exact pilot hole insertion view or belt clamp alignment figures was provided; related visuals were attached where relevant.

## Source Lineage

- Candidate IDs: candidate_l2_install_z_axis_gearbox_and_set_belt_tension
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
