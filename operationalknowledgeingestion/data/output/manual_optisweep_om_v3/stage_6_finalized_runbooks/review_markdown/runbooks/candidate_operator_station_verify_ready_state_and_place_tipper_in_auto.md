# Move The Tipper From Home To Ready And Place It In AUTO Mode

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_move_the_tipper_from_home_to_ready_and_place_it_in_auto_mode_v1` |
| Title | Move The Tipper From Home To Ready And Place It In AUTO Mode |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Advance the tipper from the homed state to ready and place it in AUTO mode so it waits for WCS instructions.

## When To Use

Use after the tipper has been homed and the operator station is being placed into its documented ready operating state. This procedure is used to move the motor from home to ready, place the tipper in AUTO mode, and confirm the tipper is waiting for WCS instructions.

## Do Not Use For

* WCS communication troubleshooting
* Recovery when the motor does not move to ready
* Recovery when AUTO mode cannot be established

## Safety And Operational Notes

* Use only the documented operator station controls and HMI actions supported by the source.
* The source does not provide additional recovery steps if the motor does not move to ready or if AUTO mode cannot be established.
* Do not infer WCS communication troubleshooting from this section.

## Access Or Tools Needed

* Operator station controls or HMI with CYCLE START
* Ability to place the tipper in AUTO mode

## Related Operational Context

* ctx_manual_tipper_auto_mode_ready_v1
* ctx_manual_operator_station_overview_v1

## Procedure Steps

### Step 1 — Press CYCLE START

**Responsible role:** operator

**Instruction:**
At the operator station, press CYCLE START.

**Expected result:**
The startup sequence begins and the tipper motor proceeds from home toward ready.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the CYCLE START control on the operator station control panel.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup-related system screen context associated with pressing CYCLE START.*


**Stop or Escalate If:**

* CYCLE START does not initiate the expected move from home to ready.
* The source does not provide additional recovery steps for failure to move to ready.

---

### Step 2 — Verify the motor moves from home to ready

**Responsible role:** operator

**Instruction:**
Verify that the motor moves from home to ready after CYCLE START is pressed.

**Expected result:**
The motor moves from home to ready.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup screen context associated with the move from home to ready.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Operator station control panel context for the ready-state transition.*


**Stop or Escalate If:**

* The motor does not move from home to ready.
* The source does not provide additional recovery steps if the motor does not move to ready.

---

### Step 3 — Place the tipper in AUTO mode

**Responsible role:** operator

**Instruction:**
Place the tipper in AUTO mode.

**Expected result:**
The tipper is in AUTO mode.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Locate the AUTO button on the operator station control panel.*

![artifact_page_86_image_10](assets/artifact_page_86_image_10.png)

*Nearby operator station context showing AUTO as part of manual-supported operator actions.*


**Stop or Escalate If:**

* AUTO mode cannot be established.
* The source does not provide additional recovery steps if AUTO mode cannot be established.

---

### Step 4 — Verify the tipper waits for WCS instructions

**Responsible role:** operator

**Instruction:**
Verify the tipper is waiting for the WCS to send instructions.

**Expected result:**
The tipper waits for the WCS to send instructions.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup-related screen context associated with the AUTO waiting state.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Operator station main control context after AUTO mode is set.*


**Stop or Escalate If:**

* The tipper does not appear to be waiting for WCS instructions.
* Do not infer WCS communication troubleshooting from this section.

---

## Success Criteria

* The motor has moved from home to ready.
* The tipper is in AUTO mode.
* The tipper is waiting for WCS instructions.

## Failure Conditions

* CYCLE START does not initiate the expected transition.
* The motor does not move from home to ready.
* AUTO mode cannot be established.
* The tipper does not appear to be waiting for WCS instructions.

## Escalation Guidance

* Escalate if the motor does not move from home to ready because the source does not provide additional recovery steps.
* Escalate if AUTO mode cannot be established because the source does not provide additional recovery steps.
* Do not perform inferred WCS communication troubleshooting from this section.

## Missing Details / Known Gaps

* The source does not specify a documented indicator or screen field to confirm the ready state beyond stating that the motor moves from home to ready.
* The source does not specify a documented indicator or screen field to confirm AUTO mode beyond instructing the operator to place the tipper in AUTO mode.
* The source does not provide recovery or troubleshooting steps if the motor does not move to ready.
* The source does not provide recovery or troubleshooting steps if AUTO mode cannot be established.
* The source does not provide WCS-side actions or troubleshooting details.

## Source Lineage

- Candidate IDs: candidate_operator_station_verify_ready_state_and_place_tipper_in_auto
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
