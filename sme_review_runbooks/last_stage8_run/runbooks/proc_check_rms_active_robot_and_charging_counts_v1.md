# Check RMS active robot count and charging robots count on the map monitor summary

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_rms_active_robot_and_charging_counts_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `fleet_system_status` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS / fleet status UI map monitor summary metrics to read (1) the active robot count (robots actively running) and (2) the charging robots count (robots actively charging) at the current moment.

## When To Use

When you need a quick, high-level check of how many robots are actively running and how many are actively charging right now using the RMS map monitor summary metrics.

## Source Procedure References

- proc_check_rms_active_robot_and_charging_counts_v1

## Procedure Steps

### Step 1 — Open the RMS / fleet status UI map monitor summary area

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI and navigate to the map monitor summary area that contains the Map Monitor Message Panel summary metrics.

**Expected result:**
The RMS map monitor summary metrics panel is visible, including the metric labeled 'active robot count' (robots actively running) and the metric labeled for robots charging (charging robots count).

---

### Step 2 — Read the active robot count (robots actively running)

**Responsible role:** L1_support

**Instruction:**
In the RMS map monitor summary metrics, locate the 'active robot count' metric and read its value.

**Expected result:**
You obtain the numeric value for 'active robot count' that represents how many robots are actively running in the system.

---

### Step 3 — Read the charging robots count (robots actively charging)

**Responsible role:** L1_support

**Instruction:**
In the RMS map monitor summary metrics, locate the metric for robots that are on the charter / charging robots (charging robots count) and read its value.

**Expected result:**
You obtain the numeric value for the charging robots count that represents how many robots are actively charging at the moment (example described as '10').

---

### Step 4 — Stop and escalate on unexpected count mismatch

**Responsible role:** L1_support

**Instruction:**
If either the active robot count or the charging robots count is unexpectedly low/high relative to operator expectation for the shift, stop and escalate.

**Expected result:**
A mismatch condition is identified and escalation is initiated when counts are unexpectedly low/high or do not align with observed system behavior.

---

## Success Criteria

- Active robot count value is read from the RMS map monitor summary and interpreted as robots actively running.
- Charging robots count value is read from the RMS map monitor summary and interpreted as robots actively charging.
- Escalation occurs when either count is unexpectedly low/high relative to operator expectation or mismatches observed behavior.

## Failure Conditions

- Active robot count is unexpectedly low/high relative to operator expectation for the shift.
- Charging robots count is unexpectedly low/high relative to operator expectation for the shift.
- Charging robots count does not align with observed system behavior (e.g., robots visibly charging but charging count is 0, or vice versa).

## Escalation Guidance

- Escalate when either metric is unexpectedly low/high relative to operator expectation for the shift or when the charging count mismatches observed system behavior.

## Missing Details / Known Gaps

- No explicit numeric thresholds for 'unexpectedly low/high' are provided; escalation judgment must use operator expectation supplied externally.
