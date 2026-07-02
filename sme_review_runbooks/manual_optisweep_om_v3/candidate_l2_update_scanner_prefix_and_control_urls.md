# Verify Scanner Prefixes and Update HTTP and OPC URL Settings

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_scanner_prefixes_and_update_http_and_opc_url_settings_v1` |
| Title | Verify Scanner Prefixes and Update HTTP and OPC URL Settings |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Access scanner settings in the Barcode Interface application, enter the documented default settings password, verify configured prefixes against tote and location labels, update the HTTP and OPC URL fields with the documented control IP addresses, and save the settings.

## When To Use

Use this procedure during scanner setup or scanner replacement configuration when scanner settings must be checked, prefixes must be verified against tote and location labels, or the HTTP and OPC URL settings must be updated to the AGV control and Hospital control IP addresses.

## Do Not Use For

* Do not use this runbook to determine the actual prefix values; the source only instructs verification against tote and location labels.
* Do not use this runbook to determine the actual AGV control or Hospital control IP addresses; the source states they must be entered but does not provide the values.
* Do not use this runbook for scanner connectivity calibration or dock setup; those activities are referenced elsewhere in the scanner setup section but are not part of this candidate.

## Safety And Operational Notes

* This procedure changes scanner communication-related configuration values.
* Stop and escalate if the correct AGV control or Hospital control IP addresses are not available.
* Stop and escalate if the settings cannot be saved.

## Access Or Tools Needed

* Barcode Interface application
* Settings access password
* Tote labels for prefix comparison
* Location labels for prefix comparison
* AGV control IP address
* Hospital control IP address

## Related Operational Context

* ctx_manual_scanner_settings_access_v1
* ctx_manual_scanner_prefix_and_url_configuration_v1
* ctx_manual_estop_reset_reference_v1

## Procedure Steps

### Step 1 — Open scanner settings

**Responsible role:** L2_support

**Instruction:**
In the Barcode Interface application, click the settings button to open scanner settings.

**Expected result:**
The scanner settings access prompt or settings screen opens.

**Screens / Images:**

![artifact_page_211_image_2](assets/artifact_page_211_image_2.jpeg)

*Settings button on the scanner setup screen.*

![artifact_page_211_image_4](assets/artifact_page_211_image_4.jpeg)

*Scanner setup screen associated with settings access.*


**Stop or Escalate If:**

* Stop and escalate if the settings screen cannot be opened.

---

### Step 2 — Enter the settings password

**Responsible role:** L2_support

**Instruction:**
When prompted, enter the settings password. By default, the password is "Opti."

**Expected result:**
Settings access is granted and the scanner settings screen is displayed.

**Screens / Images:**

![artifact_page_211_image_2](assets/artifact_page_211_image_2.jpeg)

*Password entry associated with scanner settings access.*

![artifact_page_211_image_3](assets/artifact_page_211_image_3.jpeg)

*Scanner settings access screen related to password entry.*


**Stop or Escalate If:**

* Escalate if the settings password is not accepted.

---

### Step 3 — Verify configured prefixes

**Responsible role:** L2_support

**Instruction:**
Review the configured prefix values in scanner settings and verify they match the labels on the totes and locations.

**Expected result:**
Configured prefixes match the tote and location labels.

**Screens / Images:**

![artifact_page_211_image_4](assets/artifact_page_211_image_4.jpeg)

*Settings screen showing prefix values and the fields used for comparison.*

![artifact_page_211_image_2](assets/artifact_page_211_image_2.jpeg)

*Scanner setup screen associated with prefix verification.*


**Stop or Escalate If:**

* Stop and escalate if configured prefixes do not match tote or location labels.
* Stop and escalate if the correct expected prefix values cannot be determined from the available labels.

---

### Step 4 — Update the HTTP URL setting

**Responsible role:** L2_support

**Instruction:**
Change the HTTP URL setting so it contains the AGV control IP address.

**Expected result:**
The HTTP URL field contains the AGV control IP address.

**Screens / Images:**

![artifact_page_211_image_4](assets/artifact_page_211_image_4.jpeg)

*Settings screen showing the HTTP URL field.*

![artifact_page_211_image_3](assets/artifact_page_211_image_3.jpeg)

*Scanner configuration screen related to HTTP URL entry.*


**Stop or Escalate If:**

* Escalate if the correct AGV control IP address is not available.

---

### Step 5 — Update the OPC URL setting

**Responsible role:** L2_support

**Instruction:**
Change the OPC URL setting so it contains the Hospital control IP address.

**Expected result:**
The OPC URL field contains the Hospital control IP address.

**Screens / Images:**

![artifact_page_211_image_4](assets/artifact_page_211_image_4.jpeg)

*Settings screen showing the OPC URL field.*

![artifact_page_211_image_2](assets/artifact_page_211_image_2.jpeg)

*Scanner setup screen associated with OPC URL configuration.*


**Stop or Escalate If:**

* Escalate if the correct Hospital control IP address is not available.

---

### Step 6 — Save scanner settings

**Responsible role:** L2_support

**Instruction:**
Click the "Save Settings" button to save the configuration.

**Expected result:**
The updated scanner settings are saved.

**Screens / Images:**

![artifact_page_211_image_4](assets/artifact_page_211_image_4.jpeg)

*Settings screen showing the "Save Settings" button.*

![artifact_page_211_image_3](assets/artifact_page_211_image_3.jpeg)

*Scanner configuration screen associated with saving settings.*


**Stop or Escalate If:**

* Stop and escalate if the settings cannot be saved.

---

## Success Criteria

* Scanner settings are accessible.
* Configured prefixes match the labels on the totes and locations.
* The HTTP URL field contains the documented AGV control IP address.
* The OPC URL field contains the documented Hospital control IP address.
* The updated settings are saved.

## Failure Conditions

* The settings password is not accepted.
* Configured prefixes do not match tote or location labels.
* The correct AGV control IP address is not available.
* The correct Hospital control IP address is not available.
* The settings cannot be saved.

## Escalation Guidance

* Escalate if the settings password is not accepted.
* Escalate if the correct AGV control or Hospital control IP addresses are not available.
* Stop and escalate if the settings cannot be saved.

## Missing Details / Known Gaps

* The source does not provide the actual settings screen field values for the prefixes.
* The source does not provide the actual AGV control IP address.
* The source does not provide the actual Hospital control IP address.
* The source does not state whether production must be stopped before changing these settings.
* The source does not provide a time estimate for completing this procedure.
* The source does not describe the exact confirmation message or visual indication after saving settings.

## Source Lineage

- Candidate IDs: candidate_l2_update_scanner_prefix_and_control_urls
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
