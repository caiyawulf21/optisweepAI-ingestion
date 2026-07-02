# Remove the Idler Pulley Assembly

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_the_idler_pulley_assembly_v1` |
| Title | Remove the Idler Pulley Assembly |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely remove the idler pulley assembly from the tipper column so it can be replaced. The documented source procedure includes lockout/tagout, optional side panel removal for motor access, positioning and securing the A-axis and counterbalance before releasing belt tension, removing belt clamps, loosening the tensioning screws, removing the assembly mounting screws, and sliding the idler pulley assembly out of the column.

## When To Use

Use when the idler pulley assembly must be removed from the tipper column for replacement, as documented in the OptiSweep Operation and Maintenance Manual section 7.3.20.1 Removal.

## Do Not Use For

* Do not use for installation or reassembly of the idler pulley assembly; those details are not provided in this source packet.
* Do not use if the A-axis and counterbalance cannot be safely positioned and secured below both carriages before belt tension is released.
* Do not use if the documented fasteners, holes, clamps, or screw locations cannot be positively identified from the source-backed equipment layout.

## Safety And Operational Notes

* Perform the documented Operator Station Lockout/Tagout procedure before beginning removal.
* Use safety glasses and gloves.
* Secure the A-axis and counterbalance below both carriages before releasing belt tension to prevent dropping.
* This procedure involves mechanical access, manual positioning of components, belt tension release, and hardware removal.

## Access Or Tools Needed

* Access to the tipper
* Operator Station Lockout/Tagout procedure
* Safety glasses
* Gloves
* 5-mm hex wrench
* 3/8-in. wrench or socket
* M6 socket-head screws for securing below both carriages
* Access to the station side panel, motor area, actuator base, rails, belt clamps, and idler pulley assembly
* Replacement idler pulley assembly
* 6-mm hex wrench
* Loctite
* Sonic belt tension meter

## Procedure Steps

### Step 1 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the documented Operator Station Lockout/Tagout procedure referenced by the manual before performing any removal work.

**Expected result:**
The tipper is in a locked out and tagged out state and safe for maintenance access.

**Stop or Escalate If:**

* The documented Operator Station Lockout/Tagout procedure is unavailable.
* Safe isolation cannot be confirmed.

---

### Step 2 — Remove the station side panel if motor access is needed

**Responsible role:** L2_support

**Instruction:**
If needed to access the motor, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the station side panel, then remove the side panel.

**Expected result:**
The station side panel is removed and the motor access area is exposed if needed.

**Screens / Images:**

![artifact_fig_7_15_tip_cable](assets/artifact_fig_7_15_tip_cable.png)

*Station side panel and motor access area referenced in nearby maintenance procedures.*

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Overall idler pulley assembly service context for this procedure.*


**Stop or Escalate If:**

* The station side panel or its nine self-tapping fasteners cannot be positively identified from source-backed equipment layout.
* Motor access is needed but cannot be obtained safely.

---

### Step 3 — Position the A-axis and counterbalance between the actuator base holes

**Responsible role:** L2_support

**Instruction:**
Manually position the A-axis and the counterbalance between the threaded holes in the actuator base. There are two holes adjacent to each rail, and the carriages should be positioned between the holes on the respective rails.

**Expected result:**
The A-axis and counterbalance carriages are aligned between the threaded holes adjacent to each rail.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly service context and related A-axis drive area.*

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Actuator base, rails, and carriage positioning between threaded holes.*

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Similar A-axis and counterbalance positioning context below both carriages.*


**Stop or Escalate If:**

* The A-axis or counterbalance cannot be safely positioned between the threaded holes in the actuator base.
* The holes adjacent to each rail cannot be positively identified from source-backed equipment layout.

---

### Step 4 — Secure both carriages with M6 socket-head screws

**Responsible role:** L2_support

**Instruction:**
Thread M6 socket-head screws into the holes below both carriages to prevent the A-axis and counterbalance from dropping once belt tension is released.

**Expected result:**
Both carriages are mechanically secured below the carriages before belt tension is released.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Overall service context for the idler pulley assembly removal.*

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Holes below both carriages and carriage support arrangement.*

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Reference arrangement for inserting M6 socket-head screws below both carriages.*


**Stop or Escalate If:**

* The A-axis or counterbalance cannot be safely secured below both carriages before belt tension is released.
* The holes below both carriages cannot be positively identified from source-backed equipment layout.

---

### Step 5 — Remove the belt clamps

**Responsible role:** L2_support

**Instruction:**
Remove the belt clamps by removing the six M6x20 countersunk screws from each clamp with a 5-mm hex wrench to free the carriages from the belt.

**Expected result:**
The belt clamps are removed and the carriages are free from the belt.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly and related belt path service context.*

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Timing belt area and likely belt clamp location context.*


**Stop or Escalate If:**

* The belt clamps or the six M6x20 countersunk screws on each clamp cannot be positively identified from source-backed equipment layout.
* The carriages cannot be freed from the belt after clamp removal.

---

### Step 6 — Loosen the tensioning screws to release belt tension

**Responsible role:** L2_support

**Instruction:**
Release belt tension by loosening the two M6x35 socket-head screws on the bottom side of the assembly.

**Expected result:**
Belt tension is released from the assembly.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly and bottom-side tensioning screw area.*


**Stop or Escalate If:**

* The A-axis and counterbalance are not secured below both carriages before belt tension is released.
* The two M6x35 socket-head screws on the bottom side of the assembly cannot be positively identified.
* Any component begins to drop or shift unexpectedly when tension is released.

---

### Step 7 — Remove the idler pulley assembly from the column

**Responsible role:** L2_support

**Instruction:**
Remove the two M8x25 socket-head screws holding the idler pulley assembly in place, then slide the idler pulley assembly out of the column.

**Expected result:**
The idler pulley assembly is removed from the column.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly mounting screw locations and assembly removal context.*


**Stop or Escalate If:**

* The two M8x25 socket-head screws holding the assembly in place cannot be positively identified.
* The assembly does not slide out of the column after the mounting screws are removed.
* The removal direction cannot be confirmed from the source-backed equipment layout.

---

### Step 8 — Transfer the tensioning screws if replacement requires it

**Responsible role:** L2_support

**Instruction:**
If needed for replacement, transfer the M6x35 tensioning screws from the removed idler pulley assembly to the new assembly.

**Expected result:**
The M6x35 tensioning screws are available on the replacement assembly if required.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly context for identifying the M6x35 tensioning screws.*


**Stop or Escalate If:**

* The M6x35 tensioning screws cannot be positively identified on the removed assembly.
* Replacement requires transfer but the screws cannot be removed or reused.

---

## Success Criteria

* The tipper was locked out/tagged out before removal work began.
* The A-axis and counterbalance were positioned and secured below both carriages before belt tension was released.
* The belt clamps were removed and the carriages were freed from the belt.
* Belt tension was released by loosening the two M6x35 socket-head screws.
* The two M8x25 socket-head screws were removed and the idler pulley assembly was slid out of the column.
* If replacement required it, the M6x35 tensioning screws were transferred to the new assembly.

## Failure Conditions

* Safe lockout/tagout cannot be confirmed.
* The A-axis or counterbalance cannot be safely positioned and secured below both carriages before belt tension is released.
* The documented fasteners, holes, clamps, or screw locations cannot be positively identified from the source-backed equipment layout.
* The belt clamps, tensioning screws, or mounting screws cannot be removed as documented.
* Any component begins to drop or shift unexpectedly during belt tension release or assembly removal.

## Escalation Guidance

* Stop and escalate if the A-axis or counterbalance cannot be safely positioned and secured before belt tension is released.
* Stop and escalate if the documented fasteners, holes, clamps, or screw locations cannot be positively identified from the source-backed equipment layout.
* Stop and escalate if safe isolation cannot be confirmed through the documented Operator Station Lockout/Tagout procedure.

## Missing Details / Known Gaps

* The source packet does not provide the OCR text of section 7.3.20.1 Removal, so step wording is grounded primarily in the candidate and artifact retrieval summaries.
* The source packet does not provide installation, reassembly, retensioning, or torque details for the replacement assembly.
* The source packet does not provide explicit production stop status.
* The source packet does not provide explicit role boundaries beyond the candidate's L2_support designation.
* Several visual supports requested in the candidate are satisfied only by related reference artifacts rather than a step-specific figure explicitly showing each fastener location.

## Source Lineage

- Candidate IDs: candidate_l2_remove_idler_pulley_assembly
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
