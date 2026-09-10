# Confirm Pre Bag Out scope: exchange the lowest 25% of destinations per sorter leg

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_confirm_pre_bag_out_scope_lowest_25_percent_per_leg_v1` |
| Title | Confirm Pre Bag Out scope: exchange the lowest 25% of destinations per sorter leg |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `bag_out_or_closeout_state` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the UPSFORTNA OptiSweep bag out control UI to confirm that “Pre bag out” is configured to exchange the lowest 25% of destinations per sorter leg (not all destinations).

## When To Use

Use when you are running bag out and need to ensure the “Pre bag out” exchange scope is limited to the lowest 25% of destinations per sorter leg.

## Access Or Tools Needed

* Access to the bag out control UI that includes “pre bag out”
* UI/status visibility for destination subset and sorter leg scope

## Related Operational Context

* ctx_training_video_pre_bag_out_exchange_scope_v1

## Procedure Steps

### Step 1 — Locate the “pre bag out” option in the bag out control area

**Responsible role:** operator

**Instruction:**
In the Overall System Bag Out Control UI, locate the “Pre bag out” option within the bag out control area.

**Expected result:**
The “Pre bag out” option is visible in the bag out control UI.

**Stop or Escalate If:**

* Stop and escalate if the UI does not support a “pre bag out” option.

---

### Step 2 — Select “pre bag out” and confirm the scope is lowest 25% per sorter leg

**Responsible role:** operator

**Instruction:**
Select “Pre bag out” in the Overall System Bag Out Control UI and confirm the scope corresponds to “the lowest 25% of destinations per leg of the sorter.”

**Expected result:**
The selected bag out mode indicates “Pre bag out” with the lowest 25% per leg scope.

**Stop or Escalate If:**

* Stop and escalate if the UI does not reflect the “lowest 25% per leg” scope described by the source.

---

### Step 3 — Verify sorter leg selection (if applicable) so the lowest 25% rule applies per selected leg(s)

**Responsible role:** operator

**Instruction:**
If the bag out control UI allows selecting a sorter leg, verify the leg selection so the “lowest 25% of destinations per leg of the sorter” rule applies to the selected leg(s).

**Expected result:**
The sorter leg selection (if present) is set such that the lowest-25% rule applies per the selected leg(s).

**Stop or Escalate If:**

* Stop and escalate if the exchange tasks appear to include destinations outside the lowest 25% subset per leg.

---

### Step 4 — Observe exchange tasks correspond to the lowest 25% destination subset per leg

**Responsible role:** operator

**Instruction:**
After selecting “Pre bag out,” observe the exchange tasks (or the UI status that lists included destinations) and confirm they correspond only to the lowest 25% destination subset per sorter leg.

**Expected result:**
The exchange tasks/destination list includes only destinations within the lowest 25% subset per leg.

**Stop or Escalate If:**

* Stop and escalate if the exchange tasks appear to include destinations outside the lowest 25% subset per leg.

---

## Success Criteria

* “Pre bag out” is selected in the Overall System Bag Out Control UI.
* The UI reflects that pre bag out exchanges the lowest 25% of destinations per sorter leg.
* The resulting exchange tasks/destination subset correspond only to that lowest-25% per-leg scope.

## Failure Conditions

* No “Pre bag out” option exists in the bag out control UI.
* UI does not reflect the lowest 25% per leg scope.
* Exchange tasks include destinations outside the lowest 25% subset per leg.

## Escalation Guidance

* If the UI does not support “pre bag out,” or if the UI/scope does not match “lowest 25% per leg,” stop the operation and escalate.

## Missing Details / Known Gaps

* The packet does not include a live UI screenshot showing the exact control/field where the “lowest 25% per leg” subset is displayed or how to verify the included destination subset beyond the textual rule shown in the artifact.
* The packet does not provide explicit UI labels/controls for selecting sorter leg(s) within the bag out control UI.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_pre_bag_out_lowest_25_percent_per_leg
- Source ID: `training_video_day1`
- Source Type: `training_video`
