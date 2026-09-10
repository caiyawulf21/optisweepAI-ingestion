# Cancel active exchanges after a manual bag out (when system is back up)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_cancel_active_unactive_exchanges_after_manual_bag_out_v1` |
| Title | Cancel active exchanges after a manual bag out (when system is back up) |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `bag_out_or_closeout_state` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

After a manual bag out, items/requests are marked to exchange. Once the system is back up and running, use the system “cancel” function to cancel the active unactive exchanges created by that bag out so the canceled bag-out requests do not continue to require processing.

## When To Use

Use when a customer/operator performed a manual bag out, the system is back up and running, and you need to cancel the active unactive exchanges that were created by the bag out so those bag-out requests do not have to be processed further.

## Safety And Operational Notes

* The source frames manual bag out as a high-impact, labor-intensive event; proceed only after the system is back up and running.

## Access Or Tools Needed

* Access to the system feature/control that performs the “cancel” function for active unactive exchanges (exact UI/API control name not specified in the packet).
* API Dog access is referenced in the source as the tool used for API calls.

## Related Operational Context

* ctx_training_video_cancel_exchanges_after_bag_out_v1

## Visual References

![artifact_training_video_training_video_day2_0033_a_purge_or_close_so_manual_primary_02_50_45_500](assets/a47b2c64a103b938.jpg)

*Source segment explaining that after the system is back up and running, you can cancel all active unactive exchanges created by a manual bag out; includes the “cancel” intent and labor-impact context.*

![artifact_training_video_training_video_day2_0025_yeah_you_know_it_s_it_primary_02_21_32_000](assets/dede127121710b0e.jpg)

*Database/model context for how exchanges/bag-out closeout are represented in system state (active exchange model / active bag out entry).*

## Procedure Steps

### Step 1 — Confirm the system is back up and running after the manual bag out

**Responsible role:** L1_support

**Instruction:**
Confirm the system is back up and running before attempting to cancel active unactive exchanges created by the manual bag out.

**Expected result:**
System status is in a back-up-and-running state (so the cancel action is applicable).

**Stop or Escalate If:**

* If the system is not back up and running, do not proceed with cancel; resolve system recovery first.

---

### Step 2 — Identify that the bag out event marked items/requests to exchange

**Responsible role:** L1_support

**Instruction:**
Confirm that the manual bag out caused the relevant items/requests to be marked to exchange (i.e., the bag-out-related active unactive exchanges exist).

**Expected result:**
Bag-out-related exchanges are present/marked to exchange as a result of the manual bag out.

**Stop or Escalate If:**

* If you cannot confirm bag-out-related exchanges are marked to exchange, pause and reassess before canceling.

---

### Step 3 — Use the “cancel” function to cancel all active unactive exchanges

**Responsible role:** L1_support

**Instruction:**
Execute the documented “cancel” action to cancel all active unactive exchanges created by the manual bag out.

**Expected result:**
Active unactive exchanges created by the bag out are canceled.

**Stop or Escalate If:**

* If the cancel action does not clear the active exchanges created by the bag out, escalate to support.

---

### Step 4 — Verify the bag-out requests/exchanges are canceled

**Responsible role:** L1_support

**Instruction:**
Verify that the bag-out-related exchanges/requests are canceled so the system no longer requires those bag-out requests to be processed.

**Expected result:**
The system no longer requires the canceled bag-out requests to be processed (bag-out-related exchanges are no longer active).

**Stop or Escalate If:**

* If the cancel action does not clear the active exchanges created by the bag out, escalate to support.

---

## Success Criteria

* Active unactive exchanges created by the manual bag out are canceled.
* Canceled bag-out requests do not continue to require processing.

## Failure Conditions

* Cancel does not clear the active exchanges created by the bag out.
* Bag-out requests/exchanges remain active and still require processing after cancel.

## Escalation Guidance

* If the cancel action does not clear the active exchanges created by the bag out, escalate to support (the source frames manual bag out as a labor-intensive, high-impact event).

## Missing Details / Known Gaps

* The packet does not specify the exact live UI screen/control or the exact API Dog request name/parameters for the “cancel all active unactive exchanges” action.
* The packet does not specify the exact live verification method (which table/model/view or which field/state indicates that bag-out-related exchanges are canceled).

## Source Lineage

- Candidate IDs: candidate_training_video_day2_cancel_active_exchanges_after_bag_out
- Source ID: `training_video_day2`
- Source Type: `training_video`
