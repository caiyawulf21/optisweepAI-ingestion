# Stop The Operator Station From The Main Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_stop_the_operator_station_from_the_main_screen_v1` |
| Title | Stop The Operator Station From The Main Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Stop the operator station using the documented CYCLE STOP control on the operator station main screen.

## When To Use

Use when the operator needs to stop the operator station from the operator station main screen using the documented HMI control.

## Do Not Use For

* Do not use this runbook for system shutdown from the system API screen.
* Do not use this runbook as a lockout/tagout procedure.
* Do not use this runbook for fault recovery, manual reset, jogging, or axis referencing procedures.

## Safety And Operational Notes

* This runbook only covers the documented HMI stop action for the operator station.
* The related lockout/tagout reference indicates additional steps are required before LOTO, including turning the operator station electrical panel power switch to OFF before LOTO.
* No additional safety controls, confirmations, or recovery actions are provided in the source section for this stop action.

## Access Or Tools Needed

* Access to the operator station HMI main screen

## Related Operational Context

* ctx_manual_operator_station_loto_reference_v1

## Procedure Steps

### Step 1 — Go to the operator station main screen

**Responsible role:** operator

**Instruction:**
Go to the operator station main screen.

**Expected result:**
The operator station main screen is displayed.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Use the page 82 stopping/startup screen artifact associated with the stopping the operator station procedure.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Use the operator station control panel figure as a visual reference for the main operator HMI screen and its controls.*


**Stop or Escalate If:**

* The operator station main screen cannot be accessed or displayed.

---

### Step 2 — Locate the CYCLE STOP control

**Responsible role:** operator

**Instruction:**
Locate the CYCLE STOP control on the operator station main screen.

**Expected result:**
The CYCLE STOP control is identified on the operator station main screen.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Look for the operator station stopping/startup screen context associated with CYCLE STOP.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Look for the CYCLE STOP control on the operator station control panel figure.*


**Stop or Escalate If:**

* The CYCLE STOP control is not visible on the operator station main screen.

---

### Step 3 — Press CYCLE STOP

**Responsible role:** operator

**Instruction:**
Press CYCLE STOP.

**Expected result:**
The operator station is stopped using the documented main screen control.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Use the figure to identify the CYCLE STOP control before pressing it.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Use the page 82 artifact associated with the stopping procedure as supporting visual context.*


**Stop or Escalate If:**

* Pressing CYCLE STOP does not stop the operator station.
* Additional recovery, confirmation, or escalation details are needed beyond what the source provides.

---

## Success Criteria

* The operator station is stopped using the documented CYCLE STOP control on the operator station main screen.

## Failure Conditions

* The operator station main screen cannot be accessed.
* The CYCLE STOP control cannot be located on the operator station main screen.
* Pressing CYCLE STOP does not stop the operator station.
* The source does not provide additional recovery, confirmation, or escalation details if the stop action does not work.

## Escalation Guidance

* If the operator station main screen cannot be accessed, stop and seek site-specific support because the source does not provide an alternate method in this procedure.
* If the CYCLE STOP control cannot be located or does not work, stop and escalate for SME or support review because the source does not provide recovery or confirmation details.

## Missing Details / Known Gaps

* The source section does not provide explicit confirmation indicators after pressing CYCLE STOP.
* The source section does not provide alternate navigation instructions to reach the operator station main screen.
* The source section does not provide recovery steps if the stop action fails.
* The source section does not provide an estimated completion time.
* The source section does not state whether production stop or LOTO is required for this specific action.

## Source Lineage

- Candidate IDs: candidate_operator_stop_operator_station_via_cycle_stop
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
