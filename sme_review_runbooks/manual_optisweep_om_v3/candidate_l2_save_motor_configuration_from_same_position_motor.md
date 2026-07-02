# Save Motor Configuration From a Working Motor in the Same Position

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_save_motor_configuration_from_a_working_motor_in_the_same_position_v1` |
| Title | Save Motor Configuration From a Working Motor in the Same Position |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use Teknic ClearPath software to connect to a working motor in the same position as the replacement motor, save that motor configuration as an .mtr file, and retain the file for later upload to the replacement motor. The source states that motors used in the same position, such as Z1 or Z2, have the same parameters.

## When To Use

Use this procedure during motor replacement work when the configuration file for the motor being replaced is not already available and a working motor in the same position is available to copy from.

## Do Not Use For

* Do not use when a same-position working motor is not available.
* Do not use to copy parameters from a motor in a different position when same-position equivalence is not supported by the source.

## Safety And Operational Notes

* This procedure is associated with motor replacement activity and is not framed by the source as a normal operator task.
* Use only a working motor in the same position because the source states motors in the same position have the same parameters.

## Access Or Tools Needed

* Laptop with Teknic ClearPath application
* USB cable
* Access to the motor USB connection
* A working motor in the same position or the motor being replaced

## Procedure Steps

### Step 1 — Confirm a working same-position motor is available

**Responsible role:** L2_support

**Instruction:**
Identify whether the replacement motor position is the same as another working motor position, such as Z1 or Z2. Use a working motor in the same position because the source states motors used in the same position have the same parameters.

**Expected result:**
A suitable working motor in the same position is identified as the source for the configuration file.

**Screens / Images:**

![artifact_fig_7_5_teknic_sd_motor](assets/artifact_fig_7_5_teknic_sd_motor.png)

*Identify the Teknic SD motor referenced by the motor replacement and parameter save procedure.*


**Stop or Escalate If:**

* A same-position working motor is not available.
* It is not possible to determine that the available motor is in the same position as the replacement motor.

---

### Step 2 — Connect the USB cable between the motor and laptop

**Responsible role:** L2_support

**Instruction:**
If the configuration file for the motor being replaced is not already available, connect a USB cable to the motor and the laptop.

**Expected result:**
The motor and laptop are connected by USB and ready for software access.

**Screens / Images:**

![artifact_page_122_image_2](assets/artifact_page_122_image_2.jpeg)

*Locate the motor USB port cover and the motor connection point for the USB cable.*


**Stop or Escalate If:**

* The configuration file is not already available and the USB connection cannot be established.
* The motor USB port cover or connection point cannot be located from the available source-supported visual reference.

---

### Step 3 — Run Teknic ClearPath

**Responsible role:** L2_support

**Instruction:**
Run the Teknic ClearPath application.

**Expected result:**
Teknic ClearPath is open and available for saving the motor configuration.

**Stop or Escalate If:**

* The Teknic ClearPath application is not available or cannot be launched.

---

### Step 4 — Save the motor configuration as an .mtr file

**Responsible role:** L2_support

**Instruction:**
From the File menu, select Save Configuration to save the configuration as an .mtr file.

**Expected result:**
The motor configuration is saved as an .mtr file.

**Stop or Escalate If:**

* The configuration cannot be obtained from the existing motor.
* The .mtr file cannot be saved.

---

### Step 5 — Disconnect from the motor

**Responsible role:** L2_support

**Instruction:**
Disconnect from the motor after the configuration file is saved.

**Expected result:**
The motor is disconnected and the saved .mtr file is retained for reuse.

**Stop or Escalate If:**

* The configuration file was not successfully saved before disconnecting.

---

## Success Criteria

* A motor configuration file is saved as an .mtr file.
* The saved .mtr file is available for upload to a replacement motor in the same position.

## Failure Conditions

* A same-position working motor is not available.
* The configuration cannot be obtained from the existing motor.
* The USB connection cannot be established.
* The Teknic ClearPath application cannot be run.
* The configuration cannot be saved as an .mtr file.

## Escalation Guidance

* Escalate if a same-position working motor is not available.
* Escalate if the configuration cannot be obtained from the existing motor.

## Missing Details / Known Gaps

* The source packet does not provide a time estimate for this specific procedure.
* The source packet does not explicitly state whether production stop is required.
* The source packet does not explicitly state whether LOTO is required for this specific configuration save sequence.
* The source packet does not provide exact file naming or storage location guidance for the .mtr file.
* The source packet does not provide detailed software screen captures for the Teknic ClearPath File menu.

## Source Lineage

- Candidate IDs: candidate_l2_save_motor_configuration_from_same_position_motor
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
