# Use Sorter Sweeper Database Tipper/Tag Logging to Diagnose Tipper Departure Issues

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_sorter_sweeper_database_tipper_tag_logging_to_diagnose_tipper_departure_issues_v1` |
| Title | Use Sorter Sweeper Database Tipper/Tag Logging to Diagnose Tipper Departure Issues |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Sorter Sweeper Database “Tipper/Tag Logging” (tipper departure activity model records) to review tag read/write logging for AGV send-away events from tipper-related drop-off locations (DropOffSorter and DropOffHospital). For the relevant send-away record(s), check the recorded Tote, Tag path, and any fault code to narrow down the tipper departure issue.

## When To Use

When an AGV is reported to have a tipper departure issue and you need to narrow down what happened during the send-away event by reviewing the recorded tag read/write logging and the tipper departure activity model record fields (Tote, Tag path, fault code).

## Access Or Tools Needed

* Sorter Sweeper Database (Tipper/Tag Logging / Tipper departure activity model records view)

## Related Operational Context

* ctx_training_video_tag_read_write_logs_v1
* ctx_training_video_tipper_departure_activity_model_records_v1
* ctx_training_video_departure_record_fields_v1
* ctx_training_video_tipper_issue_narrowing_logs_v1

## Visual References

![artifact_training_video_training_video_day2_0023_the_tag_read_and_tag_write_primary_02_01_38_500](assets/727226e69bc5bd42.jpg)

*Sorter Sweeper Database “Tipper/Tag Logging” showing tipper departure activity model records and the fields described for send-away events (DropOffSorter/DropOffHospital, Tote, Tag path, fault code).*

## Procedure Steps

### Step 1 — Open the Sorter Sweeper Database “Tipper/Tag Logging” / “Tipper departure activity model records” view

**Responsible role:** L2_support

**Instruction:**
Open the Sorter Sweeper Database view/model shown as “Tipper/Tag Logging” / “Tipper departure activity model records.”

**Expected result:**
You are viewing the “Tipper/Tag Logging” / tipper departure activity model records screen where send-away events are logged with tag read/write logging.

---

### Step 2 — Filter/locate records for the send-away time window (DropOffSorter and DropOffHospital)

**Responsible role:** L2_support

**Instruction:**
Filter or locate the tipper departure activity model records corresponding to the time window when an AGV was sent away from the tipper, including send-away events for “DropOffSorter” and “DropOffHospital.”

**Expected result:**
You have one or more tipper departure activity model record(s) for the relevant send-away event(s) from DropOffSorter and/or DropOffHospital within the reported time window.

---

### Step 3 — Check the recorded Tote, Tag path, and any fault code for the send-away record(s)

**Responsible role:** L2_support

**Instruction:**
For the relevant send-away record(s), check the recorded fields: “Tote,” “Tag path,” and any fault code.

**Expected result:**
For each selected send-away record, you can see the Tote value, the Tag path value, and whether a fault code is recorded for that send-away event.

---

### Step 4 — Use presence/absence of a fault code to narrow down the tipper issue

**Responsible role:** L2_support

**Instruction:**
Review whether the record includes a fault code for the send-away event; use the presence/absence of a fault code to help narrow down the tipper issue.

**Expected result:**
You determine whether the send-away record(s) include a fault code and use that to narrow down the tipper departure issue.

**Stop or Escalate If:**

* Escalate if the tag read/write logs do not contain the expected send-away record details (tote/tag path/fault code) for the time of the reported tipper issue.

---

### Step 5 — Stop and escalate if the expected send-away record details are missing

**Responsible role:** L2_support

**Instruction:**
If the records do not show the expected send-away event details (tote/tag path/fault code) for the time of the issue, stop and escalate for deeper investigation.

**Expected result:**
You stop the current narrowing attempt and escalate because the required send-away record details are not present for the reported time window.

**Stop or Escalate If:**

* Tag read/write logs do not contain the expected send-away record details (tote/tag path/fault code) for the time of the reported tipper issue.

---

## Success Criteria

* You locate tipper departure activity model record(s) for AGV send-away events from DropOffSorter and/or DropOffHospital within the reported time window.
* For the selected record(s), you can observe Tote, Tag path, and whether a fault code is recorded.
* You use fault code presence/absence to narrow down the tipper departure issue, or you escalate when the expected record details are missing.

## Failure Conditions

* No send-away records are found for DropOffSorter/DropOffHospital in the reported time window.
* Selected send-away record(s) do not show Tote, Tag path, and/or fault code details needed for narrowing down the issue.

## Escalation Guidance

* Escalate for deeper investigation if the tag read/write logs do not contain the expected send-away record details (tote/tag path/fault code) for the time of the reported tipper issue.

## Missing Details / Known Gaps

* The source does not provide explicit UI navigation steps (e.g., exact clicks/menus) to reach the “Tipper/Tag Logging” view; only the view/model name is provided.
* The source does not specify the exact filter controls or query fields to use for the time window; it only states to filter/locate records for the send-away time window.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_tag_read_write_logs_tipper_departure
- Source ID: `training_video_day2`
- Source Type: `training_video`
