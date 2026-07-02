# Navigate the Viva Main Overview and Open Subscreens

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_navigate_the_viva_main_overview_and_open_subscreens_v1` |
| Title | Navigate the Viva Main Overview and Open Subscreens |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Viva main overview screen as the home screen for system overview and navigation. From this screen, the operator can review the overall layout, use the Main Menu to open listed subscreens, and click available layout icons for more information on system areas.

## When To Use

Use when an operator needs to start from the Viva home overview screen, review overall system visibility, navigate to the listed subscreens, or open more information for the Tippers, Hospital, or GLDS areas from the system layout.

## Do Not Use For

* Do not use for navigation paths beyond the Main Menu items and clickable icons explicitly named in the source.
* Do not use as a corrective or troubleshooting procedure beyond the source-provided tip to click "ACB1— AMR TT" if a subscreen does not update.
* Do not assume additional actions, controls, or follow-on behavior not described in the source.

## Safety And Operational Notes

* This source-supported procedure is limited to viewing and navigation actions on the Viva overview screen.
* Do not assume additional control actions from the overview beyond what is explicitly described in this runbook.

## Access Or Tools Needed

* Access to the Viva HMI main overview screen
* Main Menu on the Viva overview
* Clickable system layout icons for Tippers, Hospitals, and GLDS

## Related Operational Context

* ctx_training_video_viva_main_overview_v1
* ctx_training_video_viva_main_menu_navigation_v1
* ctx_training_video_viva_system_layout_components_v1

## Procedure Steps

### Step 1 — Open or view the Viva main overview screen

**Responsible role:** operator

**Instruction:**
Open or view the Viva main overview screen identified in the source as the home screen for system overview and navigation.

**Expected result:**
The Viva main overview screen is visible and can be used as the starting point for navigation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*The Viva overall system main overview screen used as the home screen.*


**Stop or Escalate If:**

* Stop or escalate if the Viva main overview screen cannot be accessed or identified from the available display.

---

### Step 2 — Use the Main Menu to open listed subscreens

**Responsible role:** operator

**Instruction:**
Use the Main Menu on the Viva overview to navigate to the available subscreens listed in the source: Detail, Statistics, HMI Calculations, API, and RMS.

**Expected result:**
The selected subscreen opens from the Main Menu.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*The Main Menu area showing the listed subscreen options: Detail, Statistics, HMI Calculations, API, and RMS.*


**Stop or Escalate If:**

* Stop or escalate if the expected subscreen does not open after selecting a listed Main Menu option.

---

### Step 3 — Review the system layout area

**Responsible role:** operator

**Instruction:**
Review the system layout area on the Viva overview and identify the areas shown in the source: Sorter, Tippers, Hospital, and GLDS.

**Expected result:**
The operator can see the system layout and identify the named areas.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*The system layout area showing Sorter, Tippers, Hospital, and GLDS.*


**Stop or Escalate If:**

* Stop or escalate if the overview does not show the expected system layout areas.

---

### Step 4 — Click layout icons to open more information

**Responsible role:** operator

**Instruction:**
Click the icons for Tippers, Hospitals, or GLDS on the system layout to open more information for those areas.

**Expected result:**
More information opens for the selected Tippers, Hospital, or GLDS area.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*The system layout icons for Tippers, Hospital, and GLDS that can be clicked for more information.*


**Stop or Escalate If:**

* Stop or escalate if clicking a supported icon does not open more information.

---

### Step 5 — Use the source-provided refresh tip if a subscreen does not update

**Responsible role:** operator

**Instruction:**
If a subscreen does not update, click "ACB1— AMR TT" as noted in the source tip.

**Expected result:**
The subscreen updates after using the source-provided tip.

**Stop or Escalate If:**

* Stop or escalate if the expected subscreen does not update after clicking "ACB1— AMR TT."

---

## Success Criteria

* The Viva main overview is used as the starting screen for system overview and navigation.
* The operator can open the listed Main Menu subscreens: Detail, Statistics, HMI Calculations, API, and RMS.
* The operator can identify the system layout areas: Sorter, Tippers, Hospital, and GLDS.
* The operator can click supported layout icons to open more information for Tippers, Hospital, or GLDS.

## Failure Conditions

* The Viva main overview screen cannot be accessed or identified.
* A listed Main Menu subscreen does not open.
* The system layout or named areas are not visible.
* Clicking a supported icon does not open more information.
* The subscreen still does not update after clicking "ACB1— AMR TT."

## Escalation Guidance

* If the expected subscreen does not update after using the source-provided tip, escalate for additional support.
* Escalate if the operator cannot access the Viva main overview or cannot open the listed subscreens.
* Escalate if the displayed behavior requires navigation or corrective actions not described in the source.

## Missing Details / Known Gaps

* The source does not provide a time estimate for this procedure.
* The source does not specify whether production stop or LOTO is required.
* The source does not explain why clicking "ACB1— AMR TT" refreshes the subscreen or what internal behavior follows.
* The source does not define additional troubleshooting steps if the subscreen still does not update.
* The source does not identify supporting roles or approval requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_navigate_viva_main_overview_and_subscreens
- Source ID: `training_video_day1`
- Source Type: `training_video`
