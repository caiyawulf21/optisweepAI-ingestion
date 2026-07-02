# Download motor configuration from a matching motor and upload it to the replacement motor

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_download_motor_configuration_from_a_matching_motor_and_upload_it_to_the_replacement_motor_v1` |
| Title | Download motor configuration from a matching motor and upload it to the replacement motor |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Teknic ClearPath application and a USB connection to save a motor configuration from the motor being replaced or, if that file is unavailable, from a working motor in the same position. Save the configuration as an .mtr file, disconnect from the source motor, and upload the saved configuration to the replacement motor. If the replacement motor will be tested, ensure it is clamped down before testing.

## When To Use

Use during motor replacement when the replacement motor needs the correct configuration parameters transferred from the motor being replaced or from a working motor in the same position. The source notes that motors in the same position, such as Z1 or Z2, share the same parameters.

## Do Not Use For

* Do not use as a complete motor replacement procedure; the source section only provides the configuration transfer portion.
* Do not use when detailed upload steps are required beyond the instruction to upload the saved configuration file; the source does not provide those detailed steps.

## Safety And Operational Notes

* If the new motor will be tested, make sure it is clamped down before testing.
* This procedure is associated with motor replacement activity; the source packet does not define full safety boundaries for replacement or testing.

## Access Or Tools Needed

* Laptop
* USB cable
* Access to the motor USB connection
* Teknic ClearPath application
* Configuration file saved as an .mtr file
* Replacement motor

## Procedure Steps

### Step 1 — Identify a matching source motor if the original configuration file is unavailable

**Responsible role:** L2_support

**Instruction:**
If the configuration file for the motor being replaced is not available, identify a working motor in the same position as the replacement target, such as another Z1 motor for a Z1 replacement or another Z2 motor for a Z2 replacement.

**Expected result:**
A valid source motor in the same position is identified for configuration download.

**Screens / Images:**

![artifact_fig_7_5_teknic_sd_motor](assets/artifact_fig_7_5_teknic_sd_motor.png)

*Use the Teknic SD Motor figure to confirm the motor type associated with this configuration transfer workflow.*


**Stop or Escalate If:**

* A matching-position motor cannot be identified.
* It is unclear whether the candidate source motor shares the same parameters as the replacement target.

---

### Step 2 — Connect the motor to the laptop by USB

**Responsible role:** L2_support

**Instruction:**
Connect the USB cable to the motor and the laptop.

**Expected result:**
The motor and laptop are physically connected by USB.

**Screens / Images:**

![artifact_page_122_image_2](assets/artifact_page_122_image_2.jpeg)

*Look for the motor USB connection point and any labeled USB port cover associated with the motor replacement workflow.*

![artifact_fig_7_5_teknic_sd_motor](assets/artifact_fig_7_5_teknic_sd_motor.png)

*Use the Teknic SD Motor figure to identify the motor referenced by the procedure.*


**Stop or Escalate If:**

* The USB connection point cannot be located.
* The USB cable cannot be connected to the motor and laptop.

---

### Step 3 — Launch the Teknic ClearPath application

**Responsible role:** L2_support

**Instruction:**
Run the Teknic ClearPath application on the laptop.

**Expected result:**
The Teknic ClearPath application is open and available for configuration operations.

**Stop or Escalate If:**

* The Teknic ClearPath application is not available on the laptop.
* The application does not start.

---

### Step 4 — Save the motor configuration as an .mtr file

**Responsible role:** L2_support

**Instruction:**
From the File menu, select Save Configuration and save the configuration as an .mtr file.

**Expected result:**
An .mtr configuration file is saved from the source motor.

**Stop or Escalate If:**

* The File > Save Configuration action is unavailable.
* The configuration cannot be saved as an .mtr file.

---

### Step 5 — Disconnect from the source motor

**Responsible role:** L2_support

**Instruction:**
Disconnect from the motor after saving the configuration file.

**Expected result:**
The source motor is disconnected after the configuration file is saved.

**Stop or Escalate If:**

* The configuration file was not successfully saved before disconnecting.
* The connection cannot be cleanly ended.

---

### Step 6 — Upload the saved configuration to the replacement motor

**Responsible role:** L2_support

**Instruction:**
Upload the saved configuration file to the new motor.

**Expected result:**
The replacement motor receives the saved configuration file.

**Stop or Escalate If:**

* Detailed upload steps are required and are not available in this source.
* The saved configuration file cannot be uploaded to the replacement motor.

---

### Step 7 — Clamp the replacement motor before any testing

**Responsible role:** L2_support

**Instruction:**
If the new motor will be tested, make sure it is clamped down before testing.

**Expected result:**
The replacement motor is secured before testing begins.

**Stop or Escalate If:**

* The motor cannot be clamped down before testing.
* Testing is requested without the motor being secured.

---

## Success Criteria

* A configuration file is saved as an .mtr file from the motor being replaced or from a working motor in the same position.
* The saved configuration file is available for upload to the replacement motor.
* The replacement motor receives the saved configuration.
* If testing is performed, the replacement motor is clamped down before testing.

## Failure Conditions

* No matching-position source motor can be identified.
* The USB connection to the motor cannot be established.
* Teknic ClearPath is unavailable or cannot be run.
* The configuration cannot be saved as an .mtr file.
* The source does not provide the detailed upload steps needed to complete the upload.
* The motor is not clamped down before testing.

## Escalation Guidance

* If detailed upload steps are needed, consult the ClearPath User Manual referenced by the source section.
* Escalate when a matching-position source motor cannot be identified.
* Escalate when the Teknic ClearPath application is unavailable or the configuration cannot be saved.
* Use a higher-support role if site safety or service controls require it for motor replacement or testing.

## Missing Details / Known Gaps

* The source does not provide detailed upload steps for transferring the saved configuration to the new motor.
* The source does not provide a time estimate for this configuration transfer procedure.
* The source does not define whether production stop or LOTO is required for this specific configuration transfer activity.
* The source does not define explicit role boundaries beyond the inferred support level.

## Source Lineage

- Candidate IDs: motor_configuration_download_and_upload_for_replacement
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
