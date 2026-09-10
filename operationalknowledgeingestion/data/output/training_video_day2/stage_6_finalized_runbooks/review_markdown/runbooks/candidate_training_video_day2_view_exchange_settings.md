# View Current Tote Exchange Settings in the OptiSweep / WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_current_tote_exchange_settings_v1` |
| Title | View Current Tote Exchange Settings in the OptiSweep / WCS API |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `tote_exchange_sequence` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog to submit GET GetExchangeSettings and inspect the current tote exchange headings or exchange settings.

## When To Use

Use the OptiSweep / WCS API through Apidog when support needs to inspect the current tote exchange headings or exchange settings without changing them.

## Do Not Use For

* Do not use this read-only check to modify exchange settings.
* Do not use it to infer settings that are not returned by GET GetExchangeSettings.
* Do not use it as a substitute for a procedure that updates exchange settings.

## Safety And Operational Notes

* This procedure is a read-only check.
* Do not submit an exchange-setting update while performing this procedure.

## Access Or Tools Needed

* OptiSweep / WCS API (wcs_api)
* Apidog / WCS API client (apidog)
* Totes API area
* GET GetExchangeSettings

## Related Operational Context

* ctx_training_video_tote_api_reference_v1
* ctx_training_video_tote_exchange_settings_v1

## Visual References

![artifact_training_video_training_video_day2_0031_for_totes_we_have_exchange_sorter_primary_02_44_11_000](assets/54d41adfcf4b3f8f.jpg)

*OptiSweep / WCS API Totes area showing GET GetExchangeSettings and the current exchange-settings function.*

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep API overview identifying Apidog on the primary server and the Totes API endpoints.*

## Procedure Steps

### Step 1 — Open the Totes API area in Apidog

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent WCS API client, open the OptiSweep / WCS API and navigate to the Totes API area.

**Expected result:**
The Totes API area is visible and includes the GET GetExchangeSettings request.

**Stop or Escalate If:**

* Escalate to L3 support if the Totes API area or GET GetExchangeSettings request is unavailable.

---

### Step 2 — Submit GET GetExchangeSettings

**Responsible role:** L2_support

**Instruction:**
In the Totes API area of Apidog, open the GET GetExchangeSettings request and submit it using the displayed request controls.

**Expected result:**
The GET GetExchangeSettings request completes and displays a returned result for the current exchange settings.

**Stop or Escalate If:**

* Escalate to L3 support if the request cannot be submitted.
* Escalate to L3 support if the request does not return the current exchange settings.

---

### Step 3 — Review the returned exchange headings or settings

**Responsible role:** L2_support

**Instruction:**
Review the returned result in the OptiSweep / WCS API client and identify the displayed current exchange headings or exchange settings.

**Expected result:**
The returned result displays the current exchange headings or current exchange settings.

**Stop or Escalate If:**

* Escalate to L3 support if the returned result does not display the current exchange headings or exchange settings.
* Do not modify exchange settings as part of this read-only check.

---

## Success Criteria

* The Totes API area is available in Apidog or an equivalent WCS API client.
* GET GetExchangeSettings can be submitted.
* The returned result displays the current exchange headings or current exchange settings.
* No exchange settings are modified during the check.

## Failure Conditions

* The Totes API area or GET GetExchangeSettings request is unavailable.
* The request cannot be submitted.
* The request does not return the current exchange headings or exchange settings.

## Escalation Guidance

* Escalate to L3 support if GET GetExchangeSettings cannot be submitted.
* Escalate to L3 support if the request does not return the current exchange headings or exchange settings.
* Do not infer a response schema or HTTP response-code meaning; the source does not define response fields or HTTP response codes.
* Do not modify exchange settings during this diagnostic.

## Missing Details / Known Gaps

* The source does not define the returned exchange-settings response fields or schema.
* The source does not define HTTP response codes or their meanings.
* The source does not provide a specific Apidog request URL, server address, authentication procedure, or connection configuration.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_view_exchange_settings
- Source ID: `training_video_day2`
- Source Type: `training_video`
