# Recover an AGV Fault During Exchange

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_an_agv_fault_during_exchange_v1` |
| Title | Recover an AGV Fault During Exchange |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Recover the exchange area after an AGV faults while lifted and leaving the RMS by stopping RMS, removing the faulted AGV through AGV API Controls, conditionally removing the following AGV if it does not back fill, introducing a new tote at the affected location, and placing an empty AGV in the zone.

## When To Use

Use when an AGV faults during exchange while lifted and leaving the RMS, and the exchange area must be restored by removing the affected AGV, restoring tote presence at the location, and placing an empty AGV in the zone.

## Safety And Operational Notes

* This procedure is not marked support-safe in the source candidate.
* The procedure involves E-stop use and physical intervention in the exchange location or zone.
* Stop and escalate if the faulted AGV cannot be removed from RMS.
* Stop and escalate if the AGV behind the faulted AGV does not back fill and cannot be safely removed.

## Access Or Tools Needed

* Access to RMS E-stop control
* Access to AGV API Controls
* Physical access to the exchange location or zone
* Replacement tote
* Empty AGV

## Related Operational Context

* ctx_manual_agv_api_controls_reference_v1
* ctx_manual_rms_estop_resume_reference_v1

## Procedure Steps

### Step 1 — E-stop RMS

**Responsible role:** L2_support

**Instruction:**
E-stop RMS before attempting to remove the faulted AGV or perform exchange-area recovery actions.

**Expected result:**
RMS is E-stopped and recovery actions can proceed under the stopped condition referenced by the source.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*System stop or shut-down state context relevant to placing RMS into a stopped condition.*

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Fault recovery screen context associated with AGV fault recovery procedures that begin with E-stop RMS.*


**Stop or Escalate If:**

* RMS cannot be E-stopped.
* The system does not enter a clear stopped state for recovery.

---

### Step 2 — Remove the faulted lifted AGV from RMS

**Responsible role:** L2_support

**Instruction:**
Remove the lifted AGV that faulted while leaving from the RMS using the AGV API Controls.

**Expected result:**
The faulted lifted AGV is removed from RMS.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls screen, specifically the Remove AGV function.*

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Faulted AGV recovery screen context associated with removing a faulted AGV from RMS.*


**Stop or Escalate If:**

* The lifted faulted AGV cannot be removed from RMS.

---

### Step 3 — Remove the following AGV if it does not back fill

**Responsible role:** L2_support

**Instruction:**
If the AGV behind the faulted AGV does not back fill, remove that AGV also.

**Expected result:**
If needed, the following AGV is also removed so the exchange area can be restored.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls screen used if the following AGV must also be removed.*


**Stop or Escalate If:**

* The AGV behind the faulted AGV does not back fill and cannot be safely removed.

---

### Step 4 — Introduce a new tote at the affected location

**Responsible role:** L2_support

**Instruction:**
Introduce a new tote at that location.

**Expected result:**
A new tote is introduced at the affected location.

**Screens / Images:**

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*Add Tote screen context for scanning or confirming tote introduction back into the system.*

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station tote-handling context relevant to tote handling and return to the system.*


**Stop or Escalate If:**

* A replacement tote cannot be introduced at the affected location.

---

### Step 5 — Place an empty AGV in the zone

**Responsible role:** L2_support

**Instruction:**
Place an empty AGV in that zone.

**Expected result:**
An empty AGV is placed in the affected zone.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Screen associated with adding an AGV to a zone during AGV recovery scenarios.*

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls context if AGV addition or removal actions are needed as part of placing the AGV in the zone.*


**Stop or Escalate If:**

* An empty AGV cannot be placed in the zone.

---

## Success Criteria

* The faulted AGV is removed from the exchange area.
* If required, the AGV behind the faulted AGV is also removed when it does not back fill.
* A new tote is introduced at the affected location.
* An empty AGV is placed in the affected zone.

## Failure Conditions

* The lifted faulted AGV cannot be removed from RMS.
* The AGV behind the faulted AGV does not back fill and cannot be safely removed.
* The source does not provide detailed confirmation checks after the tote and empty AGV are introduced.

## Escalation Guidance

* Escalate if the lifted faulted AGV cannot be removed from RMS.
* Escalate if the AGV behind it does not back fill and cannot be safely removed.
* Escalate for SME review if confirmation of tote introduction or empty AGV placement is required beyond what is stated in the source.

## Missing Details / Known Gaps

* The source packet does not provide explicit confirmation checks after introducing the new tote.
* The source packet does not provide explicit confirmation checks after placing the empty AGV in the zone.
* The source packet does not provide a documented resume step for this specific procedure excerpt.
* The source packet does not provide an estimated completion time.
* The source packet does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_l2_recover_agv_fault_during_exchange
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
