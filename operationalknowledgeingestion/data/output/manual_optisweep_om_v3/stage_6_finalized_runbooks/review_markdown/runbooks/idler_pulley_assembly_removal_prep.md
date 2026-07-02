# Prepare for idler pulley assembly removal

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_prepare_for_idler_pulley_assembly_removal_v1` |
| Title | Prepare for idler pulley assembly removal |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely prepare the tipper for idler pulley assembly removal by performing lockout/tagout, removing the station side panel if motor access is needed, positioning the A-axis and counterbalance between the threaded holes in the actuator base, verifying carriage alignment relative to the rail holes, and installing M6 socket-head screws below both carriages so the A-axis and counterbalance cannot drop when belt tension is released.

## When To Use

Use this procedure when preparing the OptiSweep tipper for idler pulley assembly replacement/removal and before belt tension is released in the idler pulley assembly service task.

## Do Not Use For

* Do not use this as a complete idler pulley assembly replacement procedure; the packet only supports the preparation and early removal setup steps.
* Do not use if lockout/tagout cannot be completed.
* Do not use if the A-axis and counterbalance cannot be positioned and secured with M6 socket-head screws as described.

## Safety And Operational Notes

* Perform lockout/tagout on the tipper before beginning removal preparation.
* Secure the A-axis and counterbalance with M6 socket-head screws before belt tension is released to prevent dropping.
* Use safety glasses and gloves.

## Access Or Tools Needed

* Replacement part: idler pulley assembly
* PPE: safety glasses
* PPE: gloves
* 5-mm hex wrench
* 6-mm hex wrench
* 3/8-in. wrench or socket
* Loctite
* sonic belt tension meter
* Access to the station side panel and motor area
* M6 socket-head screws

## Procedure Steps

### Step 1 — Lock out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper as referenced by "Operator Station Lockout/Tagout" on page 2.

**Expected result:**
The tipper is locked out and safe for maintenance access.

**Stop or Escalate If:**

* LOTO cannot be completed.

---

### Step 2 — Remove the station side panel if motor access is needed

**Responsible role:** L2_support

**Instruction:**
If needed for motor access, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel, then remove the station side panel.

**Expected result:**
The station side panel is removed when needed and the motor access area is exposed.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly maintenance figure for the service area associated with motor access and removal preparation.*


**Stop or Escalate If:**

* Motor access is needed but the station side panel cannot be removed.

---

### Step 3 — Position the A-axis and counterbalance

**Responsible role:** L2_support

**Instruction:**
Manually position the A-axis and the counterbalance between the threaded holes in the actuator base.

**Expected result:**
The A-axis and counterbalance are positioned between the threaded holes in the actuator base.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly area and surrounding service location used during A-axis and counterbalance positioning.*


**Stop or Escalate If:**

* The A-axis and counterbalance cannot be positioned as described.

---

### Step 4 — Verify carriage alignment with the rail holes

**Responsible role:** L2_support

**Instruction:**
Verify there are two holes adjacent to each rail and that the carriages are positioned between the holes on the respective rails.

**Expected result:**
Each rail has two adjacent holes and each carriage is positioned between the holes on its respective rail.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Service area around the idler pulley assembly and adjacent A-axis/counterbalance components to confirm carriage position relative to the rail holes.*


**Stop or Escalate If:**

* The carriages are not positioned between the holes on the respective rails.

---

### Step 5 — Install M6 socket-head screws below both carriages

**Responsible role:** L2_support

**Instruction:**
Thread M6 socket-head screws into the holes below both carriages to prevent the A-axis and counterbalance from dropping once belt tension is released.

**Expected result:**
M6 socket-head screws are installed below both carriages and the A-axis and counterbalance are secured against dropping.

**Screens / Images:**

![artifact_fig_7_21_idler_pulley_assembly](assets/artifact_fig_7_21_idler_pulley_assembly.png)

*Idler pulley assembly figure and adjacent A-axis/counterbalance area near the motor access area where the M6 socket-head screws are installed below both carriages.*


**Stop or Escalate If:**

* The A-axis and counterbalance cannot be positioned and secured with M6 socket-head screws as described.
* The M6 socket-head screws cannot be installed below both carriages.

---

## Success Criteria

* The tipper is locked out.
* The motor access area is exposed if required.
* The A-axis and counterbalance are positioned between the threaded holes in the actuator base.
* The carriages are positioned between the adjacent holes on the respective rails.
* M6 socket-head screws are installed below both carriages before belt tension is released.

## Failure Conditions

* LOTO cannot be completed.
* The station side panel cannot be removed when motor access is needed.
* The A-axis and counterbalance cannot be positioned between the threaded holes in the actuator base.
* The carriages are not positioned between the holes on the respective rails.
* M6 socket-head screws cannot be installed below both carriages.
* The A-axis and counterbalance are not secured before belt tension is released.

## Escalation Guidance

* Stop and escalate if lockout/tagout cannot be completed.
* Stop and escalate if the A-axis and counterbalance cannot be positioned and secured with M6 socket-head screws as described.
* Escalate for additional source material because the provided source section is truncated and does not include the remaining removal or installation steps.

## Missing Details / Known Gaps

* The packet does not include the full removal sequence after the preparation steps.
* The packet does not include installation or reassembly steps.
* The packet does not provide explicit role boundaries beyond the inferred L2_support role.
* The packet does not provide explicit production stop status.
* The source section text in the packet is empty/truncated, so step wording is grounded primarily in the candidate and artifact summaries.

## Source Lineage

- Candidate IDs: idler_pulley_assembly_removal_prep
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
