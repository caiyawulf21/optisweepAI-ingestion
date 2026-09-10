# Explain why an AGV can move out without a replacement (exchange/backfill gap) during AGV exchange pairing

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_explain_agv_exchange_backfill_gap_v1` |
| Title | Explain why an AGV can move out without a replacement (exchange/backfill gap) during AGV exchange pairing |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `agv_tracking_or_path_lost`, `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep exchange pairing rule to explain an observed “AGV moves out without another one to replace it.” The source-backed mechanism is that OptiSweep sends the exchange commands as a paired action; therefore, a visible gap typically indicates the trailing AGV behind the departing AGV had a fault / was not backfilled properly. The source also describes a timing edge case where the trailing AGV is reported ready for a new task and completes/faults at the same time, which can lead to improper backfill.

## When To Use

When you need to interpret the source-backed reason an AGV appears to depart during an exchange pairing without a replacement AGV backfilling it.

## Access Or Tools Needed

* Training video segment transcript (00:28:37.000 to 00:32:10.000) for the pairing/backfill explanation

## Related Operational Context

* ctx_training_video_agv_exchange_pairing_v1

## Procedure Steps

### Step 1 — Apply the exchange pairing rule (front AGV movement depends on the trailing AGV)

**Responsible role:** L1_support

**Instruction:**
Use the source pairing rule: the front AGV will not move until the AGV behind it is available for the paired exchange command, because OptiSweep sends both exchange commands at the same time.

**Expected result:**
Your interpretation is consistent with the rule that the exchange command to leave is only sent when there is an AGV behind it (paired commands).

---

### Step 2 — Check whether the trailing AGV fault/backfill issue explains the gap

**Responsible role:** L1_support

**Instruction:**
When you observe an AGV moving out without a replacement, evaluate whether the trailing AGV behind it could have had a fault / was not backfilled properly, since the source states this is the only time this can happen.

**Expected result:**
You can explain the gap using the source-backed mechanism: the trailing AGV behind the departing AGV had a fault or was not backfilled properly.

**Stop or Escalate If:**

* If the observed behavior cannot be explained by the source-backed mechanism (paired commands + trailing AGV fault/backfill issue), escalate for deeper system evidence beyond this training segment.

---

### Step 3 — Consider the timing edge case: trailing AGV ready for new task and completes/faults at the same time

**Responsible role:** L1_support

**Instruction:**
If you need a more specific explanation, consider the source’s timing edge case: the trailing AGV behind the departing AGV may be “ready for a new task” and also “completed and faulted at the same time,” which can lead to improper backfill.

**Expected result:**
Your explanation includes the edge case where the trailing AGV is reported ready for a new task while also completing/faulting simultaneously, resulting in improper backfill.

**Stop or Escalate If:**

* If the observed behavior cannot be explained by the source-backed mechanism (paired commands + trailing AGV fault/backfill issue), escalate for deeper system evidence beyond this training segment.

---

### Step 4 — Use chute-closure behavior as context for exchange timing effects

**Responsible role:** L1_support

**Instruction:**
When interpreting related behavior around the exchange, remember the source’s chute-closure rule: chute gets closed when the chute is full, not when both AGVs are in the station (or “it’s both”).

**Expected result:**
Your explanation accounts for the possibility that exchange timing issues can contribute to later chute fullness/closure effects, consistent with the source’s closure rule.

---

## Success Criteria

* You can explain the observed “AGV moves out without another one to replace it” using the source-backed paired-command mechanism and the trailing AGV fault/backfill issue.
* If needed, your explanation includes the source-described timing edge case where the trailing AGV is ready for a new task and completes/faults at the same time, leading to improper backfill.

## Failure Conditions

* The observed behavior cannot be explained by the source-backed mechanism (paired commands + trailing AGV fault/backfill issue).

## Escalation Guidance

* If the observed behavior cannot be explained by the source-backed mechanism (paired commands + trailing AGV fault/backfill issue), escalate for deeper system evidence beyond this training segment.

## Missing Details / Known Gaps

* The packet does not provide live system fields/rows/statuses to verify the trailing AGV fault/backfill condition in RMS/WCS/SSMS; it only provides the source-backed explanation mechanism.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_interpret_agv_exchange_backfill_gap
- Source ID: `training_video_day1`
- Source Type: `training_video`
