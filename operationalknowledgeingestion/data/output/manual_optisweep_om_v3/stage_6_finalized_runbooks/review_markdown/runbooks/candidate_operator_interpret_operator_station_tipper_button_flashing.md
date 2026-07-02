# Interpret Flashing Operator Station Tipper Buttons Before Starting A Cycle

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_flashing_operator_station_tipper_buttons_before_starting_a_cycle_v1` |
| Title | Interpret Flashing Operator Station Tipper Buttons Before Starting A Cycle |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented operator-station push-button flashing behavior to determine which tipper side is ready, whether the tote contains Surepost packages or other packages, and whether opposite-side flashing is being suppressed by an active tipping cycle.

## When To Use

Use this reference when observing the operator station push-buttons before starting a tipper cycle and you need to interpret which tipper is ready, what package type is indicated by the flashing button color, or whether flashing on the opposite side is being delayed or suppressed by an active cycle.

## Do Not Use For

* Do not use this runbook to diagnose causes beyond the documented button behavior.
* Do not use this runbook as a broader troubleshooting or recovery procedure.

## Safety And Operational Notes

* Use visual observation only; this runbook does not authorize undocumented control actions.
* The emergency stop push-button shown in the operator station push-button figure is only used if there is imminent danger to personnel or damage to equipment.

## Access Or Tools Needed

* Visual access to the operator station push-buttons
* Documented push-button layout and flashing behavior from Figure 3-3 and Table 3-2

## Related Operational Context

* ctx_manual_operator_station_push_buttons_overview_v1
* ctx_manual_hmi_axis_button_status_v1
* ctx_manual_operator_station_tipper_interlock_status_v1

## Procedure Steps

### Step 1 — Identify left and right tipper push-button groups

**Responsible role:** operator

**Instruction:**
Locate the operator station push-buttons and identify which two buttons belong to the left tipper and which two belong to the right tipper.

**Expected result:**
You can distinguish the left tipper button pair from the right tipper button pair.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The top two buttons for the left tipper and the bottom two buttons for the right tipper.*

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Physical location of the operator station and push-button area.*


**Stop or Escalate If:**

* Escalate if the observed button layout does not match the documented left/right assignment.

---

### Step 2 — Observe which tipper-side button is flashing

**Responsible role:** operator

**Instruction:**
Observe whether a green or yellow button is flashing on the left or right tipper side.

**Expected result:**
You identify the flashing button color and the tipper side where it is flashing.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The green and yellow push-buttons used to start left or right tipper cycles, including Surepost tote cycles.*


**Stop or Escalate If:**

* Escalate if observed flashing behavior does not match the documented green, yellow, dual-flash, or suppressed-flash patterns.

---

### Step 3 — Interpret flashing yellow as Surepost tote delivery

**Responsible role:** operator

**Instruction:**
Interpret a flashing yellow button as indicating that a tote with Surepost packages is being delivered to that tipper.

**Expected result:**
A flashing yellow button is understood as a Surepost tote indication for that tipper.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The yellow Surepost tote cycle buttons for the left and right tippers.*


**Stop or Escalate If:**

* Escalate if a flashing yellow button is observed but the system behavior appears inconsistent with the documented Surepost indication.

---

### Step 4 — Interpret flashing green as all other packages

**Responsible role:** operator

**Instruction:**
Interpret a flashing green button for that tipper as indicating all other packages.

**Expected result:**
A flashing green button is understood as the indication for packages other than Surepost.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The green tipper cycle buttons for the left and right tippers.*


**Stop or Escalate If:**

* Escalate if a flashing green button is observed but the system behavior appears inconsistent with the documented all-other-packages indication.

---

### Step 5 — Interpret missing opposite-side flashing during an active cycle

**Responsible role:** operator

**Instruction:**
If one tipper is already in a tipping cycle, check whether the other side is not flashing even though a tote is present; compare that observation to the documented behavior that the other button will not start flashing until the first cycle is completed.

**Expected result:**
You can distinguish documented suppressed flashing from an unexplained missing indication.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The left and right tipper button pairs while one tipper cycle is already in process.*


**Stop or Escalate If:**

* Escalate if the opposite-side button behavior does not match the documented suppression during an active cycle.

---

### Step 6 — Interpret both sides flashing and opposite-side stop after one button press

**Responsible role:** operator

**Instruction:**
If both sides are flashing, interpret that as both sides having AGVs waiting, and note that once one tip button is pressed the opposite button stops flashing until the opposite cycle is done.

**Expected result:**
You understand that dual flashing indicates both sides waiting and that opposite-side flashing stopping after one button press is expected behavior.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*Both left and right tipper button pairs when both sides have AGVs waiting.*


**Stop or Escalate If:**

* Escalate if both sides are flashing or the opposite-side flashing stop behavior does not match the documented interaction.

---

### Step 7 — Interpret ignored early button presses before tote grip

**Responsible role:** operator

**Instruction:**
If a button was pressed before a tote was in the gripper, verify that the source says the command is ignored and that the corresponding tip button flashes only after the tote is gripped.

**Expected result:**
You understand that an early button press before tote grip is ignored and that flashing begins only after the tote is gripped.

**Screens / Images:**

![artifact_fig_3_3_operator_station_push_buttons](assets/artifact_fig_3_3_operator_station_push_buttons.png)

*The tipper cycle buttons and their flashing state relative to tote grip.*


**Stop or Escalate If:**

* Escalate if a button press before tote grip produces behavior inconsistent with the documented ignored-command behavior.

---

## Success Criteria

* The operator can identify which button pair belongs to the left tipper and which belongs to the right tipper.
* The operator can interpret flashing yellow as a Surepost tote indication.
* The operator can interpret flashing green as an all-other-packages indication.
* The operator can recognize documented suppressed flashing during an active opposite-side cycle.
* The operator can recognize documented dual-flashing behavior when both sides have AGVs waiting.
* The operator can recognize that a button press before tote grip is ignored until the tote is gripped.

## Failure Conditions

* Observed flashing behavior does not match the documented green, yellow, dual-flash, or suppressed-flash patterns.
* The operator cannot confirm left/right button assignment from the documented layout.
* A button response appears inconsistent with the documented ignored-command behavior before tote grip.
* The user attempts to infer undocumented causes beyond the source-provided button behavior.

## Escalation Guidance

* Escalate if observed flashing behavior does not match the documented green, yellow, dual-flash, or suppressed-flash patterns.
* Do not infer undocumented causes beyond the source-provided button behavior.
* Escalate if the button layout or flashing behavior at the station cannot be reconciled with Figure 3-3 and the documented notes.

## Missing Details / Known Gaps

* The source does not provide a time estimate for using this reference.
* The source does not define formal escalation contacts or routing.
* The source does not provide broader troubleshooting logic beyond the documented button behavior.
* The source does not specify production-stop or LOTO requirements for this observational reference.

## Source Lineage

- Candidate IDs: candidate_operator_interpret_operator_station_tipper_button_flashing
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
