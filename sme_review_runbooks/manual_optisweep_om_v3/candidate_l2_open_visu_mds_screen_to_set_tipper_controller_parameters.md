# Open The Visu_MDs HMI Screen To Set Initial Tipper Controller Parameters

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_the_visu_mds_hmi_screen_to_set_initial_tipper_controller_parameters_v1` |
| Title | Open The Visu_MDs HMI Screen To Set Initial Tipper Controller Parameters |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Access the operator station HMI Machine Data screen (Visu_MDs) as the documented starting point for setting initial controller parameters for each tipper axis during tipper commissioning. The source supports the required login level and navigation to the screen, but does not provide the actual parameter entries or save/update actions for this specific step.

## When To Use

Use during tipper commissioning when initial controller parameters must be accessed for each tipper axis, particularly in the commissioning context described after tipper component replacement.

## Do Not Use For

* Do not use this runbook to enter or change specific parameter names or values, because they are not provided in the source excerpt.
* Do not use this runbook to perform save, update, or confirmation actions for controller parameters, because those actions are not provided in the source excerpt.
* Do not use this runbook as a complete tipper commissioning procedure; it only covers the source-backed access steps for reaching the Visu_MDs screen.

## Safety And Operational Notes

* This procedure is part of tipper commissioning activity associated with replaced tipper components and changing controller settings.
* You must be logged in as maintenance or admin to be able to change the settings.
* The source does not provide enough detail to safely perform actual parameter changes within this runbook.

## Access Or Tools Needed

* Operator station HMI
* Maintenance or admin login credentials

## Related Operational Context

* ctx_manual_visu_mds_screen_reference_v1
* ctx_manual_tipper_parameter_access_roles_v1
* ctx_manual_tipper_commissioning_overview_v1

## Procedure Steps

### Step 1 — Log in with maintenance or admin access

**Responsible role:** L2_support

**Instruction:**
Log in to the operator station HMI using a maintenance or admin account before attempting to change controller settings.

**Expected result:**
The user is logged in with sufficient privileges to change settings.

**Screens / Images:**

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*Operator station HMI screen referenced for controller parameter setup during tipper commissioning.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Login/logout controls and logged-in user ID area on the operator station HMI.*


**Stop or Escalate If:**

* Stop and escalate if maintenance or admin access is not available.
* Stop and escalate if you cannot confirm the HMI session has sufficient privileges to change settings.

---

### Step 2 — Navigate to the Visu_MDs screen

**Responsible role:** L2_support

**Instruction:**
On the operator station HMI, navigate to the "Visu_MDs" screen using F2.

**Expected result:**
The Visu_MDs screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*The operator station HMI screen referenced in the commissioning section for accessing Visu_MDs.*

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*The Machine Data screen layout for axes Z1, A1, Z2, and A2.*


**Stop or Escalate If:**

* Stop and escalate if F2 does not open the Visu_MDs screen.
* Stop and escalate if the displayed screen does not match the Machine Data screen used for axis parameters.

---

### Step 3 — Use Visu_MDs as the starting point for axis parameter setup

**Responsible role:** L2_support

**Instruction:**
Use the Visu_MDs screen as the documented starting point for setting the initial parameters for each axis of the tippers. Do not enter parameter names, values, or update actions from this runbook unless separately supported by source material.

**Expected result:**
The user is at the documented Machine Data screen used to access initial controller parameters for each tipper axis.

**Screens / Images:**

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*The commissioning-related operator station HMI screen used for controller parameter access.*

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Axis parameter sections for Z1, A1, Z2, and A2 on the Machine Data screen.*


**Stop or Escalate If:**

* Stop and escalate if the required parameter-setting details are needed but are not available in this source excerpt.
* Stop and escalate if specific parameter names, values, or save/update actions are required to continue.

---

## Success Criteria

* The user is logged in to the operator station HMI as maintenance or admin.
* The Visu_MDs screen is opened using F2.
* The Machine Data screen is available as the documented starting point for initial tipper axis controller parameter setup.

## Failure Conditions

* The user does not have maintenance or admin access.
* The Visu_MDs screen cannot be reached using F2.
* Specific parameter entry details are required but are not provided in this source excerpt.

## Escalation Guidance

* Escalate if maintenance or admin access is not available to change settings.
* Escalate if the HMI does not open the Visu_MDs screen as documented.
* Escalate to SME/manual follow-up if specific parameter names, values, or save/update actions are needed, because they are not provided in this source-backed procedure.

## Missing Details / Known Gaps

* The source excerpt does not provide the specific controller parameter names to set.
* The source excerpt does not provide parameter values or thresholds.
* The source excerpt does not provide save, update, or confirmation actions for this controller-parameter step.
* The source excerpt does not specify whether production must be stopped.
* The source excerpt does not specify lockout/tagout requirements.
* The source excerpt does not provide an estimated completion time.

## Source Lineage

- Candidate IDs: candidate_l2_open_visu_mds_screen_to_set_tipper_controller_parameters
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
