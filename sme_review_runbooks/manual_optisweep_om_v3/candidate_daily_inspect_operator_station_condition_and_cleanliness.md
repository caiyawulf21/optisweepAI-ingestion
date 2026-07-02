# Perform Daily Preventive Inspection Of The Operator Station

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_perform_daily_preventive_inspection_of_the_operator_station_v1` |
| Title | Perform Daily Preventive Inspection Of The Operator Station |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Perform the documented daily preventive inspection of the operator station by checking for controller damage, confirming stacklights are operational, and verifying the chute is free of debris such as stuck labels.

## When To Use

Use during the daily preventive maintenance inspection for the operator station.

## Do Not Use For

* Corrective repair of controller damage
* Detailed stacklight troubleshooting or electrical repair
* Debris removal methods not documented in the source
* Tipper maintenance or robot maintenance procedures

## Safety And Operational Notes

* This source provides inspection points only and does not provide corrective maintenance steps.
* Do not perform repair or non-documented clearing methods based on this runbook alone.

## Access Or Tools Needed

* Physical access to the operator station
* Visual access to the controller, stacklights, and chute

## Related Operational Context

* ctx_manual_daily_preventive_maintenance_overview_v1
* ctx_manual_operator_station_hmi_reference_v1

## Procedure Steps

### Step 1 — Go to the operator station

**Responsible role:** L2_support

**Instruction:**
Go to the operator station to perform the daily preventive maintenance inspection.

**Expected result:**
You are at the operator station and can visually inspect the controller, stacklights, and chute.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Use the operator station reference photo to identify the chute, stacklights, and overall station layout.*

![artifact_fig_3_2_rotary_station](assets/artifact_fig_3_2_rotary_station.png)

*Use the rotary station photo to orient yourself to the area under the chute.*


**Stop or Escalate If:**

* The operator station cannot be safely accessed for inspection.
* The required inspection points cannot be identified from the available source material.

---

### Step 2 — Inspect the controller for damage

**Responsible role:** L2_support

**Instruction:**
Inspect the controller for damage.

**Expected result:**
No controller damage is observed.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Use the operator station reference image to identify the operator station area while locating inspection points.*


**Stop or Escalate If:**

* Controller damage is observed.
* The controller cannot be adequately inspected.

---

### Step 3 — Verify stacklights are operational

**Responsible role:** L2_support

**Instruction:**
Verify that the stacklights are operational.

**Expected result:**
The stacklights are operational.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Look at the top of the frame on either side of the chute where the stacklights are mounted.*


**Stop or Escalate If:**

* A stacklight is not operational.
* Stacklight condition cannot be confirmed from inspection.

---

### Step 4 — Inspect the chute for debris

**Responsible role:** L2_support

**Instruction:**
Inspect the chute and confirm it is free of debris, including stuck labels.

**Expected result:**
The chute is free of debris, including stuck labels.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Identify the chute in the operator station reference image and inspect the corresponding physical chute area.*

![artifact_fig_3_2_rotary_station](assets/artifact_fig_3_2_rotary_station.png)

*Use the rotary station image to orient the chute area above the rotary station.*


**Stop or Escalate If:**

* Debris or stuck labels are found and cannot be cleared using source-approved methods.
* The chute cannot be adequately inspected.

---

## Success Criteria

* Controller damage is not observed.
* Stacklights are confirmed operational.
* Chute is confirmed free of debris, including stuck labels.

## Failure Conditions

* Controller damage is observed.
* Stacklights are not operational.
* Debris or stuck labels are present in the chute.
* Any required inspection point cannot be adequately inspected.

## Escalation Guidance

* Escalate if controller damage is observed.
* Escalate if stacklights are not operational.
* Escalate if chute debris cannot be cleared using source-approved methods.
* Escalate when corrective action is required, because the source provides inspection points only and does not provide corrective actions.

## Missing Details / Known Gaps

* The source does not provide a documented inspection method for proving stacklights are operational.
* The source does not provide corrective actions for controller damage, stacklight failure, or chute debris.
* The source does not provide a documented debris-clearing method.
* The source does not specify whether production must be stopped for this inspection.
* The source does not specify whether LOTO is required for this inspection.
* The source does not provide an estimated completion time.
* The source does not explicitly assign the task to a named role; L2_support is inherited from the candidate.

## Source Lineage

- Candidate IDs: candidate_daily_inspect_operator_station_condition_and_cleanliness
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
