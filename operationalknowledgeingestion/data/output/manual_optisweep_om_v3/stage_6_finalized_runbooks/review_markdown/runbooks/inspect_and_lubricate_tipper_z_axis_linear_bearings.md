# Inspect and lubricate tipper Z-axis linear bearings

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_inspect_and_lubricate_tipper_z_axis_linear_bearings_v1` |
| Title | Inspect and lubricate tipper Z-axis linear bearings |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Visually inspect both tipper Z-axis linear rails for grease condition and, if the rails are dry, lubricate the bearing blocks using automotive bearing grease through the bearing block grease nipples. The source specifies two bearing blocks, one standard 1/4-in. grease nipple on each end of each block, and 1.0 to 3.0 cc of grease per block.

## When To Use

Use for preventive maintenance inspection of the tipper Z-axis linear rails and bearing blocks when checking grease condition and lubricating the bearing blocks if the rails are dry.

## Do Not Use For

* Do not use wiping grease on the rails as a substitute for lubricating the bearing blocks.

## Access Or Tools Needed

* Automotive bearing grease (e.g., Mobil1™)
* Means to apply 1.0 to 3.0 cc of grease to each bearing block
* Access to both Z-axis linear rails and bearing block grease nipples

## Related Operational Context

* ctx_manual_z_axis_linear_bearings_reference_v1

## Procedure Steps

### Step 1 — Inspect both Z-axis linear rails for grease condition

**Responsible role:** L2_support

**Instruction:**
Visually inspect both Z-axis linear rails for wetness of grease and/or signs of dried grease.

**Expected result:**
The grease condition of both Z-axis linear rails is identified.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Use the tipper component diagram as a general location reference for the tipper assembly while identifying the Z-axis area to inspect.*


**Stop or Escalate If:**

* The source does not provide escalation criteria beyond the lubrication instruction.

---

### Step 2 — Lubricate bearing blocks if rails are dry

**Responsible role:** L2_support

**Instruction:**
If the rails are dry, lubricate the bearing blocks using automotive bearing grease.

**Expected result:**
Bearing blocks are lubricated when dry rail condition is observed.

**Stop or Escalate If:**

* Required grease or means to apply grease is not available.

---

### Step 3 — Apply grease at all bearing block nipples

**Responsible role:** L2_support

**Instruction:**
Apply grease at the bearing block nipples. There are two bearing blocks, with one standard 1/4-in. nipple on each end of each block, for a total of four nipples.

**Expected result:**
All specified grease nipples on both bearing blocks are identified and used as the lubrication points.

**Stop or Escalate If:**

* Bearing block grease nipples cannot be accessed.

---

### Step 4 — Add specified grease quantity to each block

**Responsible role:** L2_support

**Instruction:**
Add 1.0 to 3.0 cc of grease to each block.

**Expected result:**
Each bearing block receives 1.0 to 3.0 cc of grease.

**Stop or Escalate If:**

* No means is available to apply the specified grease quantity.

---

### Step 5 — Do not substitute rail wiping for lubrication

**Responsible role:** L2_support

**Instruction:**
Do not treat wiping grease on the rails as adequate lubrication.

**Expected result:**
Lubrication is performed through the bearing blocks rather than by wiping grease onto the rails.

**Stop or Escalate If:**

* The intended lubrication method is only wiping grease on the rails.

---

## Success Criteria

* Both Z-axis linear rails have been visually inspected for wetness of grease and/or signs of dried grease.
* If the rails were dry, the bearing blocks were lubricated using automotive bearing grease.
* Grease was applied through the bearing block nipples.
* Each bearing block received 1.0 to 3.0 cc of grease.
* Lubrication was not performed by only wiping grease on the rails.

## Failure Conditions

* Rails are dry and bearing blocks are not lubricated.
* Grease is not applied through the bearing block nipples.
* Specified grease quantity is not applied to each block.
* Grease is only wiped on the rails.

## Escalation Guidance

* The source does not provide explicit escalation guidance beyond performing lubrication when the rails are dry and noting that wiping grease on the rails is not adequate.

## Missing Details / Known Gaps

* The source packet does not provide explicit production stop requirements.
* The source packet does not provide explicit LOTO requirements for this task.
* The source packet does not provide explicit PPE requirements for this task.
* The source packet does not provide explicit escalation triggers beyond the lubrication note.
* The source packet does not include a directly matched image of the Z-axis linear bearing grease nipples or rails on page 98.

## Source Lineage

- Candidate IDs: inspect_and_lubricate_tipper_z_axis_linear_bearings
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
