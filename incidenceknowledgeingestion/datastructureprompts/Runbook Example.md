# Canonical Runbook Example — Start Operator Station

<!--
Stage 6 / Shared canonical runbook reference.
Example prompt/schema for reviewable runbook structure; incident Stage 6 should
produce candidates, while shared finalization later decides canonical runbooks.
-->

File path:

`backend/app/prompts/manual_ingestion/examples/canonical_runbook_example_start_operator_station.md`

---

# Start Operator Station

## Runbook Header

| Field                    | Value                            |
| ------------------------ | -------------------------------- |
| Procedure ID             | `proc_start_operator_station_v1` |
| Title                    | Start Operator Station           |
| Procedure Type           | `operation`                      |
| Product                  | OptiSweep                        |
| Primary Role             | `operator`                       |
| Supporting Roles         | `L1_support`, `L2_support`       |
| Support Safe             | Yes                              |
| Requires Production Stop | No                               |
| Requires LOTO            | No                               |
| Estimated Time           | 5-10 minutes                     |
| Validation Status        | `needs_sme_review`               |
| Canonical Source Quality | Official manual                  |
| Merge Status             | New canonical runbook            |

---

## Summary

Start the Operator Station after the system has been turned off by verifying prerequisites, clearing a flashing ESTOP condition if present, homing the documented tipper axes, starting the tipper cycle, and placing the tipper in AUTO mode.

This runbook is intended for operators or support personnel guiding an operator through the documented startup sequence.

---

## When To Use

Use this runbook when:

* The Operator Station needs to be started after the system has been turned off.
* The tipper axes need to be homed as part of startup.
* The Operator Station needs to be placed into AUTO mode.
* Another approved recovery or startup procedure directs the user to start the Operator Station.

Do not use this runbook to:

* Start AGVs from the Geek+ system.
* Perform maintenance work inside guarded or locked-out equipment.
* Troubleshoot unresolved startup faults beyond the documented startup checks.
* Replace the referenced AGV startup manual.

---

## Roles And Responsibilities

| Role       | Responsibility                                                                                                       |
| ---------- | -------------------------------------------------------------------------------------------------------------------- |
| Operator   | Performs the HMI and control panel actions. Verifies visible indicators.                                             |
| L1 Support | Guides the operator, confirms steps were completed, and records observed failures.                                   |
| L2 Support | Assists if faults do not clear, axes do not home, AUTO mode cannot be enabled, or expected indicators do not appear. |
| L3 Support | Reviews unresolved technical failures or suspected software/control issues.                                          |

---

## Safety And Operational Notes

* Do not touch the tippers while the system is powered on.
* Only perform the steps documented in this runbook.
* Do not invent or perform undocumented AGV startup steps.
* If an ESTOP condition does not clear after the documented reset action, stop and escalate.
* If any axis fails to home or unexpected motion occurs, stop and escalate.
* AGV startup is referenced by the manual but is not described in this runbook.

---

## Prerequisites

### Access Required

* Physical access to the Operator Station.
* Access to the Operator Station control panel.
* Access to the Operator Station HMI.

### System Preconditions

* AGVs are powered on.
* Main disconnect is ON.
* Operator Station HMI is available.
* The user can observe the tipper axes and HMI indicators.

### External References

* Geek+ P40A V2.0 user manual for AGV startup instructions.
* OptiSweep Operation and Maintenance Manual, section 5.3: Starting the Operator Station.

---

## Related Operational Context

Attach these context records when available:

* `ctx_operator_station_overview_v1`
* `ctx_operator_station_hmi_navigation_v1`
* `ctx_operator_station_control_panel_v1`
* `ctx_operator_station_startup_prereqs_v1`
* `ctx_estop_reset_reference_v1`
* `ctx_tipper_axis_reference_status_v1`
* `ctx_tipper_auto_mode_reference_v1`
* `ctx_wcs_tipper_instruction_wait_state_v1`

---

## Visual References

Attach these artifacts when available:

| Artifact ID                                                  | Description                                                                                                  | Required                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------ |
| `artifact_manual_fig_4_18_operator_station_display_controls` | Operator Station display controls showing F3, F5, F6, navigation buttons, and screen selection.              | Recommended                                |
| `artifact_manual_fig_4_19_operator_station_control_panel`    | Visu_MCP_Dual screen showing AUTO, REF, RESET, AUTO REF, CYCLE START, axis indicators, and related controls. | Required                                   |
| `artifact_manual_fig_3_3_operator_station_push_buttons`      | Physical Operator Station push-buttons and ESTOP button.                                                     | Recommended                                |
| `artifact_page_82_image_2`                                   | Startup-related page image extracted from the manual, if mapped to section 5.3.                              | Optional until figure mapping is validated |

