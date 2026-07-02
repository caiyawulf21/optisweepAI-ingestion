# Rescan a Tote to Reassociate It With Its Designated Location

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_rescan_a_tote_to_reassociate_it_with_its_designated_location_v1` |
| Title | Rescan a Tote to Reassociate It With Its Designated Location |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use rescanning to properly reassociate a tote with its designated location when a tote removed from the sorter stand was not returned with the same Tote ID to its original position. The source explicitly states rescanning is required in this condition, but the full rescanning workflow is only partially supported by the supplied source evidence.

## When To Use

Use when a tote has been manually removed from the sorter stand and was not returned with the same Tote ID to its original position, causing the tote-to-location association to be disrupted and requiring rescanning to restore the designated location association.

## Do Not Use For

* Do not use as a complete standalone rescanning procedure when the operator does not have access to the documented scanner-based tote handling process, because the full rescan steps are not provided in this source section.
* Do not use for unrelated hospital-station barcode exception workflows, AGV recovery workflows, or other HMI fault conditions not tied to sorter tote-position reassociation.

## Safety And Operational Notes

* The supplied source evidence does not identify lockout/tagout requirements for this activity.
* Only use the documented scanner-based process available to the user; the full rescanning sequence is not provided in this source section.

## Access Or Tools Needed

* Zebra scanner
* Access to the tote being reassociated
* Documented scanner-based tote handling process

## Related Operational Context

* ctx_manual_sorter_scanner_operation_overview_v1
* ctx_manual_sorter_tote_id_position_association_v1
* ctx_manual_acb_api_screen_reference_v1

## Procedure Steps

### Step 1 — Identify the tote-position association mismatch

**Responsible role:** L1_support

**Instruction:**
Determine whether a tote manually removed from the sorter stand was not returned with the same Tote ID to its original position. Treat this as a tote-to-location association issue requiring rescanning.

**Expected result:**
The operator confirms that the tote association has been disrupted and that rescanning is required.

**Screens / Images:**

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*Sorter scanner operation context showing Add Tote workflow and the note that rescanning is required if the same Tote ID is not returned to its original position.*


**Stop or Escalate If:**

* The operator cannot determine whether the tote returned is the same Tote ID.
* The original sorter position cannot be identified from available information.

---

### Step 2 — Rescan the tote using the documented scanner process

**Responsible role:** L1_support

**Instruction:**
Use the documented scanner-based process available to the user to rescan the tote so it can be properly associated with its designated location. Where the available scanner workflow includes sorter destination or tote/position barcode pairing, follow that documented process exactly.

**Expected result:**
The tote is rescanned through the documented process and the system accepts the reassociation attempt.

**Screens / Images:**

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*Sorter scanner operation image tied to Add Tote, tote barcode scan, tote ID verification, and Confirm & Execute.*

![artifact_page_94_image_2](assets/artifact_page_94_image_2.jpeg)

*Tote Initialization Procedure image showing Sorter Destinations selection and scanning of sorter stand position barcode and tote barcode.*


**Stop or Escalate If:**

* The documented rescanning procedure available to the user is incomplete or unavailable.
* The scanner indicates an unsuccessful scan or pairing and repeated rescanning does not resolve it.
* The tote cannot be properly associated using the documented scanner process.

---

### Step 3 — Verify the tote is associated to the intended location

**Responsible role:** L1_support

**Instruction:**
Verify through the documented tote identification process that the tote is associated to the intended location after rescanning. If the available workflow includes tote ID display verification or successful scan confirmation, use those indicators.

**Expected result:**
The tote is confirmed to be associated with the intended designated location.

**Screens / Images:**

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*Displayed tote ID verification on the Add Tote workflow before Confirm & Execute.*

![artifact_page_94_image_2](assets/artifact_page_94_image_2.jpeg)

*Successful scan indication for tote/position pairing.*


**Stop or Escalate If:**

* The tote cannot be confirmed as associated with the intended location.
* The tote ID does not display correctly in the documented workflow.
* Repeated rescanning does not produce a successful association.

---

## Success Criteria

* The tote is properly reassociated with its designated location.
* The documented scanner workflow completes successfully.
* The tote identification or scan confirmation indicates the intended association has been restored.

## Failure Conditions

* The tote was returned with a different Tote ID or to the wrong position and reassociation is not completed.
* The source section does not provide enough detail to execute the full rescanning workflow without another documented scanner process available to the user.
* The scanner indicates an unsuccessful scan or pairing.
* The tote cannot be confirmed as associated with the intended location after rescanning.

## Escalation Guidance

* Escalate for review if the reassociation cannot be completed using the documented scanner process available to the user.
* Escalate if the original tote position or correct Tote ID cannot be determined.
* Escalate if repeated rescanning attempts do not produce a successful association.

## Missing Details / Known Gaps

* The supplied source section explicitly states rescanning is required but does not provide a complete standalone rescanning procedure for this exact recovery case.
* The exact screen name, application state, and confirmation method for reassociation in this specific mismatch scenario are not fully provided in the packet.
* No explicit production-stop requirement is provided in the source evidence.
* No explicit LOTO requirement is provided in the source evidence.
* No time estimate is provided in the source evidence.

## Source Lineage

- Candidate IDs: candidate_l1_rescan_tote_to_reassociate_with_designated_location_after_position_mismatch
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
