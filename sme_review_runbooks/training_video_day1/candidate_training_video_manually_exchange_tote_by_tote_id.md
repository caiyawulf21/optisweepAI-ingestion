# Manually Exchange a Tote by Tote ID

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_manually_exchange_a_tote_by_tote_id_v1` |
| Title | Manually Exchange a Tote by Tote ID |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the tote management Exchange Tote function to manually trigger a tote exchange for a specific tote by entering its tote ID. The training states that any tote on the system can be manually exchanged and shows Exchange Tote as a tote management API feature.

## When To Use

Use when a knowledgeable support user needs to manually trigger a tote exchange for a specific tote and the tote ID is known.

## Do Not Use For

* Do not use when the tote ID cannot be confirmed from the available system information.
* Do not use as a fully validated recovery workflow; the source presents the function and its purpose but does not define detailed safeguards or validation steps.

## Safety And Operational Notes

* This is a live state-changing action.
* The source states the function can be used for testing, but does not provide additional safeguards, approval requirements, or validation controls.
* Do not proceed if the tote ID cannot be confidently confirmed.

## Access Or Tools Needed

* Access to tote management interface or API-backed Exchange Tote function
* Tote ID
* Ability to review tote status or task response

## Related Operational Context

* ctx_training_video_manual_tote_exchange_reference_v1
* ctx_training_video_tote_management_api_overview_v1

## Procedure Steps

### Step 1 — Identify the tote ID

**Responsible role:** L1_support

**Instruction:**
Identify and confirm the tote ID for the tote that needs to be manually exchanged before opening the Exchange Tote function.

**Expected result:**
A specific tote ID is available for entry into the Exchange Tote function.

**Stop or Escalate If:**

* Escalate if the tote ID cannot be confirmed.

---

### Step 2 — Open the Exchange Tote function

**Responsible role:** L1_support

**Instruction:**
Open the tote management interface or API page and select the Exchange Tote function.

**Expected result:**
The Exchange Tote function is open and ready for tote ID entry.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management API page listing Exchange Tote among the available tote management features.*


**Stop or Escalate If:**

* Stop if the Exchange Tote function is not visible or accessible from the tote management page.

---

### Step 3 — Enter the tote ID

**Responsible role:** L1_support

**Instruction:**
Enter the confirmed tote ID into the Exchange Tote function.

**Expected result:**
The Exchange Tote function contains the tote ID for the tote to be exchanged.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The Exchange Tote function on the tote management page, which the training describes as operating by tote ID.*


**Stop or Escalate If:**

* Stop if there is uncertainty that the entered tote ID matches the intended tote.

---

### Step 4 — Submit the manual exchange

**Responsible role:** L1_support

**Instruction:**
Submit the Exchange Tote action after entering the tote ID.

**Expected result:**
A manual tote exchange is triggered for the specified tote ID.

**Stop or Escalate If:**

* Escalate if the exchange action does not complete or the tote remains in the original state.

---

### Step 5 — Verify the exchange was triggered

**Responsible role:** L1_support

**Instruction:**
Verify through the available tote status or system response that the tote exchange was triggered.

**Expected result:**
The system response or tote status indicates that the manual exchange was triggered for the specified tote.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management page features such as Get Tote Task or related tote management functions that indicate available status or response review capability.*


**Stop or Escalate If:**

* Escalate if the exchange action does not complete or the tote remains in the original state.

---

## Success Criteria

* The Exchange Tote function is accessed successfully.
* The intended tote ID is entered.
* The manual exchange action is submitted.
* Available tote status or system response indicates the exchange was triggered for the specified tote.

## Failure Conditions

* The tote ID cannot be confirmed.
* The Exchange Tote function cannot be accessed.
* The exchange action does not complete.
* The tote remains in the original state after submission.
* The source does not provide detailed safeguards or validation steps beyond basic status/response verification.

## Escalation Guidance

* Escalate if the tote ID cannot be confirmed.
* Escalate if the exchange action does not complete or the tote remains in the original state.
* Escalate to SME review if additional safeguards, approvals, or validation steps are required because the source does not define them.

## Missing Details / Known Gaps

* The source does not provide the exact button label or submission control used to execute Exchange Tote.
* The source does not provide the exact verification screen, field, or response message that confirms success.
* The source does not define approval requirements, rollback steps, or production impact constraints for this action.
* The source does not provide a time estimate for completing the procedure.

## Source Lineage

- Candidate IDs: candidate_training_video_manually_exchange_tote_by_tote_id
- Source ID: `training_video_day1`
- Source Type: `training_video`
