# Access Teknic SD motor software and prepare to save custom motor parameters

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_access_teknic_sd_motor_software_and_prepare_to_save_custom_motor_parameters_v1` |
| Title | Access Teknic SD motor software and prepare to save custom motor parameters |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Obtain the Teknic manufacturer application and connect to a Teknic SD motor so the motor's custom parameters can be accessed and saved before motor or gearbox replacement work. The source states this applies to Z-axis and A-axis motors mounted into gearboxes and identifies the required software selections as ClearPath, SD motor type, and NEMA 23/34 IP53 Motor Body.

## When To Use

Use this procedure before Teknic SD motor or related gearbox replacement work when custom motor parameters must be accessed and saved from a Z-axis or A-axis motor.

## Do Not Use For

* Do not use this runbook as a complete motor removal or replacement procedure.
* Do not use this runbook when detailed connection sequence, save dialog workflow, or recovery steps are required; the source does not provide those details.

## Safety And Operational Notes

* Use safety glasses and gloves as listed in the broader motor replacement context referenced by the candidate.
* This task is embedded in motor replacement work and involves powered connections and replacement-related work; use a higher safe role.
* The source packet does not provide a detailed electrical safety, power-up, or lockout sequence for this software access task.

## Access Or Tools Needed

* Replacement Part: Teknic SD Motor
* PPE: Safety glasses
* PPE: gloves
* Torque wrench
* 4-mm hex wrench
* 5-mm hex wrench
* 3/8-in. wrench/socket
* laptop
* USB-A to micro-USB cable
* 25-V power supply
* 75-V power supply
* 4-pin Molex power supply connector
* 8-pin Molex communication cable
* Access to https://teknic.com/downloads/

## Procedure Steps

### Step 1 — Gather required tools and connection hardware

**Responsible role:** L2_support

**Instruction:**
Gather the listed items needed for this task: laptop, USB-A to micro-USB cable, 25-V power supply, 75-V power supply, 4-pin Molex power supply connector, and 8-pin Molex communication cable.

**Expected result:**
All listed tools and connection hardware are available for the software access task.

**Stop or Escalate If:**

* Required connection hardware or power supplies are not available.
* The technician cannot confirm the correct equipment for connecting to the motor.

---

### Step 2 — Identify the Teknic SD motor to be serviced

**Responsible role:** L2_support

**Instruction:**
Identify the Teknic SD motor to be worked on. This section applies to Z-axis and A-axis motors and notes that these motors are mounted into gearboxes which may also be replaced.

**Expected result:**
The correct Teknic SD motor has been identified for the parameter backup task.

**Screens / Images:**

![artifact_fig_7_5_teknic_sd_motor](assets/artifact_fig_7_5_teknic_sd_motor.png)

*Use Figure 7-5 to identify the Teknic SD motor.*

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Use the gearbox figure as optional context to distinguish the motor from gearbox-related hardware.*

![artifact_fig_7_6_gearbox](assets/artifact_fig_7_6_gearbox.png)

*Use the gearbox figure as optional context to distinguish the motor from gearbox-related hardware.*


**Stop or Escalate If:**

* The correct Z-axis or A-axis Teknic SD motor cannot be identified.
* The technician cannot distinguish the motor from the gearbox assembly.

---

### Step 3 — Connect to the motor

**Responsible role:** L2_support

**Instruction:**
Connect a cable to the motor so the motor's custom parameters can be accessed.

**Expected result:**
A cable connection to the motor is established for software access.

**Screens / Images:**

![artifact_page_122_image_2](assets/artifact_page_122_image_2.jpeg)

*Use the page 122 image as recommended visual support for locating the motor USB access point or USB port cover.*


**Stop or Escalate If:**

* The motor cannot be connected.
* The connection point cannot be located.
* The custom parameters cannot be accessed after connection.

---

### Step 4 — Open the Teknic download site

**Responsible role:** L2_support

**Instruction:**
Open the manufacturer download site at https://teknic.com/downloads/ on the laptop.

**Expected result:**
The Teknic downloads page is open on the laptop.

**Stop or Escalate If:**

* The Teknic download site cannot be reached.
* The technician does not have access to the download site.

---

### Step 5 — Select the required software options

**Responsible role:** L2_support

**Instruction:**
In the download selections, choose "ClearPath," then "SD" for the motor type, and then "NEMA 23/34 IP53 Motor Body."

**Expected result:**
The correct software selection path has been chosen on the manufacturer site.

**Stop or Escalate If:**

* The required software options cannot be found on the manufacturer site.
* The available selections do not match ClearPath, SD, and NEMA 23/34 IP53 Motor Body.

---

### Step 6 — Run the manufacturer application and save parameters

**Responsible role:** L2_support

**Instruction:**
Run the manufacturer application to access and save the motor's custom parameters.

**Expected result:**
The manufacturer application is running and the motor's custom parameters are accessible for saving.

**Stop or Escalate If:**

* The manufacturer application cannot be run.
* The motor's custom parameters cannot be accessed.
* The motor's custom parameters cannot be saved.

---

## Success Criteria

* The Teknic manufacturer application is obtained from the specified download site.
* The correct software selections are used: ClearPath, SD motor type, and NEMA 23/34 IP53 Motor Body.
* The Teknic SD motor is connected so its custom parameters are accessible.
* The motor's custom parameters are saved before replacement work.

## Failure Conditions

* Required tools or connection hardware are missing.
* The correct motor cannot be identified.
* The motor cannot be connected.
* The manufacturer site or application cannot be accessed.
* The custom parameters cannot be accessed or saved.

## Escalation Guidance

* If the motor cannot be connected or the custom parameters cannot be accessed or saved, escalate for higher-level support.
* Escalate when the source's missing details prevent safe or successful completion, including missing connection sequence or save workflow details.

## Missing Details / Known Gaps

* The source packet does not provide the detailed cable connection sequence.
* The source packet does not provide the exact application installation workflow.
* The source packet does not provide the exact save dialog or file naming workflow for saving parameters in this section.
* The source packet does not provide explicit production stop or LOTO requirements for this specific software access subsection.
* The source_sections text for the cited section is empty in this packet, so final wording relies on the candidate and attached artifact summaries.

## Source Lineage

- Candidate IDs: backup_teknic_sd_motor_parameters_via_manufacturer_software
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
