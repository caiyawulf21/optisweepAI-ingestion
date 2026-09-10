# Explain/verify area-to-area movement constraints using entrance/exit layout model (Hospital, SorterSide, Charger, Tipper)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_explain_verify_area_to_area_movement_constraints_entrance_exit_v1` |
| Title | Explain/verify area-to-area movement constraints using entrance/exit layout model (Hospital, SorterSide, Charger, Tipper) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the source-backed modular layout rule—each named area has an entrance and an exit—to interpret whether observed AGV/AGB movement between areas (Hospital, SorterSide, Charger, Tipper) follows the expected entrance/exit transition constraint.

## When To Use

When you are troubleshooting or explaining an AGV/AGB’s movement pattern between distinct layout areas and you need to check whether the movement is consistent with the modular entrance/exit constraint for the named areas (Hospital, SorterSide, Charger, Tipper).

## Do Not Use For

* Do not use this procedure as a substitute for system-specific fault isolation when movement cannot be reconciled with the entrance/exit constraint; escalate for deeper investigation.

## Access Or Tools Needed

* Visual access to the layout representation used in the live system or the layout example referenced by the source segment
* Training video segment evidence for the entrance/exit movement rule and named area types

## Related Operational Context

* ctx_training_video_layout_modularity_overview_v1
* ctx_training_video_layout_area_types_v1

## Procedure Steps

### Step 1 — Identify the relevant layout areas named by the source in the example design: Hospital, SorterSide, Charger, and Tipper

**Responsible role:** L1_support

**Instruction:**
From the source’s example layout, note the named area types: Hospital, SorterSide, Charger, and Tipper. Use these as the distinct boundaries for your movement interpretation.

**Expected result:**
You can clearly map the observed movement endpoints to the named areas: Hospital, SorterSide, Charger, and/or Tipper.

---

### Step 2 — Apply the source rule: to move from one area to another, an AGV/AGB must go to the exit before entering the next area

**Responsible role:** L1_support

**Instruction:**
Use the modular layout rule stated by the source: when moving from one area to another, the AGV/AGB must go to the exit before entering the next area.

**Expected result:**
Your interpretation framework is set: every area-to-area transition you evaluate should include an exit step before the next area entrance.

---

### Step 3 — When observing an item’s movement between areas, check whether the movement pattern is consistent with the entrance/exit constraint described by the source

**Responsible role:** L1_support

**Instruction:**
For the observed AGV/AGB movement between the named areas (Hospital, SorterSide, Charger, Tipper), verify that the transition includes the exit-before-entrance behavior implied by the modular layout rule.

**Expected result:**
You can conclude whether the observed movement pattern is consistent with the entrance/exit constraint (exit occurs before the next area entrance).

---

### Step 4 — If movement appears to skip an area boundary, re-check that the observation is between distinct areas that have entrance/exit points in the described modular layout

**Responsible role:** L1_support

**Instruction:**
If the observed movement seems to skip the expected boundary behavior, re-check that the movement you are interpreting is actually between distinct areas (Hospital, SorterSide, Charger, Tipper) that follow the modular entrance/exit model.

**Expected result:**
Either (a) you reconcile the observation with the exit-before-entrance constraint by correctly identifying the distinct areas, or (b) you confirm the movement cannot be reconciled with the constraint.

**Stop or Escalate If:**

* If observed movement cannot be reconciled with the entrance/exit constraint described by the source, escalate for deeper system-specific investigation beyond this layout explanation.

---

## Success Criteria

* You correctly identify the relevant distinct areas (Hospital, SorterSide, Charger, Tipper) for the movement you are analyzing.
* You apply the entrance/exit transition rule to interpret whether observed movement is consistent with exit-before-entrance between distinct areas.
* If movement cannot be reconciled with the rule, you escalate for deeper system-specific investigation.

## Failure Conditions

* Observed movement appears to skip the exit-before-entrance behavior between distinct areas.
* Area classification is ambiguous such that you cannot determine which entrance/exit constraint should apply.

## Escalation Guidance

* If observed movement cannot be reconciled with the entrance/exit constraint described by the source, escalate for deeper system-specific investigation beyond this layout explanation.

## Missing Details / Known Gaps

* The packet does not provide explicit live UI elements or named live screens/fields to observe for area-to-area movement; this runbook is therefore framed as an interpretation aid based on the source’s entrance/exit layout rule.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_layout_entrance_exit_area_movement_model
- Source ID: `training_video_day1`
- Source Type: `training_video`
