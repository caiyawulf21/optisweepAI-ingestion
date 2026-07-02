# Show Alarm History From the Visu_Alarm Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_show_alarm_history_from_the_visu_alarm_screen_v1` |
| Title | Show Alarm History From the Visu_Alarm Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the SHOW HISTORY button on the Operator Station HMI Visu_Alarm screen to display historical alarm records. The source states that the SHOW HISTORY button shows the last 1500 records.

## When To Use

Use this procedure when an operator needs to view alarm history from the Operator Station HMI Visu_Alarm screen.

## Do Not Use For

* Do not use this procedure to perform alarm filtering.
* Do not use this procedure to export alarm history.
* Do not use this procedure to acknowledge alarms.
* Do not use this procedure to clear alarms.

## Safety And Operational Notes

* This source documents an HMI viewing action only.
* Do not assume any additional alarm-history handling functions beyond displaying the last 1500 records.

## Access Or Tools Needed

* Access to the Operator Station HMI
* Visu_Alarm screen
* SHOW HISTORY button

## Related Operational Context

* ctx_manual_visu_alarm_screen_reference_v1

## Procedure Steps

### Step 1 — Access the Visu_Alarm screen

**Responsible role:** operator

**Instruction:**
Access the Operator Station HMI Visu_Alarm screen.

**Expected result:**
The Visu_Alarm screen is displayed on the Operator Station HMI.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen-navigation controls showing access to Visu_Alarm, including F6 mapped to Visu_Alarm.*

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*The VISU_ALARM screen layout showing tipper alarms and timestamps.*


**Stop or Escalate If:**

* Stop or escalate if the Visu_Alarm screen cannot be accessed.

---

### Step 2 — Locate the SHOW HISTORY button

**Responsible role:** operator

**Instruction:**
Locate the SHOW HISTORY button on the Visu_Alarm screen.

**Expected result:**
The SHOW HISTORY button is visible and ready to be selected.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*The SHOW HISTORY button on the Visu_Alarm screen.*


**Stop or Escalate If:**

* Stop or escalate if the SHOW HISTORY button is not present on the Visu_Alarm screen.

---

### Step 3 — Press SHOW HISTORY

**Responsible role:** operator

**Instruction:**
Press the SHOW HISTORY button.

**Expected result:**
The HMI updates to show alarm history records.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*The SHOW HISTORY button on the VISU_ALARM screen before selection.*


**Stop or Escalate If:**

* Escalate if pressing SHOW HISTORY does not display alarm history records as documented.

---

### Step 4 — Verify alarm history is displayed

**Responsible role:** operator

**Instruction:**
Verify that the screen shows alarm history records, with the documented history limited to the last 1500 records.

**Expected result:**
The Visu_Alarm screen displays alarm history records representing the last 1500 records.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*Alarm entries and timestamps on the VISU_ALARM screen as the reference view for alarm display.*


**Stop or Escalate If:**

* Escalate if alarm history records are not displayed.
* Escalate if the displayed behavior does not align with the documented statement that SHOW HISTORY shows the last 1500 records.

---

## Success Criteria

* The operator reaches the Visu_Alarm screen.
* The SHOW HISTORY button is located and used.
* Alarm history records are displayed.
* The displayed history corresponds to the last 1500 records as documented.

## Failure Conditions

* The Visu_Alarm screen cannot be accessed.
* The SHOW HISTORY button cannot be found on the Visu_Alarm screen.
* Pressing SHOW HISTORY does not display alarm history records.
* The source does not support any additional alarm-history functions beyond displaying records.

## Escalation Guidance

* Escalate if pressing SHOW HISTORY does not display alarm history records as documented.
* Escalate if the Visu_Alarm screen or SHOW HISTORY button is unavailable.
* Do not assume filtering, export, acknowledgement, or clearing functions because they are not described in this source.

## Missing Details / Known Gaps

* The source does not provide a detailed navigation sequence beyond identifying the Visu_Alarm screen and related display controls.
* The source does not specify whether login is required to view alarm history.
* The source does not describe filtering, sorting, exporting, acknowledging, or clearing alarm history.
* The source does not provide a time estimate for this procedure.
* The source does not state whether production must be stopped or whether LOTO is required.

## Source Lineage

- Candidate IDs: candidate_operator_show_alarm_history_on_visu_alarm_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
