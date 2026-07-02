# Add a Tote Back to the System Using a Station ID

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_add_a_tote_back_to_the_system_using_a_station_id_v1` |
| Title | Add a Tote Back to the System Using a Station ID |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the tote management API function to add a specified tote back into the system and associate it with a destination station ID. The source states that the station ID can be identified in RMS by selecting the relevant cell, and that the tote management page includes an Add Tote function.

## When To Use

Use when a tote needs to be re-added or placed back into the system and the intended destination station must be specified by station ID.

## Do Not Use For

* Do not use when the correct station ID cannot be confirmed in RMS.
* Do not use as a substitute for procedures requiring exact field names, exact UI sequence, or explicit success indicators, because those details are not provided in this source.

## Safety And Operational Notes

* This action changes live tote state in the system.
* Use the correct station ID before submitting the add action.
* Escalate if the correct station ID cannot be confirmed in RMS.

## Access Or Tools Needed

* Access to tote management interface or API-backed tote add function
* RMS access to view station IDs
* Tote identifier and target station ID

## Related Operational Context

* ctx_training_video_tote_management_api_overview_v1
* ctx_training_video_station_id_reference_for_totes_v1

## Procedure Steps

### Step 1 — Identify the tote to add back

**Responsible role:** L1_support

**Instruction:**
Identify the tote that needs to be added back into the system.

**Expected result:**
A specific tote has been identified for the add action.

**Stop or Escalate If:**

* Stop and escalate if the tote cannot be clearly identified.

---

### Step 2 — Confirm the destination station ID in RMS

**Responsible role:** L1_support

**Instruction:**
Determine the correct station ID for that tote by checking RMS and selecting the relevant cell to view the station ID.

**Expected result:**
The correct station ID is confirmed for the tote destination.

**Stop or Escalate If:**

* Escalate if the correct station ID cannot be confirmed in RMS.

---

### Step 3 — Open the Add Tote function

**Responsible role:** L1_support

**Instruction:**
Open the tote management function that allows a tote to be added to the system.

**Expected result:**
The Add Tote function is available for data entry.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The API Features for Tote Management list showing Add Tote among the available functions.*


**Stop or Escalate If:**

* Stop and escalate if the Add Tote function cannot be located or accessed.

---

### Step 4 — Enter tote information and station ID

**Responsible role:** L1_support

**Instruction:**
Enter the tote information and specify the station ID for the destination station.

**Expected result:**
The tote information and destination station ID are entered into the add function.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management API page context showing Add Tote as the function used for this action.*


**Stop or Escalate If:**

* Escalate if the correct station ID cannot be confirmed.
* Stop and escalate if the source-provided interface does not make the required entry fields clear.

---

### Step 5 — Submit and verify tote association

**Responsible role:** L1_support

**Instruction:**
Submit the add action and verify in the available interface that the tote is now associated with the intended station.

**Expected result:**
The specified tote is added to the system and associated with the intended station ID.

**Stop or Escalate If:**

* Escalate if the tote cannot be added.
* Escalate if the tote does not appear at the intended station after submission.
* Escalate if the interface does not provide a clear success indicator.

---

## Success Criteria

* The specified tote is added to the system.
* The tote is associated with the intended station ID.
* The association can be verified in an available interface.

## Failure Conditions

* The correct station ID cannot be confirmed in RMS.
* The Add Tote function cannot be accessed.
* The tote cannot be added.
* The tote does not appear at the intended station after submission.
* The source does not provide exact field names or explicit success indicators.

## Escalation Guidance

* Escalate if the correct station ID cannot be confirmed in RMS.
* Escalate if the tote cannot be added or does not appear at the intended station after submission.
* Escalate if the interface does not provide enough detail to determine the correct fields or success state.

## Missing Details / Known Gaps

* The source does not provide the exact UI sequence for opening and using Add Tote.
* The source does not provide exact field names for the Add Tote function.
* The source does not provide explicit success message text or exact success indicators.
* The source does not provide a time estimate for completing this procedure.
* The source does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_add_tote_to_station_by_station_id
- Source ID: `training_video_day1`
- Source Type: `training_video`
