# Recover From AGV Fault During Exchange

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_from_agv_fault_during_exchange_v1` |
| Title | Recover From AGV Fault During Exchange |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Restore the exchange location after a lifted AGV faults while leaving the RMS by stopping the RMS, removing the affected AGV, checking whether the trailing AGV back fills, removing the trailing AGV if it does not back fill, and restoring the location with a new tote and an empty AGV in the zone.

## When To Use

Use when an AGV faults during exchange and the AGV is lifted and faulted while leaving the RMS, as described in manual section 5.8.2.5.

## Do Not Use For

* Do not use for AGV bump fault recovery scenarios covered elsewhere in the manual.
* Do not use for faulted AGV with tote recovery scenarios covered elsewhere in the manual.
* Do not use when detailed tote introduction or empty AGV placement instructions are required, because this source does not provide those steps.

## Safety And Operational Notes

* The procedure begins with E-stop of the RMS.
* This is not marked support-safe in the candidate and involves system-level AGV removal from RMS.
* The source does not provide detailed recovery actions if AGV removal cannot be completed.

## Access Or Tools Needed

* Access to the RMS E-stop control
* Access to AGV API Controls referenced on page 24
* Ability to identify the faulted lifted AGV and the trailing AGV
* A new tote
* An empty AGV
* Access to the affected zone/location

## Related Operational Context

* ctx_manual_agv_fault_during_exchange_v1
* ctx_manual_rms_estop_fault_recovery_v1
* ctx_manual_agv_api_controls_reference_v1

## Procedure Steps

### Step 1 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
E-stop the RMS.

**Expected result:**
The RMS is stopped and the recovery can proceed under the documented fault-recovery condition.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*System shut-down mode indication after E-stop.*


**Stop or Escalate If:**

* The RMS cannot be E-stopped.
* System stop state cannot be confirmed.

---

### Step 2 — Identify the faulted lifted AGV

**Responsible role:** L2_support

**Instruction:**
Identify the AGV that is lifted and has faulted while leaving the RMS during the exchange.

**Expected result:**
The specific lifted AGV that faulted while leaving the RMS is identified.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Faulted AGV visual context to help recognize the affected AGV condition.*


**Stop or Escalate If:**

* The faulted lifted AGV cannot be identified.
* Multiple AGVs appear affected and the source does not provide disambiguation steps.

---

### Step 3 — Remove the faulted AGV from RMS

**Responsible role:** L2_support

**Instruction:**
Remove the identified lifted AGV that faulted while leaving from the RMS using AGV API Controls referenced on page 24.

**Expected result:**
The faulted AGV is removed from the RMS.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls interface, especially Remove AGV.*


**Stop or Escalate If:**

* AGV API Controls are not accessible.
* The AGV cannot be removed through AGV API Controls.
* Removal outcome cannot be confirmed.

---

### Step 4 — Check whether the trailing AGV back fills

**Responsible role:** L2_support

**Instruction:**
Check whether the AGV behind the faulted AGV back fills.

**Expected result:**
A determination is made whether the trailing AGV back fills.

**Stop or Escalate If:**

* Back-fill status cannot be determined.
* Unexpected AGV behavior occurs and the source provides no further guidance.

---

### Step 5 — Remove the trailing AGV if it does not back fill

**Responsible role:** L2_support

**Instruction:**
If the AGV behind the faulted AGV does not back fill, remove that AGV as well using AGV API Controls referenced on page 24.

**Expected result:**
Any trailing AGV that does not back fill is removed from the RMS.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls interface used to remove the trailing AGV.*


**Stop or Escalate If:**

* The trailing AGV does not back fill and cannot be removed.
* AGV API Controls are unavailable.
* The source does not provide next actions after failed removal.

---

### Step 6 — Introduce a new tote at the affected location

**Responsible role:** L2_support

**Instruction:**
Introduce a new tote at that location.

**Expected result:**
A new tote is introduced at the affected location.

**Screens / Images:**

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*Add Tote screen context for tote introduction, if used by local process.*


**Stop or Escalate If:**

* A new tote is not available.
* The source does not provide the detailed tote introduction method needed for execution.

---

### Step 7 — Place an empty AGV in the affected zone

**Responsible role:** L2_support

**Instruction:**
Place an empty AGV in that zone.

**Expected result:**
An empty AGV is placed in the affected zone.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Related add-AGV-to-zone screen for contextual guidance on restoring AGV presence in a zone.*


**Stop or Escalate If:**

* An empty AGV is not available.
* The source does not provide the detailed method for placing the empty AGV in the zone.

---

## Success Criteria

* The faulted lifted AGV is removed from the RMS.
* If the trailing AGV does not back fill, it is also removed from the RMS.
* A new tote is introduced at the affected location.
* An empty AGV is placed in the affected zone.

## Failure Conditions

* RMS cannot be E-stopped.
* The faulted AGV cannot be identified.
* The faulted AGV cannot be removed through AGV API Controls.
* The trailing AGV does not back fill and cannot be removed.
* The source does not provide enough detail to complete tote introduction or empty AGV placement.

## Escalation Guidance

* Escalate if AGV removal through AGV API Controls cannot be completed.
* Escalate if the faulted AGV or trailing AGV cannot be confidently identified.
* Escalate if detailed instructions are needed for introducing the new tote or placing the empty AGV, because the source does not provide them.
* Use a higher-support role if local policy requires additional authority for system-level AGV removal.

## Missing Details / Known Gaps

* The source does not provide detailed instructions for how to identify the faulted AGV in the interface.
* The source does not provide step-by-step AGV API Controls interaction details for removal.
* The source does not provide detailed instructions for how to introduce the new tote at the affected location.
* The source does not provide detailed instructions for how to place the empty AGV in the affected zone.
* The source does not describe what to do if AGV removal through AGV API Controls cannot be completed.
* The source does not provide explicit completion confirmations, timing, or validation checks after restoration.

## Source Lineage

- Candidate IDs: candidate_recover_agv_fault_during_exchange
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
