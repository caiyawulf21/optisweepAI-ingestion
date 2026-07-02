# Install Z-Axis Sensor And Route CLINK Wiring

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_z_axis_sensor_and_route_clink_wiring_v1` |
| Title | Install Z-Axis Sensor And Route CLINK Wiring |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Mount the Z-axis sensor on the rear side, route the Z-axis wire down through the column and out the lower grommet into the control box, connect the wire to a documented control box input, and restart the operator station using the referenced startup procedure.

## When To Use

Use when performing the documented Z-axis sensor installation and CLINK wiring connection described in the OptiSweep Operation and Maintenance Manual.

## Do Not Use For

* Do not use for selecting among I/O1, DI6, or DI7 when the source does not provide criteria for that choice.
* Do not use when the referenced operator station restart procedure on page 66 is unavailable.

## Safety And Operational Notes

* This procedure is not marked support-safe in the candidate.
* Do not invent connection selection logic for I/O1, DI6, or DI7 beyond what is documented in the source.

## Access Or Tools Needed

* Physical access to the sensor mounting location
* Access to the rear-side wire routing hole
* Access to the column, lower grommet, and control box
* M3 button-head screw
* Figure 7-2: Z-Axis CLINK Connections
* Referenced procedure: Starting The Operator Station

## Procedure Steps

### Step 1 — Mount the Z-axis sensor at the rear-side routing hole

**Responsible role:** L2_support

**Instruction:**
Feed the sensor through the wire routing hole on the rear side and fasten it in place using the M3 button-head screw.

**Expected result:**
The Z-axis sensor is installed at the rear-side mounting location and secured with the M3 button-head screw.

**Screens / Images:**

![artifact_fig_7_2_z_axis_clink_connections](assets/artifact_fig_7_2_z_axis_clink_connections.jpeg)

*Rear-side wire routing hole and Z-axis sensor mounting location referenced by the installation text.*


**Stop or Escalate If:**

* The installer cannot identify the rear wire routing hole from the available source material.
* The installer cannot identify the sensor mounting location from the available source material.

---

### Step 2 — Route the Z-axis wire through the column to the control box

**Responsible role:** L2_support

**Instruction:**
Route the Z-axis wire down through the column and out the lower grommet into the control box.

**Expected result:**
The Z-axis wire follows the documented path through the column and exits the lower grommet into the control box.

**Screens / Images:**

![artifact_fig_7_2_z_axis_clink_connections](assets/artifact_fig_7_2_z_axis_clink_connections.jpeg)

*Z-axis wire routing path through the column and lower grommet exit into the control box.*


**Stop or Escalate If:**

* The installer cannot identify the lower grommet from the available source material.
* The documented wire routing path through the column is unclear or cannot be followed.

---

### Step 3 — Connect the Z-axis wire in the control box

**Responsible role:** L2_support

**Instruction:**
Plug the Z-axis wire into either I/O1, DI6, or DI7 in the control box.

**Expected result:**
The Z-axis wire is connected to a documented control box input.

**Screens / Images:**

![artifact_fig_7_2_z_axis_clink_connections](assets/artifact_fig_7_2_z_axis_clink_connections.jpeg)

*Documented control box connection points labeled I/O1, DI6, or DI7.*


**Stop or Escalate If:**

* The installer cannot identify the documented I/O1, DI6, or DI7 locations from the available source material.
* The source does not provide criteria for choosing among I/O1, DI6, or DI7.

---

### Step 4 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced startup procedure on page 66.

**Expected result:**
The operator station is restarted using the referenced procedure.

**Stop or Escalate If:**

* The referenced operator station restart procedure is not available.

---

## Success Criteria

* The Z-axis sensor is mounted at the documented rear-side location.
* The Z-axis wire is routed down through the column and out the lower grommet into the control box.
* The wire is connected to a documented control box input.
* The operator station is restarted using the referenced startup procedure.

## Failure Conditions

* Rear wire routing hole or mounting location cannot be identified.
* Lower grommet or wire routing path through the column cannot be identified.
* Control box connection points I/O1, DI6, or DI7 cannot be identified.
* The source does not provide criteria for choosing among I/O1, DI6, or DI7.
* The referenced operator station restart procedure is not available.

## Escalation Guidance

* Escalate if the installer cannot identify the rear wire routing hole, lower grommet, control box connection points, or the documented I/O1, DI6, or DI7 locations from the available source material.
* Escalate if the referenced operator station restart procedure is not available.
* Escalate for SME review if a selection must be made among I/O1, DI6, or DI7 because the source does not explain how to choose.

## Missing Details / Known Gaps

* The source packet does not include the actual body text of section 7.3.2.1.2; step wording is grounded in the candidate and artifact retrieval text.
* The source does not explain how to choose among I/O1, DI6, or DI7.
* The referenced operator station startup procedure on page 66 is not included in this packet.
* No explicit production stop, LOTO requirement, or time estimate is provided in the supplied packet for this procedure.

## Source Lineage

- Candidate IDs: candidate_l2_install_z_axis_sensor_and_route_clink_wiring
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