---

## Procedure Steps

### Step 1 — Verify AGVs are powered on

**Responsible role:** Operator
**Supporting role:** L1 Support

**Purpose:**
Confirm the AGVs are available before starting the Operator Station.

**Instruction:**
Verify that the AGVs are powered on.

**Expected result:**
AGVs are powered on.

**Healthy condition:**
AGVs are powered on and available for OptiSweep operation.

**Failure condition:**
AGVs are not powered on, unavailable, or their state cannot be confirmed.

**Actions:**

| Field         | Value                            |
| ------------- | -------------------------------- |
| Action Type   | `inspection_action`              |
| Label         | Verify AGV power state           |
| Exact Action  | Confirm the AGVs are powered on. |
| Role Required | `operator`                       |

**Commands:**
None.

**Screens or Images:**
None required unless a validated AGV status artifact is available.

**Stop or Escalate If:**

* AGVs are not powered on.
* AGV power state cannot be confirmed.
* The user needs AGV startup steps not included in the OptiSweep manual.

**Source Evidence:**
Official manual, section 5.3: Starting the Operator Station.

---

### Step 2 — Verify the main disconnect is ON

**Responsible role:** Operator
**Supporting role:** L1 Support

**Purpose:**
Confirm the Operator Station has power before continuing startup.

**Instruction:**
Verify that the main disconnect is ON.

**Expected result:**
The main disconnect is ON.

**Healthy condition:**
The Operator Station is powered and the HMI/control panel can be used.

**Failure condition:**
The main disconnect is OFF, unavailable, or cannot be verified.

**Actions:**

| Field         | Value                                 |
| ------------- | ------------------------------------- |
| Action Type   | `physical_inspection`                 |
| Label         | Verify main disconnect                |
| Exact Action  | Check that the main disconnect is ON. |
| Role Required | `operator`                            |

**Commands:**
None.

**Screens or Images:**
None.

**Stop or Escalate If:**

* Main disconnect is OFF and the operator is not authorized to turn it on.
* The HMI does not become available after power is confirmed.

**Source Evidence:**
Official manual, section 5.3: Starting the Operator Station.

---

### Step 3 — Clear flashing ESTOP if present

**Responsible role:** Operator
**Supporting role:** L1 Support

**Purpose:**
Clear the documented startup ESTOP condition before homing axes.

**Instruction:**
At the Operator Station control panel, check whether the ESTOP is flashing. If the ESTOP is flashing, pull out the ESTOP and press RESET on the HMI screen to clear any faults.

**Expected result:**
The flashing ESTOP condition clears and startup can continue.

**Healthy condition:**
ESTOP is not flashing, or it clears after pulling out the ESTOP and pressing RESET.

**Failure condition:**
ESTOP remains flashing, faults do not clear, or the RESET control does not restore the station to a startup-ready state.

**Actions:**

| Field         | Value                                         |
| ------------- | --------------------------------------------- |
| Action Type   | `physical_action`                             |
| Label         | Pull out ESTOP if flashing                    |
| Exact Action  | If the ESTOP is flashing, pull out the ESTOP. |
| Role Required | `operator`                                    |

| Field         | Value                                              |
| ------------- | -------------------------------------------------- |
| Action Type   | `hmi_action`                                       |
| Label         | Press RESET                                        |
| Exact Action  | Press RESET on the HMI screen to clear any faults. |
| Role Required | `operator`                                         |

**Commands:**
None.

**Screens or Images:**

| Artifact ID                                               | What To Look At                                       |
| --------------------------------------------------------- | ----------------------------------------------------- |
| `artifact_manual_fig_4_19_operator_station_control_panel` | RESET control and Operator Station HMI controls.      |
| `artifact_manual_fig_3_3_operator_station_push_buttons`   | Emergency stop push-button, if artifact is available. |

**Stop or Escalate If:**

* ESTOP condition does not clear.
* Faults do not clear after RESET.
* User sees alarms not covered by this runbook.
* The source does not provide additional recovery steps.

**Source Evidence:**
Official manual, section 5.3: Starting the Operator Station.

---

### Step 4 — Home every documented tipper axis

**Responsible role:** Operator
**Supporting role:** L1 Support

**Purpose:**
Reference the documented axes before placing the tipper into AUTO mode.

