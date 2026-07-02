# Verify the tipper recommissioning requirement after part replacement

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_tipper_recommissioning_requirement_after_part_replacement_v1` |
| Title | Verify the tipper recommissioning requirement after part replacement |
| Procedure Type | `reference` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Reference procedure to confirm and communicate the documented maintenance requirement that a tipper must be re-commissioned after any part is replaced.

## When To Use

Use when reviewing tipper maintenance work, replacement activity, or return-to-service readiness to confirm whether the manual requires recommissioning after a part replacement.

## Do Not Use For

* Do not use as the actual tipper recommissioning procedure.
* Do not use as a part replacement procedure.
* Do not use to derive recommissioning steps not provided in this source section.

## Safety And Operational Notes

* This source packet provides a maintenance requirement note only; it does not provide the recommissioning procedure in this section.
* Do not return the tipper to service based only on this note without completing the applicable recommissioning procedure from the appropriate source section.

## Access Or Tools Needed

* Access to the maintenance manual note for section 7.3

## Related Operational Context

* ctx_manual_tipper_recommissioning_note_v1

## Procedure Steps

### Step 1 — Identify whether a tipper part was replaced

**Responsible role:** L2_support

**Instruction:**
Review the maintenance situation and identify whether any part on the tipper has been replaced.

**Expected result:**
A determination is made on whether a tipper part replacement occurred.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Major tipper components that may have been replaced.*


**Stop or Escalate If:**

* It cannot be determined whether any tipper part was replaced.

---

### Step 2 — Verify the documented recommissioning requirement

**Responsible role:** L2_support

**Instruction:**
Verify in the maintenance manual note that the tipper must be re-commissioned after any part is replaced.

**Expected result:**
The source requirement is confirmed from the manual.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Nearby page 103 maintenance context in section 7.3.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Nearby page 103 maintenance context in section 7.3.*


**Stop or Escalate If:**

* The source note cannot be verified from the supplied packet.
* Additional recommissioning steps are needed but are not present in this section.

---

### Step 3 — Record or communicate the requirement before return to service

**Responsible role:** L2_support

**Instruction:**
Record or communicate that re-commissioning is required before returning the tipper to service.

**Expected result:**
The recommissioning requirement is documented or communicated for the affected tipper.

**Screens / Images:**

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*Commissioning-related HMI context showing that tipper commissioning activities exist elsewhere in the manual.*


**Stop or Escalate If:**

* The recommissioning procedure is needed but not available in this source section.
* There is any attempt to return the tipper to service without completing the required recommissioning.

---

## Success Criteria

* It is confirmed whether a tipper part was replaced.
* The manual requirement that a tipper must be re-commissioned after any part is replaced is verified.
* The recommissioning requirement is recorded or communicated before the tipper is returned to service.

## Failure Conditions

* A tipper part replacement occurs and the recommissioning requirement is not recognized.
* The source note cannot be verified from the supplied packet.
* The tipper is returned to service without addressing the documented recommissioning requirement.

## Escalation Guidance

* Escalate if the maintenance status does not clearly show whether a tipper part was replaced.
* Escalate if the actual recommissioning procedure is required, because this source section provides only the requirement note and not the procedure steps.
* Escalate before return to service if recommissioning has not been completed.

## Missing Details / Known Gaps

* The supplied source section does not provide the actual recommissioning procedure steps.
* The supplied source section does not specify exact documentation method, system, or form for recording the requirement.
* The supplied source section does not specify production stop or LOTO requirements for this reference activity.
* The supplied source section does not provide a time estimate.

## Source Lineage

- Candidate IDs: record_recommissioning_requirement_after_tipper_part_replacement
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
