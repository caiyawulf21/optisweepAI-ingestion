# Perform Hospital Station Daily Preventive Maintenance Checks (Barcode Scanner, Stacklight, Tabletop Debris)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_perform_hospital_station_daily_preventive_maintenance_checks_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `hospital_diversion` |
| Access Surface | `hospital_hmi`, `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Perform a daily physical inspection of each Hospital Station to verify the barcode scanner is operational, the stacklight is operational, and the tabletop is free of debris.

## When To Use

Use this procedure at the start of each day (daily preventive maintenance) to confirm each Hospital Station is safe/ready for operation by checking: (1) barcode scanner operational status, (2) stacklight operational status, and (3) tabletop debris-free condition.

## Source Procedure References

- proc_perform_hospital_station_daily_preventive_maintenance_checks_v1

## Procedure Steps

### Step 1 — Inspect each Hospital Station barcode scanner and confirm it is operational

**Responsible role:** operator

**Instruction:**
For each Hospital Station, visually inspect the barcode scanner and confirm it is operational.

**Expected result:**
For the station being inspected, the barcode scanner is operational.

---

### Step 2 — Inspect each Hospital Station stacklight and confirm it is operational

**Responsible role:** operator

**Instruction:**
For each Hospital Station, visually inspect the stacklight and confirm it is operational.

**Expected result:**
For the station being inspected, the stacklight is operational.

---

### Step 3 — Inspect each Hospital Station tabletop and confirm it is free of debris

**Responsible role:** operator

**Instruction:**
For each Hospital Station, visually inspect the tabletop area and confirm it is free of debris.

**Expected result:**
For the station being inspected, the tabletop is free of debris.

---

### Step 4 — Stop inspection and escalate if any required condition fails

**Responsible role:** operator

**Instruction:**
If any barcode scanner issue is observed, if the stacklight is not operational, or if debris is present on the tabletop, stop the inspection and escalate to maintenance/support as required by site practice.

**Expected result:**
Inspection is stopped for the day/sequence and escalation is initiated when any required condition fails.

---

## Success Criteria

- For each Hospital Station inspected: barcode scanner is operational
- For each Hospital Station inspected: stacklight is operational
- For each Hospital Station inspected: tabletop is free of debris

## Failure Conditions

- Barcode scanner is not operational at a Hospital Station
- Stacklight is not operational at a Hospital Station
- Debris is present on the tabletop at a Hospital Station

## Escalation Guidance

- Stop the inspection and escalate to maintenance/support as required by site practice if any barcode scanner issue is observed, if the stacklight is not operational, or if debris is present on the tabletop.

## Missing Details / Known Gaps

- The source does not define a specific observable test method for what “operational” means for the barcode scanner and stacklight during this daily PM (e.g., specific LED states, scan test steps, or pass/fail indicators).
