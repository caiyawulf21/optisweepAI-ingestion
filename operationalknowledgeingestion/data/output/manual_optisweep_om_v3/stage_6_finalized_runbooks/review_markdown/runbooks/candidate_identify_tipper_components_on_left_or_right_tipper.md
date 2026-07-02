# Identify Tipper Components on a Left or Right Tipper

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_tipper_components_on_a_left_or_right_tipper_v1` |
| Title | Identify Tipper Components on a Left or Right Tipper |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use Figure 3-4 and Table 3-3 from the OptiSweep Operation and Maintenance Manual to identify major tipper components on a left tipper and apply the same component naming to a right tipper, which the source states is a mirror-image assembly from the operator perspective.

## When To Use

Use when a technician or support user needs to identify named tipper components on the assembly, confirm left-versus-right tipper orientation from the operator perspective, or communicate component locations using the source-provided names from Figure 3-4 and Table 3-3.

## Do Not Use For

* Do not use for maintenance, adjustment, removal, replacement, or commissioning steps because this source packet only supports component identification and orientation reference.
* Do not use to assign component names not listed in the source-provided figure and table.

## Safety And Operational Notes

* This runbook is limited to identification and reference activity only; the packet does not provide source-supported maintenance or adjustment actions.
* Do not infer removal, motion, or service actions from the component diagram alone.

## Access Or Tools Needed

* Access to the tipper assembly
* Figure 3-4 Tipper Components (Left Tipper Shown)
* Table 3-3 Tipper Components

## Related Operational Context

* ctx_manual_tipper_left_right_orientation_v1
* ctx_manual_tipper_component_inventory_v1
* ctx_manual_tipper_motion_axes_reference_v1

## Procedure Steps

### Step 1 — Determine left or right tipper orientation

**Responsible role:** L1_support

**Instruction:**
Determine whether the unit being checked is a left tipper or right tipper using the operator perspective described in the source.

**Expected result:**
The assembly is classified as either left tipper or right tipper from the operator perspective.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Use the left tipper reference view while applying the source note that left and right are defined from the operator perspective.*


**Stop or Escalate If:**

* Escalate if the observed assembly does not match the documented mirror-image expectation for left versus right tippers.

---

### Step 2 — Use the left tipper figure as the identification reference

**Responsible role:** L1_support

**Instruction:**
Use Figure 3-4, which shows a left tipper, as the component identification reference.

**Expected result:**
The user is working from the correct labeled source figure for component identification.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Labeled Figure 3-4 showing the left tipper and numbered component callouts.*


**Stop or Escalate If:**

* Escalate if a required component cannot be confidently matched to the figure callout and table entry.

---

### Step 3 — Match figure callouts to the component table

**Responsible role:** L1_support

**Instruction:**
Match the numbered callouts in the figure to Table 3-3 to identify the documented components: upper hard stops, Z-axis motor, Z-axis cable carrier, A-axis motor, lower hard stops, CLINK controller cover, column, sub-plate, counterbalances, counterbalance carriage, timing belt, A-axis cable carrier, air valve connection junction box, and gripper.

**Expected result:**
The selected callout is matched to a source-supported component name from Table 3-3.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Maintenance diagram identifying the major components of a left-side OptiSweep tipper assembly and its numbered callouts.*


**Stop or Escalate If:**

* Escalate if a required component cannot be confidently matched to the figure callout and table entry.

---

### Step 4 — Apply mirror-image mapping for a right tipper

**Responsible role:** L1_support

**Instruction:**
If checking a right tipper, apply the source note that the assemblies are mirror images of each other and verify the same component names on the mirrored assembly orientation.

**Expected result:**
The same documented component names are identified on the right tipper using mirrored orientation relative to the left tipper figure.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Use the left tipper component layout as the baseline and verify the right tipper as a mirrored assembly.*


**Stop or Escalate If:**

* Escalate if the observed assembly does not match the documented mirror-image expectation for left versus right tippers.
* Escalate if a required component cannot be confidently matched to the figure callout and table entry.

---

### Step 5 — Record the identified component and location

**Responsible role:** L1_support

**Instruction:**
Record the component name and observed location for the part being identified, using only the source-provided component names.

**Expected result:**
The identified part is documented with a source-supported name and observed location.

**Stop or Escalate If:**

* Escalate if a required component cannot be confidently matched to the figure callout and table entry.

---

## Success Criteria

* The user correctly identifies the documented tipper components on a left tipper using Figure 3-4 and Table 3-3.
* The user applies the same component mapping to a right tipper as a mirror-image assembly from the operator perspective.
* Recorded component names use only source-provided terminology.

## Failure Conditions

* The observed assembly does not match the documented mirror-image expectation for left versus right tippers.
* A required component cannot be confidently matched to the figure callout and table entry.
* The user must rely on names or interpretations not supported by the source.

## Escalation Guidance

* Escalate if the observed assembly does not match the documented mirror-image expectation for left versus right tippers.
* Escalate if a required component cannot be confidently matched to the figure callout and table entry.

## Missing Details / Known Gaps

* The packet does not provide the full Table 3-3 callout numbering, so this runbook identifies components by source-provided names rather than explicit callout-number mappings.
* The packet does not provide a source-supported estimate for completion time.
* The packet does not provide source-supported requirements for production stop or LOTO for this identification-only activity.
* The packet does not provide a source-supported recording format or destination for documenting identified component locations.

## Source Lineage

- Candidate IDs: candidate_identify_tipper_components_on_left_or_right_tipper
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
