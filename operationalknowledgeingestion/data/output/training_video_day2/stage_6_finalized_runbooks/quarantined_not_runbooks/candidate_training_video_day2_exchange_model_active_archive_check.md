# Check Exchange Activity Tracking in Sorter Sweeper Database (Active Exchange vs Exchange Activity)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_exchange_activity_tracking_in_sorter_sweeper_database_active_exchange_vs_exchange_activity_v1` |
| Title | Check Exchange Activity Tracking in Sorter Sweeper Database (Active Exchange vs Exchange Activity) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sorter_item_or_scan_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `sort_lifecycle_stuck`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify that chute exchange lifecycle is represented correctly in the Sorter Sweeper Database: when a chute closes, an active exchange record is created in the active exchange model; when an empty tote replaces the chute, the exchange is closed and archived to the exchange activity table, while the active exchange list remains limited to a few current items.

## When To Use

Use when you need to confirm that chute exchange events are flowing into the Sorter Sweeper Database correctly—specifically that chute-close creates an active exchange record, and that empty-tote replacement closes and archives the exchange to the exchange activity archive.

## Access Or Tools Needed

* SSMS
* Sorter Sweeper Database (exchange active exchange model and exchange activity archive tables/models as named in the source)

## Related Operational Context

* ctx_training_video_exchange_and_bagout_models_v1

## Visual References

![artifact_training_video_training_video_day2_0025_yeah_you_know_it_s_it_primary_02_21_32_000](assets/dede127121710b0e.jpg)

*Transcript evidence for exchange lifecycle: chute close creates active exchange; empty tote replacement closes and archives to exchange activity; active list remains small.*

## Procedure Steps

### Step 1 — Open the Sorter Sweeper Database exchange tracking models (active exchange model and exchange activity archive)

**Responsible role:** L2_support

**Instruction:**
In SSMS, open the Sorter Sweeper Database view(s)/table(s) for the exchange tracking models referenced in the segment: the active exchange model and the exchange activity archive table/model.

**Expected result:**
You can view both (1) the active exchange model records and (2) the exchange activity archive records in the Sorter Sweeper Database.

---

### Step 2 — Confirm active exchange records are created when a chute is closed

**Responsible role:** L2_support

**Instruction:**
Locate active exchange records in the active exchange model and confirm that an active exchange is created for recently closed chutes (i.e., active exchange entries corresponding to chute-close events).

**Expected result:**
Active exchange records exist for currently relevant chute exchanges, including entries corresponding to recently closed chutes.

**Stop or Escalate If:**

* If chute-close events do not create active exchange records, escalate for deeper investigation of the exchange lifecycle data flow described by the source.

---

### Step 3 — Confirm exchange closure and archiving when an empty tote replaces the chute

**Responsible role:** L2_support

**Instruction:**
Identify the event where an empty tote replaces the chute, then confirm that the exchange is closed (no longer only present in the active exchange list) and that the corresponding record exists in the exchange activity archive table/model.

**Expected result:**
When an empty tote replaces a chute, the exchange record is closed and present in the exchange activity archive (and is no longer only in the active exchange list).

**Stop or Escalate If:**

* If empty-tote replacement does not result in closure/archiving, escalate for deeper investigation of the exchange lifecycle data flow described by the source.

---

### Step 4 — Verify active exchange list remains small while older exchanges move to the archive

**Responsible role:** L2_support

**Instruction:**
Review the active exchange model and confirm it remains limited to a few current items, while older exchange records are moved into the larger exchange activity archive table/model.

**Expected result:**
The active exchange list contains only a few current exchange items; older exchanges are found in the exchange activity archive.

---

## Success Criteria

* Active exchange records exist for currently relevant chute exchanges, including entries corresponding to chute-close events.
* When an empty tote replaces a chute, the exchange is closed and the corresponding record is present in the exchange activity archive.
* Active exchange list remains limited to a few current items while older exchanges move to the larger archive table/model.

## Failure Conditions

* Chute-close events do not create active exchange records.
* Empty-tote replacement does not close and archive the exchange to exchange activity.
* Active exchange list contains older exchanges that should have been archived.

## Escalation Guidance

* If chute-close events do not create active exchange records, or if empty-tote replacement does not result in closure/archiving, escalate for deeper investigation of the exchange lifecycle data flow described by the source.

## Missing Details / Known Gaps

* The packet does not name the exact SSMS table/view names or columns for the active exchange model and exchange activity archive; it only describes them conceptually as 'active exchange model' and 'exchange activity' archive.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_exchange_model_active_archive_check
- Source ID: `training_video_day2`
- Source Type: `training_video`
