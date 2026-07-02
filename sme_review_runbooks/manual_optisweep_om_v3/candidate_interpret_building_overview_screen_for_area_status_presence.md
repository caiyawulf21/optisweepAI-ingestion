# Check Building Overview Screen for Facility Area Status Display

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_building_overview_screen_for_facility_area_status_display_v1` |
| Title | Check Building Overview Screen for Facility Area Status Display |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Building Overview screen to verify that the facility layout is displayed and that each shown area has a color-coded status indication. This runbook is limited to confirming screen presence and recording displayed colors; it does not define color meanings.

## When To Use

Use when an operator needs to confirm that the Building Overview HMI screen is accessible, shows the layout of the entire facility, and presents a color-coded status for each area.

## Do Not Use For

* Do not use this runbook to infer the meaning of any displayed color from this source section alone.
* Do not use this runbook for corrective action or troubleshooting beyond confirming whether the Building Overview screen displays the facility layout and area-level color-coded status.

## Safety And Operational Notes

* This source supports screen observation only.
* Do not infer the meaning of any color from this section alone.

## Access Or Tools Needed

* Access to the system HMI
* Building Overview screen

## Related Operational Context

* ctx_manual_building_overview_screen_v1

## Procedure Steps

### Step 1 — Open the Building Overview screen

**Responsible role:** operator

**Instruction:**
Press OVERVIEW to access the "Building Overview" screen.

**Expected result:**
The Building Overview screen opens on the HMI.

**Screens / Images:**

![artifact_fig_4_3_building_overview_screen](assets/artifact_fig_4_3_building_overview_screen.png)

*Use the figure as the reference image for the Building Overview screen that should appear after pressing OVERVIEW.*


**Stop or Escalate If:**

* Escalate if the Building Overview screen does not display as described.

---

### Step 2 — Confirm the facility layout is displayed

**Responsible role:** operator

**Instruction:**
Identify the facility layout displayed on the Building Overview screen.

**Expected result:**
The screen shows the layout of the entire facility.

**Screens / Images:**

![artifact_fig_4_3_building_overview_screen](assets/artifact_fig_4_3_building_overview_screen.png)

*Review the overall facility layout shown in the Building Overview screen figure.*


**Stop or Escalate If:**

* Escalate if the Building Overview screen does not display the facility layout as described.

---

### Step 3 — Locate the displayed facility areas

**Responsible role:** operator

**Instruction:**
Locate the individual areas shown within the facility layout.

**Expected result:**
The operator can identify the displayed areas on the Building Overview screen.

**Screens / Images:**

![artifact_fig_4_3_building_overview_screen](assets/artifact_fig_4_3_building_overview_screen.png)

*Identify the separate areas shown within the facility layout on the Building Overview screen.*


**Stop or Escalate If:**

* Escalate if the displayed layout does not show identifiable facility areas.

---

### Step 4 — Verify color-coded status is shown for each area

**Responsible role:** operator

**Instruction:**
Check whether each displayed area has a color-coded status indication associated with it.

**Expected result:**
Each displayed area shows a color-coded status indication.

**Screens / Images:**

![artifact_fig_4_3_building_overview_screen](assets/artifact_fig_4_3_building_overview_screen.png)

*Look for the color-coded status indications associated with each displayed area on the Building Overview screen.*


**Stop or Escalate If:**

* Escalate if the Building Overview screen does not display area-level color-coded status as described.
* Stop if interpretation of color meaning is required, because this source section does not define color meanings.

---

### Step 5 — Record displayed area status colors if needed

**Responsible role:** operator

**Instruction:**
Record the observed area status colors exactly as displayed if documentation or support personnel need the current screen state.

**Expected result:**
Observed area status colors are documented exactly as displayed on the screen.

**Screens / Images:**

![artifact_fig_4_3_building_overview_screen](assets/artifact_fig_4_3_building_overview_screen.png)

*Use the Building Overview screen figure as the reference for the facility layout and area color presentation to be recorded.*


**Stop or Escalate If:**

* Escalate if the Building Overview screen does not display the facility layout or area-level color-coded status as described.
* Stop if asked to assign meaning to the colors using this source section alone.

---

## Success Criteria

* The Building Overview screen is accessible from the HMI by pressing OVERVIEW.
* The screen shows the layout of the entire facility.
* Each displayed area has a color-coded status indication.
* If needed, the currently displayed area status colors are recorded exactly as shown.

## Failure Conditions

* The Building Overview screen does not open after pressing OVERVIEW.
* The screen does not show the layout of the entire facility.
* Displayed facility areas cannot be identified.
* One or more displayed areas do not show a color-coded status indication.
* The procedure requires interpretation of color meaning not provided by this source.

## Escalation Guidance

* Escalate if the Building Overview screen does not display the facility layout or area-level color-coded status as described.
* Escalate if the screen cannot be accessed by pressing OVERVIEW.
* Do not infer the meaning of any color from this section alone; seek additional approved reference or support if interpretation is required.

## Missing Details / Known Gaps

* The source does not define the meaning of the displayed colors.
* The source does not provide corrective actions if an area is missing a color-coded status.
* The source does not provide an estimated completion time.
* The source does not specify whether production stop or LOTO is required.
* The source does not define role boundaries beyond operator access to the HMI.

## Source Lineage

- Candidate IDs: candidate_interpret_building_overview_screen_for_area_status_presence
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
