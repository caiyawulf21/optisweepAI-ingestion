# Follow the source-described AGV under-rack lift sequence during a tote exchange

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_follow_the_source_described_agv_under_rack_lift_sequence_during_a_tote_exchange_v1` |
| Title | Follow the source-described AGV under-rack lift sequence during a tote exchange |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tote_exchange_sequence` |
| Access Surface | `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify the tote-exchange physical sequence described by the source: an AGV with no tote designated to the tote zone moves under the racking to position for a lift; the tote is lifted in position; then an AGV with an empty tote travels under the sorter behind it; the full-tote AGV moves out into the aisle while the empty-tote AGV moves into the rack location and lowers its empty tote into the rack; finally, the AGV that just dropped its tote becomes the AGV that will pick up the next tote.

## When To Use

Use when you are observing/confirming a tote exchange and need to check that the AGV under-rack positioning, lift, and the subsequent full/empty AGV movements occur in the source-described order.

## Access Or Tools Needed

* Live system visibility of AGV movements under racking and at the sorter/rack locations

## Related Operational Context

* ctx_training_video_agv_zone_and_lift_positioning_v1
* ctx_training_video_post_exchange_agv_role_transition_v1

## Procedure Steps

### Step 1 — Identify the AGV described as having no tote and designated to the tote zone

**Responsible role:** operator

**Instruction:**
During the tote exchange, identify the AGV that the source describes as having no tote and being designated to the tote zone.

**Expected result:**
You can point to the AGV that is the “AGV with no tote” for the tote zone exchange sequence.

**Stop or Escalate If:**

* If you cannot confidently identify the “no tote” AGV for the tote zone, stop and request support/clarification.

---

### Step 2 — Observe the no-tote AGV move under the racking to position for a lift

**Responsible role:** operator

**Instruction:**
Watch the identified no-tote AGV move under the racking to position for a lift.

**Expected result:**
The no-tote AGV moves under the racking and reaches the position for the lift.

**Stop or Escalate If:**

* If the observed sequence does not match the source-described order (e.g., lift does not occur after under-rack positioning), stop and request support/clarification.

---

### Step 3 — Observe the tote being lifted in position

**Responsible role:** operator

**Instruction:**
Observe the tote lift in position as described by the source (the source describes an AGV running under the racks of the totes and lifting up a tote).

**Expected result:**
A tote is lifted in position by the AGV that is under the racks.

**Stop or Escalate If:**

* If the observed sequence does not match the source-described order (e.g., lift does not occur after under-rack positioning), stop and request support/clarification.

---

### Step 4 — Observe the empty-tote AGV traveling under the sorter behind the lift sequence

**Responsible role:** operator

**Instruction:**
Observe that an AGV with an empty tote travels under the sorter position itself behind the sequence.

**Expected result:**
An empty-tote AGV travels under the sorter behind the lift sequence.

**Stop or Escalate If:**

* If the observed sequence does not match the source-described order, stop and request support/clarification.

---

### Step 5 — Observe exchange outcome: full tote AGV out to aisle; empty tote AGV into rack location and lowered

**Responsible role:** operator

**Instruction:**
Observe that (1) the AGV with the full tote moves out into the aisle, and (2) the AGV with the empty tote moves into the rack location and lowers its empty tote into the rack.

**Expected result:**
Full tote AGV moves out into the aisle; empty tote AGV moves into the rack location and lowers its empty tote into the rack.

**Stop or Escalate If:**

* If the observed sequence does not match the source-described order (e.g., lift does not occur after under-rack positioning), stop and request support/clarification.

---

### Step 6 — Confirm the post-exchange role transition: dropped-tote AGV becomes next picker

**Responsible role:** operator

**Instruction:**
After the empty tote is lowered into the rack, confirm that the AGV that just dropped its tote becomes the AGV that will pick up the next tote.

**Expected result:**
The AGV that just dropped its tote is the one that will pick up the next tote in the zone.

**Stop or Escalate If:**

* If the observed sequence does not match the source-described order, stop and request support/clarification.

---

## Success Criteria

* You can describe the exchange sequence as: under-rack positioning for lift → tote lifted → empty-under-sorter behind → full out to aisle / empty into rack and lowered → dropped-tote AGV becomes next picker.

## Failure Conditions

* Observed sequence does not match the source-described order (e.g., lift does not occur after under-rack positioning).
* Full/empty outcome movements do not match the source-described directions (full not out to aisle; empty not into rack location and lowered).
* Post-exchange role transition does not occur as described (dropped-tote AGV does not become next picker).

## Escalation Guidance

* If the observed sequence does not match the source-described order, stop and request support/clarification.

## Missing Details / Known Gaps

* The packet does not provide named RMS/SSMS UI controls or specific observable UI fields/labels for identifying the “AGV with no tote” or confirming the lift/empty/full states; this runbook therefore relies on live physical observation of AGV movements under the racking and under the sorter/rack locations.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_tote_exchange_agv_under_racking_lift_sequence
- Source ID: `training_video_day1`
- Source Type: `training_video`
