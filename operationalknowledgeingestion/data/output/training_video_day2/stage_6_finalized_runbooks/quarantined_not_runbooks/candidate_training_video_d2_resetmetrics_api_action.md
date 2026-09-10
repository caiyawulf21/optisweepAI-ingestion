# Use System API action “ResetMetrics” to generate a new sort GUID for metrics tracking

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_system_api_action_resetmetrics_generate_new_sort_guid_v1` |
| Title | Use System API action “ResetMetrics” to generate a new sort GUID for metrics tracking |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the System API action labeled “ResetMetrics” when UPS cycles a sort to generate a new sort GUID so metrics tracking can be associated with the new sort.

## When To Use

Use when UPS cycles a sort and you need metrics tracking to roll over to a new sort GUID via the System API action “ResetMetrics”.

## Access Or Tools Needed

* System API interface that exposes the “ResetMetrics” action

## Related Operational Context

* ctx_training_video_system_api_actions_overview_v1
* ctx_training_video_hmi_metric_resetmetrics_sort_guid_v1

## Visual References

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*System API actions list including “ResetMetrics” and its description: “ResetMetrics: Is called when UPS cycles a sort. Generates a new sort guid for metrics to be tracked.”*

## Procedure Steps

### Step 1 — Identify the System API action labeled “ResetMetrics”

**Responsible role:** L1_support

**Instruction:**
In the System API interface, locate the action/control labeled “ResetMetrics”.

**Expected result:**
The “ResetMetrics” action label/control is identified and ready to be executed.

---

### Step 2 — Run “ResetMetrics” when UPS cycles a sort

**Responsible role:** L1_support

**Instruction:**
Execute the System API action “ResetMetrics” at the time UPS cycles a sort (as described by the source).

**Expected result:**
ResetMetrics execution results in generation of a new sort GUID for metrics tracking.

**Stop or Escalate If:**

* If a new sort GUID is not generated, stop and escalate (the source does not provide troubleshooting steps).

---

### Step 3 — Confirm ResetMetrics effect: new sort GUID for metrics tracking

**Responsible role:** L1_support

**Instruction:**
After executing ResetMetrics, confirm that the system has generated a new sort GUID for metrics tracking.

**Expected result:**
A new sort GUID is generated for metrics tracking.

**Stop or Escalate If:**

* If a new sort GUID is not generated, stop and escalate (the source does not provide troubleshooting steps).

---

## Success Criteria

* After UPS cycles a sort and ResetMetrics is executed, a new sort GUID is generated for metrics tracking.

## Failure Conditions

* No new sort GUID is generated for metrics tracking after executing ResetMetrics when UPS cycles a sort.

## Escalation Guidance

* Stop and escalate if a new sort GUID is not generated (the source does not provide troubleshooting steps).

## Missing Details / Known Gaps

* The source does not specify where the new sort GUID is displayed/returned in the live System API interface.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_resetmetrics_api_action
- Source ID: `training_video_day2`
- Source Type: `training_video`
