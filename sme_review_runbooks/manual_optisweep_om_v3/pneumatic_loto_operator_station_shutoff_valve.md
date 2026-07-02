# Apply pneumatic LOTO at an operator station shut-off valve

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_apply_pneumatic_loto_at_an_operator_station_shut_off_valve_v1` |
| Title | Apply pneumatic LOTO at an operator station shut-off valve |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Isolate pneumatic energy at an operator station by locating that station's shut-off valve, turning the valve to OFF, and applying lockout/tagout to the valve. The source indicates each operator station has its own shut-off valve.

## When To Use

Use when pneumatic energy at a specific operator station must be isolated using the station's dedicated shut-off valve.

## Do Not Use For

* Do not use if the correct operator station shut-off valve cannot be positively identified from the source.
* Do not use if the valve cannot be turned to OFF.
* Do not use if the valve cannot be locked/tagged out as required.

## Safety And Operational Notes

* This procedure is a lockout/tagout energy-isolation task.
* Stop and escalate if the correct shut-off valve cannot be identified.
* Stop and escalate if the valve cannot be turned to OFF or cannot be locked/tagged out as required.

## Access Or Tools Needed

* Access to the operator station shut-off valve
* LOTO device/tag for the valve

## Procedure Steps

### Step 1 — Identify the operator station shut-off valve

**Responsible role:** L2_support

**Instruction:**
Identify the operator station shut-off valve for the station being isolated. The source states that each operator station has its own shut-off valve.

**Expected result:**
The correct shut-off valve for the intended operator station is identified.

**Stop or Escalate If:**

* The correct shut-off valve cannot be identified from the source.

---

### Step 2 — Turn the shut-off valve to OFF

**Responsible role:** L2_support

**Instruction:**
Turn the shut-off valve to "OFF."

**Expected result:**
The shut-off valve is in the OFF position.

**Stop or Escalate If:**

* The valve cannot be turned to OFF.

---

### Step 3 — Apply lockout/tagout to the valve

**Responsible role:** L2_support

**Instruction:**
Apply LOTO to the valve.

**Expected result:**
The valve is locked/tagged out in the OFF position.

**Stop or Escalate If:**

* The valve cannot be locked/tagged out as required.

---

## Success Criteria

* The correct operator station shut-off valve was identified.
* The shut-off valve is in the OFF position.
* The valve is locked/tagged out.
* The operator station pneumatic shut-off valve is in the OFF position and locked/tagged out.

## Failure Conditions

* The correct shut-off valve cannot be identified from the source.
* The valve cannot be turned to OFF.
* The valve cannot be locked/tagged out as required.

## Escalation Guidance

* Stop and escalate if the correct shut-off valve cannot be identified from the source.
* Stop and escalate if the valve cannot be turned to OFF.
* Stop and escalate if the valve cannot be locked/tagged out as required.

## Missing Details / Known Gaps

* The source packet does not provide the actual text or OCR content of section 1.3 Pneumatic LOTO.
* The source does not provide a visual artifact for the operator station shut-off valve in this packet.
* The source does not specify a supporting role beyond the primary executor.
* The source does not specify whether production stop is required.
* The source does not provide an estimated completion time.
* The source does not provide a verification method beyond the valve being OFF and locked/tagged out.

## Source Lineage

- Candidate IDs: pneumatic_loto_operator_station_shutoff_valve
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
