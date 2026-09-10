# Use hospital tag variable type to determine which value column to read/write (string vs boolean via lookup)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_hospital_tag_variable_type_lookup_v1` |
| Title | Use hospital tag variable type to determine which value column to read/write (string vs boolean via lookup) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When troubleshooting hospital-controller tag behavior, confirm that the hospital tag table’s “variable type” drives which value column the system should use. The source describes a modular design where each hospital tag row has zeros/ones across value columns, and a lookup table maps “value variable type” to the correct value column for that tag.

## When To Use

Use this when you need to determine which hospital tag value column (e.g., string vs boolean representation) should be active for a specific hospital station/tag row, based on the row’s “variable type” and the lookup table mapping described in the source.

## Access Or Tools Needed

* Access to the hospital tag table configuration/view used for hospital controller communication
* Access to the lookup table that maps “value variable type” to the value column

## Related Operational Context

* ctx_training_video_hospital_tag_variable_type_lookup_v1

## Visual References

![artifact_training_video_training_video_day2_0022_wait_do_we_need_to_stay_primary_01_54_40_000](assets/4b2d26c738220b4e.jpg)

*Training frame showing hospital tags model processing and the concept of “value variable type” and a lookup table that indicates which column to look at; also describes hospital tag table rows having zeros/ones with only one column having a ones.*

## Procedure Steps

### Step 1 — Open the hospital tag table configuration/view used for hospital controller communication

**Responsible role:** L2_support

**Instruction:**
Open the hospital tag table configuration/view that the system uses to communicate with the hospital controller (hospital tags model).

**Expected result:**
You can view hospital tag table rows where each hospital station ID has a row containing a “variable type” field and multiple value columns represented with zeros/ones.

**Stop or Escalate If:**

* Stop if the live system does not expose the “variable type” field in the hospital tag table view.
* Stop if the live system does not expose the value columns/zero-one representation needed to identify the active value column.

---

### Step 2 — Locate the “variable type” field for the specific hospital station/tag row

**Responsible role:** L2_support

**Instruction:**
In the hospital tag table, select the row for the specific hospital station ID/tag you are investigating, then locate the “value variable type” / “variable type” field in that row.

**Expected result:**
The selected row shows a “variable type” value (described as indicating what type of string/value the tag represents).

**Stop or Escalate If:**

* Stop if the live system does not expose the “variable type” field for the hospital tag table row.

---

### Step 3 — Use the lookup table to map variable type to the expected value column

**Responsible role:** L2_support

**Instruction:**
Open the lookup table referenced by the hospital tags model and use the row’s “value variable type” to determine which value column should be used for that specific tag.

**Expected result:**
You identify the specific value column that the lookup table indicates should be used for the tag’s variable type.

**Stop or Escalate If:**

* If variable type does not map to the expected value column (or the lookup table is inconsistent), escalate for configuration/data model review.
* Stop if the live system does not expose the lookup table needed to map variable type to value column.

---

### Step 4 — Confirm the hospital tag row’s zero/one pattern matches the mapped value column

**Responsible role:** L2_support

**Instruction:**
In the same hospital tag table row, check the value columns and confirm that zeros/ones are present with only one column having a ones value—specifically the column identified by the lookup-table mapping.

**Expected result:**
The mapped value column is the one column set to ones for that hospital tag row; other value columns are zeros.

**Stop or Escalate If:**

* If variable type does not map to the expected value column (or the lookup table is inconsistent), escalate for configuration/data model review.

---

### Step 5 — Record the expected active value column for the tag based on variable type

**Responsible role:** L2_support

**Instruction:**
Record which value column is expected to hold the active value for the tag based on the variable type and the lookup-table mapping you applied.

**Expected result:**
A clear mapping is documented for the investigated hospital station/tag row: variable type -> lookup mapping -> expected active value column.

**Stop or Escalate If:**

* If the expected value column does not match the observed active column, escalate for configuration/data model review.

---

## Success Criteria

* For the investigated hospital tag row, the “variable type” value maps (via the lookup table) to a specific value column.
* The hospital tag row’s zero/one pattern shows ones in the mapped value column and zeros in the other value columns.

## Failure Conditions

* “variable type” field is not exposed in the hospital tag table view.
* Lookup table needed to map “value variable type” to value column is not exposed or unavailable.
* Lookup mapping does not match the row’s active (ones) value column.
* Row has an unexpected zero/one pattern (e.g., multiple ones columns).

## Escalation Guidance

* Escalate for configuration/data model review if variable type does not map to the expected value column or if the lookup table is inconsistent.

## Missing Details / Known Gaps

* The source does not provide the exact hospital tag table name, the exact “variable type” column name, or the exact value column names to read/write.
* The source does not provide the exact lookup table name or the exact mapping keys/fields used to map “value variable type” to the value column.
* The source does not specify the exact live UI/DB surface (e.g., SSMS table name/view) where the hospital tag table and lookup table are accessed.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_hospital_tag_variable_type_value_column_lookup
- Source ID: `training_video_day2`
- Source Type: `training_video`
