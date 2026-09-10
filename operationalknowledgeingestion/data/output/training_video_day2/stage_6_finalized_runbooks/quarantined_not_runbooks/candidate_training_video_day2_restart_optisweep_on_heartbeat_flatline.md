# Restart OptiSweep service when heartbeat is flat-lined (Ignition/WCS startup delay)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_restart_optsweep_service_when_heartbeat_flatlined_v1` |
| Title | Restart OptiSweep service when heartbeat is flat-lined (Ignition/WCS startup delay) |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `gateway_health`, `wcs_api_responsiveness` |
| Access Surface | `event_viewer` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `gateway_unhealthy`, `service_crash_or_restart` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

If the heartbeat indicator is flat-lined, the source associates it with an unplanned restart condition where Ignition likely came up later than WCS/AGV (or takes longer on startup). In that case, restart the OptiSweep Windows service and confirm the heartbeat is no longer flat-lined.

## When To Use

Use when the OptiSweep heartbeat indicator is flat-lined and you need to restore OptiSweep availability by restarting the OptiSweep service, per the source’s guidance that Ignition startup timing can delay OptiSweep and lead to this condition.

## Access Or Tools Needed

* Windows Services (to restart/verify OptiSweep service status as shown in the source screenshot)
* Heartbeat indicator (as referenced by the source)

## Related Operational Context

* ctx_training_video_heartbeat_flatline_restart_reference_v1
* ctx_training_video_ignition_startup_timing_reference_v1
* ctx_training_video_optisweep_windows_service_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0051_you_know_this_is_like_you_primary_03_13_45_500](assets/594db6d378d1227e.jpg)

*Frame showing the guidance: 'Unplanned restart If the heartbeat is flat lined' and the Windows Services list with an 'OptiSweep' service entry (Status/Startup Type columns).*

## Procedure Steps

### Step 1 — Check the heartbeat indicator and determine whether it is flat-lined

**Responsible role:** L2_support

**Instruction:**
On the live system, check the heartbeat indicator referenced by the source and determine whether it is flat-lined (vs. not flat-lined).

**Expected result:**
The heartbeat indicator is identified as flat-lined.

---

### Step 2 — If heartbeat is flat-lined, treat as unplanned restart condition related to Ignition startup timing

**Responsible role:** L2_support

**Instruction:**
If the heartbeat is flat-lined, apply the source’s association: Ignition likely came up later than WCS/AGV (and Ignition may take longer on startup).

**Expected result:**
You confirm the condition matches the source’s 'Igniton ... came up later then wcs' / delayed-start explanation for the flat-lined heartbeat.

---

### Step 3 — Restart the OptiSweep Windows service

**Responsible role:** L2_support

**Instruction:**
In Windows Services, restart the service named "OptiSweep" (as shown in the source’s Services list frame).

**Expected result:**
The OptiSweep service restart is initiated/completed (service management action performed on the 'OptiSweep' entry).

---

### Step 4 — Re-check the heartbeat indicator to confirm it is no longer flat-lined

**Responsible role:** L2_support

**Instruction:**
After restarting OptiSweep, re-check the heartbeat indicator and confirm it is no longer flat-lined.

**Expected result:**
The heartbeat indicator is no longer flat-lined.

**Stop or Escalate If:**

* If the heartbeat remains flat-lined after restarting OptiSweep, stop and escalate for deeper troubleshooting (source provides no further steps).

---

## Success Criteria

* OptiSweep has been restarted.
* Heartbeat indicator is no longer flat-lined after the restart.

## Failure Conditions

* Heartbeat indicator remains flat-lined after restarting OptiSweep.

## Escalation Guidance

* If the heartbeat remains flat-lined after restarting OptiSweep, stop and escalate for deeper troubleshooting; the source does not provide additional steps.

## Missing Details / Known Gaps

* The source does not specify the exact Windows Services UI clicks/controls (e.g., which context-menu option) beyond the instruction to restart the OptiSweep service.
* The source does not provide the exact location/label of the heartbeat indicator UI element; it only references checking heartbeats and flat-lined heartbeat behavior.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_restart_optisweep_on_heartbeat_flatline
- Source ID: `training_video_day2`
- Source Type: `training_video`
