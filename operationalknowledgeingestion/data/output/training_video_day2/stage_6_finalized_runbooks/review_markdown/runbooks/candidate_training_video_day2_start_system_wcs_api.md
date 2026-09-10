# Start OptiSweep System Through the WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_start_optisweep_system_through_wcs_api_v1` |
| Title | Start OptiSweep System Through the WCS API |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog or an equivalent approved API client to start the system from a shutdown state, then verify the live system state is no longer shutdown.

## When To Use

Use the OptiSweep / WCS API when the live system state is shutdown and an authorized L2 or L3 support user needs to start the system through the System Startup operation.

## Do Not Use For

* Do not use when GET System State does not report shutdown.
* Do not use as a substitute for investigating an API request that cannot be executed or returns an unrecognized result.
* Do not use this procedure to perform physical recovery, E-stop, or LOTO actions.

## Safety And Operational Notes

* Confirm the live system state before issuing POST System Startup.
* Stop and escalate if the system state does not change after the startup request.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog / WCS API client
* GET System State
* POST System Startup

## Related Operational Context

* ctx_training_video_system_api_operations_v1
* ctx_training_video_system_state_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep / WCS API list showing GET System State and POST System Startup in the System API operations.*

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*System API list and live-operation descriptions showing System State and System Startup behavior.*

## Procedure Steps

### Step 1 — Locate System Startup in the WCS API client

**Responsible role:** L2_support

**Instruction:**
Open the OptiSweep / WCS API in Apidog or an equivalent approved API client and locate POST System Startup in the System API list.

**Expected result:**
The System API list displays POST System Startup and GET System State.

**Stop or Escalate If:**

* The required API operation cannot be located or executed.

---

### Step 2 — Confirm the system is shut down

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client, execute GET System State and inspect the returned current system state. Continue only when the returned state is shutdown.

**Expected result:**
GET System State returns shutdown as the current system state.

**Stop or Escalate If:**

* GET System State does not report shutdown.
* GET System State cannot be executed or returns an unrecognized result.

---

### Step 3 — Execute System Startup and recheck state

**Responsible role:** L2_support

**Instruction:**
After confirming shutdown in the OptiSweep / WCS API, execute POST System Startup. Then execute GET System State again and inspect the returned state.

**Expected result:**
The startup request completes and the subsequent GET System State response returns the current post-startup state.

**Stop or Escalate If:**

* The System Startup request cannot be executed.
* The API returns an unrecognized result.
* The subsequent system state remains shutdown.

---

### Step 4 — Verify the system left shutdown

**Responsible role:** L2_support

**Instruction:**
Compare the second GET System State result with the initial shutdown result in the OptiSweep / WCS API client.

**Expected result:**
The second GET System State result no longer reports shutdown, indicating that the system left the shutdown state.

**Stop or Escalate If:**

* The system state does not change after the startup request.
* The returned state is unrecognized.

---

## Success Criteria

* GET System State initially reports shutdown.
* POST System Startup executes successfully.
* A subsequent GET System State no longer reports shutdown.
* The returned post-startup state is recognized as running or another non-shutdown state.

## Failure Conditions

* The API operation cannot be located or executed.
* GET System State returns an unrecognized result.
* POST System Startup returns an unrecognized result.
* The system state remains shutdown after the startup request.

## Escalation Guidance

* Stop and escalate if the system state does not change after the startup request.
* Escalate if the API request cannot be executed or returns an unrecognized result.
* This source does not define additional API response handling or a detailed startup confirmation response.

## Missing Details / Known Gaps

* The source does not define the exact successful API response or a complete list of valid running/non-shutdown state values.
* The source does not define API authentication, request parameters, endpoint URLs, timeout handling, or retry behavior.
* The source does not state whether a production stop or LOTO is required before using POST System Startup.
* The source does not define additional recovery actions when the state remains shutdown.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_start_system_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