**Instruction:**
Home every documented axis: Z1 and A1 for the left tipper, and Z2 and A2 for the right tipper.

**Expected result:**
All documented axes are ready to be referenced/homed.

**Healthy condition:**
Z1, A1, Z2, and A2 are available for homing.

**Failure condition:**
One or more axes are unavailable, faulted, or cannot be selected/observed.

**Actions:**

| Field         | Value                                                                                 |
| ------------- | ------------------------------------------------------------------------------------- |
| Action Type   | `hmi_inspection`                                                                      |
| Label         | Confirm documented axes                                                               |
| Exact Action  | Confirm Z1, A1, Z2, and A2 are present on the Operator Station HMI/control interface. |
| Role Required | `operator`                                                                            |

**Commands:**
None.

**Screens or Images:**

| Artifact ID                                               | What To Look At                     |
| --------------------------------------------------------- | ----------------------------------- |
| `artifact_manual_fig_4_19_operator_station_control_panel` | A1, Z1, A2, and Z2 axis indicators. |

**Stop or Escalate If:**

* Axis indicators are missing.
* Axis indicators show an unresolved fault.
* Operator cannot identify the left/right tipper axes.

**Source Evidence:**
Official manual, section 5.3: Starting the Operator Station.
Official manual, Operator Station HMI control panel reference.

---

### Step 5 — Press AUTO REF

**Responsible role:** Operator
**Supporting role:** L1 Support

**Purpose:**
Automatically reference the axes of both tippers.

**Instruction:**
Press AUTO REF.

**Expected result:**
Axis homing/reference begins.

**Healthy condition:**
The axis button changes from green to yellow to indicate it is moving.

**Failure condition:**
AUTO REF is unavailable, nothing moves, or the expected color change does not occur.

**Actions:**

| Field         | Value                                                     |
| ------------- | --------------------------------------------------------- |
| Action Type   | `hmi_action`                                              |
| Label         | Press AUTO REF                                            |
| Exact Action  | Press AUTO REF on the Operator Station HMI/control panel. |
| Role Required | `operator`                                                |

**Commands:**
None.

**Screens or Images:**

| Artifact ID                                               | What To Look At                      |
| --------------------------------------------------------- | ------------------------------------ |
| `artifact_manual_fig_4_19_operator_station_control_panel` | AUTO REF button and axis indicators. |

**Stop or Escalate If:**

* AUTO REF is disabled.
* Axis button does not change from green to yellow.
* Axis movement does not begin.
* Unexpected motion or fault occurs.

**Source Evidence:**
Official manual, section 5.3: Starting the Operator Station.
Official manual, Operator Station Control Panel description.

---

### Step 6 — Wait for homing movement to complete

**Responsible role:** Operator
**Supporting role:** L1 Support

**Purpose:**
Confirm the tipper motor completes the documented homing movement.

**Instruction:**
Observe the tipper motor as it moves until it senses the home proximity switch, then stops.

**Expected result:**
The tipper motor moves to the home position and stops.

**Healthy condition:**
The motor moves as expected and stops after sensing the home proximity switch.

**Failure condition:**
The motor does not move, does not stop, faults, or cannot be confirmed to have reached home.

**Actions:**

| Field         | Value                                                                                   |
| ------------- | --------------------------------------------------------------------------------------- |
| Action Type   | `inspection_action`                                                                     |
| Label         | Observe homing movement                                                                 |
| Exact Action  | Watch for the tipper motor to move until it senses the home proximity switch and stops. |
| Role Required | `operator`                                                                              |

**Commands:**
None.

**Screens or Images:**

| Artifact ID                                               | What To Look At                                   |
| --------------------------------------------------------- | ------------------------------------------------- |
| `artifact_manual_fig_4_19_operator_station_control_panel` | Axis reference indicators and axis status fields. |

**Stop or Escalate If:**

* Tipper motor fails to move.
* Tipper motor does not stop.
* Axis does not appear referenced.
* A fault occurs.

**Source Evidence:**
Official manual, section 5.3: Starting the Operator Station.

---

### Step 7 — Press CYCLE START

**Responsible role:** Operator
**Supporting role:** L1 Support

**Purpose:**
Start the tipper operation cycle after axes have been homed.

**Instruction:**
Press CYCLE START.

**Expected result:**
The motor moves from home to ready.

**Healthy condition:**
Motor moves from home to ready without fault.

**Failure condition:**
CYCLE START does not work, motor does not move to ready, or a fault appears.

**Actions:**

