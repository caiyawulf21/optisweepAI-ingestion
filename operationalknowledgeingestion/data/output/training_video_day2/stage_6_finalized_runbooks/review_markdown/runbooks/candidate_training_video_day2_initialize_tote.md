# Initialize a Tote Through the Totes API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_initialize_tote_through_totes_api_v1` |
| Title | Initialize a Tote Through the Totes API |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `tote_lifecycle_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog or an equivalent WCS API client to submit POST InitializeTote with the required ToteId and StationId and add a tote to the system.

## When To Use

Use this procedure when an authorized L2 or L3 support user needs to add a tote to OptiSweep through the live OptiSweep / WCS API.

## Do Not Use For

* Do not use this procedure for Exchange Tote, Exchange Lane, Remove Tote, Get Tote Task, Resend Tote Task, or exchange-setting operations.
* Do not proceed when either ToteId or StationId is unavailable.

## Safety And Operational Notes

* Confirm that the ToteId and StationId are available before submitting the request.
* Stop if the API rejects the request or if either required identifier is unavailable.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog or equivalent WCS API client
* Totes API area
* POST InitializeTote
* ToteId
* StationId

## Related Operational Context

* ctx_training_video_tote_api_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep / WCS API overview in Apidog, including the Totes API area and POST InitializeTote.*

![artifact_training_video_training_video_day2_0031_for_totes_we_have_exchange_sorter_primary_02_44_11_000](assets/54d41adfcf4b3f8f.jpg)

*Totes API view showing InitializeTote and the required ToteId and StationId identifiers.*

## Procedure Steps

### Step 1 — Open the Totes API area in Apidog

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent OptiSweep / WCS API client, open the Totes API area and locate the InitializeTote request.

**Expected result:**
The Totes API area is open and the InitializeTote request is available.

**Stop or Escalate If:**

* Stop if POST InitializeTote is not available in the OptiSweep / WCS API client.
* Escalate to L3 support if the request is unavailable after verifying access to the WCS API client.

---

### Step 2 — Enter the ToteId and StationId

**Responsible role:** L2_support

**Instruction:**
Open POST InitializeTote in the OptiSweep / WCS API client and enter the required ToteId and StationId fields.

**Expected result:**
Both required fields, ToteId and StationId, contain the identifiers for the tote and station being initialized.

**Stop or Escalate If:**

* Stop if ToteId is unavailable.
* Stop if StationId is unavailable.

---

### Step 3 — Submit InitializeTote and inspect the API outcome

**Responsible role:** L2_support

**Instruction:**
Submit the POST InitializeTote request in the OptiSweep / WCS API client and inspect the resulting request outcome.

**Expected result:**
The API displays the outcome of the InitializeTote request; a successful outcome indicates that the tote was added to the system.

**Stop or Escalate If:**

* Stop if the API rejects the request.
* Escalate to L3 support if the request is rejected after both ToteId and StationId have been supplied.
* Escalate if the API outcome does not indicate whether the tote was added.

---

## Success Criteria

* POST InitializeTote is submitted through the OptiSweep / WCS API.
* The request contains both ToteId and StationId.
* The API outcome indicates that the tote was added to the system.

## Failure Conditions

* ToteId is unavailable or missing.
* StationId is unavailable or missing.
* The API rejects the InitializeTote request.
* The API outcome does not indicate whether the tote was added.

## Escalation Guidance

* Escalate to L3 support if POST InitializeTote is rejected after both required identifiers are supplied.
* Include the ToteId, StationId, and displayed API request outcome when escalating, subject to applicable handling requirements.
* The source does not define the success response format or HTTP response codes.

## Missing Details / Known Gaps

* The source does not define the successful API response body, status text, or HTTP response code.
* The source does not specify how to verify the initialized tote after the API request beyond the displayed API outcome.
* The source does not define the exact endpoint URL, authentication method, or request payload format.
* The source does not establish whether production operation must be stopped before initializing a tote.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_initialize_tote
- Source ID: `training_video_day2`
- Source Type: `training_video`
