# Exchange a Specific Tote Through the OptiSweep / WCS API (Apidog)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_exchange_specific_tote_through_totes_api_v1` |
| Title | Exchange a Specific Tote Through the OptiSweep / WCS API (Apidog) |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `tote_exchange_sequence` |
| Access Surface | `apidog`, `wcs_api` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Apidog / WCS API client to open the Totes API, submit POST Exchange Tote with the required ToteName, and review the displayed request outcome.

## When To Use

Use the Apidog / WCS API client when support needs to submit an exchange request for one specific tote identified by its ToteName.

## Do Not Use For

* Do not use POST Exchange Lane when the intent is to exchange one specific tote; Exchange Lane uses a LaneName and exchanges a specific destination.
* Do not use this procedure when the required ToteName is unavailable.

## Safety And Operational Notes

* Confirm the intended ToteName before submitting the request because the endpoint exchanges the specific named tote.
* Stop if the required ToteName is unavailable or if the API rejects the request.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog or equivalent WCS API client on a primary server
* Totes API area
* POST Exchange Tote
* ToteName

## Related Operational Context

* ctx_training_video_tote_api_reference_v1
* ctx_training_video_tote_exchange_settings_v1

## Visual References

![artifact_training_video_training_video_day2_0031_for_totes_we_have_exchange_sorter_primary_02_44_11_000](assets/54d41adfcf4b3f8f.jpg)

*Apidog / WCS API Totes area showing POST Exchange Tote and the required ToteName; the endpoint exchanges the specific tote.*

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep API overview showing Apidog installed on primary servers and the Totes API group.*

## Procedure Steps

### Step 1 — Open the Totes API in Apidog

**Responsible role:** L2_support

**Instruction:**
On the primary server, open Apidog or an equivalent OptiSweep / WCS API client and open the Totes API area.

**Expected result:**
The Totes API area is displayed and includes the POST Exchange Tote request.

**Stop or Escalate If:**

* Stop if the OptiSweep / WCS API client or Totes API area is unavailable.
* Escalate if the POST Exchange Tote request is not available after confirming access to the primary server.

---

### Step 2 — Enter the required ToteName

**Responsible role:** L2_support

**Instruction:**
Open POST Exchange Tote in the Apidog / WCS API client and enter the required ToteName.

**Expected result:**
The POST Exchange Tote request contains the intended ToteName.

**Stop or Escalate If:**

* Stop if the required ToteName is unavailable.
* Stop and confirm the target before submitting if the ToteName does not identify the intended specific tote.

---

### Step 3 — Submit the exchange request and review the API outcome

**Responsible role:** L2_support

**Instruction:**
Submit POST Exchange Tote in the Apidog / WCS API client and review the resulting request outcome displayed by the OptiSweep / WCS API.

**Expected result:**
The API displays an outcome for the submitted POST Exchange Tote request.

**Stop or Escalate If:**

* Stop if the API rejects the request.
* Escalate to L3_support if the request is rejected after a valid ToteName is supplied.
* Escalate if the API does not display a resulting request outcome.

---

## Success Criteria

* POST Exchange Tote is available in the Apidog / WCS API client.
* The request is submitted with the confirmed ToteName.
* The API displays a resulting outcome for the request.
* The displayed outcome indicates that the named tote exchange request was processed; the exact success response and HTTP response code are not defined in the source.

## Failure Conditions

* The required ToteName is unavailable.
* The POST Exchange Tote request is unavailable in the Apidog / WCS API client.
* The API rejects the request after a valid ToteName is supplied.
* The API does not display a resulting request outcome.

## Escalation Guidance

* Escalate to L3_support when POST Exchange Tote is rejected after a valid ToteName has been supplied.
* Include the ToteName and the displayed API request outcome when escalating, if available.
* Do not infer success from an undocumented HTTP response code or response body.

## Missing Details / Known Gaps

* The source does not define the endpoint URL, authentication method, or environment-selection details for Apidog.
* The source does not define the API success response, response body, or HTTP response codes.
* The source does not define how to independently verify the tote's post-exchange state after the API request.
* Production-stop and LOTO requirements for submitting this exchange request are not specified.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_exchange_specific_tote
- Source ID: `training_video_day2`
- Source Type: `training_video`
