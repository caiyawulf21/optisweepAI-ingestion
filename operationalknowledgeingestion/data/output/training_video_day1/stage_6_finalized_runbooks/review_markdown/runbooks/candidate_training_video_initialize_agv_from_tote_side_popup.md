# Initialize an AGV From the Tote Side Popup

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_initialize_an_agv_from_the_tote_side_popup_v1` |
| Title | Initialize an AGV From the Tote Side Popup |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the tote-side popup to initialize an AGV and specify the associated station ID when supported by the interface. The source confirms that AGV initialization is available from a tote-side popup and that station ID can be identified in RMS when selecting a cell, but it does not provide exact field names, button labels, or detailed confirmation behavior.

## When To Use

Use when support personnel need to initialize an AGV from the tote side using the popup interface and need to provide or verify a station ID as part of that workflow.

## Do Not Use For

* Do not use when the required AGV or station ID controls are not available in the popup.
* Do not use when the correct station ID cannot be confirmed from RMS.
* Do not use as a detailed error-handling procedure; the source does not provide confirmation messages or recovery steps.

## Safety And Operational Notes

* The source is a brief training mention and does not define full operator safety or permission boundaries for this action.
* Do not assume additional controls, confirmations, or recovery actions beyond what is shown in the source.

## Access Or Tools Needed

* Access to the tote side interface
* AGV initialization popup
* RMS access to view station ID when selecting a cell

## Related Operational Context

* ctx_training_video_initialize_agv_popup_v1
* ctx_training_video_station_id_reference_for_totes_v1

## Procedure Steps

### Step 1 — Open the tote-side AGV initialization popup

**Responsible role:** L1_support

**Instruction:**
Go to the tote side interface and open the popup used to initialize an AGV.

**Expected result:**
The AGV initialization popup is open and available for input.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*Reference frame associated with the training explanation that AGV initialization is performed from a tote-side popup.*


**Stop or Escalate If:**

* Escalate if the popup does not provide the needed AGV or station ID controls.

---

### Step 2 — Identify the AGV or tote-side item in the popup

**Responsible role:** L1_support

**Instruction:**
Identify the AGV or tote-side item to initialize using the controls available in the popup.

**Expected result:**
The intended AGV or tote-side item is selected or identified in the popup.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*Use the tote-side training reference to orient to the popup workflow; exact field names are not shown in the source.*


**Stop or Escalate If:**

* Escalate if the popup does not provide the needed AGV or station ID controls.

---

### Step 3 — Enter or select the station ID

**Responsible role:** L1_support

**Instruction:**
Enter or select the station ID when the popup requires a destination or station reference.

**Expected result:**
A station ID is populated in the popup when required by the workflow.

**Stop or Escalate If:**

* Escalate if the popup does not provide the needed AGV or station ID controls.
* Escalate if the correct station ID cannot be confirmed from RMS.

---

### Step 4 — Verify the station ID in RMS if needed

**Responsible role:** L1_support

**Instruction:**
Use the station ID shown in RMS when selecting a cell, if that is how the station ID is being verified in this workflow.

**Expected result:**
The station ID used for initialization matches the station ID shown in RMS.

**Stop or Escalate If:**

* Escalate if the correct station ID cannot be confirmed from RMS.

---

### Step 5 — Confirm initialization and verify interface response

**Responsible role:** L1_support

**Instruction:**
Confirm the initialization action in the popup and verify that the AGV has been initialized according to the interface response.

**Expected result:**
The AGV is initialized from the tote side with the intended station ID reference entered through the popup.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*General tote-side API/training reference associated with the initialization discussion; the source does not show exact confirmation text for AGV initialization.*


**Stop or Escalate If:**

* Escalate if the popup does not provide the needed AGV or station ID controls.
* Escalate if the correct station ID cannot be confirmed from RMS.
* Escalate if the interface does not provide a clear success indication or if initialization cannot be verified.

---

## Success Criteria

* The tote-side popup is accessible for AGV initialization.
* The intended AGV or tote-side item is identified in the popup.
* The required station ID is entered or selected when applicable.
* The station ID is confirmed from RMS when needed.
* The interface indicates the AGV has been initialized.

## Failure Conditions

* The popup does not provide the needed AGV or station ID controls.
* The correct station ID cannot be confirmed from RMS.
* The source does not provide detailed confirmation messages or error handling steps.
* Initialization cannot be verified from the interface response.

## Escalation Guidance

* Escalate if the popup does not provide the needed AGV or station ID controls.
* Escalate if the correct station ID cannot be confirmed from RMS.
* Escalate if the interface does not provide enough information to verify successful initialization.
* Escalate for SME review because the source is a brief training mention and does not define exact fields, buttons, or error handling.

## Missing Details / Known Gaps

* The source does not provide exact popup field names, button labels, or control names.
* The source does not specify how the AGV is selected within the popup.
* The source does not provide explicit success or error messages for AGV initialization.
* The source does not define detailed troubleshooting or rollback steps if initialization fails.
* The source does not define whether production stop or LOTO requirements apply.

## Source Lineage

- Candidate IDs: candidate_training_video_initialize_agv_from_tote_side_popup
- Source ID: `training_video_day1`
- Source Type: `training_video`
