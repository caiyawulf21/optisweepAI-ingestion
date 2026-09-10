# Use OptiSweep/WCS API Tote endpoints to initialize, exchange, and exchange-lane totes (Exchange sorter side zone)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_optsweep_wcs_api_tote_endpoints_exchange_sorter_side_zone_v1` |
| Title | Use OptiSweep/WCS API Tote endpoints to initialize, exchange, and exchange-lane totes (Exchange sorter side zone) |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Capability Tags | None |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API (via Apidog / WCS API client) tote endpoints to initialize a tote, trigger tote exchange actions (including Exchange sorter side zone requirements: sorter side name + zone), exchange to a specific lane destination, and verify results using GetToteTask and GetExchangeSettings. If needed, update exchange settings with UpdateExchange.

## When To Use

When you need to add/initialize totes and trigger tote exchange actions for testing using OptiSweep/WCS API tote endpoints, including Exchange sorter side zone usage (sorter side name + zone).

## Access Or Tools Needed

* Apidog / WCS API client (OptiSweep / WCS API)

## Related Operational Context

* ctx_training_video_tote_exchange_sorter_side_zone_v1
* ctx_training_video_tote_api_parameter_reference_v1
* ctx_training_video_tote_task_state_and_resend_v1
* ctx_training_video_exchange_settings_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0031_for_totes_we_have_exchange_sorter_primary_02_44_11_000](assets/54d41adfcf4b3f8f.jpg)

*Frame showing tote API endpoints and required identifiers for Exchange sorter side zone, InitializeTote (ToteID + StationID), ExchangeTote (ToteName), ExchangeLane (LaneName), GetToteTask (active state), GetExchangeSettings (current exchange headings/settings), and UpdateExchange (adjust exchange settings).*

## Procedure Steps

### Step 1 — Open the OptiSweep / WCS API client (Apidog / WCS API)

**Responsible role:** L2_support

**Instruction:**
Open the OptiSweep / WCS API client (Apidog / WCS API) and navigate to the tote endpoints area for the calls used in this procedure.

**Expected result:**
You are positioned in the API client to select/call the tote endpoints: InitializeTote, ExchangeTote, ExchangeLane, GetToteTask, GetExchangeSettings, and UpdateExchange.

---

### Step 2 — Set Exchange sorter side zone parameters (sorter side name + zone)

**Responsible role:** L2_support

**Instruction:**
When using the Exchange sorter side zone, set the required sorter side name and zone values in the request context/parameters.

**Expected result:**
The request includes both a sorter side name and a zone for Exchange sorter side zone usage.

**Stop or Escalate If:**

* Stop and escalate if required identifiers (sorter side name + zone) are rejected or missing in API responses.

---

### Step 3 — Initialize a tote using InitializeTote (ToteID + StationID)

**Responsible role:** L2_support

**Instruction:**
Call InitializeTote and provide ToteID and StationID.

**Expected result:**
The InitializeTote API call succeeds and the tote is added/initialized using ToteID + StationID.

**Stop or Escalate If:**

* Stop and escalate if required identifiers (ToteID/StationID) are rejected or missing in API responses.

---

### Step 4 — Exchange a specific tote using ExchangeTote (ToteName)

**Responsible role:** L2_support

**Instruction:**
Call ExchangeTote and provide the required ToteName.

**Expected result:**
The ExchangeTote API call succeeds and exchanges the specific tote identified by ToteName.

**Stop or Escalate If:**

* Stop and escalate if required identifiers (ToteName) are rejected or missing in API responses.

---

### Step 5 — Exchange to a specific destination via lane using ExchangeLane (LaneName)

**Responsible role:** L2_support

**Instruction:**
Call ExchangeLane and provide the required LaneName.

**Expected result:**
The ExchangeLane API call succeeds and exchanges to the destination associated with the provided LaneName.

**Stop or Escalate If:**

* Stop and escalate if required identifiers (LaneName) are rejected or missing in API responses.

---

### Step 6 — Verify tote activity state using GetToteTask

**Responsible role:** L2_support

**Instruction:**
Call GetToteTask and observe the returned active state of the totes.

**Expected result:**
GetToteTask returns tote task/active state information showing the tote activity state after the requested InitializeTote/ExchangeTote/ExchangeLane action.

**Stop or Escalate If:**

* Stop and escalate if GetToteTask does not show the expected active state change after the requested Initialize/Exchange action.

---

### Step 7 — View current exchange headings/settings using GetExchangeSettings

**Responsible role:** L2_support

**Instruction:**
Call GetExchangeSettings and confirm the response includes the current exchange headings/settings.

**Expected result:**
GetExchangeSettings returns the current exchange headings/settings for the exchange lane.

---

### Step 8 — Adjust exchange settings using UpdateExchange (exchange headings/settings)

**Responsible role:** L2_support

**Instruction:**
If adjustment is needed, call UpdateExchange to update the exchange settings/heading values.

**Expected result:**
UpdateExchange returns a successful update of exchange settings/heading values.

---

## Success Criteria

* InitializeTote succeeds using ToteID + StationID to add/initialize a tote.
* ExchangeTote succeeds using ToteName to exchange the specific tote.
* ExchangeLane succeeds using LaneName to exchange to the specific destination.
* GetToteTask returns tote active state reflecting the expected tote activity change after the requested initialize/exchange action.
* GetExchangeSettings returns current exchange headings/settings.
* UpdateExchange succeeds when exchange settings/heading values are updated.

## Failure Conditions

* Required identifiers (sorter side name + zone, ToteID/StationID, ToteName, LaneName) are rejected or missing in API responses.
* GetToteTask does not show the expected active state change after the requested Initialize/Exchange action.
* GetExchangeSettings does not return exchange headings/settings.

## Escalation Guidance

* Stop and escalate if required identifiers are rejected or missing in API responses.
* Stop and escalate if GetToteTask does not show the expected active state change after the requested Initialize/Exchange action.

## Missing Details / Known Gaps

* The packet does not provide the exact Apidog UI navigation steps (endpoint selection area) or the exact request/response field names beyond the required identifiers (sorter side name + zone, ToteID + StationID, ToteName, LaneName).
* The packet does not provide the exact GetToteTask response schema/field names or the specific 'active state' values that should be observed as the expected change.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_tote_exchange_sorter_side_zone_api_calls
- Source ID: `training_video_day2`
- Source Type: `training_video`
