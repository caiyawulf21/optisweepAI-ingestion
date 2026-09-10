# Interpret Disabled RMS Charger Button: Charger Assignment Is Controlled by WCS

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_disabled_rms_charger_button_charger_assignment_controlled_by_wcs_v1` |
| Title | Interpret Disabled RMS Charger Button: Charger Assignment Is Controlled by WCS |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_system_faults` |
| Access Surface | `rms_ui`, `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

If an RMS UI charger-related button appears but is disabled/unusable, the expected explanation is that charger assignment and charging management were transferred to WCS. WCS assigns an AGV to a particular charger; RMS does not assign the charger ID, so the RMS charger UI action cannot be used as before.

## When To Use

Use when you see a charger-related button in the RMS UI that is disabled/unusable and you need to interpret what that means for charger assignment responsibility.

## Do Not Use For

* Do not use this procedure as a WCS-side diagnostic guide for why charger assignment fails after WCS control is confirmed.

## Access Or Tools Needed

* RMS UI access (to observe the charger button state)
* WCS knowledge/engagement (responsibility for charger assignment per source)

## Related Operational Context

* ctx_training_video_charger_assignment_control_in_wcs_v1

## Visual References

![artifact_training_video_training_video_day2_0014_the_robot_command_database_model_table_primary_01_18_59_000](assets/bc80d134a7f69ff3.jpg)

*Training frame showing Robot Command Database model and the 'GoCharge' API call context mentioned in the segment (used as supporting evidence for command/API behavior).*

## Procedure Steps

### Step 1 — Locate the charger-related button in the RMS UI that may be visible but not usable

**Responsible role:** L2_support

**Instruction:**
In the RMS UI, locate the charger-related button that the source indicates may still appear on the UI but is not usable for assigning a charger ID.

**Expected result:**
You can point to the charger-related button in the RMS UI that is present but not usable for charger ID assignment.

---

### Step 2 — Observe whether charger selection/action is disabled (cannot assign charger ID via RMS)

**Responsible role:** L2_support

**Instruction:**
Check whether the charger selection/action is disabled/unusable when you attempt to use the RMS charger-related button to assign a charger ID.

**Expected result:**
The RMS charger-related action is disabled/unusable for assigning a charger ID.

---

### Step 3 — Interpret the behavior using the WCS responsibility split (WCS assigns AGV to charger; RMS does not)

**Responsible role:** L2_support

**Instruction:**
Use the source explanation to interpret the disabled RMS charger UI behavior: WCS is responsible to assign an AGV to a particular charger; RMS does not assign the charger ID even if a button appears on the UI.

**Expected result:**
You can explain that charger assignment is under WCS control, so RMS charger UI actions may be disabled/unusable even when a button appears.

---

### Step 4 — If RMS charger assignment still fails, treat it as expected and escalate for WCS/API investigation

**Responsible role:** L2_support

**Instruction:**
If attempting to use the RMS charger assignment fails, interpret it as expected given the WCS control transfer described in the segment; then escalate for deeper WCS/API investigation because this segment does not provide WCS-side diagnostic steps.

**Expected result:**
You stop pursuing RMS charger ID assignment and escalate for WCS/API investigation when charger assignment still fails.

**Stop or Escalate If:**

* Charger assignment still fails after applying the WCS responsibility interpretation (segment provides no WCS-side diagnostic steps).

---

## Success Criteria

* You can correctly explain that charger assignment is controlled by WCS, so RMS charger UI actions may be disabled/unusable even when a button appears.
* If charger assignment still fails, you escalate for deeper WCS/API investigation rather than continuing RMS-based charger ID assignment attempts.

## Failure Conditions

* RMS charger UI appears enabled/usable for charger ID assignment (contradicting the source responsibility split).
* Charger assignment still fails and the team does not escalate for WCS/API investigation.

## Escalation Guidance

* If charger assignment still fails after confirming the expected RMS disabled/unusable behavior, escalate for deeper WCS/API investigation. This segment does not include WCS-side diagnostic steps.

## Missing Details / Known Gaps

* No WCS-side diagnostic steps are provided in this packet for investigating why charger assignment fails after confirming WCS control.

## Source Lineage

- Candidate IDs: candidate_training_video_reference_charger_assignment_not_via_rms_ui_use_wcs_control
- Source ID: `training_video_day2`
- Source Type: `training_video`
