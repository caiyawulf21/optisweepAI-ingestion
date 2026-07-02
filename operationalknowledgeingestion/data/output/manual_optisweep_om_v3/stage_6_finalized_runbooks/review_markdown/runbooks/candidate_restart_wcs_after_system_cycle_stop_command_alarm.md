# Restart the WCS From a System Cycle Stop Command Alarm

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_restart_the_wcs_from_a_system_cycle_stop_command_alarm_v1` |
| Title | Restart the WCS From a System Cycle Stop Command Alarm |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented corrective action for the System Cycle Stop Command alarm to return from the Op Station Cycle Stop state. The source states that when WCS sends Cycle Stop to the Op Station, the corrective action is to press CYCLE START on the WCS HMI.

## When To Use

Use when the displayed alarm matches the documented System Cycle Stop Command alarm entry and the source-backed corrective action is needed to recover from the Op Station Cycle Stop state.

## Do Not Use For

* Do not use for alarms other than the documented System Cycle Stop Command entry.
* Do not use when WCS HMI access is not available.

## Safety And Operational Notes

* Use only the documented corrective action from the source.
* The source does not provide a WCS HMI navigation path; do not improvise unsupported navigation or controls.

## Access Or Tools Needed

* Access to the WCS HMI
* Alarm text confirmation from the HMI or alarm list
* Table 4-23 Alarms and Corrective Actions

## Related Operational Context

* ctx_manual_tipper_system_overview_v1

## Procedure Steps

### Step 1 — Confirm the System Cycle Stop Command alarm is displayed

**Responsible role:** L1_support

**Instruction:**
Review the alarm list and confirm the displayed alarm text matches "Left Tipper: System Cycle Stop Command" or the corresponding system cycle stop command entry.

**Expected result:**
The alarm text is confirmed as the documented System Cycle Stop Command entry.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*VISU_ALARM view showing tipper alarms and their timestamps; verify the alarm text matches the documented System Cycle Stop Command entry.*


**Stop or Escalate If:**

* The alarm text does not match the documented System Cycle Stop Command entry.
* The alarm list cannot be accessed or the alarm text cannot be verified.

---

### Step 2 — Verify the documented cause and controller response

**Responsible role:** L1_support

**Instruction:**
Verify from the alarm table that the cause is WCS sending Cycle Stop to the Op Station and that the controller response is Op Station Cycle Stop state.

**Expected result:**
The documented cause and controller response match the observed condition.

**Stop or Escalate If:**

* The observed condition does not match the documented cause or controller response.
* The source table entry cannot be verified.

---

### Step 3 — Press CYCLE START on the WCS HMI

**Responsible role:** L1_support

**Instruction:**
Press CYCLE START on the WCS HMI as listed in the corrective action.

**Expected result:**
The corrective action is issued from the WCS HMI.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Cycle control area showing CYCLE START/CYCLE STOP controls for visual context of cycle control terminology.*


**Stop or Escalate If:**

* WCS HMI access is not available.
* CYCLE START cannot be pressed or is not available on the WCS HMI.

---

### Step 4 — Observe whether the system leaves Cycle Stop state

**Responsible role:** L1_support

**Instruction:**
Observe whether the system leaves the Cycle Stop state after the command is issued.

**Expected result:**
The system returns from the documented Cycle Stop condition after CYCLE START is pressed on the WCS HMI.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*Alarm list and timestamps for continued indication of the alarm condition or recovery observation context.*

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Operator station status/troubleshooting context if additional read-only observation is needed.*


**Stop or Escalate If:**

* The system remains in Cycle Stop after CYCLE START is pressed on the WCS HMI.

---

## Success Criteria

* The documented System Cycle Stop Command alarm condition is confirmed.
* CYCLE START is pressed on the WCS HMI.
* The system leaves the Op Station Cycle Stop state.

## Failure Conditions

* The displayed alarm does not match the documented System Cycle Stop Command entry.
* The documented cause/controller response does not match the observed condition.
* WCS HMI access is unavailable or CYCLE START cannot be issued.
* The system remains in Cycle Stop after the documented action is performed.

## Escalation Guidance

* Escalate if the system remains in Cycle Stop after the documented action is performed.
* Escalate if the alarm cannot be matched to the documented System Cycle Stop Command entry.
* Escalate if WCS HMI access is required but not available.

## Missing Details / Known Gaps

* The source does not provide the exact WCS HMI navigation path to reach CYCLE START.
* The source does not state whether normal operators have WCS HMI access.
* The source does not provide a time estimate for completing this recovery.
* The packet source section text is empty; evidence is grounded from candidate and artifact source references only.

## Source Lineage

- Candidate IDs: candidate_restart_wcs_after_system_cycle_stop_command_alarm
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
