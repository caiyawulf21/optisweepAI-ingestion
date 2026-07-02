# Open the ACB System Overview Screen in the System HMI

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_the_acb_system_overview_screen_in_the_system_hmi_v1` |
| Title | Open the ACB System Overview Screen in the System HMI |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Access the ACB System overview screen in the System HMI to view the tilt-tray system layout and the color-coded status of each bin.

## When To Use

Use this procedure when you need to navigate within the System HMI to the ACB System overview screen and confirm the tilt-tray system layout and color-coded bin status display.

## Access Or Tools Needed

* Access to the System HMI

## Related Operational Context

* ctx_manual_system_hmi_overview_screens_v1

## Procedure Steps

### Step 1 — Open the System HMI

**Responsible role:** L1_support

**Instruction:**
Open the System HMI.

**Expected result:**
The System HMI is open and available for navigation.

**Screens / Images:**

![artifact_page_31_image_2](assets/artifact_page_31_image_2.jpeg)

*Reference the ACB System overview-related System HMI screen artifact to confirm you are working within the correct HMI context.*


**Stop or Escalate If:**

* The System HMI is not available or cannot be opened.

---

### Step 2 — Press SMALLS

**Responsible role:** L1_support

**Instruction:**
Press "SMALLS".

**Expected result:**
The HMI advances into the SMALLS area or menu path.

**Screens / Images:**

![artifact_fig_4_4_smalls_system_overview_screen](assets/artifact_fig_4_4_smalls_system_overview_screen.jpeg)

*Use the Smalls System Overview Screen artifact as a reference for the SMALLS area reached through this navigation path.*


**Stop or Escalate If:**

* The documented menu options are not available in the System HMI.

---

### Step 3 — Select ACB from the drop-down menu

**Responsible role:** L1_support

**Instruction:**
Select "ACB" from the drop-down menu.

**Expected result:**
The ACB option is selected and the ACB-specific options are available.

**Stop or Escalate If:**

* The documented menu options are not available in the System HMI.

---

### Step 4 — Select ACB1 - AMT TT

**Responsible role:** L1_support

**Instruction:**
Select "ACB1 - AMT TT" from the options.

**Expected result:**
The ACB1 - AMT TT selection is accepted and the ACB System overview screen opens.

**Stop or Escalate If:**

* The documented menu options or screen names are not available in the System HMI.
* The ACB System overview screen does not display after following the documented navigation path.

---

### Step 5 — Verify the ACB System overview screen is displayed

**Responsible role:** L1_support

**Instruction:**
Verify that the ACB System overview screen is displayed and shows the tilt-tray system layout with a color-coded status of each bin.

**Expected result:**
The ACB System overview screen is open and displays the tilt-tray system layout and color-coded bin statuses.

**Screens / Images:**

![artifact_page_31_image_2](assets/artifact_page_31_image_2.jpeg)

*Compare the displayed screen to the ACB System overview-related screen artifact showing system status information.*

![artifact_fig_4_1_acb_system_overview_screen](assets/artifact_fig_4_1_acb_system_overview_screen.jpeg)

*Use Figure 4-1 to confirm the ACB System Overview interface is the screen currently displayed.*

![artifact_fig_4_2_acb_system_overview_screen_legend](assets/artifact_fig_4_2_acb_system_overview_screen_legend.jpeg)

*Use the legend to interpret indicators and color-coded status elements shown on the ACB System overview screen.*


**Stop or Escalate If:**

* The ACB System overview screen does not display after following the documented navigation path.

---

## Success Criteria

* The ACB System overview screen is open.
* The displayed screen shows the tilt-tray system layout.
* The displayed screen shows a color-coded status of each bin.

## Failure Conditions

* The documented menu options or screen names are not available in the System HMI.
* The ACB System overview screen does not display after following the documented navigation path.
* The displayed screen does not show the tilt-tray system layout and color-coded status of each bin.

## Escalation Guidance

* Escalate if the documented menu options or screen names are not available in the System HMI.
* Escalate if the ACB System overview screen does not display after following the documented navigation path.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not specify whether production stop is required.
* The source does not specify whether lockout/tagout is required.
* The source does not define role boundaries beyond the candidate's inferred L1_support role.
* The source does not provide explicit recovery actions if the screen or menu options are unavailable.

## Source Lineage

- Candidate IDs: candidate_l1_access_acb_system_overview_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
