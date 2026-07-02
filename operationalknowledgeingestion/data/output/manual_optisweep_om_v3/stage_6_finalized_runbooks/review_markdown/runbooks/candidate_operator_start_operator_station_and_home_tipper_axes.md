# Start The Operator Station And Home The Tipper Axes

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_start_the_operator_station_and_home_the_tipper_axes_v1` |
| Title | Start The Operator Station And Home The Tipper Axes |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Start the operator station by verifying AGV and power prerequisites, clearing a flashing ESTOP if present, homing axes Z1, A1, Z2, and A2 with AUTO REF, pressing CYCLE START so the motor moves from home to ready, and placing the tipper in AUTO mode to wait for WCS instructions.

## When To Use

Use when starting the operator station and preparing the tipper axes for operation as documented in the OptiSweep Operation and Maintenance Manual.

## Do Not Use For

* Do not use this runbook as the AGV startup procedure; the source states AGV startup details are in a separate AGV manual.
* Do not use this runbook for troubleshooting axis homing failures, uncleared faults, or failure to move to ready; the source does not provide those recovery steps here.

## Safety And Operational Notes

* If the ESTOP is flashing, pull out the ESTOP and press RESET on the HMI screen to clear any faults.
* The source does not provide additional safety controls, LOTO requirements, or production stop requirements for this procedure.

## Access Or Tools Needed

* Access to the operator station control panel
* Access to the operator station HMI
* AUTO REF control
* RESET control on the HMI
* CYCLE START control
* Ability to observe axis button color changes and tipper motion

## Related Operational Context

* ctx_manual_operator_station_startup_prerequisites_v1
* ctx_manual_estop_reset_reference_v1
* ctx_manual_tipper_auto_mode_ready_v1

## Procedure Steps

### Step 1 — Verify AGVs are powered on

**Responsible role:** operator

**Instruction:**
Verify the AGVs are powered on.

**Expected result:**
AGVs are confirmed powered on.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*AGV system startup-related screen context supporting the AGV powered-on prerequisite.*


**Stop or Escalate If:**

* AGVs are not powered on.
* AGV startup instructions are needed beyond this prerequisite check.

---

### Step 2 — Verify main disconnect is ON

**Responsible role:** operator

**Instruction:**
Verify the main disconnect is ON.

**Expected result:**
Main disconnect is confirmed ON.

**Stop or Escalate If:**

* Main disconnect is not ON.
* Main disconnect state cannot be verified.

---

### Step 3 — Clear flashing ESTOP if present

**Responsible role:** operator

**Instruction:**
At the operator station control panel, check whether the ESTOP is flashing. If it is flashing, pull out the ESTOP and press RESET on the HMI screen to clear any faults.

**Expected result:**
Any flashing ESTOP condition is cleared using the documented reset action.

**Screens / Images:**

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*RESET control on the operator station HMI.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Axis controls and RESET instruction on the operator station HMI.*

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*Emergency stop push-button on the operator station.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup procedure context on page 82 including ESTOP reset and HMI actions.*


**Stop or Escalate If:**

* ESTOP remains flashing after pulling it out and pressing RESET.
* Faults do not clear after pressing RESET.

---

### Step 4 — Home axes Z1, A1, Z2, and A2

**Responsible role:** operator

**Instruction:**
Home every axis: Z1 and A1 for the left tipper, and Z2 and A2 for the right tipper.

**Expected result:**
All documented axes are selected for homing.

**Screens / Images:**

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Operator station HMI context for referencing axes.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Axis labels Z1, Z2, A1, and A2 on the operator station HMI.*

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Axis controls for left and right tipper on the operator station screen.*


**Stop or Escalate If:**

* The required axes Z1, A1, Z2, and A2 cannot be identified on the HMI.

---

### Step 5 — Press AUTO REF

**Responsible role:** operator

**Instruction:**
Press AUTO REF.

**Expected result:**
Automatic referencing is initiated for the documented axes.

**Screens / Images:**

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*AUTO REF control on the operator station HMI.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup procedure context including AUTO REF.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Axis-related HMI controls that help orient the operator to the referencing screen.*


**Stop or Escalate If:**

* AUTO REF is unavailable on the HMI.
* Pressing AUTO REF does not initiate axis movement.

---

### Step 6 — Observe axis button color change during movement

**Responsible role:** operator

**Instruction:**
Observe that the axis button changes from green to yellow to indicate it is moving.

**Expected result:**
The axis button changes from green to yellow while the axis is moving.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*System screen artifact associated with startup and operator station procedures.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Axis referencing HMI context where status indications may be observed.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Axis buttons and controls on the operator station HMI.*


**Stop or Escalate If:**

* Axis button does not change from green to yellow.

---

### Step 7 — Observe tipper motor stop at home proximity switch

**Responsible role:** operator

**Instruction:**
Observe that the tipper motor moves until it senses the home proximity switch, then stops.

**Expected result:**
The tipper motor moves to the home position and stops when the home proximity switch is sensed.

**Stop or Escalate If:**

* Tipper motor does not move during homing.
* Tipper motor does not stop after reaching the home proximity switch.

---

### Step 8 — Press CYCLE START

**Responsible role:** operator

**Instruction:**
Press CYCLE START.

**Expected result:**
The cycle start command is issued.

**Screens / Images:**

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*CYCLE START control on the operator station HMI.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup procedure context including CYCLE START.*


**Stop or Escalate If:**

* CYCLE START is unavailable.
* Pressing CYCLE START does not initiate movement from home to ready.

---

### Step 9 — Observe motor move from home to ready

**Responsible role:** operator

**Instruction:**
Observe that the motor moves from home to ready.

**Expected result:**
The motor moves from home to ready.

**Stop or Escalate If:**

* Motor does not move from home to ready.

---

### Step 10 — Place tipper in AUTO mode

**Responsible role:** operator

**Instruction:**
Place the tipper in AUTO mode.

**Expected result:**
Tipper is placed in AUTO mode.

**Screens / Images:**

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*AUTO-related controls on the operator station HMI.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup procedure context including AUTO mode.*


**Stop or Escalate If:**

* AUTO mode cannot be set.

---

### Step 11 — Verify tipper waits for WCS instructions

**Responsible role:** operator

**Instruction:**
Verify the tipper waits for the WCS to send instructions.

**Expected result:**
Tipper is in AUTO mode and waiting for WCS instructions.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup procedure context describing the WCS wait state.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Operator station HMI context for AUTO and post-reference operation.*


**Stop or Escalate If:**

* Tipper does not remain in the expected waiting state for WCS instructions.

---

## Success Criteria

* AGVs are powered on.
* Main disconnect is ON.
* Any flashing ESTOP condition is cleared using the documented reset action.
* Axes Z1, A1, Z2, and A2 are homed.
* Axis button changes from green to yellow during movement.
* Tipper motor moves until it senses the home proximity switch and then stops.
* After CYCLE START, the motor moves from home to ready.
* Tipper is placed in AUTO mode.
* Tipper waits for WCS instructions.

## Failure Conditions

* AGVs are not powered on.
* Main disconnect is not ON.
* ESTOP remains flashing or faults do not clear after RESET.
* An axis does not home as expected.
* Axis button does not change from green to yellow as described.
* Tipper motor does not stop at the home proximity switch.
* Motor does not move from home to ready after CYCLE START.
* Tipper does not enter AUTO mode.
* Tipper does not wait for WCS instructions.

## Escalation Guidance

* Use the separate AGV manual for AGV startup instructions; this source does not include those steps here.
* If an axis does not home, the button color does not change as described, faults do not clear, or the motor does not move to ready, the source does not provide escalation guidance in this procedure.
* Escalate for SME review when the documented startup sequence cannot be completed using the source-backed steps above.

## Missing Details / Known Gaps

* The source references a separate AGV manual for AGV startup instructions and does not include those steps here.
* The source does not provide escalation guidance if an axis does not home, the button color does not change as described, faults do not clear, or the motor does not move to ready.
* The source does not provide an estimated completion time.
* The source does not specify supporting roles beyond the operator.
* The source does not specify whether production stop or LOTO is required for this procedure.

## Source Lineage

- Candidate IDs: candidate_operator_start_operator_station_and_home_tipper_axes
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
