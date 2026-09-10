# Interpret Charging Database Model Tables to Understand Charging Areas, Chargers, and Thresholds

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_charging_db_model_tables_v1` |
| Title | Interpret Charging Database Model Tables to Understand Charging Areas, Chargers, and Thresholds |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_charging_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `charging_abnormal`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the charging-related database model tables in the OptiSweep/WCS database to explain how charging areas (with entrance/exit IDs and disabled flags), charging locations (chargers tied to stations and tote stands, with disabled flags), and charging threshold variables drive AGV charging decisions—normal charge, kick-off, and emergency charging behavior.

## When To Use

When you need to interpret how the system’s charging configuration and threshold variables are represented in the charging database model tables, to explain or troubleshoot AGV charging behavior (including emergency charging) based on the stored mappings and variables.

## Do Not Use For

* Do not use this procedure to make configuration changes based only on this segment’s described tables/fields; use it to gather evidence and explain behavior.

## Access Or Tools Needed

* SSMS
* Helix/WCS database access (charging database model tables described in the segment)

## Related Operational Context

* ctx_training_video_charging_database_tables_v1
* ctx_training_video_charging_threshold_usage_v1
* ctx_training_video_charging_area_layout_mapping_v1
* ctx_training_video_assigned_chargers_and_emergency_fallback_v1

## Visual References

![artifact_training_video_training_video_day2_0013_let_s_see_and_the_last_primary_00_53_44_500](assets/7f73e84f02ceaaf8.jpg)

*Segment frame describing the three charging-related database model tables (charging areas with entrance/exit IDs, charging locations with chargers/stations/tote stands and disabled flags, and charging threshold variables used by code for charge/kick-off/emergency charge).*

## Procedure Steps

### Step 1 — Identify the charging database model tables described in the segment

**Responsible role:** L2_support

**Instruction:**
In the Helix/WCS database accessed via SSMS, identify the three charging-related database model tables described in the segment: (1) charging area database model table, (2) charging location database model table, and (3) charging threshold database model table.

**Expected result:**
You can name and locate the three charging-related database model tables in the database that correspond to: charging areas (entrance/exit IDs), charging locations (chargers/stations/tote stands and disabled flags), and charging threshold variables (values used by code for charge/kick-off/emergency charge).

**Stop or Escalate If:**

* If the database does not contain the described tables/fields, escalate to deeper support for database schema/model verification.

---

### Step 2 — Verify charging area records: entrance IDs, exit IDs, and disabled state

**Responsible role:** L2_support

**Instruction:**
Using SSMS, query the charging area database model table and locate records for charging areas. Verify that each charging area record includes: entrance IDs, exit IDs, and whether the area is marked disabled or not.

**Expected result:**
For the charging area(s) relevant to the behavior you are explaining, you can point to the stored entrance IDs and exit IDs and confirm the disabled/not-disabled state for that area.

**Stop or Escalate If:**

* If the expected mappings (entrance/exit IDs, disabled flags) cannot be found, escalate to deeper support for database schema/model verification.

---

### Step 3 — Verify charging location records: charger-to-station, charger-to-tote-stand, and disabled state

**Responsible role:** L2_support

**Instruction:**
Using SSMS, query the charging location database model table and locate individual charger records. Verify the stored station association and tote stand association for each charger record, and confirm whether each charger record is marked disabled or not.

**Expected result:**
For the charger(s) relevant to the behavior you are explaining, you can point to the stored station association and tote stand association and confirm the disabled/not-disabled state for each charger record.

**Stop or Escalate If:**

* If the expected mappings (charger-to-station, charger-to-tote-stand associations, disabled flags) cannot be found, escalate to deeper support for database schema/model verification.

---

### Step 4 — Verify charging threshold values used by code for charge, kick-off, and emergency charge

**Responsible role:** L2_support

**Instruction:**
Using SSMS, query the charging threshold database model table and locate the threshold values/variables described as being used by code to decide: (a) whether an AGV needs charge, (b) whether it can be kicked off the charger, and (c) whether it needs an emergency charge.

**Expected result:**
You can point to the specific threshold values/variables in the charging threshold database model table that correspond to normal charge vs kick-off vs emergency charge decisions.

**Stop or Escalate If:**

* If the expected threshold variables cannot be found, escalate to deeper support for database schema/model verification.

---

### Step 5 — Explain charging behavior using the stored layout mapping and threshold variables

**Responsible role:** L2_support

**Instruction:**
Using the records you identified in Steps 2–4, explain how the stored mapping/variables determine charging behavior: charging decisions are driven by the threshold values, and the layout mapping ties entrance/exit IDs and tote stand IDs to the chargers/areas.

**Expected result:**
You can produce an evidence-based explanation that references: (1) the charging area entrance/exit IDs and disabled state, (2) the charger-to-station and charger-to-tote-stand associations and disabled state, and (3) the threshold variables used by code for charge vs kick-off vs emergency charge.

**Stop or Escalate If:**

* If the database does not contain the described tables/fields or the expected mappings (entrance/exit IDs, disabled flags, charger-to-tote stand associations, threshold values) cannot be found, escalate to deeper support for database schema/model verification.
* Do not attempt configuration changes based only on this training segment; use it to gather evidence and explain behavior.

---

### Step 6 — If emergency charging is involved, verify emergency fallback behavior and cycling/lowest-charge behavior

**Responsible role:** L2_support

**Instruction:**
When the issue involves emergency charging, verify the segment’s described emergency behavior: if an AGV’s own sorter-side charger is not available, it can use a charger from another sorter side; also note that AGVs keep cycling on the charge and the system keeps the lowest charge on the charger.

**Expected result:**
You can explain emergency charging behavior using the described fallback rule (use another sorter side’s free charger when own is unavailable) and the described cycling/lowest-charge behavior.

**Stop or Escalate If:**

* If the database does not contain the described tables/fields or the expected mappings (entrance/exit IDs, disabled flags, charger-to-tote stand associations, threshold values) cannot be found, escalate to deeper support for database schema/model verification.

---

## Success Criteria

* You can identify the three charging-related database model tables described in the segment (charging area, charging location, charging threshold).
* You can point to charging area records showing entrance IDs, exit IDs, and disabled state.
* You can point to charging location records showing charger-to-station association, charger-to-tote-stand association, and disabled state.
* You can point to charging threshold values/variables used by code for charge vs kick-off vs emergency charge decisions.
* For emergency charging scenarios, you can explain the described fallback behavior (use another sorter side’s free charger when own is unavailable) and the described cycling/lowest-charge behavior.

## Failure Conditions

* Charging area entrance/exit IDs or disabled state cannot be found for relevant records.
* Charging location charger-to-station or charger-to-tote-stand associations or disabled state cannot be found for relevant records.
* Charging threshold values/variables used by code for charge/kick-off/emergency charge cannot be found.
* Emergency fallback behavior cannot be supported by the available evidence from the stored mappings/variables.

## Escalation Guidance

* If the database does not contain the described tables/fields or the expected mappings (entrance/exit IDs, disabled flags, charger-to-tote stand associations, threshold values) cannot be found, escalate to deeper support for database schema/model verification.

## Missing Details / Known Gaps

* The source does not provide exact SSMS navigation paths or exact table/column names beyond the conceptual table names (charging area database model table, charging location database model table, charging threshold database model table).
* The source does not provide the specific threshold variable names/fields or their numeric meanings; it only states that the charging threshold database model table stores values used by code for charge vs kick-off vs emergency charge.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_charging_db_model_tables_interpret
- Source ID: `training_video_day2`
- Source Type: `training_video`
