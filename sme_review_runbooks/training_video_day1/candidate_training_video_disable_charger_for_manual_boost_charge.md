# Logically Disable A Charger To Reserve It For Manual AGV Boost Charging

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_logically_disable_a_charger_to_reserve_it_for_manual_agv_boost_charging_v1` |
| Title | Logically Disable A Charger To Reserve It For Manual AGV Boost Charging |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Charger Selection view to logically disable a charger so RMS and WCS do not allocate other AGVs to that charging location while a very low-power AGV is manually moved there for a charging boost. The source states this is a logical allocation control and not a hardware power-off.

## When To Use

Use when an AGV is extremely low on power and needs manual charging assistance by being physically moved to a charger that must be reserved from normal AGV allocation.

## Do Not Use For

* Do not use this procedure as a hardware charger shutdown.
* Do not use this procedure when site-specific physical movement or charger access safety controls are required but not defined in the source.
* Do not use this procedure if the charger disable action does not logically prevent AGV allocation as described by the source.

## Safety And Operational Notes

* Disabling the charger is a logical control only; it does not kill charger hardware.
* The procedure involves physically moving an AGV, so additional site-specific safety controls may apply but are not described in the source.
* Stop and escalate if physical movement of the AGV or charger access requires safety controls not covered by the source.

## Access Or Tools Needed

* Access to the Charger Selection screen
* Ability to select a charger by charger ID
* Access to the disable and enable charger controls
* Physical access to the AGV and charging location

## Related Operational Context

* ctx_training_video_charger_selection_screen_v1
* ctx_training_video_disabled_charger_status_v1
* ctx_training_video_manual_charging_use_case_v1
* ctx_training_video_charging_control_architecture_v1

## Procedure Steps

### Step 1 — Open Charger Selection and select the target charger

**Responsible role:** L2_support

**Instruction:**
Open the Charger Selection view and select the desired charger using its unique charger ID.

**Expected result:**
The selected charger record is displayed in Charger Selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Charger Selection screen showing charger ID selection and charger details.*


**Stop or Escalate If:**

* Stop and escalate if the correct charger cannot be identified by charger ID.

---

### Step 2 — Verify charger status and associated robot

**Responsible role:** L2_support

**Instruction:**
Review the selected charger details and verify the charger status, whether it is enabled or disabled, and which robot is currently associated with that charger before making any change.

**Expected result:**
The current charger state and associated robot information are confirmed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Charger Selection details showing charger status, enabled/disabled state, and which robot is on the charger.*


**Stop or Escalate If:**

* Stop and escalate if charger status or associated robot information cannot be confirmed.

---

### Step 3 — Disable the charger logically

**Responsible role:** L2_support

**Instruction:**
Use the disable function for the selected charger in Charger Selection.

**Expected result:**
The charger is placed into a disabled state for allocation control.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Charger Selection screen area showing the disable charger function.*


**Stop or Escalate If:**

* Stop and escalate if the disable action does not complete or the charger does not show a disabled state.
* Do not proceed if the action is being treated as a hardware power-off.

---

### Step 4 — Confirm allocation is blocked for the disabled charger

**Responsible role:** L2_support

**Instruction:**
Confirm the charger is logically disabled so RMS will not route AGVs to that charging location.

**Expected result:**
The charger is reserved from normal AGV allocation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Disabled charger status in Charger Selection and related charger state information.*


**Stop or Escalate If:**

* Stop and escalate if the charger disable action does not logically prevent allocation as described in the source.

---

### Step 5 — Move the low-power AGV to the reserved charger for boost charging

**Responsible role:** L2_support

**Instruction:**
Physically move the low-power AGV to the disabled charging location for a charging boost, as described by the source.

**Expected result:**
The intended AGV is positioned at the reserved charger for manual charging assistance.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Training explanation that a disabled charger can be used so the desired AGV can be pushed into that charging station.*


**Stop or Escalate If:**

* Stop and escalate if physical movement of the AGV or charger access requires site-specific safety controls not described in the source.

---

### Step 6 — Re-enable the charger after manual charging is complete

**Responsible role:** L2_support

**Instruction:**
After the charging boost is complete and the AGV is removed, re-enable the charging location so RMS and WCS can again assign AGVs in the charging queue to use that charger.

**Expected result:**
The charger is returned to normal allocation and can be reused by the system.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Charger Selection context for returning the charger from disabled to enabled state.*


**Stop or Escalate If:**

* Stop and escalate if the charger cannot be re-enabled or normal charger reuse does not resume.

---

## Success Criteria

* The selected charger is logically disabled and not allocated to other AGVs during the manual charging activity.
* The low-power AGV is able to use the reserved charging location for a charging boost.
* After recovery, the charger is re-enabled and returned to normal use.

## Failure Conditions

* The charger disable action does not logically prevent allocation as described in the source.
* The disable action is misinterpreted as a hardware power-off.
* Physical movement of the AGV or charger access requires site-specific safety controls not described in the source.
* The charger cannot be re-enabled for normal reuse after the manual charging activity.

## Escalation Guidance

* Escalate if the charger disable action does not logically prevent AGV allocation.
* Escalate if safe physical movement of the AGV cannot be performed under documented site controls.
* Escalate if charger state cannot be confirmed in Charger Selection.
* Escalate if the charger cannot be returned to enabled status after use.

## Missing Details / Known Gaps

* The source does not provide exact button labels or confirmation prompts for disable or enable actions.
* The source does not define detailed physical safety controls for manually moving the AGV.
* The source does not provide a formal verification method beyond the stated logical behavior that RMS will not route AGVs to the disabled charger.
* The source does not provide a time estimate for the procedure.
* The source does not specify whether additional personnel are required for physical AGV movement.

## Source Lineage

- Candidate IDs: candidate_training_video_disable_charger_for_manual_boost_charge
- Source ID: `training_video_day1`
- Source Type: `training_video`
