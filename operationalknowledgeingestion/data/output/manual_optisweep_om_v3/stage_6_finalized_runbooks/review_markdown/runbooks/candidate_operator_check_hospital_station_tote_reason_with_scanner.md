# Identify Why A Tote Was Sent To The Hospital Station

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_why_a_tote_was_sent_to_the_hospital_station_v1` |
| Title | Identify Why A Tote Was Sent To The Hospital Station |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the hospital station stacklight and green scanner to confirm a tote is present and determine the reason it was brought to the hospital station.

## When To Use

Use this procedure when a tote has been sent to the hospital station and the operator needs to confirm tote presence and determine why the tote was brought there for manual handling.

## Do Not Use For

* Do not use this runbook to interpret scanner codes, status values, or HMI fields beyond determining the reason, because the source does not provide those details.
* Do not use this runbook as a complete tote handling, removal, add-back, or manual bagging procedure.

## Safety And Operational Notes

* The source states the tote is manually handled by an operator at the hospital station.
* Do not invent or apply unsupported follow-up handling steps, scanner interpretations, or controls not described in the source.

## Access Or Tools Needed

* Access to the hospital station
* Visual access to the hospital station stacklight
* Green scanner

## Related Operational Context

* ctx_manual_hospital_station_overview_v1

## Procedure Steps

### Step 1 — Go to the hospital station and check for tote presence indication

**Responsible role:** operator

**Instruction:**
Go to the hospital station and observe the station indication that shows a tote is present.

**Expected result:**
The operator identifies whether the station indicates a tote is present.

**Screens / Images:**

![artifact_fig_3_5_hospital_station](assets/artifact_fig_3_5_hospital_station.png)

*Use the hospital station photo to identify the station and its stacklight context.*

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Use the hospital station operation artifact as supporting visual context for hospital station tote handling.*


**Stop or Escalate If:**

* The station does not indicate a tote is present when one is expected.
* The observed station condition does not match the expected hospital station condition.

---

### Step 2 — Confirm the tote is on the operator-right side of the hospital station

**Responsible role:** operator

**Instruction:**
Confirm the AGV has brought the tote to the right side of the hospital station from the operator's perspective.

**Expected result:**
The operator confirms the tote is positioned on the right side of the hospital station.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Use the hospital station operation artifact for visual context on AGV tote delivery and station sides.*


**Stop or Escalate If:**

* The tote is not on the right side of the hospital station from the operator's perspective.
* The tote presence or position does not match the expected hospital station condition.

---

### Step 3 — Use the green scanner to determine the reason for hospital station routing

**Responsible role:** operator

**Instruction:**
Use the green scanner at the hospital station to determine the reason the tote was brought to the station.

**Expected result:**
The scanner provides the reason the tote was brought to the hospital station.

**Screens / Images:**

![artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen](assets/artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen.png)

*Use as an example of a hospital station exception screen related to a no-read barcode condition.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen.png)

*Use as an example of a hospital station exception screen related to barcode mismatch.*

![artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen](assets/artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen.png)

*Use as an example of a hospital station exception screen related to tote failed to empty.*

![artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen](assets/artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen.png)

*Use as an example of a hospital station screen associated with a sent-from-bagging-station condition.*


**Stop or Escalate If:**

* The scanner does not provide a reason.
* The source-supported scanner interaction is insufficient to determine the reason.

---

### Step 4 — Record or communicate the reported reason

**Responsible role:** operator

**Instruction:**
Record or communicate the reason reported by the scanner for manual handling of the tote.

**Expected result:**
The reason is captured or communicated for the next action outside this runbook.

**Stop or Escalate If:**

* The scanner-reported reason is unavailable or unclear.
* Follow-up handling requires details not provided by the source.

---

## Success Criteria

* The operator confirms a tote is present at the hospital station.
* The operator confirms the tote is on the right side of the hospital station from the operator's perspective.
* The operator determines the reason the tote was brought to the hospital station using the green scanner.
* The reason is recorded or communicated for manual handling.

## Failure Conditions

* The hospital station does not indicate a tote is present when expected.
* The tote is not on the expected side of the hospital station.
* The green scanner does not provide a reason.
* The source does not provide enough detail to continue with interpretation or follow-up handling.

## Escalation Guidance

* Escalate if the scanner does not provide a reason.
* Escalate if tote presence does not match the expected hospital station condition.
* Escalate if follow-up handling depends on scanner screens, codes, or interpretation details not provided in the source.

## Missing Details / Known Gaps

* The source does not provide scanner screens, scanner codes, or exact scanner interaction details for determining the reason.
* The source does not define the exact stacklight state to use for this specific tote-present confirmation in this procedure.
* The source does not provide required follow-up handling steps after the reason is identified.
* The source does not provide a formal recording method, destination, or communication channel for the identified reason.
* The source does not provide an estimated completion time.

## Source Lineage

- Candidate IDs: candidate_operator_check_hospital_station_tote_reason_with_scanner
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
