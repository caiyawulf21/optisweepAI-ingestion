# Repair Broken Links In The Z-Axis Cable Carrier

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_repair_broken_links_in_the_z_axis_cable_carrier_v1` |
| Title | Repair Broken Links In The Z-Axis Cable Carrier |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Repair the Z-Axis cable carrier when only a limited number of links are broken by snapping apart the carrier, replacing the broken link sections, verifying divider placement between the cable and air line, and snapping the carrier back together.

## When To Use

Use this procedure when the Z-Axis cable carrier has broken links and the damage is limited enough that repair is appropriate instead of full replacement.

## Do Not Use For

* Do not use when damage is beyond a limited number of broken links.
* Do not use when divider placement cannot be verified.
* Do not use when the air line may contact the FFC after reassembly.

## Safety And Operational Notes

* Wear safety glasses and gloves.
* This is a physical maintenance repair task involving manual disassembly and reassembly of the cable carrier.
* The source packet does not provide explicit LOTO or production-stop requirements for this specific procedure.

## Access Or Tools Needed

* Physical access to the Z-Axis cable carrier
* Replacement part: Z-Axis cable carrier
* PPE: safety glasses
* PPE: gloves
* Standard screwdriver
* 1.5-mm hex wrench
* 3/8-in. wrench/socket
* Figure 7-17 Cable Carrier

## Procedure Steps

### Step 1 — Put on required PPE

**Responsible role:** L2_support

**Instruction:**
Put on safety glasses and gloves before starting the repair.

**Expected result:**
Required PPE is in place before handling the cable carrier.

**Stop or Escalate If:**

* Required PPE is unavailable.

---

### Step 2 — Gather tools and replacement parts

**Responsible role:** L2_support

**Instruction:**
Obtain the replacement Z-Axis cable carrier, standard screwdriver, 1.5-mm hex wrench, and 3/8-in. wrench or socket.

**Expected result:**
All listed tools and parts are available at the work area.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Use the cable carrier figure to confirm the component being repaired.*


**Stop or Escalate If:**

* Replacement carrier or required tools are unavailable.

---

### Step 3 — Inspect broken links and confirm repair scope

**Responsible role:** L2_support

**Instruction:**
Inspect the Z-Axis cable carrier and identify the broken links to confirm the repair is limited to a limited number of links.

**Expected result:**
Broken links are identified and the repair scope is confirmed as limited.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Identify the Z-Axis cable carrier assembly and the link sections that may be broken.*


**Stop or Escalate If:**

* Damage is beyond a limited number of broken links.
* It is unclear whether repair is appropriate instead of full replacement.

---

### Step 4 — Snap apart the cable carrier

**Responsible role:** L2_support

**Instruction:**
Snap apart the cable carrier by hand or with the help of a small standard screwdriver.

**Expected result:**
The cable carrier is separated at the required link sections for repair access.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Use the cable carrier figure to orient to the carrier link construction before snapping links apart.*


**Stop or Escalate If:**

* The carrier cannot be snapped apart using the source-supported method.
* Additional damage is observed while separating the links.

---

### Step 5 — Replace broken link sections

**Responsible role:** L2_support

**Instruction:**
Repair the cable carrier by replacing the broken link sections using the snap-together carrier construction.

**Expected result:**
Broken link sections are replaced and the carrier is ready for divider verification and reassembly.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Use the figure to identify the cable carrier assembly while replacing broken link sections.*


**Stop or Escalate If:**

* Broken sections cannot be repaired with replacement link sections.
* Damage appears more extensive than initially assessed.

---

### Step 6 — Verify divider presence and position

**Responsible role:** L2_support

**Instruction:**
Check the dividers between the cable and the air line in every second link and verify their position.

**Expected result:**
Divider placement has been checked in every second link where dividers are present.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Look for divider locations between the cable and air line in every second link.*


**Stop or Escalate If:**

* Divider placement cannot be verified.
* The air line may contact the FFC.

---

### Step 7 — Position dividers against the air line

**Responsible role:** L2_support

**Instruction:**
Position the dividers all the way to one side against the air line to prevent the air line from contacting the FFC.

**Expected result:**
Dividers are positioned fully to one side against the air line.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Confirm divider position fully to one side against the air line.*


**Stop or Escalate If:**

* Divider placement cannot be set as required.
* The air line may still contact the FFC after positioning.

---

### Step 8 — Snap the cable carrier back together

**Responsible role:** L2_support

**Instruction:**
Reassemble the cable carrier by snapping the links back together.

**Expected result:**
The cable carrier is reassembled with repaired links and verified divider positioning.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Use the figure to confirm overall cable carrier assembly orientation during reassembly.*


**Stop or Escalate If:**

* Links do not snap back together.
* Divider placement cannot be maintained during reassembly.
* The air line may contact the FFC after reassembly.

---

## Success Criteria

* The Z-Axis cable carrier is repaired.
* The carrier links are snapped back together.
* Dividers are positioned against the air line.
* The air line does not contact the FFC.

## Failure Conditions

* Damage is beyond a limited number of broken links.
* The carrier cannot be snapped apart or reassembled as required.
* Divider placement cannot be verified.
* The air line may contact the FFC after reassembly.

## Escalation Guidance

* Escalate if the damage is beyond a limited number of broken links because the source distinguishes repair from full replacement but does not provide a decision threshold.
* Escalate if divider placement cannot be verified.
* Escalate if the air line may contact the FFC after reassembly.

## Missing Details / Known Gaps

* The source does not provide an exact threshold for what qualifies as a limited number of broken links.
* The source does not provide a detailed disassembly sequence beyond snapping the carrier apart.
* The source does not provide a detailed reassembly sequence beyond snapping the links back together.
* The source does not provide explicit LOTO requirements for this specific procedure in the supplied packet.
* The source does not provide an estimated time for this procedure in the supplied packet.
* The source packet does not provide exact instructions for use of the 1.5-mm hex wrench or 3/8-in. wrench/socket during this repair.

## Source Lineage

- Candidate IDs: candidate_l2_repair_z_axis_cable_carrier_broken_links
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
