# Cancel manual bag out exchange tasks that are not in process

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_cancel_manual_bag_out_exchange_tasks_not_in_process_v1` |
| Title | Cancel manual bag out exchange tasks that are not in process |
| Procedure Type | `recovery` |
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

When performing a manual bag out, use the “cancel bag out” option to cancel exchange tasks that are not currently in process. Exchange tasks already in an exchange must be allowed to come and still finish.

## When To Use

Use during a manual bag out when you need to cancel exchange tasks/chests that are not in process, while ensuring any exchange already in progress is allowed to complete.

## Access Or Tools Needed

* Bag out control system UI/control (manual bag out and cancel bag out options)

## Related Operational Context

* ctx_training_video_cancel_bag_out_reference_v1

## Procedure Steps

### Step 1 — Initiate the manual bag out action from the bag out control system

**Responsible role:** operator

**Instruction:**
On the bag out control system, initiate the manual bag out action (the UI/control that provides manual bag out and cancel bag out options).

**Expected result:**
The bag out control system is in the manual bag out context where the cancel bag out option is available.

---

### Step 2 — Select the “cancel bag out” option

**Responsible role:** operator

**Instruction:**
In the manual bag out UI/control, select the “cancel bag out” option.

**Expected result:**
The system applies the cancel bag out behavior for the manual bag out operation.

---

### Step 3 — Verify cancellation scope: cancel exchange tasks/chests that are not in process

**Responsible role:** operator

**Instruction:**
Confirm that the cancel bag out behavior is intended to cancel exchange tasks/chests that are not in process (i.e., not currently in an exchange).

**Expected result:**
Exchange tasks/chests that are not in process are cancelled by the cancel bag out behavior.

**Stop or Escalate If:**

* Stop and escalate if the cancel bag out action cancels items that are already in process.

---

### Step 4 — Ensure in-process exchanges are allowed to finish

**Responsible role:** operator

**Instruction:**
Before/while applying cancel bag out, ensure that any exchange task/chest that is already in an exchange is not cancelled; it must be allowed to come and still finish.

**Expected result:**
Exchange tasks/chests already in an exchange continue to completion (they are not cancelled by cancel bag out).

**Stop or Escalate If:**

* Stop and escalate if the cancel bag out action cancels items that are already in process.
* Stop and escalate if non-in-process exchange tasks are not cancelled as described.

---

## Success Criteria

* Exchange tasks/chests not in process are cancelled during the manual bag out cancel bag out behavior.
* Exchange tasks/chests already in process continue and still finish.

## Failure Conditions

* Cancel bag out cancels exchange tasks/chests that are already in process.
* Exchange tasks/chests that are not in process are not cancelled as described.

## Escalation Guidance

* Stop and escalate if the cancel bag out action cancels items that are already in process, or if non-in-process exchange tasks are not cancelled as described.

## Missing Details / Known Gaps

* The packet does not provide the exact UI label text for the manual bag out initiation control (only that a bag out control system exists).
* The packet does not provide the exact UI label text for the “cancel bag out” button beyond the phrase “cancel bag out/cancelled bag out”.
* The packet does not specify how to visually confirm, on the live system, which exchange tasks/chests are “in process” vs “not in process” (no UI field names/statuses are provided).

## Source Lineage

- Candidate IDs: candidate_training_video_manual_bag_out_cancel_bag_out
- Source ID: `training_video_day1`
- Source Type: `training_video`