| Field         | Value                                                        |
| ------------- | ------------------------------------------------------------ |
| Action Type   | `hmi_action`                                                 |
| Label         | Press CYCLE START                                            |
| Exact Action  | Press CYCLE START on the Operator Station HMI/control panel. |
| Role Required | `operator`                                                   |

**Commands:**
None.

**Screens or Images:**

| Artifact ID                                               | What To Look At                                          |
| --------------------------------------------------------- | -------------------------------------------------------- |
| `artifact_manual_fig_4_19_operator_station_control_panel` | CYCLE START control and related tipper state indicators. |

**Stop or Escalate If:**

* CYCLE START is unavailable.
* Motor does not move from home to ready.
* A fault appears.

**Source Evidence:**
Official manual, section 5.3: Starting the Operator Station.

---

### Step 8 — Place the tipper in AUTO mode

**Responsible role:** Operator
**Supporting role:** L1 Support

**Purpose:**
Return the tipper to automatic operation so it can wait for WCS instructions.

**Instruction:**
Place the tipper in AUTO mode.

**Expected result:**
The tipper enters AUTO mode and waits for WCS instructions.

**Healthy condition:**
AUTO mode is active and the tipper is waiting for WCS instructions.

**Failure condition:**
AUTO mode cannot be enabled, the tipper does not wait for WCS instructions, or an alarm/fault appears.

**Actions:**

| Field         | Value                                                                |
| ------------- | -------------------------------------------------------------------- |
| Action Type   | `hmi_action`                                                         |
| Label         | Enable AUTO mode                                                     |
| Exact Action  | Press or select AUTO mode on the Operator Station HMI/control panel. |
| Role Required | `operator`                                                           |

**Commands:**
None.

**Screens or Images:**

| Artifact ID                                                 | What To Look At                                                         |
| ----------------------------------------------------------- | ----------------------------------------------------------------------- |
| `artifact_manual_fig_4_19_operator_station_control_panel`   | AUTO button and active status indication.                               |
| `artifact_manual_fig_4_20_operator_station_hmi_data_screen` | Process status indicators, if checking operational state after startup. |

**Stop or Escalate If:**

* AUTO mode cannot be enabled.
* AUTO indicator does not become active.
* Tipper does not wait for WCS instructions.
* Any fault or alarm appears.

**Source Evidence:**
Official manual, section 5.3: Starting the Operator Station.
Official manual, Operator Station Control Panel description.

---

## Success Criteria

The runbook is successful when:

* AGVs are confirmed powered on.
* Main disconnect is ON.
* Flashing ESTOP condition, if present, has been cleared using the documented action.
* Z1 and A1 for the left tipper have been homed.
* Z2 and A2 for the right tipper have been homed.
* Axis button changes from green to yellow during movement.
* Tipper motor moves until it senses the home proximity switch, then stops.
* CYCLE START is pressed.
* Motor moves from home to ready.
* Tipper is placed in AUTO mode.
* Tipper waits for WCS instructions.

---

## Healthy Conditions

* Operator Station HMI is available.
* Required HMI controls are visible.
* RESET clears the documented flashing ESTOP/fault condition.
* AUTO REF initiates homing.
* Axis indicators behave as documented.
* Motor moves from home to ready.
* AUTO mode is enabled.
* No active startup-blocking faults are visible.

---

## Failure Conditions

* AGVs are not powered on.
* Main disconnect is not ON.
* ESTOP remains flashing after documented reset action.
* Faults do not clear after RESET.
* Axis indicators are missing or do not change as expected.
* Axis does not home.
* Motor does not move to ready.
* AUTO mode cannot be enabled.
* Tipper does not wait for WCS instructions.
* Any undocumented alarm/fault appears.

---

## Escalation Guidance

Escalate to L2 Support if:

* AGV power state cannot be confirmed.
* Faults do not clear after pressing RESET.
* AUTO REF is unavailable or does not initiate homing.
* Any axis fails to home.
* The motor does not move from home to ready after CYCLE START.
* AUTO mode cannot be enabled.
* The Operator Station HMI controls are missing or unavailable.
* The operator observes a fault or alarm not covered by this runbook.

Escalate to L3 Support if:

* L2 Support suspects a control/software issue.
* WCS instructions are not received after startup appears complete.
* The issue appears related to WCS, HMI, PLC, controller, or system integration behavior.
* Multiple stations show the same unexpected startup behavior.

---

## Commands

No terminal, PowerShell, SQL, API, or service-control commands are provided by the source for this procedure.

Do not invent commands.

