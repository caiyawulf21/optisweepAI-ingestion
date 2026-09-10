# Perform/Understand Bag Out End-of-Sort Clearing: Close Shoots → Bag Out Back-to-Front → Exchange/Mark Items

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_perform_understand_bag_out_end_of_sort_clearing_v1` |
| Title | Perform/Understand Bag Out End-of-Sort Clearing: Close Shoots → Bag Out Back-to-Front → Exchange/Mark Items |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sort_lifecycle_state`, `bag_out_or_closeout_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `operator` |
| Failure Pattern Tags | `sort_lifecycle_stuck`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the end-of-sort “bag out” procedure to empty the sorter system before the next sort configuration: close every shoot, start bag out for all locations, exchange or mark any tote that has an item for exchange, then run the bag-out order back-to-front until everything is out of the system and ready for another sort.

## When To Use

Use at the end of a sort when you are done with sorting and need to clear remaining items from the sorter system so the next sort can start with a new load plan/destination.

## Do Not Use For

* Do not continue to the next sort configuration if bag out does not clear all locations or items remain in the system after completion.

## Access Or Tools Needed

* Operational access to the sorter end-of-sort/bag-out process (as described in the provided training video segment).

## Related Operational Context

* ctx_training_video_bag_out_cycle_v1

## Procedure Steps

### Step 1 — Confirm you are at the end of a sort

**Responsible role:** operator

**Instruction:**
Confirm you are done with the current sort (the point where you would transition to end-of-sort clearing).

**Expected result:**
You have reached the end-of-sort point where bag out is required to clear remaining items before the next sort.

---

### Step 2 — Close every shoot (including shoots that may be empty)

**Responsible role:** operator

**Instruction:**
Close every shoot as part of the bag out preparation, including shoots that may be empty.

**Expected result:**
All shoots are closed for the bag out cycle.

---

### Step 3 — Start bag out for all locations

**Responsible role:** operator

**Instruction:**
Start bag out for all locations (bag out all locations).

**Expected result:**
Bag out is initiated for all locations as part of the end-of-sort clearing cycle.

---

### Step 4 — Exchange or mark for exchange any tote with an item (one parcel)

**Responsible role:** operator

**Instruction:**
During bag out, ensure any tote that has an item (one parcel) is exchanged or marked for an exchange.

**Expected result:**
Totes with items are either exchanged or explicitly marked for exchange as part of bag out.

---

### Step 5 — Run bag out order back-to-front

**Responsible role:** operator

**Instruction:**
Ensure the bag out sequence proceeds from back to front.

**Expected result:**
Bag out proceeds in the back-to-front order as described for the end-of-sort clearing cycle.

---

### Step 6 — Observe AGV movement pattern during bag out (farthest area of zone, then every other)

**Responsible role:** operator

**Instruction:**
During bag out, observe that AGVs go to the farthest area of their zone first, then it goes every other.

**Expected result:**
AGVs follow the described movement pattern: farthest area of their zone, then every other.

---

### Step 7 — Confirm end-of-cycle completion: everything out of the system and ready for another sort

**Responsible role:** operator

**Instruction:**
After bag out completes, confirm the documented result: everything is out of the system and the system is ready to start another sort.

**Expected result:**
Everything is out of the system and the system is ready to start another sort.

**Stop or Escalate If:**

* If bag out does not clear all locations or items remain in the system after completion, stop and escalate rather than continuing with the next sort configuration.

---

## Success Criteria

* All shoots are closed for the bag out cycle.
* Bag out is started for all locations.
* Any tote with an item is exchanged or marked for an exchange during bag out.
* Bag out proceeds back-to-front with the described AGV movement pattern (farthest area of zone, then every other).
* After completion, everything is out of the system and the system is ready to start another sort.

## Failure Conditions

* Any shoot remains open during bag out.
* A tote with an item remains unexchanged/unmarked for exchange.
* Bag out does not clear all locations (items remain in the system after completion).
* System is not ready for the next sort after bag out completion.

## Escalation Guidance

* If bag out does not clear all locations or items remain in the system after completion, stop and escalate rather than continuing with the next sort configuration.

## Missing Details / Known Gaps

* The source describes the bag out behavior and ordering but does not name specific live UI controls/buttons or exact operator clicks to start/close shoots and initiate bag out.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_bag_out_end_of_sort_clear_locations
- Source ID: `training_video_day1`
- Source Type: `training_video`
