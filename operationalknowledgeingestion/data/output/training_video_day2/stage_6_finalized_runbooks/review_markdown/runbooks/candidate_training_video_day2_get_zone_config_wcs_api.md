# View Current Zone Configuration in the WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_current_zone_configuration_wcs_api_v1` |
| Title | View Current Zone Configuration in the WCS API |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `zone_config_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog or an equivalent approved API client to execute GET Get Zone Config and inspect the live zone configuration.

## When To Use

Use the OptiSweep / WCS API to retrieve and inspect the current live zone configuration during configuration verification or troubleshooting.

## Do Not Use For

* Do not use this procedure to change the zone configuration.
* Do not use Update Zone Config; the operation is described as no longer used.

## Safety And Operational Notes

* This procedure is read-only and does not include Update Zone Config or another configuration-changing operation.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog / WCS API client
* GET Get Zone Config

## Related Operational Context

* ctx_training_video_system_api_operations_v1
* ctx_training_video_zone_configuration_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep / WCS API System API list showing GET Get Zone Config among the available operations.*

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*OptiSweep / WCS API System operations view identifying GetZoneConfig as the operation that shows the current zone configuration and distinguishing UpdateZoneConfig as unused.*

## Procedure Steps

### Step 1 — Open GET Get Zone Config in the OptiSweep / WCS API

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent approved API client, open the OptiSweep / WCS API and locate GET Get Zone Config in the System API list.

**Expected result:**
GET Get Zone Config is visible and selected as the API operation to inspect the current zone configuration.

**Stop or Escalate If:**

* Escalate if GET Get Zone Config is not available or cannot be selected.

---

### Step 2 — Execute GET Get Zone Config in the OptiSweep / WCS API

**Responsible role:** L2_support

**Instruction:**
With GET Get Zone Config selected in Apidog or the approved OptiSweep / WCS API client, execute GET Get Zone Config.

**Expected result:**
The API client returns a response for GET Get Zone Config.

**Stop or Escalate If:**

* Escalate if the GET Get Zone Config request fails.
* Do not proceed to any configuration update operation.

---

### Step 3 — Review the returned zone configuration

**Responsible role:** L2_support

**Instruction:**
Review the returned configuration values in the OptiSweep / WCS API client and use them as the current zone configuration for the diagnostic.

**Expected result:**
The GET Get Zone Config response displays the current live zone configuration values.

**Stop or Escalate If:**

* Escalate if the response does not display the current zone configuration.

---

## Success Criteria

* GET Get Zone Config is available in the OptiSweep / WCS API client.
* The request executes successfully.
* The response displays the current live zone configuration values.

## Failure Conditions

* GET Get Zone Config is unavailable or cannot be selected.
* The GET Get Zone Config request fails.
* The response does not display the current zone configuration.

## Escalation Guidance

* Escalate to L3_support if the request fails or the response does not display the current zone configuration.
* Do not use Update Zone Config as a workaround; the operation is described as no longer used.

## Missing Details / Known Gaps

* The source does not provide the API URL, authentication requirements, request headers, or response schema.
* The source does not provide individual zone-configuration field names or their expected values.
* The source does not define a specific API error response or troubleshooting action beyond escalating when the request fails or the current configuration is not displayed.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_get_zone_config_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
