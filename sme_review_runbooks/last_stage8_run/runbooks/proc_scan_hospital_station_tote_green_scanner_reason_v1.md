# Scan Hospital Station Tote With Green Scanner to Determine Reason for Arrival

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_scan_hospital_station_tote_green_scanner_reason_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `hospital_diversion` |
| Access Surface | `hospital_hmi`, `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

When an AGV delivers a tote to the hospital station, the operator uses the green scanner to determine why the tote was brought to the station for manual handling.

## When To Use

Use when an AGV brings a tote to a hospital station for manual handling (mis-sort, bad tip, or tote overload scenarios).

## Source Procedure References

- proc_scan_hospital_station_tote_green_scanner_reason_v1

## Procedure Steps

### Step 1 — Wait for the AGV to bring the tote to the correct side of the hospital station

**Responsible role:** operator

**Instruction:**
At the hospital station, wait for the AGV to bring the tote to the right side (from the operator’s perspective).

**Expected result:**
The tote is delivered to the right side of the hospital station (extract side) where the operator can attend it.

---

### Step 2 — Confirm tote presence using the hospital station stacklight indication

**Responsible role:** operator

**Instruction:**
Visually check the hospital station stacklight to confirm a tote is present at the station.

**Expected result:**
The stacklight indicates a tote is present at the hospital station.

---

### Step 3 — Scan the tote with the green scanner to determine the reason for arrival

**Responsible role:** operator

**Instruction:**
Scan the tote barcode using the green scanner.

**Expected result:**
A scan-based reason for the tote’s arrival is produced/available for use in manual handling.

---

### Step 4 — Verify the scan result is available on the hospital station HMI (or scanner output) and proceed with manual handling

**Responsible role:** operator

**Instruction:**
Check the hospital station HMI (if present) or the scanner output to confirm the scan result is available, then use that reason to proceed with manual handling.

**Expected result:**
The operator can see the scan-based reason (or the scan-populated tote ID/barcode fields that drive the station’s status) on the hospital station HMI or scanner output and uses it to proceed.

---

## Success Criteria

- Operator obtains a scan-based reason for why the tote arrived at the hospital station and can proceed with the appropriate manual handling action.

## Failure Conditions

- Green scanner cannot read/produce a reason for the tote arrival (no scan result available).
- Tote reason cannot be determined even after re-scanning.
- Hospital HMI does not show scan-populated fields/status messages needed to determine the tote arrival reason.

## Escalation Guidance

- Escalate if the green scanner cannot read/produce a reason for the tote arrival (no scan result available).
- Escalate if the tote reason cannot be determined even after re-scanning.

## Missing Details / Known Gaps

- The manual confirms the operator uses a green scanner to determine the reason for arrival, but it does not specify the exact scanner UI workflow beyond scanning and (in some screens) tote ID auto-population. This runbook therefore focuses on observable outcomes: stacklight tote presence, scan-based reason availability, and HMI status messages/fields populated from the green scanner.
