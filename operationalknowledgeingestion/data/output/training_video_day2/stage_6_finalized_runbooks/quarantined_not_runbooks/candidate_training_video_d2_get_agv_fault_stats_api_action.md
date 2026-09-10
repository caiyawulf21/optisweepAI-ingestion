# Use System API action “Get AGV Fault Stats” to retrieve current AGV fault statistics

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_system_api_get_agv_fault_stats_v1` |
| Title | Use System API action “Get AGV Fault Stats” to retrieve current AGV fault statistics |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_smeme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the System API action labeled “Get AGV Fault Stats” (shown as “GetAgvFaultstats”) to retrieve the current AGV fault statistics, such as after a manual bag out.

## When To Use

When you need the current AGV fault statistics (for example, after a manual bag out).

## Access Or Tools Needed

* System API interface that exposes the action labeled “GetAgvFaultstats” / “Get AGV Fault Stats”.

## Related Operational Context

* ctx_training_video_system_api_actions_overview_v1
* ctx_training_video_alarm_agv_fault_stats_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*Frame showing the System API actions list including “GetAgvFaultstats” / “Get AGV Fault Stats” and surrounding action descriptions (e.g., Open All Chutes, CloseOut, System State).*

## Procedure Steps

### Step 1 — Identify the System API action labeled “GetAgvFaultstats” / “Get AGV Fault Stats”

**Responsible role:** L1_support

**Instruction:**
In the System API interface, locate the action labeled “GetAgvFaultstats” (shown as “Get AGV Fault Stats”).

**Expected result:**
You have identified the correct System API action control/label “GetAgvFaultstats” / “Get AGV Fault Stats”.

---

### Step 2 — Run “Get AGV Fault Stats” to fetch current AGV fault statistics

**Responsible role:** L1_support

**Instruction:**
Execute the System API action “GetAgvFaultstats” / “Get AGV Fault Stats” to fetch the current AGV fault statistics.

**Expected result:**
The API returns the current AGV fault statistics.

**Stop or Escalate If:**

* If no fault stats are returned or the response is empty/failed, stop and escalate.

---

### Step 3 — Record/inspect the returned fault stats as the current values

**Responsible role:** L1_support

**Instruction:**
Inspect the returned payload from “Get AGV Fault Stats” and record the current AGV fault statistics values you receive.

**Expected result:**
You have recorded the returned current AGV fault statistics values from the API response.

**Stop or Escalate If:**

* If the response is empty/failed (no fault stats), stop and escalate.

---

## Success Criteria

* The “Get AGV Fault Stats” System API action returns current AGV fault statistics (non-empty response).
* The returned fault statistics are recorded as the current values.

## Failure Conditions

* API response is empty or indicates failure (no fault stats returned).

## Escalation Guidance

* If no fault stats are returned or the response is empty/failed, stop and escalate (the source provides no further troubleshooting steps).

## Missing Details / Known Gaps

* The source does not specify the exact response fields/format for the fault stats payload.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_get_agv_fault_stats_api_action
- Source ID: `training_video_day2`
- Source Type: `training_video`
