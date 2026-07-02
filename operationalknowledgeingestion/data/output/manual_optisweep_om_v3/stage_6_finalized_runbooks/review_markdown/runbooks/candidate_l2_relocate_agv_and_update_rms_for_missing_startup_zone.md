# Relocate An AGV Without A Tote To The Missing Zone And Add It To RMS

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_relocate_an_agv_without_a_tote_to_the_missing_zone_and_add_it_to_rms_v1` |
| Title | Relocate An AGV Without A Tote To The Missing Zone And Add It To RMS |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Restore the documented AGV distribution needed for start-up by identifying a zone missing an AGV, moving an AGV without a tote into that zone, and adding the moved AGV to RMS. The source states the required startup distribution is nine AGVs without totes in the system: five under the north rack and four under the south rack.

## When To Use

Use when the system has been started or is being prepared for start-up and the documented AGV-without-tote distribution is not present, specifically when a zone is missing an AGV and an AGV without a tote must be relocated into that zone and then added to RMS.

## Do Not Use For

* Do not use for AGV bump fault recovery.
* Do not use for faulted AGV with tote recovery.
* Do not use when physical AGV movement instructions or site-specific RMS entry steps are required but not available from this source.

## Safety And Operational Notes

* The source does not describe the physical movement method for the AGV; use site-specific safe handling instructions.
* Do not invent RMS screens, commands, or confirmation indicators that are not provided in the source.
* The source wording says 'started without nine totes' while the surrounding text discusses AGVs without totes; this inconsistency should be reviewed before operational use.

## Access Or Tools Needed

* Access to identify AGV placement by zone
* Means to move an AGV without a tote
* Access to RMS to add the AGV after relocation

## Related Operational Context

* ctx_manual_agv_startup_vehicle_distribution_v1
* ctx_manual_agv_api_controls_reference_v1

## Procedure Steps

### Step 1 — Identify the missing AGV zone against startup distribution

**Responsible role:** L2_support

**Instruction:**
Check AGV placement by zone against the documented startup distribution. Confirm whether the system has fewer than the required AGVs without totes in the expected locations and identify the zone that is missing an AGV.

**Expected result:**
A specific zone missing an AGV is identified relative to the documented startup distribution.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*Startup-related system context associated with the requirement for nine AGVs without totes and the AGV distribution expectation.*


**Stop or Escalate If:**

* You cannot determine AGV placement by zone from available system views or local process knowledge.
* The startup distribution cannot be verified from the available source-supported information.

---

### Step 2 — Select an AGV without a tote for relocation

**Responsible role:** L2_support

**Instruction:**
Select an AGV without a tote to be moved into the zone that is missing an AGV.

**Expected result:**
An AGV without a tote is identified and ready for relocation.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*Use startup-related AGV distribution context to identify an AGV without a tote.*


**Stop or Escalate If:**

* You cannot confirm that the selected AGV is without a tote.
* No suitable AGV without a tote is available for relocation.

---

### Step 3 — Move the AGV into the missing zone

**Responsible role:** L2_support

**Instruction:**
Move the selected AGV without a tote into the zone that is missing an AGV.

**Expected result:**
The missing zone now has the relocated AGV without a tote.

**Stop or Escalate If:**

* The source does not provide the physical movement method and site-specific instructions are required.
* The AGV cannot be safely or correctly moved into the missing zone.

---

### Step 4 — Add the moved AGV to RMS

**Responsible role:** L2_support

**Instruction:**
After moving the AGV, add the moved AGV to RMS using the available AGV API Controls or site-specific RMS procedure.

**Expected result:**
The moved AGV is added to RMS after relocation.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls interface referenced for AGV removal and insertion actions in RMS.*

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Nearby recovery screen showing AGV add-to-zone workflow context; use only as visual support, not as a substitute for exact instructions unless locally validated.*


**Stop or Escalate If:**

* The source does not provide exact RMS navigation or confirmation steps needed at the site.
* You cannot determine how to add the AGV to RMS from the available source-supported interface references.

---

## Success Criteria

* The previously missing zone has an AGV without a tote.
* The relocated AGV has been added to RMS.
* AGV distribution matches the documented startup requirement or the identified missing-zone condition has been corrected.

## Failure Conditions

* A zone remains missing an AGV after relocation attempt.
* No AGV without a tote is available for relocation.
* The AGV cannot be physically moved using source-supported instructions.
* The moved AGV is not added to RMS.
* Required RMS interface details are not available from the source.

## Escalation Guidance

* Escalate for site-specific instructions if physical AGV movement details are required.
* Escalate for site-specific RMS instructions if the exact add-AGV workflow is needed.
* Escalate for SME review of the source wording inconsistency referring to 'started without nine totes' versus AGVs without totes.

## Missing Details / Known Gaps

* The source does not describe how to physically move the AGV.
* The source does not provide exact RMS navigation steps for adding the AGV.
* The source does not provide explicit confirmation indicators for successful RMS add-back in this specific procedure.
* The source does not specify whether production must be stopped before performing this recovery.
* The source does not specify whether LOTO is required.
* The source section text payload is empty in the packet, so grounding relies on supplied source references, artifacts, and context records.

## Source Lineage

- Candidate IDs: candidate_l2_relocate_agv_and_update_rms_for_missing_startup_zone
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
