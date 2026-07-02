# Navigate Directly To Another HMI Screen Using The VISU_MANCONTROL Drop-Down Menu

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_navigate_directly_to_another_hmi_screen_using_the_visu_mancontrol_drop_down_menu_v1` |
| Title | Navigate Directly To Another HMI Screen Using The VISU_MANCONTROL Drop-Down Menu |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the drop-down menu on the VISU_MANCONTROL screen to directly select and open another HMI screen.

## When To Use

Use this procedure when working from the Operator Station HMI VISU_MANCONTROL screen and you need to directly open another HMI screen using the documented screen-selection drop-down menu.

## Do Not Use For

* Do not use this runbook to identify the full list of selectable screen names, because this source section does not enumerate them.
* Do not use this runbook for navigation from HMI screens other than VISU_MANCONTROL unless separately supported by source evidence.

## Safety And Operational Notes

* This runbook is source-supported as a screen navigation action only.
* The VISU_MANCONTROL screen shown in the source is described as the screen seen by personnel logged in as maintenance.

## Access Or Tools Needed

* Operator Station HMI access
* VISU_MANCONTROL screen
* Screen-selection drop-down menu

## Related Operational Context

* ctx_manual_visu_mancontrol_screen_overview_v1

## Procedure Steps

### Step 1 — Open the VISU_MANCONTROL screen

**Responsible role:** L1_support

**Instruction:**
Open the VISU_MANCONTROL screen on the Operator Station HMI.

**Expected result:**
The VISU_MANCONTROL screen is displayed.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The VISU_MANCONTROL screen layout and the screen-selection drop-down menu shown on the manual control screen.*


**Stop or Escalate If:**

* Escalate if the VISU_MANCONTROL screen is not available as documented.

---

### Step 2 — Locate the screen-selection drop-down menu

**Responsible role:** L1_support

**Instruction:**
Locate the drop-down menu on the VISU_MANCONTROL screen that is used to directly select the screen to view.

**Expected result:**
The screen-selection drop-down menu is visible and identifiable on the VISU_MANCONTROL screen.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The screen-selection drop-down on the VISU_MANCONTROL screen, along with the surrounding manual control screen layout.*


**Stop or Escalate If:**

* Escalate if the drop-down menu is not available as documented.

---

### Step 3 — Open the drop-down menu

**Responsible role:** L1_support

**Instruction:**
Open the screen-selection drop-down menu on the VISU_MANCONTROL screen.

**Expected result:**
The drop-down menu opens and displays available screen choices.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The drop-down menu control on the VISU_MANCONTROL screen.*


**Stop or Escalate If:**

* Escalate if the drop-down menu does not open.
* Escalate if the drop-down menu does not allow screen selection as documented.

---

### Step 4 — Select the desired screen

**Responsible role:** L1_support

**Instruction:**
Select the desired screen from the available list in the drop-down menu.

**Expected result:**
The selected HMI screen opens.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*The VISU_MANCONTROL screen area containing the screen-selection drop-down used for direct navigation.*


**Stop or Escalate If:**

* Escalate if the desired screen cannot be selected.
* Escalate if the selected screen does not open.
* Note that this source section does not list the available screen names.

---

## Success Criteria

* The selected HMI screen is opened from the VISU_MANCONTROL screen using the drop-down menu.

## Failure Conditions

* The VISU_MANCONTROL screen is not available.
* The drop-down menu is not available on the VISU_MANCONTROL screen.
* The drop-down menu does not open.
* The drop-down menu does not allow screen selection as documented.
* The source section does not provide the list of available screen names.

## Escalation Guidance

* Escalate if the drop-down menu is not available or does not allow screen selection as documented.
* Escalate if the selected screen does not open from the VISU_MANCONTROL screen.
* If identification of specific selectable screen names is required, escalate because this source section does not enumerate them.

## Missing Details / Known Gaps

* The source section does not enumerate the available screen names in the drop-down menu.
* The source does not provide a time estimate for this navigation task.
* The source does not explicitly state whether production stop or LOTO is required.
* The source does not define additional supporting roles for this action.

## Source Lineage

- Candidate IDs: candidate_l1_navigate_to_hmi_screen_using_visu_mancontrol_dropdown
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
