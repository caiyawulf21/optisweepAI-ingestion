# Retrieve Current AGV Fault Statistics From the WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_retrieve_current_agv_fault_statistics_from_wcs_api_v1` |
| Title | Retrieve Current AGV Fault Statistics From the WCS API |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog or an equivalent approved API client to retrieve current AGV fault statistics. Treat sort goods information as historical rather than as the current fault result.

## When To Use

Use the OptiSweep / WCS API in Apidog when a live diagnostic result for current AGV fault statistics is required.

## Do Not Use For

* Do not use historical sort information as a substitute for the current AGV fault statistics.
* Do not use this procedure to assign fault severity or prescribe corrective actions; the source does not define fault meanings or corrective actions.

## Safety And Operational Notes

* This procedure retrieves AGV fault statistics with the GET GetAgvFaultStats operation; no production stop or physical action is defined in the source.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog / WCS API client
* GET GetAgvFaultStats
* Access to the approved WCS API client on the primary server

## Related Operational Context

* ctx_training_video_system_api_operations_v1
* ctx_training_video_agv_fault_stats_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*Apidog / WCS API overview showing GET GetAgvFaultStats in the System API list.*

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*WCS API System list and live-use description identifying GetAgvFaultStats as the operation for current AGV fault statistics and distinguishing sort goods as historical.*

## Procedure Steps

### Step 1 — Locate GetAgvFaultStats in the OptiSweep / WCS API client

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent approved API client, open the OptiSweep / WCS API and locate GET GetAgvFaultStats in the System API list.

**Expected result:**
GET GetAgvFaultStats is visible and selected as the request to inspect current AGV fault statistics.

**Stop or Escalate If:**

* Escalate if the OptiSweep / WCS API cannot be opened.
* Escalate if GET GetAgvFaultStats is not present in the System API list.

---

### Step 2 — Execute GET GetAgvFaultStats

**Responsible role:** L2_support

**Instruction:**
With GET GetAgvFaultStats selected in Apidog or the approved WCS API client, execute the GET request.

**Expected result:**
The OptiSweep / WCS API returns a response containing the current AGV fault statistics.

**Stop or Escalate If:**

* Escalate if the GET request fails.
* Escalate if the response does not contain current AGV fault statistics.

---

### Step 3 — Verify that the response is current AGV fault information

**Responsible role:** L2_support

**Instruction:**
Review the returned result in the OptiSweep / WCS API client and identify it as the current AGV fault statistics. Do not substitute sort goods or other historical sort information for this result.

**Expected result:**
The diagnostic record identifies the returned result as current AGV fault statistics, while historical sort information remains separate.

**Stop or Escalate If:**

* Escalate if the response cannot be distinguished from historical sort information.
* Do not infer fault severity meanings or corrective actions from this result.

---

## Success Criteria

* GET GetAgvFaultStats is available in the OptiSweep / WCS API client.
* The GET request completes successfully.
* The response provides current AGV fault statistics.
* Historical sort information is not substituted for the current fault result.

## Failure Conditions

* The OptiSweep / WCS API or GET GetAgvFaultStats request is unavailable.
* The request fails.
* The response does not return current AGV fault statistics.
* The result cannot be distinguished from historical sort information.

## Escalation Guidance

* Escalate to the appropriate support path if the request fails or does not return current AGV fault statistics.
* Do not assign fault severity or corrective actions from this procedure because those meanings are not defined in the source.

## Missing Details / Known Gaps

* The source does not provide the API response schema or field names.
* The source does not define AGV fault categories, severity meanings, or corrective actions.
* The source does not provide the API endpoint URL, authentication method, or connection troubleshooting details.
* The source does not define a response status or threshold that confirms current data beyond the operation description.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_get_agv_fault_stats_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
