# Interpret Overall System API Page Status And Available System-Level Functions

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_overall_system_api_page_status_and_available_system_level_functions_v1` |
| Title | Interpret Overall System API Page Status And Available System-Level Functions |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Overall System Aveva API page to identify the current System State and interpret the source-described meaning of the listed system-level functions shown on the left side of the page: System Startup, System Bag Out, System Shutdown, and System Purge.

## When To Use

Use when viewing the Overall System Aveva API page and needing to understand the current system state display and the documented meaning of the system-level functions shown on the left side of the page.

## Do Not Use For

* Do not use this runbook to execute startup, bag out, shutdown, or purge actions beyond interpreting their documented purpose.
* Do not use this runbook to infer undocumented behavior, corrective actions, or control logic not stated in the source.
* Do not use this runbook if the API page is not accessible or the expected fields and items are not visible.

## Safety And Operational Notes

* This is a reference/interpretation procedure derived from training content and does not authorize control actions.
* Do not invent additional actions or operational meaning beyond the source-provided descriptions.

## Access Or Tools Needed

* Access to the Overall System Aveva API page
* Visual access to the left-side system item list
* Training source or documented descriptions for the API page items

## Related Operational Context

* ctx_training_video_api_page_overview_v1
* ctx_training_video_system_state_reference_v1
* ctx_training_video_system_startup_agv_staging_v1
* ctx_training_video_bag_out_close_out_reference_v1
* ctx_training_video_system_shutdown_agv_charging_v1
* ctx_training_video_system_purge_reference_v1

## Procedure Steps

### Step 1 — Open or view the Overall System API page

**Responsible role:** operator

**Instruction:**
Open or view the Overall System Aveva API page referred to in the training as the API page. Confirm the page shown is the Overall System page with the left-side list of system items.

**Expected result:**
The Overall System Aveva API page is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*Overall System Aveva API page and the left-side list of system items.*


**Stop or Escalate If:**

* The API page is not accessible.
* The expected Overall System page or left-side system items are not visible.

---

### Step 2 — Read the System State field

**Responsible role:** operator

**Instruction:**
Locate the System State field on the page and read the current state shown.

**Expected result:**
The current system state is identified from the System State field.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*System State field on the Overall System Aveva API page.*


**Stop or Escalate If:**

* The System State field is not visible.
* The displayed state cannot be read or interpreted from the page.

---

### Step 3 — Identify the listed system-level items

**Responsible role:** operator

**Instruction:**
Identify the listed system-level items on the left side of the page: System Startup, System Bag Out, System Shutdown, and System Purge.

**Expected result:**
The four listed system-level items are identified on the page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*Left-side list showing System Startup, System Bag Out, System Shutdown, and System Purge.*


**Stop or Escalate If:**

* One or more expected system-level items are missing from view.

---

### Step 4 — Interpret each listed function using the source descriptions

**Responsible role:** operator

**Instruction:**
Use the source-provided descriptions to interpret each item: System Startup stages AGVs for exchanges; System Bag Out or close out closes all chutes and exchanges totes with items; System Shutdown puts the system into a shutdown state for AGVs to rotate on the charger; and System Purge exchanges all totes and does not print a label at the tipper.

**Expected result:**
Each listed function is interpreted according to the source-provided description.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*The listed functions on the left side of the Overall System API page and their associated training descriptions.*


**Stop or Escalate If:**

* You are being asked to infer behavior or corrective actions not stated in the source.
* The displayed function names do not match the source-described items.

---

### Step 5 — Record or communicate the displayed state and function meaning

**Responsible role:** operator

**Instruction:**
Record or communicate the displayed system state and the documented meaning of the relevant function without inventing additional actions beyond the source.

**Expected result:**
The current system state and relevant function meaning are communicated or documented using only source-supported descriptions.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*Displayed System State and the listed system-level functions being referenced for communication.*


**Stop or Escalate If:**

* You cannot access the page to verify the displayed state.
* You would need to add undocumented behavior or corrective guidance to answer the request.

---

## Success Criteria

* The Overall System Aveva API page is identified correctly.
* The current System State is read from the page.
* The listed system-level items are identified as System Startup, System Bag Out, System Shutdown, and System Purge.
* The meaning of each listed function is interpreted using only the source-provided descriptions.
* The displayed state and relevant function meaning are recorded or communicated without unsupported additions.

## Failure Conditions

* The API page is not accessible.
* The expected fields or listed items are not visible.
* The System State field cannot be read.
* The user attempts to infer undocumented behavior or corrective actions beyond the source.

## Escalation Guidance

* Escalate if the API page is not accessible or the expected fields and items are not visible.
* Escalate if the displayed page content does not match the training-described Overall System API page.
* Do not provide undocumented behavior or corrective actions; seek SME clarification if more detail is required.

## Missing Details / Known Gaps

* The source does not provide exact navigation steps to open the Overall System Aveva API page.
* The source does not provide button-press execution steps for startup, bag out, shutdown, or purge in this segment.
* The source does not provide a time estimate for this reference procedure.
* The source does not specify supporting roles beyond the operator audience.
* The source does not define exact escalation contacts or routing.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_api_page_system_state_and_functions
- Source ID: `training_video_day1`
- Source Type: `training_video`
