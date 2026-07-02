# Log In To or Log Out From the Hospital HMI Using the Default Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_log_in_to_or_log_out_from_the_hospital_hmi_using_the_default_screen_v1` |
| Title | Log In To or Log Out From the Hospital HMI Using the Default Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Hospital HMI Default screen to perform login or logout on the hospital HMI. The source supports that the Default screen displays installed software information and the Hospital Station IP address, and that users can log in to and log out from the hospital HMI, but it does not provide exact button labels, prompts, credentials, or confirmation messages.

## When To Use

Use this procedure when a user needs to log in to or log out from the Hospital HMI from the Default screen.

## Do Not Use For

* Do not use this runbook to update HMI date or time.
* Do not use this runbook to operate the REBOOT TO SETUP function.
* Do not use this runbook to infer undocumented credential requirements, prompts, button labels, or status messages.

## Safety And Operational Notes

* Only maintenance personnel should use the REBOOT TO SETUP button when updating the HMI date or time.
* Do not invent credential requirements, confirmation prompts, or status messages because the source does not provide them.

## Access Or Tools Needed

* Access to the Hospital HMI
* Hospital HMI Default screen
* Any required user credentials if prompted by the HMI

## Related Operational Context

* ctx_manual_hospital_hmi_default_screen_v1

## Procedure Steps

### Step 1 — Open the Hospital HMI Default screen

**Responsible role:** operator

**Instruction:**
Open the Hospital HMI "Default" screen. If starting from the Hospital HMI Maintenance Menu, use the available access to the 2.4 Default screen.

**Expected result:**
The Hospital HMI Default screen is displayed.

**Screens / Images:**

![artifact_fig_4_41_hospital_hmi_2_4_default_screen](assets/artifact_fig_4_41_hospital_hmi_2_4_default_screen.png)

*Hospital HMI 2.4 Default screen layout, including installed software information, station IP address, and login/logout access if visible.*

![artifact_fig_4_38_hospital_hmi_maintenance_menu_screen](assets/artifact_fig_4_38_hospital_hmi_maintenance_menu_screen.png)

*Maintenance Menu access to the 2.4 Default screen.*


**Stop or Escalate If:**

* The Default screen is not available from the Hospital HMI.
* The displayed screen does not match the Default screen described by the source.

---

### Step 2 — Locate the login or logout control

**Responsible role:** operator

**Instruction:**
On the Default screen, locate the available login or logout control presented by the HMI.

**Expected result:**
A login or logout control is visible on the Default screen.

**Screens / Images:**

![artifact_fig_4_41_hospital_hmi_2_4_default_screen](assets/artifact_fig_4_41_hospital_hmi_2_4_default_screen.png)

*Default Hospital HMI 2.4 screen showing installed software information, the station IP address, and login/logout access.*


**Stop or Escalate If:**

* The login or logout control is not available on the Default screen.

---

### Step 3 — Perform the requested login or logout action

**Responsible role:** operator

**Instruction:**
Use the available control to log in to the hospital HMI or log out from the hospital HMI, following the on-screen interaction that is actually presented. If the HMI prompts for credentials, use the required credentials available to the user.

**Expected result:**
The requested login or logout action is completed from the Default screen.

**Screens / Images:**

![artifact_fig_4_41_hospital_hmi_2_4_default_screen](assets/artifact_fig_4_41_hospital_hmi_2_4_default_screen.png)

*Default Hospital HMI 2.4 screen showing login/logout access.*


**Stop or Escalate If:**

* The HMI does not allow the requested login or logout action from the Default screen.
* The interaction requires undocumented prompts or controls that cannot be completed safely from the source guidance.

---

### Step 4 — Confirm the resulting logged-in or logged-out state

**Responsible role:** operator

**Instruction:**
Confirm that the HMI reflects the requested logged-in or logged-out state using only the on-screen indication provided by the system.

**Expected result:**
The HMI visibly reflects the requested logged-in or logged-out state.

**Screens / Images:**

![artifact_fig_4_41_hospital_hmi_2_4_default_screen](assets/artifact_fig_4_41_hospital_hmi_2_4_default_screen.png)

*Any on-screen indication on the Default screen that shows whether the HMI is in the requested logged-in or logged-out state.*


**Stop or Escalate If:**

* The HMI does not clearly indicate the resulting logged-in or logged-out state.
* The displayed state does not match the requested action.

---

## Success Criteria

* The user completes a login or logout action from the Hospital HMI Default screen.
* The HMI reflects the requested logged-in or logged-out state using the on-screen indication provided by the system.

## Failure Conditions

* The Default screen cannot be reached.
* The login or logout control is not available on the Default screen.
* The HMI does not complete the requested login or logout action.
* The HMI does not clearly indicate the resulting logged-in or logged-out state.

## Escalation Guidance

* Escalate if the login or logout control is not available on the Default screen.
* Escalate if the HMI does not clearly reflect the requested logged-in or logged-out state.
* Escalate if the interaction requires undocumented credential requirements, confirmation prompts, or status messages not provided by the source.

## Missing Details / Known Gaps

* The source does not provide the exact login control label.
* The source does not provide the exact logout control label.
* The source does not provide the exact navigation sequence to reach the Default screen from every starting point.
* The source does not provide credential requirements or user account rules.
* The source does not provide confirmation prompts or status message text for successful login or logout.
* The source does not provide explicit failure messages or recovery actions beyond escalation.

## Source Lineage

- Candidate IDs: candidate_operator_log_in_or_out_hospital_hmi_default_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
