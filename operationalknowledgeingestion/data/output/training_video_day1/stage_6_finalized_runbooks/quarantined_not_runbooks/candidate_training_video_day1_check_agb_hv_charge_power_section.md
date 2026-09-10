# Check AGB HV charge percentage in the Power section after selecting an AGB

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_agb_hv_charge_percentage_power_section_v1` |
| Title | Check AGB HV charge percentage in the Power section after selecting an AGB |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `wcs_sql`, `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

After selecting the AGB in the OptiSweep/HMI interface, a small “power” section shows the AGB’s HV charge percentage (example: 50%). Use this value to judge whether extended troubleshooting time risks the AGB “dying” (operational concern discussed in the source).

## When To Use

Use when you have selected an AGB in the OptiSweep/HMI interface and you need to quickly assess its HV charge percentage to understand whether an extended troubleshooting window (e.g., ~1–2 hours) is likely to become risky.

## Do Not Use For

* Do not use this procedure as a substitute for resolving the underlying fault condition; it only provides an HV charge percentage awareness check.

## Access Or Tools Needed

* AGB selection access on the OptiSweep/HMI interface shown in the source
* UI element/section labeled “power” that shows “charge percentage of the HV”

## Related Operational Context

* ctx_training_video_agb_hv_power_display_v1
* ctx_training_video_agb_low_charge_operational_risk_v1

## Procedure Steps

### Step 1 — Select the AGB you are working with in the AGB/HMI interface

**Responsible role:** L1_support

**Instruction:**
In the OptiSweep/HMI interface, select the AGB you are working with so that the interface updates to show the AGB’s details.

**Expected result:**
The interface updates for the selected AGB such that a small section labeled “power” is available for reading HV charge percentage.

**Stop or Escalate If:**

* If the HV charge percentage is not displayed after selecting the AGB, stop and escalate for assistance.

---

### Step 2 — Locate the small “power” section for the selected AGB

**Responsible role:** L1_support

**Instruction:**
Find the small UI section labeled “power” that appears for the selected AGB.

**Expected result:**
The small “power” section is located and ready for reading the HV charge percentage.

**Stop or Escalate If:**

* If the HV charge percentage is not displayed after selecting the AGB, stop and escalate for assistance.

---

### Step 3 — Read the HV charge percentage from the “power” section

**Responsible role:** L1_support

**Instruction:**
In the “power” section, read the “charge percentage of the HV” value for the selected AGB.

**Expected result:**
A numeric HV charge percentage is displayed in the “power” section (example from source: 50%).

**Stop or Escalate If:**

* If the HV charge percentage is not displayed after selecting the AGB, stop and escalate for assistance.

---

### Step 4 — Assess operational risk based on the displayed HV charge percentage

**Responsible role:** L1_support

**Instruction:**
Compare the displayed HV charge percentage to the operational concern range discussed in the source (example concern around ~30% / 32% when troubleshooting may take ~1–2 hours).

**Expected result:**
You determine whether the displayed HV charge percentage is in the operationally concerning area discussed by the source (e.g., around 30%/32% for ~1–2 hours of troubleshooting).

**Stop or Escalate If:**

* If the HV charge percentage is not displayed after selecting the AGB, stop and escalate for assistance.

---

## Success Criteria

* After selecting the AGB, the “power” section displays the “charge percentage of the HV” value for that AGB.
* The HV charge percentage is read and used to make an operational risk awareness judgment for the expected troubleshooting duration.

## Failure Conditions

* The “power” section does not appear after selecting the AGB.
* The “power” section appears but does not show the HV charge percentage value.

## Escalation Guidance

* If the HV charge percentage is not displayed after selecting the AGB, stop and escalate for assistance (no alternate UI location/steps are provided in the source).

## Missing Details / Known Gaps

* The source does not specify exact UI navigation steps beyond “select the AGB” (e.g., which panel/tab to click) or the exact numeric thresholds as formal cutoffs; it only provides example concern values (~30%/32%) and timing context (~1–2 hours).

## Source Lineage

- Candidate IDs: candidate_training_video_day1_check_agb_hv_charge_power_section
- Source ID: `training_video_day1`
- Source Type: `training_video`
