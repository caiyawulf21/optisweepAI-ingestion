# Select A Container Location To View Tote Details

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_select_a_container_location_to_view_tote_details_v1` |
| Title | Select A Container Location To View Tote Details |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen to select a location and view the associated box icon and tote number.

## When To Use

Use when viewing the Container Selection screen and you need to identify or confirm the tote associated with a selected location. The source states that selecting a location shows a box icon and the tote number.

## Do Not Use For

* Do not use this procedure to assume additional container details beyond the box icon and tote number unless they are shown on the source screen.
* Do not use this procedure as navigation guidance to reach the Container Selection screen; the source does not provide the navigation path or exact control names.

## Safety And Operational Notes

* Use only the viewing and selection behavior supported by the source.
* Do not infer or act on unsupported controls or additional container metadata not shown in the source evidence.

## Access Or Tools Needed

* Access to the Container Selection screen

## Related Operational Context

* ctx_training_video_container_selection_screen_v1

## Procedure Steps

### Step 1 — View the Container Selection screen

**Responsible role:** operator

**Instruction:**
Open or view the Container Selection screen.

**Expected result:**
The Container Selection screen is visible and available for location selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Container Selection screen with selectable locations or positions.*


**Stop or Escalate If:**

* Stop or seek support if the Container Selection screen is not available.

---

### Step 2 — Select the desired location

**Responsible role:** operator

**Instruction:**
Select the desired location on the Container Selection screen.

**Expected result:**
The system accepts the location selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Selectable location on the Container Selection screen.*


**Stop or Escalate If:**

* Escalate or seek support if selecting a location does not show the expected box icon or tote number.

---

### Step 3 — Confirm the box icon appears

**Responsible role:** operator

**Instruction:**
Observe whether a box icon appears after the selection.

**Expected result:**
A box icon appears for the selected location.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Source frame showing the box icon displayed after a location is selected.*


**Stop or Escalate If:**

* Escalate or seek support if the box icon does not appear after selecting a location.

---

### Step 4 — Read the tote number

**Responsible role:** operator

**Instruction:**
Read the tote number shown for the selected location.

**Expected result:**
The tote number for the selected location is visible and can be read.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Displayed tote number associated with the selected location.*


**Stop or Escalate If:**

* Escalate or seek support if the tote number does not appear after selecting a location.

---

### Step 5 — Use the displayed location and tote information for confirmation

**Responsible role:** operator

**Instruction:**
Use the displayed tote number and selected location information for identification or confirmation.

**Expected result:**
The operator has the selected location and tote number available for confirmation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Selected location result showing the box icon and tote number.*


**Stop or Escalate If:**

* Do not proceed based on assumed details beyond the box icon and tote number unless they are shown in the source-supported screen.
* Escalate or seek support if the displayed information does not match the expected selected location result.

---

## Success Criteria

* A location is selected on the Container Selection screen.
* A box icon appears for the selected location.
* The tote number associated with the selected location is displayed and readable.

## Failure Conditions

* The Container Selection screen cannot be viewed.
* Selecting a location does not show the expected box icon.
* Selecting a location does not show the tote number.
* Additional details are needed but are not shown in the source-supported screen.

## Escalation Guidance

* Escalate or seek support if selecting a location does not show the expected box icon or tote number.
* Do not assume additional container details beyond the box icon and tote number unless they are shown in the source.

## Missing Details / Known Gaps

* The source does not specify the navigation path to open the Container Selection screen.
* The source does not provide exact control names for the selectable location.
* The source does not define what to do beyond seeking support if the box icon or tote number does not appear.
* The source does not provide a time estimate for completing this procedure.
* The source does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_view_container_details_from_selected_location
- Source ID: `training_video_day1`
- Source Type: `training_video`
