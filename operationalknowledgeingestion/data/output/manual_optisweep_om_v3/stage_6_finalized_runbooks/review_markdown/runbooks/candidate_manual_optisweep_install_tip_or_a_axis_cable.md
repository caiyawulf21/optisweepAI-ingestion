# Install Tip or A-Axis Cable (A-axis PCA to cable carrier/grommet and sensor/valve M8 connectors)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_tip_or_a_axis_cable_v1` |
| Title | Install Tip or A-Axis Cable (A-axis PCA to cable carrier/grommet and sensor/valve M8 connectors) |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi`, `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Replace/install the Tip or A-Axis cable by routing it correctly around the gearbox and into the cable carrier, securing it, routing all required M8 connectors through the grommet, connecting the labeled Valve/tote detect/LONG/SHORT gripper sensors, installing the valve cover without pinching wires, reinstalling side panels if needed, and restarting the operator station.

## When To Use

Use when the Tip or A-Axis cable needs replacement/installation and you must ensure correct cable routing, grommet use, labeled M8 connector connections (Valve, tote detect, LONG/SHORT gripper sensors), valve cover installation without pinching wires, and a successful operator station restart.

## Safety And Operational Notes

* The source references LOTO in the surrounding Tip or A-Axis cable section (7.3.15.1 REMOVAL) and includes PPE/tooling context for the Tip or A-Axis cable work.

## Access Or Tools Needed

* Physical access to the A-axis PCA, gearbox area, cable carrier, cross bars, grommet, valve, tote detect sensor, LONG/SHORT gripper sensors, and valve cover
* Wire ties
* Four M4x50 socket-head screws
* Operator station restart capability

## Visual References

![artifact_page_167_image_2](assets/db14d4bdc5149e5e.jpeg)

*Installation diagram for the Tip or A-Axis cable showing cable routing around the gearbox into the cable carrier and through the grommet with M8 connector labeling context.*

## Procedure Steps

### Step 1 — Plug new cable into A-axis PCA and route around gearbox into cable carrier

**Responsible role:** operator

**Instruction:**
Plug the new Tip or A-Axis cable into the A-axis PCA, then route the cable around the gearbox and into and around the cable carrier.

**Expected result:**
The cable is plugged into the A-axis PCA and physically routed around the gearbox and into/around the cable carrier along the intended path.

---

### Step 2 — Close cross bars with dividers between cable and air line

**Responsible role:** operator

**Instruction:**
Close all the cross bars, ensuring the dividers are positioned between the cable and the air line.

**Expected result:**
All cross bars are closed and the dividers are between the cable and the air line.

**Stop or Escalate If:**

* Stop and re-check wiring/routing if the dividers are not positioned between the cable and air line.

---

### Step 3 — Align cable markings and wire-tie in place (both cable carrier ends and A-axis carriage tie point)

**Responsible role:** operator

**Instruction:**
Align the cable markings to the cable carrier and wire-tie in place as before, including both ends of the cable carrier and the tie point on the A-axis carriage.

**Expected result:**
Cable markings align to the cable carrier and wire ties secure both ends of the cable carrier and the tie point on the A-axis carriage.

---

### Step 4 — Ensure no dangling wires near A-axis PCA; contain with wire ties

**Responsible role:** operator

**Instruction:**
Near the A-axis PCA, ensure no wires are dangling; use wire ties as needed to contain the cable.

**Expected result:**
No dangling wires are present near the A-axis PCA; cable is contained/secured with wire ties as needed.

**Stop or Escalate If:**

* Stop and re-check wiring/routing if any wires are dangling near the A-axis PCA.

---

### Step 5 — Route all four M8 connectors through grommet and push jacketed cable end through

**Responsible role:** operator

**Instruction:**
Route all four M8 connectors through the grommet one at a time, then finish by pushing the end of the jacketed cable through the grommet.

**Expected result:**
All four M8 connectors are routed through the grommet and the jacketed cable end is pushed through the grommet.

---

### Step 6 — Connect 3-pin M8 connector labeled "Valve" to the valve

**Responsible role:** operator

**Instruction:**
Connect the 3-pin M8 connector labeled "Valve" to the valve.

**Expected result:**
The 3-pin M8 connector labeled "Valve" is connected to the valve.

---

### Step 7 — Connect 4-pin M8 connector to tote detect sensor

**Responsible role:** operator

**Instruction:**
Connect the 4-pin M8 connector to the tote detect sensor.

**Expected result:**
The 4-pin M8 connector is connected to the tote detect sensor.

---

### Step 8 — Connect 3-pin M8 connector labeled "LONG" to longer gripper sensor

**Responsible role:** operator

**Instruction:**
Connect the 3-pin M8 connector labeled "LONG" to the longer gripper sensor.

**Expected result:**
The 3-pin M8 connector labeled "LONG" is connected to the longer gripper sensor.

---

### Step 9 — Connect 3-pin M8 connector labeled "SHORT" to shorter gripper sensor

**Responsible role:** operator

**Instruction:**
Connect the 3-pin M8 connector labeled "SHORT" to the shorter gripper sensor.

**Expected result:**
The 3-pin M8 connector labeled "SHORT" is connected to the shorter gripper sensor.

---

### Step 10 — Install valve cover with M4x50 screws; avoid pinching wires; seat grommet into tote sensor wire notch

**Responsible role:** operator

**Instruction:**
Install the valve cover using the four M4x50 socket-head screws. Make sure not to pinch any wires along the edges of the cover, and insert the grommet into the notch for the tote sensor wire.

**Expected result:**
Valve cover is installed with four M4x50 socket-head screws; no wires are pinched along the cover edges; grommet is inserted into the notch for the tote sensor wire.

**Stop or Escalate If:**

* Stop and re-check wiring/routing if wires appear pinched at the valve cover edges.
* Stop and re-check wiring/routing if the grommet is not seated into the notch for the tote sensor wire.

---

### Step 11 — Reinstall top and/or bottom side panels if necessary

**Responsible role:** operator

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Top and/or bottom side panels are reinstalled as required for the station configuration.

---

### Step 12 — Restart operator station

**Responsible role:** operator

**Instruction:**
Re-start the operator station (see "Starting The Operator Station" on page 66).

**Expected result:**
Operator station restarts successfully after reassembly.

**Stop or Escalate If:**

* If the operator station does not restart successfully, escalate using the site’s standard support process.

---

## Success Criteria

* Cross bars are closed with dividers positioned between the cable and air line
* Cable markings are aligned to the cable carrier and the cable is wire-tied at both cable carrier ends and the A-axis carriage tie point
* No dangling wires are present near the A-axis PCA
* All four M8 connectors are routed through the grommet and connected to the labeled targets: Valve, tote detect sensor, LONG gripper sensor, SHORT gripper sensor
* Valve cover is installed with four M4x50 socket-head screws without pinching wires along cover edges
* Grommet is inserted into the notch for the tote sensor wire
* Side panels are reinstalled if necessary
* Operator station restarts successfully

## Failure Conditions

* Any wires are dangling near the A-axis PCA
* Dividers are not positioned between the cable and air line
* Grommet is not seated into the notch for the tote sensor wire
* Wires appear pinched at the valve cover edges
* Operator station does not restart successfully

## Escalation Guidance

* If the operator station does not restart successfully, escalate using the site’s standard support process (the source does not provide additional troubleshooting steps).

## Missing Details / Known Gaps

* The source references "Starting The Operator Station" on page 66, but the actual restart procedure steps are not included in the provided packet; only the restart instruction is available here.

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_install_tip_or_a_axis_cable
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
