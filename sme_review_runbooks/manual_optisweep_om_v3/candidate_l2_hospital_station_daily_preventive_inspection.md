# Inspect Each Hospital Station During Daily Preventive Maintenance

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_inspect_each_hospital_station_during_daily_preventive_maintenance_v1` |
| Title | Inspect Each Hospital Station During Daily Preventive Maintenance |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Perform the documented daily preventive maintenance inspection for each hospital station by checking barcode scanner operation, confirming stacklight operation, verifying the tabletop is free of debris, and recording whether each inspection point meets the source criteria.

## When To Use

Use during daily preventive maintenance when inspecting each hospital station for the documented inspection points: barcode scanner operation, stacklight operation, and tabletop cleanliness.

## Do Not Use For

* Do not use this runbook as a repair procedure for a non-operational barcode scanner.
* Do not use this runbook as a repair procedure for a non-operational stacklight.
* Do not use this runbook as a cleaning procedure beyond verifying that the tabletop is free of debris, because no cleaning method is provided in this source section.
* Do not use this runbook to define detailed test methods for scanner or stacklight operation, because this source section lists inspection points only.

## Safety And Operational Notes

* This source section is an inspection-only maintenance reference and does not provide repair, cleaning, lockout/tagout, or production-stop instructions.
* Escalate if a documented inspection point does not meet the source criteria and no source-backed corrective action is provided in this section.

## Access Or Tools Needed

* Physical access to each hospital station
* Visual access to the barcode scanner, stacklight, and tabletop
* Daily preventive maintenance checklist or record

## Related Operational Context

* ctx_manual_hospital_station_daily_inspection_v1

## Procedure Steps

### Step 1 — Inspect barcode scanner operation at the hospital station

**Responsible role:** L2_support

**Instruction:**
Go to the hospital station and inspect whether the barcode scanner is operational.

**Expected result:**
The barcode scanner is operational.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station area and green scanner context associated with hospital station operation.*

![artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen](assets/artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen.png)

*Hospital station barcode-related HMI context to identify barcode handling at the hospital station.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen.png)

*Hospital station barcode-related HMI context associated with barcode verification and mismatch handling.*

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*Scanner-related visual context included in the packet for scanner identification support.*


**Stop or Escalate If:**

* Barcode scanner is not operational.
* Barcode scanner operational state cannot be confirmed using the source-backed inspection point alone.

---

### Step 2 — Inspect stacklight operation at the hospital station

**Responsible role:** L2_support

**Instruction:**
Check whether the hospital station stacklight is operational.

**Expected result:**
The stacklight is operational.

**Screens / Images:**

![artifact_fig_3_5_hospital_station](assets/artifact_fig_3_5_hospital_station.png)

*Overall hospital station view to identify the station and stacklight location.*

![artifact_fig_3_6_stacklight](assets/artifact_fig_3_6_stacklight.png)

*Hospital station stacklight photo for stacklight identification and visual reference.*


**Stop or Escalate If:**

* Stacklight is not operational.
* Stacklight operational state cannot be confirmed using the source-backed inspection point alone.

---

### Step 3 — Inspect tabletop cleanliness

**Responsible role:** L2_support

**Instruction:**
Inspect the hospital station tabletop and verify it is free of debris.

**Expected result:**
The tabletop is free of debris.

**Screens / Images:**

![artifact_fig_3_5_hospital_station](assets/artifact_fig_3_5_hospital_station.png)

*Hospital station physical layout for tabletop area identification.*

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station area for general tabletop and work-surface context.*


**Stop or Escalate If:**

* Tabletop is not free of debris and no source-backed cleaning method is provided in this section.
* Tabletop condition cannot be restored using source-backed actions from this section.

---

### Step 4 — Record inspection results for each hospital station

**Responsible role:** L2_support

**Instruction:**
Record whether each documented inspection point meets the source criteria for each hospital station.

**Expected result:**
Inspection results are recorded for barcode scanner operation, stacklight operation, and tabletop cleanliness for each hospital station.

**Stop or Escalate If:**

* Any inspection point does not meet the source criteria.
* Required inspection results cannot be recorded on the daily preventive maintenance checklist or record.

---

## Success Criteria

* Each hospital station has been inspected for the three documented daily preventive maintenance points.
* Each hospital station barcode scanner is confirmed operational.
* Each hospital station stacklight is confirmed operational.
* Each hospital station tabletop is verified to be free of debris.
* Inspection results are recorded for each hospital station.

## Failure Conditions

* A hospital station barcode scanner is not operational.
* A hospital station stacklight is not operational.
* A hospital station tabletop is not free of debris.
* An inspection point cannot be confirmed using the source-backed inspection information.
* Inspection results are not recorded for one or more hospital stations.

## Escalation Guidance

* Escalate if a barcode scanner is not operational.
* Escalate if a stacklight is not operational.
* Escalate if tabletop debris cannot be addressed through source-backed actions; no cleaning method is provided in this section.
* Escalate if the source does not provide enough detail to confirm operational status for a documented inspection point.

## Missing Details / Known Gaps

* The source section provides inspection points only and does not define a detailed test method for confirming barcode scanner operation.
* The source section provides inspection points only and does not define a detailed test method for confirming stacklight operation.
* The source section does not provide a cleaning method for removing tabletop debris.
* The source section does not provide repair or corrective action steps for failed inspection points.
* The source section does not provide an estimated completion time.
* The source section does not specify whether production stop or lockout/tagout is required.

## Source Lineage

- Candidate IDs: candidate_l2_hospital_station_daily_preventive_inspection
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
