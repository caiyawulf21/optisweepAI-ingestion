# View Tipper Alarms And Timestamps On the Visu_Alarm Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_tipper_alarms_and_timestamps_on_the_visu_alarm_screen_v1` |
| Title | View Tipper Alarms And Timestamps On the Visu_Alarm Screen |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Operator Station HMI Visu_Alarm screen to view the list of tipper alarms and the timestamp shown with each alarm.

## When To Use

Use this procedure when an operator needs to inspect the Operator Station HMI Visu_Alarm screen to see the tipper alarms currently displayed and the timestamp associated with each listed alarm.

## Do Not Use For

* Do not use this procedure to infer alarm meanings from the displayed alarm list alone.
* Do not use this procedure to determine corrective actions from this source section alone.

## Safety And Operational Notes

* This source supports screen-based alarm viewing only.
* Do not infer alarm meanings or corrective actions from this source section alone.

## Access Or Tools Needed

* Access to the Operator Station HMI
* Visu_Alarm screen

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1
* ctx_manual_tipper_motion_axes_reference_v1

## Procedure Steps

### Step 1 — Access the Visu_Alarm screen

**Responsible role:** operator

**Instruction:**
Access the Operator Station HMI Visu_Alarm screen. If using the operator station display controls reference, use the screen navigation controls associated with Visu_Alarm.

**Expected result:**
The Visu_Alarm screen is displayed on the Operator Station HMI.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen-navigation controls and the mapping showing F6 to Visu_Alarm.*

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*The VISU_ALARM screen layout used for viewing tipper alarms.*


**Stop or Escalate If:**

* Stop and escalate if the Visu_Alarm screen cannot be accessed.
* Stop and escalate if the displayed screen does not match the documented alarm screen.

---

### Step 2 — Observe the displayed tipper alarm list

**Responsible role:** operator

**Instruction:**
Observe the list of tipper alarms displayed on the Visu_Alarm screen.

**Expected result:**
A list of tipper alarms is visible on the screen.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*The alarm list area showing the tipper alarms displayed on the VISU_ALARM screen.*


**Stop or Escalate If:**

* Stop and escalate if the Visu_Alarm screen does not display the documented alarm list.

---

### Step 3 — Check for timestamps on each listed alarm

**Responsible role:** operator

**Instruction:**
Check that each listed alarm includes a timestamp.

**Expected result:**
Each displayed alarm entry includes timestamp information.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*Alarm entries and the associated timestamp information shown with each alarm.*


**Stop or Escalate If:**

* Stop and escalate if the screen does not display timestamp information with the alarm list.

---

### Step 4 — Use the displayed list to identify shown alarms

**Responsible role:** operator

**Instruction:**
Use the displayed alarm list and timestamps to identify the alarms currently shown on the screen.

**Expected result:**
The operator can identify the alarms currently shown and see the timestamp associated with each listed alarm.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*The full VISU_ALARM screen showing the alarm list and timestamps used to identify the alarms currently displayed.*


**Stop or Escalate If:**

* Stop and escalate if the Visu_Alarm screen cannot be accessed or does not display the documented alarm list and timestamp information.

---

## Success Criteria

* The Operator Station HMI Visu_Alarm screen is accessible.
* The screen displays a list of tipper alarms.
* The displayed alarm entries include timestamps.
* The operator can identify the alarms currently shown on the screen using the displayed list and timestamps.

## Failure Conditions

* The Visu_Alarm screen cannot be accessed.
* The screen does not display the documented alarm list.
* Timestamp information is not shown with the displayed alarms.
* The source section does not provide alarm meanings or corrective actions.

## Escalation Guidance

* Escalate if the Visu_Alarm screen cannot be accessed.
* Escalate if the screen does not display the documented alarm list and timestamp information.
* Escalate to a higher support level or SME if alarm interpretation or corrective action is required, because this source section does not provide those details.

## Missing Details / Known Gaps

* The source does not provide detailed navigation steps to reach the Visu_Alarm screen beyond related display-control references.
* The source does not define alarm meanings.
* The source does not provide alarm acknowledgement steps.
* The source does not provide corrective actions for displayed alarms.
* The source section text in the packet is empty; the runbook relies on supplied source references and artifact retrieval text.

## Source Lineage

- Candidate IDs: candidate_operator_view_tipper_alarms_on_visu_alarm_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
