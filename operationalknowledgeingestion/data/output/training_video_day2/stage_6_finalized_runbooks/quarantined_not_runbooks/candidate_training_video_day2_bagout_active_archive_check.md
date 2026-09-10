# Check Bag Out Activity Tracking in Sorter Sweeper Database (Active Bag Out vs Bag Out Archive)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_bag_out_activity_tracking_sorter_sweeper_db_active_vs_archive_v1` |
| Title | Check Bag Out Activity Tracking in Sorter Sweeper Database (Active Bag Out vs Bag Out Archive) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `bag_out_or_closeout_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `bag_out_stuck`, `sort_lifecycle_stuck`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify that bag out lifecycle events are represented correctly in the Sorter Sweeper Database: when a bag out closes out as requested, open shoots are closed and totes with items are marked for exchange with an entry created in the active bag out model; after the tote is tipped, the record is archived to the bag out archive.

## When To Use

Use when you need to confirm that bag out closeout and tote tipping are reflected in the Sorter Sweeper Database as active bag out entries first, then archived bag out records after tipping.

## Access Or Tools Needed

* SSMS
* Sorter Sweeper Database (active bag out and bag out archive tables/models as named in the source)

## Related Operational Context

* ctx_training_video_exchange_and_bagout_models_v1

## Visual References

![artifact_training_video_training_video_day2_0025_yeah_you_know_it_s_it_primary_02_21_32_000](assets/dede127121710b0e.jpg)

*Transcript frame describing bag out lifecycle tracking: active bag out entry created when bag out closes out as requested; once tote is tipped, record is archived to bag out.*

## Procedure Steps

### Step 1 — Open the Sorter Sweeper Database view for active bag out and bag out archive tracking models

**Responsible role:** L2_support

**Instruction:**
In SSMS, open the Sorter Sweeper Database views/tables/models for the bag out tracking surfaces referenced in the segment: the active bag out model and the bag out archive model.

**Expected result:**
You can view both the active bag out tracking entries and the bag out archive tracking records in the Sorter Sweeper Database.

---

### Step 2 — Validate active bag out entries created at bag out closeout (open shoots closed; totes with items marked for exchange)

**Responsible role:** L2_support

**Instruction:**
Locate active bag out entries and confirm that when a bag out closes out as requested: (1) open shoots are closed, and (2) any tote with an item is marked for an exchange, with an entry created in the active bag out model.

**Expected result:**
For the bag out closeout you are validating, there are corresponding entries in the active bag out model indicating totes with items are marked for exchange (active bag out contains current bag-out-related tote exchange entries until the tote is tipped).

**Stop or Escalate If:**

* If bag out closeout does not create active bag out entries, escalate for investigation of the bag out lifecycle data flow described by the source.

---

### Step 3 — Validate archiving after tote is tipped (active -> bag out archive)

**Responsible role:** L2_support

**Instruction:**
Identify a tote that has been tipped and confirm that the corresponding record is archived to the bag out archive (i.e., moved from active bag out tracking to the archived bag out record).

**Expected result:**
For the tipped tote under review, the record appears in the bag out archive model after tipping, consistent with the behavior that active bag out retains entries until the tote is tipped and then archives them.

**Stop or Escalate If:**

* If tipped totes do not result in archiving, escalate for investigation of the bag out lifecycle data flow described by the source.

---

### Step 4 — Confirm active vs archived tracking difference matches expected bag out lifecycle behavior

**Responsible role:** L2_support

**Instruction:**
Confirm that the difference between active tracking and archived tracking matches the source’s described behavior for the bag out lifecycle you validated.

**Expected result:**
Active bag out shows current bag-out-related tote exchange entries prior to tipping, and the bag out archive shows the corresponding records after tipping.

---

## Success Criteria

* A bag out closeout as requested results in an entry in the active bag out model for totes with items marked for exchange.
* After the tote is tipped, the corresponding record appears in the bag out archive model (archived from active bag out tracking).

## Failure Conditions

* Bag out closeout does not create active bag out entries.
* Tipped totes do not result in archiving to the bag out archive.

## Escalation Guidance

* If active bag out entries are missing at bag out closeout, or if tipped totes do not archive, escalate for investigation of the bag out lifecycle data flow described by the source.

## Missing Details / Known Gaps

* The packet does not name the exact SSMS table/view names for the active bag out model and bag out archive model; it only references them generically as “active bag out” and “bag out archive.”

## Source Lineage

- Candidate IDs: candidate_training_video_day2_bagout_active_archive_check
- Source ID: `training_video_day2`
- Source Type: `training_video`
