# Repair or replace the Z-Axis cable carrier

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_repair_or_replace_the_z_axis_cable_carrier_v1` |
| Title | Repair or replace the Z-Axis cable carrier |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Restore the Z-Axis cable carrier by either replacing the full carrier or repairing it when only a limited number of links are broken. The source states that the carrier snaps together and can be snapped apart by hand or with a small standard screwdriver, and that dividers between the cable and air line must be positioned fully to one side against the air line to prevent the air line from contacting the FFC.

## When To Use

Use this procedure when the Z-Axis cable carrier is damaged and needs either repair or full replacement, especially when evaluating whether only a limited number of links are broken and repair is still possible.

## Do Not Use For

* Do not use this runbook when the source does not provide enough detail to safely continue disassembly or reassembly beyond snapping links apart.
* Do not use this runbook as a complete removal and installation procedure beyond the source-supported repair-or-replace guidance.

## Safety And Operational Notes

* Wear safety glasses.
* Wear gloves.
* Stop if the source does not provide enough detail to safely continue disassembly or reassembly beyond snapping links apart.

## Access Or Tools Needed

* Replacement part: Z-Axis cable carrier
* PPE: safety glasses
* PPE: gloves
* Standard screwdriver
* 1.5-mm hex wrench
* 3/8-in. wrench/socket

## Procedure Steps

### Step 1 — Put on required PPE

**Responsible role:** L2_support

**Instruction:**
Put on safety glasses and gloves before starting the cable carrier repair or replacement work.

**Expected result:**
Required PPE is in place before maintenance begins.

**Stop or Escalate If:**

* Required PPE is unavailable.

---

### Step 2 — Gather required tools and replacement part

**Responsible role:** L2_support

**Instruction:**
Gather the replacement Z-Axis cable carrier, a standard screwdriver, a 1.5-mm hex wrench, and a 3/8-in. wrench or socket.

**Expected result:**
All required tools, PPE, and replacement part are available for the task.

**Stop or Escalate If:**

* Required tools are missing.
* Replacement Z-Axis cable carrier is unavailable.

---

### Step 3 — Inspect the cable carrier to decide repair versus replacement

**Responsible role:** L2_support

**Instruction:**
Inspect the Z-Axis cable carrier and determine whether the full carrier needs replacement or whether repair is possible because only a limited number of links are broken.

**Expected result:**
A repair-versus-replace decision is made based on the extent of broken links.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Overall Z-Axis cable carrier assembly and link arrangement to support inspection of damaged or broken links.*


**Stop or Escalate If:**

* Cable carrier damage is beyond a limited number of broken links.
* The source does not provide enough detail to safely continue.

---

### Step 4 — Snap the cable carrier apart as needed

**Responsible role:** L2_support

**Instruction:**
Snap the cable carrier apart by hand, or use a small standard screwdriver to help separate the links as needed.

**Expected result:**
The required carrier links are separated for repair or replacement work.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Carrier link construction and assembly layout while separating links.*


**Stop or Escalate If:**

* The source does not provide enough detail to safely continue disassembly beyond snapping links apart.
* Carrier links cannot be separated without forcing unsupported disassembly.

---

### Step 5 — Repair broken links or replace the full carrier

**Responsible role:** L2_support

**Instruction:**
Replace the full Z-Axis cable carrier or repair the carrier by addressing the broken links, using the replacement part as needed.

**Expected result:**
The cable carrier is restored by either full replacement or repair of broken links.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Cable carrier assembly reference during repair or full replacement.*


**Stop or Escalate If:**

* Cable carrier damage is beyond a limited number of broken links.
* The source does not provide enough detail to safely continue reassembly.

---

### Step 6 — Check divider presence in every second link

**Responsible role:** L2_support

**Instruction:**
Check the dividers between the cable and the air line in every second link. It is acceptable if several dividers are missing.

**Expected result:**
Divider presence is checked across the carrier and missing several dividers is recognized as acceptable per source guidance.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Divider locations between the cable and air line in the cable carrier links.*


**Stop or Escalate If:**

* Divider arrangement cannot be restored or verified.

---

### Step 7 — Position dividers against the air line

**Responsible role:** L2_support

**Instruction:**
Position the dividers all the way to one side against the air line to prevent the air line from contacting the FFC.

**Expected result:**
Dividers are positioned fully to one side against the air line.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Correct divider position fully to one side against the air line.*


**Stop or Escalate If:**

* Proper divider positioning cannot be restored.
* The air line still contacts or may contact the FFC.

---

### Step 8 — Visually verify carrier assembly and divider locations

**Responsible role:** L2_support

**Instruction:**
Observe the cable carrier assembly and divider locations during the work using the source figure showing the Z-Axis cable carrier assembly, example carrier links, and divider position between the cable and air line.

**Expected result:**
The assembly and divider locations visually match the source-supported reference.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Z-Axis cable carrier assembly, example carrier links, and divider position between the cable and air line.*


**Stop or Escalate If:**

* Assembly does not match the source figure.
* Divider locations cannot be visually confirmed.

---

## Success Criteria

* The Z-Axis cable carrier is repaired or replaced.
* Carrier links are reassembled.
* Dividers are positioned against the air line.
* The air line does not contact the FFC.

## Failure Conditions

* Damage is beyond a limited number of broken links.
* The source does not provide enough detail to safely continue disassembly or reassembly beyond snapping links apart.
* Proper divider positioning cannot be restored.
* The air line contacts or may contact the FFC.

## Escalation Guidance

* Escalate if cable carrier damage is beyond a limited number of broken links.
* Escalate if proper divider positioning cannot be restored.
* Stop and escalate if the source does not provide enough detail to safely continue disassembly or reassembly beyond snapping links apart.

## Missing Details / Known Gaps

* The source packet does not provide the detailed removal sequence for the existing Z-Axis cable carrier.
* The source packet does not provide the detailed installation or reassembly sequence beyond snapping links apart and together.
* The source packet does not specify whether production stop is required.
* The source packet does not specify whether LOTO is required.
* The source packet does not provide an estimated completion time.
* The source_sections text for the referenced section is empty in this packet, so detailed quoted procedure text is unavailable.

## Source Lineage

- Candidate IDs: z_axis_cable_carrier_repair_or_replacement
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
