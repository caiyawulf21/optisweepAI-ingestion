# Pause Both Tippers From The VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_pause_both_tippers_from_the_visu_data_screen_v1` |
| Title | Pause Both Tippers From The VISU_DATA Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the PAUSE TIPPER control on the Operator Station HMI VISU_DATA screen to pause both tippers.

## When To Use

Use when an operator needs to pause both tippers from the VISU_DATA screen on the operator station HMI.

## Do Not Use For

* Do not use this runbook to pause AGVs; the packet includes separate AGV API controls in another source section.
* Do not use this runbook for maintenance-only manual control, fault reset, or CellIO actions on the VISU_MANCONTROL screen.

## Safety And Operational Notes

* Use only the documented PAUSE TIPPER control on the VISU_DATA screen.
* The source does not describe a pause confirmation prompt or a detailed paused-state indicator in this section.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_DATA screen

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1

## Procedure Steps

### Step 1 — Open the VISU_DATA screen

**Responsible role:** operator

**Instruction:**
Open the VISU_DATA screen on the operator station HMI.

**Expected result:**
The VISU_DATA screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*VISU_DATA screen layout including login controls, message banner, and tipper statistics.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Screen-navigation controls and the mapping showing F5 to Visu_Data.*


**Stop or Escalate If:**

* Stop or escalate if the operator station HMI does not display the VISU_DATA screen.
* Stop or escalate if the screen navigation controls do not allow access to Visu_Data.

---

### Step 2 — Locate the PAUSE TIPPER button

**Responsible role:** operator

**Instruction:**
Locate the PAUSE TIPPER button on the VISU_DATA screen.

**Expected result:**
The PAUSE TIPPER button is identified on the VISU_DATA screen.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The VISU_DATA screen area containing the PAUSE TIPPER control.*


**Stop or Escalate If:**

* Stop or escalate if the PAUSE TIPPER button is not present on the VISU_DATA screen.

---

### Step 3 — Press the PAUSE TIPPER button

**Responsible role:** operator

**Instruction:**
Press the PAUSE TIPPER button on the VISU_DATA screen.

**Expected result:**
The pause command is issued for both tippers.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*The VISU_DATA screen where the PAUSE TIPPER button is located.*


**Stop or Escalate If:**

* Stop or escalate if pressing PAUSE TIPPER does not pause both tippers.

---

### Step 4 — Verify both tippers are paused

**Responsible role:** operator

**Instruction:**
Verify that both tippers are paused using available HMI status indications or system observation supported by the source.

**Expected result:**
Both tippers are paused.

**Screens / Images:**

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Available VISU_DATA screen status areas such as process/status regions and other visible indicators that may support confirmation.*


**Stop or Escalate If:**

* Stop or escalate if pressing PAUSE TIPPER does not pause both tippers.
* Stop or escalate if the paused state cannot be confirmed because the source does not define a detailed paused-state indicator in this section.

---

## Success Criteria

* The VISU_DATA screen is opened on the operator station HMI.
* The PAUSE TIPPER button is located and pressed.
* Both tippers are paused.

## Failure Conditions

* The VISU_DATA screen cannot be accessed.
* The PAUSE TIPPER button cannot be located on the VISU_DATA screen.
* Pressing PAUSE TIPPER does not pause both tippers.
* The source section does not define a detailed paused-state confirmation indicator.

## Escalation Guidance

* Escalate if pressing PAUSE TIPPER does not pause both tippers.
* Escalate if the paused state cannot be confirmed from the available source-supported HMI indications or system observation.

## Missing Details / Known Gaps

* The source does not describe a confirmation prompt for PAUSE TIPPER.
* The source does not define the exact paused-state indicator or message used to confirm both tippers are paused.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required for this action.

## Source Lineage

- Candidate IDs: candidate_operator_pause_both_tippers_from_visu_data
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
