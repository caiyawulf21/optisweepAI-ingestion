# Verify Hot Bin Disable Leaves Chutes Closed After Exchange

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_hot_bin_disable_leaves_chutes_closed_after_exchange_v1` |
| Title | Verify Hot Bin Disable Leaves Chutes Closed After Exchange |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training source to verify the documented behavior that hot bin disable does not reopen chutes after the exchange is complete.

## When To Use

Use when reviewing or confirming expected chute behavior for a hot bin disable condition after an exchange has completed.

## Do Not Use For

* Do not use this runbook to enable or disable hot bin behavior.
* Do not use this runbook to force a chute to reopen.
* Do not use this runbook as a recovery procedure when chute behavior differs from the documented source statement.

## Safety And Operational Notes

* This source supports a verification of documented behavior only.
* Do not infer or perform a chute reopen action from this source because no such procedure is provided.

## Access Or Tools Needed

* Access to the training source or documented hot bin disable behavior
* Ability to observe chute state after exchange completion

## Related Operational Context

* ctx_training_video_hot_bin_disable_status_v1

## Procedure Steps

### Step 1 — Identify hot bin disable condition

**Responsible role:** operator

**Instruction:**
Identify that the condition being reviewed is hot bin disable, using the source terminology.

**Expected result:**
The operator confirms the review is for a hot bin disable condition.

**Screens / Images:**

![artifact_training_video_training_video_day1_0065_so_you_can_do_a_hop_primary_02_17_25_500](assets/2cb5e083dc8ddcbb.jpg)

*Look for the training frame text and transcript context describing hot bin behavior and the statement about hot bin disable not reopening chutes after exchange.*


**Stop or Escalate If:**

* Stop or escalate if the condition cannot be tied to hot bin disable using the source-supported terminology.

---

### Step 2 — Verify exchange is complete

**Responsible role:** operator

**Instruction:**
Verify that an exchange has completed for the affected tote or chute handling sequence.

**Expected result:**
The operator confirms the exchange is complete before checking whether the chute reopened.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the exchange process description showing the tote exchange sequence and timing context.*

![artifact_training_video_training_video_day1_0065_so_you_can_do_a_hop_primary_02_17_25_500](assets/2cb5e083dc8ddcbb.jpg)

*Look for the source statement that specifically applies after the exchange is complete.*


**Stop or Escalate If:**

* Stop or escalate if exchange completion cannot be confirmed.
* Stop or escalate if the observed sequence does not clearly correspond to the affected tote or chute handling sequence.

---

### Step 3 — Check chute state after exchange

**Responsible role:** operator

**Instruction:**
Check the chute state after exchange completion against the source statement that hot bin disable will not reopen chutes after the exchange is complete.

**Expected result:**
The chute remains closed after exchange completion when hot bin disable behavior applies.

**Screens / Images:**

![artifact_training_video_training_video_day1_0065_so_you_can_do_a_hop_primary_02_17_25_500](assets/2cb5e083dc8ddcbb.jpg)

*Look for the slide or transcript text stating that hot bin disable will not reopen chutes after the exchange is complete.*


**Stop or Escalate If:**

* Escalate if the chute behavior does not match the documented source statement.
* Stop if chute state cannot be observed or verified from the available view.

---

### Step 4 — Record verification result

**Responsible role:** operator

**Instruction:**
Record whether the chute remains closed in accordance with the documented behavior.

**Expected result:**
A verification result is recorded as matching or not matching the documented behavior.

**Stop or Escalate If:**

* Escalate if the recorded observation does not match the documented source statement.

---

## Success Criteria

* The condition is confirmed as hot bin disable.
* Exchange completion is confirmed for the affected tote or chute handling sequence.
* The chute is verified to remain closed after exchange completion in accordance with the source.
* The verification result is recorded.

## Failure Conditions

* The condition cannot be confirmed as hot bin disable.
* Exchange completion cannot be confirmed.
* The chute reopens after exchange completion.
* The chute state cannot be verified.
* Observed behavior does not match the documented source statement.

## Escalation Guidance

* Escalate if the chute behavior does not match the documented source statement.
* Do not infer how to force a chute reopen because the source does not provide that procedure.

## Missing Details / Known Gaps

* The source does not provide a control path for enabling or disabling hot bin behavior.
* The source does not provide a procedure for reopening a chute after hot bin disable.
* The source does not define where or how the verification result should be recorded.
* The source does not specify a time estimate for this verification.
* The source does not specify escalation destination or contact path.

## Source Lineage

- Candidate IDs: candidate_training_video_verify_hot_bin_disable_does_not_reopen_chutes
- Source ID: `training_video_day1`
- Source Type: `training_video`
