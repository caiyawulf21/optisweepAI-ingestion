# Confirm Which Tools/Locations Hold Operational Data (Data Collection Fragmentation Reference)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_confirm_which_tools_locations_hold_operational_data_v1` |
| Title | Confirm Which Tools/Locations Hold Operational Data (Data Collection Fragmentation Reference) |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When gathering operational data in real time, the source indicates you may need to use separate tools and that operational information is collected in 3 or 4 different places. This procedure helps you identify which tool/location holds the specific operational data element you need, aligned with the ongoing effort to narrow toward a standard single location.

## When To Use

Use this when you need to determine where a specific operational data element is collected for real-time troubleshooting/verification, and you suspect the environment uses multiple tools/locations rather than a single consolidated interface.

## Access Or Tools Needed

* Access to the separate tools used for operational data gathering (tool names not specified in the source)
* Awareness of the current “3 or 4 different places” where information is being collected (as discovered on-site)

## Related Operational Context

* ctx_training_video_data_collection_tools_fragmentation_v1
* ctx_training_video_information_collection_multiple_locations_v1

## Visual References

![artifact_training_video_training_video_day2_0036_works_but_in_real_time_having_primary_02_59_48_000](assets/e0fc5fc6c1fb24ec.jpg)

*Frame showing the discussion that real-time data gathering requires separate tools and that information is collected in 3 or 4 different places, with an effort to narrow to a standard single slot/location.*

## Procedure Steps

### Step 1 — Account for fragmented real-time operational data collection across separate tools

**Responsible role:** L1_support

**Instruction:**
When you start gathering operational data in real time, treat the data collection as potentially requiring separate tools (not one consolidated interface).

**Expected result:**
You proceed with the understanding that the operational data you need may require checking multiple tools/locations rather than a single place.

---

### Step 2 — Identify the current set of 3 or 4 information collection places

**Responsible role:** L1_support

**Instruction:**
Identify the current set of “3 or 4 different places” where information is being collected for the relevant operational topic.

**Expected result:**
You can list the current 3 or 4 tool/location places that are used to collect the operational information for the topic you are working on.

---

### Step 3 — Map the needed data element to the correct tool/location

**Responsible role:** L1_support

**Instruction:**
If multiple locations exist, determine which location/tool corresponds to the specific data element you need, noting the source’s stated effort to narrow toward a standard single slot/location.

**Expected result:**
You identify the specific tool/location that contains the operational data element you need for the current real-time task.

**Stop or Escalate If:**

* If you cannot determine which tool/location contains the needed data, stop and request guidance from the team responsible for standardization (as implied by the source discussion).

---

## Success Criteria

* You can name the relevant tool(s)/location(s) that contain the needed operational data element, consistent with the source’s “separate tools” and “3 or 4 different places” framing.

## Failure Conditions

* You cannot identify the current 3 or 4 information collection places for the operational topic.
* You cannot map the needed data element to the correct tool/location.

## Escalation Guidance

* If you cannot determine which tool/location contains the needed operational data, stop and request guidance from the team responsible for standardization (implied by the source discussion about narrowing to a standard single slot).

## Missing Details / Known Gaps

* The source does not name the specific tools/locations that make up the “3 or 4 different places,” so this runbook cannot instruct which exact systems to check.
* The source does not specify which operational data elements map to which specific tool/location(s), so mapping requires on-site discovery or team guidance.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_identify_data_collection_tool_fragmentation
- Source ID: `training_video_day2`
- Source Type: `training_video`
