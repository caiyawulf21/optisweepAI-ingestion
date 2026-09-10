# Verify hospital location pickup/dropoff ID mapping in the location table (pickup ID and dropoff ID as location IDs)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_hospital_location_pickup_dropoff_id_mapping_location_table_v1` |
| Title | Verify hospital location pickup/dropoff ID mapping in the location table (pickup ID and dropoff ID as location IDs) |
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

Verify that the hospital station pickup ID and hospital station dropoff ID fields in the location table map to location IDs as described, and confirm the current implementation expectation is one-to-one (one pickup ID maps to one location; one dropoff ID maps to one location).

## When To Use

Use when you need to confirm how hospital pickup/dropoff identifiers relate to location IDs in the location table, specifically validating the described naming relationship and the one-to-one mapping expectation.

## Access Or Tools Needed

* Access to the location table configuration (database/config UI not specified in source)
* Ability to view columns/fields: hospital station pickup ID, hospital station dropoff ID, and location ID/ID column

## Related Operational Context

* ctx_training_video_location_hospital_pickup_dropoff_mapping_v1

## Visual References

![artifact_training_video_training_video_day2_0022_wait_do_we_need_to_stay_primary_01_54_40_000](assets/4b2d26c738220b4e.jpg)

*Frame/transcript discussing hospital tags model and the mapping relationship: location table contains hospital station pickup ID and dropoff ID; each location has an ID; pickup ID and dropoff ID correspond to location ID values; implementation expects one-to-one.*

## Procedure Steps

### Step 1 — Open the configuration view for the “location table” referenced by the hospital integration

**Responsible role:** L2_support

**Instruction:**
Open the configuration view for the “location table” referenced by the hospital integration in the live system (database/config UI not specified in the source).

**Expected result:**
You can view the location table structure/rows and identify the columns/fields needed for hospital station pickup ID, hospital station dropoff ID, and the location ID/ID column.

**Stop or Escalate If:**

* Stop if the live system does not expose the described location table columns/fields in an accessible way; request the correct configuration access.

---

### Step 2 — Find the columns for hospital station pickup ID and hospital station dropoff ID, and confirm there is also an ID column for each location

**Responsible role:** L2_support

**Instruction:**
In the location table view, locate the columns/fields described as “hospital station pickup ID” and “hospital station dropoff ID”, and confirm there is also an “ID” column for each location.

**Expected result:**
The location table contains fields for hospital station pickup ID and hospital station dropoff ID, and there is a location ID/ID column for each location.

---

### Step 3 — Confirm the mapping relationship: pickup ID and dropoff ID correspond to location ID values (naming can be confusing)

**Responsible role:** L2_support

**Instruction:**
Using the location table fields, confirm that the hospital pickup/dropoff identifiers correspond to the location ID values (i.e., pickup ID and drop off ID are the location ID values, even though naming may be confusing).

**Expected result:**
You can confirm that the pickup ID and dropoff ID values used in the hospital relationship match the location ID values in the location table.

---

### Step 4 — Check one-to-one implementation expectation for pickup ID and dropoff ID

**Responsible role:** L2_support

**Instruction:**
Validate that the current implementation is consistent with the described one-to-one expectation: one pickup ID maps to one location, and one dropoff ID maps to one location.

**Expected result:**
Pickup IDs and dropoff IDs each map one-to-one to location IDs (no pickup ID maps to multiple locations; no dropoff ID maps to multiple locations).

**Stop or Escalate If:**

* If the mapping is not one-to-one (or does not match the described relationship), escalate for deeper configuration/data model review.

---

### Step 5 — Record the pickup/dropoff IDs and corresponding location ID(s) used by the mapping

**Responsible role:** L2_support

**Instruction:**
Record the hospital pickup ID and hospital dropoff ID values you validated, along with the corresponding location ID(s) they map to in the location table.

**Expected result:**
You have a recorded set of pickup/dropoff IDs and their corresponding location ID(s) that reflect the validated mapping relationship.

---

## Success Criteria

* Location table exposes hospital station pickup ID and hospital station dropoff ID fields and a location ID/ID column for each location.
* Pickup ID and dropoff ID values correspond to location ID values as described.
* Current implementation matches the one-to-one expectation: one pickup ID maps to one location and one dropoff ID maps to one location.

## Failure Conditions

* Mapping is not one-to-one (pickup ID or dropoff ID maps to multiple locations).
* Pickup/dropoff identifiers do not correspond to location ID values as described.
* Live system does not expose the described location table fields/columns in an accessible way.

## Escalation Guidance

* If the mapping is not one-to-one (or does not match the described relationship), escalate for deeper configuration/data model review.

## Missing Details / Known Gaps

* The source does not specify the exact live system UI name, database name, or table name for the “location table” configuration view.
* The source does not specify the exact query method/steps to verify one-to-one beyond the conceptual expectation.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_location_table_pickup_dropoff_id_mapping
- Source ID: `training_video_day2`
- Source Type: `training_video`
