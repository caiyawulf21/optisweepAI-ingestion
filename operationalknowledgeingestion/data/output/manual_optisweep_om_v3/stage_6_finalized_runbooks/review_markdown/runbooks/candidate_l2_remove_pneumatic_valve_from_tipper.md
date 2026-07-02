# Remove Pneumatic Valve From Tipper

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_pneumatic_valve_from_tipper_v1` |
| Title | Remove Pneumatic Valve From Tipper |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely remove the pneumatic valve from the tipper to support valve replacement work. This source-specific runbook covers the documented removal portion only: lockout/tagout, PPE, tool gathering, side panel access if needed, valve cover removal, electrical disconnection, air line disconnection, and valve fastener removal.

## When To Use

Use when the pneumatic valve on the tipper must be removed as part of the documented pneumatic valve replacement/removal procedure in the OptiSweep Operation and Maintenance Manual.

## Do Not Use For

* Do not use for pneumatic valve installation or post-install verification; this source section covers removal only.
* Do not use if lockout/tagout cannot be completed using the referenced Operator Station Lockout/Tagout procedure.
* Do not use if connector or air line locations cannot be positively identified before disconnection.

## Safety And Operational Notes

* Lockout/tagout the tipper using the referenced Operator Station Lockout/Tagout procedure before beginning removal work.
* Wear safety glasses and gloves.
* Note where each air line connects before removal.
* Stop if the lockout/tagout cannot be completed using the referenced procedure.

## Access Or Tools Needed

* Access to the tipper
* Operator Station Lockout/Tagout procedure on page 2
* Safety glasses
* Gloves
* 2.5-mm hex wrench
* 3-mm hex wrench
* 5-mm hex wrench
* 6-mm hex wrench
* 3/8-in. wrench or socket
* Loctite
* Replacement pneumatic valve

## Procedure Steps

### Step 1 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure on page 2 before starting pneumatic valve removal.

**Expected result:**
The tipper is locked out and tagged out in accordance with the referenced procedure.

**Stop or Escalate If:**

* Stop if the lockout/tagout cannot be completed using the referenced procedure.

---

### Step 2 — Put on required PPE

**Responsible role:** L2_support

**Instruction:**
Put on safety glasses and gloves.

**Expected result:**
Required PPE is in place before removal work continues.

**Stop or Escalate If:**

* Stop if required PPE is not available.

---

### Step 3 — Gather required tools and materials

**Responsible role:** L2_support

**Instruction:**
Gather the listed tools and replacement-related materials from the source: 2.5-mm hex wrench, 3-mm hex wrench, 5-mm hex wrench, 6-mm hex wrench, 3/8-in. wrench or socket, and Loctite.

**Expected result:**
The required tools and listed material are available at the work area.

**Stop or Escalate If:**

* Escalate if required tools or listed materials are not available.

---

### Step 4 — Remove the station side panel if needed

**Responsible role:** L2_support

**Instruction:**
If necessary, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel, then remove the station side panel to access the valve area.

**Expected result:**
The station side panel is removed when needed and the valve area is accessible.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*Use the pneumatic valve figure for general valve-area location after side panel access is opened.*


**Stop or Escalate If:**

* Escalate if the valve cannot be accessed after removing the documented side panel fasteners.
* Escalate if the side panel cannot be removed using the documented fasteners.

---

### Step 5 — Remove the valve cover

**Responsible role:** L2_support

**Instruction:**
Remove the four M4 socket-head screws holding the valve cover in place, then remove the valve cover.

**Expected result:**
The valve cover is removed and the valve is exposed.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*Valve cover area and the four M4 socket-head screws referenced for cover removal.*


**Stop or Escalate If:**

* Escalate if the valve cover cannot be removed using the documented fasteners.

---

### Step 6 — Disconnect the M8 electrical connector

**Responsible role:** L2_support

**Instruction:**
Disconnect the M8 electrical connector from the edge of the valve.

**Expected result:**
The M8 electrical connector is disconnected from the valve.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*M8 electrical connector location at the edge of the valve.*


**Stop or Escalate If:**

* Stop if connector location cannot be positively identified before disconnection.

---

### Step 7 — Disconnect the three air lines

**Responsible role:** L2_support

**Instruction:**
Disconnect the three air lines going to the valve, noting where each line connects before removal.

**Expected result:**
All three air lines are disconnected and their connection positions have been noted.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*Three air line connections and their positions on the valve.*


**Stop or Escalate If:**

* Stop if air line locations cannot be positively identified before disconnection.
* Escalate if the air lines cannot be disconnected using the documented removal approach.

---

### Step 8 — Remove the valve mounting screws

**Responsible role:** L2_support

**Instruction:**
Remove the two M4 socket-head screws holding the valve in place.

**Expected result:**
The pneumatic valve is unfastened from the tipper and ready to be removed for replacement.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*Two M4 screws that secure the valve.*


**Stop or Escalate If:**

* Escalate if the valve cannot be accessed or removed using the documented fasteners and connections.

---

## Success Criteria

* The tipper has been locked out and tagged out using the referenced procedure.
* The valve area has been accessed as needed.
* The valve cover has been removed.
* The M8 electrical connector has been disconnected.
* The three air lines have been disconnected with their connection positions noted before removal.
* The two valve mounting screws have been removed.
* The pneumatic valve is disconnected and unfastened from the tipper, ready for replacement.

## Failure Conditions

* Lockout/tagout cannot be completed using the referenced procedure.
* Required PPE or tools are unavailable.
* The valve area cannot be accessed using the documented side panel removal.
* The valve cover cannot be removed using the documented fasteners.
* Connector or air line locations cannot be positively identified before disconnection.
* The valve cannot be accessed or removed using the documented fasteners and connections.

## Escalation Guidance

* Use L2_support because the source includes LOTO and component removal work.
* Stop if the lockout/tagout cannot be completed using the referenced procedure.
* Stop if connector or air line locations cannot be positively identified before disconnection.
* Escalate if the valve cannot be accessed or removed using the documented fasteners and connections.

## Missing Details / Known Gaps

* The source packet does not provide the OCR text of section 7.3.9.1, so step wording is grounded primarily in the candidate and artifact retrieval text.
* The source does not provide explicit role boundaries beyond the candidate classification of L2_support.
* The source does not provide explicit production stop status.
* The source packet does not include a dedicated artifact specifically showing the station side panel access area beyond the general pneumatic valve figure.
* The source section in this packet covers removal only and does not include installation, torque values, or post-removal verification steps.

## Source Lineage

- Candidate IDs: candidate_l2_remove_pneumatic_valve_from_tipper
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
