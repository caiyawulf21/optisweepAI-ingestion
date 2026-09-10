# Check RMS for Overall System AGV Status to confirm remote availability

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_rms_overall_system_agv_status_remote_availability_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `fleet_system_status` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS / fleet status web UI to open the page titled “Overall System AGV Status” and confirm the page loads and displays the current overall system status content. This is used to verify remote availability of the RMS overview page.

## When To Use

When you need to confirm that the RMS fleet status UI is reachable remotely and that the “Overall System AGV Status” overview page is displaying the current overall system status.

## Source Procedure References

- proc_check_rms_overall_system_agv_status_remote_availability_v1

## Procedure Steps

### Step 1 — Open the RMS / fleet status UI (RMS web UI)

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status web UI (rms_ui).

**Expected result:**
RMS / fleet status UI opens successfully (i.e., you can proceed to navigate within RMS).

---

### Step 2 — Navigate to the “Overall System AGV Status” page

**Responsible role:** L1_support

**Instruction:**
Within RMS, navigate to the page titled “Overall System AGV Status”.

**Expected result:**
The “Overall System AGV Status” page is displayed (page title/header visible).

---

### Step 3 — Verify the page displays the current overall system status content

**Responsible role:** L1_support

**Instruction:**
On the “Overall System AGV Status” page, observe the page content that indicates the current overall system status (the page is described as showing the current status).

**Expected result:**
The “Overall System AGV Status” page loads and displays current overall system status information (not blank/unavailable).

---

## Success Criteria

- RMS / fleet status UI is reachable remotely.
- The “Overall System AGV Status” page loads successfully.
- The “Overall System AGV Status” page displays current overall system status content (not blank/unavailable).

## Failure Conditions

- RMS / fleet status UI cannot be reached remotely.
- “Overall System AGV Status” page does not load.
- “Overall System AGV Status” page content is missing/blank.

## Escalation Guidance

- If RMS is unreachable or the “Overall System AGV Status” content is missing/blank, escalate for remote access/network/service troubleshooting.

## Missing Details / Known Gaps

- The candidate does not provide the exact RMS navigation path/click sequence to reach “Overall System AGV Status” (only the page title is referenced).
- The candidate does not specify which exact fields/indicators on the page represent “current overall system status” beyond the general statement that the page shows current status.
