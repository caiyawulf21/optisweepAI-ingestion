# Use chute-closure fullness behavior and exchange timing targets to interpret exchange performance issues

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_chute_closure_fullness_and_exchange_timing_targets_v1` |
| Title | Use chute-closure fullness behavior and exchange timing targets to interpret exchange performance issues |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sort_lifecycle_state`, `tipper_station_fault` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `charging_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Chute closure is described as a fullness-driven behavior: the chute closes when the chute is full (not simply when both AGVs are in the station). The source also provides exchange timing targets and a threshold concept: stage exchanges before reaching 80% fullness, with a goal of median 8-second exchange time and a floor of 6.7 seconds. If exchanges/tipping are slow, chutes can close, and exchange time can extend into the minutes area after closure.

## When To Use

Use when you need to interpret why chute closure is occurring and how exchange timing targets relate to avoiding chute closure during AGV/tipper exchanges.

## Access Or Tools Needed

* Training video segment transcript (00:28:37.000 to 00:32:10.000) for chute closure and timing targets

## Related Operational Context

* ctx_training_video_chute_closure_and_exchange_timing_v1

## Procedure Steps

### Step 1 — Apply the chute-closure rule: chute closes when the chute is full

**Responsible role:** L1_support

**Instruction:**
When you observe chute closure behavior during exchanges, interpret it using the source rule: the chute gets closed when the chute is full, not when both AGVs are in the station.

**Expected result:**
Your explanation for the observed chute closure is based on chute fullness (full chute triggers closure), rather than on whether both AGVs were in the station.

**Stop or Escalate If:**

* If chute closure timing does not align with the fullness-based explanation, escalate for deeper investigation beyond this segment.

---

### Step 2 — Link slow exchange/tipping to eventual chute closure

**Responsible role:** L1_support

**Instruction:**
If exchange performance is slow (for example, tipping is not happening quickly enough), interpret that shoots/chutes will eventually close as everything gets full.

**Expected result:**
You can connect the observed exchange slowness to eventual chute closure as a consequence of the chute reaching full conditions.

**Stop or Escalate If:**

* If the observed behavior does not match the “slow tipping/exchange leads to eventual closure” model, escalate for deeper investigation beyond this segment.

---

### Step 3 — Use the exchange staging threshold concept: exchange before 80%

**Responsible role:** L1_support

**Instruction:**
When interpreting exchange performance, apply the source’s threshold concept: stage for an exchange and complete it before hitting 80% fullness.

**Expected result:**
Your interpretation includes whether exchanges were completed before the 80% fullness threshold concept described by the source.

**Stop or Escalate If:**

* If chute closure occurs despite exchanges being expected to complete before 80%, escalate for deeper investigation beyond this segment.

---

### Step 4 — Frame expectations with exchange timing targets (median 8 seconds; floor 6.7 seconds)

**Responsible role:** L1_support

**Instruction:**
When interpreting exchange timing, use the source’s targets: goal is a median 8-second exchange time and the floor is 6.7 seconds.

**Expected result:**
You can state whether the observed exchange timing is consistent with the source’s median 8-second goal and 6.7-second floor.

**Stop or Escalate If:**

* If exchange timing does not match the source’s targets and chute closure behavior cannot be explained by the fullness/threshold model, escalate for deeper investigation beyond this segment.

---

### Step 5 — Explain the impact when chute closes before the exchange completes

**Responsible role:** L1_support

**Instruction:**
If you determine the chute closed before the exchange, anticipate the source-described impact: exchange time can extend into the minutes area after closing the chute, picking it up, and then exchanging.

**Expected result:**
Your interpretation explains prolonged exchange time as a downstream effect of chute closure occurring before the exchange.

**Stop or Escalate If:**

* If chute closure timing and exchange timing do not follow the source-described sequence (closure first leading to minutes-area exchange time), escalate for deeper investigation beyond this segment.

---

## Success Criteria

* You can explain chute closure timing using the fullness-based rule (chute closes when full, not when both AGVs are in station).
* You can relate observed exchange slowness to eventual chute closure (e.g., not tipping quick enough).
* You can apply the source’s threshold concept (exchange before 80%) and timing targets (median 8 seconds; floor 6.7 seconds).
* If chute closure occurs first, you can explain why exchange time extends into minutes area.

## Failure Conditions

* Chute closure occurs and cannot be explained by the chute-fullness rule.
* Exchange timing is slow enough that chute closure occurs before exchange completion.
* Observed exchange timing extends into minutes area without a chute-closure-first sequence that matches the source model.

## Escalation Guidance

* If chute closure timing does not align with the fullness-based explanation, escalate for deeper investigation beyond this training segment.

## Missing Details / Known Gaps

* The packet does not provide live system UI/API fields to measure chute fullness, chute-closed timestamps, or exchange timing directly; it only provides the interpretation rules and timing targets from the training segment.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_interpret_chute_closure_and_exchange_timing_targets
- Source ID: `training_video_day1`
- Source Type: `training_video`
