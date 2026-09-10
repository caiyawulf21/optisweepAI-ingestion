# Initialize a Tote Using the Initialize Tote Aveva API Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_initialize_tote_aveva_api_page_v1` |
| Title | Initialize a Tote Using the Initialize Tote Aveva API Page |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tote_lifecycle_state` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Aveva API “Initialize Tote” page to initialize a tote for processing by entering BarcodeID/Code ID, StationID, and ToteID, submitting the request, and reading the on-screen Response field for confirmation or error/tote status (including AGV-related rejection conditions).

## When To Use

When you need to initialize a tote in the system using the Aveva API “Initialize Tote” page and you must verify success/failure from the Response field.

## Do Not Use For

* Do not proceed with additional configuration changes based only on the training segment; rely on the Response field’s error/tote status text to determine what happened.

## Access Or Tools Needed

* Access to the “Initialize Tote Aveva API” page (Aveva API interface)
* Ability to view and enter fields: BarcodeID, Code ID, StationID, ToteID
* Ability to click “Request to Initialize Tote” and read the “Response” field

## Related Operational Context

* ctx_training_video_initialize_tote_api_page_v1
* ctx_training_video_initialize_tote_fields_v1
* ctx_training_video_initialize_tote_response_v1
* ctx_training_video_initialize_tote_agv_limitation_v1

## Procedure Steps

### Step 1 — Open the “Initialize Tote Aveva API” page

**Responsible role:** L1_support

**Instruction:**
Navigate to and open the Aveva API “Initialize Tote” page that contains the BarcodeID, StationID, ToteID fields, the “Request to Initialize Tote” button, and the “Response” field.

**Expected result:**
The page loads and shows the input fields (BarcodeID, StationID, ToteID) and the “Request to Initialize Tote” button, with a visible “Response” field area.

**Stop or Escalate If:**

* If the page does not load or the “Response” field is not visible, stop and escalate.

---

### Step 2 — Enter the tote number into the BarcodeID field

**Responsible role:** L1_support

**Instruction:**
In the “BarcodeID” field, enter the tote’s barcode/tote number.

**Expected result:**
The “BarcodeID” field contains the tote number you intend to initialize.

**Stop or Escalate If:**

* If you cannot determine the correct tote number for BarcodeID, stop and escalate.

---

### Step 3 — Enter the same number into the Code ID field

**Responsible role:** L1_support

**Instruction:**
If the page includes a “Code ID” field, enter the same tote number value you used for BarcodeID.

**Expected result:**
The “Code ID” field (if present) contains the same number as “BarcodeID”.

**Stop or Escalate If:**

* If the page does not show a Code ID field, proceed with the remaining required fields (StationID and ToteID).

---

### Step 4 — Enter the StationID value

**Responsible role:** L1_support

**Instruction:**
In the “StationID” field, enter the StationID value for the rack/station (the source indicates StationID is shown in RMS).

**Expected result:**
The “StationID” field contains the correct station ID value.

**Stop or Escalate If:**

* If you cannot determine the correct StationID, stop and escalate.

---

### Step 5 — Enter the ToteID value

**Responsible role:** L1_support

**Instruction:**
In the “ToteID” field, enter the ToteID value for the tote you are initializing.

**Expected result:**
The “ToteID” field contains the tote ID value.

**Stop or Escalate If:**

* If you cannot determine the correct ToteID, stop and escalate.

---

### Step 6 — Click “Request to Initialize Tote”

**Responsible role:** L1_support

**Instruction:**
Click the “Request to Initialize Tote” button to submit the initialization request.

**Expected result:**
The system processes the request and updates the “Response” field with a confirmation message or an error message/tote status.

**Stop or Escalate If:**

* If the Response field does not provide a clear error/tote status, stop and escalate.
* If you cannot determine whether the failure is due to AGV-related conditions described by the source, stop and escalate.

---

### Step 7 — Observe the “Response” field after the request completes

**Responsible role:** L1_support

**Instruction:**
After the request completes, read the “Response” field to determine whether initialization succeeded (confirmation) or failed (error message and/or tote status).

**Expected result:**
Response field shows either: (a) a confirmation message for success, or (b) an error message and/or tote status explaining why initialization failed.

**Stop or Escalate If:**

* Stop and escalate if the Response field does not provide a clear error/tote status.
* Do not proceed with additional configuration changes based only on the training segment; rely on the Response field’s error/tote status text.

---

### Step 8 — Interpret AGV-related rejection and tote status from the Response field

**Responsible role:** L1_support

**Instruction:**
If the Response indicates initialization cannot be done, interpret the Response/tote status text using the AGV-related conditions described: totes on an AGV may be rejected; only AGVs not in the system or AGVs that have been removed are referenced as conditions that lead to a “can’t be initialized” response and a tote status explaining why.

**Expected result:**
When initialization fails, the Response field includes an error message and/or tote status text that indicates the reason, including AGV-related conditions (e.g., tote on an AGV rejection; AGV not in the system or removed AGV conditions).

**Stop or Escalate If:**

* Stop and escalate if the Response field does not provide a clear error/tote status.
* Stop and escalate if you cannot determine whether the failure is due to AGV-related conditions described by the source.

---

## Success Criteria

* Response field shows a confirmation message indicating the tote initialization request succeeded.

## Failure Conditions

* Response field does not provide a clear error/tote status.
* Response field indicates initialization cannot be done due to AGV-related conditions (totes on an AGV rejection; AGV not in the system or removed AGV conditions) and the tote status text does not clearly explain the reason.

## Escalation Guidance

* If the Response field does not provide a clear error/tote status, stop and escalate.
* If you cannot determine whether the failure is due to AGV-related conditions described by the source, stop and escalate.
* When escalating, include the exact text shown in the Response field (confirmation vs error/tote status).

## Missing Details / Known Gaps

* The packet does not specify the exact URL/navigation path to the “Initialize Tote Aveva API” page.
* The packet does not provide the exact UI label text for the “Code ID” field beyond stating it may be present and should match BarcodeID.

## Source Lineage

- Candidate IDs: candidate_training_video_d1_initialize_tote_aveva_api
- Source ID: `training_video_day1`
- Source Type: `training_video`
