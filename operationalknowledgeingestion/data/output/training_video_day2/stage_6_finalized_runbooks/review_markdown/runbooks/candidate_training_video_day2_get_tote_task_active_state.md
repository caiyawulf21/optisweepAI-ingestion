# Inspect Active Tote State With GetToteTask

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_inspect_active_tote_state_with_gettოტetask_v1` |
| Title | Inspect Active Tote State With GetToteTask |
| Procedure Type | `diagnostic` |
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

Use the OptiSweep / WCS API through Apidog or an equivalent WCS API client to submit the GET GetToteTask request and inspect the current active state of totes.

## When To Use

Use when L2 or L3 support needs to inspect the live active state of tote tasks through the OptiSweep / WCS API using Apidog or an equivalent WCS API client.

## Do Not Use For

* Removing a tote from the system.
* Resending a tote task to the Robotics database model.
* Interpreting response fields or HTTP response codes not defined in the source.

## Safety And Operational Notes

* Use the GET GetToteTask request for state inspection. Do not substitute tote-changing requests such as RemoveTote, InitializeTote, Exchange Tote, or Update Exchange Settings.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog or equivalent WCS API client
* Totes API area
* GET GetToteTask

## Related Operational Context

* ctx_training_video_tote_api_reference_v1
* ctx_training_video_tote_system_state_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*Apidog / WCS API overview showing the API client and the Totes API group, including GET GetToteTask.*

![artifact_training_video_training_video_day2_0031_for_totes_we_have_exchange_sorter_primary_02_44_11_000](assets/54d41adfcf4b3f8f.jpg)

*Totes API view showing GET GetToteTask and the description that it shows the active state of totes.*

## Procedure Steps

### Step 1 — Open the Totes API area in Apidog

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent WCS API client, open the OptiSweep / WCS API and select the Totes API area.

**Expected result:**
The Totes API area is open and the GET GetToteTask request is visible.

**Stop or Escalate If:**

* Escalate to L3 support if the GetToteTask request cannot be opened.

---

### Step 2 — Submit the GET GetToteTask request

**Responsible role:** L2_support

**Instruction:**
Open GET GetToteTask and submit it using the request controls available in Apidog or the equivalent WCS API client.

**Expected result:**
The GET GetToteTask request is submitted and returns tote-task information.

**Stop or Escalate If:**

* Escalate to L3 support if the GetToteTask request cannot be submitted.

---

### Step 3 — Review the returned active tote state

**Responsible role:** L2_support

**Instruction:**
Review the returned tote-task information from GET GetToteTask for the active state of the totes.

**Expected result:**
The returned tote-task information shows the current active state of the totes.

**Stop or Escalate If:**

* Escalate to L3 support if the returned information does not show tote task state.

---

## Success Criteria

* The Totes API area is accessible in Apidog or an equivalent WCS API client.
* GET GetToteTask is opened and submitted successfully.
* The returned tote-task information shows the active state of the totes.

## Failure Conditions

* GET GetToteTask cannot be opened.
* GET GetToteTask cannot be submitted.
* The returned information does not show tote task state.

## Escalation Guidance

* Escalate to L3 support if the GetToteTask request cannot be opened or submitted.
* Escalate to L3 support if the returned information does not show tote task state.
* The source does not define HTTP response codes or additional response fields; do not infer them during this procedure.

## Missing Details / Known Gaps

* The source does not define the HTTP response codes.
* The source does not define the response schema or additional response fields.
* The source does not provide the API endpoint, base URL, authentication steps, or environment-selection procedure.
* The source does not define how to interpret individual tote-task states beyond identifying the active state of the totes.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_get_tote_task_active_state
- Source ID: `training_video_day2`
- Source Type: `training_video`
