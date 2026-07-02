# Handle A Tote At The Hospital Station And Return An Empty Tote To The AGV

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_handle_a_tote_at_the_hospital_station_and_return_an_empty_tote_to_the_agv_v1` |
| Title | Handle A Tote At The Hospital Station And Return An Empty Tote To The AGV |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Operator procedure for responding to a tote delivered to the hospital station, confirming tote presence, using the green scanner and hospital station information to determine why the tote was sent there, manually handling the tote at the station, and placing an empty tote on the AGV so it can return to the sorter area.

## When To Use

Use when a tote has been directed to the hospital station for manual handling. The source states this occurs in the event of a mis-sort, bad tip, or tote overload, and that the operator uses the hospital station indication and green scanner to determine why the tote was brought to the station.

## Do Not Use For

* Do not use as a detailed corrective procedure for specific issue types such as mis-sort, bad tip, tote overload, no-read bar code, bar code mismatch, tote failed to empty, or sent from bagging station when source-specific handling details are required but not provided in this packet.
* Do not use when the tote is not present at the hospital station or the AGV does not complete the documented right-side then left-side positioning sequence.

## Safety And Operational Notes

* Use only the documented operator interaction at the hospital station from this source packet.
* The source does not provide detailed manual handling steps for each tote exception type; obtain SME guidance if the required task is not clear from the station status or scanner result.
* Stop and escalate if the scanner does not provide the reason the tote was brought to the station or if the AGV does not complete the documented positioning sequence.

## Access Or Tools Needed

* Access to the hospital station
* Green scanner
* An empty tote
* Ability to observe AGV position relative to the operator

## Related Operational Context

* ctx_manual_hospital_station_overview_v1
* ctx_manual_hospital_station_presence_and_scanner_v1
* ctx_manual_hospital_station_agv_positioning_v1

## Procedure Steps

### Step 1 — Go to the hospital station and verify tote presence

**Responsible role:** operator

**Instruction:**
Go to the hospital station and verify that a tote is present by checking the station indication for tote presence.

**Expected result:**
The operator confirms that a tote is present at the hospital station.

**Screens / Images:**

![artifact_fig_3_6_stacklight](assets/artifact_fig_3_6_stacklight.png)

*Hospital station stacklight indication used to identify station and AGV presence/status.*

![artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen](assets/artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen.png)

*Hospital HMI example for a tote that must be handled manually at the hospital station when a tote bar code cannot be read at the Operator Station.*


**Stop or Escalate If:**

* The operator cannot confirm tote presence at the hospital station.
* The station indication does not support proceeding with manual handling.

---

### Step 2 — Use the green scanner to determine why the tote was sent to the station

**Responsible role:** operator

**Instruction:**
Use the green scanner and available hospital station status information to determine the reason the tote was brought to the hospital station.

**Expected result:**
The operator identifies why the tote was sent to the hospital station.

**Screens / Images:**

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/artifact_fig_4_30_hospital_hmi_operations_screen.png)

*Status messages and WCS-provided information that tell the operator why the tote is there and what action to perform.*

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station operation context showing scanner use and status-driven handling.*

![artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen](assets/artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen.png)

*Example exception screen for a no-read bar code condition.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen.png)

*Example exception screen for a bar code mismatch condition.*

![artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen](assets/artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen.png)

*Example exception screen for a tote failed to empty condition.*

![artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen](assets/artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen.png)

*Example exception screen for a sent from bagging station condition.*


**Stop or Escalate If:**

* The scanner does not provide the reason the tote was brought to the station.
* The station status does not make the required operator action clear.

---

### Step 3 — Manually handle the tote at the hospital station

**Responsible role:** operator

**Instruction:**
Manually handle the tote at the hospital station according to the reason identified by the scanner and hospital station status information.

**Expected result:**
The tote is manually handled at the hospital station as required.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station operation context for extracting and handling the tote.*

![artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen](assets/artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen.png)

*Example exception context where the operator must manually bag items and print the correct bag label.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen.png)

*Example exception context where the operator must manually bag items and print the correct bag label.*

![artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen](assets/artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen.png)

*Example exception context where the operator removes the tote from the system so the required task can be performed.*

![artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen](assets/artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen.png)

*Example exception context where the operator removes the tote from the system so the required task can be performed.*


**Stop or Escalate If:**

* The source does not provide enough detail to perform the required manual handling safely or correctly.
* The identified tote condition requires a more specific procedure than is available in this packet.

---

### Step 4 — Observe AGV delivery on the right side of the hospital station

**Responsible role:** operator

**Instruction:**
Observe that the AGV brings the tote to the right side of the hospital station from the operator perspective.

**Expected result:**
The AGV is observed at the right side of the hospital station with the tote.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station tote delivery layout and AGV position relative to the operator.*


**Stop or Escalate If:**

* The AGV does not complete the documented right-side positioning sequence.

---

### Step 5 — Place an empty tote on the AGV after it moves to the left side

**Responsible role:** operator

**Instruction:**
After the AGV moves to the left side of the hospital station, place an empty tote on the AGV.

**Expected result:**
An empty tote is placed on the AGV at the left side of the hospital station.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station induct-side tote placement context.*

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*Add Tote screen used when sending a tote back into the system after proper positioning on the induct side.*


**Stop or Escalate If:**

* The AGV does not complete the documented move to the left side.
* The operator cannot place an empty tote on the AGV.

---

### Step 6 — Verify the AGV has a tote to return with

**Responsible role:** operator

**Instruction:**
Verify that the AGV has a tote to return with so it can re-enter the sorter area.

**Expected result:**
The AGV has a tote to return with and is ready to re-enter the sorter area.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station tote return context after tote placement.*

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*Add Tote workflow context for sending a tote back into the system.*


**Stop or Escalate If:**

* The AGV does not have a tote to return with.
* The AGV does not re-enter the sorter area after the tote exchange.

---

## Success Criteria

* The operator confirms tote presence at the hospital station.
* The operator determines why the tote was brought to the hospital station using the green scanner and available station status information.
* The tote is manually handled at the hospital station.
* The AGV follows the documented right-side then left-side positioning sequence.
* An empty tote is placed on the AGV.
* The AGV has a tote to return with so it can re-enter the sorter area.

## Failure Conditions

* The operator cannot confirm tote presence at the hospital station.
* The scanner does not provide the reason the tote was brought to the station.
* The required manual handling task is not sufficiently defined by the source for the identified condition.
* The AGV does not complete the documented right-side then left-side positioning sequence.
* The AGV does not have a tote to return with after the exchange.

## Escalation Guidance

* Escalate for SME review if the scanner or station status does not clearly identify the reason the tote was brought to the hospital station.
* Escalate if the required manual handling task for the identified tote condition is not described clearly enough in the source to execute.
* Escalate if the AGV does not complete the documented right-side then left-side positioning sequence.
* Escalate if the AGV does not have a tote to return with and cannot re-enter the sorter area.

## Missing Details / Known Gaps

* The source does not provide detailed manual handling steps for each tote issue type such as mis-sort, bad tip, or tote overload.
* The source packet does not provide a complete page text extract for section 3.3 Hospital Station.
* The source does not provide a supported time estimate for completing this procedure.
* The source does not explicitly state whether production stop or LOTO is required.
* The packet includes HMI artifacts that imply more detailed remove/add tote interactions, but the candidate and source packet do not provide enough direct procedural detail to fully specify those button-by-button actions for this runbook.

## Source Lineage

- Candidate IDs: candidate_operator_handle_tote_at_hospital_station
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
