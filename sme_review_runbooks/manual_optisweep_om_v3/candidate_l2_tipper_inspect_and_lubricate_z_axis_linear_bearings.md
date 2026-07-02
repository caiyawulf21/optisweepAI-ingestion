# Inspect And Lubricate Tipper Z-Axis Linear Bearings

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_inspect_and_lubricate_tipper_z_axis_linear_bearings_v1` |
| Title | Inspect And Lubricate Tipper Z-Axis Linear Bearings |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Preventive maintenance procedure to inspect both tipper Z-axis linear rails for grease condition and lubricate the bearing blocks when the rails are dry.

## When To Use

Use this procedure during tipper preventive maintenance when checking Z-axis linear rail grease condition and when the rails are dry (not wet with grease).

## Do Not Use For

* Do not use wiping grease on the rails as a substitute for bearing block lubrication.

## Safety And Operational Notes

* This procedure is not marked operator-safe in the source candidate and was assigned to L2_support because it involves maintenance access and component lubrication.
* Use a higher-safe role because this is preventive maintenance involving component lubrication and source text does not define operator-safe access conditions.

## Access Or Tools Needed

* Visual access to both Z-axis linear rails
* Access to the two bearing blocks and four grease nipples
* Automotive bearing grease such as Mobil1™
* Means to apply 1.0 to 3.0 cc of grease to each bearing block

## Related Operational Context

* ctx_manual_tipper_z_axis_linear_bearings_reference_v1
* ctx_manual_tipper_z_axis_grease_spec_reference_v1

## Procedure Steps

### Step 1 — Inspect both Z-axis linear rails for grease condition

**Responsible role:** L2_support

**Instruction:**
Visually inspect both Z-axis linear rails for wetness of grease and for signs of dried grease.

**Expected result:**
The grease condition of both Z-axis linear rails is identified.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Use the tipper components diagram to orient to the tipper assembly and Z-axis area before inspecting both linear rails.*


**Stop or Escalate If:**

* Access conditions needed to inspect the rails are not available or are not defined by the source.

---

### Step 2 — Determine whether the rails are dry

**Responsible role:** L2_support

**Instruction:**
Determine whether the rails are dry, meaning they are not wet with grease.

**Expected result:**
A clear decision is made on whether bearing block lubrication is required.

**Stop or Escalate If:**

* The grease condition cannot be confidently determined from visual inspection.

---

### Step 3 — Lubricate the bearing blocks if the rails are dry

**Responsible role:** L2_support

**Instruction:**
If the rails are dry, lubricate the bearing blocks using automotive bearing grease such as Mobil1™.

**Expected result:**
Bearing block lubrication is performed using the specified grease type when dry rails are found.

**Stop or Escalate If:**

* Required grease or application means is not available.

---

### Step 4 — Locate and grease all four grease nipples on the two bearing blocks

**Responsible role:** L2_support

**Instruction:**
Locate the two bearing blocks and grease the standard 1/4-in. nipple on each end of each block, for a total of four nipples.

**Expected result:**
All four documented grease nipples are identified and greased.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Use the tipper components diagram to orient to the tipper assembly while locating the bearing block area for lubrication points.*


**Stop or Escalate If:**

* The bearing blocks or grease nipples cannot be located from available source-backed references.

---

### Step 5 — Apply 1.0 to 3.0 cc of grease to each bearing block

**Responsible role:** L2_support

**Instruction:**
Add 1.0 to 3.0 cc of grease to each bearing block.

**Expected result:**
Each bearing block receives the documented grease quantity.

**Stop or Escalate If:**

* The grease quantity cannot be measured or applied as specified by the source.

---

### Step 6 — Do not use grease wiped on the rails as the lubrication method

**Responsible role:** L2_support

**Instruction:**
Do not treat wiping grease on the rails as adequate lubrication.

**Expected result:**
Lubrication is performed through the bearing blocks rather than by wiping grease on the rails.

**Stop or Escalate If:**

* The only available lubrication approach is wiping grease on the rails.

---

## Success Criteria

* Both Z-axis linear rails have been inspected for grease condition.
* If the rails were dry, both bearing blocks were lubricated using automotive bearing grease such as Mobil1™.
* All four standard 1/4-in. grease nipples were greased.
* Each bearing block received 1.0 to 3.0 cc of grease.
* Lubrication was not performed by merely wiping grease on the rails.

## Failure Conditions

* Rails are dry and bearing blocks are not lubricated.
* Any of the four grease nipples is not greased.
* Grease quantity per bearing block is not within the documented 1.0 to 3.0 cc range.
* Grease is wiped on the rails instead of lubricating the bearing blocks.
* Required access, grease, or application means is unavailable.

## Escalation Guidance

* Escalate to appropriate maintenance support if safe access conditions for inspection or lubrication are not defined or available.
* Escalate if the bearing blocks or grease nipples cannot be located using the available source-backed references.
* Escalate if the required grease type or a means to apply 1.0 to 3.0 cc per block is unavailable.

## Missing Details / Known Gaps

* The source packet does not provide a source-backed image specifically identifying both Z-axis linear rails and grease condition.
* The source packet does not provide a source-backed image specifically showing the bearing blocks and grease nipple locations.
* The source does not state whether production stop is required.
* The source does not state whether LOTO is required for this preventive maintenance task.
* The source does not provide an estimated completion time.
* The source section text body is empty in the packet, so step wording is grounded from candidate and source reference excerpts only.

## Source Lineage

- Candidate IDs: candidate_l2_tipper_inspect_and_lubricate_z_axis_linear_bearings
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
