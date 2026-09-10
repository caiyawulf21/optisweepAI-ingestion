# Check active dwell events in SSMS via LocationActiveDwellModel (dwell tracking true/false per station)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_active_dwell_events_ssms_locationactivedwellmodel_v1` |
| Title | Check active dwell events in SSMS via LocationActiveDwellModel (dwell tracking true/false per station) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use SSMS to verify which stations/locations are currently accumulating dwell time by checking the robot location database model’s DwellTracking (true/false) flag and then inspecting the LocationActiveDwellModel table for active dwell rows. Active dwell events should appear with timing fields such as SatTime, FinishTime, and TotalTime, and completed dwell should be archived to LocationDwellActivity after the AGV leaves.

## When To Use

When you need to determine which dwell-tracked stations/locations currently have active dwell events and to interpret the active dwell timing fields shown in LocationActiveDwellModel.

## Do Not Use For

* Do not use this procedure as a substitute for investigating physical safety stops (E-stop). This procedure is limited to database dwell tracking visibility and timing fields.

## Access Or Tools Needed

* SSMS
* Robot location database model (with DwellTracking true/false field)
* LocationActiveDwellModel table
* LocationDwellActivity table (for understanding that completed dwell is archived)

## Related Operational Context

* ctx_training_video_dwell_tracking_overview_v1
* ctx_training_video_location_dwell_tracking_flag_v1
* ctx_training_video_location_active_dwell_model_v1

## Visual References

![artifact_training_video_training_video_day2_0016_so_everybody_s_at_a_location_primary_01_32_39_000](assets/4da092dc0229edfc.jpg)

*Slide/frame showing LocationActiveDwellModel displays active dwells at locations marked for DwellTracking (true/false) and lists fields including AgvName, Station, SortGuid, SatTime, FinishTime, TotalTime; also notes archiving to LocationDwellActivity once the AGV leaves.*

## Procedure Steps

### Step 1 — Open SSMS and connect to the OptiSweep/WCS database that contains dwell tracking tables

**Responsible role:** L2_support

**Instruction:**
Open SSMS and connect to the OptiSweep/WCS database that contains the robot location database model and dwell tracking tables.

**Expected result:**
SSMS is connected and you can browse/query the database objects needed for dwell tracking (robot location database model and LocationActiveDwellModel).

**Stop or Escalate If:**

* If you cannot access the database or cannot locate the dwell tracking tables/models, stop and escalate to L3_support/vendor support for database access/schema clarification.

---

### Step 2 — Identify stations/locations with DwellTracking = true in the robot location database model

**Responsible role:** L2_support

**Instruction:**
Locate the robot location database model that includes the DwellTracking true/false field, and identify which stations/locations are marked for dwell tracking (DwellTracking set to true).

**Expected result:**
You can identify the set of stations/locations where DwellTracking is true.

**Stop or Escalate If:**

* If the expected tables/fields (including DwellTracking) are not present or cannot be found, stop and escalate to L3_support/vendor support for database access/schema clarification.

---

### Step 3 — Open LocationActiveDwellModel and confirm it shows active dwells for DwellTracking=true locations

**Responsible role:** L2_support

**Instruction:**
Open the LocationActiveDwellModel table and confirm it is displaying active dwells at locations marked for DwellTracking.

**Expected result:**
LocationActiveDwellModel contains active dwell rows corresponding to stations/locations where DwellTracking is true.

**Stop or Escalate If:**

* If LocationActiveDwellModel shows no active dwell rows for stations you expect to be dwell-tracked, re-check the robot location database model’s DwellTracking true/false setting for those stations.
* If the expected tables/fields (LocationActiveDwellModel) are not present or cannot be found, stop and escalate to L3_support/vendor support for database access/schema clarification.

---

### Step 4 — Review LocationActiveDwellModel timing and identity fields (AgvName, Station, SortGuid, SatTime, FinishTime, TotalTime)

**Responsible role:** L2_support

**Instruction:**
In LocationActiveDwellModel, review the columns/fields shown in the source: AgvName, Station, SortGuid, SatTime, FinishTime, and TotalTime.

**Expected result:**
The LocationActiveDwellModel view/table shows the fields AgvName, Station, SortGuid, SatTime, FinishTime, and TotalTime for active dwell rows.

**Stop or Escalate If:**

* If the expected tables/fields (LocationActiveDwellModel and the listed columns) are not present or cannot be found, stop and escalate to L3_support/vendor support for database access/schema clarification.

---

### Step 5 — Confirm the dwell event is represented as an active record (current in LocationActiveDwellModel vs archived)

**Responsible role:** L2_support

**Instruction:**
For the active dwell rows you are investigating, confirm the dwell event is currently represented in LocationActiveDwellModel (active) rather than only archived.

**Expected result:**
The dwell event you are investigating appears in LocationActiveDwellModel as an active record.

---

### Step 6 — Record observed active dwell values for the dwell rows under investigation

**Responsible role:** L2_support

**Instruction:**
Record the relevant observed values for the active dwell rows you are investigating (AgvName, Station, SortGuid, SatTime/FinishTime/TotalTime as displayed).

**Expected result:**
You have a list of active dwell rows with the values for AgvName, Station, SortGuid, SatTime, FinishTime, and TotalTime.

---

## Success Criteria

* You identify stations/locations with DwellTracking set to true in the robot location database model.
* LocationActiveDwellModel shows active dwell rows for those DwellTracking=true stations/locations.
* Active dwell rows display the expected fields: AgvName, Station, SortGuid, SatTime, FinishTime, TotalTime.

## Failure Conditions

* No active dwell rows appear in LocationActiveDwellModel for stations/locations expected to be dwell-tracked.
* DwellTracking true/false field is missing or cannot be found in the robot location database model.
* LocationActiveDwellModel or the expected columns (AgvName, Station, SortGuid, SatTime, FinishTime, TotalTime) are missing or cannot be found.

## Escalation Guidance

* If LocationActiveDwellModel shows no active dwell rows for stations you expect to be dwell-tracked, re-check the robot location database model’s DwellTracking true/false setting for those stations.
* If the expected tables/fields (LocationActiveDwellModel and the listed columns, or the DwellTracking field) are not present or cannot be found, stop and escalate to L3_support/vendor support for database access/schema clarification.

## Missing Details / Known Gaps

* The source does not provide exact SSMS navigation steps (server/database name, schema name, or specific query syntax). Steps are kept at the table/model and field level.

## Source Lineage

- Candidate IDs: candidate_training_video_dwell_tracking_check_location_active_dwell_model
- Source ID: `training_video_day2`
- Source Type: `training_video`
