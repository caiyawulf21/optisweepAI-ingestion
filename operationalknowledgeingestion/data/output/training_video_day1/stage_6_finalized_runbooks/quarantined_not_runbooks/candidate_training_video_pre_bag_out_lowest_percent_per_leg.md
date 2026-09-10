# Run pre bag out to exchange the lowest 25% of destinations per sorter leg

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_run_pre_bag_out_lowest_25_percent_per_leg_v1` |
| Title | Run pre bag out to exchange the lowest 25% of destinations per sorter leg |
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

Use the bag out control system to run “pre bag out,” which exchanges the lowest 25% of destinations per sorter leg.

## When To Use

When you need to perform the pre bag out behavior that exchanges the lowest 25% of destinations per sorter leg.

## Access Or Tools Needed

* Bag out control system UI/control (pre bag out option)

## Related Operational Context

* ctx_training_video_pre_bag_out_exchange_threshold_v1

## Procedure Steps

### Step 1 — Open the bag out control system and locate the “pre bag out” option

**Responsible role:** operator

**Instruction:**
Open the bag out control system and locate the “pre bag out” option.

**Expected result:**
The “pre bag out” option is visible/available in the bag out control system UI.

---

### Step 2 — Select “pre bag out”

**Responsible role:** operator

**Instruction:**
In the bag out control system, select the “pre bag out” option.

**Expected result:**
Pre bag out is selected as the bag out behavior to run.

---

### Step 3 — Verify pre bag out behavior: lowest 25% of destinations per sorter leg

**Responsible role:** operator

**Instruction:**
Confirm that the pre bag out behavior exchanges the lowest 25% of destinations per sorter leg.

**Expected result:**
For each sorter leg, the exchanged destinations correspond to the lowest 25% threshold per leg.

**Stop or Escalate If:**

* Stop and escalate if the exchanged destinations do not align with the source-described “lowest 25% per leg” behavior.

---

### Step 4 — If leg selection is required, apply pre bag out per sorter leg

**Responsible role:** operator

**Instruction:**
If the system requires leg selection, ensure the pre bag out action is applied per sorter leg consistent with the “lowest 25% of destinations per leg” description.

**Expected result:**
Pre bag out is applied per sorter leg (not globally), so each leg exchanges its own lowest 25% of destinations.

**Stop or Escalate If:**

* Stop and escalate if the exchanged destinations do not align with the source-described “lowest 25% per leg” behavior.

---

## Success Criteria

* Pre bag out exchanges the lowest 25% of destinations per sorter leg.

## Failure Conditions

* Exchanged destinations do not align with the “lowest 25% per leg” behavior.

## Escalation Guidance

* Stop and escalate if the exchanged destinations do not align with the source-described “lowest 25% per leg” behavior.

## Missing Details / Known Gaps

* The source does not specify which exact UI field(s) or status indicator(s) confirm that the lowest 25% threshold has been applied per leg (only the definition is provided).

## Source Lineage

- Candidate IDs: candidate_training_video_pre_bag_out_lowest_percent_per_leg
- Source ID: `training_video_day1`
- Source Type: `training_video`
