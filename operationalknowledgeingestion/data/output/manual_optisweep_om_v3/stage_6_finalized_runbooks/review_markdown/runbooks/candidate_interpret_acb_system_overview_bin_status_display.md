# View Bin Statuses on the ACB System Overview Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_bin_statuses_on_the_acb_system_overview_screen_v1` |
| Title | View Bin Statuses on the ACB System Overview Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the ACB System overview screen in the System HMI to view the tilt-tray system layout and the color-coded status of each bin.

## When To Use

Use this reference procedure when an operator needs to access the ACB System overview screen and view the tilt-tray layout together with the color-coded status presentation for each bin.

## Do Not Use For

* Do not use this procedure to assign undocumented meanings to specific colors, because this source section states only that statuses are color-coded.
* Do not use this procedure if the required ACB System overview screen is not available or does not display the tilt-tray layout or bin status indications as described.

## Safety And Operational Notes

* This candidate is marked support safe.
* Use only the documented display concept from the source; do not infer or assign unsupported meanings to specific colors.

## Access Or Tools Needed

* Access to the System HMI
* ACB System overview screen

## Related Operational Context

* ctx_manual_system_hmi_overview_screens_v1
* ctx_manual_smalls_color_coded_status_reference_v1

## Procedure Steps

### Step 1 — Open the ACB System overview screen

**Responsible role:** operator

**Instruction:**
On the System HMI, press "SMALLS," select "ACB" from the drop-down menu, then select "ACB1 - AMT TT" to open the ACB System overview screen.

**Expected result:**
The ACB System overview screen opens.

**Screens / Images:**

![artifact_page_31_image_2](assets/artifact_page_31_image_2.jpeg)

*The System HMI screen associated with the ACB System overview screen and the documented navigation path.*

![artifact_fig_4_1_acb_system_overview_screen](assets/artifact_fig_4_1_acb_system_overview_screen.jpeg)

*The ACB System Overview interface that should appear after navigation.*


**Stop or Escalate If:**

* The ACB System overview screen does not display as described.

---

### Step 2 — Observe the tilt-tray system layout

**Responsible role:** operator

**Instruction:**
Observe the displayed ACB System overview screen and review the tilt-tray system layout shown on the screen.

**Expected result:**
The tilt-tray system layout is visible on the ACB System overview screen.

**Screens / Images:**

![artifact_fig_4_1_acb_system_overview_screen](assets/artifact_fig_4_1_acb_system_overview_screen.jpeg)

*The overall tilt-tray system layout shown on the ACB System Overview screen.*

![artifact_page_31_image_2](assets/artifact_page_31_image_2.jpeg)

*The overview display associated with the ACB System screen showing system status information.*


**Stop or Escalate If:**

* The ACB System overview screen does not display the tilt-tray layout as described.

---

### Step 3 — Identify the color-coded status for each bin

**Responsible role:** operator

**Instruction:**
Review the bins shown on the ACB System overview screen and identify the color-coded status displayed for each bin.

**Expected result:**
Each bin on the overview screen shows a color-coded status indication.

**Screens / Images:**

![artifact_fig_4_1_acb_system_overview_screen](assets/artifact_fig_4_1_acb_system_overview_screen.jpeg)

*Bins on the ACB System Overview screen and their displayed color-coded status indications.*

![artifact_fig_4_2_acb_system_overview_screen_legend](assets/artifact_fig_4_2_acb_system_overview_screen_legend.jpeg)

*The legend associated with the ACB System Overview screen for indicator reference.*


**Stop or Escalate If:**

* The screen does not display color-coded status indications for each bin.
* You need to assign a specific meaning to a color that is not documented in this source section.

---

### Step 4 — Compare the displayed bin indications across the screen

**Responsible role:** operator

**Instruction:**
Compare the displayed bin indications across the ACB System overview screen to understand the current status presentation of each bin, using only the source-provided color-coded display concept.

**Expected result:**
The operator can review the current screen-wide presentation of bin statuses without applying unsupported interpretations.

**Screens / Images:**

![artifact_page_31_image_2](assets/artifact_page_31_image_2.jpeg)

*The overall ACB System overview display showing system status information across the screen.*

![artifact_fig_4_1_acb_system_overview_screen](assets/artifact_fig_4_1_acb_system_overview_screen.jpeg)

*The full ACB System Overview screen for comparing bin indications across the layout.*


**Stop or Escalate If:**

* The ACB System overview screen does not display the tilt-tray layout or bin status indications as described.
* A decision would require assigning undocumented meanings to specific colors.

---

## Success Criteria

* The ACB System overview screen is opened using the documented System HMI path.
* The tilt-tray system layout is visible on the screen.
* The color-coded status of each bin is visible on the screen.
* The operator can compare displayed bin indications across the overview without relying on unsupported color interpretations.

## Failure Conditions

* The ACB System overview screen does not open.
* The tilt-tray system layout is not displayed.
* Bin status indications are not shown as described.
* Specific color meanings are needed but are not documented in this source section.

## Escalation Guidance

* Stop and escalate if the ACB System overview screen does not display the tilt-tray layout or bin status indications as described.
* Escalate if interpretation depends on specific color meanings not documented in this source section.

## Missing Details / Known Gaps

* The supplied source section does not define the meaning of individual colors for bin status.
* The supplied source packet does not provide an estimated completion time.
* The supplied source packet does not specify whether production stop or LOTO is required.
* The supplied source section does not provide commands for this procedure.

## Source Lineage

- Candidate IDs: candidate_interpret_acb_system_overview_bin_status_display
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
