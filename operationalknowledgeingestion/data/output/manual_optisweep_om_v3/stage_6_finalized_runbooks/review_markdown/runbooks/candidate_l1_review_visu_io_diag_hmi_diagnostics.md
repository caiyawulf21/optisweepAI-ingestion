# Review VISU_IO_DIAG Screen Readings For Operator Station Troubleshooting

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_review_visu_io_diag_screen_readings_for_operator_station_troubleshooting_v1` |
| Title | Review VISU_IO_DIAG Screen Readings For Operator Station Troubleshooting |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the read-only VISU_IO_DIAG screen on the Operator Station HMI to inspect alarms or informational messages, HMI temperatures, voltage levels, and displayed input states during troubleshooting.

## When To Use

Use this procedure when troubleshooting at the Operator Station and read-only diagnostic information is needed from the VISU_IO_DIAG screen, including banner messages, control temperatures, voltage levels, and station input states.

## Do Not Use For

* Do not use this procedure to make control changes from the VISU_IO_DIAG screen because the source states the screen is read-only.

## Safety And Operational Notes

* The VISU_IO_DIAG screen is read-only and can be used for troubleshooting.
* Do not attempt control changes from this screen.

## Access Or Tools Needed

* Access to the Operator Station HMI
* VISU_IO_DIAG screen
* Screen selection drop-down menu

## Related Operational Context

* ctx_manual_visu_io_diag_screen_overview_v1
* ctx_manual_visu_io_diag_banner_messages_v1
* ctx_manual_visu_io_diag_voltage_levels_v1
* ctx_manual_visu_io_diag_station_switch_inputs_v1
* ctx_manual_visu_io_diag_screen_selection_dropdown_v1

## Procedure Steps

### Step 1 — Open the VISU_IO_DIAG screen

**Responsible role:** L1_support

**Instruction:**
Open or navigate to the VISU_IO_DIAG screen using the HMI screen selection drop-down menu.

**Expected result:**
The VISU_IO_DIAG screen is displayed on the Operator Station HMI.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*VISU_IO_DIAG layout and the screen selection drop-down.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Operator station display controls and navigation reference for accessing Visu_IO_Diag.*


**Stop or Escalate If:**

* The VISU_IO_DIAG screen cannot be accessed.
* The expected diagnostic sections are not available.

---

### Step 2 — Check the informational banner

**Responsible role:** L1_support

**Instruction:**
Check the informational banner for any displayed alarms or informational messages.

**Expected result:**
Any current banner message is visible for review.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Informational banner area on the VISU_IO_DIAG screen.*


---

### Step 3 — Navigate through banner messages

**Responsible role:** L1_support

**Instruction:**
Use the arrows on the right side of the banner to navigate through available banner messages and note the displayed messages.

**Expected result:**
Available banner messages are reviewed and noted.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Banner area and the message navigation arrows on the right side.*


---

### Step 4 — Review control temperatures

**Responsible role:** L1_support

**Instruction:**
Review the "Control Temps" section and observe the CPU and motherboard (MB) temperature readings.

**Expected result:**
CPU and motherboard temperature readings are visible and noted.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*"Control Temps" section showing CPU and MB temperature readings.*


---

### Step 5 — Verify voltage levels

**Responsible role:** L1_support

**Instruction:**
Review the "Voltage Levels" section and verify the internal controller voltage reading is 24 V.

**Expected result:**
The internal controller voltage reading is visible and compared to the expected 24 V value.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*"Voltage Levels" section showing the internal controller voltage reading.*


**Stop or Escalate If:**

* The internal controller voltage is not 24 V.

---

### Step 6 — Inspect station switch input states

**Responsible role:** L1_support

**Instruction:**
Inspect the section corresponding to the switch mounted on the station and observe which inputs are shown as on and off.

**Expected result:**
The displayed on/off states for the station switch inputs are visible and noted.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Section corresponding to the switch mounted on the station and its displayed on/off input states.*


---

### Step 7 — Open detailed input information

**Responsible role:** L1_support

**Instruction:**
Select one of the input sections to open the window with more information about what the inputs are.

**Expected result:**
A window opens with more information about the selected inputs.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Input sections on the VISU_IO_DIAG screen and the selectable area used to open more input information.*


---

### Step 8 — Record observed diagnostic information

**Responsible role:** L1_support

**Instruction:**
Record the observed messages, temperatures, voltage reading, and input states for troubleshooting.

**Expected result:**
Observed VISU_IO_DIAG information is documented for use in troubleshooting.

**Stop or Escalate If:**

* Key diagnostic sections could not be reviewed.
* The internal controller voltage is not 24 V.

---

## Success Criteria

* The VISU_IO_DIAG screen is accessed successfully.
* Banner messages, CPU temperature, motherboard temperature, internal controller voltage, and displayed input states are reviewed.
* Any additional input detail window needed for troubleshooting is opened successfully.
* Observed diagnostic information is recorded for troubleshooting.

## Failure Conditions

* The VISU_IO_DIAG screen cannot be accessed.
* Expected diagnostic sections are not available.
* The internal controller voltage is not 24 V.
* Banner messages or input detail windows cannot be reviewed as described.

## Escalation Guidance

* Escalate if the screen cannot be accessed or the expected diagnostic sections are not available.
* Escalate if the internal controller voltage is not 24 V.
* Escalate if troubleshooting requires control changes, because the source states this screen is read-only.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not specify whether production must be stopped before using this screen.
* The source does not specify whether lockout/tagout is required.
* The source does not define acceptable CPU or motherboard temperature thresholds.
* The source does not specify a required recording format for captured observations.

## Source Lineage

- Candidate IDs: candidate_l1_review_visu_io_diag_hmi_diagnostics
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
