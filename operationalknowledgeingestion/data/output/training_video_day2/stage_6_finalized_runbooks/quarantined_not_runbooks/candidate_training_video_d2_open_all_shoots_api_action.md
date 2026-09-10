# Use System API action “Open All Chutes” to reopen all closed chutes

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_system_api_action_open_all_chutes_reopen_all_closed_chutes_v1` |
| Title | Use System API action “Open All Chutes” to reopen all closed chutes |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `zone_config_state` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the System API action labeled “Open All Chutes” to open all previously closed chutes so the system can be started up again after a closeout was done without cycling the sort.

## When To Use

When a customer performed a closeout but did not cycle the sort, and you need to reopen all closed chutes so the system can be started up again.

## Access Or Tools Needed

* System API interface that exposes the “Open All Chutes” action

## Related Operational Context

* ctx_training_video_system_api_actions_overview_v1
* ctx_training_video_operation_chute_and_closeout_functions_v1

## Visual References

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*Frame showing the System API actions list including the “Open All Chutes” action label and related System/CloseOut/Purge actions.*

## Procedure Steps

### Step 1 — Identify the System API action labeled “Open All Chutes”

**Responsible role:** L1_support

**Instruction:**
In the System API interface, locate the action labeled “Open All Chutes” under the System API actions.

**Expected result:**
The “Open All Chutes” action is visible and selectable in the System API interface.

---

### Step 2 — Run “Open All Chutes” to open all closed chutes

**Responsible role:** L1_support

**Instruction:**
Execute the System API action “Open All Chutes”.

**Expected result:**
All previously closed chutes are opened.

**Stop or Escalate If:**

* If chutes do not reopen as expected, stop and escalate to support for deeper troubleshooting (the source does not provide additional recovery steps).

---

### Step 3 — Confirm chutes opened to support system start-up

**Responsible role:** L1_support

**Instruction:**
Confirm that the system/chute state reflects that chutes are open after running “Open All Chutes”.

**Expected result:**
All previously closed chutes are opened.

**Stop or Escalate If:**

* If chutes do not reopen as expected, stop and escalate to support for deeper troubleshooting (the source does not provide additional recovery steps).

---

## Success Criteria

* After executing “Open All Chutes”, all previously closed chutes are open.

## Failure Conditions

* Chutes do not reopen as expected after running “Open All Chutes”.

## Escalation Guidance

* If chutes do not reopen as expected, stop and escalate to support for deeper troubleshooting. The source does not provide additional recovery steps.

## Missing Details / Known Gaps

* The source names the “Open All Chutes” action and its intended effect, but does not provide the exact live execution workflow (e.g., which specific UI/API request fields to set, how to submit, or what response/status indicates completion).

## Source Lineage

- Candidate IDs: candidate_training_video_d2_open_all_shoots_api_action
- Source ID: `training_video_day2`
- Source Type: `training_video`
