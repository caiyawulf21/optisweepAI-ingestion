# Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_from_agv_fault_during_exchange_recovery_v1` |
| Title | Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV) |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | None |
| Access Surface | `rms_ui`, `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Restore exchange flow after an AGV faults while leaving by stopping RMS, removing the faulted AGV from the RMS, optionally removing the trailing AGV if it does not backfill, then introducing a new tote and placing an empty AGV in the affected zone.

## When To Use

Use when an AGV faults during exchange while leaving and you need to restore exchange flow by removing the faulted AGV from RMS, handling backfill behavior, and reintroducing the correct tote + empty-AGV state in the affected zone.

## Safety And Operational Notes

* Perform an RMS E-stop as the first recovery action for this fault scenario.

## Access Or Tools Needed

* RMS / fleet status UI (rms_ui)
* AGV API Controls referenced by the manual (accessed via RMS / fleet status UI)

## Related Operational Context

* ctx_manual_agv_fault_during_exchange_v1

## Visual References

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/d87070d22301b81d.jpeg)

*HMI screenshot showing the faulted AGV with tote state (used as visual context for the faulted condition during exchange recovery).*

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/ec83d895fff08cd8.jpeg)

*RMS screen for adding an AGV to a zone when no empty AGV is present (visual support for re-establishing empty AGV state in the affected zone).*

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*RMS screen showing an AGV fault example (visual context for RMS fault screens; not specific to this exact exchange-fault step).*

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*AGV API Controls screen showing controls such as Remove AGV / Recover AGV / Pause All AGVs / Resume All AGVs (used for the AGV removal action referenced by the recovery procedure).*

## Procedure Steps

### Step 1 — E-stop RMS

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), perform an E-stop of the RMS.

**Expected result:**
RMS is in an E-stopped state (fleet movement is stopped) on the RMS / fleet status UI.

**Stop or Escalate If:**

* RMS does not stop as expected (movement continues) — stop recovery actions and escalate.

---

### Step 2 — Remove the faulted AGV that is lifted and faulted out while leaving

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), identify the AGV that is lifted and has faulted out while leaving, then remove that AGV from the RMS using the AGV API Controls flow referenced by the manual.

**Expected result:**
The faulted AGV is removed from the RMS (it no longer appears as an active AGV in the RMS fleet context for the affected zone).

**Stop or Escalate If:**

* If the faulted AGV cannot be removed from RMS using the AGV API Controls flow — escalate.

---

### Step 3 — Check backfill; remove trailing AGV if it does not backfill

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), check whether the AGV behind the faulted AGV backfills into the expected position. If it does not backfill, remove that trailing AGV as well using the same AGV API Controls flow referenced by the manual.

**Expected result:**
Either (a) the AGV behind backfills into the expected position, or (b) the trailing AGV is removed from RMS when it does not backfill.

**Stop or Escalate If:**

* Trailing AGV does not backfill and cannot be removed/cleared as described — escalate.

---

### Step 4 — Introduce new tote and place an empty AGV in the affected zone

**Responsible role:** L2_support

**Instruction:**
Introduce a new tote at the faulted location and place an empty AGV in that zone using the RMS UI actions referenced by the manual.

**Expected result:**
A newly introduced tote is present at the affected location, and an empty AGV is placed in that zone so exchange can proceed.

**Stop or Escalate If:**

* New tote/empty AGV cannot be introduced into the correct zone — escalate.

---

## Success Criteria

* Faulted AGV is removed from RMS.
* If the AGV behind did not backfill, the trailing AGV is also removed.
* Affected exchange location has a newly introduced tote and an empty AGV placed in the correct zone so exchange can proceed.

## Failure Conditions

* Trailing AGV does not backfill and cannot be removed/cleared as described.
* New tote and/or empty AGV cannot be introduced into the correct zone.

## Escalation Guidance

* Escalate if the trailing AGV does not backfill and cannot be removed/cleared as described, or if the new tote/empty AGV cannot be introduced into the correct zone.

## Missing Details / Known Gaps

* The manual section provides the recovery sequence but does not provide explicit RMS UI navigation/field labels for the RMS E-stop control and the specific RMS UI controls used to identify the faulted AGV and confirm removal.
* The manual section does not specify the exact RMS UI workflow for introducing a new tote and placing an empty AGV into the correct zone (only the high-level actions are stated).

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_agv_fault_during_exchange_recovery
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
