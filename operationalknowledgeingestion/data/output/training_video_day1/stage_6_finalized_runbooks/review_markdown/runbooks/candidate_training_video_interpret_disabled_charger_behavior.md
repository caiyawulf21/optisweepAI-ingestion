# Interpret What A Disabled Charger Means In OptiSweep Charging Control

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_what_a_disabled_charger_means_in_optisweep_charging_control_v1` |
| Title | Interpret What A Disabled Charger Means In OptiSweep Charging Control |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

This source-backed reference explains that a disabled charger in the Charger Selection view is a logical allocation state, not a hardware power-off. A disabled charger remains physically present but is marked unavailable for AGV allocation, so RMS will not route AGVs to that charging location. When the charger is enabled again, the station can be reused for AGVs in the charging queue.

## When To Use

Use this reference when reviewing charger status in the Charger Selection view and you need to correctly interpret what enabled versus disabled means for OptiSweep charging behavior and AGV allocation.

## Do Not Use For

* Do not use this runbook to conclude that charger hardware power has been shut off.
* Do not use this runbook to infer undocumented hardware effects from the disabled state.
* Do not use this runbook as a physical charger repair or electrical shutdown procedure.

## Safety And Operational Notes

* The source states that disabling a charger does not kill the charger itself; do not assume a disabled state means hardware shutdown.
* Do not assume undocumented hardware behavior from the enabled or disabled state.

## Access Or Tools Needed

* Access to the Charger Selection screen
* Documented understanding of charger enabled and disabled meanings

## Related Operational Context

* ctx_training_video_disabled_charger_status_v1
* ctx_training_video_charging_control_architecture_v1

## Procedure Steps

### Step 1 — Open Charger Selection and locate the charger

**Responsible role:** L1_support

**Instruction:**
Open the Charger Selection view and locate the charger of interest by its unique charger ID.

**Expected result:**
The target charger is visible in the Charger Selection view.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Charger Selection screen showing charger identification by unique charger ID.*


**Stop or Escalate If:**

* Escalate if the charger of interest cannot be identified in the Charger Selection view.

---

### Step 2 — Check whether the charger is enabled or disabled

**Responsible role:** L1_support

**Instruction:**
Check whether the charger is shown as enabled or disabled in the Charger Selection view.

**Expected result:**
The displayed charger state is identified as enabled or disabled.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Charger Selection screen showing charger status and disable function.*


**Stop or Escalate If:**

* Escalate if the charger status cannot be determined from the Charger Selection view.

---

### Step 3 — Interpret disabled as a logical allocation state

**Responsible role:** L1_support

**Instruction:**
Interpret a disabled charger state as a logical allocation control in OptiSweep charging behavior, not as a hardware shutdown of the charger itself.

**Expected result:**
The disabled state is understood as logical unavailability rather than physical power loss.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Training explanation that disable does not kill the charger itself.*


**Stop or Escalate If:**

* Stop and correct the interpretation if anyone assumes the disabled state means charger hardware shutdown.
* Escalate if observed system behavior appears inconsistent with the documented meaning.

---

### Step 4 — Interpret routing impact of a disabled charger

**Responsible role:** L1_support

**Instruction:**
Use the documented source meaning to conclude that RMS will not route AGVs to a charger that is disabled.

**Expected result:**
The routing consequence of the disabled state is correctly understood.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Training explanation that RMS will not route AGVs to a disabled charging location.*


**Stop or Escalate If:**

* Escalate if observed routing behavior does not match the documented statement that RMS will not route AGVs to a disabled charging location.

---

### Step 5 — Interpret enabled as allowing charger reuse

**Responsible role:** L1_support

**Instruction:**
When the charger is later shown as enabled again, interpret that state as allowing the station to be reused for AGVs in the charging queue.

**Expected result:**
The enabled state is understood as restoring charger availability for reuse.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Training explanation that enabling the charger allows the station to be reused.*


**Stop or Escalate If:**

* Escalate if the charger is shown as enabled but system behavior does not reflect reuse availability.

---

### Step 6 — Record the charger state meaning accurately

**Responsible role:** L1_support

**Instruction:**
Record or communicate the charger state meaning accurately without assuming undocumented hardware behavior.

**Expected result:**
The charger state is documented or communicated using the source-backed interpretation only.

**Stop or Escalate If:**

* Escalate if observed behavior does not match the documented meaning of disabled or enabled charger states.
* Do not proceed with unsupported conclusions about hardware effects.

---

## Success Criteria

* The user correctly interprets a disabled charger as logically unavailable for AGV allocation rather than physically powered off.
* The user correctly understands that RMS will not route AGVs to a disabled charging location.
* The user correctly understands that an enabled charger can be reused for AGVs in the charging queue.
* Support notes and communication avoid unsupported assumptions about charger hardware behavior.

## Failure Conditions

* The disabled state is interpreted as charger hardware shutdown.
* A disabled charger is assumed to remain available for AGV routing.
* An enabled charger is assumed to remain unavailable for reuse.
* Observed system behavior does not match the documented meaning of enabled or disabled charger states.

## Escalation Guidance

* Escalate if the observed system behavior does not match the documented meaning of disabled or enabled charger states.
* Escalate if charger status cannot be determined from the Charger Selection view.
* Do not assume undocumented hardware effects from the disabled state.

## Missing Details / Known Gaps

* The source does not provide a formal time estimate for this reference procedure.
* The source does not define additional supporting roles or approval boundaries for this interpretation task.
* The source does not provide a documented command, API call, or log query for verifying charger state.
* The source does not provide explicit UI field names beyond the Charger Selection view and charger status concepts.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_disabled_charger_behavior
- Source ID: `training_video_day1`
- Source Type: `training_video`
