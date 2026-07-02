# Review Installed Software and Hospital Station IP Address on the Hospital HMI Default Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_review_installed_software_and_hospital_station_ip_address_on_the_hospital_hmi_default_screen_v1` |
| Title | Review Installed Software and Hospital Station IP Address on the Hospital HMI Default Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Hospital HMI Default screen to identify the currently installed software information and the Hospital Station IP address, then record both exactly as displayed.

## When To Use

Use this procedure when you need to identify or document the software currently installed on the Hospital HMI and the Hospital Station IP address shown on the Default screen.

## Do Not Use For

* Do not use this procedure to infer missing software details or network values if they are not visible on the screen.
* Do not use this procedure to update HMI date or time or use the REBOOT TO SETUP button.

## Safety And Operational Notes

* Only maintenance personnel should use the REBOOT TO SETUP button when updating the HMI date or time.
* Do not infer missing software details or network values if they are not visible on the screen.

## Access Or Tools Needed

* Access to the Hospital HMI
* Hospital HMI Default screen

## Related Operational Context

* ctx_manual_hospital_hmi_default_screen_v1
* ctx_manual_hospital_station_daily_inspection_v1

## Procedure Steps

### Step 1 — Open the Hospital HMI Default screen

**Responsible role:** operator

**Instruction:**
Open the Hospital HMI "Default" screen.

**Expected result:**
The Default screen is visible on the Hospital HMI.

**Screens / Images:**

![artifact_fig_4_41_hospital_hmi_2_4_default_screen](assets/artifact_fig_4_41_hospital_hmi_2_4_default_screen.png)

*Hospital HMI Default screen showing the software information area and IP address area.*


**Stop or Escalate If:**

* Escalate if the Default screen does not show the expected software information or IP address fields.

---

### Step 2 — Locate the installed software information

**Responsible role:** operator

**Instruction:**
Locate the information related to the software currently installed.

**Expected result:**
The installed software information is identified on the screen.

**Screens / Images:**

![artifact_fig_4_41_hospital_hmi_2_4_default_screen](assets/artifact_fig_4_41_hospital_hmi_2_4_default_screen.png)

*The area of the Default screen that displays information related to the software currently installed.*


**Stop or Escalate If:**

* Escalate if the Default screen does not show the expected software information field.
* Do not infer missing software details if they are not visible on the screen.

---

### Step 3 — Locate the Hospital Station IP address

**Responsible role:** operator

**Instruction:**
Locate the displayed IP address of the Hospital Station.

**Expected result:**
The Hospital Station IP address is identified on the screen.

**Screens / Images:**

![artifact_fig_4_41_hospital_hmi_2_4_default_screen](assets/artifact_fig_4_41_hospital_hmi_2_4_default_screen.png)

*The area of the Default screen that displays the Hospital Station IP address.*


**Stop or Escalate If:**

* Escalate if the Default screen does not show the expected IP address field.
* Do not infer missing network values if they are not visible on the screen.

---

### Step 4 — Record the installed software information

**Responsible role:** operator

**Instruction:**
Record the installed software information exactly as shown on the screen.

**Expected result:**
The installed software information is documented exactly as displayed.

**Screens / Images:**

![artifact_fig_4_41_hospital_hmi_2_4_default_screen](assets/artifact_fig_4_41_hospital_hmi_2_4_default_screen.png)

*Installed software information on the Default Hospital HMI 2.4 screen.*


**Stop or Escalate If:**

* Escalate if the installed software information is not visible on the Default screen.
* Do not infer missing software details if they are not visible on the screen.

---

### Step 5 — Record the Hospital Station IP address

**Responsible role:** operator

**Instruction:**
Record the Hospital Station IP address exactly as shown on the screen.

**Expected result:**
The Hospital Station IP address is documented exactly as displayed.

**Screens / Images:**

![artifact_fig_4_41_hospital_hmi_2_4_default_screen](assets/artifact_fig_4_41_hospital_hmi_2_4_default_screen.png)

*Hospital Station IP address on the Default Hospital HMI 2.4 screen.*


**Stop or Escalate If:**

* Escalate if the Hospital Station IP address is not visible on the Default screen.
* Do not infer missing network values if they are not visible on the screen.

---

## Success Criteria

* The Hospital HMI Default screen is opened successfully.
* The installed software information is identified from the Default screen.
* The Hospital Station IP address is identified from the Default screen.
* Both the installed software information and the Hospital Station IP address are recorded exactly as shown.

## Failure Conditions

* The Default screen does not show the expected software information field.
* The Default screen does not show the expected Hospital Station IP address field.
* The displayed software information or IP address is not visible clearly enough to record exactly.
* The user attempts to infer missing software details or network values that are not visible on the screen.

## Escalation Guidance

* Escalate if the Default screen does not show the expected software information or IP address fields.
* Escalate if the displayed information cannot be read clearly enough to document exactly.
* Do not infer missing software details or network values if they are not visible on the screen.

## Missing Details / Known Gaps

* The source does not provide field labels for the installed software information.
* The source does not provide the expected software value or version format.
* The source does not provide the expected IP address value or format beyond stating that the Hospital Station IP address is displayed.
* The source does not specify how the user navigates to the Default screen.
* The source does not specify where or how the recorded information should be documented.

## Source Lineage

- Candidate IDs: candidate_operator_review_hospital_hmi_default_screen_details
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
