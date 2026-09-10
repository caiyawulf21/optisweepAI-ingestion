# Use Aveva API tote management to exchange a tote by tote ID or lane number

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_aveva_api_tote_exchange_by_tote_or_lane_v1` |
| Title | Use Aveva API tote management to exchange a tote by tote ID or lane number |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tote_exchange_sequence` |
| Access Surface | `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Manually trigger a tote exchange using the Aveva API tote management page, either by specifying a tote ID (Exchange Tote) or by specifying a lane number (Exchange Lane). The lane-number format requires adding a leading zero (example: 3050 -> 03050).

## When To Use

Use when you need to manually trigger a tote exchange to remove/correct a tote state in the system using the Aveva API tote management functions: “Exchange Tote” (by tote Id) or “Exchange Lane” (by lane number with a leading zero).

## Do Not Use For

* Do not use this procedure if the system issue is not related to tote exchange (the source frames this as a way to remove a tote from the system / correct tote state).

## Access Or Tools Needed

* Aveva API page for tote management (API Features for Tote Management)
* Tote Id or lane number (lane number requires adding a zero per the source example)

## Related Operational Context

* ctx_training_video_tote_management_api_overview_v1
* ctx_training_video_manual_tote_exchange_reference_v1

## Procedure Steps

### Step 1 — Open the Aveva API tote management page (API Features for Tote Management)

**Responsible role:** L2_support

**Instruction:**
Open the Aveva API page for tote management that contains the “API Features for Tote Management” section with the “Exchange Tote” and “Exchange Lane” functions.

**Expected result:**
The Aveva API tote management page is visible and shows the “Exchange Tote” and “Exchange Lane” controls under “API Features for Tote Management”.

**Stop or Escalate If:**

* If you cannot access the Aveva API tote management page or cannot locate the “Exchange Tote” / “Exchange Lane” controls, stop and escalate to support.

---

### Step 2 — Exchange a specific tote using “Exchange Tote” (by tote Id)

**Responsible role:** L2_support

**Instruction:**
On the Aveva API tote management page, use the “Exchange Tote” function and provide the tote Id.

**Expected result:**
A manual tote exchange is triggered for the specified tote Id via the “Exchange Tote” function.

**Stop or Escalate If:**

* If the exchange cannot be triggered or the API does not return an acceptance/confirmation, stop and escalate to support.

---

### Step 3 — Exchange by lane using “Exchange Lane” (lane number with leading zero)

**Responsible role:** L2_support

**Instruction:**
On the Aveva API tote management page, use the “Exchange Lane” function and provide the lane number, adding a leading zero to the lane number format (example given: 3050 -> 03050).

**Expected result:**
A manual tote exchange is triggered for the specified lane number via the “Exchange Lane” function using the leading-zero lane format.

**Stop or Escalate If:**

* If the exchange cannot be triggered or the API does not return an acceptance/confirmation, stop and escalate to support.

---

### Step 4 — Submit/execute the exchange action from the API page

**Responsible role:** L2_support

**Instruction:**
Execute/submit the exchange action from the Aveva API tote management page after entering the tote Id (Exchange Tote) or lane number (Exchange Lane).

**Expected result:**
The exchange request is submitted from the API page.

**Stop or Escalate If:**

* If the exchange cannot be triggered or the API does not return an acceptance/confirmation, stop and escalate to support.

---

### Step 5 — Verify the exchange request was accepted (API page response/output)

**Responsible role:** L2_support

**Instruction:**
Observe the Aveva API tote management page output/response area for the exchange action and confirm it returns acceptance/confirmation.

**Expected result:**
The API page shows an acceptance/confirmation output for the exchange action.

**Stop or Escalate If:**

* If the exchange cannot be triggered or the API does not return an acceptance/confirmation, stop and escalate to support.

---

## Success Criteria

* A manual tote exchange is triggered for the specified tote Id via “Exchange Tote”, or for the specified lane number (with leading zero) via “Exchange Lane”.
* The Aveva API tote management page returns acceptance/confirmation output for the exchange action.

## Failure Conditions

* Exchange cannot be triggered from the Aveva API tote management page.
* The API does not return acceptance/confirmation output for the exchange action.
* Lane number formatting is incorrect (lane number not entered with leading zero as required by the source example).

## Escalation Guidance

* If the exchange cannot be triggered or the API does not return acceptance/confirmation, stop and escalate to support.

## Missing Details / Known Gaps

* Exact UI control name for the submit/execute button/link for the exchange action is not explicitly captured in the provided OCR/transcript; the candidate requested screenshot support for the trigger button and response area.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_aveva_api_exchange_tote
- Source ID: `training_video_day1`
- Source Type: `training_video`
