# Determine Why A Tote Was Sent To The Hospital Station Using The Green Scanner

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_determine_why_a_tote_was_sent_to_the_hospital_station_using_the_green_scanner_v1` |
| Title | Determine Why A Tote Was Sent To The Hospital Station Using The Green Scanner |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the hospital station stacklight and green scanner to confirm tote presence and determine why a tote was brought to the hospital station.

## When To Use

Use when an operator needs to identify why a tote was brought to the hospital station and the source indicates the hospital station stacklight and green scanner are used for that purpose.

## Do Not Use For

* Detailed tote handling, removal, or reinsertion procedures not explicitly provided in this source section
* Any scanner workflow requiring exact scan target, button sequence, or field interpretation not specified in the source

## Safety And Operational Notes

* Use only the source-supported diagnostic actions in this runbook.
* Do not perform additional tote handling or system control actions unless directed by a separate source-supported procedure.

## Access Or Tools Needed

* Access to the hospital station
* Green scanner
* Ability to observe the hospital station stacklight

## Related Operational Context

* ctx_manual_hospital_station_presence_and_scanner_v1

## Procedure Steps

### Step 1 — Verify tote presence at the hospital station

**Responsible role:** operator

**Instruction:**
At the hospital station, observe the stacklight indication to verify that a tote is present.

**Expected result:**
The operator confirms from the stacklight that a tote is present at the hospital station.

**Screens / Images:**

![artifact_fig_3_6_stacklight](assets/artifact_fig_3_6_stacklight.png)

*Hospital station stacklight indication meanings, including flashing yellow for 15 seconds meaning an AGV is present at either position of the station.*


**Stop or Escalate If:**

* The stacklight does not indicate a tote/AGV present at the station
* The stacklight shows fault or RMS error indications
* The indication is indeterminate and the operator cannot confirm tote presence

---

### Step 2 — Use the green scanner to determine the tote reason

**Responsible role:** operator

**Instruction:**
Use the green scanner at the hospital station on the tote or station process as documented by the source to determine the reason the tote was brought there.

**Expected result:**
The scanner-supported hospital station process provides the reason the tote was brought to the station.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station operation context showing the tote barcode is scanned using the green scanner and the Tote ID field auto-populates.*

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*Status information fields that tell the station operator why the tote is there, what menu they need to use, and what action they need to perform.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen.png)

*Example mismatch condition screen associated with a tote sent to the hospital station because the scanned bar code did not match the tote ID expected by the WCS.*

![artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen](assets/artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen.png)

*Example no-read condition screen associated with a tote sent to the hospital station because the bar code could not be scanned.*

![artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen](assets/artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen.png)

*Example failed-to-empty condition screen where the green scanner is used to scan the tote bar code.*

![artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen](assets/artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen.png)

*Example sent-from-bagging-station condition screen where the green scanner populates Tote ID and Bar Code fields.*

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*Reference example showing green scanner use to populate Tote ID and Barcode fields.*


**Stop or Escalate If:**

* The scanner does not provide a reason for the tote at the hospital station
* The operator cannot determine the required scan target or scanner interaction from the source
* The displayed reason or status cannot be interpreted from the available source material

---

### Step 3 — Read and record the returned reason

**Responsible role:** operator

**Instruction:**
Read the reason returned by the scanner-supported hospital station process and record that reason for the tote.

**Expected result:**
The operator has identified and recorded the reason the tote was brought to the hospital station.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*Status fields that explain why the tote is there and what action is needed.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen.png)

*Example of a specific reason category: bar code mismatch.*

![artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen](assets/artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen.png)

*Example of a specific reason category: no read bar code.*

![artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen](assets/artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen.png)

*Example of a specific reason category: tote failed to empty.*

![artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen](assets/artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen.png)

*Example of a specific reason category: sent from bagging station.*


**Stop or Escalate If:**

* The scanner or associated station process does not provide a reason
* The reason cannot be interpreted from the available status information
* The source does not provide enough detail to continue to the next handling action

---

## Success Criteria

* The operator confirms tote presence at the hospital station.
* The green scanner-supported process yields the reason the tote was brought to the station.
* The reason is read and recorded by the operator.

## Failure Conditions

* The stacklight does not confirm tote presence.
* The scanner does not provide a reason for the tote.
* The source does not specify enough scanner interaction detail to complete a more detailed procedure.
* The returned reason cannot be interpreted from the available source-supported information.

## Escalation Guidance

* Escalate if the scanner does not provide a reason for the tote at the hospital station.
* Escalate for SME review because the source does not specify the scanner interaction details, scan target, or displayed fields.
* Escalate if the stacklight indicates a fault or RMS error instead of normal presence.

## Missing Details / Known Gaps

* The source does not specify the exact scanner interaction details.
* The source does not specify the exact scan target for determining the tote reason.
* The source does not specify the exact displayed fields returned by the scanner interaction in the cited section.
* The source does not define the exact recording method for the returned reason.
* The source does not provide a time estimate for this procedure.

## Source Lineage

- Candidate IDs: candidate_operator_determine_hospital_station_tote_reason_with_green_scanner
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
