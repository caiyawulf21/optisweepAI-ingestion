# Remove Timing Belt From Tipper Assembly

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_timing_belt_from_tipper_assembly_v1` |
| Title | Remove Timing Belt From Tipper Assembly |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely remove the timing belt from the tipper pulleys during timing belt replacement by positioning the A-axis and counterbalance, locking out the tipper, opening side panel access, securing both carriages with M6 socket-head screws, removing belt clamps, releasing belt tension, and removing the belt when only the timing belt is being replaced.

## When To Use

Use this procedure for the documented removal portion of timing belt replacement on the tipper assembly when the timing belt must be removed from the pulleys.

## Do Not Use For

* Do not use for operator execution; the documented task includes lockout/tagout and mechanical disassembly.
* Do not use for installation, retensioning, adjustment, or recovery actions beyond belt removal because those details are not provided in this source section.
* Do not proceed if the A-axis, counterbalance, or carriages cannot be positioned as described before belt tension is released.

## Safety And Operational Notes

* This procedure is not support-safe for operator execution.
* Perform lockout/tagout on the tipper before accessing internal components.
* Install M6 socket-head screws below both carriages before releasing belt tension to prevent the A-axis and counterbalance from dropping.
* Stop if the A-axis, counterbalance, or carriages cannot be positioned as described before belt tension is released.
* Stop if the securing screws or belt clamp fasteners cannot be identified or removed as documented.
* Do not proceed beyond the documented removal scope when the source does not provide additional recovery or adjustment guidance in this section.

## Access Or Tools Needed

* Replacement timing belt
* Safety glasses
* Gloves
* Torque wrench
* 5-mm hex wrench
* 6-mm hex wrench
* 3/8-in. wrench or socket
* Loctite
* Sonic belt tension meter
* Access to the tipper side panels and timing belt area
* Ability to perform Operator Station Lockout/Tagout

## Procedure Steps

### Step 1 — Gather replacement part, PPE, and tools

**Responsible role:** L2_support

**Instruction:**
Gather the replacement timing belt, safety glasses, gloves, torque wrench, 5-mm hex wrench, 6-mm hex wrench, 3/8-in. wrench or socket, Loctite, and sonic belt tension meter.

**Expected result:**
All documented parts, PPE, and tools are available at the work area.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Use the timing belt figure as the primary visual reference for the component being serviced.*


**Stop or Escalate If:**

* Required part, PPE, or tools are not available.

---

### Step 2 — Position the A-axis and counterbalance

**Responsible role:** L2_support

**Instruction:**
Manually position the A-axis and the counterbalance between the threaded holes in the actuator base. Verify there are two holes adjacent to each rail and that the carriages are positioned between the holes on the respective rails.

**Expected result:**
The A-axis and counterbalance are positioned between the threaded holes, and both carriage positions are verified relative to the rail holes.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Timing belt location and the A-axis/counterbalance position relative to the actuator base holes and carriage position on the rails.*

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Related visual context for jogging/positioning the A-axis and counterbalance and securing below both carriages.*

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*General counterbalance identification context.*


**Stop or Escalate If:**

* The A-axis, counterbalance, or carriages cannot be positioned as described before belt tension is released.

---

### Step 3 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure.

**Expected result:**
The tipper is locked out and tagged out per the referenced procedure.

**Stop or Escalate If:**

* LOTO cannot be completed before proceeding.

---

### Step 4 — Remove the station side panels

**Responsible role:** L2_support

**Instruction:**
Use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panels, then remove the station side panels to access the timing belt.

**Expected result:**
The side panels are removed and the timing belt area is accessible.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Access area behind the station side panels and timing belt location.*


**Stop or Escalate If:**

* The side panel fasteners cannot be identified or removed as documented.
* The timing belt area cannot be accessed after panel removal.

---

### Step 5 — Secure both carriages with M6 screws

**Responsible role:** L2_support

**Instruction:**
Thread M6 socket-head screws into the holes below both carriages to prevent the A-axis and counterbalance from dropping once belt tension is released.

**Expected result:**
Both carriages are secured with M6 socket-head screws below them.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Threaded holes used for the M6 socket-head screws below both carriages.*

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Related visual context showing M6 socket-head screws below both carriages to prevent dropping when belt tension is released.*


**Stop or Escalate If:**

* The threaded holes below both carriages cannot be identified.
* The M6 socket-head screws cannot be installed to secure the carriages before belt tension is released.

---

### Step 6 — Remove the belt clamps

**Responsible role:** L2_support

**Instruction:**
Remove the belt clamps by removing the six M6x20 countersunk screws from each clamp with a 5-mm hex wrench to free the carriages from the belt.

**Expected result:**
The belt clamps are removed and the carriages are freed from the belt.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Belt clamps and the M6x20 countersunk screws securing them.*


**Stop or Escalate If:**

* The belt clamp fasteners cannot be identified or removed as documented.

---

### Step 7 — Release belt tension

**Responsible role:** L2_support

**Instruction:**
Release belt tension by loosening the two M6x35 socket-head screws on the bottom side of the assembly and loosening the two M8x25 socket-head screws holding the idler pulley assembly in place.

**Expected result:**
Belt tension is released and the idler pulley assembly is loosened.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly and the area where the M8x25 socket-head screws hold it in place.*

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Timing belt removal context around the belt path and tension release area.*


**Stop or Escalate If:**

* The M6x35 socket-head screws cannot be identified or loosened as documented.
* The M8x25 socket-head screws holding the idler pulley assembly cannot be identified or loosened as documented.

---

### Step 8 — Hold the idler assembly and remove the timing belt

**Responsible role:** L2_support

**Instruction:**
If only the timing belt is being replaced, slide the idler pulley assembly up and re-tighten the two M6x35 socket-head screws to hold the idler pulley assembly in place, then remove the timing belt from the pulleys.

**Expected result:**
The idler pulley assembly is held in place and the timing belt is removed from the pulleys.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Timing belt path on the pulleys for final belt removal.*

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly location while sliding it up and holding it in place.*


**Stop or Escalate If:**

* The idler pulley assembly cannot be positioned and held as documented.
* The timing belt cannot be removed from the pulleys.
* Additional installation, adjustment, or recovery guidance is needed beyond the documented removal scope.

---

## Success Criteria

* The timing belt is removed from the pulleys.
* The A-axis and counterbalance remain secured against dropping during belt tension release.
* The documented removal scope is completed without proceeding into unsupported installation or adjustment actions.

## Failure Conditions

* Required part, PPE, or tools are missing.
* The A-axis, counterbalance, or carriages cannot be positioned as described before belt tension is released.
* LOTO cannot be completed before proceeding.
* The side panel fasteners, securing screws, belt clamp fasteners, or idler pulley assembly fasteners cannot be identified or removed/loosened as documented.
* The threaded holes below both carriages cannot be identified or the M6 socket-head screws cannot be installed.
* The timing belt cannot be removed from the pulleys.
* Additional recovery, installation, or adjustment guidance is required beyond what this source section provides.

## Escalation Guidance

* Escalate if the A-axis, counterbalance, or carriages cannot be positioned as described before belt tension is released.
* Escalate if the securing screws or belt clamp fasteners cannot be identified or removed as documented.
* Escalate if the idler pulley assembly fasteners cannot be identified or loosened as documented.
* Escalate if the task requires actions beyond the documented removal scope in this source section.

## Missing Details / Known Gaps

* The source packet does not provide the full OCR text of section 7.3.8.1 removal for direct quotation.
* No estimated time is provided in this packet for the timing belt removal procedure.
* The source section in this packet does not provide installation, retensioning, torque values, or post-removal validation steps.
* No explicit role boundaries beyond L2_support are provided in the packet.
* No commands are provided in the source packet.
* No explicit production stop requirement is stated in the packet.

## Source Lineage

- Candidate IDs: candidate_l2_remove_timing_belt_from_tipper_assembly
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
