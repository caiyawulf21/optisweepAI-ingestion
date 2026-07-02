# Process a Tote at the Hospital Station

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_process_a_tote_at_the_hospital_station_v1` |
| Title | Process a Tote at the Hospital Station |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Extract an arriving tote from the system at the hospital station, identify it by barcode scan, perform the task indicated by the HMI status fields, and return the tote to the system on the induct side when needed.

## When To Use

Use when a tote arrives at the hospital station and must be extracted, identified, manually handled according to the HMI status fields, and possibly returned to the system.

## Do Not Use For

* Do not use when the correct HMI screen or required task cannot be determined from the status fields; the source provides no further guidance.
* Do not use as a recovery procedure when the Tote ID field does not automatically populate after scanning; the source provides no recovery steps.

## Access Or Tools Needed

* Hospital station access
* HMI access to the corresponding hospital station screen
* Visibility of status fields on the HMI
* Green barcode scanner
* Access to the Tote ID field on the HMI
* Physical access to the right side and left-side induct area of the station

## Related Operational Context

* ctx_manual_hospital_station_status_fields_reference_v1
* ctx_manual_scanner_setup_overview_v1
* ctx_manual_hospital_station_overview_v1
* ctx_manual_hospital_station_main_menu_access_v1

## Procedure Steps

### Step 1 — Confirm tote arrival on the right side of the hospital station

**Responsible role:** operator

**Instruction:**
Confirm that the AGV has brought the tote to the right side of the hospital station.

**Expected result:**
The tote is present on the right side of the hospital station.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station view associated with tote arrival and handling; use it to orient to the station sides and tote-handling area.*


**Stop or Escalate If:**

* The tote is not on the right side of the hospital station.
* The operator cannot confirm the tote arrival location from the station view.

---

### Step 2 — Open the corresponding HMI screen

**Responsible role:** operator

**Instruction:**
Use the information shown in the status fields to determine and open the corresponding HMI screen for extracting the tote from the system.

**Expected result:**
The correct HMI screen for the tote is open.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*Status-related fields such as AGV#, Tote ID, Bar Code, and Status that help determine the correct hospital station screen.*

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/artifact_fig_4_32_hospital_hmi_remove_tote_screen.png)

*Example remove-tote screen used when extracting a tote from the system.*

![artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen](assets/artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen.png)

*Example status-driven hospital station screen showing extract position information and tote handling context.*

![artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen](assets/artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen.png)

*Example status-driven hospital station screen for a tote requiring manual handling.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen.png)

*Example status-driven hospital station screen showing tote identification and mismatch context.*


**Stop or Escalate If:**

* The correct HMI screen cannot be determined from the status fields.

---

### Step 3 — Scan the tote barcode with the green scanner

**Responsible role:** operator

**Instruction:**
Scan the tote barcode using the green scanner.

**Expected result:**
The tote barcode is read by the scanner.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station procedure image associated with barcode scanning at the station.*

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/artifact_fig_4_32_hospital_hmi_remove_tote_screen.png)

*Remove Tote screen context showing barcode scan use with the green scanner.*

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*Add Tote screen context showing barcode scan use with the green scanner.*


**Stop or Escalate If:**

* The barcode scan does not lead to Tote ID population on the HMI.

---

### Step 4 — Verify Tote ID field population

**Responsible role:** operator

**Instruction:**
Verify that the Tote ID automatically populates the Tote ID field after scanning.

**Expected result:**
The Tote ID field is populated automatically after the barcode scan.

**Screens / Images:**

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/artifact_fig_4_32_hospital_hmi_remove_tote_screen.png)

*Tote ID and Barcode fields populated after scanning on the Remove Tote screen.*

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*Tote ID and Barcode fields populated after scanning on the Add Tote screen.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen.png)

*Tote ID-related fields for comparison when barcode-related issues are present.*


**Stop or Escalate If:**

* The Tote ID field does not automatically populate after scanning.

---

### Step 5 — Perform the task indicated by the status fields

**Responsible role:** operator

**Instruction:**
Perform the required task for the tote as determined by the information in the status fields.

**Expected result:**
The tote-specific task indicated by the HMI status fields is completed.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*Status field content that tells the operator why the tote is there, what menu to use, and what action to perform.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen.png)

*Example task-specific hospital station screen for barcode mismatch handling.*

![artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen](assets/artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen.png)

*Example task-specific hospital station screen for failed-to-empty handling.*

![artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen](assets/artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen.png)

*Example task-specific hospital station screen for sent-from-bagging-station handling.*


**Stop or Escalate If:**

* The required task cannot be determined from the status fields.
* The source does not provide enough detail to complete the indicated task.

---

### Step 6 — Place returning tote on the left-side induct area

**Responsible role:** operator

**Instruction:**
If the tote is going back into the system, place it on the induct side on the left side of the station.

**Expected result:**
A tote that must re-enter the system is placed on the left-side induct area.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station induct-side placement area on the left side of the station.*

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*Add Tote screen context for sending a tote back into the system from the induct side.*


**Stop or Escalate If:**

* The tote needs to go back into the system but cannot be placed on the left-side induct area.

---

### Step 7 — Align the tote flush against the end stops

**Responsible role:** operator

**Instruction:**
Ensure the tote is flush against the end stops.

**Expected result:**
The tote is aligned against the end stops.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Induct-side tote placement and end-stop alignment area associated with the hospital station procedure.*


**Stop or Escalate If:**

* The tote cannot be positioned flush against the end stops.

---

## Success Criteria

* The tote is extracted and identified at the hospital station.
* The Tote ID field automatically populates after barcode scanning.
* The required task indicated by the HMI status fields is completed.
* If the tote is returning to the system, it is placed on the left-side induct area flush against the end stops.

## Failure Conditions

* The tote is not at the expected right-side hospital station location.
* The correct HMI screen cannot be determined from the status fields.
* The Tote ID field does not automatically populate after scanning.
* The required task cannot be determined from the status fields.
* A tote returning to the system is not placed on the left-side induct area or is not flush against the end stops.

## Escalation Guidance

* If the Tote ID field does not automatically populate after scanning, stop and escalate because the source does not provide recovery steps.
* If the correct HMI screen or required task cannot be determined from the status fields, stop and escalate because the source does not provide further guidance.

## Missing Details / Known Gaps

* The source does not provide a time estimate for completing this procedure.
* The source does not specify production-stop or LOTO requirements for this procedure.
* The source does not provide recovery steps if the Tote ID field does not automatically populate after scanning.
* The source does not provide further guidance if the correct HMI screen or required task cannot be determined from the status fields.
* The source does not specify the exact HMI button sequence to open the corresponding screen within this page 92 procedure.
* The source does not define the detailed task variants beyond stating that they are determined by the status fields.

## Source Lineage

- Candidate IDs: candidate_operator_process_tote_at_hospital_station
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
