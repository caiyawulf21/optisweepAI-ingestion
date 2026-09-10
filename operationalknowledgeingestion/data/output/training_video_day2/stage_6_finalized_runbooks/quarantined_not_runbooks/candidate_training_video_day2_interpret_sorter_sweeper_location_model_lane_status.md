# Interpret Sorter Sweeper Database Location Model: location types and lane status (active/bypass/not tracking)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_sorter_sweeper_location_model_lane_status_v1` |
| Title | Interpret Sorter Sweeper Database Location Model: location types and lane status (active/bypass/not tracking) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `zone_config_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Sorter Sweeper database Location Model fields to identify what a location represents (Sorter, Tipper, Hospital, Induction) and interpret the lane status for a destination as active/open, bypass/closed, or not tracking/not yet used.

## When To Use

When you need to interpret how a sorter-side destination is represented in the Sorter Sweeper database Location Model—specifically the location type and whether the destination is active/open, bypass/closed, or not tracking/not yet used.

## Do Not Use For

* Do not use this procedure to perform physical safety actions (no E-stop).
* Do not use this procedure if you cannot access the Sorter Sweeper database objects needed to view the Location Model fields (request the correct database/table/view name instead).

## Safety And Operational Notes

* This procedure is interpretive (database field meaning). It does not require physical safety actions.

## Access Or Tools Needed

* Sorter Sweeper database access appropriate for interpreting the Location Model (access may be limited; CS/support teams may use VM).

## Related Operational Context

* ctx_training_video_sorter_model_legs_and_receiver_fields_v1
* ctx_training_video_location_model_station_types_v1
* ctx_training_video_sort_location_attributes_v1
* ctx_training_video_lane_status_reference_v1
* ctx_training_video_access_reference_cs_team_vm_access_v1

## Visual References

![artifact_training_video_training_video_day2_0021_all_right_finish_with_brother_send_primary_01_42_21_000](assets/b5edd9932a6a736d.jpg)

*Frame showing Sorter Sweeper Database Location Model: locations represent stations in the map; LocationType values (Sorter, Tipper, Hospital, Induction) and lane status meanings (active/open, bypass/closed, not tracking/not yet used).*

## Procedure Steps

### Step 1 — Open the Sorter Sweeper database Location Model view/table for sorter-side stations

**Responsible role:** L2_support

**Instruction:**
Open the Sorter Sweeper database view/table that contains the Location Model for sorter-side stations (the source indicates there is an actual database, but access may be limited and may require CS/support team access via VM).

**Expected result:**
You can view location records in the Sorter Sweeper database that include (at minimum) a LocationType field and a lane status field for each location/destination record.

**Stop or Escalate If:**

* If you cannot find the LocationType or lane status fields in the database view you opened, stop and request the correct database/table/view name from the CS/support team mentioned as having access.

---

### Step 2 — Identify the station type using LocationType (Sorter, Tipper, Hospital, Induction)

**Responsible role:** L2_support

**Instruction:**
In the Location Model records, locate the LocationType field and confirm the value is one of: Sorter, Tipper, Hospital, or Induction.

**Expected result:**
For the destination/location record you are analyzing, LocationType is one of the four supported types: Sorter, Tipper, Hospital, Induction.

**Stop or Escalate If:**

* If LocationType is not present or does not match the source-listed values, stop and escalate to the team that owns the database schema/definitions for that site.

---

### Step 3 — Interpret Induction and Hospital LocationType meanings

**Responsible role:** L2_support

**Instruction:**
If LocationType is Induction, confirm it is described as the specified tote induction location at the hospital. If LocationType is Hospital, confirm it is described as the specified tote drop-off location at the hospital.

**Expected result:**
For the record(s) where LocationType is Induction or Hospital, you can state which hospital tote function the location represents (induction vs drop-off) using the source-backed definitions.

---

### Step 4 — Read lane status for the destination/location record

**Responsible role:** L2_support

**Instruction:**
Find the lane status field for the location/destination record and identify whether it is one of: active, bypass, or not tracking.

**Expected result:**
The lane status value for the record is one of the source-listed values: active, bypass, or not tracking.

**Stop or Escalate If:**

* If the lane status value is not one of the source-listed values (active, bypass, not tracking), stop and escalate to the team that owns the database schema/definitions for that site.

---

### Step 5 — Map lane status to operational meaning (active=open, bypass=closed, not tracking=not yet used)

**Responsible role:** L2_support

**Instruction:**
Map the observed lane status to the source meanings: active = open; bypass = closed; not tracking = destinations that have not been used yet.

**Expected result:**
You can state the destination’s operational state as open/active, closed/bypassed, or not yet used based on the lane status value in the record.

---

### Step 6 — Optionally verify additional location attributes to ensure you are looking at the correct location record

**Responsible role:** L2_support

**Instruction:**
Optionally verify additional location attributes mentioned by the source (e.g., sort name, sort side, zone, sequence from sort entrance, lane/chute number, lane delay, keep-closed, tipper select) to ensure you are looking at the correct location record for the destination you care about.

**Expected result:**
The record’s additional attributes align with the destination context you are investigating (sort/zone/sequence/lane/chute and related flags).

---

## Success Criteria

* For the destination/location record you opened, LocationType is identified as one of: Sorter, Tipper, Hospital, Induction.
* For that same record, lane status is read as active, bypass, or not tracking.
* You can correctly interpret the destination state as open/active, closed/bypassed, or not yet used based on the lane status mapping.

## Failure Conditions

* Lane status contains a value outside active/bypass/not tracking.
* LocationType field is missing or contains values outside the four named types.
* The required fields (LocationType and lane status) are not present in the opened database view/table.

## Escalation Guidance

* If lane status is not one of the source-listed values (active, bypass, not tracking), stop and escalate to the team that owns the database schema/definitions for that site.
* If you cannot find the LocationType or lane status fields in the database view you opened, stop and request the correct database/table/view name from the CS/support team mentioned as having access.

## Missing Details / Known Gaps

* The candidate references a specific “Sorter Sweeper database view/table” name, but the packet does not provide the exact database object name(s) to open.
* The packet does not provide the exact column name for the lane status field (only the lane status values and their meanings).

## Source Lineage

- Candidate IDs: candidate_training_video_day2_interpret_sorter_sweeper_location_model_lane_status
- Source ID: `training_video_day2`
- Source Type: `training_video`
