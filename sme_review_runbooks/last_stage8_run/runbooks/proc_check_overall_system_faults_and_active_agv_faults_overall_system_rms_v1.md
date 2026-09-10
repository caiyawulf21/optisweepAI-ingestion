# Check Overall System Faults and Active AGV Faults on the Overall System RMS Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `fleet_system_status`, `agv_active_errors` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Perform a first-pass live check on the RMS / fleet status UI (Geek+ RMS web page) to determine whether the system has any system faults (left side) and whether any AGVs have active faults (right side).

## When To Use

Use when a caller reports a potential fleet/system issue and you need a quick overview of (1) system faults and (2) any active AGV faults visible on the Overall System RMS page.

## Source Procedure References

- proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1

## Procedure Steps

### Step 1 — Open the Overall System RMS page in the RMS / fleet status UI

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (Geek+ RMS web page) for the site and navigate to the Overall System RMS page.

**Expected result:**
The Overall System RMS page loads and shows the two fault areas: system faults on the left and active AGV faults on the right.

---

### Step 2 — Check the left-side “system faults” area

**Responsible role:** L1_support

**Instruction:**
On the Overall System RMS page, look at the left-side “system faults” area and determine whether any system faults are listed/present.

**Expected result:**
You can state whether the left-side “system faults” area shows one or more fault entries or is empty/not showing faults at the time of the check.

---

### Step 3 — Check the right-side “active AGV faults” area

**Responsible role:** L1_support

**Instruction:**
On the same Overall System RMS page, look at the right-side “active AGV faults” area and determine whether any active AGV faults are listed/present.

**Expected result:**
You can state whether the right-side “active AGV faults” area shows one or more fault entries or is empty/not showing faults at the time of the check.

---

### Step 4 — Report the displayed fault indications (or confirm none are displayed)

**Responsible role:** L1_support

**Instruction:**
If the left “system faults” area and/or the right “active AGV faults” area shows entries, report those fault indications to support. If both areas are empty/not showing faults, report that no system faults/active AGV faults are currently displayed on this page.

**Expected result:**
A clear statement is provided indicating whether system faults are present on the left and whether active AGV faults are present on the right at the time of the check.

---

## Success Criteria

- You verify the presence/absence of system faults in the left-side “system faults” area on the Overall System RMS page.
- You verify the presence/absence of active AGV faults in the right-side “active AGV faults” area on the Overall System RMS page.
- You report whether each side shows fault entries or is empty/not showing faults.

## Failure Conditions

- Left-side “system faults” area lists one or more system faults.
- Right-side “active AGV faults” area lists one or more active AGV faults.
- Overall System RMS page cannot be reached or does not load the content needed to view the left/right fault areas.

## Escalation Guidance

- If the RMS page cannot be reached or does not load the Overall System RMS content needed to view system faults (left) and active AGV faults (right), escalate/continue troubleshooting.
- If the caller cannot share screen, request a viewable screenshot or ask them to navigate to the Overall System RMS page so the left/right fault areas can be verified.

## Missing Details / Known Gaps

- Exact navigation path/click sequence to reach the Overall System RMS page within the RMS / fleet status UI is not provided in the packet; only the expected page layout (system faults left, active AGV faults right) is specified.
