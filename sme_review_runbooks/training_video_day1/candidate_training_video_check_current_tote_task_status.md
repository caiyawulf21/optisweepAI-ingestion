# Check the Current Status and Task for a Tote

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_current_status_and_task_for_a_tote_v1` |
| Title | Check the Current Status and Task for a Tote |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Get Tote Task function in the tote management API view to retrieve the current tote task and review the tote's current status and task information.

## When To Use

Use when support or operations needs to see the current status of a tote and its assigned task information using the Get Tote Task function shown in the training.

## Do Not Use For

* Do not use for changing tote assignments or exchange behavior; the source only supports viewing current tote task/status information in this procedure.
* Do not use when a corrective interpretation of a mismatched status is required; the source does not provide further interpretation logic in this segment.

## Safety And Operational Notes

* This source describes a status lookup function and does not describe a physical intervention.
* Do not invent corrective actions from the returned status; escalate if the returned status does not match the observed system condition and no interpretation is provided by the source.

## Access Or Tools Needed

* Access to tote management interface or API-backed Get Tote Task function
* Tote identifier

## Related Operational Context

* ctx_training_video_get_tote_task_status_reference_v1
* ctx_training_video_tote_management_api_overview_v1

## Procedure Steps

### Step 1 — Open Get Tote Task in the tote management interface

**Responsible role:** L1_support

**Instruction:**
Open the tote management function for Get Tote Task on the API page shown in the training.

**Expected result:**
The Get Tote Task function is visible and ready to use.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*API Features for Tote Management list showing Get Tote Task on the tote management page.*


**Stop or Escalate If:**

* Escalate if the Get Tote Task function cannot be accessed.

---

### Step 2 — Enter or select the tote to inspect

**Responsible role:** L1_support

**Instruction:**
Enter or select the tote to inspect using the available tote identifier.

**Expected result:**
The target tote is selected for lookup.

**Stop or Escalate If:**

* Escalate if the tote identifier is not available.
* Escalate if the tote cannot be selected for lookup.

---

### Step 3 — Retrieve the tote task information

**Responsible role:** L1_support

**Instruction:**
Retrieve the tote task information for the selected tote.

**Expected result:**
The system returns the current tote task information.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*Get Tote Task function on the tote management API page used to retrieve current tote task information.*


**Stop or Escalate If:**

* Escalate if the tote task information cannot be retrieved.

---

### Step 4 — Review the returned status and task details

**Responsible role:** L1_support

**Instruction:**
Review the returned current status and task details for that tote.

**Expected result:**
The current tote status and task details are visible for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Example tote task detail fields such as Tote ID, AGV ID, Original Destination, Station, Task ID, Task Name, and Tote Error.*


**Stop or Escalate If:**

* Escalate if the returned status does not match the observed system condition and the source provides no further interpretation.
* Escalate if the returned details are missing or cannot be understood from the available source guidance.

---

### Step 5 — Record the observed tote status and task information

**Responsible role:** L1_support

**Instruction:**
Record the observed tote status and task information for troubleshooting or operational follow-up.

**Expected result:**
The observed tote status and task information is documented for later use.

**Stop or Escalate If:**

* Escalate if the returned information cannot be retrieved or is too unclear to document reliably.

---

## Success Criteria

* The Get Tote Task function is accessed.
* A tote is selected using a tote identifier.
* Current tote task information is returned.
* The tote's current status and task details are reviewed.
* The observed status and task information is recorded for troubleshooting or follow-up.

## Failure Conditions

* The Get Tote Task function cannot be accessed.
* The tote cannot be identified or selected.
* The tote task information cannot be retrieved.
* The returned status does not match the observed system condition and the source provides no interpretation.

## Escalation Guidance

* Escalate if the tote task information cannot be retrieved.
* Escalate if the returned status does not match the observed system condition and the source provides no further interpretation.
* Escalate if the Get Tote Task function is unavailable in the accessible interface.

## Missing Details / Known Gaps

* The source does not provide exact button names, field entry mechanics, or submission controls for Get Tote Task.
* The source does not provide a precise navigation path to the tote management API page.
* The source does not provide a time estimate for completing this procedure.
* The source does not define exact output formatting or a required documentation destination for recorded observations.
* The source does not provide interpretation rules for specific tote statuses or task states.

## Source Lineage

- Candidate IDs: candidate_training_video_check_current_tote_task_status
- Source ID: `training_video_day1`
- Source Type: `training_video`
