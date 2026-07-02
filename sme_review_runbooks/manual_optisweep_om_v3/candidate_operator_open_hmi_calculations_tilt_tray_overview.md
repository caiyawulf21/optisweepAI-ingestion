# Open the HMI Calculations Tilt Tray Overview Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_the_hmi_calculations_tilt_tray_overview_screen_v1` |
| Title | Open the HMI Calculations Tilt Tray Overview Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Access the HMI Calculations screen from the ACB System screen to view Tilt Tray overview information, including system operations, bin statistics, and tipper statistics.

## When To Use

Use this procedure when an operator needs to open the HMI Calculations screen from the ACB System screen to view Tilt Tray overview information and related operational statistics.

## Do Not Use For

* Do not use this procedure for recovery if the HMI Calculations screen does not open, because the source does not provide alternate navigation or recovery steps.
* Do not use this procedure for accessing other HMI screens such as Statistics, API, Building Overview, or Tipping Station screens.

## Safety And Operational Notes

* This source describes an HMI navigation action only.
* No lockout/tagout, production stop, or physical intervention requirements are stated in the source.

## Access Or Tools Needed

* Access to the HMI
* ACB System screen

## Related Operational Context

* ctx_manual_hmi_calculations_screen_reference_v1
* ctx_manual_hmi_calculations_navigation_reference_v1

## Procedure Steps

### Step 1 — Start at the ACB System screen

**Responsible role:** operator

**Instruction:**
Go to the "ACB System" screen before attempting to open HMI Calculations.

**Expected result:**
The ACB System screen is displayed and ready for screen selection.

**Screens / Images:**

![artifact_fig_4_1_acb_system_overview_screen](assets/artifact_fig_4_1_acb_system_overview_screen.jpeg)

*The ACB System overview screen used as the starting point for navigation.*

![artifact_page_31_image_2](assets/artifact_page_31_image_2.jpeg)

*System HMI screen associated with the ACB System overview and status display.*


**Stop or Escalate If:**

* Stop or escalate if the ACB System screen cannot be reached or confirmed.

---

### Step 2 — Press HMI CALCULATIONS

**Responsible role:** operator

**Instruction:**
On the ACB System screen, press "HMI CALCULATIONS" to access the Tilt Tray overview screen.

**Expected result:**
The HMI Calculations screen opens.

**Screens / Images:**

![artifact_fig_4_6_hmi_calculations_screen](assets/artifact_fig_4_6_hmi_calculations_screen.jpeg)

*The HMI Calculations screen that is opened from the ACB System screen.*


**Stop or Escalate If:**

* Escalate if the HMI Calculations screen does not open from the ACB System screen as documented.

---

### Step 3 — Verify the HMI Calculations screen is displayed

**Responsible role:** operator

**Instruction:**
Verify that the displayed screen is the "HMI Calculations" screen and that it presents information related to system operations, bin statistics, and tipper statistics.

**Expected result:**
The displayed screen matches the HMI Calculations screen.

**Screens / Images:**

![artifact_fig_4_6_hmi_calculations_screen](assets/artifact_fig_4_6_hmi_calculations_screen.jpeg)

*Figure 4-6 HMI Calculations screen and the information it displays for system operations, bin statistics, and tipper statistics.*


**Stop or Escalate If:**

* Stop or escalate if the displayed screen is not the HMI Calculations screen.
* Stop or escalate if the expected HMI Calculations information is not available.
* Escalate if additional recovery or alternate navigation is needed, because the source does not provide it.

---

## Success Criteria

* The HMI Calculations screen opens from the ACB System screen.
* The operator can view Tilt Tray overview information.
* The displayed screen shows information pertaining to system operations, bin statistics, and tipper statistics.

## Failure Conditions

* The ACB System screen cannot be confirmed as the starting screen.
* The HMI Calculations screen does not open from the ACB System screen as documented.
* The displayed screen is not the HMI Calculations screen.
* The source provides no alternate navigation or recovery steps.

## Escalation Guidance

* Escalate if the HMI Calculations screen does not open from the ACB System screen as documented.
* Escalate if the displayed screen does not match the HMI Calculations screen.
* Escalate when alternate navigation or recovery is required, because the source does not provide additional recovery steps.

## Missing Details / Known Gaps

* The source wording for the navigation instruction is awkward and does not provide a more detailed button-by-button sequence beyond pressing HMI CALCULATIONS from the ACB System screen.
* The source does not provide alternate navigation, troubleshooting, or recovery steps if the screen does not open.
* The source does not provide an estimated completion time.
* The source does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_operator_open_hmi_calculations_tilt_tray_overview
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
