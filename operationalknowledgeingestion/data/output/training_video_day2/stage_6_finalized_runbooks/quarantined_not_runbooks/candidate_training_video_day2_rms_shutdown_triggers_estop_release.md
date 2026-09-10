# Handle E-stop condition after RMS shutdown (release E-stop / site release)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_handle_estop_condition_after_rms_shutdown_release_estop_v1` |
| Title | Handle E-stop condition after RMS shutdown (release E-stop / site release) |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `e_stop_or_safety_stop`, `fleet_system_status` |
| Access Surface | `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `site_stoppage` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

If RMS is shut down and an E-stop appears, the E-stop must be released (either by the support team or by site release) so the system can resume.

## When To Use

Use when RMS has been shut down and the system comes up with an E-stop condition.

## Safety And Operational Notes

* Treat the E-stop as a safety condition that must be released before resuming normal operation.

## Access Or Tools Needed

* Access to the E-stop release control/indicator (as described in the source context)
* Ability to coordinate with site for E-stop release if required

## Related Operational Context

* ctx_training_video_rms_estop_relationship_v1

## Procedure Steps

### Step 1 — Confirm E-stop is present after RMS shutdown

**Responsible role:** L2_support

**Instruction:**
On the live RMS-related controls/indication, confirm that an E-stop is currently present following the RMS shutdown event.

**Expected result:**
An E-stop indication is present after RMS shutdown.

**Stop or Escalate If:**

* If you cannot confirm the E-stop condition on the live controls/indicator, stop and escalate for further safety/system investigation.

---

### Step 2 — Release the E-stop (or coordinate site release)

**Responsible role:** L2_support

**Instruction:**
Release the E-stop. If the source indicates the site performs the release, coordinate with site to release the E-stop.

**Expected result:**
E-stop is released after RMS shutdown so the system is no longer in the E-stop condition.

**Stop or Escalate If:**

* If the E-stop cannot be released, escalate to appropriate support for further safety/system investigation.

---

## Success Criteria

* E-stop is released after RMS shutdown and the system is no longer in the E-stop condition.

## Failure Conditions

* E-stop remains active after attempting release.

## Escalation Guidance

* If the E-stop cannot be released, escalate to appropriate support for further safety/system investigation.

## Missing Details / Known Gaps

* The source segment does not specify the exact E-stop release control/indicator name(s) or the exact UI path/control labels used to release the E-stop.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_rms_shutdown_triggers_estop_release
- Source ID: `training_video_day2`
- Source Type: `training_video`
