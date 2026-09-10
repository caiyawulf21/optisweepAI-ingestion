# Retrieve tote exchange settings using the Tote Management API (Get Exchange Settings)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_retrieve_tote_exchange_settings_get_exchange_settings_v1` |
| Title | Retrieve tote exchange settings using the Tote Management API (Get Exchange Settings) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tote_exchange_sequence` |
| Access Surface | `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Totes Aveva API page (API Features for Tote Management) to retrieve tote exchange settings/configurations via the “Get Exchange Settings” function and confirm the API returns exchange configuration data.

## When To Use

When you need to retrieve the current tote exchange settings/configurations from the Tote Management API using the “Get Exchange Settings” function.

## Safety And Operational Notes

* Do not bypass the supported control layer; use the exposed API functions rather than attempting direct database access (the source emphasizes not bypassing the official software/API layer).

## Access Or Tools Needed

* Totes Aveva API page / “API Features for Tote Management”
* Obeyba access (implied by the login prompt shown on the API page)

## Related Operational Context

* ctx_training_video_tote_api_exchange_functions_v1

## Procedure Steps

### Step 1 — Navigate to the “API Features for Tote Management” page on the Totes Aveva API screen

**Responsible role:** L2_support

**Instruction:**
Open the Totes Aveva API screen and navigate to the page titled “API Features for Tote Management”. If prompted, log in to Obeyba.

**Expected result:**
The “API Features for Tote Management” page is visible and includes a function labeled “Get Exchange Settings”.

**Stop or Escalate If:**

* If you cannot log in to Obeyba / cannot reach the API features page, stop and escalate (no further troubleshooting is provided in the source).

---

### Step 2 — Use “Get Exchange Settings” to retrieve tote exchange settings/configurations

**Responsible role:** L2_support

**Instruction:**
On the “API Features for Tote Management” page, locate the function labeled “Get Exchange Settings” and run it. If the UI prompts for required parameters, provide them and submit the request.

**Expected result:**
The API returns tote exchange settings and configurations for tote exchanges.

**Stop or Escalate If:**

* If the settings cannot be retrieved or the response is empty/error, stop and escalate (the source does not provide further troubleshooting steps).

---

### Step 3 — Record the returned exchange settings/configurations as displayed by the API

**Responsible role:** L2_support

**Instruction:**
Copy/record the tote exchange settings/configurations exactly as displayed in the API response after running “Get Exchange Settings”.

**Expected result:**
You have captured the returned tote exchange settings/configurations from the API response.

**Stop or Escalate If:**

* If the response is empty/error and you cannot record settings, stop and escalate (no further troubleshooting steps are provided in the source).

---

## Success Criteria

* “Get Exchange Settings” returns tote exchange settings/configurations (non-empty response).
* The retrieved settings/configurations are recorded from the API response display.

## Failure Conditions

* API response is empty.
* API response shows an error or settings cannot be retrieved.

## Escalation Guidance

* If the settings cannot be retrieved or the response is empty/error, stop and escalate. The source does not provide additional troubleshooting steps.

## Missing Details / Known Gaps

* The source does not specify which parameters (if any) “Get Exchange Settings” requires, nor the exact response fields/format returned by the API.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_tote_api_get_exchange_settings
- Source ID: `training_video_day1`
- Source Type: `training_video`
