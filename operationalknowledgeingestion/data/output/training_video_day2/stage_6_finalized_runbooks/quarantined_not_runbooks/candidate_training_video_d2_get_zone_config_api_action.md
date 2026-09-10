# Use System API action “Get Zone Config” to view current zone configuration

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_system_api_get_zone_config_v1` |
| Title | Use System API action “Get Zone Config” to view current zone configuration |
| Procedure Type | `diagnostic` |
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

Use the OptiSweep System API action “Get Zone Config” (GetZoneConfig) to retrieve and display the current zone configuration values.

## When To Use

When you need to view the current zone configuration values via the OptiSweep System API action list that includes “Get Zone Config” / “GetZoneConfig”.

## Access Or Tools Needed

* System API interface that exposes the action labeled “Get Zone Config” / “GetZoneConfig”.

## Related Operational Context

* ctx_training_video_system_api_actions_overview_v1
* ctx_training_video_component_zone_configuration_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*Frame showing the System API action list including “Get Zone Config” / “GetZoneConfig”.*

## Procedure Steps

### Step 1 — Identify the System API action labeled “Get Zone Config” / “GetZoneConfig”

**Responsible role:** L1_support

**Instruction:**
In the OptiSweep System API action interface, locate the action labeled “Get Zone Config” (GetZoneConfig).

**Expected result:**
You can point to/select the action labeled “Get Zone Config” / “GetZoneConfig” in the System API interface.

**Stop or Escalate If:**

* If you cannot retrieve the zone configuration (action not available or cannot be executed), stop and escalate (no troubleshooting steps are provided in the source).

---

### Step 2 — Run “Get Zone Config” to display the current zone configuration

**Responsible role:** L1_support

**Instruction:**
Execute/run the System API action “Get Zone Config” (GetZoneConfig) and wait for the response/output that displays the zone configuration.

**Expected result:**
The API returns/displays the current zone configuration.

**Stop or Escalate If:**

* If zone configuration cannot be retrieved, stop and escalate (no troubleshooting steps are provided in the source).

---

### Step 3 — Review the returned zone configuration values as the current configuration

**Responsible role:** L1_support

**Instruction:**
Review the values returned by the “Get Zone Config” API action output and treat them as the current zone configuration values.

**Expected result:**
The returned output includes zone configuration values that can be reviewed as the current configuration.

**Stop or Escalate If:**

* If zone configuration cannot be retrieved, stop and escalate (no troubleshooting steps are provided in the source).

---

## Success Criteria

* The “Get Zone Config” System API action returns/displays the current zone configuration values.

## Failure Conditions

* Zone configuration cannot be retrieved (no output/empty response for “Get Zone Config”).

## Escalation Guidance

* If zone configuration cannot be retrieved, stop and escalate (no troubleshooting steps are provided in the source).

## Missing Details / Known Gaps

* The source does not specify the exact zone configuration fields/structure returned by “Get Zone Config”.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_get_zone_config_api_action
- Source ID: `training_video_day2`
- Source Type: `training_video`
