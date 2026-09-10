# Perform OptiSweep CloseOut Through the WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_perform_optisweep_closeout_through_the_wcs_api_v1` |
| Title | Perform OptiSweep CloseOut Through the WCS API |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `bag_out_or_closeout_state`, `tote_exchange_sequence` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `bag_out_stuck` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use POST CloseOut in the OptiSweep / WCS API through Apidog or an equivalent approved API client for a bag-out operation. CloseOut closes all chutes and exchanges totes containing parcels.

## When To Use

Use the OptiSweep / WCS API when the customer wants to perform a bag-out operation using CloseOut.

## Do Not Use For

* Do not use CloseOut as a substitute for Purge. Purge exchanges every tote in the system and does not print a label, while CloseOut exchanges totes containing parcels.
* Do not use this procedure when the required operation is to cancel closeout exchanges that are not in progress; the source identifies Cancel Closeout for that situation.

## Safety And Operational Notes

* CloseOut is associated with bag-out activity and changes chute and tote state.
* Confirm that CloseOut, rather than Purge or Cancel Closeout, matches the required operation before sending the request.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog / WCS API client
* Access to the primary server where Apidog is installed
* Live chute and tote status

## Related Operational Context

* ctx_training_video_system_api_operations_v1
* ctx_training_video_closeout_purge_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep API overview showing Apidog on the primary server and the System, AGV, and Totes API groups.*

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*System API list showing POST CloseOut, POST Purge, POST Cancel Closeout, and the documented CloseOut behavior.*

## Procedure Steps

### Step 1 — Locate POST CloseOut in the OptiSweep / WCS API

**Responsible role:** L2_support

**Instruction:**
On the primary server, open Apidog or an equivalent approved API client for the OptiSweep / WCS API. In the System API list, locate POST CloseOut. Verify that the selected operation is CloseOut rather than Purge or Cancel Closeout.

**Expected result:**
POST CloseOut is available in the System API list and is selected for the bag-out operation.

**Stop or Escalate If:**

* POST CloseOut is not available in the OptiSweep / WCS API.
* The required operation is unclear between CloseOut, Purge, and Cancel Closeout.

---

### Step 2 — Execute POST CloseOut in the OptiSweep / WCS API

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client, execute POST CloseOut. Use the request configuration available in the approved client; the supplied source does not define request parameters or a response confirmation field.

**Expected result:**
The POST CloseOut request is submitted to the OptiSweep / WCS API for the bag-out operation.

**Stop or Escalate If:**

* POST CloseOut cannot be submitted.
* The API client returns an error or does not provide a usable request result.

---

### Step 3 — Observe CloseOut results on the live OptiSweep / WCS system

**Responsible role:** L2_support

**Instruction:**
After submitting POST CloseOut, observe the live chute and tote status associated with the OptiSweep / WCS operation. Verify that all chutes close and that totes containing parcels are exchanged.

**Expected result:**
All chutes close and totes containing parcels are exchanged.

**Stop or Escalate If:**

* Chutes do not close.
* Totes containing parcels are not exchanged as described.
* CloseOut remains incomplete or its resulting live state cannot be verified.

---

## Success Criteria

* POST CloseOut is submitted through the OptiSweep / WCS API.
* All chutes close.
* Totes containing parcels are exchanged.

## Failure Conditions

* POST CloseOut is unavailable or cannot be submitted.
* The API client reports an error or does not provide a usable request result.
* One or more chutes remain open after CloseOut.
* Totes containing parcels are not exchanged.

## Escalation Guidance

* Stop and escalate if chutes do not close.
* Stop and escalate if parcel-containing totes are not exchanged as described.
* Escalate if the CloseOut request cannot be submitted or its live result cannot be verified.
* Do not substitute Purge for CloseOut; Purge has different tote-exchange behavior.

## Missing Details / Known Gaps

* The source does not provide request parameters or payload fields for POST CloseOut.
* The source does not provide response fields, HTTP status criteria, or an API confirmation control.
* The source does not identify the exact live UI or status fields used to verify chute closure and tote exchange.
* The source does not specify timing for completion or what to do if CloseOut remains in progress.
* Production-stop and LOTO requirements are not specified.
* Authorization requirements for executing CloseOut are not specified.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_closeout_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
