# Install Tote Sensor And Restore Operator Station

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_tote_sensor_and_restore_operator_station_v1` |
| Title | Install Tote Sensor And Restore Operator Station |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Mount and reconnect the tote sensor, restore the wire grommet placement, and restart the operator station after tote sensor replacement using the documented installation section and referenced startup procedure.

## When To Use

Use this procedure after tote sensor removal or replacement work when the source-directed installation steps must be completed and the operator station must be returned to service.

## Do Not Use For

* Do not use this procedure as a standalone tote sensor removal procedure.
* Do not use this procedure to perform operator station startup beyond the referenced "Starting The Operator Station" procedure on page 66.
* Do not proceed if required installation details are unavailable in the current source packet.

## Safety And Operational Notes

* This procedure is associated with sensor replacement work and the source section includes LOTO in the removal procedure context.
* Use safety glasses and gloves as listed in the source candidate tools and PPE.
* Do not proceed beyond source-backed restart steps; use the referenced operator station startup procedure on page 66.

## Access Or Tools Needed

* Replacement tote sensor
* Safety glasses
* Gloves
* 1.5-mm hex wrench
* 6-mm hex wrench
* Access to the tote sensor mounting location
* Access to the operator station restart procedure on page 66

## Procedure Steps

### Step 1 — Mount the tote sensor

**Responsible role:** L2_support

**Instruction:**
Mount the tote sensor with the M3 socket-head screws.

**Expected result:**
The tote sensor is fastened in place at its mounting location.

**Stop or Escalate If:**

* The sensor cannot be mounted.
* The mounting points or required figure details are unclear from the available packet evidence.

---

### Step 2 — Connect the M8 connector

**Responsible role:** L2_support

**Instruction:**
Connect the M8 connector to the tote sensor.

**Expected result:**
The M8 connector is connected to the tote sensor.

**Stop or Escalate If:**

* The M8 connector cannot be connected.
* The connector location cannot be confirmed from the available packet evidence.

---

### Step 3 — Restore the wire grommet

**Responsible role:** L2_support

**Instruction:**
Put the small grommet around the wire back into the slot in the valve cover.

**Expected result:**
The small grommet is back around the wire and seated in the valve cover slot.

**Stop or Escalate If:**

* The grommet cannot be restored to the valve cover slot.
* The wire or grommet does not fit back into the documented position.

---

### Step 4 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the documented "Starting The Operator Station" procedure on page 66.

**Expected result:**
The operator station is restarted using the referenced source procedure.

**Stop or Escalate If:**

* The operator station cannot be restarted.
* The referenced startup procedure on page 66 is not available to the technician.
* Additional restart steps would require unsupported details not present in this packet.

---

## Success Criteria

* The tote sensor is mounted with the M3 socket-head screws.
* The M8 connector is connected to the tote sensor.
* The small grommet around the wire is returned to the slot in the valve cover.
* The operator station is restarted using the referenced page 66 procedure.

## Failure Conditions

* The sensor cannot be mounted.
* The M8 connector cannot be connected.
* The grommet cannot be restored to the valve cover slot.
* The operator station cannot be restarted using the referenced procedure.

## Escalation Guidance

* Escalate if the sensor cannot be mounted, the M8 connector cannot be connected, or the grommet cannot be restored to the valve cover slot.
* Escalate if the referenced operator station startup procedure on page 66 is unavailable or insufficient to complete restart from the current state.
* Escalate if additional installation details are needed that are not supported by the current source packet.

## Missing Details / Known Gaps

* No tote-sensor-specific artifact ID was provided for the figure referenced in the installation notes.
* The current packet does not include the actual page 66 startup procedure steps, so restart remains a referenced external procedure only.
* The packet does not provide explicit confirmation of whether LOTO is required for this installation subsection itself.
* The packet does not provide an estimated completion time for this procedure.
* The packet does not provide explicit torque values, alignment criteria, or verification checks for the tote sensor installation.

## Source Lineage

- Candidate IDs: candidate_l2_install_tote_sensor_and_restore_operator_station
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
