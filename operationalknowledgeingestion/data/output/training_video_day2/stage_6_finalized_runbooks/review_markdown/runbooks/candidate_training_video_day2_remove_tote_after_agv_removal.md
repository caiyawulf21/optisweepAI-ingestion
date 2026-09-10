# Remove a Tote via the OptiSweep / WCS API After AGV Removal

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_tote_after_agv_removal_v1` |
| Title | Remove a Tote via the OptiSweep / WCS API After AGV Removal |
| Procedure Type | `recovery` |
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

Use the OptiSweep / WCS API through Apidog or an equivalent WCS API client to remove a tote by submitting POST RemoveTote with the required ToteId. The associated AGV must be removed before the tote-removal request is submitted.

## When To Use

Use the OptiSweep / WCS API when a tote must be removed from the system and the associated AGV has already been removed.

## Do Not Use For

* Do not use POST RemoveTote while the associated AGV remains in the system.
* Do not use this procedure to remove the AGV; the source identifies RemoveAgv separately but does not define the complete AGV-removal procedure or its verification response.

## Safety And Operational Notes

* Confirm that the associated AGV has been removed before submitting the tote-removal request.
* Stop and escalate if the AGV cannot be removed first or if RemoveTote rejects the request.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog or equivalent WCS API client
* Totes API area
* POST RemoveTote
* ToteId
* AGVs API area and the available AGV status/removal request information

## Related Operational Context

* ctx_training_video_tote_api_reference_v1
* ctx_training_video_tote_system_state_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0031_for_totes_we_have_exchange_sorter_primary_02_44_11_000](assets/54d41adfcf4b3f8f.jpg)

*OptiSweep / WCS API Totes area showing POST RemoveTote and the ToteId requirement.*

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep / WCS API overview showing Apidog on the primary server and the Totes and AGVs API areas.*

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*OptiSweep / WCS API AGVs area showing POST RemoveAgv and the robotId requirement.*

## Procedure Steps

### Step 1 — Verify the associated AGV removal state in the OptiSweep / WCS API

**Responsible role:** L2_support

**Instruction:**
In Apidog or an equivalent OptiSweep / WCS API client, review the AGVs API area and the available AGV status or removal information for the AGV associated with the tote. Proceed only when the associated AGV has been removed from the system.

**Expected result:**
The associated AGV is confirmed as removed before any POST RemoveTote request is submitted.

**Stop or Escalate If:**

* The associated AGV remains in the system.
* The AGV cannot be removed first.
* The available OptiSweep / WCS API state does not allow removal to be confirmed.

---

### Step 2 — Enter the ToteId in POST RemoveTote

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client's Totes API area, open POST RemoveTote and enter the required ToteId.

**Expected result:**
The POST RemoveTote request contains the ToteId for the tote whose associated AGV has already been removed.

**Stop or Escalate If:**

* The required ToteId is unavailable or cannot be entered.
* The associated AGV has not been removed.

---

### Step 3 — Submit POST RemoveTote and review the API outcome

**Responsible role:** L2_support

**Instruction:**
Submit POST RemoveTote in the OptiSweep / WCS API client and review the resulting API response or displayed removal outcome.

**Expected result:**
The API displays the outcome of the RemoveTote request and indicates whether the tote was removed from the system.

**Stop or Escalate If:**

* RemoveTote rejects the request.
* The API does not indicate that the tote was removed.

---

## Success Criteria

* The associated AGV was removed before the tote-removal request was submitted.
* POST RemoveTote was submitted with the required ToteId.
* The OptiSweep / WCS API outcome indicates that the tote was removed from the system.

## Failure Conditions

* The associated AGV remains in the system when RemoveTote is attempted.
* The ToteId is missing or unavailable.
* RemoveTote rejects the request.
* The API response does not indicate that the tote was removed.

## Escalation Guidance

* Escalate to L3_support if the associated AGV cannot be removed first.
* Escalate to L3_support if the API state cannot confirm AGV removal.
* Escalate to L3_support if POST RemoveTote rejects the request or does not produce a removal outcome.

## Missing Details / Known Gaps

* The source does not identify a definitive live API field or response value that confirms the associated AGV has been removed.
* The source does not define the complete AGV-removal procedure or the exact request used to perform it.
* The source does not define the successful POST RemoveTote response, status code, response body, or exact removal confirmation field.
* The source does not provide exact Apidog navigation or request configuration details beyond the Totes API area and POST RemoveTote.
* The source does not provide a ToteId value or a site-specific API endpoint.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_remove_tote_after_agv_removal
- Source ID: `training_video_day2`
- Source Type: `training_video`
