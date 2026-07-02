# Start A Left Or Right Tipper Cycle Using The Operator Station Push-Buttons

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_start_a_left_or_right_tipper_cycle_using_the_operator_station_push_buttons_v1` |
| Title | Start A Left Or Right Tipper Cycle Using The Operator Station Push-Buttons |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station push-buttons to identify which tipper side is ready, determine whether the tote requires the standard or Surepost cycle based on the flashing button color, and press the corresponding flashing button to start the left or right tipper cycle.

## When To Use

Use this procedure when a tote has arrived at the operator station tipper and the operator must start the left or right tipping cycle using the physical push-buttons at the operator station.

## Do Not Use For

* Do not use the emergency stop push-button as part of normal tipper cycle initiation.
* Do not rely on a tip button press made before a tote is in the gripper, because the source states that command is ignored.

## Safety And Operational Notes

* The emergency stop button is only used if there is imminent danger to personnel or damage to equipment.
* Do not use the emergency stop push-button during normal tipper cycle initiation.
* If the tip button is pressed before a tote is in the gripper, the tipper will ignore that command.

## Access Or Tools Needed

* Physical access to the operator station
* Visual access to the operator station push-buttons
* Operator station push-button layout from Figure 3-3 and Table 3-2

## Related Operational Context

* ctx_manual_operator_station_push_buttons_overview_v1
* ctx_manual_tipper_axis_mapping_v1
* ctx_manual_hmi_axis_button_status_v1
* ctx_manual_operator_station_tipper_interlock_status_v1

## Procedure Steps

### Step 1 — Identify the operator station push-button layout

**Responsible role:** operator

**Instruction:**
Go to the operator station and identify the push-button layout. Use the top two buttons for the left tipper and the bottom two buttons for the right tipper. Identify the emergency stop push-button separately from the cycle start buttons.

**Expected result:**
The operator can correctly identify which buttons belong to the left tipper, which belong to the right tipper, and which button is the emergency stop.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*Top two buttons for left tipper, bottom two buttons for right tipper, and emergency stop location.*

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Overall operator station location and physical control area.*


**Stop or Escalate If:**

* Stop and escalate if the push-button layout does not match the documented arrangement.
* Stop and escalate if the emergency stop cannot be clearly distinguished from the cycle buttons.

---

### Step 2 — Observe which tipper button is flashing

**Responsible role:** operator

**Instruction:**
Observe the operator station push-buttons and identify which button is flashing for the tote that has arrived at the tipper.

**Expected result:**
A flashing button indicates the tipper side and cycle type that is ready to be started.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The physical push-buttons used to start left or right tipper cycles, including Surepost buttons and emergency stop.*


**Stop or Escalate If:**

* Escalate if the observed button behavior does not match the documented flashing behavior.
* Escalate if a tote is expected to be gripped but no corresponding button flashes.

---

### Step 3 — Interpret a flashing green button as the standard cycle

**Responsible role:** operator

**Instruction:**
If the flashing button is green, identify it as the standard tipper cycle button for that tipper.

**Expected result:**
The operator recognizes that the green flashing button is the correct button for a standard tipping cycle.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*Green button assignment for standard left or right tipper cycle.*


**Stop or Escalate If:**

* Escalate if the button color indication does not match the documented package-type behavior.

---

### Step 4 — Interpret a flashing yellow button as the Surepost cycle

**Responsible role:** operator

**Instruction:**
If the flashing button is yellow, identify it as the Surepost tipper cycle button for that tipper and press it only after the appropriate bag is ready for the Surepost packages.

**Expected result:**
The operator recognizes the Surepost cycle condition and waits until the appropriate bag is ready before starting the cycle.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*Yellow button assignment for Surepost left or right tipper cycle.*


**Stop or Escalate If:**

* Stop if the appropriate bag for Surepost packages is not ready.
* Escalate if the button color indication does not match the documented package-type behavior.

---

### Step 5 — Press the corresponding flashing button to start the cycle

**Responsible role:** operator

**Instruction:**
Press the corresponding flashing button for the left or right tipper to initiate the tipping cycle.

**Expected result:**
The selected left or right tipper cycle is initiated for the tote and package type indicated by the flashing button.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The physical green or yellow button corresponding to the ready left or right tipper.*


**Stop or Escalate If:**

* Escalate if the cycle does not initiate after a valid flashing button press.
* Stop if the only button being considered is the emergency stop push-button.

---

### Step 6 — Observe button behavior when both sides are waiting

**Responsible role:** operator

**Instruction:**
If both sides are flashing because both sides have AGVs waiting, press the button for the side you are starting and observe that the opposite side stops flashing until the opposite cycle is done.

**Expected result:**
After one tip button is pressed, the opposite side stops flashing until the opposite cycle is done.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*Both left and right tipper buttons and the change in opposite-side flashing after one side is started.*


**Stop or Escalate If:**

* Escalate if the opposite side does not stop flashing after one tip button is pressed when both sides were waiting.
* Escalate if button behavior does not match the documented interlock behavior.

---

### Step 7 — Do not rely on a button press made before the tote is gripped

**Responsible role:** operator

**Instruction:**
Do not rely on a button press made before a tote is gripped. If the tip button was pressed before a tote was in the gripper, expect that command to be ignored. Wait until the corresponding tip button flashes once the tote is gripped, then use the flashing button.

**Expected result:**
The operator understands that only a flashing button after tote grip indicates a valid cycle-start opportunity.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The corresponding tip button flashing only after the tote is gripped.*


**Stop or Escalate If:**

* Escalate if a valid flashing button press does not initiate the cycle after the tote is gripped.
* Do not continue assuming an early button press was accepted before tote grip.

---

## Success Criteria

* The operator identifies the correct left or right tipper push-button.
* The operator correctly interprets green as the standard cycle and yellow as the Surepost cycle.
* For Surepost packages, the operator waits until the appropriate bag is ready before pressing the yellow button.
* The corresponding flashing button is pressed and the selected tipping cycle is initiated.

## Failure Conditions

* The emergency stop push-button is used as part of normal cycle initiation.
* A button is pressed before a tote is in the gripper and the operator expects the command to be accepted.
* Observed button behavior does not match the documented flashing behavior.
* The cycle does not initiate after a valid flashing button press.

## Escalation Guidance

* Escalate if the observed button behavior does not match the documented flashing behavior.
* Escalate if the cycle does not initiate after a valid flashing button press.
* Escalate if the push-button layout or button assignment does not match the documented arrangement.

## Missing Details / Known Gaps

* The source does not provide a detailed cycle completion confirmation indicator beyond documented button flashing behavior.
* The source does not provide an estimated completion time for this procedure.
* The source does not specify production-stop or LOTO requirements for this normal operator action.

## Source Lineage

- Candidate IDs: candidate_operator_start_tipper_cycle_from_operator_station_push_buttons
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
