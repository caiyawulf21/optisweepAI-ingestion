# Start Up the AGV System

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_start_up_the_agv_system_v1` |
| Title | Start Up the AGV System |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Bring the AGV system from shut-down mode into operation by verifying AGV readiness, confirming shut-down mode, starting the system at the documented time, resetting metrics, starting the system, completing close out (Bag Out), and confirming the system returns to Running.

## When To Use

Use this procedure when the AGV system is in shut-down mode and needs to be brought into operation before a sort. The source notes the system should be started 15 minutes before the sort starts.

## Do Not Use For

* Do not use this runbook as a detailed AGV redistribution or RMS add-back procedure; the source notes the AGV readiness condition but does not provide the corrective substeps here.
* Do not use this runbook for system shut down; shutdown appears as a separate operation in the source material.
* Do not use this runbook when detailed HMI button names, screen paths, or close out substeps are required, because those details are not provided in this source section.

## Safety And Operational Notes

* Use only the documented startup sequence from this source.
* Do not assume startup is complete if the required AGV readiness condition is not met.
* The source does not provide detailed corrective actions for missing AGV readiness, detailed HMI navigation, or close out substeps; escalate if those details are needed.

## Access Or Tools Needed

* Access to the AGV system controls
* Ability to verify AGV count and location under the north rack and south rack
* System screen reference for "System in Shut-down Mode"
* Access to metrics reset and system start functions

## Related Operational Context

* ctx_manual_agv_status_screen_v1
* ctx_manual_agv_startup_timing_note_v1
* ctx_manual_hmi_system_shutdown_mode_screen_v1

## Procedure Steps

### Step 1 — Verify AGV readiness count and location

**Responsible role:** operator

**Instruction:**
Before starting the system, verify there are nine AGVs without totes in the system: five under the north rack and four under the south rack.

**Expected result:**
The required number of tote-free AGVs is confirmed in the documented rack distribution.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*Use the startup section screen reference associated with AGV startup to orient to the documented system state before startup.*


**Stop or Escalate If:**

* Stop if the system does not have nine AGVs without totes.
* Stop if the AGV distribution is not five under the north rack and four under the south rack.
* Escalate if corrective actions are needed to restore the required AGV readiness condition because this source section does not provide the full corrective substeps.

---

### Step 2 — Confirm the system is in shut-down mode

**Responsible role:** operator

**Instruction:**
Use the documented system screen reference titled "System in Shut-down Mode" to confirm the system is in shut-down mode before startup.

**Expected result:**
The operator confirms the system is in the documented shut-down mode state.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*The screen titled "System in Shut-down Mode" and any visible status or start-related indicators shown in the source artifact.*


**Stop or Escalate If:**

* Stop if the system cannot be confirmed to be in shut-down mode.
* Escalate if the displayed system state does not match the documented shut-down mode reference.

---

### Step 3 — Start the system 15 minutes before sort

**Responsible role:** operator

**Instruction:**
Start the system 15 minutes before the sort starts.

**Expected result:**
Startup is initiated at the documented time relative to the sort start.

**Stop or Escalate If:**

* Escalate if the system cannot be started within the documented startup timing window.

---

### Step 4 — Reset the metrics

**Responsible role:** operator

**Instruction:**
Reset the metrics before starting the system.

**Expected result:**
Metrics are reset as part of the startup sequence.

**Screens / Images:**

![artifact_fig_4_9_system_api_controls](assets/artifact_fig_4_9_system_api_controls.jpeg)

*The System API Controls screen showing the Reset Metrics control.*


**Stop or Escalate If:**

* Escalate if the metrics reset function is unavailable.
* Escalate if the operator cannot confirm the metrics reset action on the available system controls.

---

### Step 5 — Start the system

**Responsible role:** operator

**Instruction:**
Start the system.

**Expected result:**
The system startup action is initiated from the system controls.

**Screens / Images:**

![artifact_fig_4_9_system_api_controls](assets/artifact_fig_4_9_system_api_controls.jpeg)

*The System API Controls screen showing the System Startup control.*


**Stop or Escalate If:**

* Escalate if the system startup control is unavailable.
* Escalate if the system does not respond to the startup action.

---

### Step 6 — Complete close out (Bag Out)

**Responsible role:** operator

**Instruction:**
Complete close out (Bag Out).

**Expected result:**
Close out (Bag Out) is completed as part of the startup sequence.

**Screens / Images:**

![artifact_fig_4_9_system_api_controls](assets/artifact_fig_4_9_system_api_controls.jpeg)

*The System API Controls screen showing the System Close Out control.*


**Stop or Escalate If:**

* Escalate if close out (Bag Out) cannot be completed.
* Escalate if the operator needs detailed close out substeps not provided in this source.

---

### Step 7 — Verify the system returns to Running

**Responsible role:** operator

**Instruction:**
After close out (Bag Out) is completed, verify the system goes back to "Running".

**Expected result:**
The system state returns to Running.

**Screens / Images:**

![artifact_fig_4_9_system_api_controls](assets/artifact_fig_4_9_system_api_controls.jpeg)

*The System section or state display used to confirm the system is back to Running.*


**Stop or Escalate If:**

* Escalate if the system does not go back to "Running" after close out (Bag Out).

---

## Success Criteria

* The AGV readiness condition is verified before startup.
* The system is confirmed to be in shut-down mode before startup.
* The startup is performed 15 minutes before the sort starts.
* Metrics are reset.
* The system is started.
* Close out (Bag Out) is completed.
* The system returns to "Running" after close out (Bag Out).

## Failure Conditions

* The required AGV readiness condition is not met.
* The system cannot be confirmed to be in shut-down mode before startup.
* The startup timing note cannot be met.
* Metrics cannot be reset.
* The system does not start.
* Close out (Bag Out) cannot be completed.
* The system does not go back to "Running" after close out (Bag Out).

## Escalation Guidance

* Escalate if the required AGV readiness condition is not met and corrective actions are needed.
* Escalate if the system state does not match the documented shut-down mode reference.
* Escalate if metrics reset, system startup, or close out controls are unavailable.
* Escalate if the system does not return to "Running" after close out (Bag Out).
* Escalate when detailed HMI button names, screen paths, or close out substeps are required, because this source does not provide them.

## Missing Details / Known Gaps

* The source does not provide detailed HMI button names or navigation steps for reset metrics, system startup, or close out.
* The source does not provide detailed close out (Bag Out) substeps.
* The source does not provide a detailed corrective procedure in this section for restoring the required AGV readiness condition if the count or distribution is wrong.
* The source does not provide an estimated completion time for the procedure.

## Source Lineage

- Candidate IDs: candidate_agv_system_start_up_sequence
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
