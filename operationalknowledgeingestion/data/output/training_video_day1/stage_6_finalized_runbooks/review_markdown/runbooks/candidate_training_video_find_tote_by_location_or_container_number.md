# Find A Tote By Entering A Location Number Or Container Number

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_find_a_tote_by_entering_a_location_number_or_container_number_v1` |
| Title | Find A Tote By Entering A Location Number Or Container Number |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen to locate a tote in the system by entering a location number or tote/container number, then identify the rack or AGV where it is located if the system returns a result.

## When To Use

Use this procedure when you need to locate a tote/container in OptiSweep using a known location number or tote/container number and determine the associated rack or AGV location shown by the Container Selection screen.

## Do Not Use For

* Do not use this runbook for tote recovery or reinitialization steps; the source does not provide those actions here.
* Do not use this runbook to remove AGVs or perform other control actions in the interface; the packet includes cautionary source context but not an approved procedure for those actions.
* Do not use this runbook when you do not have a known location number or tote/container number to enter.

## Safety And Operational Notes

* This source supports a lookup/view procedure only.
* The source does not provide recovery actions if the tote is not found in the system.
* Related training context warns against using this interface for removal actions on an active system; this runbook is limited to locating a tote.

## Access Or Tools Needed

* Access to the Container Selection screen
* Known location number or tote/container number

## Related Operational Context

* ctx_training_video_container_selection_screen_v1
* ctx_training_video_container_search_reference_v1

## Procedure Steps

### Step 1 — Open or view the Container Selection screen

**Responsible role:** operator

**Instruction:**
Open or view the Container Selection screen for totes or containers before starting the lookup.

**Expected result:**
The Container Selection screen is visible and ready for lookup activity.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Container Selection screen and the search/entry area used for location number or tote/container number lookup.*


**Stop or Escalate If:**

* Stop or escalate if the Container Selection screen cannot be accessed.

---

### Step 2 — Enter the location number or tote/container number

**Responsible role:** operator

**Instruction:**
Type the known location number or tote/container number into the available entry field on the Container Selection screen.

**Expected result:**
The entered number is accepted in the lookup field.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*The Container Selection screen area used to enter a location number or tote/container number.*


**Stop or Escalate If:**

* Stop or escalate if the interface does not present a usable entry field.
* Stop or escalate if the field label or exact entry location is unclear and additional guidance is needed.

---

### Step 3 — Review whether the tote is returned by the system

**Responsible role:** operator

**Instruction:**
Review the returned result after entry to determine whether the tote is in the system.

**Expected result:**
A result indicates whether the tote is present in the system.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Returned lookup information indicating tote presence and associated location context.*


**Stop or Escalate If:**

* Stop or escalate if the tote is not in the system.
* Stop or escalate if the entered number does not return a usable result.

---

### Step 4 — Select the returned rack or AGV

**Responsible role:** operator

**Instruction:**
Select the rack or AGV associated with the returned result.

**Expected result:**
The selected rack or AGV is highlighted or displayed as the tote location.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*The rack or AGV location associated with the searched tote on the Container Selection screen.*


**Stop or Escalate If:**

* Stop or escalate if the returned result does not identify a selectable rack or AGV.
* Stop or escalate if selecting the result does not show a usable location.

---

### Step 5 — Confirm the displayed tote location

**Responsible role:** operator

**Instruction:**
Confirm the displayed rack or AGV location for the tote.

**Expected result:**
The tote location is identified as a rack or AGV shown by the system.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*The displayed rack or AGV location associated with the searched tote.*


**Stop or Escalate If:**

* Stop or escalate if the displayed rack or AGV location is not usable.
* Escalate if the entered number does not return a usable rack or AGV location and additional guidance is needed.

---

## Success Criteria

* The operator enters a known location number or tote/container number on the Container Selection screen.
* The system returns a result indicating the tote is in the system.
* The associated rack or AGV location can be selected and confirmed.

## Failure Conditions

* The Container Selection screen cannot be accessed.
* The entry field or exact field label is unclear from the source.
* The tote is not in the system.
* The entered number does not return a usable rack or AGV location.

## Escalation Guidance

* Escalate if the tote is not in the system, because the source does not provide further recovery steps.
* Escalate if the entered number does not return a usable rack or AGV location and additional guidance is needed.
* Escalate if the interface does not clearly support the lookup as shown in the training source.

## Missing Details / Known Gaps

* The source does not clearly identify the exact field label used for location number or tote/container number entry.
* The source does not provide explicit navigation steps to reach the Container Selection screen.
* The source does not provide recovery steps when the tote is not found in the system.
* The source does not provide a time estimate for completing the lookup.

## Source Lineage

- Candidate IDs: candidate_training_video_find_tote_by_location_or_container_number
- Source ID: `training_video_day1`
- Source Type: `training_video`
