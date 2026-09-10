# Look Up System Error Definitions and Interpret Active Errors (SystemErrorDefinition + SystemActiveErrorModel)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_look_up_system_error_definitions_and_interpret_active_errors_systemerrordefinition_systemactiveerrormodel_v1` |
| Title | Look Up System Error Definitions and Interpret Active Errors (SystemErrorDefinition + SystemActiveErrorModel) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | None |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robotics Database System Error Definition table (SystemErrorDefinition) to find the documented description and resolution for a system error, then cross-check the corresponding active record in the System Active Error model (SystemActiveErrorModel) using the error name/area/area code/description. When the error is resolved, the active error is archived to the System Error Activity model table.

## When To Use

Use when you need to interpret what a currently active system error means and what resolution is documented for it, by mapping the active error shown in SystemActiveErrorModel to its definition in SystemErrorDefinition.

## Do Not Use For

* Do not use this procedure as a substitute for applying an actual resolution workflow when the source system error definition cannot be found or when the active error does not transition to archived after the expected resolution.

## Access Or Tools Needed

* Robotics Database access to view SystemErrorDefinition
* Robotics Database access to view SystemActiveErrorModel
* Robotics Database access to view the System Error Activity model table (archived/resolved errors)

## Related Operational Context

* ctx_training_video_system_error_definition_table_v1
* ctx_training_video_system_active_error_model_v1
* ctx_training_video_system_error_activity_model_v1

## Visual References

![artifact_training_video_training_video_day2_0017_so_moving_on_system_error_definition_primary_01_34_34_500](assets/445c91f76e7e9c07.jpg)

*Slide frame showing System Error Definition table fields (SystemErrorDescription, SystemErrorResolution) and SystemActiveErrorModel fields (name, area, area code, description), plus note that resolved active errors are archived to SystemErrorActivityModel.*

## Procedure Steps

### Step 1 — Open the Robotics Database view/table area that contains the System Error Definition table (SystemErrorDefinition)

**Responsible role:** L2_support

**Instruction:**
In the Robotics Database, navigate to the System Error Definition table (SystemErrorDefinition) and locate the columns/fields for SystemErrorDescription and SystemErrorResolution.

**Expected result:**
You can view SystemErrorDefinition rows that include SystemErrorDescription and SystemErrorResolution for system errors.

---

### Step 2 — Locate the specific error entry by matching the error name/code you are investigating to the SystemErrorDefinition rows

**Responsible role:** L2_support

**Instruction:**
In SystemErrorDefinition, match the error you are investigating (by error name/code) to the correct row in the table.

**Expected result:**
You identify a specific SystemErrorDefinition row corresponding to the active error you are investigating.

**Stop or Escalate If:**

* If the active error cannot be matched to any SystemErrorDefinition entry, stop and escalate for deeper investigation (the source does not describe how to handle missing definitions).

---

### Step 3 — Read the documented fields for that error: SystemErrorDescription and SystemErrorResolution

**Responsible role:** L2_support

**Instruction:**
From the selected SystemErrorDefinition row, read SystemErrorDescription and SystemErrorResolution.

**Expected result:**
You have the SystemErrorDescription and SystemErrorResolution values for the selected error.

---

### Step 4 — Open the System Active Error model (SystemActiveErrorModel) view that shows active errors currently in the system

**Responsible role:** L2_support

**Instruction:**
In the Robotics Database, open the System Active Error model (SystemActiveErrorModel) view that lists active errors currently in the system.

**Expected result:**
You can view active error records in SystemActiveErrorModel with fields including name, area, area code, and description.

---

### Step 5 — Find the active error record that corresponds to the same error name/code you looked up in SystemErrorDefinition

**Responsible role:** L2_support

**Instruction:**
In SystemActiveErrorModel, locate the active error record that corresponds to the same error name/code you matched in SystemErrorDefinition.

**Expected result:**
You identify the active error record in SystemActiveErrorModel that corresponds to the selected SystemErrorDefinition entry.

---

### Step 6 — Verify the active error record’s displayed information includes: name, area, area code, and description

**Responsible role:** L2_support

**Instruction:**
On the selected SystemActiveErrorModel active error record, verify that the displayed information includes name, area, area code, and description.

**Expected result:**
The active error record displays name, area, area code, and description.

---

### Step 7 — After the error is resolved, confirm it is no longer shown as active and is instead archived to the System Error Activity model table

**Responsible role:** L2_support

**Instruction:**
After resolution, check that the error is no longer present in SystemActiveErrorModel as an active error, and confirm it appears in the System Error Activity model table as an archived/resolved record.

**Expected result:**
The error is removed from SystemActiveErrorModel (no longer shown as active) and is present in the System Error Activity model table as an archived/resolved entry.

**Stop or Escalate If:**

* If the error remains active after the documented resolution is expected to be applied, stop and escalate (the source only states that resolved errors are archived, not how to force resolution).

---

## Success Criteria

* A currently active error record in SystemActiveErrorModel can be mapped to a SystemErrorDefinition entry using the error name/code and the model fields (name/area/area code/description).
* SystemErrorDefinition provides SystemErrorDescription and SystemErrorResolution for the matched error.
* After resolution, the error is no longer shown as active and is archived to the System Error Activity model table.

## Failure Conditions

* No matching SystemErrorDefinition entry exists for the active error name/code.
* The active error cannot be found in SystemActiveErrorModel for the looked-up error name/code.
* After expected resolution, the error remains active (still shown in SystemActiveErrorModel) and/or does not appear in the System Error Activity model table.

## Escalation Guidance

* If the active error cannot be matched to any SystemErrorDefinition entry, stop and escalate for deeper investigation (the source does not describe how to handle missing definitions).
* If the error remains active after the documented resolution is expected to be applied, stop and escalate (the source only states that resolved errors are archived, not how to force resolution).

## Missing Details / Known Gaps

* The packet does not provide explicit Robotics Database navigation steps (exact UI path/menu/table names beyond the model/table names).
* The packet does not describe how to handle cases where an active error exists but no matching SystemErrorDefinition entry is found (only that you should stop and escalate).
* The packet does not describe how to force resolution or remediate when an error remains active after the documented resolution is expected to be applied (only that you should stop and escalate).

## Source Lineage

- Candidate IDs: candidate_training_video_day2_interpret_system_error_definition_and_active_error_models
- Source ID: `training_video_day2`
- Source Type: `training_video`
