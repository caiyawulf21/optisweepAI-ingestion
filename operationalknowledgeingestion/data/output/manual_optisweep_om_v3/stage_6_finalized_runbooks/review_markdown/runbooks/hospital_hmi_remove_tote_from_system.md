# Remove a tote from the system using the Hospital HMI Remove Tote screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_a_tote_from_the_system_using_the_hospital_hmi_remove_tote_screen_v1` |
| Title | Remove a tote from the system using the Hospital HMI Remove Tote screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Hospital HMI Remove Tote screen to scan a tote bar code, verify extract-side information received from the WCS, confirm the tote is properly positioned on the extract side, and press CONFIRM & EXECUTE to remove the tote from the system so the station operator can perform the required task.

## When To Use

Use this procedure when a tote must be removed from the system at the Hospital Station using the Hospital HMI Remove Tote screen, after the tote is properly positioned on the extract side and the station operator needs to perform the required task.

## Do Not Use For

* Do not use this procedure to add a tote back into the system; the source only identifies the Add Tote screen as a shortcut from this screen.
* Do not press CONFIRM & EXECUTE until the tote is positioned properly on the extract side.
* Do not use this runbook as a recovery procedure for missing or unexpected Tote ID, Bar Code, or WCS Status information; the source does not provide recovery or escalation steps for those conditions.

## Safety And Operational Notes

* Do not press CONFIRM & EXECUTE until the tote is positioned properly on the extract side.

## Access Or Tools Needed

* Access to the Hospital HMI Remove Tote screen
* Green scanner
* Tote bar code

## Procedure Steps

### Step 1 — Open the Hospital HMI Remove Tote screen

**Responsible role:** operator

**Instruction:**
Open or use the Hospital HMI Remove Tote screen.

**Expected result:**
The Remove Tote screen is displayed and available for tote processing.

**Screens / Images:**

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/artifact_fig_4_32_hospital_hmi_remove_tote_screen.png)

*Hospital HMI Remove Tote screen showing the Tote ID field, Barcode control, CONFIRM & EXECUTE button, extract position information, and Add Tote shortcut button.*


**Stop or Escalate If:**

* The Remove Tote screen cannot be accessed.

---

### Step 2 — Scan the tote bar code with the green scanner

**Responsible role:** operator

**Instruction:**
Use the green scanner to scan the tote bar code so the Tote ID is populated.

**Expected result:**
The Tote ID is populated on the Remove Tote screen after the scan.

**Screens / Images:**

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/artifact_fig_4_32_hospital_hmi_remove_tote_screen.png)

*Tote ID field and barcode-related controls on the Remove Tote screen.*


**Stop or Escalate If:**

* The Tote ID does not populate after scanning.

---

### Step 3 — Use the Barcode control if needed and rescan

**Responsible role:** operator

**Instruction:**
If needed, press the Barcode control and then use the green scanner to scan the tote bar code.

**Expected result:**
The barcode scan is accepted through the Barcode control workflow and the tote information is populated.

**Screens / Images:**

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/artifact_fig_4_32_hospital_hmi_remove_tote_screen.png)

*Barcode control and Tote ID/barcode fields on the Remove Tote screen.*


**Stop or Escalate If:**

* The tote information still does not populate after using the Barcode control and rescanning.

---

### Step 4 — Check extract position information from the WCS

**Responsible role:** operator

**Instruction:**
Check the Extract Position Information shown from the WCS, including AGV#, Tote ID, Bar Code, and Status.

**Expected result:**
The operator can view extract-side information from the WCS for the tote being removed.

**Screens / Images:**

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/artifact_fig_4_32_hospital_hmi_remove_tote_screen.png)

*Extract Position Information area showing AGV#, Tote ID, Bar Code, and Status.*


**Stop or Escalate If:**

* Extract Position Information does not appear as expected.

---

### Step 5 — Verify the tote is properly positioned on the extract side

**Responsible role:** operator

**Instruction:**
Verify the tote is positioned properly on the extract side.

**Expected result:**
The tote is confirmed to be properly positioned for removal.

**Stop or Escalate If:**

* The tote is not positioned properly on the extract side.

---

### Step 6 — Press CONFIRM & EXECUTE to remove the tote

**Responsible role:** operator

**Instruction:**
Press CONFIRM & EXECUTE to remove the tote from the system so the station operator can perform the required task.

**Expected result:**
The tote is removed from the system and the station operator can perform the required task.

**Screens / Images:**

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/artifact_fig_4_32_hospital_hmi_remove_tote_screen.png)

*CONFIRM & EXECUTE button on the Remove Tote screen.*


**Stop or Escalate If:**

* The tote is not properly positioned on the extract side.
* The Tote ID, Bar Code, or WCS Status information does not appear as expected before execution.

---

## Success Criteria

* The tote is removed from the system.
* The station operator can perform the required task.
* The operator completed the action using the Hospital HMI Remove Tote screen after verifying extract-side information and tote position.

## Failure Conditions

* The Remove Tote screen cannot be accessed.
* The Tote ID does not populate after scanning the tote bar code.
* Extract Position Information is missing, incomplete, or does not appear as expected.
* The tote is not properly positioned on the extract side.
* The source does not provide recovery or escalation steps if the Tote ID, Bar Code, or WCS Status information does not appear as expected.

## Escalation Guidance

* Stop before pressing CONFIRM & EXECUTE if the tote is not positioned properly on the extract side.
* If the Tote ID, Bar Code, or WCS Status information does not appear as expected, the source packet does not provide a recovery path; escalate for SME or supervisory review per local practice.

## Missing Details / Known Gaps

* The packet does not provide the full OCR text of the Remove Tote section.
* The source does not provide explicit recovery steps if scanning fails or if Tote ID, Bar Code, or WCS Status information does not appear as expected.
* The source does not provide an explicit completion confirmation message after CONFIRM & EXECUTE.
* The source does not provide an estimated procedure time.
* The source does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: hospital_hmi_remove_tote_from_system
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
