# Check OptiSweep System State API in Apidog

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_optisweep_system_state_api_in_apidog_v1` |
| Title | Check OptiSweep System State API in Apidog |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `apidog`, `wcs_api` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Apidog / WCS API client on an OptiSweep primary server to perform a read-only check of the GET System State request and determine whether it returns live OptiSweep system data. The source does not define response fields, HTTP status criteria, or response interpretation.

## When To Use

Use Apidog / WCS API client on an OptiSweep primary server when support needs to verify whether the read-only GET System State request can return live OptiSweep system data.

## Do Not Use For

* Do not use this procedure to execute POST System Startup, POST System Shutdown, POST CloseOut, POST Purge, POST ResetMetrics, or other mutating API requests.
* Do not use this procedure as a substitute for interpreting response fields, because the source does not define those fields or their meanings.
* Do not use this procedure for API configuration or endpoint setup; the source does not provide configuration or access details.

## Safety And Operational Notes

* Keep the check read-only. Do not execute the POST requests listed in the OptiSweep API catalog.

## Access Or Tools Needed

* Apidog / WCS API client on an OptiSweep primary server
* OptiSweep / WCS API access
* GET System State request

## Related Operational Context

* ctx_training_video_optisweep_api_suite_overview_v1
* ctx_training_video_apidog_primary_servers_v1
* ctx_training_video_api_endpoint_categories_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*Apidog API overview showing the System endpoint group and the listed GET System State request.*

## Procedure Steps

### Step 1 — Open Apidog on the OptiSweep primary server

**Responsible role:** L2_support

**Instruction:**
On an OptiSweep primary server, open the Apidog / WCS API client and display the OptiSweep API overview.

**Expected result:**
The live Apidog / WCS API client is open and the OptiSweep API overview is visible.

**Stop or Escalate If:**

* Apidog cannot be opened or the OptiSweep API catalog cannot be reached; escalate to L3 support or the appropriate API/system owner.

---

### Step 2 — Select GET System State

**Responsible role:** L2_support

**Instruction:**
In the live Apidog / WCS API client, open the System API group and select the GET System State request.

**Expected result:**
The GET System State request is selected in Apidog and ready to send.

**Stop or Escalate If:**

* GET System State is not listed or cannot be selected; escalate to L3 support or the appropriate API/system owner.

---

### Step 3 — Send the read-only GET System State request

**Responsible role:** L2_support

**Instruction:**
In Apidog / WCS API client, send only the selected GET System State request. Observe whether the response contains live OptiSweep system data rather than an empty or failed request result. Do not send any POST request.

**Expected result:**
The GET System State request returns content representing live OptiSweep system data. The source does not specify the response fields or their meanings.

**Stop or Escalate If:**

* The GET System State request fails, returns no data, or cannot be reached from Apidog; escalate to L3 support or the appropriate API/system owner.
* A POST request is selected or would be executed; stop and return to the read-only GET System State request.

---

## Success Criteria

* Apidog / WCS API client is opened on an OptiSweep primary server.
* The System API group and GET System State request are available.
* The read-only GET System State request returns live OptiSweep system data.

## Failure Conditions

* Apidog or the OptiSweep API catalog cannot be reached.
* GET System State is not listed or cannot be selected.
* The GET System State request fails or returns no data.
* The source does not define HTTP status criteria, response fields, or field meanings.

## Escalation Guidance

* Escalate to L3 support or the appropriate API/system owner if Apidog cannot reach the OptiSweep / WCS API, GET System State is unavailable, or the request fails or returns no data.
* Do not execute mutating POST requests while investigating this read-only check.

## Missing Details / Known Gaps

* The source does not provide Apidog navigation or endpoint configuration details beyond identifying Apidog on the primary servers.
* The source does not provide the GET System State URL, request parameters, authentication requirements, or connection configuration.
* The source does not define HTTP status codes, response fields, field meanings, or detailed healthy-response criteria.
* The source does not establish whether the procedure requires a production stop or LOTO.
* Site-specific primary-server identification and access authorization are not provided.

## Source Lineage

- Candidate IDs: candidate_training_video_apidog_check_system_state_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
