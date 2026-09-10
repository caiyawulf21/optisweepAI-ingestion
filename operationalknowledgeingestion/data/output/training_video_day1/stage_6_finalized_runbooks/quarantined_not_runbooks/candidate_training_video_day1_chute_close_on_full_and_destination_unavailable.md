# Confirm chute closure and destination unavailable when tote reaches full threshold

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_confirm_chute_closure_destination_unavailable_v1` |
| Title | Confirm chute closure and destination unavailable when tote reaches full threshold |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sort_lifecycle_state` |
| Access Surface | `stunnel` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `chute_bypassed_or_stuck_closed`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify that when a tote reaches the system’s “full” threshold (~80%), the system closes the chute and communicates to Chat that the chute/destination is unavailable so no additional packages come down during the tote exchange.

## When To Use

Use this procedure when you need to confirm the expected behavior that occurs at the tote “full” threshold: the chute is closed (highest priority) and Chat is told the chute is unavailable so packages do not continue coming down during the exchange.

## Access Or Tools Needed

* Chat interface/logs where the chute unavailable directive is communicated (as referenced by the source)

## Related Operational Context

* ctx_training_video_chute_close_on_full_v1

## Procedure Steps

### Step 1 — Identify the tote fullness state using the source thresholds (~80% full)

**Responsible role:** L1_support

**Instruction:**
Using the tote fullness thresholds described by the source, confirm the tote is at the “full” threshold (~80%).

**Expected result:**
The tote is at the “full” threshold (~80%), which is the point where the source states the chute is closed (highest priority).

---

### Step 2 — Check that Chat is told the chute is unavailable so no packages come down during exchange

**Responsible role:** L1_support

**Instruction:**
When the tote is at the “full” threshold, check Chat communications/logs for the directive that the chute is unavailable so that no packages come down while doing an exchange.

**Expected result:**
At the full threshold (~80%), Chat receives/reflects the message that the chute is unavailable, preventing additional packages from coming down during the exchange.

**Stop or Escalate If:**

* If the chute-unavailable indication is not present when the tote is at the full threshold, escalate (source states this should prevent additional packages from coming down during exchange).

---

### Step 3 — Confirm the chute is closed at the full threshold (highest priority)

**Responsible role:** L1_support

**Instruction:**
At the time the tote reaches the “full” threshold (~80%), confirm the chute is closed.

**Expected result:**
At the full threshold (~80%), the chute is closed.

**Stop or Escalate If:**

* If the chute is not closed at the full threshold, note this as a failure of the source-described highest-priority behavior and escalate.

---

### Step 4 — If chute closure/unavailable behavior is missing at full, record and escalate

**Responsible role:** L1_support

**Instruction:**
If either (a) Chat does not indicate the chute is unavailable at full, or (b) the chute is not closed at full, document the discrepancy and escalate per your support process.

**Expected result:**
A discrepancy is recorded when the source-described behavior is not present at the full threshold, and escalation is initiated.

**Stop or Escalate If:**

* Escalate if the chute closure/unavailable indication is not present when the tote is at the full threshold.

---

## Success Criteria

* When tote fullness reaches the “full” threshold (~80%), the chute is closed.
* At the same full threshold, Chat indicates the chute is unavailable so no packages come down during the exchange.

## Failure Conditions

* Tote is at full (~80%) but Chat does not indicate chute is unavailable.
* Tote is at full (~80%) but the chute is not closed.

## Escalation Guidance

* Escalate if chute closure/unavailable indication is not present when the tote is at the full threshold, since the source describes this as the mechanism to stop packages during exchange.

## Missing Details / Known Gaps

* The source does not specify the exact live UI element/log field name that shows the “chute unavailable” message beyond “tell Chat”.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_chute_close_on_full_and_destination_unavailable
- Source ID: `training_video_day1`
- Source Type: `training_video`
