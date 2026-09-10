# Apply Pneumatic LOTO at an Operator Station Shut-off Valve

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_apply_pneumatic_loto_at_operator_station_shutoff_valve_v1` |
| Title | Apply Pneumatic LOTO at an Operator Station Shut-off Valve |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `e_stop_or_safety_stop` |
| Access Surface | `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_smeme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely isolate the pneumatic supply for a specific OptiSweep operator station by turning that station’s pneumatic shut-off valve to OFF and applying LOTO to secure the OFF position.

## When To Use

Use when you need to isolate pneumatic power for a specific operator station by securing its pneumatic shut-off valve in the OFF position with LOTO.

## Safety And Operational Notes

* Each operator station has its own pneumatic shut-off valve; ensure you isolate the correct station before applying LOTO.

## Access Or Tools Needed

* Physical access to the operator station pneumatic shut-off valve
* LOTO hardware (lock and tag) appropriate for the site procedure

## Procedure Steps

### Step 1 — Identify the operator station’s pneumatic shut-off valve

**Responsible role:** operator

**Instruction:**
Locate the pneumatic shut-off valve for the specific operator station you need to isolate (each operator station has its own shut-off valve).

**Expected result:**
You have positively identified the pneumatic shut-off valve that corresponds to the targeted operator station.

**Stop or Escalate If:**

* Stop and escalate if you cannot positively identify the correct operator station’s shut-off valve.

---

### Step 2 — Turn the shut-off valve to OFF

**Responsible role:** operator

**Instruction:**
Turn the identified shut-off valve to “OFF.”

**Expected result:**
The targeted operator station pneumatic shut-off valve is in the OFF position.

**Stop or Escalate If:**

* Stop and escalate if the valve does not remain in the OFF position after turning it to OFF (unexpected movement/behavior).

---

### Step 3 — Apply LOTO to the valve

**Responsible role:** operator

**Instruction:**
Apply LOTO to the valve to lockout/tagout the OFF position.

**Expected result:**
The targeted operator station pneumatic shut-off valve is secured with LOTO in the OFF position.

---

## Success Criteria

* The targeted operator station pneumatic shut-off valve is in the OFF position.
* The OFF position is secured with LOTO.

## Failure Conditions

* Cannot positively identify the correct operator station’s shut-off valve.
* Valve does not remain in the OFF position after turning it to OFF (unexpected movement/behavior).
* Valve OFF position is not secured with LOTO.

## Escalation Guidance

* Stop and escalate if you cannot positively identify the correct operator station’s shut-off valve.
* Stop and escalate if the valve does not remain in the OFF position after turning it to OFF (unexpected movement/behavior).

## Missing Details / Known Gaps

* No additional live observable checks (e.g., pneumatic pressure indicators) are provided in the supplied section excerpt beyond valve OFF position and LOTO application.

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_pneumatic_loto_shutoff_valve_off_loto
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
