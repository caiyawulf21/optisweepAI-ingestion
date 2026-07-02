# Verify That a Tipper Alarm Results in a Hospital Request to WCS

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_that_a_tipper_alarm_results_in_a_hospital_request_to_wcs_v1` |
| Title | Verify That a Tipper Alarm Results in a Hospital Request to WCS |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Hospital HMI alarm text and the documented alarm table entries to determine whether a current tipper alarm is explicitly identified as causing a Hospital request to the WCS or as causing the WCS to send the AGV/tote to the hospital for diagnosis.

## When To Use

Use when a tipper alarm is displayed and you need to verify from the source manual whether that alarm is one of the documented conditions that results in a Hospital request to the WCS.

## Do Not Use For

* Do not use to infer hospital-request behavior when the table does not explicitly state that a Hospital request is sent to the WCS or that WCS will send the AGV/tote to the hospital for diagnosis.
* Do not use as a downstream recovery or routing procedure; the source only supports identification of documented hospital-request alarm conditions.

## Safety And Operational Notes

* This is a reference/verification procedure only.
* Do not infer that an alarm sends a Hospital request unless the table explicitly states it.

## Access Or Tools Needed

* Access to the Hospital HMI alarm text
* Table 4-23 Alarms and Corrective Actions

## Related Operational Context

* ctx_manual_hospital_hmi_alarms_screen_v1

## Procedure Steps

### Step 1 — Read the displayed tipper alarm text

**Responsible role:** L1_support

**Instruction:**
Open or view the Hospital HMI alarm list and read the displayed tipper alarm text exactly as shown, including the associated time-stamped entry if needed for identification.

**Expected result:**
The current alarm text is identified from the Hospital HMI alarm list.

**Screens / Images:**

![artifact_fig_4_42_hospital_hmi_alarms_screen](assets/artifact_fig_4_42_hospital_hmi_alarms_screen.jpeg)

*The Hospital HMI alarms list and associated time stamps to identify the exact displayed tipper alarm text.*


**Stop or Escalate If:**

* The alarm text is missing or unreadable on the HMI.
* The displayed alarm cannot be confidently identified from the alarm list.

---

### Step 2 — Match the alarm text to documented hospital-request entries

**Responsible role:** L1_support

**Instruction:**
Compare the displayed alarm text to the documented Left Tipper alarm entries in Table 4-23. Look specifically for entries whose documentation states that a Hospital request is sent to the WCS or that WCS will send the AGV/tote to the hospital for diagnosis.

**Expected result:**
A documented match is found, or it is determined that no explicit hospital-request statement is present for the displayed alarm.

**Screens / Images:**

![artifact_fig_4_42_hospital_hmi_alarms_screen](assets/artifact_fig_4_42_hospital_hmi_alarms_screen.jpeg)

*The exact alarm text in the Hospital HMI alarm list for comparison to the documented table entries.*


**Stop or Escalate If:**

* The alarm appears related to hospital routing but no matching table entry can be found.
* The table entry is incomplete or unclear about whether hospital-request behavior occurs.
* The alarm text does not exactly align with a documented entry and would require inference.

---

### Step 3 — Confirm the documented cause and controller response

**Responsible role:** L1_support

**Instruction:**
For the matched alarm row in Table 4-23, review the Cause and Controller Response fields and confirm that the documented response explicitly states that a Hospital request is sent to the WCS or that WCS will send the AGV/tote to the hospital for diagnosis.

**Expected result:**
The matched row's documented Cause and Controller Response confirm whether hospital-request behavior is explicitly supported by the source.

**Stop or Escalate If:**

* The Cause or Controller Response fields are missing, incomplete, or unclear.
* The alarm seems related but the documented response does not explicitly state hospital-request behavior.

---

### Step 4 — Record whether the alarm is a documented hospital-request condition

**Responsible role:** L1_support

**Instruction:**
Record that the alarm is a documented hospital-request condition only when the matched table entry explicitly states that response. If the source does not explicitly state it, record that the condition is not confirmed by this reference and escalate if clarification is needed.

**Expected result:**
The verification result is documented as confirmed, not confirmed, or requiring escalation based on the source wording.

**Screens / Images:**

![artifact_fig_4_42_hospital_hmi_alarms_screen](assets/artifact_fig_4_42_hospital_hmi_alarms_screen.jpeg)

*The displayed alarm entry being verified before recording the result.*


**Stop or Escalate If:**

* The table entry is missing, incomplete, or unclear.
* The alarm appears related to hospital routing but the source does not explicitly confirm it.
* A determination would require inference beyond the documented wording.

---

## Success Criteria

* The displayed tipper alarm is compared against the documented entries in Table 4-23.
* A determination is made only when the source explicitly states that a Hospital request is sent to the WCS or that WCS will send the AGV/tote to the hospital for diagnosis.
* The verification result is recorded without inference.

## Failure Conditions

* The alarm text cannot be clearly identified from the HMI.
* No matching documented entry is found.
* The table entry is missing, incomplete, or unclear.
* The source does not explicitly state hospital-request behavior for the alarm under review.

## Escalation Guidance

* Escalate if the alarm appears related to hospital routing but the table entry is missing, incomplete, or unclear.
* Escalate if a determination would require inference rather than explicit source wording.

## Missing Details / Known Gaps

* The packet does not provide the full text of Table 4-23 alarm rows, including exact alarm names, causes, and controller responses for every hospital-request condition.
* The source packet does not provide a documented recording location or system of record for saving the verification result.
* The packet does not provide explicit Hospital HMI navigation steps to open the Alarms screen beyond related artifact context.

## Source Lineage

- Candidate IDs: candidate_verify_hospital_request_alarm_conditions_for_tipper
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
