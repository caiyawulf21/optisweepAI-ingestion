# Replace The Z-Axis Cable Carrier

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_replace_the_z_axis_cable_carrier_v1` |
| Title | Replace The Z-Axis Cable Carrier |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Replace the Z-Axis cable carrier using the listed replacement part, PPE, and tools, and verify divider placement so the air line does not contact the FFC. The source confirms the carrier can be fully replaced and that the links snap together and apart, but it does not provide a complete removal and installation sequence.

## When To Use

Use when the Z-Axis cable carrier needs full replacement and the technician needs source-supported guidance on required PPE, tools, carrier identification, snap-apart/snap-together handling, and divider positioning.

## Do Not Use For

* Do not use as a complete removal and installation procedure when a full step-by-step sequence is required, because the source does not provide one.
* Do not use when the task requires unsupported decisions beyond the source-provided replacement, snap-apart handling, and divider-position verification guidance.

## Safety And Operational Notes

* Wear safety glasses and gloves.
* Support safety is not established as safe for general operator execution in the source candidate; treat as maintenance work requiring L2 support.
* Ensure divider placement prevents the air line from contacting the FFC.

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
Put on safety glasses and gloves before handling the Z-Axis cable carrier replacement task.

**Expected result:**
Required PPE is in place before physical work begins.

**Stop or Escalate If:**

* Required PPE is unavailable.

---

### Step 2 — Gather replacement part and tools

**Responsible role:** L2_support

**Instruction:**
Obtain the replacement Z-Axis cable carrier and the listed tools: standard screwdriver, 1.5-mm hex wrench, and 3/8-in. wrench or socket.

**Expected result:**
All required parts and tools are available at the work area.

**Stop or Escalate If:**

* The replacement Z-Axis cable carrier is not available.
* Required tools are missing.

---

### Step 3 — Identify the Z-Axis cable carrier assembly

**Responsible role:** L2_support

**Instruction:**
Locate the existing Z-Axis cable carrier assembly and use Figure 7-17 to identify the part being replaced.

**Expected result:**
The technician has positively identified the Z-Axis cable carrier assembly.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*The Z-Axis cable carrier assembly shown in Figure 7-17 to identify the part being replaced.*


**Stop or Escalate If:**

* The Z-Axis cable carrier assembly cannot be positively identified.

---

### Step 4 — Remove or snap apart the existing cable carrier

**Responsible role:** L2_support

**Instruction:**
Snap apart or remove the existing cable carrier by hand, or use a small standard screwdriver where needed, because the carrier snaps together and apart.

**Expected result:**
The existing cable carrier is separated or removed using the snap-apart method described by the source.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*The cable carrier construction and link arrangement referenced by Figure 7-17 while separating the snap-together carrier.*


**Stop or Escalate If:**

* The replacement cannot be completed from the source-provided information because the section does not provide a full removal and installation sequence.
* The carrier does not separate by hand or with a small standard screwdriver as described.

---

### Step 5 — Install the replacement cable carrier

**Responsible role:** L2_support

**Instruction:**
Install the replacement Z-Axis cable carrier, using the source-supported understanding that the carrier links snap together.

**Expected result:**
The replacement cable carrier is installed in place of the old carrier.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*The cable carrier assembly in Figure 7-17 as a visual reference during replacement installation.*


**Stop or Escalate If:**

* The replacement cannot be completed from the source-provided information because the section does not provide a full removal and installation sequence.

---

### Step 6 — Inspect divider placement in the carrier links

**Responsible role:** L2_support

**Instruction:**
Check the dividers between the cable and the air line in every second link and verify their position using Figure 7-17.

**Expected result:**
Divider presence and placement are reviewed across the carrier links.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Dividers between the cable and air line and the correct side for divider placement.*


**Stop or Escalate If:**

* Divider placement cannot be verified from the available source evidence.
* The air line may contact the FFC after replacement.

---

### Step 7 — Set dividers against the air line

**Responsible role:** L2_support

**Instruction:**
Position the dividers all the way to one side against the air line.

**Expected result:**
Divider placement protects the FFC from air-line contact.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Divider orientation relative to the air line so the divider is fully to one side against the air line.*


**Stop or Escalate If:**

* The air line may contact the FFC after replacement.

---

### Step 8 — Verify all snap-together links are fully connected

**Responsible role:** L2_support

**Instruction:**
Verify the replacement carrier is assembled with the snap-together links fully connected.

**Expected result:**
The replacement carrier is fully assembled and ready for service.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Overall cable carrier assembly in Figure 7-17 while confirming the replacement links are fully connected.*


**Stop or Escalate If:**

* Links do not remain fully connected.
* The air line may contact the FFC after replacement.

---

## Success Criteria

* The Z-Axis cable carrier is replaced.
* The replacement carrier is assembled with snap-together links fully connected.
* Dividers are positioned all the way to one side against the air line.
* The air line does not contact the FFC.

## Failure Conditions

* The replacement cannot be completed from the source-provided information because the section does not provide a full removal and installation sequence.
* The Z-Axis cable carrier assembly cannot be confidently identified.
* The carrier cannot be separated or reassembled using the source-described snap-together method.
* Divider placement cannot be verified.
* The air line may contact the FFC after replacement.

## Escalation Guidance

* Escalate if the replacement cannot be completed from the source-provided information because the section does not provide a full removal and installation sequence.
* Escalate if the air line may contact the FFC after replacement.

## Missing Details / Known Gaps

* The source does not provide a complete step-by-step removal and installation sequence for full cable carrier replacement.
* The source does not specify whether production stop is required.
* The source does not specify whether LOTO is required for this procedure.
* The source does not provide an estimated completion time.
* The source does not define detailed role boundaries beyond maintenance-style execution.

## Source Lineage

- Candidate IDs: candidate_l2_replace_z_axis_cable_carrier
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
