# Verify parcel divert/sort confirmation message is received to track tote contents

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_parcel_divert_sort_confirmation_message_v1` |
| Title | Verify parcel divert/sort confirmation message is received to track tote contents |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `stunnel` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

After a parcel sorts down to a chute location and into a tote, a divert confirm or sort confirmation chat message is triggered. This message is critical for tracking: without it, the system does not know where the parcel went or what is in the tote. This runbook provides a live-system check to confirm the confirmation message is received and that the software associates the parcel to the tote location in the rack.

## When To Use

Use when you need to verify that a parcel’s divert/sort confirmation chat message was received after the parcel sorts down to a chute location and into a tote, so the system can record the parcel’s destination and tote contents.

## Access Or Tools Needed

* Chat interface/logs where divert confirm or sort confirmation messages appear (as referenced by the source)

## Related Operational Context

* ctx_training_video_sort_confirmation_message_v1
* ctx_training_video_parcel_lifecycle_tote_tracking_v1

## Procedure Steps

### Step 1 — Identify the parcel lifecycle moment (sorted down to chute location and into a tote)

**Responsible role:** L1_support

**Instruction:**
Confirm the parcel has reached the lifecycle moment described as: it sorts down to a chute location and into a tote.

**Expected result:**
You can identify that the parcel has sorted down to a chute location and into a tote (the point at which the next chat message should be triggered).

---

### Step 2 — Check for the next divert confirm / sort confirmation chat message

**Responsible role:** L1_support

**Instruction:**
In the chat interface/logs, check whether the next chat message is received that indicates a divert confirm or sort confirmation for the parcel lifecycle moment (sort down to chute location and into a tote).

**Expected result:**
A divert confirm or sort confirmation chat message is received for the parcel.

**Stop or Escalate If:**

* Stop and escalate if the divert/sort confirmation message is not received, because the system then cannot determine where the parcel went or what is in the tote.

---

### Step 3 — Confirm software associates the parcel to the tote location in the rack

**Responsible role:** L1_support

**Instruction:**
After the divert confirm / sort confirmation chat message is received, confirm that the software adds the parcel to the tote location in the rack.

**Expected result:**
The software adds the parcel to the tote location in the rack (tote tracking is updated based on the confirmation).

---

## Success Criteria

* A divert confirm or sort confirmation chat message is received for the parcel after it sorts down to a chute location and into a tote.
* Software associates the parcel to the tote location in the rack (tote contents tracking is updated).

## Failure Conditions

* Divert confirm / sort confirmation chat message is missing after the parcel sorts down to the chute location and into a tote.
* Software does not add the parcel to the tote location in the rack after sorting to the destination.

## Escalation Guidance

* Escalate if the divert/sort confirmation chat message is not received, because the system then cannot determine where the parcel went or what is in the tote.

## Missing Details / Known Gaps

* The source states to check “chat” for the divert confirm / sort confirmation message but does not specify the exact live UI/log location or message label fields to filter by in the chat interface.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_parcel_sort_confirmation_divert_tracking
- Source ID: `training_video_day1`
- Source Type: `training_video`
