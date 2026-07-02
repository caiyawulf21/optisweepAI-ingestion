# Verify Trailing AGV Back Fill During Exchange Fault Recovery

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_trailing_agv_back_fill_during_exchange_fault_recovery_v1` |
| Title | Verify Trailing AGV Back Fill During Exchange Fault Recovery |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-specific diagnostic procedure during the manual's AGV fault during exchange recovery scenario to verify whether the AGV behind the faulted lifted AGV has back filled, and to document whether the manual's condition for also removing the trailing AGV applies.

## When To Use

Use when working from the manual's AGV fault during exchange recovery guidance on page 91 and you need to determine whether the AGV behind the lifted AGV that faulted while leaving the RMS has back filled, because the manual states that if it does not back fill, that AGV is also removed.

## Do Not Use For

* Do not use to define a precise back fill position or visual indicator, because the source does not provide one.
* Do not use as a complete AGV removal or replacement procedure; this runbook only finalizes the source-specific verification and documentation of trailing AGV back fill behavior.
* Do not invent additional criteria for back fill beyond the source wording.

## Safety And Operational Notes

* The candidate references placing the RMS in E-stop state before performing the check.
* Use only the source-supported condition for the trailing AGV decision: if the AGV behind the faulted AGV does not back fill, also remove that AGV.
* Escalate unresolved ambiguity because the source does not define the exact expected back fill position or visual indicator.

## Access Or Tools Needed

* Access to the RMS area or system view needed to identify the trailing AGV
* Access to the documented fault-recovery section on page 91

## Related Operational Context

* ctx_manual_agv_fault_during_exchange_v1
* ctx_manual_rms_estop_fault_recovery_v1
* ctx_manual_agv_api_controls_reference_v1

## Procedure Steps

### Step 1 — Place the RMS in E-stop state

**Responsible role:** L1_support

**Instruction:**
Place the RMS in E-stop state as referenced in the fault-recovery section before checking the AGV positions involved in the exchange fault scenario.

**Expected result:**
The RMS is in the E-stop state used for AGV-related fault recovery.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*Use as a general visual reference for a stopped or shut-down system state context.*

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Use as nearby AGV fault recovery visual context on page 91.*


**Stop or Escalate If:**

* You cannot confirm the RMS is in the referenced E-stop state.
* The source context for the exchange fault scenario is unclear.

---

### Step 2 — Identify the faulted lifted AGV

**Responsible role:** L1_support

**Instruction:**
Identify the lifted AGV that faulted while leaving the RMS during the exchange scenario described by the manual.

**Expected result:**
The specific faulted lifted AGV is identified.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Use as a nearby AGV fault visual reference while identifying the faulted AGV.*


**Stop or Escalate If:**

* You cannot distinguish the faulted lifted AGV from other AGVs.
* The observed condition does not clearly match the manual's exchange fault scenario.

---

### Step 3 — Locate the AGV behind the faulted AGV

**Responsible role:** L1_support

**Instruction:**
Locate the AGV behind the faulted AGV in the exchange sequence.

**Expected result:**
The trailing AGV behind the faulted AGV is identified for observation.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Use as nearby AGV fault recovery context while locating the AGV behind the faulted AGV.*


**Stop or Escalate If:**

* The trailing AGV cannot be identified from the RMS area or system view.
* AGV ordering or position is ambiguous.

---

### Step 4 — Observe whether the trailing AGV back filled

**Responsible role:** L1_support

**Instruction:**
Observe whether the AGV behind the faulted AGV has back filled into the expected position based only on the source wording. Do not apply any additional criteria not stated by the source.

**Expected result:**
A determination is made whether the trailing AGV did or did not back fill.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Use as nearby AGV fault recovery visual context while observing AGV position.*


**Stop or Escalate If:**

* The exact expected back fill position or visual indicator is unclear.
* You would need to invent criteria beyond the source wording to decide whether back fill occurred.

---

### Step 5 — Record the back fill result

**Responsible role:** L1_support

**Instruction:**
Record whether the trailing AGV did or did not back fill.

**Expected result:**
The recovery record reflects whether the trailing AGV back filled.

**Stop or Escalate If:**

* The observer cannot confidently determine whether back fill occurred from the source-supported evidence.

---

### Step 6 — Document the source-backed removal condition

**Responsible role:** L1_support

**Instruction:**
If documenting the source-backed outcome, note that the manual states the trailing AGV is also removed when it does not back fill.

**Expected result:**
The record includes the manual's explicit condition for also removing the trailing AGV when applicable.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*Use as the referenced AGV removal interface context if the documented outcome indicates the trailing AGV must also be removed.*


**Stop or Escalate If:**

* The back fill result is ambiguous.
* The operator is being asked to define removal criteria beyond the manual's explicit statement.

---

## Success Criteria

* The faulted lifted AGV and the AGV behind it are identified.
* A source-grounded determination is made whether the trailing AGV back filled.
* The recovery record states whether the trailing AGV did or did not back fill.
* If the trailing AGV did not back fill, the documentation notes the manual's instruction that the AGV is also removed.

## Failure Conditions

* The exact expected back fill position or visual indicator cannot be determined from the source.
* The faulted or trailing AGV cannot be confidently identified.
* The observer would need to invent additional criteria to decide whether back fill occurred.
* The result cannot be documented clearly from source-supported evidence.

## Escalation Guidance

* Escalate if the exact expected back fill position or visual indicator is ambiguous, because the source does not define it.
* Escalate if the AGV behind the faulted AGV cannot be confidently identified.
* Escalate rather than inventing additional criteria for back fill beyond the source wording.

## Missing Details / Known Gaps

* The source does not define the exact expected back fill position.
* The source does not define a specific visual indicator or HMI field to confirm back fill.
* The source does not provide a time expectation for how long to wait before deciding the trailing AGV did not back fill.
* The source does not specify a formal recording location or template for documenting the result.
* The source does not explicitly state whether production stop is required beyond the referenced E-stop condition.
* The source does not specify whether any supporting role must review the determination.

## Source Lineage

- Candidate IDs: candidate_check_trailing_agv_backfill_during_exchange_fault_recovery
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
