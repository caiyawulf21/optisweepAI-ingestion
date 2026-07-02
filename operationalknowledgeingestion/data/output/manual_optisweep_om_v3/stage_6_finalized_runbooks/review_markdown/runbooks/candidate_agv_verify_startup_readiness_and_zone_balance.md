# Verify AGV Startup Readiness and Correct AGV Zone Balance

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_agv_startup_readiness_and_correct_agv_zone_balance_v1` |
| Title | Verify AGV Startup Readiness and Correct AGV Zone Balance |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Confirm before startup that there are nine AGVs without totes in the system, distributed as five under the north rack and four under the south rack. If a zone is missing an AGV, move an AGV without a tote into the missing zone and add that AGV to RMS after the move.

## When To Use

Use before starting the AGV system to verify the required AGV-without-tote count and rack distribution, and when correcting a missing-AGV zone condition described by the source.

## Do Not Use For

* Do not use as a complete AGV movement method; the source does not provide safe-motion controls or relocation steps.
* Do not use as a complete RMS operating procedure; the source does not provide the RMS access path, fields, or confirmation indicators.
* Do not use this runbook to infer unsupported screen indicators from the shut-down mode image beyond the source-backed AGV startup context.

## Safety And Operational Notes

* This procedure is not support-safe based on the source packet because the source does not describe how to move an AGV safely.
* Do not invent or apply unsupported safe-motion controls, movement methods, or system constraints when relocating an AGV.
* Escalate if AGV relocation cannot be completed using approved local methods not documented in this source.

## Access Or Tools Needed

* Ability to verify AGV count and location under the north rack and south rack
* Access to move an AGV without a tote
* Access to RMS to add the moved AGV
* Optional reference to the "System in Shut-down Mode" screen

## Related Operational Context

* ctx_manual_agv_status_screen_v1
* ctx_manual_agv_szonestaging_state_reference_v1
* ctx_manual_hmi_system_shutdown_mode_screen_v1

## Procedure Steps

### Step 1 — Count AGVs without totes in the system

**Responsible role:** L2_support

**Instruction:**
Before starting the system, count the AGVs without totes in the system and verify that there are nine AGVs without totes total.

**Expected result:**
Nine AGVs without totes are present in the system before startup.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*Use only as a startup-context visual reference for the AGV system in shut-down mode; do not infer unsupported counts or indicators beyond the source-backed context.*


**Stop or Escalate If:**

* The total number of AGVs without totes is not nine.
* AGV count cannot be verified from available system information.

---

### Step 2 — Verify north-rack and south-rack AGV distribution

**Responsible role:** L2_support

**Instruction:**
Verify that the nine AGVs without totes are distributed as five under the north rack and four under the south rack.

**Expected result:**
AGV distribution matches the documented startup requirement.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*Use as a startup/shut-down mode visual reference only where the source supports AGV-related rack-area context.*


**Stop or Escalate If:**

* The north rack does not have five AGVs without totes.
* The south rack does not have four AGVs without totes.
* The expected zone distribution cannot be achieved or verified.

---

### Step 3 — Use the shut-down mode screen as an optional visual reference

**Responsible role:** L2_support

**Instruction:**
If using the associated shut-down mode screen as support, compare the visible AGV-related areas or indicators only to the extent supported by the source artifact and startup context.

**Expected result:**
The screen is used only as a contextual visual aid for the AGV startup readiness check.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*System in Shut-down Mode screen associated with AGV startup guidance.*


**Stop or Escalate If:**

* The screen does not provide enough supported detail to verify the AGV distribution.
* Verification would require inferring unsupported indicators or controls from the image.

---

### Step 4 — Move an AGV without a tote into the missing zone

**Responsible role:** L2_support

**Instruction:**
If a zone is missing an AGV, move an AGV without a tote into the zone that is missing an AGV.

**Expected result:**
The missing zone has an AGV without a tote positioned in it.

**Stop or Escalate If:**

* AGV relocation cannot be completed.
* Safe movement method details are required but not provided by the source.
* The source-expected AGV count or zone distribution cannot be achieved.

---

### Step 5 — Add the moved AGV to RMS

**Responsible role:** L2_support

**Instruction:**
After moving the AGV, add the moved AGV to the RMS.

**Expected result:**
The moved AGV has been added to RMS.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Optional nearby recovery visual showing an AGV-add workflow context; use only as supporting context because the startup source text does not provide RMS path, fields, or confirmation indicators.*

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*Optional AGV-related controls reference; do not treat as direct evidence for the specific RMS add path unless locally validated.*


**Stop or Escalate If:**

* RMS addition cannot be completed.
* The RMS access path, fields, or confirmation indicators are needed but not provided by the source.

---

## Success Criteria

* Before startup, there are nine AGVs without totes in the system.
* The AGV distribution is five under the north rack and four under the south rack.
* If an AGV was moved to correct a missing zone, that AGV has been added to RMS.

## Failure Conditions

* The total AGV count without totes is not nine.
* The north/south rack distribution does not match five/four.
* A missing-AGV zone cannot be corrected.
* The moved AGV cannot be added to RMS.
* Required movement or RMS details are needed but not provided by the source.

## Escalation Guidance

* Escalate if AGV relocation or RMS addition cannot be completed.
* Escalate if the source-expected AGV count or zone distribution cannot be achieved.
* Escalate when safe-motion controls or movement method details are required, because they are not provided by this source.
* Escalate when RMS access path, fields, or confirmation indicators are required, because they are not provided by this source.

## Missing Details / Known Gaps

* The source does not provide the RMS access path, fields, or confirmation indicators for adding the moved AGV.
* The source does not provide safe-motion controls or movement method details for relocating an AGV.
* The source does not specify whether production must be stopped beyond the pre-start context.
* The source does not provide a time estimate for completing this procedure.
* The source text says "started without nine totes," but the surrounding startup requirement is framed as AGVs without totes; SME review should confirm intended wording.

## Source Lineage

- Candidate IDs: candidate_agv_verify_startup_readiness_and_zone_balance
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
