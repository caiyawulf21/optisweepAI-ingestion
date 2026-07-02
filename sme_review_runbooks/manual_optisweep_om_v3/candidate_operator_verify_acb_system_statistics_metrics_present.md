# Verify Which Metrics Are Present on the ACB System Statistics Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_which_metrics_are_present_on_the_acb_system_statistics_screen_v1` |
| Title | Verify Which Metrics Are Present on the ACB System Statistics Screen |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented ACB System Statistics screen to confirm that the expected statistics fields are present on the HMI. This procedure is limited to verifying field presence on the screen and does not interpret values, limits, or corrective actions.

## When To Use

Use when you need to confirm that the ACB System Statistics screen includes the documented metrics shown in the manual: robot faults, system faults, cycle time, and tipping station bag counts.

## Do Not Use For

* Do not use this procedure to interpret metric meanings, limits, thresholds, or normal ranges.
* Do not use this procedure as a troubleshooting or corrective-action procedure for abnormal values.
* Do not use this procedure to infer missing controls, hidden fields, or undocumented screen behavior.

## Safety And Operational Notes

* This candidate is a screen-reference verification and is marked support safe.
* The source only documents field presence and screen purpose; do not infer meanings, limits, or corrective actions for displayed values.

## Access Or Tools Needed

* Access to the system HMI
* ACB System screen
* ACB System Statistics screen
* Figure 4-5 or equivalent documented screen reference

## Related Operational Context

* ctx_manual_acb_system_statistics_screen_v1
* ctx_manual_acb_robot_and_system_fault_counts_v1
* ctx_manual_tipping_station_metrics_reference_v1

## Procedure Steps

### Step 1 — Open the ACB System Statistics screen

**Responsible role:** operator

**Instruction:**
From the "ACB System" screen, press STATISTICS to open the ACB System Statistics screen.

**Expected result:**
The ACB System Statistics screen is displayed.

**Screens / Images:**

![artifact_fig_4_5_acb_system_statistics_screen](assets/artifact_fig_4_5_acb_system_statistics_screen.jpeg)

*Use Figure 4-5 as the reference for the ACB System Statistics screen reached from the ACB System screen.*


**Stop or Escalate If:**

* The ACB System Statistics screen cannot be accessed from the ACB System screen.
* The displayed screen does not match the documented ACB System Statistics screen reference.

---

### Step 2 — Identify the documented statistics fields on the screen

**Responsible role:** operator

**Instruction:**
Review the ACB System Statistics screen and identify the documented statistics fields shown there: robot faults, system faults, cycle time, and tipping station bag counts.

**Expected result:**
The operator has identified the documented fields to verify on the screen.

**Screens / Images:**

![artifact_fig_4_5_acb_system_statistics_screen](assets/artifact_fig_4_5_acb_system_statistics_screen.jpeg)

*Review the Figure 4-5 layout and locate the documented statistics fields on the ACB System Statistics screen.*


**Stop or Escalate If:**

* The screen content does not show the documented statistics categories.
* The displayed screen appears inconsistent with Figure 4-5.

---

### Step 3 — Verify robot faults value is present

**Responsible role:** operator

**Instruction:**
Check the ACB System Statistics screen and verify that a robot faults value is present.

**Expected result:**
A robot faults value is visible on the ACB System Statistics screen.

**Screens / Images:**

![artifact_fig_4_5_acb_system_statistics_screen](assets/artifact_fig_4_5_acb_system_statistics_screen.jpeg)

*Locate the robot faults value on the ACB System Statistics screen.*


**Stop or Escalate If:**

* The robot faults value is not present on the ACB System Statistics screen.

---

### Step 4 — Verify system faults value is present

**Responsible role:** operator

**Instruction:**
Check the ACB System Statistics screen and verify that a system faults value is present.

**Expected result:**
A system faults value is visible on the ACB System Statistics screen.

**Screens / Images:**

![artifact_fig_4_5_acb_system_statistics_screen](assets/artifact_fig_4_5_acb_system_statistics_screen.jpeg)

*Locate the system faults value on the ACB System Statistics screen.*


**Stop or Escalate If:**

* The system faults value is not present on the ACB System Statistics screen.

---

### Step 5 — Verify cycle time value is present

**Responsible role:** operator

**Instruction:**
Check the ACB System Statistics screen and verify that a cycle time value is present.

**Expected result:**
A cycle time value is visible on the ACB System Statistics screen.

**Screens / Images:**

![artifact_fig_4_5_acb_system_statistics_screen](assets/artifact_fig_4_5_acb_system_statistics_screen.jpeg)

*Locate the cycle time value on the ACB System Statistics screen.*


**Stop or Escalate If:**

* The cycle time value is not present on the ACB System Statistics screen.

---

### Step 6 — Verify tipping station bag counts are present

**Responsible role:** operator

**Instruction:**
Check the ACB System Statistics screen and verify that tipping station bag counts are present.

**Expected result:**
Tipping station bag count information is visible on the ACB System Statistics screen.

**Screens / Images:**

![artifact_fig_4_5_acb_system_statistics_screen](assets/artifact_fig_4_5_acb_system_statistics_screen.jpeg)

*Locate the tipping station bag count information on the ACB System Statistics screen.*


**Stop or Escalate If:**

* The tipping station bag counts are not present on the ACB System Statistics screen.

---

### Step 7 — Record any missing documented metric fields

**Responsible role:** operator

**Instruction:**
Record any documented metric fields that are missing from the ACB System Statistics screen for follow-up.

**Expected result:**
Any missing documented fields are noted for follow-up.

**Screens / Images:**

![artifact_fig_4_5_acb_system_statistics_screen](assets/artifact_fig_4_5_acb_system_statistics_screen.jpeg)

*Use Figure 4-5 as the documented reference when noting any missing metric fields.*


**Stop or Escalate If:**

* One or more documented metric fields are not present on the ACB System Statistics screen.

---

## Success Criteria

* The ACB System Statistics screen is accessed from the ACB System screen.
* The presence of the documented metrics is confirmed: robot faults, system faults, cycle time, and tipping station bag counts.
* Any missing documented metric fields are recorded for follow-up.

## Failure Conditions

* The ACB System Statistics screen cannot be accessed from the ACB System screen.
* One or more documented metric fields are not present on the ACB System Statistics screen.
* The displayed screen cannot be matched to the documented ACB System Statistics screen reference.

## Escalation Guidance

* Escalate if one or more documented metric fields are not present on the ACB System Statistics screen.
* Escalate if the ACB System Statistics screen cannot be accessed or does not match the documented Figure 4-5 reference.
* Do not infer corrective actions from displayed values because the source only documents field presence and screen purpose.

## Missing Details / Known Gaps

* The source does not provide thresholds, normal ranges, or interpretation guidance for the displayed values.
* The source does not provide troubleshooting or corrective actions if a metric field is missing.
* The source does not provide an estimated completion time.
* The source does not specify whether production stop or LOTO is required; these fields remain unknown.
* The source section text in the packet is empty, so grounding relies on the candidate source references, related context records, and artifact retrieval text included in the packet.

## Source Lineage

- Candidate IDs: candidate_operator_verify_acb_system_statistics_metrics_present
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
