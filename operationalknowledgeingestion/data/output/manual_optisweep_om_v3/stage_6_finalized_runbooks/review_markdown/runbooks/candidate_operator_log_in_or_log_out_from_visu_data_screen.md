# Log In Or Log Out From The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_log_in_or_log_out_from_the_visu_data_screen_v1` |
| Title | Log In Or Log Out From The VISU_DATA Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the VISU_DATA screen on the operator station HMI to log in to the operator station or log out the currently logged-in user, then verify the displayed user ID reflects the intended session state.

## When To Use

Use this procedure when an operator needs to change the active user session at the operator station using the VISU_DATA screen LOGIN or LOGOUT controls and verify the displayed current user ID.

## Do Not Use For

* Do not use this runbook for credential-entry instructions or alternate login methods; the source does not provide those details.
* Do not use this runbook for maintenance or admin-only parameter changes; the source packet does not support those actions here.

## Safety And Operational Notes

* This source describes an HMI interaction and does not specify lockout/tagout requirements.
* Do not assume credential prompts, alternate login paths, or additional controls beyond those shown on the VISU_DATA screen.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen

**Responsible role:** operator

**Instruction:**
Open or navigate to the VISU_DATA screen on the operator station HMI.

**Expected result:**
The VISU_DATA screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen-navigation controls and the Visu_Data mapping used to access the VISU_DATA screen.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Overall VISU_DATA screen layout, including the LOGIN button, LOGOUT button, and current user ID field.*


**Stop or Escalate If:**

* Stop or escalate if the VISU_DATA screen cannot be opened.
* Stop or escalate if the expected LOGIN, LOGOUT, or current user ID display is not present.

---

### Step 2 — Locate the current user ID display

**Responsible role:** operator

**Instruction:**
Locate the displayed current user ID on the VISU_DATA screen.

**Expected result:**
The operator can identify the user ID field that shows the currently logged-in user.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The display area showing the ID of the user currently logged in.*


**Stop or Escalate If:**

* Stop or escalate if the current user ID field cannot be found on the VISU_DATA screen.

---

### Step 3 — Press LOGIN to log in

**Responsible role:** operator

**Instruction:**
To log in, press the LOGIN button on the VISU_DATA screen.

**Expected result:**
The operator station begins or completes the login action through the LOGIN control.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The LOGIN button and nearby current user ID display on the VISU_DATA screen.*

![artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats](assets/artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats.jpeg)

*Additional VISU_DATA screen context for the data screen layout.*


**Stop or Escalate If:**

* Stop or escalate if pressing LOGIN does not change the displayed session state as expected.
* Stop or escalate if additional credential-entry details are required, since the source does not provide them.

---

### Step 4 — Verify the logged-in user ID

**Responsible role:** operator

**Instruction:**
Verify that the user ID display updates to show the currently logged-in user.

**Expected result:**
The current user ID field reflects the active logged-in user.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The current user ID field after pressing LOGIN.*


**Stop or Escalate If:**

* Stop or escalate if the displayed user ID does not update after pressing LOGIN.
* Stop or escalate if the displayed user ID does not match the intended session state.

---

### Step 5 — Press LOGOUT to log out the current user

**Responsible role:** operator

**Instruction:**
To log out the current user, press the LOGOUT button on the VISU_DATA screen.

**Expected result:**
The operator station begins or completes logout of the currently logged-in user.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The LOGOUT button and nearby current user ID display on the VISU_DATA screen.*

![artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats](assets/artifact_fig_4_21_operator_station_hmi_data_screen_operator_stats.jpeg)

*Additional VISU_DATA screen context for the data screen layout.*


**Stop or Escalate If:**

* Stop or escalate if pressing LOGOUT does not change the displayed session state as expected.

---

### Step 6 — Verify the user session display after logout

**Responsible role:** operator

**Instruction:**
Verify the user session display after logout by checking the current user ID field.

**Expected result:**
The current user ID field reflects the post-logout session state.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The current user ID field after pressing LOGOUT.*


**Stop or Escalate If:**

* Stop or escalate if the current user ID field does not change after pressing LOGOUT.
* Stop or escalate if the displayed session state remains inconsistent with the intended logout result.

---

## Success Criteria

* The VISU_DATA screen is accessible on the operator station HMI.
* The LOGIN and LOGOUT controls are available on the VISU_DATA screen.
* The current user ID field can be viewed.
* After login or logout, the displayed user ID reflects the intended session state.

## Failure Conditions

* The VISU_DATA screen cannot be opened.
* The LOGIN or LOGOUT button is not visible or does not respond as expected.
* The current user ID field cannot be identified.
* Pressing LOGIN or LOGOUT does not change the displayed session state as expected.
* Credential-entry details are needed but are not provided by the source.

## Escalation Guidance

* Escalate if pressing LOGIN or LOGOUT does not change the displayed session state as expected.
* Escalate if the VISU_DATA screen or its current user ID field is unavailable.
* Escalate if additional credential-entry or alternate login-path details are required, because the source does not provide them.

## Missing Details / Known Gaps

* The source does not provide credential-entry details for the LOGIN action.
* The source does not describe the exact post-logout display state beyond using the current user ID field for session indication.
* The source does not provide timing expectations for login or logout completion.
* The source does not specify whether production must be stopped before performing this action.
* The source does not specify lockout/tagout requirements for this HMI action.

## Source Lineage

- Candidate IDs: candidate_operator_log_in_or_log_out_from_visu_data_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
