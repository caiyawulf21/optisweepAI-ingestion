# Interpret the Robot Location database model table fields to understand RMS station/orange location attributes

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_robot_location_model_fields_rms_orange_station_attributes_v1` |
| Title | Interpret the Robot Location database model table fields to understand RMS station/orange location attributes |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `wcs_sql`, `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

A support user reviews the Robot Location database model table field list to explain how location attributes map to the RMS-displayed orange station locations (including station number, occupied status, zone/closeout zone, location type, max AGVs, and dwell-time tracking).

## When To Use

Use when you need to interpret which Robot Location model table fields define a location and how those fields correspond to the orange station locations shown on RMS (including how to classify location types/statuses and whether dwell tracking is enabled).

## Do Not Use For

* Do not use this procedure as a substitute for deeper database/model ownership support if the Robot Location model table does not contain the documented fields or the expected location-type/status list.

## Access Or Tools Needed

* SSMS / Helix/WCS database access to view the Robot Location database model table (exact access method not specified in the source).
* Robot Location database model table (fields/columns as described in the segment).
* RMS screen access for the orange locations/workstation ID concept (if used for cross-check).

## Related Operational Context

* ctx_training_video_robot_location_database_model_v1
* ctx_training_video_location_types_and_statuses_v1
* ctx_training_video_rms_orange_locations_and_station_mapping_v1

## Visual References

![artifact_training_video_training_video_day2_0009_the_robot_location_database_model_table_primary_00_17_15_500](assets/e6b308f21a2ed402.jpg)

*Frame showing Robot Location database model table field list (station number, occupied, zone, closeout zone, location type, max AGVs, dwell tracking) and the location types/statuses list; also references orange RMS locations and workstation ID/station concept; includes XY coordinate notes.*

## Procedure Steps

### Step 1 — Open the Robot Location database model table described in the training segment

**Responsible role:** L2_support

**Instruction:**
In SSMS / Helix/WCS database access, open the Robot Location database model table that contains the location information (station number, occupied status, zone, closeout zone, location type, max AGVs allowed, and dwell-time tracking).

**Expected result:**
You can view the Robot Location database model table that includes the location attribute field list.

**Stop or Escalate If:**

* If the Robot Location model table does not contain the documented fields needed for station/orange location interpretation, stop and escalate to deeper database/model ownership support (L3/vendor).

---

### Step 2 — Review the documented location attributes (station number, occupied, zone, closeout zone, location type, max AGVs, dwell-time tracking)

**Responsible role:** L2_support

**Instruction:**
In the Robot Location database model table, locate and review the fields/attributes for: station number, occupied (occupied or not), zone, closeout zone, location type, Max number of AGVs allowed at that location, and whether the location should be tracked for dwell time there.

**Expected result:**
You can point to the Robot Location model fields that correspond to: station number, occupied status, zone, closeout zone, location type, max AGVs allowed, and dwell-time tracking.

**Stop or Escalate If:**

* If the Robot Location model table does not contain the documented fields/attributes, stop and escalate to deeper database/model ownership support (L3/vendor).

---

### Step 3 — Use the documented location types/statuses to classify the location type/status category

**Responsible role:** L2_support

**Instruction:**
From the Robot Location model table’s documented location types/statuses list, identify which category the location belongs to. Use the following categories: sorter entrance queue, sorter queue, sorter exit queue, tipper, tipper queue, tipper exit queue, hospital drop off, hospital entrance queue, hospital pickup, hospital exit queue, queue shut down, off the end shut down queue, GLD pre queue entrance, GLD pre queue exit.

**Expected result:**
You can select the correct location type/status category for the location based on the Robot Location model’s location type/status list.

**Stop or Escalate If:**

* If the Robot Location model table does not contain the expected location-type/status list, stop and escalate to deeper database/model ownership support (L3/vendor).

---

### Step 4 — Cross-check that RMS orange locations correspond to stations identified via workstation ID

**Responsible role:** L2_support

**Instruction:**
On RMS (orange locations view), use the workstation ID shown on the orange segments/locations to confirm that the orange locations correspond to stations that can be identified via workstation ID, consistent with the Robot Location model’s station concept.

**Expected result:**
You can correlate an RMS orange location/segment (where workstation ID is visible) to the station concept used in the Robot Location model.

**Stop or Escalate If:**

* If the station mapping cannot be validated because the Robot Location model table does not support the documented station/orange location mapping concept, stop and escalate to deeper database/model ownership support (L3/vendor).

---

### Step 5 — Review coordinate fields (XY coordinates / lat-long) and units (centimeters)

**Responsible role:** L2_support

**Instruction:**
In the Robot Location database model table, review the coordinate fields: XY coordinates (not enums) that are provided as coordinates (lat/long) and are in centimeters.

**Expected result:**
You can identify the coordinate fields in the Robot Location model and explain that they represent XY coordinates (lat/long) in centimeters.

---

## Success Criteria

* The user can point to the Robot Location model fields that define a location’s station/orange RMS representation (station number, occupied, zone, closeout zone, location type, max AGVs, dwell-time tracking).
* The user can classify a location into one of the documented location types/statuses categories used for RMS orange locations.
* The user can correlate RMS orange segments/locations (with workstation ID visible) to the station concept used in the Robot Location model.

## Failure Conditions

* Robot Location model table does not contain the documented fields/attributes needed for interpretation.
* Robot Location model table does not contain the expected location-type/status list.
* RMS orange locations cannot be correlated to stations via workstation ID.

## Escalation Guidance

* If the Robot Location model table does not contain the documented fields or the expected location-type/status list, stop and escalate to deeper database/model ownership support (L3/vendor), since the source does not provide alternate field names.

## Missing Details / Known Gaps

* The source does not specify exact SSMS/Helix/WCS navigation steps or query names to open the Robot Location database model table.
* The source does not provide the exact RMS URL/path or specific UI clicks for the orange locations view; only the concept that orange segments show workstation ID is provided.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_robot_location_model_interpret_location_fields
- Source ID: `training_video_day2`
- Source Type: `training_video`
