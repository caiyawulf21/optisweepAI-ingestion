# Clear A Flashing ESTOP Condition At The Operator Station

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_clear_a_flashing_estop_condition_at_the_operator_station_v1` |
| Title | Clear A Flashing ESTOP Condition At The Operator Station |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Clear a documented flashing ESTOP condition at the operator station by pulling out the ESTOP and pressing RESET on the HMI screen to clear faults before continuing startup.

## When To Use

Use this procedure when the operator station control panel shows a flashing ESTOP during operator station startup or readiness checks.

## Do Not Use For

* Do not use this procedure for faults other than the documented flashing ESTOP condition.
* Do not use this procedure to perform additional fault-clearing actions not described in the source.
* Do not continue with normal startup actions until the flashing ESTOP condition has cleared.

## Safety And Operational Notes

* Use only the documented ESTOP pull-out and HMI RESET actions supported by the source.
* The source does not provide additional recovery actions if faults do not clear after RESET.
* Do not invent additional fault-clearing, bypass, or override actions beyond the documented procedure.

## Access Or Tools Needed

* Operator station control panel
* HMI screen

## Related Operational Context

* ctx_manual_estop_reset_reference_v1
* ctx_manual_operator_station_overview_v1

## Procedure Steps

### Step 1 — Observe the operator station for a flashing ESTOP

**Responsible role:** operator

**Instruction:**
At the operator station control panel, observe whether the ESTOP is flashing.

**Expected result:**
The operator determines whether the ESTOP is flashing.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Operator station control panel context for locating the operator controls.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*System/startup screen context associated with the page containing the flashing ESTOP instruction.*


**Stop or Escalate If:**

* The ESTOP condition cannot be determined from the operator station control panel.

---

### Step 2 — Pull out the flashing ESTOP

**Responsible role:** operator

**Instruction:**
If the ESTOP is flashing, pull out the ESTOP.

**Expected result:**
The ESTOP is physically reset to the pulled-out position.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Operator station control panel area for the ESTOP location.*


**Stop or Escalate If:**

* The ESTOP cannot be pulled out or does not reset physically.

---

### Step 3 — Press RESET on the HMI to clear faults

**Responsible role:** operator

**Instruction:**
On the HMI screen, press RESET to clear any faults.

**Expected result:**
Any faults addressed by the documented RESET action are cleared.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*System/startup screen context associated with the flashing ESTOP and RESET instruction.*

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*RESET control shown on the operator station HMI in a fault recovery context.*

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*General operator station HMI screen context.*


**Stop or Escalate If:**

* Faults do not clear after pressing RESET.
* Additional recovery steps are needed but are not provided by the source.

---

### Step 4 — Verify the flashing ESTOP condition has cleared

**Responsible role:** operator

**Instruction:**
Verify the flashing ESTOP condition has cleared before continuing with normal startup actions.

**Expected result:**
The flashing ESTOP condition is no longer present and startup can continue.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Operator station control panel to confirm the ESTOP is no longer flashing.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Startup procedure context for continuing only after the ESTOP condition is cleared.*


**Stop or Escalate If:**

* The ESTOP continues flashing after the documented reset actions.
* Faults remain after pressing RESET and no further source-supported steps are available.

---

## Success Criteria

* The ESTOP has been pulled out.
* RESET has been pressed on the HMI screen.
* Any faults addressed by the documented RESET action are cleared.
* The flashing ESTOP condition is no longer present and normal startup can continue.

## Failure Conditions

* The ESTOP cannot be reset by pulling it out.
* Faults do not clear after pressing RESET.
* The flashing ESTOP condition remains present after the documented actions.
* The source provides no additional recovery steps for unresolved faults.

## Escalation Guidance

* If faults do not clear after pressing RESET, stop at the documented boundary because the source does not provide additional steps.
* If the flashing ESTOP condition remains after completing the documented actions, do not invent further recovery actions; seek SME or site-specific guidance outside this source.

## Missing Details / Known Gaps

* The source does not provide additional troubleshooting or escalation steps if faults do not clear after pressing RESET.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required for this action.
* The source does not identify a specific HMI screen name for the RESET action in this procedure.

## Source Lineage

- Candidate IDs: candidate_operator_station_clear_flashing_estop_and_reset_faults
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
