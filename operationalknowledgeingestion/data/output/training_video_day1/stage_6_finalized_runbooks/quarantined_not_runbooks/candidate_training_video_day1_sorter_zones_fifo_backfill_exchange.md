# Interpret Sorter Zone Behavior: AGV Pickup/Drop-Off Restricted to Its Zone; Backfill Uses FIFO-like Logic

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_sorter_zone_behavior_agv_pickup_dropoff_fifo_backfill_v1` |
| Title | Interpret Sorter Zone Behavior: AGV Pickup/Drop-Off Restricted to Its Zone; Backfill Uses FIFO-like Logic |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sort_lifecycle_state` |
| Access Surface | None |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the sorter-side zone rules to interpret observed AGV movement during exchange/backfill: an AGV operating in a zone only picks up and drops off within that zone, performs an in-zone exchange check, and backfill behaves FIFO-like with additional considerations such as zone closures.

## When To Use

When you are observing AGV movement and exchange/backfill behavior on the sorter side and need to interpret whether the behavior matches zone-constrained pickup/drop-off and FIFO-like backfill logic.

## Do Not Use For

* Do not use this as a troubleshooting procedure for specific RMS/WCS/SSMS faults or to diagnose system faults; the source does not provide named UI fields/controls or fault codes for zone behavior.

## Access Or Tools Needed

* Visual/operational observation of AGV movement relative to zone boundaries
* Sorter zone layout reference (if available on-site)

## Related Operational Context

* ctx_training_video_sorter_zones_v1

## Procedure Steps

### Step 1 — Identify the concept of “zones” on the sorter side (zone-based operating areas).

**Responsible role:** operator

**Instruction:**
Using the sorter zone layout reference (if available on-site), identify the zone boundary for the AGV you are observing.

**Expected result:**
You can map the observed AGV’s activity to a specific sorter zone (i.e., you know which zone it is operating within).

---

### Step 2 — Confirm the zone constraint: an AGV in a zone only picks up and drops off in its zone.

**Responsible role:** operator

**Instruction:**
Observe the AGV’s pickup and drop-off actions and check that both occur within the same zone it is operating in.

**Expected result:**
Your interpretation matches the rule: the AGV only picks up and drops off within its zone.

**Stop or Escalate If:**

* If AGVs appear to pick up/drop off outside their zone, escalate for support rather than assuming normal behavior.

---

### Step 3 — Observe the in-zone exchange/backfill behavior: come into its zone, check if anything needs to be exchanged, then move on.

**Responsible role:** operator

**Instruction:**
Watch the AGV as it enters its zone: interpret its behavior as coming into the zone, checking whether anything needs to be exchanged, and then moving on.

**Expected result:**
You can describe the observed behavior as an in-zone exchange check followed by movement onward.

**Stop or Escalate If:**

* If exchange checks do not occur as described, escalate for support rather than assuming normal behavior.

---

### Step 4 — Interpret backfill ordering as FIFO-like with additional considerations (e.g., zone closures).

**Responsible role:** operator

**Instruction:**
When interpreting which AGV/tote actions occur first during backfill, treat the ordering as FIFO-like, and account for additional considerations such as whether a zone is closed.

**Expected result:**
Your interpretation matches FIFO-like backfill behavior rather than priority/time-based exchange behavior.

---

## Success Criteria

* You can explain observed AGV movement as zone-constrained pickup/drop-off with an in-zone exchange check.
* You can interpret backfill ordering as FIFO-like (not priority/time-based) with possible effects from zone closures.

## Failure Conditions

* AGVs appear to pick up/drop off outside their zone.
* Exchange checks do not occur as described.
* Backfill ordering appears inconsistent with FIFO-like logic without an explanation tied to zone closure considerations.

## Escalation Guidance

* If AGVs appear to pick up/drop off outside their zone or exchange checks do not occur as described, escalate for support rather than assuming normal behavior.

## Missing Details / Known Gaps

* The source does not provide explicit RMS/WCS/SSMS UI fields or named controls to verify zone membership or exchange-check status; this runbook remains an interpretation aid based on observed behavior.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_sorter_zones_fifo_backfill_exchange
- Source ID: `training_video_day1`
- Source Type: `training_video`
