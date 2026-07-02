# Verify Induct and Extract Position Information on the Hospital HMI Operations Menu

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_induct_and_extract_position_information_on_the_hospital_hmi_operations_menu_v1` |
| Title | Verify Induct and Extract Position Information on the Hospital HMI Operations Menu |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Check the documented read-only fields on the Hospital HMI Operations Menu for the induct and extract sides of the station and capture the currently displayed AGV#, Tote ID, Bar Code, and Status information.

## When To Use

Use this procedure when an operator needs to view and record the current Induct Position and Extract Position information shown on the Hospital HMI Operations Menu, including AGV#, Tote ID, Bar Code, and Status fields that are received from the WCS.

## Do Not Use For

* Do not use this procedure to modify Induct Position or Extract Position values, because the source states this information is read-only.
* Do not use this procedure as a corrective action procedure for missing, unclear, or incorrect values, because the source defines displayed fields but does not provide corrective actions.

## Safety And Operational Notes

* The Induct Position and Extract Position information on this screen is read-only and received from the WCS.
* Do not attempt to modify displayed values.

## Access Or Tools Needed

* Access to the Hospital HMI Operations Menu screen
* Ability to view the Induct Position and Extract Position sections

## Related Operational Context

* ctx_manual_hospital_operations_menu_screen_v1
* ctx_manual_hospital_operations_menu_status_messages_v1

## Procedure Steps

### Step 1 — Open or view the Hospital HMI Operations Menu

**Responsible role:** operator

**Instruction:**
Open or view the Hospital HMI Operations Menu screen and confirm that the Induct Position and Extract Position areas are visible.

**Expected result:**
The Hospital HMI Operations Menu is visible with both position sections available for review.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Induct Position and Extract Position sections on the Hospital HMI Operations Screen.*


**Stop or Escalate If:**

* The Hospital HMI Operations Menu screen is not available.
* The Induct Position or Extract Position sections are missing from view.

---

### Step 2 — Locate the Induct Position fields

**Responsible role:** operator

**Instruction:**
Locate the Induct Position section and identify the AGV#, Tote ID, Bar Code, and Status fields.

**Expected result:**
The operator can identify all four documented fields in the Induct Position section.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Induct Position area and its AGV#, Tote ID, Bar Code, and Status fields.*


**Stop or Escalate If:**

* Any required Induct Position field is missing or unclear on the screen.

---

### Step 3 — Read the induct AGV number

**Responsible role:** operator

**Instruction:**
Read and record the AGV# shown for the induct side of the station.

**Expected result:**
The current induct-side AGV# is captured.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The AGV# field in the Induct Position section.*


**Stop or Escalate If:**

* The induct AGV# is missing or unclear on the screen.

---

### Step 4 — Read the induct Tote ID

**Responsible role:** operator

**Instruction:**
Read and record the Tote ID shown for the induct side of the station.

**Expected result:**
The current induct-side Tote ID is captured.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Tote ID field in the Induct Position section.*


**Stop or Escalate If:**

* The induct Tote ID is missing or unclear on the screen.

---

### Step 5 — Read the induct bar code information

**Responsible role:** operator

**Instruction:**
Read and record the Bar Code information shown for the induct side of the station.

**Expected result:**
The current induct-side Bar Code information is captured.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Bar Code field in the Induct Position section.*


**Stop or Escalate If:**

* The induct Bar Code information is missing or unclear on the screen.

---

### Step 6 — Read the induct status message

**Responsible role:** operator

**Instruction:**
Read and record the Status message shown for the induct side of the station.

**Expected result:**
The current induct-side Status message is captured.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Status field in the Induct Position section.*


**Stop or Escalate If:**

* The induct Status message is missing or unclear on the screen.

---

### Step 7 — Locate the Extract Position fields

**Responsible role:** operator

**Instruction:**
Locate the Extract Position section and identify the AGV#, Tote ID, Bar Code, and Status fields.

**Expected result:**
The operator can identify all four documented fields in the Extract Position section.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Extract Position area and its AGV#, Tote ID, Bar Code, and Status fields.*


**Stop or Escalate If:**

* Any required Extract Position field is missing or unclear on the screen.

---

### Step 8 — Read the extract AGV number

**Responsible role:** operator

**Instruction:**
Read and record the AGV# shown for the extract side of the station.

**Expected result:**
The current extract-side AGV# is captured.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The AGV# field in the Extract Position section.*


**Stop or Escalate If:**

* The extract AGV# is missing or unclear on the screen.

---

### Step 9 — Read the extract Tote ID

**Responsible role:** operator

**Instruction:**
Read and record the Tote ID shown for the extract side of the station.

**Expected result:**
The current extract-side Tote ID is captured.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Tote ID field in the Extract Position section.*


**Stop or Escalate If:**

* The extract Tote ID is missing or unclear on the screen.

---

### Step 10 — Read the extract bar code information

**Responsible role:** operator

**Instruction:**
Read and record the Bar Code information shown for the extract side of the station.

**Expected result:**
The current extract-side Bar Code information is captured.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Bar Code field in the Extract Position section.*


**Stop or Escalate If:**

* The extract Bar Code information is missing or unclear on the screen.

---

### Step 11 — Read the extract status message

**Responsible role:** operator

**Instruction:**
Read and record the Status message shown for the extract side of the station.

**Expected result:**
The current extract-side Status message is captured.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Status field in the Extract Position section.*


**Stop or Escalate If:**

* The extract Status message is missing or unclear on the screen.

---

### Step 12 — Confirm the fields are read-only WCS information

**Responsible role:** operator

**Instruction:**
Verify that the Induct Position and Extract Position fields are being treated as read-only information received from the WCS.

**Expected result:**
The operator has confirmed that the displayed values are read-only WCS-provided information and has not attempted to modify them.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*The Induct Position and Extract Position information areas described as read-only and received from the WCS.*


**Stop or Escalate If:**

* There is any need to modify displayed values.
* Required values are missing or unclear on the screen.
* Corrective action is needed beyond viewing and recording the displayed information.

---

## Success Criteria

* The Hospital HMI Operations Menu was viewed successfully.
* The operator identified the AGV#, Tote ID, Bar Code, and Status fields for both Induct Position and Extract Position.
* The current values for AGV#, Tote ID, Bar Code, and Status were read and recorded for both sides of the station.
* The fields were treated as read-only information received from the WCS.

## Failure Conditions

* The Hospital HMI Operations Menu cannot be viewed.
* One or more required fields are missing, unreadable, or unclear.
* The operator attempts to modify values that the source defines as read-only.
* The source does not provide corrective actions for missing or unclear values.

## Escalation Guidance

* Escalate if required values are missing or unclear on the screen.
* Escalate if corrective action is needed, because this source section defines displayed fields but does not provide corrective actions.
* Stop and escalate rather than attempting to modify displayed values, because the information is read-only and received from the WCS.

## Missing Details / Known Gaps

* The source does not provide acceptance thresholds or expected values for AGV#, Tote ID, Bar Code, or Status.
* The source does not provide corrective actions for missing, unclear, or incorrect displayed values.
* The source does not provide an estimated completion time.
* The source does not specify whether production stop or LOTO is required.
* The source does not define a separate supporting role for this procedure.

## Source Lineage

- Candidate IDs: candidate_operator_verify_hospital_hmi_induct_extract_position_fields
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
