# Find A Tote By Entering A Location Number On The Container Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_find_a_tote_by_entering_a_location_number_on_the_container_selection_screen_v1` |
| Title | Find A Tote By Entering A Location Number On The Container Selection Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen to look up a tote by entering a location number and identifying the rack or AGV where the tote is located, if it is present in the system.

## When To Use

Use this procedure when an operator needs to locate a tote in the system from a known location number using the Container Selection screen.

## Do Not Use For

* Do not use this runbook to perform tote recovery, swap, remove, or re-add actions.
* Do not use this runbook to remove AGVs or make other control changes in the interface.
* Do not invent additional search or recovery steps if the tote is not found from the entered location number.

## Safety And Operational Notes

* This candidate is based primarily on OCR text in the training material rather than a clearly narrated live demonstration.
* The source packet includes nearby training cautions about where not to click in the interface and warns against removing AGVs on an active system.
* If the tote is not found in the system from the entered location number, stop at the screen result and escalate rather than attempting unsupported follow-on actions.

## Access Or Tools Needed

* Access to the Container Selection screen
* Known location number for the tote

## Related Operational Context

* ctx_training_video_container_selection_screen_overview_v1

## Procedure Steps

### Step 1 — Open the Container Selection screen

**Responsible role:** operator

**Instruction:**
Open the Container Selection screen used for tote or container lookup.

**Expected result:**
The Container Selection screen is visible and ready for lookup activity.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*The Container Selection screen and the area used for location-based tote lookup.*


**Stop or Escalate If:**

* Stop and escalate if the Container Selection screen cannot be accessed.

---

### Step 2 — Enter the location number

**Responsible role:** operator

**Instruction:**
Type the known location number into the location field shown on the Container Selection screen.

**Expected result:**
The entered location number is accepted by the screen as the lookup input.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*The location field on the Container Selection screen where the location number is typed.*


**Stop or Escalate If:**

* Stop and escalate if the location field is not visible or the location number cannot be entered.

---

### Step 3 — Select the rack or AGV result

**Responsible role:** operator

**Instruction:**
Use the screen to select the rack or AGV where the tote is located, if it is in the system.

**Expected result:**
A rack or AGV associated with the entered location number is selected on the screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*The rack or AGV selection area associated with the entered location number.*


**Stop or Escalate If:**

* Stop and escalate if the tote is not found in the system from the entered location number.
* Stop and escalate if the source does not provide a supported follow-on action for the missing result.

---

### Step 4 — Review the tote or container information

**Responsible role:** operator

**Instruction:**
Review the selected result for the tote or container information shown on the screen, including the tote number if displayed.

**Expected result:**
The operator can identify the tote or container information associated with the selected rack or AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*The selected result details, including any tote number, box icon, location, logic ID, layer count, or container fields shown on the screen.*


**Stop or Escalate If:**

* Stop and escalate if the selected result does not clearly identify the tote or container.
* Stop and escalate if additional follow-on actions are needed, because the source does not provide them.

---

## Success Criteria

* The operator enters a known location number on the Container Selection screen.
* The system shows the rack or AGV where the tote is located, if the tote is in the system.
* The operator can review the displayed tote or container information, including the tote number if shown.

## Failure Conditions

* The Container Selection screen cannot be accessed.
* The location number cannot be entered or is not accepted by the screen.
* The tote is not found in the system from the entered location number.
* The source does not provide supported follow-on actions beyond the lookup and selection steps.

## Escalation Guidance

* If the tote is not found in the system from the entered location number, stop at the screen result and escalate.
* Do not invent additional search, recovery, or correction steps not supported by the source.
* If the interface does not clearly show the tote or container details needed to confirm the result, escalate for further support.

## Missing Details / Known Gaps

* The source does not provide exact control names for the location entry field or selection controls.
* The source does not provide a detailed navigation path to open the Container Selection screen.
* The source does not provide explicit follow-on actions when no tote is found.
* The source does not provide a time estimate for completing the lookup.
* The source evidence is primarily OCR-based rather than a fully narrated step-by-step demonstration.

## Source Lineage

- Candidate IDs: candidate_training_video_find_tote_by_location_on_container_selection_screen
- Source ID: `training_video_day1`
- Source Type: `training_video`
