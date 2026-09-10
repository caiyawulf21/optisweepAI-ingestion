# Verify Service Presence/Running State in Windows Services When Service Appears Gone

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_service_presence_running_state_windows_services_v1` |
| Title | Verify Service Presence/Running State in Windows Services When Service Appears Gone |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `windows_service_or_event_log`, `gateway_health` |
| Access Surface | `event_viewer` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `service_crash_or_restart` |
| Validation Status | `needs_smeme_review` |
| Merge Status | `source_finalized` |

## Summary

When a crash/service stop is suspected and logs may be silent, verify whether the relevant service is actually running (or not present/running) by checking the Windows Services list on the Windows host where the gateway/service runs.

## When To Use

Use when the service appears to be gone during a suspected crash/service stop window and log visibility is limited or silent, so you need an OS-level confirmation of whether the service is running.

## Do Not Use For

* Do not use this procedure as a recovery/change procedure (it is diagnostic only).

## Safety And Operational Notes

* This procedure is diagnostic only; do not perform mutating changes unless a separate recovery procedure is available.

## Access Or Tools Needed

* Windows Services console/view
* Access to the Windows host running the gateway/service

## Related Operational Context

* ctx_training_video_windows_services_visibility_v1
* ctx_training_video_service_stop_silent_logs_v1

## Visual References

![artifact_training_video_training_video_day2_0044_probably_understand_this_so_if_the_primary_03_07_17_500](assets/0f6cee71bf142dce.jpg)

*Training frame showing the discussion: check Windows service services; there are ~10 services; service must stop; logs may be silent.*

## Procedure Steps

### Step 1 — Open Windows Services view on the host where the gateway/service runs

**Responsible role:** L2_support

**Instruction:**
On the Windows host where the gateway/service runs, open the Windows Services view (the OS-level place to check service state).

**Expected result:**
You can view the list of Windows services (the source notes there are about 10 services) so you can determine whether the expected service is running vs not running.

**Stop or Escalate If:**

* If you cannot access the Windows host or the Services list, stop and escalate for access/host guidance.

---

### Step 2 — Review the service list and determine whether the expected service is running

**Responsible role:** L2_support

**Instruction:**
In the Windows Services list, review the entries (source notes there are ~10 services) and identify whether the expected service is running vs not running (i.e., effectively “gone” during the period).

**Expected result:**
You determine from the Windows Services list whether the expected service is running or not running, matching the source expectation that a crash/service stop can make logs silent and the service appear gone.

**Stop or Escalate If:**

* If it is unclear which of the ~10 services is the one in question, stop and escalate for guidance on the specific service name to check.

---

### Step 3 — Use the Windows Services state as evidence to guide further investigation (diagnostic only)

**Responsible role:** L2_support

**Instruction:**
If the expected service is not running, treat that as evidence the service likely stopped during the silent period described in the source, and proceed with further investigation using the appropriate next diagnostic steps (outside the scope of this candidate). If the service is running, use that to narrow the hypothesis away from a stopped service.

**Expected result:**
Your conclusion about whether the service is running vs not running is consistent with the source’s scenario where logs may be silent and the service may appear gone.

**Stop or Escalate If:**

* Do not perform mutating changes as part of this diagnostic; if recovery is needed, use a separate recovery procedure.

---

## Success Criteria

* From the Windows Services list, you can state whether the expected service is running or not running during the suspected silent period.

## Failure Conditions

* Expected service is not running (service appears gone) during the suspected crash/service stop window.

## Escalation Guidance

* If you cannot identify which specific service among the ~10 services is the one in question, escalate for guidance on the exact Windows service name to check.

## Missing Details / Known Gaps

* The source does not name the specific Windows service name(s) to check; the procedure therefore cannot specify which of the ~10 services is the expected one.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_check_windows_services_service_running
- Source ID: `training_video_day2`
- Source Type: `training_video`
