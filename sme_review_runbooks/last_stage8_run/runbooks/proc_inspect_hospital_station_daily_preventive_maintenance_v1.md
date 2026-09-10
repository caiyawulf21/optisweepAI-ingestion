# Inspect Hospital Station Daily Preventive Maintenance (Barcode Scanner, Stacklight, Tabletop Debris)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_inspect_hospital_station_daily_preventive_maintenance_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `device_roster_state` |
| Access Surface | `hospital_hmi`, `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Perform a daily preventive maintenance inspection on each hospital station by verifying the barcode scanner is operational, the stacklight is operational, and the tabletop is free of debris (e.g., stuck labels).

## When To Use

Use this procedure for daily preventive maintenance on each hospital station to confirm the station’s barcode scanner and stacklight are operational and that the tabletop is clear of debris.

## Source Procedure References

- proc_inspect_hospital_station_daily_preventive_maintenance_v1

## Procedure Steps

### Step 1 — Inspect each hospital station barcode scanner for operational condition

**Responsible role:** operator

**Instruction:**
For each hospital station, visually inspect the barcode scanner to confirm it is operational (e.g., not visibly damaged/obstructed).

**Expected result:**
The barcode scanner at the station is operational (no visible damage/obstruction preventing normal use).

---

### Step 2 — Inspect each hospital station stacklight for operational condition

**Responsible role:** operator

**Instruction:**
For each hospital station, visually inspect the stacklight to confirm it is operational (e.g., not visibly damaged/obstructed).

**Expected result:**
The stacklight at the station is operational (no visible damage/obstruction preventing normal use).

---

### Step 3 — Inspect tabletop and clear debris (e.g., stuck labels)

**Responsible role:** operator

**Instruction:**
For each hospital station, inspect the tabletop and remove/clear any debris such as stuck labels.

**Expected result:**
The tabletop is free of debris (no stuck labels) at the station.

---

### Step 4 — Stop inspection and escalate when scanner/stacklight/debris issue is found

**Responsible role:** operator

**Instruction:**
If a hospital station barcode scanner or stacklight is not operational, or if debris cannot be cleared, stop the inspection for that station and escalate to the appropriate maintenance contact.

**Expected result:**
Inspection is stopped for the affected station and maintenance escalation is initiated.

---

## Success Criteria

- For every hospital station inspected: barcode scanner is operational.
- For every hospital station inspected: stacklight is operational.
- For every hospital station inspected: tabletop is free of debris (no stuck labels).

## Failure Conditions

- Any hospital station barcode scanner is not operational.
- Any hospital station stacklight is not operational.
- Any hospital station tabletop still has debris (e.g., stuck labels) after clearing attempt.

## Escalation Guidance

- If a hospital station barcode scanner or stacklight is not operational, or debris cannot be cleared, stop inspection for that station and escalate to the appropriate maintenance contact.
- If the maintenance issue is related to the tipper, contact Lifecycle Performance Services (LPS) at 888-444-4647.

## Missing Details / Known Gaps

- The manual section provided defines “operational” for the barcode scanner and stacklight at a high level (operational / not visibly damaged/obstructed) but does not specify exact pass/fail indicators beyond that; the candidate requested additional images for what “operational” looks like for the barcode scanner and tabletop debris, but those specific images are not present in the packet as dedicated scanner/debris visuals.
- The candidate includes an escalation image note about initializing totes at the sorter using a Zebra scanner; the packet does not provide a step-by-step escalation procedure for hospital-station inspection failures, so this runbook only includes the escalation instruction at a high level and the tipper-related contact number.
