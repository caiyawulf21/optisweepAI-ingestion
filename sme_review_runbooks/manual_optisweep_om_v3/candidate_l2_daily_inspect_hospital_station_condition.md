# Inspect Hospital Station During Daily Preventive Maintenance

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_inspect_hospital_station_during_daily_preventive_maintenance_v1` |
| Title | Inspect Hospital Station During Daily Preventive Maintenance |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify during daily preventive maintenance that each hospital station meets the documented inspection conditions: barcode scanner operational, stacklight operational, and tabletop free of debris.

## When To Use

Use this procedure when performing the documented daily preventive maintenance inspection for each hospital station.

## Do Not Use For

* Do not use this runbook to perform corrective repair or troubleshooting for scanner, stacklight, or tabletop issues; the source only provides inspection conditions and does not provide corrective steps.
* Do not use this runbook to define how to test barcode scanner or stacklight operation beyond inspection; the source does not define the operational test method.

## Safety And Operational Notes

* This runbook is limited to inspection and documentation steps supported by the source.
* If any inspection condition is not met, stop at documenting the observed issue; the source does not provide corrective actions.

## Access Or Tools Needed

* Physical access to each hospital station
* Ability to visually inspect the barcode scanner
* Ability to visually inspect the stacklight
* Ability to inspect the tabletop surface for debris
* Daily preventive maintenance documentation or checklist

## Related Operational Context

* ctx_manual_hospital_station_daily_pm_reference_v1
* ctx_manual_hospital_station_barcode_scanner_reference_v1
* ctx_manual_hospital_station_stacklight_overview_v1
* ctx_manual_hospital_station_tabletop_cleanliness_reference_v1

## Procedure Steps

### Step 1 — Go to each hospital station for inspection

**Responsible role:** L2_support

**Instruction:**
Go to each hospital station identified for daily preventive maintenance inspection.

**Expected result:**
Each required hospital station is reached and ready for inspection.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Use the hospital station image to identify the station area and scanner context before inspection.*


**Stop or Escalate If:**

* A required hospital station cannot be accessed for inspection.

---

### Step 2 — Inspect barcode scanner condition

**Responsible role:** L2_support

**Instruction:**
Inspect the hospital station barcode scanner and verify that it is operational.

**Expected result:**
The barcode scanner is verified as operational.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Use the hospital station image for scanner location context.*

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*Use the hospital HMI add tote screen context that references the green scanner used at the hospital station.*


**Stop or Escalate If:**

* The barcode scanner is not operational.
* The source-supported inspection cannot confirm scanner operational status.
* Corrective action is needed, because the source does not provide repair steps.

---

### Step 3 — Inspect stacklight condition

**Responsible role:** L2_support

**Instruction:**
Inspect the hospital station stacklight and verify that it is operational.

**Expected result:**
The stacklight is verified as operational.

**Screens / Images:**

![artifact_fig_3_6_stacklight](assets/artifact_fig_3_6_stacklight.png)

*Use the stacklight photo to identify the hospital station stacklight during inspection.*


**Stop or Escalate If:**

* The stacklight is not operational.
* The source-supported inspection cannot confirm stacklight operational status.
* Corrective action is needed, because the source does not provide repair steps.

---

### Step 4 — Inspect tabletop cleanliness

**Responsible role:** L2_support

**Instruction:**
Inspect the hospital station tabletop and verify that it is free of debris.

**Expected result:**
The tabletop is verified as free of debris.

**Stop or Escalate If:**

* The tabletop is not free of debris.
* Corrective action beyond documenting the issue is needed, because the source does not provide corrective steps.

---

### Step 5 — Record inspection results

**Responsible role:** L2_support

**Instruction:**
Record whether each inspected hospital station meets all documented inspection conditions.

**Expected result:**
Inspection results are documented for each hospital station.

**Stop or Escalate If:**

* Any hospital station does not meet the documented inspection conditions.
* Follow-up corrective action is required, because the source does not provide corrective steps.

---

## Success Criteria

* Each inspected hospital station is confirmed to have an operational barcode scanner.
* Each inspected hospital station is confirmed to have an operational stacklight.
* Each inspected hospital station is confirmed to have a tabletop free of debris.
* Inspection results are recorded for each inspected hospital station.

## Failure Conditions

* Barcode scanner is not operational.
* Stacklight is not operational.
* Tabletop is not free of debris.
* Operational status cannot be confirmed using the source-supported inspection information.

## Escalation Guidance

* If scanner operation, stacklight operation, or tabletop cleanliness does not meet the documented condition, stop at documenting the observed issue.
* Escalate for follow-up when corrective action is required, because the source does not provide corrective or repair steps.
* Use SME review to define the exact operational test method for scanner and stacklight status, because the source does not specify it.

## Missing Details / Known Gaps

* The source does not define how to test or confirm barcode scanner operational status.
* The source does not define how to test or confirm stacklight operational status.
* The source does not provide corrective actions if any inspection condition fails.
* The source does not explicitly assign the procedure to a role; L2_support is a conservative assignment from the candidate.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_l2_daily_inspect_hospital_station_condition
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
