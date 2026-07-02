# Start The Operator Station After The System Has Been Turned Off

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_start_the_operator_station_after_the_system_has_been_turned_off_v1` |
| Title | Start The Operator Station After The System Has Been Turned Off |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Bring the operator station from an off state to a ready state by verifying power conditions, clearing any flashing ESTOP fault condition, homing the tipper axes, starting the cycle, and placing the tipper in AUTO mode.

## When To Use

Use when the system has been turned off and the operator station must be started and returned to a ready state.

## Do Not Use For

* Do not use this runbook as the source for AGV startup instructions; the source directs the user to the referenced P40A (V2.0) user manual for AGV startup steps.
* Do not use this runbook for fault recovery beyond pulling out a flashing ESTOP and pressing RESET; the source does not provide additional recovery steps if faults do not clear.

## Safety And Operational Notes

* If the ESTOP is flashing, pull out the ESTOP and press RESET on the HMI screen to clear any faults.
* Do not invent additional recovery actions if faults do not clear after RESET; escalate per site practice or SME review because the source does not provide further steps.

## Access Or Tools Needed

* Operator station control panel
* System HMI
* Access to the main disconnect
* Access to AGV power status
* Referenced P40A (V2.0) user manual for AGV startup instructions

## Related Operational Context

* ctx_manual_operator_station_overview_v1
* ctx_manual_estop_reset_reference_v1
* ctx_manual_tipper_axis_homing_reference_v1
* ctx_manual_hmi_axis_button_status_v1
* ctx_manual_tipper_auto_mode_ready_v1

## Procedure Steps

### Step 1 — Verify AGVs are powered on

**Responsible role:** operator

**Instruction:**
Verify the AGVs are powered on. Use the referenced P40A (V2.0) user manual for AGV startup instructions because this source does not provide those AGV startup steps.

**Expected result:**
AGVs are confirmed powered on.

**Stop or Escalate If:**

* AGVs are not powered on.
* AGV startup instructions are needed beyond verification, because this source does not include them.

---

### Step 2 — Verify the main disconnect is ON

**Responsible role:** operator

**Instruction:**
Verify the main disconnect is ON.

**Expected result:**
The main disconnect is confirmed ON.

**Stop or Escalate If:**

* The main disconnect is not ON.

---

### Step 3 — Check whether the ESTOP is flashing

**Responsible role:** operator

**Instruction:**
At the operator station control panel, check whether the ESTOP is flashing.

**Expected result:**
The ESTOP condition is identified as flashing or not flashing.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*System screen artifact associated with startup and ESTOP reset context.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Operator station control panel layout for locating relevant controls and status areas.*


**Stop or Escalate If:**

* The ESTOP is flashing and faults must be cleared before continuing.

---

### Step 4 — Clear a flashing ESTOP fault

**Responsible role:** operator

**Instruction:**
If the ESTOP is flashing, pull out the ESTOP and press RESET on the HMI screen to clear any faults.

**Expected result:**
Any faults associated with the flashing ESTOP are cleared.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup system screen context associated with ESTOP reset.*

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*RESET control on the operator station HMI in related fault-reset context.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Related HMI context mentioning RESET and AUTO REF.*


**Stop or Escalate If:**

* Faults do not clear after pressing RESET.
* Additional recovery is needed beyond RESET, because the source does not provide further steps.

---

### Step 5 — Identify all axes to be homed

**Responsible role:** operator

**Instruction:**
Home every documented axis: Z1 and A1 for the left tipper, and Z2 and A2 for the right tipper.

**Expected result:**
The operator identifies the full set of axes that must be homed.

**Screens / Images:**

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Axis naming context for Z1, Z2, A1, and A2.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Primary operator screen used to control tipper movement and referencing.*


**Stop or Escalate If:**

* Required axes cannot be identified on the available HMI or controls.

---

### Step 6 — Start automatic axis referencing

**Responsible role:** operator

**Instruction:**
Press AUTO REF to home the axes.

**Expected result:**
Automatic axis homing begins.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup system screen context that includes AUTO REF.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Related HMI context mentioning AUTO REF.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Control panel reference for homing/reference controls.*


**Stop or Escalate If:**

* AUTO REF does not initiate homing.

---

### Step 7 — Observe axis homing movement to completion

**Responsible role:** operator

**Instruction:**
Observe the axis button change from green to yellow to indicate it is moving, and allow the tipper motor to move until it senses the home proximity switch and stops.

**Expected result:**
The axis button changes from green to yellow during movement, and the tipper motor stops after sensing the home proximity switch.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup system screen context for axis homing status.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Operator station screen layout where active controls and status are shown.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Related HMI context for referencing and axis movement.*


**Stop or Escalate If:**

* The axis button does not change from green to yellow during homing.
* The tipper motor does not stop after sensing the home proximity switch.

---

### Step 8 — Start the cycle

**Responsible role:** operator

**Instruction:**
Press CYCLE START.

**Expected result:**
The cycle start command is issued.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup system screen context that includes CYCLE START.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*CYCLE START control on the operator station control panel.*

![artifact_page_86_image_10](assets/artifact_page_86_image_10.png)

*Related operator station context around AUTO and CYCLE START.*


**Stop or Escalate If:**

* CYCLE START does not initiate the expected motion toward ready.

---

### Step 9 — Verify the motor moves from home to ready

**Responsible role:** operator

**Instruction:**
Verify the motor moves from home to ready.

**Expected result:**
The motor moves from home to ready.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup system screen context for move from home to ready.*

![artifact_page_86_image_10](assets/artifact_page_86_image_10.png)

*Related operator station context around cycle start and automatic mode.*


**Stop or Escalate If:**

* The motor does not move from home to ready.

---

### Step 10 — Place the tipper in AUTO mode

**Responsible role:** operator

**Instruction:**
Place the tipper in AUTO mode.

**Expected result:**
The tipper is placed in AUTO mode.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup system screen context for placing the tipper in AUTO mode.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*AUTO control on the operator station control panel.*

![artifact_page_86_image_10](assets/artifact_page_86_image_10.png)

*Related operator station context around switching to AUTO.*


**Stop or Escalate If:**

* AUTO mode cannot be selected or does not remain active.

---

### Step 11 — Verify the tipper is waiting for WCS instructions

**Responsible role:** operator

**Instruction:**
Verify the tipper waits for the WCS to send instructions.

**Expected result:**
The tipper is in AUTO mode and waiting for WCS instructions.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup system screen context for final ready/AUTO state.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Related HMI context for AUTO and cycle operation.*


**Stop or Escalate If:**

* The tipper does not enter the expected waiting-for-WCS state.

---

## Success Criteria

* AGVs are verified powered on.
* Main disconnect is verified ON.
* Any flashing ESTOP condition is cleared using pull-out and RESET.
* Axes Z1, A1, Z2, and A2 are homed using AUTO REF.
* Axis movement is observed by button color change from green to yellow and stops at the home proximity switch.
* CYCLE START is pressed and the motor moves from home to ready.
* The tipper is placed in AUTO mode.
* The tipper waits for WCS instructions.

## Failure Conditions

* AGVs are not powered on.
* Main disconnect is not ON.
* Flashing ESTOP faults do not clear after RESET.
* AUTO REF does not start homing.
* Axis button does not change from green to yellow during homing.
* Tipper motor does not stop at the home proximity switch.
* Motor does not move from home to ready after CYCLE START.
* Tipper does not enter AUTO mode or does not wait for WCS instructions.

## Escalation Guidance

* If AGV startup is required, use the referenced P40A (V2.0) user manual because this source does not provide AGV startup steps.
* If faults do not clear after pulling out the ESTOP and pressing RESET, stop and escalate because the source does not provide further recovery actions.
* If homing or move-to-ready behavior does not occur as described, stop and escalate for SME review because the source does not provide additional troubleshooting in this startup procedure.

## Missing Details / Known Gaps

* The source does not provide AGV startup sub-steps; it only states that AGVs must be powered on and references the P40A (V2.0) user manual.
* The source does not provide additional troubleshooting or recovery steps if RESET does not clear a flashing ESTOP fault.
* The source does not provide an estimated completion time.
* The source does not explicitly state whether production stop or LOTO is required for this startup procedure.

## Source Lineage

- Candidate IDs: candidate_operator_station_start_system_after_power_off
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
