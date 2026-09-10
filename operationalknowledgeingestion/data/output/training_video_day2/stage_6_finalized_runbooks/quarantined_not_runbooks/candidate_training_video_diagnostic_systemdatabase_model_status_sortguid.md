# Check live system state and current Sort GUID in SSMS via Robotics [SystemDatabaseModel]

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_live_system_state_and_sort_guid_in_ssms_systemdatabasemodel_v1` |
| Title | Check live system state and current Sort GUID in SSMS via Robotics [SystemDatabaseModel] |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `sort_lifecycle_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use SSMS to query the Robotics database model [Helix2x_1Prod_Robotics].[dbo].[SystemDatabaseModel] and confirm the live system state (Status) and the current active sort identifier (SortGuid).

## When To Use

When you need to verify the current OptiSweep system state and which sort is currently active by reading the live values stored in [dbo].[SystemDatabaseModel] (Status and SortGuid) in the Robotics database.

## Access Or Tools Needed

* SSMS access to the Robotics database [Helix2x_1Prod_Robotics]
* Table/model: [dbo].[SystemDatabaseModel]

## Related Operational Context

* ctx_training_video_system_database_model_overview_v1
* ctx_training_video_status_reference_system_database_model_statuses_v1
* ctx_training_video_hmi_screen_reference_robotics_database_view_v1

## Visual References

![artifact_training_video_training_video_day2_0018_and_like_i_said_usually_because_primary_01_35_39_000](assets/ddafaa4a681bc7fb.jpg)

*SSMS/Robotics database screen showing the query against [Helix2x_1Prod_Robotics].[dbo].[SystemDatabaseModel] WITH (SNAPSHOT) and the columns including Status and SortGuid.*

## Procedure Steps

### Step 1 — Open SSMS and connect to the Robotics database [Helix2x_1Prod_Robotics]

**Responsible role:** L2_support

**Instruction:**
In SSMS, connect to the Robotics database shown as [Helix2x_1Prod_Robotics].

**Expected result:**
SSMS is connected to [Helix2x_1Prod_Robotics] and you can access [dbo].[SystemDatabaseModel].

**Stop or Escalate If:**

* If you cannot connect to [Helix2x_1Prod_Robotics], stop and escalate for deeper investigation.

---

### Step 2 — Query [dbo].[SystemDatabaseModel] using WITH (SNAPSHOT)

**Responsible role:** L2_support

**Instruction:**
Run the query/view for [dbo].[SystemDatabaseModel] as shown in the source, using WITH (SNAPSHOT).

**Expected result:**
A result set is displayed for [Helix2x_1Prod_Robotics].[dbo].[SystemDatabaseModel] that includes columns such as Status and SortGuid.

**Stop or Escalate If:**

* If the query cannot be run, stop and escalate for deeper investigation.
* If the expected columns (Status, SortGuid) are not present in the results, stop and escalate.

---

### Step 3 — Locate Status and SortGuid in the results

**Responsible role:** L2_support

**Instruction:**
In the query results, locate the columns/fields labeled Status and SortGuid (the source also shows fields like EntityInserted and EntityLastUpdate).

**Expected result:**
You can see a row where Status and SortGuid values are both visible in the results.

**Stop or Escalate If:**

* If Status is missing/blank or not one of the documented values, stop and escalate for deeper investigation.
* If the expected columns (Status, SortGuid) are not present, stop and escalate.

---

### Step 4 — Validate Status against the documented allowed system states

**Responsible role:** L2_support

**Instruction:**
Read the current Status value and compare it to the documented set of states: StartingUp, StartUpRequested, Running, ShutDownRequested, Shutdown, ZoneConfigRequested, ZoneConfigStaging, CloseOutRequested, CloseOutStaging, CloseOutStaged.

**Expected result:**
The Status value shown in the results matches one of the documented allowed values.

**Stop or Escalate If:**

* If Status is missing/blank or not one of the documented values, stop and escalate for deeper investigation.

---

### Step 5 — Confirm SortGuid corresponds to the active sort in the same row as Status

**Responsible role:** L2_support

**Instruction:**
Read the current SortGuid value from the same row where Status is shown, and confirm it represents the active sort being processed.

**Expected result:**
SortGuid value is visible and is taken from the same row as the current Status value.

**Stop or Escalate If:**

* If Status is missing/blank or not one of the documented values, stop and escalate for deeper investigation.
* If the query cannot be run or the expected columns (Status, SortGuid) are not present, stop and escalate.

---

## Success Criteria

* A result row is visible in [Helix2x_1Prod_Robotics].[dbo].[SystemDatabaseModel] with Status matching one of the documented allowed values.
* A SortGuid value is visible in the same row as the current Status value.

## Failure Conditions

* Status is missing/blank or not one of the documented values.
* The query cannot be run.
* Expected columns (Status, SortGuid) are not present in the results.

## Escalation Guidance

* If Status is missing/blank or not one of the documented values, stop and escalate for deeper investigation.
* If the query cannot be run or the expected columns (Status, SortGuid) are not present, stop and escalate for deeper investigation.

## Missing Details / Known Gaps

* The source packet does not provide the exact SSMS query text (only that it is run against [Helix2x_1Prod_Robotics].[dbo].[SystemDatabaseModel] WITH (SNAPSHOT)).
* The source packet does not provide explicit SSMS navigation/click-by-click steps beyond identifying the database and model.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_systemdatabase_model_status_sortguid
- Source ID: `training_video_day2`
- Source Type: `training_video`
