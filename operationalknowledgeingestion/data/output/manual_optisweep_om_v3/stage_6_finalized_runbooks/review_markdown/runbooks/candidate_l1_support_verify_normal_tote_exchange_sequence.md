# Verify The Normal Tote Exchange Sequence Coordinated By WCS

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_the_normal_tote_exchange_sequence_coordinated_by_wcs_v1` |
| Title | Verify The Normal Tote Exchange Sequence Coordinated By WCS |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-backed diagnostic procedure to verify that the documented normal tote exchange sequence occurs during operation: parcels are directed into a tote, the tote reaches a configured limit, the WCS signals the sorter PLC to stop diverting packages, an AGV retrieves the full tote, another AGV places an empty tote, and the WCS signals the sorter PLC to resume sortation.

## When To Use

Use when verifying whether normal WCS-coordinated tote exchange behavior matches the sequence described in the source during sorter operation.

## Do Not Use For

* Not for performing tote exchange configuration changes.
* Not for AGV fault recovery or lost-task recovery procedures.
* Not for manual tote add/remove or hospital station handling procedures.
* Not for confirming specific screen names, message text, or status fields not provided by the source.

## Safety And Operational Notes

* This candidate is marked support-safe in the source packet.
* The source does not provide additional safety controls, lockout/tagout requirements, or production stop requirements for this verification activity.

## Access Or Tools Needed

* Ability to observe sorter and tote exchange activity
* Access to WCS or sorter status indications if available at the site

## Procedure Steps

### Step 1 — Observe parcels entering a tote during sorter operation

**Responsible role:** L1_support

**Instruction:**
Observe sorter operation and confirm that parcels are being directed into a tote.

**Expected result:**
Parcels are actively being directed into a tote during normal sorter operation.

**Stop or Escalate If:**

* No active tote filling can be observed
* System is not in normal operation, preventing sequence verification

---

### Step 2 — Check whether the tote has reached its configured exchange limit

**Responsible role:** L1_support

**Instruction:**
Check whether the tote has reached the customer-specified weight, number of parcels, or volume threshold, if that state is available from site indicators or operations context.

**Expected result:**
A tote limit condition is observable or inferable from available site indicators or context.

**Screens / Images:**

![artifact_fig_4_16_exchange_settings_pop_up_screen](assets/artifact_fig_4_16_exchange_settings_pop_up_screen.jpeg)

*Exchange threshold settings related to count, cube, and weight that define when tote exchange conditions may occur.*


**Stop or Escalate If:**

* Threshold state cannot be determined from available site indicators
* Observed exchange behavior occurs without a clear threshold condition and site-specific tooling is required to confirm

---

### Step 3 — Verify stop-diverting command from WCS to sorter PLC

**Responsible role:** L1_support

**Instruction:**
Verify that the WCS sends a message to the sorter PLC to stop diverting packages when the tote limit is reached.

**Expected result:**
Package diverting stops when the tote reaches the configured limit.

**Stop or Escalate If:**

* Diverting continues after the tote limit is reached
* The observed sequence does not match the documented order

---

### Step 4 — Verify AGV retrieval of the full tote

**Responsible role:** L1_support

**Instruction:**
Verify that an AGV is triggered via the WCS controller to retrieve the full tote.

**Expected result:**
An AGV retrieves the full tote after diverting stops.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV-related controls or status context that may help identify AGV activity if such site tooling is used for observation.*


**Stop or Escalate If:**

* The tote is not retrieved as described
* AGV retrieval does not occur after diverting stops
* The observed sequence does not match the documented order

---

### Step 5 — Verify placement of an empty tote by another AGV

**Responsible role:** L1_support

**Instruction:**
Verify that another AGV places an empty tote where the full tote was removed.

**Expected result:**
An empty tote is placed in the vacated position after the full tote is removed.

**Stop or Escalate If:**

* The tote is not replaced as described
* No empty tote is placed after full tote removal
* The observed sequence does not match the documented order

---

### Step 6 — Verify sortation resumes after empty tote placement

**Responsible role:** L1_support

**Instruction:**
Verify that the WCS sends a message to the sorter PLC to resume sortation after the empty tote is in place.

**Expected result:**
Sortation resumes after the empty tote is placed.

**Stop or Escalate If:**

* Sortation does not resume after empty tote placement
* Sortation resumes before the empty tote is in place
* The observed sequence does not match the documented order

---

## Success Criteria

* The observed tote exchange follows the documented sequence of stop diverting, retrieve the full tote, replace it with an empty tote, and resume sortation.
* The sequence occurs in the documented order after the tote reaches the configured weight, parcel-count, or volume limit.

## Failure Conditions

* The observed sequence does not match the documented order.
* The tote is not retrieved or replaced as described.
* The source does not provide screen names, message text, or status fields, so verification may require site-specific tooling not defined here.

## Escalation Guidance

* Escalate if the observed sequence does not match the documented order.
* Escalate if the tote is not retrieved or replaced as described.
* Escalate if verification depends on site-specific screens, message text, or status fields not defined in this source.

## Missing Details / Known Gaps

* The source does not provide specific screen names, message text, or status fields for verifying WCS-to-sorter PLC messaging.
* The source does not define exact operator observations or indicators that confirm threshold attainment at runtime.
* The source does not provide explicit escalation contacts or routing.
* The source does not provide a time estimate for completing this verification.
* The source does not specify whether production stop or LOTO is required for this verification.

## Source Lineage

- Candidate IDs: candidate_l1_support_verify_normal_tote_exchange_sequence
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
