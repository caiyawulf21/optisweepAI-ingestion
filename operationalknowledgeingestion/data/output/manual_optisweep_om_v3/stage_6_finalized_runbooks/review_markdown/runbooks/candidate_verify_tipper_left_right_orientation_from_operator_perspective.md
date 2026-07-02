# Verify Whether a Tipper Is Left or Right From the Operator Perspective

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_tipper_left_right_orientation_from_operator_perspective_v1` |
| Title | Verify Whether a Tipper Is Left or Right From the Operator Perspective |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | `operator` |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the manual's operator-perspective orientation rule to identify whether a tipper is left or right and confirm that the opposite-side assembly should be interpreted as a mirror image of the documented reference assembly.

## When To Use

Use when identifying a tipper as left or right, comparing a physical tipper to the manual diagram, or interpreting whether opposite-side assemblies should match as mirrored versions from the operator perspective.

## Do Not Use For

* Do not use this runbook for installation, adjustment, repair, or corrective maintenance because the source only provides orientation and mirror-image reference information.
* Do not use this runbook to infer component differences between left and right tippers beyond the source statement that they are identical assemblies mirrored from the operator perspective.

## Safety And Operational Notes

* This source packet supports a visual/reference procedure only and does not provide maintenance, motion, or lockout instructions.
* Escalate if the operator perspective needed to assign left versus right cannot be established from the site setup.
* Escalate if the physical assembly appears inconsistent with the documented mirror-image relationship.

## Access Or Tools Needed

* Physical access or visual access to the tipper location
* Figure 3-4 Tipper Components (Left Tipper Shown)

## Related Operational Context

* ctx_manual_tipper_left_right_orientation_v1
* ctx_manual_tipper_component_inventory_v1

## Procedure Steps

### Step 1 — Establish the operator perspective at the tipper

**Responsible role:** L1_support

**Instruction:**
Go to the tipper location or obtain a clear visual of it and identify the assembly from the perspective of the operator, because the manual states that right and left tippers are based on the operator perspective.

**Expected result:**
The observer has established the operator-facing viewpoint to use for orientation naming.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Use the operator station view to understand the operator-facing side of the equipment.*


**Stop or Escalate If:**

* The operator perspective needed to assign left versus right cannot be established from the site setup.

---

### Step 2 — Assign left or right tipper orientation

**Responsible role:** L1_support

**Instruction:**
Using the operator-perspective naming convention from the manual, determine whether the unit should be referred to as a left tipper or a right tipper.

**Expected result:**
The tipper is identified as left or right using the documented convention.

**Stop or Escalate If:**

* The operator perspective remains unclear after review.

---

### Step 3 — Use Figure 3-4 as the left tipper reference

**Responsible role:** L1_support

**Instruction:**
Use Figure 3-4, labeled 'Tipper Components (Left Tipper Shown),' as the documented reference for component placement when reviewing the assembly.

**Expected result:**
The left tipper reference diagram is selected as the baseline for comparison.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Confirm the figure title 'Tipper Components (Left Tipper Shown)' and use the labeled component layout as the reference arrangement.*


**Stop or Escalate If:**

* The required Figure 3-4 reference is not available for comparison.

---

### Step 4 — Verify the opposite-side assembly as a mirror image

**Responsible role:** L1_support

**Instruction:**
When comparing the opposite-side assembly, verify that it contains the same documented components arranged as a mirror image of the reference assembly rather than as a different design.

**Expected result:**
The opposite-side tipper is interpreted as the same assembly mirrored from the operator perspective.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Compare labeled components and their relative placement to determine whether the opposite side is a mirrored arrangement of the left tipper reference.*


**Stop or Escalate If:**

* The physical assembly appears inconsistent with the documented mirror-image relationship.

---

### Step 5 — Record the orientation finding

**Responsible role:** L1_support

**Instruction:**
Record the tipper orientation and note that left and right tippers are identical assemblies mirrored from the operator perspective.

**Expected result:**
The orientation is documented together with the mirror-image interpretation.

**Stop or Escalate If:**

* The orientation finding cannot be documented clearly due to unresolved viewpoint or comparison issues.

---

## Success Criteria

* The tipper is consistently identified as left or right using the operator perspective.
* Figure 3-4 is used as the documented left tipper reference.
* The opposite-side assembly is interpreted as a mirror image of the documented reference rather than a different design.
* The orientation finding is recorded with the mirror-image note.

## Failure Conditions

* The operator perspective cannot be established from the site setup.
* The physical assembly appears inconsistent with the documented mirror-image relationship.
* The reference figure needed for comparison is unavailable.
* The orientation finding cannot be documented clearly.

## Escalation Guidance

* Escalate if the physical assembly appears inconsistent with the documented mirror-image relationship.
* Escalate if the operator perspective needed to assign left versus right cannot be established from the site setup.

## Missing Details / Known Gaps

* The source does not provide a detailed method for physically determining left versus right beyond stating that naming is based on the operator perspective.
* The source does not define a required documentation system or record format for capturing the orientation result.
* The source does not provide corrective actions if the assembly does not match the documented mirror-image relationship.
* The source section text content was not included in the packet beyond referenced summaries and figure metadata.

## Source Lineage

- Candidate IDs: candidate_verify_tipper_left_right_orientation_from_operator_perspective
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
