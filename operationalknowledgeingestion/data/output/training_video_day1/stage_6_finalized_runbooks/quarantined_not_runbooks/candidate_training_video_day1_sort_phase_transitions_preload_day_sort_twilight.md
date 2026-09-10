# Understand Sort Phase Transitions: Preload → Day Sort → Twilight (and Why They Must Cycle)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_understand_sort_phase_transitions_preload_day_sort_twilight_v1` |
| Title | Understand Sort Phase Transitions: Preload → Day Sort → Twilight (and Why They Must Cycle) |
| Procedure Type | `diagnostic` |
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

Use the documented rationale for sorter sort-phase transitions (preload, day sort, twilight) to interpret why the system cycles between phases and why it cannot run one sort phase continuously into the next without clearing/pushing out volume.

## When To Use

When you need to interpret observed sorter behavior that appears to be transitioning between sort phases (preload → day sort → twilight), especially when volume/destination characteristics change and you want to understand why the system must cycle rather than run one phase into another.

## Access Or Tools Needed

* Operational awareness of sorter sort phases (preload/day sort/twilight) as described in the provided training video segment.

## Related Operational Context

* ctx_training_video_sort_transitions_v1

## Procedure Steps

### Step 1 — Identify the current sort phase conceptually (preload, day sort, twilight)

**Responsible role:** operator

**Instruction:**
From the documented set of sort phases, determine whether the system is in the conceptual phase of preload, day sort, or twilight.

**Expected result:**
You can name the active conceptual phase as one of: preload, day sort, or twilight.

---

### Step 2 — Confirm the operational requirement that sort phases must be cycled (not run into each other)

**Responsible role:** operator

**Instruction:**
Use the documented requirement that preload/day sort/twilight must be cycled in and cannot run into each other.

**Expected result:**
You can state that the system cycles between sort phases and does not run one phase continuously into the next without clearing.

---

### Step 3 — Interpret transitions using the documented reason: different volume/destinations require pushing out volume before the phase ends

**Responsible role:** operator

**Instruction:**
Use the documented rationale: during each sort phase you expect to receive different volume destined for different locations, and the operational goal is to push out that volume before the sort ends—therefore the next phase requires cycling rather than continuous operation.

**Expected result:**
You can justify an observed transition by explaining that the incoming volume/destination characteristics change by phase, so the system must push out the current phase’s volume before moving on.

---

### Step 4 — Check that transitions can still occur during peak season

**Responsible role:** operator

**Instruction:**
If you observe transitions even during peak season, confirm the documented expectation that peak season still includes transitions between sort phases.

**Expected result:**
You can explain that even in peak season, transitions between preload/day sort/twilight still occur.

---

## Success Criteria

* Operator can identify the active conceptual sort phase as preload, day sort, or twilight.
* Operator can justify observed transitions using the documented rationale: different volume/destinations by phase require cycling and pushing out volume before the phase ends.
* Operator can explain that transitions can still occur during peak season.

## Failure Conditions

* Operator assumes phases can run into each other without cycling/clearing.
* Operator misclassifies peak-season transitions as abnormal solely due to timing/season.

## Escalation Guidance

* If transitions occur in a way that contradicts the documented need to clear/push out volume before sort end, escalate for support rather than assuming normal behavior.

## Missing Details / Known Gaps

* The packet does not provide a named live sorter control/screen or a specific live UI control surface that shows the current sort phase (preload/day sort/twilight). The runbook therefore focuses on conceptual interpretation rather than step-by-step UI verification.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_sort_phase_transitions_preload_day_sort_twilight
- Source ID: `training_video_day1`
- Source Type: `training_video`
