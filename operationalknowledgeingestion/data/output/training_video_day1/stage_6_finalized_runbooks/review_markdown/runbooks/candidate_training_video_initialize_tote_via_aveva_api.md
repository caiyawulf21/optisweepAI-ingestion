# Initialize a Tote Using the Aveva API Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_initialize_a_tote_using_the_aveva_api_page_v1` |
| Title | Initialize a Tote Using the Aveva API Page |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Initialize Tote Aveva API page to enter BarcodeID, StationID, and ToteID, submit the request, and review the response returned by the system.

## When To Use

Use this procedure when a tote needs to be initialized for processing through the Initialize Tote Aveva API page shown in the source.

## Do Not Use For

* Do not use this procedure to assume a tote was initialized if the Response field shows an error or tote status instead of confirmation.
* Do not use this procedure to resolve response conditions that the source does not explain how to correct.

## Safety And Operational Notes

* The source presents this as an Aveva API page workflow and does not provide broader permission or access controls.
* Do not assume initialization succeeded unless the Response field confirms it.

## Access Or Tools Needed

* Access to the Initialize Tote Aveva API page
* Barcode or tote number
* Station ID
* Tote ID
* RMS reference for station ID as mentioned in the transcript

## Related Operational Context

* ctx_training_video_initialize_tote_api_page_v1
* ctx_training_video_initialize_tote_fields_v1
* ctx_training_video_initialize_tote_response_v1

## Procedure Steps

### Step 1 — Open the Initialize Tote Aveva API page

**Responsible role:** L1_support

**Instruction:**
Open the Initialize Tote Aveva API page.

**Expected result:**
The Initialize Tote Aveva API page is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0074_what_s_this_so_this_is_primary_02_26_01_500](assets/42f7b5cdc1ad71cb.jpg)

*Initialize Tote Aveva API page with BarcodeID, StationID, ToteID, Request to Initialize Tote, and Response areas.*


**Stop or Escalate If:**

* Stop or escalate if the Initialize Tote Aveva API page cannot be accessed.
* Stop or escalate if the expected fields or request/response areas are not present.

---

### Step 2 — Enter the BarcodeID value

**Responsible role:** L1_support

**Instruction:**
Enter the barcode or tote number in the BarcodeID field. Use the source note that the barcode and tote ID may be the same number.

**Expected result:**
The BarcodeID field contains the intended barcode or tote number.

**Screens / Images:**

![artifact_training_video_training_video_day1_0074_what_s_this_so_this_is_primary_02_26_01_500](assets/42f7b5cdc1ad71cb.jpg)

*BarcodeID field on the Initialize Tote Aveva API page.*


**Stop or Escalate If:**

* Stop or escalate if the correct barcode or tote number is not available.

---

### Step 3 — Enter the StationID value

**Responsible role:** L1_support

**Instruction:**
Enter the StationID for the station on the rack, using the station ID as shown in RMS according to the transcript.

**Expected result:**
The StationID field contains the intended station identifier.

**Screens / Images:**

![artifact_training_video_training_video_day1_0074_what_s_this_so_this_is_primary_02_26_01_500](assets/42f7b5cdc1ad71cb.jpg)

*StationID field on the Initialize Tote Aveva API page.*


**Stop or Escalate If:**

* Stop or escalate if the station ID cannot be determined from RMS as referenced by the source.

---

### Step 4 — Enter the ToteID value

**Responsible role:** L1_support

**Instruction:**
Enter the ToteID field.

**Expected result:**
The ToteID field contains the intended tote identifier.

**Screens / Images:**

![artifact_training_video_training_video_day1_0074_what_s_this_so_this_is_primary_02_26_01_500](assets/42f7b5cdc1ad71cb.jpg)

*ToteID field on the Initialize Tote Aveva API page.*


**Stop or Escalate If:**

* Stop or escalate if the correct tote ID is not available.

---

### Step 5 — Submit the initialization request

**Responsible role:** L1_support

**Instruction:**
Click the Request to Initialize Tote button.

**Expected result:**
The system processes the request and returns a result in the Response field.

**Screens / Images:**

![artifact_training_video_training_video_day1_0074_what_s_this_so_this_is_primary_02_26_01_500](assets/42f7b5cdc1ad71cb.jpg)

*Request to Initialize Tote button on the Initialize Tote Aveva API page.*


**Stop or Escalate If:**

* Stop or escalate if the request cannot be submitted.

---

### Step 6 — Review the Response field

**Responsible role:** L1_support

**Instruction:**
Review the Response field for the returned result, such as a confirmation message if successful or an error/status message if initialization fails.

**Expected result:**
The Response field indicates whether the tote was initialized successfully or provides an error/status explaining why it was not.

**Screens / Images:**

![artifact_training_video_training_video_day1_0074_what_s_this_so_this_is_primary_02_26_01_500](assets/42f7b5cdc1ad71cb.jpg)

*Response field on the Initialize Tote Aveva API page.*


**Stop or Escalate If:**

* Stop or escalate if the Response field shows an error or tote status instead of confirmation.
* Stop or escalate if the tote cannot be initialized and the response indicates a status the user cannot resolve from the source.

---

## Success Criteria

* The Initialize Tote Aveva API page accepts BarcodeID, StationID, and ToteID input values.
* The request is submitted using Request to Initialize Tote.
* The Response field returns confirmation that the tote was initialized successfully.

## Failure Conditions

* The Initialize Tote Aveva API page or expected fields are not available.
* Required input values are missing or cannot be determined.
* The Response field shows an error message or tote status instead of confirmation.
* The tote cannot be initialized and the returned status is not resolvable from the source.

## Escalation Guidance

* If the Response field shows an error or tote status instead of confirmation, do not assume initialization succeeded.
* If the tote cannot be initialized and the response indicates a status the user cannot resolve from the source, escalate for further support.

## Missing Details / Known Gaps

* The source does not provide explicit navigation steps for reaching the Initialize Tote Aveva API page.
* The source does not define required permissions or access approval for this page.
* The source does not provide exact success text returned in the Response field.
* The source does not provide exact error codes, error text, or remediation steps for specific failure responses.
* The source does not provide an estimated completion time.
* The source does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_initialize_tote_via_aveva_api
- Source ID: `training_video_day1`
- Source Type: `training_video`
