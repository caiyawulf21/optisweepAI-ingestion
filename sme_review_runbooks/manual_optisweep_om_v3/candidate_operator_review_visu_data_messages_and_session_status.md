# Review VISU_DATA Banner Messages And Current Login Status

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_review_visu_data_banner_messages_and_current_login_status_v1` |
| Title | Review VISU_DATA Banner Messages And Current Login Status |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the VISU_DATA screen on the operator station HMI to review alarm or informational banner messages, navigate through available messages with the banner arrows, and verify which user ID is currently logged in.

## When To Use

Use when an operator needs to check alarm or informational messages shown on the VISU_DATA screen and confirm the current logged-in user ID at the operator station.

## Do Not Use For

* Correcting banner message conditions or faults, because no corrective action is provided in the source.
* Changing login state or user permissions beyond viewing the displayed current user ID.

## Safety And Operational Notes

* This runbook is limited to viewing screen information on the operator station HMI.
* No corrective action, reset action, or maintenance action is provided by the source for this procedure.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1

## Procedure Steps

### Step 1 — Navigate to the VISU_DATA screen

**Responsible role:** operator

**Instruction:**
Open or navigate to the VISU_DATA screen using the operator station HMI screen selection controls.

**Expected result:**
The VISU_DATA screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen-navigation controls and the mapping that includes F5 to Visu_Data.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Overall VISU_DATA layout and screen-selection area.*


**Stop or Escalate If:**

* VISU_DATA cannot be accessed from the operator station HMI.

---

### Step 2 — Locate the informational banner

**Responsible role:** operator

**Instruction:**
Locate the informational banner on the VISU_DATA screen that displays alarms or informational messages.

**Expected result:**
The informational banner is identified on the screen.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Informational banner area on the VISU_DATA screen.*


**Stop or Escalate If:**

* The informational banner is not visible where expected on the VISU_DATA screen.

---

### Step 3 — Navigate through banner messages

**Responsible role:** operator

**Instruction:**
Use the arrows on the right side of the banner to navigate through available messages.

**Expected result:**
The displayed banner message changes as the operator navigates through messages.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Message banner and the navigation arrows on the right side of the banner.*


**Stop or Escalate If:**

* Banner messages cannot be navigated using the documented arrows.

---

### Step 4 — Read displayed banner messages

**Responsible role:** operator

**Instruction:**
Read each displayed alarm or informational message from the banner as you navigate through the available messages.

**Expected result:**
The operator has reviewed the available alarm or informational messages shown in the banner.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Login controls, message banner, and surrounding VISU_DATA screen elements while reviewing messages.*


**Stop or Escalate If:**

* Displayed messages are unreadable or cannot be reviewed.

---

### Step 5 — Locate the current logged-in user field

**Responsible role:** operator

**Instruction:**
Locate the field on the VISU_DATA screen that displays the ID of the user currently logged in.

**Expected result:**
The current logged-in user ID field is identified.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Displayed logged-in user ID field near the login controls.*


**Stop or Escalate If:**

* The displayed current user ID field is missing or cannot be identified.

---

### Step 6 — Verify the displayed login status

**Responsible role:** operator

**Instruction:**
Verify whether a user ID is shown and record the displayed user ID if needed.

**Expected result:**
The operator confirms whether a user ID is displayed and can identify the current logged-in user.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Current logged-in user ID display and nearby LOGIN/LOGOUT controls.*


**Stop or Escalate If:**

* The displayed login state or user ID appears inconsistent with the actual operator session.

---

## Success Criteria

* The VISU_DATA screen is accessed successfully.
* Available alarm or informational banner messages can be viewed and navigated.
* The currently logged-in user ID can be identified from the screen.

## Failure Conditions

* The VISU_DATA screen cannot be accessed.
* The informational banner cannot be located or reviewed.
* Banner messages cannot be navigated using the documented arrows.
* The displayed login state or user ID appears inconsistent with the actual operator session.

## Escalation Guidance

* Escalate if banner messages cannot be navigated using the documented arrows.
* Escalate if the displayed login state or user ID appears inconsistent with the actual operator session.

## Missing Details / Known Gaps

* The source does not provide a time estimate for this procedure.
* The source does not provide corrective actions for banner messages or login-state discrepancies.
* The source does not specify whether production stop or LOTO is required; this procedure appears observational only.
* The source does not define how or where to record the displayed user ID.

## Source Lineage

- Candidate IDs: candidate_operator_review_visu_data_messages_and_session_status
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
