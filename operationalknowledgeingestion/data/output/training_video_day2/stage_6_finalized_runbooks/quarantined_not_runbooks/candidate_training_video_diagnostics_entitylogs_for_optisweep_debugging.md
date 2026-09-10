# Use WCS EntityLogs (DeveloperLogs) to find OptiSweep application logging evidence for debugging

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_wcs_entitylogs_developerlogs_v1` |
| Title | Use WCS EntityLogs (DeveloperLogs) to find OptiSweep application logging evidence for debugging |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the WCS Entity Logs database (specifically the DeveloperLogs table/model) to locate OptiSweep logging records and use the recorded log attributes (log level, code area/part of code, and line of code) as evidence for debugging.

## When To Use

When you need to find OptiSweep application logging evidence in the WCS Entity Logs database to support debugging, and you want to use the log’s recorded attributes (log level, code area/part of code, and line of code) to pinpoint where the error originated.

## Do Not Use For

* Do not use this procedure as the only step when EntityLogs/DeveloperLogs is missing or contains no relevant OptiSweep entries; escalate to deeper WCS/OptiSweep database support instead.

## Access Or Tools Needed

* SSMS
* WCS SQL Server connection
* EntityLogs database
* DeveloperLogs table/model

## Related Operational Context

* ctx_training_video_optisweep_database_overview_v1
* ctx_training_video_entity_logs_logging_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0008_we_use_for_this_database_when_primary_00_11_14_000](assets/f7783ed9b4087772.jpg)

*Frame showing that OptiSweep only utilizes WCS Entity Logs for logging and that logs include level, code area/part of code, and line of code; also references DeveloperLogs.*

## Procedure Steps

### Step 1 — Open SSMS and connect to the WCS SQL Server database that contains EntityLogs

**Responsible role:** L2_support

**Instruction:**
Using SSMS, connect to the WCS SQL Server instance that contains the EntityLogs database (EntityLogs is within Fortna’s WCS).

**Expected result:**
SSMS is connected to the WCS SQL Server instance and you can view/select the EntityLogs database.

**Stop or Escalate If:**

* EntityLogs/DeveloperLogs is not present in the connected WCS SQL Server environment

---

### Step 2 — Select EntityLogs and locate the DeveloperLogs table/model

**Responsible role:** L2_support

**Instruction:**
In SSMS, select the EntityLogs database and locate the DeveloperLogs table/model referenced in the source.

**Expected result:**
DeveloperLogs table/model is found within the EntityLogs database.

**Stop or Escalate If:**

* EntityLogs/DeveloperLogs is not present

---

### Step 3 — Review OptiSweep-related log entries and extract debugging attributes (level, code area, line of code)

**Responsible role:** L2_support

**Instruction:**
Query or browse DeveloperLogs entries for OptiSweep-related errors, and extract the fields the source says are useful for debugging: log level, what part of the code it came from (code area/part of code), and the line of the code.

**Expected result:**
You have one or more OptiSweep logging records from DeveloperLogs with values for: (1) log level, (2) code area/part of code, and (3) line of code.

**Stop or Escalate If:**

* EntityLogs/DeveloperLogs is present but contains no relevant OptiSweep entries

---

### Step 4 — Use the log evidence to explain where the error occurred (based on logging attributes)

**Responsible role:** L2_support

**Instruction:**
Based on the extracted logging attributes from the DeveloperLogs record(s), explain what part of the code produced the error and where it occurred using the recorded code area/part of code and line of code.

**Expected result:**
A debugging explanation is produced that ties the error to the recorded log level, code area/part of code, and line of code from the DeveloperLogs record(s).

**Stop or Escalate If:**

* DeveloperLogs entries do not contain the debugging attributes needed to identify the code area/part of code and line of code

---

## Success Criteria

* DeveloperLogs records for OptiSweep-related errors are located in the WCS EntityLogs database.
* The retrieved records include log level, code area/part of code, and line of code values.
* You can produce a debugging explanation that identifies the code area/part of code and line of code associated with the error using those recorded attributes.

## Failure Conditions

* EntityLogs database is not present/visible in the connected WCS SQL Server instance.
* DeveloperLogs table/model is not present within EntityLogs.
* DeveloperLogs contains no relevant OptiSweep entries.
* Retrieved log entries do not provide the debugging attributes needed (log level, code area/part of code, line of code).

## Escalation Guidance

* If EntityLogs/DeveloperLogs is not present or contains no relevant OptiSweep entries, stop and escalate to deeper WCS/OptiSweep database support (the source only states that OptiSweep uses EntityLogs for logging, not how to remediate missing logs).

## Missing Details / Known Gaps

* The source does not provide exact SSMS navigation steps (e.g., specific object tree path) or exact column names for log level / code area / line of code within DeveloperLogs.
* The source does not specify how to filter DeveloperLogs to “OptiSweep-related errors” (no example query or filter criteria provided).

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostics_entitylogs_for_optisweep_debugging
- Source ID: `training_video_day2`
- Source Type: `training_video`
