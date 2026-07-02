# Remove Z-Axis Gearbox Access Components and Release Belt Drive for Gearbox Replacement

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_z_axis_gearbox_access_and_release_drive_components_v1` |
| Title | Remove Z-Axis Gearbox Access Components and Release Belt Drive for Gearbox Replacement |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Perform the documented removal-preparation steps for Z-axis gearbox replacement: manually position the A-axis and counter-balance, apply lockout/tagout, remove the station side panel, secure both carriages with M6 socket-head screws, remove both belt clamps, release belt tension, loosen the idler pulley assembly lock screws, and refer to the separate motor removal procedure if motor removal is required.

## When To Use

Use when performing the documented removal preparation for Z-axis gearbox replacement in the OptiSweep Operation and Maintenance Manual section 7.3.7.1 Removal, including access opening and belt-drive release steps before gearbox removal proceeds.

## Do Not Use For

* Do not use this runbook as a complete gearbox removal or re-assembly procedure.
* Do not use this runbook for Z-axis motor removal details; use the separately referenced Motor Removal procedure on page 106 if motor removal is needed.
* Do not use this runbook if the A-axis and counter-balance cannot be positioned between the threaded holes as described.
* Do not use this runbook if carriage securing screws cannot be installed below both carriages before belt tension is released.

## Safety And Operational Notes

* This procedure includes lockout/tagout and mechanical work around belt tension and suspended axis components, so it is not operator-safe.
* Secure both carriages with M6 socket-head screws before releasing belt tension to prevent the A-axis and counter-balance from dropping.
* Use safety glasses and gloves.
* Most fasteners have Loctite 277 (red), so removal may be more difficult.
* Motor removal details are not included in this section; use the separately referenced procedure if needed.

## Access Or Tools Needed

* HMI access for manual jog positioning
* LOTO access for the tipper
* Safety glasses
* Gloves
* Replacement gearbox
* Torque wrench
* 4-mm hex wrench
* 5-mm hex wrench
* 6-mm hex wrench
* 3/8-in. wrench or socket
* M6 socket-head screws for carriage securing
* Access to the station side panel, motor area, belt clamps, tensioning screws, and idler pulley assembly

## Procedure Steps

### Step 1 — Position the A-axis and counter-balance between actuator base holes

**Responsible role:** L2_support

**Instruction:**
Use the HMI to manually position (jog) the A-axis and counter-balance between the threaded holes in the actuator base. Verify there are two holes adjacent to each rail and that the carriages are positioned between the holes on the respective rails.

**Expected result:**
The A-axis and counter-balance are positioned between the threaded holes adjacent to each rail.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Gearbox area and actuator base context for the A-axis/counter-balance positioning step.*

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Positioning context showing the A-axis and counter-balance between threaded holes in the actuator base.*


**Stop or Escalate If:**

* The A-axis and counter-balance cannot be positioned between the threaded holes in the actuator base.
* The carriage positions do not align with the holes needed for securing.

---

### Step 2 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure.

**Expected result:**
The tipper is in the documented lockout/tagout state for maintenance.

**Stop or Escalate If:**

* LOTO cannot be completed or verified before panel removal or belt-tension release.

---

### Step 3 — Remove the station side panel

**Responsible role:** L2_support

**Instruction:**
Use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel, then remove the station side panel to access the motor.

**Expected result:**
The station side panel is removed and the motor access area is open.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Gearbox and motor access area associated with side-panel removal.*


**Stop or Escalate If:**

* The side panel cannot be removed safely.
* Fasteners cannot be removed with the documented tool.
* Motor access is still obstructed after panel removal.

---

### Step 4 — Secure both carriages with M6 socket-head screws

**Responsible role:** L2_support

**Instruction:**
Insert an M6 socket-head screw into the holes below both carriages to prevent the A-axis and counter-balance from dropping once belt tension is released.

**Expected result:**
Both carriages are mechanically supported by installed M6 socket-head screws below them.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Carriage area and support-hole context below both carriages.*

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Support-hole and carriage securing context used before releasing belt tension.*


**Stop or Escalate If:**

* The carriage securing screws cannot be installed below both carriages before belt tension is released.
* Either carriage is not positively supported.

---

### Step 5 — Remove the A-axis and counter-balance belt clamps

**Responsible role:** L2_support

**Instruction:**
Remove the A-axis belt clamp and the counter-balance belt clamp by removing the six M6 screws in each clamp. Verify both carriages are free from the belt after the clamps are removed.

**Expected result:**
Both belt clamps are removed and both carriages are free from the belt.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Gearbox drive area where the belt clamps are accessed.*

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Timing belt path and clamp-related belt connection context.*


**Stop or Escalate If:**

* One or both belt clamps cannot be removed.
* Both carriages are not free from the belt after clamp removal.

---

### Step 6 — Release belt tension at the lower end

**Responsible role:** L2_support

**Instruction:**
Release belt tension by loosening the two M6x35 socket-head tensioning screws on the lower end.

**Expected result:**
The belt tension is released at the lower end.

**Screens / Images:**

![artifact_fig_7_8_timing_belt](assets/artifact_fig_7_8_timing_belt.png)

*Timing belt and lower-end tensioning area associated with belt tension release.*

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Gearbox-side belt-drive context for the tension-release step.*


**Stop or Escalate If:**

* The tensioning screws cannot be loosened.
* Belt tension does not release as expected.
* Either carriage support condition changes after tension is reduced.

---

### Step 7 — Loosen the idler pulley assembly lock screws

**Responsible role:** L2_support

**Instruction:**
Loosen the two M8 socket-head screws that lock the idler pulley assembly in place.

**Expected result:**
The idler pulley assembly lock screws are loosened.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly and the lock-screw area.*


**Stop or Escalate If:**

* The two M8 socket-head screws cannot be loosened.
* The idler pulley assembly remains locked in place after the screws are loosened.

---

### Step 8 — Refer to the separate motor removal procedure if needed

**Responsible role:** L2_support

**Instruction:**
If needed, remove the Z-axis motor using the separately referenced Motor Removal procedure on page 106.

**Expected result:**
Motor removal, if required, is handed off to the correct referenced procedure rather than improvised from this section.

**Stop or Escalate If:**

* Motor removal is required but the separate Motor Removal procedure is not available.
* There is pressure to invent motor-removal steps from this section alone.

---

## Success Criteria

* The A-axis and counter-balance are positioned between the threaded holes in the actuator base.
* The tipper is locked out and tagged out.
* The station side panel is removed for motor/gearbox access.
* Both carriages are secured with M6 socket-head screws below them before belt tension is released.
* The A-axis belt clamp and counter-balance belt clamp are removed.
* Both carriages are free from the belt.
* The lower-end M6x35 tensioning screws are loosened to release belt tension.
* The two M8 socket-head screws locking the idler pulley assembly are loosened.
* Any required motor removal is deferred to the separate referenced procedure.

## Failure Conditions

* The A-axis and counter-balance cannot be positioned as described.
* LOTO cannot be completed or verified.
* The side panel cannot be removed.
* Carriage securing screws cannot be installed below both carriages.
* One or both belt clamps cannot be removed.
* Both carriages are not free from the belt after clamp removal.
* The lower-end tensioning screws cannot be loosened or belt tension is not released.
* The idler pulley assembly lock screws cannot be loosened.
* Motor removal is attempted without the separate referenced procedure.

## Escalation Guidance

* Stop and escalate if the A-axis and counter-balance cannot be positioned between the threaded holes in the actuator base.
* Stop and escalate if carriage securing screws cannot be installed below both carriages before belt tension is released.
* Stop and escalate if LOTO cannot be completed or verified.
* Escalate to the separately referenced Motor Removal procedure on page 106 if motor removal is required.
* Do not invent missing gearbox-removal or motor-removal steps not supported by this source section.

## Missing Details / Known Gaps

* The packet does not provide the OCR text of section 7.3.7.1 Removal, so step wording is grounded primarily in the candidate and artifact retrieval text.
* No explicit estimated time is provided for this exact gearbox preparation procedure in the packet.
* The packet does not provide the detailed Operator Station Lockout/Tagout procedure steps.
* The packet does not provide the separate Motor Removal procedure content from page 106.
* The packet does not provide explicit torque values or re-assembly instructions for this procedure segment.
* The packet notes re-assembly requires a belt tension meter, but re-assembly steps are not included here.
* The packet does not provide explicit role boundaries beyond the inferred L2 support requirement.

## Source Lineage

- Candidate IDs: candidate_l2_remove_z_axis_gearbox_access_and_release_drive_components
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
