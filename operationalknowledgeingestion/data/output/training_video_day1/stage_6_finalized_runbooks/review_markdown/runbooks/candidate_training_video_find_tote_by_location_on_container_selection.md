# Find A Tote By Entering A Location Number On the Container Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_find_a_tote_by_entering_a_location_number_on_the_container_selection_screen_v1` |
| Title | Find A Tote By Entering A Location Number On the Container Selection Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen to find a tote by entering a location number, then identify and select the associated rack or AGV when the tote is present in the system.

## When To Use

Use this procedure when you need to look up a tote by location number from the Container Selection screen and determine the rack or AGV associated with that location, if the tote is in the system.

## Do Not Use For

* Do not use this runbook for recovery actions when the tote is not in the system; this source does not provide recovery steps.
* Do not use this runbook for alternate lookup methods not explicitly supported here beyond entering a location number and selecting the associated rack or AGV.

## Safety And Operational Notes

* Use only the documented lookup and selection actions supported by this source.
* This source does not provide further action if no rack or AGV association is returned.

## Access Or Tools Needed

* Access to the Container Selection screen
* Location number to enter
* Ability to select the displayed rack or AGV result

## Related Operational Context

* ctx_training_video_container_location_lookup_v1

## Procedure Steps

### Step 1 — Open or view the Container Selection screen

**Responsible role:** operator

**Instruction:**
Open or view the Container Selection screen before entering the location number.

**Expected result:**
The Container Selection screen is visible and ready for lookup.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*Container Selection screen showing the location number entry field and rack or AGV selection area.*


**Stop or Escalate If:**

* Stop or escalate if the Container Selection screen cannot be accessed.

---

### Step 2 — Enter the location number

**Responsible role:** operator

**Instruction:**
Type the location number into the screen input field.

**Expected result:**
The entered location number is accepted by the screen for lookup.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*The location number entry area on the Container Selection screen.*


**Stop or Escalate If:**

* Stop or escalate if the location number cannot be entered.

---

### Step 3 — Review the returned rack or AGV association

**Responsible role:** operator

**Instruction:**
Review the displayed result to identify the rack or AGV where the tote is located, if it is in the system.

**Expected result:**
A rack or AGV association is visible for the entered location number when the tote is in the system.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*The displayed rack or AGV result associated with the entered location number.*


**Stop or Escalate If:**

* Stop or escalate if the lookup does not return a rack or AGV association.
* Stop or escalate if the tote is not in the system.

---

### Step 4 — Select the shown rack or AGV

**Responsible role:** operator

**Instruction:**
Select the shown rack or AGV associated with the entered location number.

**Expected result:**
The associated rack or AGV is selected.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*The rack or AGV item shown as the lookup result for the entered location number.*


**Stop or Escalate If:**

* Stop or escalate if no rack or AGV can be selected for the entered location number.
* Stop or escalate if the displayed association is unclear.

---

### Step 5 — Confirm the tote location association

**Responsible role:** operator

**Instruction:**
Use the displayed association to confirm the tote location.

**Expected result:**
The tote location is confirmed based on the displayed rack or AGV association.

**Screens / Images:**

![artifact_training_video_training_video_day1_0043_ok_when_we_are_going_through_primary_01_36_09_000](assets/ec07ed178ed088eb.jpg)

*The selected rack or AGV association used to confirm the tote location.*


**Stop or Escalate If:**

* Stop or escalate if the tote location cannot be confirmed from the displayed association.

---

## Success Criteria

* The location number is entered on the Container Selection screen.
* A rack or AGV association is displayed for the tote when it is in the system.
* The operator selects the shown rack or AGV.
* The tote location is confirmed from the displayed association.

## Failure Conditions

* The Container Selection screen cannot be accessed.
* The location number cannot be entered.
* The lookup does not return a rack or AGV association.
* The tote is not in the system.
* The displayed association is unclear or cannot be selected.

## Escalation Guidance

* Escalate or seek clarification if the location number lookup does not return a rack or AGV association.
* If the tote is not in the system, this source does not provide further recovery steps.

## Missing Details / Known Gaps

* The source does not specify navigation steps to reach the Container Selection screen.
* The source does not specify what exact UI response appears after entering the location number.
* The source does not provide recovery steps if the tote is not in the system.
* The source does not define role boundaries beyond operator-level use.
* The source does not provide an estimated completion time.

## Source Lineage

- Candidate IDs: candidate_training_video_find_tote_by_location_on_container_selection
- Source ID: `training_video_day1`
- Source Type: `training_video`
