# Use System API action “CloseOut” to close all chutes and exchange totes with parcels

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_system_api_closeout_to_close_all_chutes_and_exchange_totes_v1` |
| Title | Use System API action “CloseOut” to close all chutes and exchange totes with parcels |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `bag_out_or_closeout_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_smeme_review` |
| Merge Status | `source_finalized` |

## Summary

Run the System API action labeled “CloseOut” to perform a bag-out closeout: it closes all chutes and exchanges any totes with parcels.

## When To Use

Use when the customer wants to bag out and you need to close all chutes and exchange totes with parcels via the System API action “CloseOut”.

## Access Or Tools Needed

* System API interface that exposes the action labeled “CloseOut” (API Dog / System API actions UI)

## Related Operational Context

* ctx_training_video_system_api_actions_overview_v1
* ctx_training_video_operation_chute_and_closeout_functions_v1

## Visual References

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*Frame showing the System API actions list including “CloseOut” and its description (“When the customer wants to bag out this will close all chutes and exchange any totes with parcels.”).*

## Procedure Steps

### Step 1 — Identify the System API action labeled “CloseOut”

**Responsible role:** L1_support

**Instruction:**
In the System API interface (System API actions list), locate the action labeled “CloseOut”.

**Expected result:**
The “CloseOut” action is visible/identifiable in the System API actions list.

---

### Step 2 — Run “CloseOut” when the customer wants to bag out

**Responsible role:** L1_support

**Instruction:**
Execute the System API action “CloseOut” when the customer requests a bag-out.

**Expected result:**
The closeout operation is initiated such that the system will close all chutes and exchange any totes with parcels (as described for “CloseOut”).

**Stop or Escalate If:**

* If closeout does not close chutes or exchange totes as expected, stop and escalate (no additional recovery steps are provided in the source).

---

### Step 3 — Verify “CloseOut” effects: all chutes closed and totes exchanged with parcels

**Responsible role:** L1_support

**Instruction:**
After running “CloseOut”, verify that the operation results in (1) all chutes being closed and (2) totes being exchanged with parcels.

**Expected result:**
All chutes are closed and totes are exchanged with parcels.

**Stop or Escalate If:**

* If closeout does not close chutes or exchange totes as expected, stop and escalate (the source does not provide additional recovery steps).

---

## Success Criteria

* After executing “CloseOut”, all chutes are closed.
* After executing “CloseOut”, totes are exchanged with parcels.

## Failure Conditions

* Closeout does not close all chutes.
* Closeout does not exchange totes with parcels.
* Closeout execution fails or cannot be confirmed as initiated.

## Escalation Guidance

* If closeout does not close chutes or exchange totes as expected, stop and escalate. The source provides no additional recovery steps.

## Missing Details / Known Gaps

* The source does not provide an observable live completion/status signal or where/how to confirm that all chutes are closed and tote exchanges with parcels have completed.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_closeout_api_action
- Source ID: `training_video_day2`
- Source Type: `training_video`
