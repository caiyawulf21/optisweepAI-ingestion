# Query DB logs for errors/fatals using database scripts (select top 100 + filter) to support troubleshooting

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_query_db_logs_errors_fatals_v1` |
| Title | Query DB logs for errors/fatals using database scripts (select top 100 + filter) to support troubleshooting |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `windows_service_or_event_log`, `wcs_api_responsiveness` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use database-resident logs and database scripts to retrieve recent log entries limited to “errors and fatals only,” then use the resulting records as evidence for support diagnosis and subsequent troubleshooting/resolution steps.

## When To Use

When you need evidence from database-resident server logs to identify relevant error/fatal patterns for troubleshooting and support handoff.

## Access Or Tools Needed

* Database scripts used for support
* DB logs in the DB database (as referenced by the source)
* Server log view that shows “right click logs” (as referenced by the source)

## Related Operational Context

* ctx_training_video_support_database_logs_v1
* ctx_training_video_server_logs_errors_fatals_v1

## Procedure Steps

### Step 1 — Use the database scripts and server log view to inspect DB logs for support

**Responsible role:** L2_support

**Instruction:**
Using the database scripts referenced by the support workflow, open/locate the server log view described as “right click logs,” where the logs are stored in the DB database.

**Expected result:**
You have access to a server log view backed by DB logs that can be queried/filtered for support troubleshooting.

---

### Step 2 — Limit results to recent entries using a “select top 100” query pattern

**Responsible role:** L2_support

**Instruction:**
Run the database query pattern described as “select top 100 and filter if I want something” to limit results to recent entries.

**Expected result:**
A result set/list of log records is returned with a “top 100” style limit (recent entries).

---

### Step 3 — Apply filtering to narrow results to relevant entries

**Responsible role:** L2_support

**Instruction:**
Apply the described filter step (“filter if I want something”) to narrow the “top 100” results to the relevant entries you are investigating.

**Expected result:**
The result set is narrowed to only the entries matching your chosen filter criteria.

---

### Step 4 — Confirm the log view is restricted to “errors and fatals only”

**Responsible role:** L2_support

**Instruction:**
Verify that the log output you are using is restricted to “errors and fatals only,” consistent with the described server log view behavior.

**Expected result:**
The displayed/returned log records are limited to errors and fatals only.

**Stop or Escalate If:**

* If the logs are not restricted to errors/fatals, adjust the query/filter so only errors and fatals are shown.

---

### Step 5 — Use the resulting error/fatal records as evidence for diagnosis and next steps

**Responsible role:** L2_support

**Instruction:**
Use the filtered error/fatal records returned from the DB logs as the evidence set to match against the expected error type/patterns and to support subsequent diagnosis and resolution steps.

**Expected result:**
You have a filtered list of recent error/fatal log entries that can be used as evidence for the troubleshooting workflow.

**Stop or Escalate If:**

* If no relevant error/fatal records appear, stop and escalate to the support handoff/RCA process described in the source.

---

## Success Criteria

* A filtered list of recent DB log entries is produced that is restricted to “errors and fatals only.”
* The resulting records are usable as evidence for matching an expected error type/pattern and supporting subsequent diagnosis/resolution steps.

## Failure Conditions

* The log output includes non-error/non-fatal activity (not restricted to “errors and fatals only”).
* No relevant error/fatal records appear for the investigation, requiring escalation.

## Escalation Guidance

* If no relevant error/fatal records appear, stop and escalate to the support handoff/RCA process described in the source.

## Missing Details / Known Gaps

* The packet does not provide explicit DB name, table name, or exact SQL/script text beyond the pattern “select top 100 and filter.”
* The packet does not provide the exact UI steps/controls for the “right click logs” server view (only that it exists and is used).
* The packet does not specify the exact filter criteria/fields used to narrow results beyond the general “filter if I want something” guidance.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_query_db_logs_errors_fatals
- Source ID: `training_video_day2`
- Source Type: `training_video`
