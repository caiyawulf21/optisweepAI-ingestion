# Validate OptiSweep is back up after backup migration / planned restart (database, heartbeats, RMS visibility)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_validate_optsweep_back_up_after_backup_migration_planned_restart_v1` |
| Title | Validate OptiSweep is back up after backup migration / planned restart (database, heartbeats, RMS visibility) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `gateway_health` |
| Access Surface | `wcs_sql`, `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy`, `shutdown_or_dwell_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

After a primary failure with migration to a backup or during a planned restart, validate OptiSweep recovery by confirming the database is up, verifying heartbeats are present, restarting OptiSweep if heartbeats are missing, and confirming RMS is visible.

## When To Use

Use after migrating to a backup (primary failed) or during planned restarts to confirm the system is back and operational by checking database availability, heartbeat presence, and RMS visibility.

## Safety And Operational Notes

* If RMS was shut down, it may come up with an E-stop; release the E-stop or have site release the E-stop.

## Access Or Tools Needed

* OptiSweep restart capability (as described in the source)
* Access to the interface that shows database-up status
* Access to the interface that shows heartbeats
* Access to the interface that shows RMS visibility

## Related Operational Context

* ctx_training_video_restart_validation_checks_v1

## Visual References

![artifact_training_video_training_video_day2_0049_check_to_make_sure_that_tippers_primary_03_13_10_000](assets/4fbe27ac029a845c.jpg)

*Frame showing the guidance: check that tippers are getting heartbeats; if heartbeats are flat lines, restart OptiSweep.*

![artifact_training_video_training_video_day2_0051_you_know_this_is_like_you_primary_03_13_45_500](assets/594db6d378d1227e.jpg)

*Frame showing the guidance: if heartbeats are flat lined, restart OptiSweep (includes mention of checking connections and the OptiSweep service).*

## Procedure Steps

### Step 1 — Confirm the database is up after backup migration / planned restart

**Responsible role:** L2_support

**Instruction:**
On the live system, check the interface that indicates database availability and confirm the database is up following the backup migration or planned restart.

**Expected result:**
Database is up (database availability indicator shows up/healthy).

**Stop or Escalate If:**

* If the database is not up, escalate for deeper troubleshooting.

---

### Step 2 — Check for heartbeats (tippers heartbeats)

**Responsible role:** L2_support

**Instruction:**
On the live system, check the heartbeat indicator/status for tippers and confirm heartbeats are present (not flat lined).

**Expected result:**
Heartbeats are present (not flat lined).

**Stop or Escalate If:**

* If heartbeats are flat lined (missing), proceed to restart OptiSweep in the next step.

---

### Step 3 — Restart OptiSweep if heartbeats are missing / flat lined

**Responsible role:** L2_support

**Instruction:**
If heartbeats are flat lined/missing, restart OptiSweep using the restart capability available to you, then re-check heartbeats as needed before proceeding to RMS visibility.

**Expected result:**
After restart, heartbeats are no longer flat lined (heartbeats become present).

**Stop or Escalate If:**

* If heartbeats remain missing after restarting OptiSweep, escalate for deeper troubleshooting.

---

### Step 4 — Confirm RMS is visible after restart / if heartbeats were already present

**Responsible role:** L2_support

**Instruction:**
After restart (or if heartbeats were already present), check RMS visibility in the RMS interface and confirm RMS can be seen.

**Expected result:**
RMS is visible (RMS visibility/status indicates it is present).

**Stop or Escalate If:**

* If RMS cannot be seen after the checks, escalate for further investigation.

---

## Success Criteria

* Database is up after the backup migration / planned restart.
* Heartbeats are present (not flat lined).
* RMS is visible after restart/migration sequence.

## Failure Conditions

* Database is not up.
* Heartbeats are flat lined/missing.
* Heartbeats remain missing after restarting OptiSweep.
* RMS cannot be seen after the checks.

## Escalation Guidance

* If the database is not up, or heartbeats remain missing after restarting OptiSweep, escalate for deeper troubleshooting.
* If RMS cannot be seen after the checks, escalate for further investigation.

## Missing Details / Known Gaps

* The source segment does not name specific live UI screens/controls for the database-up status, heartbeat indicator, or RMS visibility; only the validation sequence is described.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_restart_validation_checks_backup_migration
- Source ID: `training_video_day2`
- Source Type: `training_video`
