# Use The Operator Station Emergency Stop Push-Button In An Imminent Danger Situation

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_operator_station_emergency_stop_push_button_v1` |
| Title | Use The Operator Station Emergency Stop Push-Button In An Imminent Danger Situation |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Identify the operator station emergency stop push-button and use it only when there is imminent danger to personnel or risk of damage to equipment.

## When To Use

Use this procedure at the operator station when there is imminent danger to personnel or damage to the equipment and the documented emergency stop push-button must be used.

## Do Not Use For

* Do not use for normal tipper cycle starts.
* Do not use as a substitute for the four normal operator station tipper push-buttons.
* Do not use this runbook for emergency stop reset, restart, or restoration because those steps are not provided in this source section.

## Safety And Operational Notes

* The emergency stop button is only used if there is imminent danger to personnel or damage to the equipment.
* This source section identifies the emergency stop location and purpose but does not provide reset or restart steps after use.

## Access Or Tools Needed

* Physical access to the operator station
* Ability to identify the emergency stop push-button
* Figure 3-3 and Table 3-2

## Related Operational Context

* ctx_manual_operator_station_push_buttons_overview_v1
* ctx_manual_operator_station_emergency_stop_use_v1

## Procedure Steps

### Step 1 — Locate the emergency stop push-button

**Responsible role:** operator

**Instruction:**
At the operator station, locate the emergency stop push-button and distinguish it from the four normal tipper push-buttons using Figure 3-3 and Table 3-2.

**Expected result:**
The operator can identify the emergency stop push-button as the documented emergency control at the operator station.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The operator station push-buttons, especially item 5 identified as the emergency stop push-button relative to the left and right tipper buttons.*

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*The overall operator station location and push-button area for physical orientation.*


**Stop or Escalate If:**

* Stop if the emergency stop push-button cannot be positively identified from the operator station controls.
* Escalate if the push-button layout does not match the documented Figure 3-3 and Table 3-2 reference.

---

### Step 2 — Confirm the emergency condition matches the documented use

**Responsible role:** operator

**Instruction:**
Use the emergency stop push-button only if there is imminent danger to personnel or damage to the equipment.

**Expected result:**
The operator confirms the situation matches the documented emergency-use condition before pressing the button.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The push-button panel showing the emergency stop in the same control group as the normal tipper buttons.*


**Stop or Escalate If:**

* Stop if there is no imminent danger to personnel or damage to equipment.
* Escalate for follow-up recovery after emergency stop use because this source does not provide restoration steps.

---

### Step 3 — Press the emergency stop push-button

**Responsible role:** operator

**Instruction:**
Press the emergency stop push-button when the documented emergency condition exists.

**Expected result:**
The documented emergency stop control is used in response to the imminent danger condition.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The emergency stop push-button on the operator station push-button panel.*


**Stop or Escalate If:**

* Escalate for follow-up recovery because post-E-stop reset or restart steps are not provided in this source section.
* Escalate if additional recovery or restoration actions are needed after the emergency stop is used.

---

## Success Criteria

* The operator correctly identifies the emergency stop push-button at the operator station.
* The emergency stop push-button is used only when there is imminent danger to personnel or damage to the equipment.
* The documented emergency control is used instead of the normal tipper push-buttons during the emergency condition.

## Failure Conditions

* The emergency stop push-button cannot be identified from the operator station controls.
* The emergency stop is used for a non-emergency purpose.
* Post-emergency reset or restart is attempted using this runbook even though the source does not provide those steps.

## Escalation Guidance

* Escalate for follow-up recovery because this source only documents when to use the emergency stop and where it is located.
* Escalate if reset, restart, or restoration of operation is required after emergency stop use because those steps are not provided in this source section.
* Escalate if the physical push-button layout does not match the documented Figure 3-3 and Table 3-2 references.

## Missing Details / Known Gaps

* This source section does not describe the resulting machine state after the emergency stop is pressed.
* This source section does not provide emergency stop reset steps.
* This source section does not provide restart or restoration steps after emergency stop use.
* This source section does not provide an estimated completion time.
* This source section does not explicitly state whether production stop or LOTO is required as part of this action.

## Source Lineage

- Candidate IDs: candidate_operator_use_operator_station_emergency_stop_push_button
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
