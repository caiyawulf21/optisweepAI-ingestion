# Explain and Verify 'Disabled' Sorter Side Entries Based on CSV Phase Configuration and Phase-Based Enable

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_explain_verify_disabled_sorter_side_entries_csv_phase_configuration_v1` |
| Title | Explain and Verify 'Disabled' Sorter Side Entries Based on CSV Phase Configuration and Phase-Based Enable |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `zone_config_state`, `sorter_item_or_scan_state` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `pairing_failure`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the live sorter-side configuration/state in the OptiSweep/WCS/Robotics database to explain why a sorter side (example: sorter 2B) appears disabled: the initial CSV configuration populates the database and disables anything not in phase one. Then verify whether a later phase-based database update/script has been applied that would enable the sorter side for its later phase (example: enabling phase 4).

## When To Use

When a sorter side entry (e.g., sorter 2B) is showing as disabled in the live sorter-side configuration/state, and you need to determine whether that disabled state is expected due to phase-based CSV configuration (phase one vs later phases) and whether a later phase enablement update has been applied.

## Do Not Use For

* Do not perform mutating database/config changes as part of this diagnostic unless a separate approved procedure exists.

## Safety And Operational Notes

* This is a diagnostic procedure. Do not perform mutating database/config changes as part of this diagnostic unless a separate approved procedure exists.

## Access Or Tools Needed

* Robotics/WCS database access to view sorter side configuration/status (SSMS/Helix/WCS DB as applicable)
* Access to configuration/phase-based update evidence (as available in the environment)

## Related Operational Context

* ctx_training_video_sorter_side_disabled_status_v1

## Visual References

![artifact_training_video_training_video_day2_0011_so_all_right_we_ll_move_primary_00_26_58_500](assets/566cf64c9e45d275.jpg)

*Training frame showing the explanation that sorter sides are disabled when not in phase one, and that a later database update can enable phase 4 (includes example sorter 2B).*

![artifact_training_video_training_video_day2_0009_the_robot_location_database_model_table_primary_00_17_15_500](assets/e6b308f21a2ed402.jpg)

*Training frame describing the SorterSideDatabaseModel fields including whether the sorter side is disabled.*

## Procedure Steps

### Step 1 — Locate the sorter side entry that is showing as disabled (example: sorter 2B)

**Responsible role:** L2_support

**Instruction:**
Using your live WCS/Robotics database access (SSMS/Helix/WCS DB as applicable), locate the sorter-side record corresponding to the sorter side that is currently disabled (example mentioned: sorter 2B). The sorter-side model includes a disabled/not-disabled attribute.

**Expected result:**
The sorter-side record you locate for the target sorter side (e.g., sorter 2B) shows it is disabled in the live database model.

---

### Step 2 — Confirm the phase rule: CSV populates the database and anything not in phase one is disabled

**Responsible role:** L2_support

**Instruction:**
In your live investigation, use the source-backed rule to interpret the disabled state: confirm that the environment’s initial configuration mechanism is CSV-based population and that entries not in phase one are disabled until later phase enablement.

**Expected result:**
You can justify the disabled state using the rule: disabled sorter sides are those not included in phase one of the CSV-based configuration.

---

### Step 3 — Identify whether the sorter side belongs to a later phase (example: phase 4) rather than phase one

**Responsible role:** L2_support

**Instruction:**
Using the live database/configuration data you have access to, determine the phase association for the target sorter side (example discussed: sorter 2B being disabled until its phase is enabled; later phase example given: enabling phase 4).

**Expected result:**
You identify that the target sorter side is associated with a later phase (not phase one), consistent with why it is disabled.

---

### Step 4 — Verify whether a phase-based database update/script has been applied to enable the later phase

**Responsible role:** L2_support

**Instruction:**
If the environment supports it and you have access to configuration/update evidence, check for evidence that the phase-based enablement update/script for the relevant later phase (example: phase 4) has been applied.

**Expected result:**
You find evidence that the later phase enablement update/script has been applied (example: phase 4 enablement), which should correspond to the sorter side no longer being disabled.

**Stop or Escalate If:**

* If the sorter side remains disabled after the relevant phase-based enablement is confirmed, stop and escalate for deeper configuration/database troubleshooting.

---

### Step 5 — Record the observed evidence and expected enablement outcome

**Responsible role:** L2_support

**Instruction:**
Record what you observed in the live database: (1) the sorter side is disabled, (2) it is not in phase one (belongs to a later phase), and (3) whether the later phase enablement update/script evidence exists (example: phase 4).

**Expected result:**
A clear diagnostic justification is recorded: the sorter side is disabled due to phase-based CSV configuration and should become enabled after the relevant phase-based update.

---

## Success Criteria

* You can point to the live sorter-side record showing it is disabled.
* You can justify the disabled state using the CSV/phase-one mechanism (disabled because not in phase one).
* You can identify the sorter side as belonging to a later phase (example: phase 4) and check for evidence that the phase-based enablement update/script was applied.
* If enablement evidence exists and the sorter side still remains disabled, you stop and escalate for deeper configuration/database troubleshooting.

## Failure Conditions

* Sorter side remains disabled even after the relevant phase-based enablement is confirmed.
* Phase association for the sorter side cannot be determined from available live evidence.
* Sorter side appears to be in phase one but is still disabled.

## Escalation Guidance

* If the sorter side remains disabled after the relevant phase-based enablement is confirmed, stop and escalate for deeper configuration/database troubleshooting.
* Do not perform mutating database/config changes as part of this diagnostic unless a separate approved procedure exists.

## Missing Details / Known Gaps

* The packet does not provide explicit live table/column names or the exact live UI/SSMS query path for the sorter-side disabled status; it only states the concept exists in the SorterSideDatabaseModel.
* The packet does not provide explicit phase association fields/columns for sorter sides; it only provides the phase-one vs later-phase rule and an example (phase 4).
* The packet does not provide explicit database update history locations or a specific evidence table/log for confirming that the phase-based enablement script was applied.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_sorter_side_disabled_phase_configuration_csv_enable_phase
- Source ID: `training_video_day2`
- Source Type: `training_video`
