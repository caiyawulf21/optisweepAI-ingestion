# Install a Replacement Pneumatic Valve

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_a_replacement_pneumatic_valve_v1` |
| Title | Install a Replacement Pneumatic Valve |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Mount and reconnect a replacement pneumatic valve, reinstall the valve cover and any removed side panels, and restart the operator station using the referenced source procedure.

## When To Use

Use this procedure for the installation portion of pneumatic valve replacement after the old valve has been removed and a replacement valve is ready to be mounted and reconnected.

## Do Not Use For

* Do not use for pneumatic valve removal.
* Do not use when the three air lines cannot be confidently returned to their original locations.
* Do not use when the referenced 'Starting The Operator Station' procedure on page 66 is not available to the user.

## Safety And Operational Notes

* Take care not to pinch any wires along the edges while installing the valve cover.
* Ensure the container sensor grommet is in place during valve cover installation.
* Stop if the three air lines cannot be confidently returned to their original locations.

## Access Or Tools Needed

* Replacement pneumatic valve
* Two (2) M4 socket head screws
* Four (4) M4 socket head screws for the valve cover
* Access to the three air line connections
* Access to the M8 electrical connector
* Access to the valve cover
* Access to the top and/or bottom side panels if removed
* Referenced 'Starting The Operator Station' procedure on page 66

## Procedure Steps

### Step 1 — Mount the replacement valve

**Responsible role:** L2_support

**Instruction:**
Mount the new valve using the two (2) M4 socket head screws.

**Expected result:**
The replacement valve is mounted in the correct location.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*Valve location and surrounding installation area for pneumatic valve replacement context.*


**Stop or Escalate If:**

* Stop if the replacement valve cannot be mounted securely with the two M4 socket head screws.

---

### Step 2 — Reconnect the air lines

**Responsible role:** L2_support

**Instruction:**
Reconnect the three (3) air lines, making sure they are connected in their original location.

**Expected result:**
All three air lines are reconnected to their original locations.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*Valve area and nearby connection context that may help identify the pneumatic valve connection region.*


**Stop or Escalate If:**

* Stop if the three air lines cannot be confidently returned to their original locations.

---

### Step 3 — Reconnect the M8 electrical connector

**Responsible role:** L2_support

**Instruction:**
Reconnect the M8 electrical connector.

**Expected result:**
The M8 electrical connector is reattached to the valve.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*Valve edge / connector area for M8 electrical connector identification.*


**Stop or Escalate If:**

* Stop if the M8 electrical connector cannot be reconnected to the valve.

---

### Step 4 — Install the valve cover

**Responsible role:** L2_support

**Instruction:**
Mount the valve cover using the four (4) M4 socket head screws.

**Expected result:**
The valve cover is reinstalled over the valve assembly.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*Valve cover area and cover fastener context.*


**Stop or Escalate If:**

* Stop if the valve cover cannot be mounted securely with the four M4 socket head screws.

---

### Step 5 — Verify wire routing and grommet placement during cover installation

**Responsible role:** L2_support

**Instruction:**
While installing the valve cover, take care not to pinch any wires along the edges and ensure the container sensor grommet is in place.

**Expected result:**
No wires are pinched and the container sensor grommet is in place.

**Stop or Escalate If:**

* Stop if wires may be pinched during cover installation.
* Stop if the container sensor grommet is not in place.

---

### Step 6 — Reinstall removed side panels

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Any removed top and/or bottom side panels are reinstalled.

**Stop or Escalate If:**

* Stop if any removed top and/or bottom side panel cannot be reinstalled.

---

### Step 7 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced 'Starting The Operator Station' procedure on page 66.

**Expected result:**
The operator station restart procedure is initiated using the referenced manual section.

**Stop or Escalate If:**

* Escalate if the source-required restart procedure on page 66 is not available to the user.

---

## Success Criteria

* The replacement pneumatic valve is installed.
* The three air lines are restored to their original locations.
* The M8 electrical connector is reconnected.
* The valve cover is reinstalled with the four M4 socket head screws.
* No wires are pinched and the container sensor grommet is in place.
* Any removed top and/or bottom side panels are reinstalled.
* The operator station is restarted using the referenced procedure on page 66.

## Failure Conditions

* The three air lines cannot be confidently returned to their original locations.
* Wires may be pinched during cover installation.
* The container sensor grommet is not in place.
* The referenced 'Starting The Operator Station' procedure on page 66 is not available to the user.

## Escalation Guidance

* Stop work if the three air lines cannot be confidently returned to their original locations.
* Stop work if wires may be pinched during cover installation.
* Stop work if the container sensor grommet is not in place.
* Escalate if the referenced restart procedure on page 66 is not available.

## Missing Details / Known Gaps

* The source section text was not provided in the packet, so step wording is grounded primarily in the candidate and attached source references.
* No explicit PPE, torque values, or tool-use instructions were provided in the supplied installation section packet.
* No explicit production stop or LOTO requirement was provided for this installation subsection in the packet.
* The detailed steps for 'Starting The Operator Station' on page 66 are not included in this packet and are therefore not expanded here.
* No source-supported image artifact specifically showing the installation page 146-147 content was included; artifact_fig_7_9_pneumatic_valve is related replacement-context imagery from the same manual section family.

## Source Lineage

- Candidate IDs: candidate_l2_install_replacement_pneumatic_valve
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
