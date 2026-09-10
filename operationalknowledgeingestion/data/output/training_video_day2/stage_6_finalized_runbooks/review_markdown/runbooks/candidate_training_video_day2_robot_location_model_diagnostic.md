# Inspect Robot Location Attributes in the Robotics Database

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_inspect_robot_location_attributes_in_the_robotics_database_v1` |
| Title | Inspect Robot Location Attributes in the Robotics Database |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `zone_config_state` |
| Access Surface | `wcs_sql`, `rms_ui` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

A read-only WCS / Helix DB (SSMS) diagnostic for inspecting Robot Location records in the OptiSweep Robotics database and comparing the record with the corresponding RMS / fleet status UI location cue. Review station number, occupied state, zone, closeout zone, location type, maximum AGVs allowed, and dwell-time tracking.

## When To Use

Use this diagnostic when L2/L3 support needs to interpret a station or location in the live WCS / Helix DB (SSMS) and associate it with a location shown in the RMS / fleet status UI.

## Do Not Use For

* Do not use this procedure to modify Robotics database records.
* Do not use this procedure as a physical AGV recovery or E-stop procedure.
* Do not use this procedure as a substitute for a live database query or RMS location comparison; the packet does not provide a complete SSMS navigation path or SQL query.

## Safety And Operational Notes

* Use read-only inspection only.
* Do not modify database records as part of this diagnostic.

## Access Or Tools Needed

* WCS / Helix DB (SSMS) access to the OptiSweep Robotics database
* Robot Location database model/table
* RMS / fleet status UI access for location comparison

## Related Operational Context

* ctx_training_video_robot_location_database_model_v1
* ctx_training_video_location_types_and_statuses_v1
* ctx_training_video_location_zones_coordinates_and_cell_codes_v1

## Procedure Steps

### Step 1 — Open the Robotics database in WCS / Helix DB (SSMS)

**Responsible role:** L2_support

**Instruction:**
In WCS / Helix DB (SSMS), select the OptiSweep Robotics database. Use read-only inspection and do not edit or execute changes against database records.

**Expected result:**
The OptiSweep Robotics database is selected and available for inspection in WCS / Helix DB (SSMS).

**Stop or Escalate If:**

* Stop if the database cannot be accessed read-only.
* Escalate to L3_support if the Robotics database is unavailable or access cannot be established.

---

### Step 2 — Locate the Robot Location record

**Responsible role:** L2_support

**Instruction:**
In WCS / Helix DB (SSMS), locate the Robot Location database model/table and inspect the record for the relevant station or location. Use the available station or location identity to select the record; do not infer an unprovided table path or SQL query.

**Expected result:**
A Robot Location record corresponding to the investigated station or location is present and readable.

**Stop or Escalate If:**

* Escalate to L2/L3 support if the expected Robot Location record is missing.
* Escalate if the record cannot be associated with the investigated location.

---

### Step 3 — Inspect Robot Location attributes

**Responsible role:** L2_support

**Instruction:**
In WCS / Helix DB (SSMS), inspect the Robot Location record fields for station number, occupied state, zone, closeout zone, location type, maximum number of AGVs allowed, and dwell-time tracking.

**Expected result:**
The live Robot Location record exposes readable values for station or location identity, occupied state, zone, closeout zone, location type, maximum AGVs allowed, and dwell-time tracking.

**Stop or Escalate If:**

* Escalate to L2/L3 support if identifying fields are blank or inconsistent.
* Do not modify the record to correct a value during this diagnostic.

---

### Step 4 — Compare the record with the RMS location cue

**Responsible role:** L2_support

**Instruction:**
In the RMS / fleet status UI, locate the corresponding orange location or workstation ID and compare that live location cue with the station or location identity from the WCS / Helix DB (SSMS) Robot Location record. Use the RMS location cue for association; do not assume that color alone proves a field value.

**Expected result:**
The Robot Location record can be associated with the corresponding RMS / fleet status UI location cue, including an orange location or visible workstation ID when present.

**Stop or Escalate If:**

* Escalate to L2/L3 support if the database record cannot be associated with the RMS location.
* Escalate if the RMS cue and database identifying fields are inconsistent.

---

## Success Criteria

* The relevant Robot Location record is found in the OptiSweep Robotics database through WCS / Helix DB (SSMS).
* Station or location identity, occupied state, zone, closeout zone, location type, maximum AGVs allowed, and dwell-time tracking are readable.
* The database record can be associated with the corresponding RMS / fleet status UI location cue.
* No database records are modified.

## Failure Conditions

* The Robotics database or Robot Location model/table cannot be accessed.
* The expected Robot Location record is missing.
* Station or location identifying fields are blank or inconsistent.
* The record cannot be associated with the RMS / fleet status UI location cue.
* The database record would need to be modified to continue.

## Escalation Guidance

* Escalate to L2/L3 support when the expected Robot Location record is missing, cannot be associated with RMS, or contains blank or inconsistent identifying fields.
* Do not modify database records during this diagnostic.

## Missing Details / Known Gaps

* The packet does not provide a dedicated Robot Location screenshot showing the requested fields; the available same-section frame is not a dedicated live Robot Location table view.
* The packet does not provide an exact SSMS navigation path, database object path, or SQL query for locating the Robot Location record.
* The packet does not provide a dedicated RMS map screenshot for the orange-location and workstation-ID comparison.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_robot_location_model_diagnostic
- Source ID: `training_video_day2`
- Source Type: `training_video`
