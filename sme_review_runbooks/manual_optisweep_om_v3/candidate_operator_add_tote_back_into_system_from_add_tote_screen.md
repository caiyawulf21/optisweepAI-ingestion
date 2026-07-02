# Add a Tote Back Into the System Using the Add Tote Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_add_a_tote_back_into_the_system_using_the_add_tote_screen_v1` |
| Title | Add a Tote Back Into the System Using the Add Tote Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Add Tote screen and scanner to scan a tote barcode, verify the displayed Tote ID, and execute the tote return so the AGV takes the tote back into the system.

## When To Use

Use this procedure when returning a tote back into the system from the Add Tote screen using the documented scanner workflow at the sorter.

## Do Not Use For

* Do not use this procedure if the tote ID is not displayed correctly on the screen.
* Not for tote initialization workflows described in the Tote Initialization Procedure.
* Not for removing a tote from the system.

## Safety And Operational Notes

* Do not proceed if the tote ID is not displayed correctly.
* The source does not provide additional recovery or escalation steps beyond verifying the displayed Tote ID.

## Access Or Tools Needed

* Access to the Add Tote screen
* Zebra scanner
* Tote barcode

## Related Operational Context

* ctx_manual_acb_api_screen_reference_v1
* ctx_manual_sorter_scanner_operation_overview_v1

## Procedure Steps

### Step 1 — Navigate to the Add Tote screen

**Responsible role:** operator

**Instruction:**
Navigate to the "Add Tote" screen.

**Expected result:**
The Add Tote screen is open and ready for barcode scanning.

**Screens / Images:**

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*The Add Tote screen layout and the area used for tote barcode scanning.*

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*The page 93 image associated with the sorter scanner operation and Add Tote workflow.*


**Stop or Escalate If:**

* Stop if the Add Tote screen cannot be reached.

---

### Step 2 — Scan the tote barcode

**Responsible role:** operator

**Instruction:**
Scan the tote barcode using the documented scanner.

**Expected result:**
The system receives the tote barcode scan.

**Screens / Images:**

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*The scanner-related image associated with the Add Tote workflow.*

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*The Add Tote screen fields populated by scanning the tote barcode.*


**Stop or Escalate If:**

* Stop if the tote barcode cannot be scanned.

---

### Step 3 — Verify the displayed Tote ID

**Responsible role:** operator

**Instruction:**
Verify that the tote ID is displayed correctly on the screen.

**Expected result:**
The displayed Tote ID matches the tote that was scanned.

**Screens / Images:**

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*The Tote ID field and related barcode information on the Add Tote screen.*

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*Where the displayed tote information appears in the Add Tote workflow image.*


**Stop or Escalate If:**

* Do not proceed if the tote ID is not displayed correctly.

---

### Step 4 — Confirm and execute the tote return

**Responsible role:** operator

**Instruction:**
Press "Confirm & Execute."

**Expected result:**
The tote return is executed and the AGV takes the tote back into the system.

**Screens / Images:**

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*The Confirm & Execute control on the Add Tote screen.*

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*The image associated with the final confirmation step for returning the tote.*


**Stop or Escalate If:**

* Stop if the Tote ID was not verified as correct before pressing Confirm & Execute.
* Escalate if the tote is not taken back into the system after execution.

---

## Success Criteria

* The tote barcode is scanned successfully.
* The displayed Tote ID is correct.
* Confirm & Execute is pressed.
* The AGV takes the tote back into the system.

## Failure Conditions

* The Add Tote screen cannot be accessed.
* The tote barcode cannot be scanned.
* The Tote ID is not displayed correctly.
* The tote is not taken back into the system after Confirm & Execute.

## Escalation Guidance

* Do not proceed if the tote ID is not displayed correctly.
* If the tote is not taken back into the system after Confirm & Execute, escalate for SME review because the source does not provide additional recovery steps.

## Missing Details / Known Gaps

* The source packet does not provide a time estimate.
* The source packet does not provide explicit production stop or LOTO requirements.
* The source packet does not provide detailed recovery steps if scanning fails or execution does not complete.
* The source packet does not explicitly define navigation path details for reaching the Add Tote screen in this sorter workflow.

## Source Lineage

- Candidate IDs: candidate_operator_add_tote_back_into_system_from_add_tote_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
