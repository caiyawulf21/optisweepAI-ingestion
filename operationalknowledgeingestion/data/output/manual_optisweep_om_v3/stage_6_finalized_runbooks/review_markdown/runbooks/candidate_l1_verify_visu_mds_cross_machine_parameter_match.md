# Verify VISU_MDS Machine Data Values Match Across Machines

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_visu_mds_machine_data_values_match_across_machines_v1` |
| Title | Verify VISU_MDS Machine Data Values Match Across Machines |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the VISU_MDS Machine Data screen to review axis machine data values and compare them across machines. The source states that most listed values should match from machine to machine, with documented exceptions for MD5 Tote Pickup Position and MD21 Home Offset, which are unique for every machine and every axis.

## When To Use

Use this procedure when reviewing VISU_MDS Machine Data parameter consistency between machines for the same axis set, based on the manual's documented list of values that should match from machine to machine.

## Do Not Use For

* Do not use this procedure to change VISU_MDS parameters; the source states these values generally do not require changing unless a motor is replaced.
* Do not treat MD5 Tote Pickup Position as a mismatch solely because it differs between machines.
* Do not treat MD21 Home Offset as a mismatch solely because it differs between machines.
* Do not use this procedure as a corrective action procedure for mismatched values; the source does not provide corrective actions.

## Safety And Operational Notes

* This runbook is diagnostic only and does not instruct parameter changes.
* The source states VISU_MDS Machine Data parameters generally should not be changed unless a motor is replaced.

## Access Or Tools Needed

* Access to the operator station HMI
* VISU_MDS Machine Data screen on the machines being compared
* Documented Table 4-10 machine data ID list

## Related Operational Context

* ctx_manual_visu_data_screen_overview_v1
* ctx_manual_visu_mds_parameter_change_guidance_v1
* ctx_manual_visu_mds_matching_values_exceptions_v1

## Procedure Steps

### Step 1 — Open the VISU_MDS Machine Data screen

**Responsible role:** L1_support

**Instruction:**
Open the VISU_MDS "Machine Data" screen for the machine being checked.

**Expected result:**
The Machine Data screen is displayed and the axis parameter fields are visible.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Machine Data screen showing axis parameter fields and IDs for Z1, A1, Z2, and A2.*

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*Operator station HMI reference associated with navigating to the Visu_MDs screen.*


**Stop or Escalate If:**

* Stop if the VISU_MDS Machine Data screen is not accessible for review.

---

### Step 2 — Identify the axis being reviewed

**Responsible role:** L1_support

**Instruction:**
Identify the axis being reviewed from Z1, A1, Z2, and A2.

**Expected result:**
A single axis is selected for comparison across machines.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Axis sections labeled Z1, A1, Z2, and A2 on the Machine Data screen.*


**Stop or Escalate If:**

* Stop if the axis cannot be confidently identified on the Machine Data screen.

---

### Step 3 — Review the documented machine data IDs

**Responsible role:** L1_support

**Instruction:**
Review the documented machine data IDs that should match from machine to machine: 0 Axis Name, 1 OT Minus, 5 Tote Pickup Position, 6 Plus Travel Opposite Axis Position, 7 Neg Travel Opposite Axis Position, 8 Tote Dump Position, 9 Soft Travel Lim Pos, 10 OT Pos, 11 Base Speed for AutoCycle, 12 Base Acc/Dec for AutoCycle, 13 Jog Speed, 14 Jog Acceleration, 16 Tote Prox Simulation, 20 Home Position, 21 Home Offset, 22 Homing Speed, 23 Homing CAM Speed, and 24 Homing Acceleration.

**Expected result:**
The reviewer has the full source-supported list of IDs to compare.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Machine Data parameter fields corresponding to the documented machine data IDs.*


**Stop or Escalate If:**

* Escalate if the source-supported ID list appears internally inconsistent and prevents confident comparison.

---

### Step 4 — Compare the values across machines

**Responsible role:** L1_support

**Instruction:**
Compare the displayed values for the reviewed machine against the corresponding machine data values on the other machine.

**Expected result:**
Matching-required values are identified as matching or not matching across the machines.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Displayed machine data values for the selected axis on the Machine Data screen.*


**Stop or Escalate If:**

* Escalate if a value expected to match from machine to machine does not match.

---

### Step 5 — Apply the documented exceptions

**Responsible role:** L1_support

**Instruction:**
Treat MD5 Tote Pickup Position and MD21 Home Offset as documented exceptions that are unique for every machine and every axis rather than expected matches.

**Expected result:**
MD5 and MD21 are excluded from mismatch findings based solely on cross-machine differences.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*The machine data entries for MD5 Tote Pickup Position and MD21 Home Offset while reviewing comparison results.*


**Stop or Escalate If:**

* Escalate if the source inconsistency around MD5 prevents confident interpretation.
* Do not treat MD5 Tote Pickup Position or MD21 Home Offset as mismatches solely because they differ.

---

### Step 6 — Record mismatches against the documented expectation

**Responsible role:** L1_support

**Instruction:**
Record any values that do not match the documented expectation.

**Expected result:**
Any nonmatching values that should match are documented for escalation or review.

**Stop or Escalate If:**

* Escalate if a value expected to match from machine to machine does not match.
* Do not record MD5 Tote Pickup Position or MD21 Home Offset as mismatches solely because they differ.

---

## Success Criteria

* The VISU_MDS Machine Data screen was reviewed for the selected axis.
* The documented machine data IDs were compared across machines.
* MD5 Tote Pickup Position and MD21 Home Offset were treated as documented exceptions.
* Any values expected to match but found not to match were recorded for escalation.

## Failure Conditions

* The VISU_MDS Machine Data screen cannot be accessed or reviewed.
* A value expected to match from machine to machine does not match.
* MD5 Tote Pickup Position or MD21 Home Offset is incorrectly treated as a mismatch solely because it differs.
* The source does not provide corrective actions for mismatched values.

## Escalation Guidance

* Escalate if a value expected to match from machine to machine does not match.
* Escalate for SME review if the source inconsistency around MD5 Tote Pickup Position creates uncertainty during interpretation.
* Use escalation rather than corrective action from this runbook because the source does not provide corrective actions for mismatched values.

## Missing Details / Known Gaps

* The source does not provide corrective actions for mismatched values.
* The source does not provide a required recording location or format for mismatch findings.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required for this review.
* The source text appears to include MD5 Tote Pickup Position in both the match list and the exception list; SME review is needed to resolve this inconsistency.

## Source Lineage

- Candidate IDs: candidate_l1_verify_visu_mds_cross_machine_parameter_match
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
