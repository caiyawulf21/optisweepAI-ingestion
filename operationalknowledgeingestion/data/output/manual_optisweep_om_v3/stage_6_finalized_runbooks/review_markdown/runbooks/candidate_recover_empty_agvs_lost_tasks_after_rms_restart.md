# Recover Empty AGVs That Lost Tasks After an RMS Restart

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_empty_agvs_that_lost_tasks_after_rms_restart_v1` |
| Title | Recover Empty AGVs That Lost Tasks After an RMS Restart |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Restore empty AGVs to a recoverable state after their tasks were lost following an RMS restart by E-stopping RMS, removing and re-adding AGVs without totes twice using Tote API Controls, verifying AGV state as "szonestaging" on the HMI if a restart is needed, then resuming RMS.

## When To Use

Use when empty AGVs have lost their tasks because the RMS was restarted.

## Do Not Use For

* Do not use for AGVs with totes.
* Do not use for recovery scenarios that require actions beyond the documented remove and re-add steps.
* Do not proceed with restart-related recovery if AGV state cannot be verified as "szonestaging" on the HMI.

## Safety And Operational Notes

* The source notes that best practice is to shut down and restart to ensure everything is in sync.
* Do not invent additional recovery actions beyond the documented remove and re-add steps.
* If the system needs to be restarted, make sure the AGVs are in the "szonestaging" state.

## Access Or Tools Needed

* Access to RMS
* Access to Tote API Controls in RMS
* Access to the HMI to view AGV state
* Ability to use RMS E-stop and resume controls

## Related Operational Context

* ctx_manual_agv_szonestaging_status_v1
* ctx_manual_tote_api_controls_agv_membership_v1
* ctx_manual_rms_estop_resume_reference_v1

## Procedure Steps

### Step 1 — E-stop RMS

**Responsible role:** L1_support

**Instruction:**
E-stop RMS.

**Expected result:**
RMS is E-stopped and ready for AGV recovery actions.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*System state context associated with shut-down mode before restart or resume-related actions.*

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Nearby fault recovery screen context on page 90 associated with E-stop and AGV recovery flow.*


---

### Step 2 — Remove and re-add empty AGVs twice using Tote API Controls

**Responsible role:** L1_support

**Instruction:**
Using Tote API Controls in RMS, remove and re-add AGVs without totes twice.

**Expected result:**
The affected empty AGVs have been removed and re-added twice in RMS using Tote API Controls.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls showing Remove AGV and Recover AGV controls relevant to the remove and re-add actions.*

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Nearby page 90 recovery screen used as contextual support for AGV add/remove actions in RMS.*


**Stop or Escalate If:**

* The affected AGV is not empty and instead has a tote.
* The documented remove and re-add actions cannot be completed in Tote API Controls.
* Additional recovery actions seem necessary beyond the documented remove and re-add steps.

---

### Step 3 — Verify AGVs are in "szonestaging" if restart is needed

**Responsible role:** L1_support

**Instruction:**
If the system needs to be restarted, verify on the HMI that the AGVs are in the "szonestaging" state.

**Expected result:**
When a restart is needed, the AGV state is verified on the HMI as "szonestaging".

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*AGV status context on the nearby recovery screen and any indication of the "szonestaging" state.*


**Stop or Escalate If:**

* The system needs to be restarted and the AGVs cannot be verified as "szonestaging" on the HMI.
* The HMI does not show the AGVs in the "szonestaging" state.

---

### Step 4 — Press the E-stop again when ready to resume

**Responsible role:** L1_support

**Instruction:**
Press the E-stop again when ready to resume.

**Expected result:**
The documented pre-resume E-stop action has been completed.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*System state context associated with transitioning from stopped to resumed operation.*


**Stop or Escalate If:**

* You are not ready to resume RMS.
* Required prior recovery actions have not been completed.

---

### Step 5 — Resume RMS

**Responsible role:** L1_support

**Instruction:**
Resume RMS. See "Starting the System" on page 65.

**Expected result:**
RMS is resumed after the AGV recovery sequence.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*System state context relevant to resuming from shut-down or stopped mode.*


**Stop or Escalate If:**

* RMS cannot be resumed after completing the documented recovery steps.

---

## Success Criteria

* RMS was E-stopped before recovery actions.
* Affected empty AGVs were removed and re-added twice using Tote API Controls.
* If a restart was needed, AGVs were verified on the HMI as being in the "szonestaging" state.
* The E-stop was pressed again when ready to resume.
* RMS was resumed.

## Failure Conditions

* The affected AGV has a tote and does not match this procedure scope.
* The AGVs cannot be removed and re-added twice using Tote API Controls.
* The AGV state cannot be verified as "szonestaging" on the HMI when restart is needed.
* RMS cannot be resumed after the documented steps.

## Escalation Guidance

* Stop and escalate if AGV state cannot be verified as "szonestaging" on the HMI when a restart is needed.
* Stop and escalate if recovery appears to require actions beyond the documented remove and re-add steps.
* Use the source note that best practice is to shut down and restart to ensure everything is in sync as guidance for SME review or operational decision-making.

## Missing Details / Known Gaps

* The source does not provide exact button names or field-level navigation for the RMS E-stop and resume controls.
* The source does not identify specific AGV IDs, counts, or selection criteria for which empty AGVs to remove and re-add.
* The source does not provide a dedicated HMI screenshot explicitly showing the "szonestaging" value for this exact procedure; nearby visual support is context-linked and should be SME-reviewed for exact applicability.
* The source does not provide estimated completion time.
* The source does not explicitly state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_recover_empty_agvs_lost_tasks_after_rms_restart
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
