# Manually Exchange a Tote by Lane Number

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_manually_exchange_a_tote_by_lane_number_v1` |
| Title | Manually Exchange a Tote by Lane Number |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the tote management Exchange Lane function to manually trigger a tote exchange by lane number. The training source explicitly states lane-based exchange is supported and provides a formatting example where a lane such as 3050 is entered as 03050.

## When To Use

Use when a manual tote exchange needs to be triggered by lane number through the tote management interface or API-backed Exchange Lane function, and the operator has the lane number to enter in the documented format example.

## Do Not Use For

* Do not use this runbook to exchange by tote ID; this runbook is specific to lane-number entry.
* Do not assume lane formats beyond the documented example; the source provides only one example of adding a leading zero.
* Do not use this runbook as a complete troubleshooting guide for failed exchange requests; the source does not define full error handling or all valid input formats.

## Safety And Operational Notes

* The source describes this as a support/operator interface action and does not specify lockout/tagout or production-stop requirements.
* Do not invent alternate lane-number formatting rules beyond the documented example from the training source.

## Access Or Tools Needed

* Access to tote management interface or API-backed Exchange Lane function
* Lane number

## Related Operational Context

* ctx_training_video_manual_tote_exchange_reference_v1
* ctx_training_video_tote_management_api_overview_v1

## Procedure Steps

### Step 1 — Identify the lane number

**Responsible role:** L1_support

**Instruction:**
Identify the lane number for the destination or lane to exchange.

**Expected result:**
A lane number is available for entry.

**Stop or Escalate If:**

* Escalate if the lane number cannot be identified.

---

### Step 2 — Format the lane number with the documented leading zero example

**Responsible role:** L1_support

**Instruction:**
Convert the lane number to the documented format by adding a leading zero when needed, such as 3050 to 03050.

**Expected result:**
The lane number is formatted according to the documented example.

**Stop or Escalate If:**

* Escalate if the lane number format is not accepted.
* Escalate if the correct lane format cannot be determined beyond the single documented example.

---

### Step 3 — Open the Exchange Lane function

**Responsible role:** L1_support

**Instruction:**
Open the Exchange Lane function in the tote management interface or API page.

**Expected result:**
The Exchange Lane function is visible and ready for input.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*API Features for Tote Management list showing Exchange Lane among the available functions.*


**Stop or Escalate If:**

* Escalate if the Exchange Lane function is not available in the tote management page.

---

### Step 4 — Enter the formatted lane number

**Responsible role:** L1_support

**Instruction:**
Enter the formatted lane number.

**Expected result:**
The formatted lane number is populated in the Exchange Lane input.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management API page context where Exchange Lane is available for lane-number entry.*


**Stop or Escalate If:**

* Escalate if the lane number format is not accepted.

---

### Step 5 — Submit the exchange and verify the response

**Responsible role:** L1_support

**Instruction:**
Submit the manual exchange action and verify through the available system response that the lane-based exchange was triggered.

**Expected result:**
A manual tote exchange is triggered using the specified lane number in the expected format.

**Screens / Images:**

![artifact_training_video_training_video_day1_0069_on_the_tote_side_you_can_primary_02_22_24_000](assets/61f88215d8f9bba4.jpg)

*The tote management API page showing Exchange Lane as the function being used for the manual exchange request.*


**Stop or Escalate If:**

* Escalate if the exchange does not trigger after entering the formatted lane number.
* Escalate if the available system response does not confirm the lane-based exchange was triggered.

---

## Success Criteria

* The Exchange Lane function is accessed from the tote management page.
* The lane number is entered using the documented format example.
* The available system response indicates the lane-based manual exchange was triggered.

## Failure Conditions

* The lane number cannot be identified.
* The lane number format is not accepted.
* The Exchange Lane function is unavailable.
* The exchange does not trigger after the formatted lane number is entered.
* The source does not define all valid lane-number formats or detailed failure responses.

## Escalation Guidance

* Escalate if the lane number format is not accepted.
* Escalate if the exchange does not trigger after entering the formatted lane number.
* Escalate if the Exchange Lane function is not available in the tote management page.
* Escalate when a lane format other than the documented leading-zero example is required, because the source does not define all valid lane formats.

## Missing Details / Known Gaps

* The source does not provide the exact button label or submission control used to execute Exchange Lane.
* The source does not show the exact input field name for the lane number.
* The source provides only one lane-formatting example and does not define all valid lane-number formats.
* The source does not define the exact success message, error message, or response text for a completed lane exchange.
* The source does not specify estimated completion time, production-stop requirements, or LOTO requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_manually_exchange_tote_by_lane_number
- Source ID: `training_video_day1`
- Source Type: `training_video`