---

## Missing Details / Known Gaps

* The manual references a separate Geek+ P40A V2.0 user manual for AGV startup instructions.
* The source does not provide additional recovery steps if AGVs are not powered on.
* The source does not provide additional recovery steps if faults do not clear.
* The source does not provide additional recovery steps if an axis fails to home.
* The source does not provide additional recovery steps if AUTO mode cannot be enabled.
* Figure/artifact mapping for the page 82 startup image should be validated.

---

## Source Evidence

### Official Manual Evidence

| Source           | Details                                                                                                                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source ID        | `manual_optisweep_om_v3`                                                                                                                                                                     |
| Source Type      | `manual`                                                                                                                                                                                     |
| Source Title     | OptiSweep Operation and Maintenance Manual                                                                                                                                                   |
| Source Version   | 3                                                                                                                                                                                            |
| Section          | 5.3: Starting the Operator Station                                                                                                                                                           |
| Page             | 82                                                                                                                                                                                           |
| Evidence Summary | Startup includes verifying AGVs are powered on, verifying the main disconnect is ON, clearing flashing ESTOP faults, homing axes, pressing CYCLE START, and placing the tipper in AUTO mode. |

### Supporting Manual Context

| Source           | Details                                                                                                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| Section          | 4.1.2: Operator Station HMI Screens                                                                             |
| Evidence Summary | Operator Station HMI navigation and display controls.                                                           |
| Section          | 4.1.2.1: Tipper Machine Control Panel / Visu_MCP_Dual Screen                                                    |
| Evidence Summary | Describes AUTO, JOG, REF, CYCLE START, CYCLE STOP, RESET, AUTO REF, ESTOP RESET, and axis reference indicators. |

---

## Candidate Merge Inputs

This canonical runbook may be created from candidate packets such as:

| Candidate ID                                                       | Source Type    | Merge Treatment                                                                                                                          |
| ------------------------------------------------------------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `candidate_operator_station_start_system_after_power_off`          | manual         | Primary source-derived candidate                                                                                                         |
| `candidate_operator_start_operator_station_and_home_tipper_axes`   | manual         | Same-source near duplicate; do not use semantic cross-source merge, but flag as same-source duplicate candidate for deterministic review |
| `candidate_operator_station_clear_flashing_estop_and_reset_faults` | manual         | Related recovery candidate; attach as related runbook or sub-step evidence, do not absorb if it should remain standalone                 |
| `candidate_training_operator_station_startup`                      | training_slide | Future cross-source evidence candidate                                                                                                   |
| `candidate_incident_restart_operator_station_after_fault`          | incident       | Future cross-source evidence candidate                                                                                                   |

---

## Merge History

| Event    | Source              | Notes                                                              |
| -------- | ------------------- | ------------------------------------------------------------------ |
| Created  | Official manual     | Created from section 5.3 and related Operator Station HMI context. |
| Enhanced | Training slides     | Placeholder for future training evidence.                          |
| Enhanced | Training transcript | Placeholder for future transcript evidence.                        |
| Enhanced | Incident data       | Placeholder for future incident evidence.                          |

---

## Validation

| Field             | Value              |
| ----------------- | ------------------ |
| Validation Status | `needs_sme_review` |
| Reviewed By       |                    |
| Reviewed Date     |                    |
| Approval Status   | Not approved       |
| SME Comments      |                    |

---

## JSON Output Expectations

The Stage 7 tool should convert this Markdown runbook into a matching JSON record.

Minimum required JSON fields:

```json
{
  "procedure_id": "proc_start_operator_station_v1",
  "title": "Start Operator Station",
  "procedure_type": "operation",
  "summary": "",
  "role_required": "operator",
  "responsible_role": "operator",
  "supporting_roles": ["L1_support", "L2_support"],
  "support_safe": true,
  "estimated_time_minutes": 10,
  "when_to_use": "",
  "not_for": [],
  "safety_notes": [],
  "access_or_tools_needed": [],
  "steps": [],
  "success_criteria": [],
  "healthy_conditions": [],
  "failure_conditions": [],
  "escalation_guidance": [],
  "commands": [],
  "screens_or_images": [],
  "source_refs": [],
  "image_refs": [],
  "related_context_ids": [],
  "source_candidate_ids": [],
  "source_lineage": [],
  "validation_status": "needs_sme_review",
  "metadata": {
    "product": "OptiSweep",
    "version": 1,
    "merge_status": "new",
    "created_by": "stage_7_canonical_runbook_drafting"
  }
}
```
