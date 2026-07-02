# Clean Small Valve Ports With Compressed Air For A Clogged Air Line

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_clean_small_valve_ports_with_compressed_air_for_a_clogged_air_line_v1` |
| Title | Clean Small Valve Ports With Compressed Air For A Clogged Air Line |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use compressed air to clean debris from the small ports inside the valve when pneumatic troubleshooting identifies a clogged air line caused by contamination in the valve ports.

## When To Use

Use when troubleshooting a clogged air line and the source identifies debris in the small ports inside the valve as the likely cause.

## Do Not Use For

* Do not use as a complete pneumatic isolation or disassembly procedure; the source does not provide those details.
* Do not use as a filtration system correction procedure; the source only notes that better filtration may be needed if contamination is common.

## Safety And Operational Notes

* This procedure is not confirmed support-safe by the source.
* The source does not provide pneumatic isolation, pressure release, disassembly, or lockout details.
* Review site maintenance controls before performing compressed-air cleaning on the valve.

## Access Or Tools Needed

* Access to the affected valve
* Compressed air

## Related Operational Context

* ctx_manual_maintenance_pneumatic_air_line_clogged_v1

## Procedure Steps

### Step 1 — Identify the valve associated with the clogged air line

**Responsible role:** L2_support

**Instruction:**
Identify the valve associated with the clogged air line so the small ports inside that valve can be inspected and cleaned.

**Expected result:**
The affected valve has been identified for inspection.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Use only as a general component-identification aid near the tipper assembly; the packet does not provide a valve-specific cleaning image.*


**Stop or Escalate If:**

* Stop or escalate if the affected valve cannot be identified from the source-supported information.
* Stop or escalate if safe access or maintenance controls are not established, because the source does not provide isolation details.

---

### Step 2 — Inspect the small ports inside the valve for debris

**Responsible role:** L2_support

**Instruction:**
Inspect the small ports inside the identified valve for debris.

**Expected result:**
The presence or absence of debris in the small valve ports is determined.

**Stop or Escalate If:**

* Stop or escalate if the valve ports cannot be safely accessed or inspected using source-supported information.
* Escalate if contamination appears common or recurring.

---

### Step 3 — Use compressed air to clean out the ports

**Responsible role:** L2_support

**Instruction:**
Use compressed air to clean out the small ports inside the valve.

**Expected result:**
Debris is blown out of the small valve ports.

**Stop or Escalate If:**

* Escalate if contamination is common, because a better filtration system may be needed.
* Stop or escalate if the ports cannot be cleaned with the source-supported action.

---

### Step 4 — Verify whether the clog condition is cleared

**Responsible role:** L2_support

**Instruction:**
Verify whether the clogged air line condition is cleared after cleaning the small valve ports.

**Expected result:**
The clogged air line condition is either cleared or confirmed to persist.

**Stop or Escalate If:**

* Escalate if the clog condition remains after cleaning the ports.

---

## Success Criteria

* Debris is cleared from the small ports inside the valve.
* The clogged air line condition is addressed after cleaning.

## Failure Conditions

* The affected valve cannot be confidently identified.
* The small ports cannot be safely accessed or inspected using the source-provided information.
* Debris remains after compressed-air cleaning.
* Contamination is common or recurring.
* The clogged air line condition remains after cleaning the ports.

## Escalation Guidance

* Escalate if contamination is common, because the source states that a better filtration system may be needed.
* Escalate if the clog condition remains after cleaning the ports.
* Escalate for SME or maintenance review because the source does not provide isolation, disassembly, or pneumatic safety details.

## Missing Details / Known Gaps

* The source does not identify the exact valve location for the clogged air line.
* The source does not provide pneumatic isolation or pressure-release instructions.
* The source does not provide disassembly or access steps for reaching the small valve ports.
* The source does not define a detailed verification method for confirming the clog is cleared.
* The packet does not include a valve-specific image for this procedure.

## Source Lineage

- Candidate IDs: candidate_clean_valve_ports_for_clogged_air_line_using_compressed_air
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
