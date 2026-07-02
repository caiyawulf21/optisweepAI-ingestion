# Remove a Tote From the System

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_a_tote_from_the_system_v1` |
| Title | Remove a Tote From the System |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented tote management function shown in the training source to remove a specified tote from the system. The source confirms that a Remove Tote function exists on the tote management API page and that it removes a specified tote from the system, but it does not provide exact field names, button labels beyond the function name, or confirmation message details.

## When To Use

Use when support needs to remove a specified tote from the system using the documented tote management function shown in the training material.

## Do Not Use For

* Do not use when the tote cannot be uniquely identified for removal.
* Do not use as a substitute for undocumented recovery or rollback actions, because the source does not provide those details.

## Safety And Operational Notes

* Use only the documented Remove Tote function shown in the source.
* The source does not provide rollback steps or detailed confirmation behavior; escalate if the result is unclear.

## Access Or Tools Needed

* Access to tote management interface or API-backed remove function
* Tote identifier

## Related Operational Context

* ctx_training_video_tote_management_api_overview_v1

## Procedure Steps

### Step 1 — Identify the tote to remove

**Responsible role:** L1_support

**Instruction:**
Identify the specific tote that needs to be removed from the system using the available tote identifier.

**Expected result:**
A single specified tote is selected for removal.

**Stop or Escalate If:**

* The tote cannot be uniquely identified for removal.

---

### Step 2 — Open the Remove Tote function

**Responsible role:** L1_support

**Instruction:**
Open the tote management function that includes the Remove Tote option on the API page shown in the training material.

**Expected result:**
The Remove Tote function is available for use.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management API page showing Remove Tote among the available tote management features.*


**Stop or Escalate If:**

* The Remove Tote function is not available in the interface.
* Required access to the tote management interface is not available.

---

### Step 3 — Enter or select the tote

**Responsible role:** L1_support

**Instruction:**
Enter or select the specified tote to remove using the available interface.

**Expected result:**
The intended tote is populated in the remove workflow.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management API page where Remove Tote is available; use the interface area associated with tote management to specify the tote.*


**Stop or Escalate If:**

* The specified tote cannot be selected or entered.
* There is uncertainty that the selected tote is the correct tote.

---

### Step 4 — Submit the remove action

**Responsible role:** L1_support

**Instruction:**
Submit the remove action through the available interface.

**Expected result:**
The system accepts the remove request for the specified tote.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management API page showing that Remove Tote is a supported function.*


**Stop or Escalate If:**

* The remove action does not complete.
* The interface shows an error or does not provide a clear completion state.

---

### Step 5 — Verify the tote is removed

**Responsible role:** L1_support

**Instruction:**
Verify through the available tote status view or system response that the tote has been removed from the system.

**Expected result:**
The specified tote no longer appears active in the system response or available tote status view.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management API feature set, including Get Tote Task, which indicates related tote status/query capability exists in the same area.*


**Stop or Escalate If:**

* The tote still appears active afterward.
* The source-provided interface does not provide a clear confirmation outcome.
* Confirmation messages or rollback steps are needed but not provided by the source.

---

## Success Criteria

* The specified tote is removed from the system.
* The tote no longer appears active in the available tote status view or system response, if available.

## Failure Conditions

* The tote cannot be uniquely identified for removal.
* The Remove Tote function cannot be accessed.
* The remove action does not complete.
* The tote still appears active afterward.
* The source does not provide exact confirmation messages or rollback steps.

## Escalation Guidance

* Escalate if the tote cannot be uniquely identified for removal.
* Escalate if the remove action does not complete or the tote still appears active afterward.
* Escalate if confirmation of removal is required but the interface response is unclear, because the source does not provide exact confirmation messages or rollback steps.

## Missing Details / Known Gaps

* Exact navigation path to the tote management page is not provided in the source.
* Exact UI field names and button labels for Remove Tote are not provided in the source.
* Exact confirmation messages, error messages, and rollback steps are not provided in the source.
* The source does not specify whether production must be stopped before performing this action.
* The source does not specify whether additional approvals or role boundaries beyond support access are required.

## Source Lineage

- Candidate IDs: candidate_training_video_remove_tote_from_system
- Source ID: `training_video_day1`
- Source Type: `training_video`
