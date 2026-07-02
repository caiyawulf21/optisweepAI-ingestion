# Verify Operator Station Stacklight Locations

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_operator_station_stacklight_locations_v1` |
| Title | Verify Operator Station Stacklight Locations |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this reference procedure to confirm that the operator station stacklights are located as documented in the manual: two stacklights mounted on the top of the frame on either side of the chute.

## When To Use

Use when identifying operator station components or verifying that the stacklights are physically located at the operator station as documented in the manual and Figure 3-1/Table 3-1 references.

## Do Not Use For

* Do not use this procedure to interpret stacklight colors, statuses, or alarms.
* Do not use this procedure for corrective action if a stacklight is missing, relocated, or malfunctioning.
* Do not use this procedure for hospital station stacklight inspection.

## Safety And Operational Notes

* This source supports visual location verification only.
* No source-supported lockout, shutdown, or intervention steps are provided in this procedure.

## Access Or Tools Needed

* Visual access to the operator station
* Figure 3-1 Operator Station (Panels Removed for Clarity)
* Operator station feature list in Table 3-1

## Related Operational Context

* ctx_manual_operator_station_overview_v1
* ctx_manual_hospital_station_stacklight_reference_v1
* ctx_manual_operator_station_component_reference_v1

## Procedure Steps

### Step 1 — Go to the operator station and locate the chute

**Responsible role:** operator

**Instruction:**
Go to the operator station and identify the chute in the operator station area.

**Expected result:**
The chute is identified at the operator station.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Use the operator station reference image to identify the chute within the operator-facing component layout.*


**Stop or Escalate If:**

* Stop or escalate if the operator station layout does not allow the chute to be identified.

---

### Step 2 — Inspect the top of the frame around the chute area

**Responsible role:** operator

**Instruction:**
Look at the top of the frame around the chute area.

**Expected result:**
The top frame area around the chute is visible for comparison to the documented stacklight location.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Look at the top of the frame in relation to the chute to orient the expected stacklight mounting area.*


**Stop or Escalate If:**

* Stop or escalate if the top of the frame around the chute cannot be visually inspected.

---

### Step 3 — Verify two stacklights are mounted on either side of the chute

**Responsible role:** operator

**Instruction:**
Identify whether there are two stacklights mounted on the top of the frame, one on either side of the chute.

**Expected result:**
Two stacklights are observed on the top of the frame, one on each side of the chute.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Use Figure 3-1 to compare the observed stacklight positions relative to the chute and top frame.*


**Stop or Escalate If:**

* Escalate if the stacklights are missing, relocated, or do not match the documented position.

---

### Step 4 — Compare the observation to the documented feature references

**Responsible role:** operator

**Instruction:**
Compare the observed stacklight positions to the documented operator station feature list and figure reference.

**Expected result:**
The observed stacklight locations align with the operator station documentation in Table 3-1 and Figure 3-1.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Use the labeled operator station photo as the primary visual reference for stacklight placement.*


**Stop or Escalate If:**

* Escalate if the observed stacklight locations do not match the documented position.
* Escalate if additional interpretation is needed beyond location verification.

---

## Success Criteria

* The user confirms that two stacklights are mounted on the top of the frame on either side of the chute.
* The observed stacklight positions match the operator station documentation in Figure 3-1 and Table 3-1.

## Failure Conditions

* A stacklight is missing.
* The stacklights are relocated from the documented position.
* The observed stacklight arrangement does not match the documented operator station layout.
* The source does not provide status meanings or corrective actions for stacklight issues.

## Escalation Guidance

* Escalate if the stacklights are missing, relocated, or do not match the documented position.
* Escalate if the user needs stacklight status meanings, alarm interpretation, or corrective actions, because this source supports location verification only.

## Missing Details / Known Gaps

* The source does not provide stacklight color meanings, status interpretation, or alarm behavior for the operator station.
* The source does not provide corrective actions if stacklights are missing or relocated.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required for this visual verification.

## Source Lineage

- Candidate IDs: candidate_operator_station_verify_stacklight_locations
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
