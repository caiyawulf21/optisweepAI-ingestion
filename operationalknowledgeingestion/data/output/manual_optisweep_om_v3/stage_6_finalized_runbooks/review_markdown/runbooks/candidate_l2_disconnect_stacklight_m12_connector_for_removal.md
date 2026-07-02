# Disconnect the Stacklight M12 Connector During Stacklight Removal

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_disconnect_the_stacklight_m12_connector_during_stacklight_removal_v1` |
| Title | Disconnect the Stacklight M12 Connector During Stacklight Removal |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Source-specific runbook for the documented stacklight removal action in the OptiSweep Operation and Maintenance Manual. The provided source excerpt identifies required items, references Figure 7-22 for stacklight identification, and instructs the technician to disconnect the M12 connector from the stacklight as the first removal step in stacklight replacement.

## When To Use

Use when performing the documented removal portion of stacklight replacement and the task required is to disconnect the M12 connector from the stacklight using the source-backed items and figure reference provided in Section 7.3.21 / 7.3.21.1 Removal.

## Do Not Use For

* Do not use as a complete stacklight replacement procedure because the packet provides only the first explicit removal step.
* Do not use when safety isolation, production stop, or LOTO requirements must be confirmed from this excerpt alone.
* Do not use if the stacklight assembly or M12 connector cannot be clearly identified from the provided source-backed figure and text.

## Safety And Operational Notes

* This runbook is not support-safe for general execution from this excerpt alone because full safety isolation and complete removal details are not included in the packet.
* Use the listed PPE: safety glasses and gloves.
* Only the first removal instruction is present in the supplied source evidence; additional removal or replacement actions are outside this finalized source-specific runbook.

## Access Or Tools Needed

* Physical access to the stacklight
* Replacement part: three-segment stacklight
* PPE: safety glasses
* PPE: gloves
* 7-mm wrench

## Procedure Steps

### Step 1 — Gather listed PPE, tool, and replacement part

**Responsible role:** L2_support

**Instruction:**
Gather the listed items for the stacklight replacement/removal task: replacement three-segment stacklight, safety glasses, gloves, and a 7-mm wrench.

**Expected result:**
The listed PPE, tool, and replacement part are available for the task.

**Screens / Images:**

![artifact_fig_7_22_stacklight](assets/artifact_fig_7_22_stacklight.png)

*Use the stacklight photo as the referenced visual for the stacklight replacement procedure while preparing for the removal task.*


**Stop or Escalate If:**

* Required PPE, tool, or replacement part is not available.
* The source-backed visual reference needed for identification is unavailable.

---

### Step 2 — Locate the stacklight and identify the M12 connector

**Responsible role:** L2_support

**Instruction:**
Locate the stacklight assembly and identify the M12 connector on the stacklight using Figure 7-22 as the source-backed visual reference.

**Expected result:**
The technician has identified the stacklight assembly and the M12 connector to be disconnected.

**Screens / Images:**

![artifact_fig_7_22_stacklight](assets/artifact_fig_7_22_stacklight.png)

*Look at the stacklight assembly shown in Figure 7-22 and use it to identify the stacklight and the connector location referenced by the procedure.*


**Stop or Escalate If:**

* The M12 connector cannot be clearly identified from the source-backed information.
* The physical assembly does not match the Figure 7-22 reference well enough to proceed confidently.

---

### Step 3 — Disconnect the M12 connector from the stacklight

**Responsible role:** L2_support

**Instruction:**
Disconnect the M12 connector from the stacklight.

**Expected result:**
The M12 connector is disconnected from the stacklight.

**Screens / Images:**

![artifact_fig_7_22_stacklight](assets/artifact_fig_7_22_stacklight.png)

*Use the stacklight photo as the visual reference for the component from which the M12 connector is to be disconnected.*


**Stop or Escalate If:**

* The connector cannot be disconnected.
* Additional removal actions are required because this source excerpt provides only the first removal step.
* The connector or component cannot be matched confidently to the Figure 7-22 reference.

---

## Success Criteria

* The listed PPE, tool, and replacement part were gathered.
* The stacklight assembly and M12 connector were identified using the provided source-backed figure.
* The M12 connector is disconnected from the stacklight.

## Failure Conditions

* Required items are missing.
* The stacklight assembly or M12 connector cannot be clearly identified from the provided source-backed information.
* The M12 connector cannot be disconnected.
* Additional removal actions are needed but are not provided in this source excerpt.

## Escalation Guidance

* Stop if the M12 connector cannot be clearly identified from the source-backed information.
* Escalate if additional removal actions are required because this source excerpt provides only the first removal step.
* Escalate for SME/manual review if safety isolation, production stop, or LOTO requirements must be confirmed before continuing.

## Missing Details / Known Gaps

* The supplied packet does not provide the full stacklight removal procedure beyond the first explicit removal step.
* The supplied packet does not confirm whether production stop is required.
* The supplied packet does not confirm whether LOTO is required for this task.
* The supplied packet does not provide reinstallation or post-removal verification steps.
* The supplied packet does not provide detailed connector handling technique or torque/use details for the 7-mm wrench.

## Source Lineage

- Candidate IDs: candidate_l2_disconnect_stacklight_m12_connector_for_removal
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
