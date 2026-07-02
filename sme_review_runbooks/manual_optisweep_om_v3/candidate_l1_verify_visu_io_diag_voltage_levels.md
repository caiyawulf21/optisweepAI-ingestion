# Verify Internal Controller Voltage On VISU_IO_DIAG Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_internal_controller_voltage_on_visu_io_diag_screen_v1` |
| Title | Verify Internal Controller Voltage On VISU_IO_DIAG Screen |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Check the Operator Station HMI VISU_IO_DIAG screen and verify whether the internal controller voltage shown in the "Voltage Levels" section matches the documented expected value of 24 V.

## When To Use

Use this procedure when troubleshooting from the Operator Station HMI and you need to verify the internal controller voltage shown on the read-only VISU_IO_DIAG screen.

## Do Not Use For

* Do not use this procedure to change settings or adjust voltage values; the VISU_IO_DIAG screen is described as read-only.
* Do not use this procedure as a corrective action procedure for voltage faults; the source only supports verification of the displayed value.

## Safety And Operational Notes

* The VISU_IO_DIAG screen is read-only and can be used for troubleshooting.

## Access Or Tools Needed

* Access to the Operator Station HMI
* VISU_IO_DIAG screen

## Related Operational Context

* ctx_manual_visu_io_diag_screen_overview_v1
* ctx_manual_visu_io_diag_voltage_levels_v1

## Procedure Steps

### Step 1 — Open the VISU_IO_DIAG screen

**Responsible role:** L1_support

**Instruction:**
Open the VISU_IO_DIAG screen on the Operator Station HMI.

**Expected result:**
The VISU_IO_DIAG screen is displayed on the Operator Station HMI.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Read-only Operator Station IO Diagnostics screen used for troubleshooting.*


**Stop or Escalate If:**

* The VISU_IO_DIAG screen is not accessible on the Operator Station HMI.

---

### Step 2 — Locate the Voltage Levels section

**Responsible role:** L1_support

**Instruction:**
Locate the "Voltage Levels" section on the VISU_IO_DIAG screen.

**Expected result:**
The "Voltage Levels" section is identified on the screen.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*The area of the VISU_IO_DIAG screen labeled "Voltage Levels".*


**Stop or Escalate If:**

* The "Voltage Levels" section is not visible on the VISU_IO_DIAG screen.

---

### Step 3 — Observe the internal controller voltage reading

**Responsible role:** L1_support

**Instruction:**
Observe the voltage reading for the internal controller of the HMI in the "Voltage Levels" section.

**Expected result:**
A displayed voltage value for the HMI internal controller is visible.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*The displayed internal controller voltage reading within the "Voltage Levels" section.*


**Stop or Escalate If:**

* The voltage value is not visible on the screen.

---

### Step 4 — Compare the displayed reading to 24 V

**Responsible role:** L1_support

**Instruction:**
Compare the displayed internal controller voltage reading to the documented expected value of 24 V.

**Expected result:**
You determine whether the displayed voltage matches 24 V.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*The internal controller voltage reading in the "Voltage Levels" section and whether it matches 24 V.*


**Stop or Escalate If:**

* The displayed internal controller voltage does not match 24 V.

---

### Step 5 — Record the verification result

**Responsible role:** L1_support

**Instruction:**
Record whether the displayed voltage matches 24 V.

**Expected result:**
The verification result is documented as either matching or not matching 24 V.

**Stop or Escalate If:**

* The voltage value could not be determined from the screen.
* The displayed internal controller voltage does not match 24 V.

---

## Success Criteria

* The VISU_IO_DIAG screen is opened successfully.
* The "Voltage Levels" section is located.
* The internal controller voltage reading is visible.
* The displayed reading is compared against the documented expected value of 24 V.
* The result is recorded.

## Failure Conditions

* The VISU_IO_DIAG screen cannot be accessed.
* The "Voltage Levels" section is not visible.
* The internal controller voltage value is not visible.
* The displayed internal controller voltage does not match 24 V.

## Escalation Guidance

* Escalate if the displayed internal controller voltage does not match 24 V.
* Escalate if the voltage value is not visible on the screen.

## Missing Details / Known Gaps

* The source does not provide navigation steps for reaching the VISU_IO_DIAG screen.
* The source does not provide a required recording location or format for documenting the result.
* The source does not provide corrective actions beyond escalation when the displayed value does not match 24 V.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_l1_verify_visu_io_diag_voltage_levels
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
