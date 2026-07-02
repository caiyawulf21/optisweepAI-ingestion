# Install a Replacement Gripper on the A-axis

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_a_replacement_gripper_on_the_a_axis_v1` |
| Title | Install a Replacement Gripper on the A-axis |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Install the correct left or right replacement gripper onto the A-axis gearbox face, secure it with the specified fasteners and torque, reconnect the cable carrier, electrical connectors, and air line, reinstall the valve cover, and leave the assembly ready for separate leveling and commissioning.

## When To Use

Use when replacing a gripper on the A-axis and the source installation section is being followed to mechanically install the replacement gripper, reconnect associated cable and air connections, and prepare for later commissioning.

## Do Not Use For

* Do not use if the replacement gripper has not been confirmed as the correct left or right gripper.
* Do not use as a complete commissioning procedure; the source states leveling and commissioning are handled by a separate Tipper Commissioning procedure.
* Do not use to restart the operator station without following the referenced Starting The Operator Station procedure.

## Safety And Operational Notes

* Use the referenced Operator Station Lockout/Tagout procedure before performing installation work.
* The A-axis may drift down after the gripper weight is added; the source states this is acceptable.
* The counter-balance weight is approximately 43 lb (19.4 kg) total and may be one or two pieces.
* Do not pinch wires when reinstalling the valve cover.
* Do not proceed if all 10 M6x20 screws cannot be inserted due to orientation or alignment issues.

## Access Or Tools Needed

* Access to the gripper and A-axis assembly
* Operator Station Lockout/Tagout procedure
* Blue Loctite® thread locker
* 10 M6x20 socket-head screws
* Four M10 socket head screws
* Two M3x8 flat head screws
* Four M4x50 socket-head screws
* Torque tools capable of 16.5 Nm (146 in-lb) and 63 Nm (47 ft-lb)
* Replacement gripper
* Counter-balance weight
* A-axis cable carrier
* M8 connectors and gripper cable
* Supply air line
* Access to the referenced Tipper Commissioning and Starting The Operator Station procedures

## Procedure Steps

### Step 1 — Verify replacement gripper and position axis for alignment

**Responsible role:** L2_support

**Instruction:**
Verify the correct replacement gripper has been selected, specifically left gripper or right gripper, and manually position the Z-axis or A-axis to simplify alignment.

**Expected result:**
The correct replacement gripper is confirmed and the axis position supports installation alignment.

**Stop or Escalate If:**

* Stop if the selected gripper is not confirmed as the correct left or right gripper.

---

### Step 2 — Lock out the gripper

**Responsible role:** L2_support

**Instruction:**
LOTO the gripper using the referenced Operator Station Lockout/Tagout procedure.

**Expected result:**
The gripper/tipper is locked out per the referenced procedure.

**Stop or Escalate If:**

* Stop if lockout/tagout cannot be completed using the referenced procedure.

---

### Step 3 — Apply thread locker to installation fasteners

**Responsible role:** L2_support

**Instruction:**
Apply blue Loctite® thread locker to all fasteners used in these installation steps.

**Expected result:**
All specified installation fasteners are prepared with blue Loctite® before use.

---

### Step 4 — Align gripper to A-axis gearbox face

**Responsible role:** L2_support

**Instruction:**
Align the gripper bolt pattern to the A-axis gearbox face and ensure the gripper and gearbox orientation allows all 10 M6x20 socket-head screws to be inserted.

**Expected result:**
The gripper is aligned to the gearbox face with the bolt pattern oriented for full fastener insertion.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*A-axis gearbox face and surrounding mounting context to help orient the gripper during alignment.*

![artifact_fig_7_6_gearbox](assets/artifact_fig_7_6_gearbox.png)

*Additional A-axis gearbox visual context that may help confirm mounting orientation.*


**Stop or Escalate If:**

* Stop if all 10 M6x20 screws cannot be inserted due to orientation or alignment issues.

---

### Step 5 — Install the gripper mounting fasteners

**Responsible role:** L2_support

**Instruction:**
Install the 10 M6x20 gripper fasteners. It may be easier to install two fasteners on opposite sides of the bolt circle first, then insert the remaining fasteners.

**Expected result:**
All 10 M6x20 gripper fasteners are installed.

**Stop or Escalate If:**

* Stop if all 10 M6x20 screws cannot be inserted.

---

### Step 6 — Torque gripper fasteners

**Responsible role:** L2_support

**Instruction:**
Tighten the 10 M6 gripper fasteners to 16.5 Nm (146 in-lb).

**Expected result:**
All 10 M6 gripper fasteners are tightened to the specified torque.

**Stop or Escalate If:**

* Stop if the specified torque cannot be applied to the gripper fasteners.

---

### Step 7 — Account for possible A-axis drift

**Responsible role:** L2_support

**Instruction:**
Note that the A-axis may drift down after the gripper weight is added; the source states this is acceptable.

**Expected result:**
Technician recognizes that downward drift may occur after adding gripper weight.

**Stop or Escalate If:**

* Escalate if A-axis behavior appears abnormal beyond the source-noted acceptable drift.

---

### Step 8 — Attach counter-balance weight

**Responsible role:** L2_support

**Instruction:**
Attach the counter-balance weight to the counter-balance carriage using four M10 socket head screws with blue Loctite® and tighten to 63 Nm (47 ft-lb). The counter-balance weight is approximately 3-in. x 4-in. x 13-in., one or two pieces, and weighs a total of 43 lbs (19.4 kg).

**Expected result:**
The counter-balance weight is installed on the carriage and tightened to the specified torque.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Counter-balance weight location, carriage attachment area, and associated hardware context.*


**Stop or Escalate If:**

* Stop if the counter-balance weight cannot be secured with the specified hardware.
* Stop if the specified 63 Nm (47 ft-lb) torque cannot be achieved.

---

### Step 9 — Attach A-axis cable carrier to gripper

**Responsible role:** L2_support

**Instruction:**
Attach the A-axis cable carrier to the gripper using two M3x8 flat head screws (included).

**Expected result:**
The A-axis cable carrier is attached to the gripper.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Cable carrier and cable handling points relevant to reconnecting the A-axis cable carrier to the gripper.*

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Cable routing context around the tip/A-axis assembly that may help identify the cable carrier path.*


**Stop or Escalate If:**

* Stop if the cable carrier cannot be attached securely.

---

### Step 10 — Route M8 connectors through grommet

**Responsible role:** L2_support

**Instruction:**
Feed the M8 connectors from the cable through the grommet one at a time, then push the end of the jacketed cable through the grommet.

**Expected result:**
The M8 connectors and jacketed cable are routed through the grommet.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Grommet location and connector routing path for passing M8 connectors one at a time.*

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Cable routing path around the assembly that supports grommet routing.*


**Stop or Escalate If:**

* Stop if the M8 connectors or jacketed cable cannot be routed through the grommet.

---

### Step 11 — Route capped air line through grommet

**Responsible role:** L2_support

**Instruction:**
Feed the capped air line through the grommet.

**Expected result:**
The capped air line is routed through the grommet.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Shared grommet routing area used for cable connectors and air line.*

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Cable and line routing context around the tip/A-axis assembly.*


**Stop or Escalate If:**

* Stop if the air line cannot be routed through the grommet.

---

### Step 12 — Remove valve cover

**Responsible role:** L2_support

**Instruction:**
Remove the valve cover by removing the four M4x50 socket-head screws.

**Expected result:**
The valve cover is removed and the connection area is accessible.

**Screens / Images:**

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Valve cover access context referenced near tip/A-axis cable routing.*


**Stop or Escalate If:**

* Stop if the valve cover cannot be removed.

---

### Step 13 — Connect valve M8 connector

**Responsible role:** L2_support

**Instruction:**
Connect the M8x3 connector labeled "Valve" to the valve.

**Expected result:**
The valve connector is connected to the valve.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Valve connection point and M8 connector handling area.*


**Stop or Escalate If:**

* Stop if the connector labeled Valve cannot be identified or connected.

---

### Step 14 — Connect tote detect sensor connector

**Responsible role:** L2_support

**Instruction:**
Connect the M8x4 connector to the tote detect sensor.

**Expected result:**
The tote detect sensor connector is connected.

**Stop or Escalate If:**

* Stop if the M8x4 connector cannot be connected to the tote detect sensor.

---

### Step 15 — Connect long gripper sensor

**Responsible role:** L2_support

**Instruction:**
Connect the M8x3 connector labeled LONG to the longer Gripper Sensor.

**Expected result:**
The LONG connector is connected to the longer gripper sensor.

**Stop or Escalate If:**

* Stop if the LONG connector cannot be connected to the longer gripper sensor.

---

### Step 16 — Connect short gripper sensor

**Responsible role:** L2_support

**Instruction:**
Connect the M8x3 connector labeled SHORT to the shorter Gripper Sensor.

**Expected result:**
The SHORT connector is connected to the shorter gripper sensor.

**Stop or Escalate If:**

* Stop if the SHORT connector cannot be connected to the shorter gripper sensor.

---

### Step 17 — Remove air line cap and valve fitting plug

**Responsible role:** L2_support

**Instruction:**
Remove the air line cap and valve fitting plug, if present.

**Expected result:**
The air line and valve fitting are ready for connection.

**Stop or Escalate If:**

* Stop if the air line cap or valve fitting plug cannot be removed.

---

### Step 18 — Connect supply air line

**Responsible role:** L2_support

**Instruction:**
Connect the supply air line by fully inserting the line into the valve fitting.

**Expected result:**
The supply air line is connected to the valve fitting.

**Stop or Escalate If:**

* Stop if the supply air line cannot be fully inserted into the valve fitting.

---

### Step 19 — Reinstall valve cover without pinching wires

**Responsible role:** L2_support

**Instruction:**
Install the valve cover using the four M4x50 socket head screws, taking care not to pinch any wires along the cover edges and inserting the grommet into the notch for the tote sensor wire.

**Expected result:**
The valve cover is reinstalled with wires protected and the grommet seated in the tote sensor wire notch.

**Screens / Images:**

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Valve cover area and cable routing context relevant to avoiding pinched wires.*

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Connector and grommet routing context that may help confirm proper wire placement before closing the cover.*


**Stop or Escalate If:**

* Stop if wiring cannot be routed without pinching at the valve cover edges.
* Stop if the grommet cannot be seated in the tote sensor wire notch.

---

### Step 20 — Hand off to Tipper Commissioning procedure

**Responsible role:** L2_support

**Instruction:**
Refer to the Tipper Commissioning procedure for leveling and commissioning the new gripper.

**Expected result:**
The installation is handed off to the separate commissioning procedure.

**Stop or Escalate If:**

* Do not treat this procedure as complete commissioning.

---

### Step 21 — Restart operator station using referenced procedure

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced Starting The Operator Station procedure.

**Expected result:**
The operator station restart is performed using the referenced procedure.

**Stop or Escalate If:**

* Escalate if the operator station cannot be restarted using the referenced procedure.

---

## Success Criteria

* The correct left or right replacement gripper is installed on the A-axis gearbox face.
* All 10 M6x20 gripper fasteners are installed and tightened to 16.5 Nm (146 in-lb).
* The counter-balance weight is attached with four M10 socket head screws and tightened to 63 Nm (47 ft-lb).
* The A-axis cable carrier is attached to the gripper.
* M8 connectors are routed through the grommet and connected to the valve, tote detect sensor, and gripper sensors as specified.
* The supply air line is connected by fully inserting it into the valve fitting.
* The valve cover is reinstalled with no pinched wires and the grommet seated in the tote sensor wire notch.
* The assembly is ready for the separate Tipper Commissioning procedure.

## Failure Conditions

* Replacement gripper is not confirmed as the correct left or right unit.
* LOTO is not performed before installation work.
* All 10 M6x20 screws cannot be inserted due to orientation or alignment issues.
* Specified torque cannot be achieved on required fasteners.
* Cable or air line cannot be routed through the grommet.
* Required connectors cannot be identified or connected.
* Wiring is pinched at the valve cover edges or the grommet cannot be seated in the tote sensor wire notch.
* Installation is treated as complete without separate leveling and commissioning.

## Escalation Guidance

* Escalate if the correct left or right replacement gripper cannot be confirmed.
* Escalate if lockout/tagout cannot be completed using the referenced procedure.
* Escalate if gripper orientation or alignment prevents insertion of all 10 M6x20 screws.
* Escalate if required torque values cannot be achieved.
* Escalate if connectors, cable, or air line cannot be routed or connected as specified.
* Escalate if the valve cover cannot be installed without pinching wires or seating the grommet correctly.
* Escalate if operator station restart cannot be completed using the referenced startup procedure.

## Missing Details / Known Gaps

* The packet does not provide the OCR text for pages 116-120, so step wording is finalized from the candidate and packet evidence rather than direct quoted source text.
* The source packet does not provide a source-supported estimated time for this procedure.
* The packet does not provide explicit role boundaries beyond the candidate's L2_support classification.
* The packet does not provide a source-supported production stop requirement.
* Several image attachments are contextually relevant but are not confirmed as exact figures from the installation section on pages 116-120.

## Source Lineage

- Candidate IDs: candidate_l2_install_replacement_gripper_on_a_axis
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
