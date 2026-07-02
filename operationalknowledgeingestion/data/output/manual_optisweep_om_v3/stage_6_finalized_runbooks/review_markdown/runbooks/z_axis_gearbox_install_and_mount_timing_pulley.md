# Install the Z-axis gearbox and mount the timing pulley

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_the_z_axis_gearbox_and_mount_the_timing_pulley_v1` |
| Title | Install the Z-axis gearbox and mount the timing pulley |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Install the Z-axis gearbox by inserting it into the actuator base pilot hole, then mount the timing pulley on the gearbox using the separately referenced installation procedure.

## When To Use

Use this procedure during the installation portion of Z-axis gearbox replacement when the gearbox must be inserted into the pilot hole and the timing pulley must be mounted on the gearbox.

## Do Not Use For

* Do not use this runbook as a complete Z-axis gearbox replacement procedure; the source subsection appears to provide only partial installation steps.
* Do not use this runbook for timing pulley installation details beyond the source reference to the separate Installation procedure on page 168.
* Do not use this runbook where acceptance checks, torque values, or alignment verification are required, because those details are not provided in this source subsection.

## Safety And Operational Notes

* This source subsection does not provide explicit LOTO, production stop, or additional safety control instructions for these installation steps.
* Do not assume torque values, alignment checks, or acceptance criteria that are not stated in this source subsection.

## Access Or Tools Needed

* Access to the Z-axis gearbox installation area
* Z-axis gearbox
* Timing pulley
* Referenced installation instructions on page 168

## Procedure Steps

### Step 1 — Insert the gearbox into the pilot hole

**Responsible role:** L2_support

**Instruction:**
Insert the gearbox into the pilot hole.

**Expected result:**
The gearbox is inserted into the pilot hole.

**Screens / Images:**

![artifact_fig_7_7_gearbox](assets/artifact_fig_7_7_gearbox.png)

*Use the gearbox figure to identify the gearbox component and installation context.*


**Stop or Escalate If:**

* Stop or escalate if the gearbox cannot be inserted into the pilot hole.
* Stop or escalate if seating or fit cannot be confirmed from the available source information.

---

### Step 2 — Mount the timing pulley on the gearbox

**Responsible role:** L2_support

**Instruction:**
Mount a timing pulley on the gearbox, using the referenced "Installation" procedure on page 168 for the pulley installation details.

**Expected result:**
A timing pulley is mounted on the gearbox.

**Screens / Images:**

![artifact_fig_7_20_timing_pulley](assets/artifact_fig_7_20_timing_pulley.png)

*Use the timing pulley figure to identify the timing pulley assembly and related installation features.*


**Stop or Escalate If:**

* Stop or escalate if the timing pulley cannot be mounted using the referenced installation procedure.
* Stop or escalate if additional installation details such as torque, alignment, or acceptance checks are needed but not available in this source subsection.

---

## Success Criteria

* The gearbox is seated in the pilot hole.
* A timing pulley is mounted on the gearbox.

## Failure Conditions

* The gearbox cannot be inserted into the pilot hole.
* The timing pulley cannot be mounted on the gearbox using the referenced installation procedure.
* Required acceptance checks, torque values, or alignment verification details are needed but are not provided in this source subsection.

## Escalation Guidance

* Escalate to L2 support if the gearbox cannot be inserted into the pilot hole.
* Escalate to L2 support if the timing pulley cannot be mounted using the referenced installation procedure.
* Escalate for SME review if torque values, alignment verification, or acceptance criteria are required for execution.

## Missing Details / Known Gaps

* The source subsection does not provide acceptance checks.
* The source subsection does not provide torque values.
* The source subsection does not provide alignment verification details.
* The source subsection does not provide explicit tools beyond the referenced installation instructions.
* The source subsection text content is not present in the packet beyond the candidate extraction and source references.

## Source Lineage

- Candidate IDs: z_axis_gearbox_install_and_mount_timing_pulley
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
