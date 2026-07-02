# Identify A Faulted Tipper From The Operator Station Fault Beacon And Return It To Service

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_and_return_faulted_tipper_to_service_from_operator_station_fault_beacon_v1` |
| Title | Identify A Faulted Tipper From The Operator Station Fault Beacon And Return It To Service |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station fault beacon to identify a tipper fault, correct the fault, and return the tipper to service. The source supports the high-level troubleshooting sequence but does not provide the detailed fault-correction method in the cited troubleshooting entry.

## When To Use

Use when too many AGVs are being directed to the hospital and the troubleshooting guidance indicates a tipper fault should be identified by looking for a fault beacon on the operator station, then corrected and returned to service.

## Do Not Use For

* Do not use as a complete repair procedure when fault-specific correction steps are required but not provided in the source.
* Do not use when the operator station fault beacon cannot be correlated to a specific tipper from the available source evidence.

## Safety And Operational Notes

* The candidate marks this procedure as not support-safe.
* The cited troubleshooting source does not provide detailed correction or recovery controls; use only documented fault-specific procedures when available.
* Do not invent reset, override, or return-to-service actions not explicitly supported by the source.

## Access Or Tools Needed

* Access to the operator station
* Visibility of the fault beacon
* Applicable fault-specific documentation if available

## Related Operational Context

* ctx_manual_hmi_fault_beacon_operator_station_v1

## Procedure Steps

### Step 1 — Check the operator station for the fault beacon

**Responsible role:** L1_support

**Instruction:**
Go to the operator station and look for the fault beacon that indicates the tipper fault.

**Expected result:**
A fault beacon is observed on the operator station, or no beacon is found.

**Screens / Images:**

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*General operator station HMI layout for orientation while locating fault-related indications.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Operator station screen context associated with fault handling and RESET-related controls; use only for orientation, not as a prescribed action.*

![artifact_page_86_image_15](assets/artifact_page_86_image_15.png)

*Physical operator station controls for general station identification.*


**Stop or Escalate If:**

* The fault beacon is present but its meaning or associated tipper cannot be determined from the source.
* No fault beacon is visible and the troubleshooting symptom persists.

---

### Step 2 — Identify the affected tipper

**Responsible role:** L1_support

**Instruction:**
Identify the tipper associated with the fault beacon.

**Expected result:**
The affected tipper is identified.

**Screens / Images:**

![artifact_page_87_image_2](assets/artifact_page_87_image_2.jpeg)

*Related operator station screen context for selecting or confirming an affected tipper in a separate tipper fault scenario.*

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*Operator station HMI context showing tipper-related station interface orientation.*


**Stop or Escalate If:**

* The affected tipper cannot be identified from the beacon and available source material.

---

### Step 3 — Correct the fault using applicable documented procedure

**Responsible role:** L1_support

**Instruction:**
Correct the fault using the applicable documented fault-specific procedure if available.

**Expected result:**
The fault condition is corrected according to a documented procedure.

**Screens / Images:**

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*Only if a separate documented fault-specific procedure identifies flat-flex cable replacement as the required correction.*

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Related fault recovery context only if the identified issue involves AGV fault handling documented elsewhere in the same source.*


**Stop or Escalate If:**

* The fault beacon is present but the source does not provide the fault-specific correction steps.
* The identified fault requires a repair or recovery procedure not included in the supplied evidence.
* Any required corrective action would require unsupported commands, settings changes, or maintenance actions not explicitly documented in the packet.

---

### Step 4 — Return the tipper to service

**Responsible role:** L1_support

**Instruction:**
Return the tipper to service.

**Expected result:**
The tipper is back in service after fault correction.

**Screens / Images:**

![artifact_page_86_image_15](assets/artifact_page_86_image_15.png)

*Operator station controls in related return-to-automatic-operation context; use only if a separate documented fault-specific procedure directs these controls.*

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station context if AGV/tote flow normalization is part of the broader recovery outcome.*


**Stop or Escalate If:**

* The tipper cannot be returned to service after the fault is corrected.
* The source does not provide the exact return-to-service actions needed for the identified fault.

---

## Success Criteria

* The faulted tipper is identified from the operator station fault beacon.
* The applicable fault is corrected using documented source-supported guidance if available.
* The tipper is returned to service.

## Failure Conditions

* The fault beacon is present but the source does not provide fault-specific correction steps.
* The affected tipper cannot be identified from the available source evidence.
* The tipper cannot be returned to service after correction.

## Escalation Guidance

* Escalate if the fault beacon is present but the source does not provide the fault-specific correction steps.
* Escalate if the tipper cannot be returned to service after the fault is corrected.
* Escalate if the operator station indication cannot be mapped to a specific tipper using the supplied source evidence.

## Missing Details / Known Gaps

* The source does not describe the appearance or exact behavior of the operator station fault beacon.
* The source does not explain how to map the fault beacon to a specific tipper.
* The source does not provide the fault-specific correction steps.
* The source does not provide the exact return-to-service actions.
* No commands are provided in the cited troubleshooting entry.
* Production stop and LOTO requirements are not stated for this troubleshooting action.

## Source Lineage

- Candidate IDs: candidate_identify_and_return_faulted_tipper_to_service_from_operator_station_fault_beacon
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
