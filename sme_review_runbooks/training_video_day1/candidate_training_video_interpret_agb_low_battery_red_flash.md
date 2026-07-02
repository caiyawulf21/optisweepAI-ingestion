# Interpret Flashing Red On An AGB As Low Battery Requiring Charge

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_flashing_red_on_an_agb_as_low_battery_requiring_charge_v1` |
| Title | Interpret Flashing Red On An AGB As Low Battery Requiring Charge |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training-video indication meaning to recognize that a flashing red AGB corresponds to battery level under 30% and means the unit needs to charge.

## When To Use

Use when an operator or support user observes an AGB flashing red and needs to interpret the indication based on the training source.

## Do Not Use For

* Do not use this runbook as a full charging or recovery procedure.
* Do not use this runbook to infer corrective actions beyond the source-backed meaning that the AGB needs to charge.
* Do not use this runbook to diagnose other red indications not explicitly supported by this source segment.

## Safety And Operational Notes

* This source only supports interpretation of the indication meaning.
* Do not infer additional controls, thresholds, or recovery actions beyond the documented statement.

## Access Or Tools Needed

* Visual access to the AGB status indication
* Training source or documented indication meaning

## Related Operational Context

* ctx_training_video_agb_low_battery_red_flash_v1

## Procedure Steps

### Step 1 — Observe the AGB indication

**Responsible role:** operator

**Instruction:**
Observe the AGB and identify whether it is flashing red.

**Expected result:**
The user determines whether the AGB is flashing red.

**Screens / Images:**

![artifact_training_video_training_video_day1_0049_so_but_yeah_under_30_is_primary_01_51_55_000](assets/22fd5b706f7b051d.jpg)

*Use the training frame associated with the transcript about the flashing red low-battery indication.*


**Stop or Escalate If:**

* Stop or escalate if the indication cannot be clearly observed.
* Escalate if a red flashing indication is observed but does not align with the documented source meaning in the current system context.

---

### Step 2 — Apply the battery threshold meaning

**Responsible role:** operator

**Instruction:**
Use the source-provided threshold that flashing red corresponds to battery level under 30%.

**Expected result:**
The flashing red indication is interpreted as battery under 30%.

**Screens / Images:**

![artifact_training_video_training_video_day1_0049_so_but_yeah_under_30_is_primary_01_51_55_000](assets/22fd5b706f7b051d.jpg)

*Reference the training segment tied to the statement that under 30% the AGB will start flashing red.*


**Stop or Escalate If:**

* Stop if you need a threshold other than the source-backed under-30% meaning.
* Escalate if the observed flashing red condition appears inconsistent with the documented threshold in the current system context.

---

### Step 3 — Interpret the condition as needing charge

**Responsible role:** operator

**Instruction:**
Interpret the flashing red condition as meaning the AGB needs to charge.

**Expected result:**
The user recognizes the flashing red AGB as needing charge.

**Screens / Images:**

![artifact_training_video_training_video_day1_0049_so_but_yeah_under_30_is_primary_01_51_55_000](assets/22fd5b706f7b051d.jpg)

*Use the associated training frame and transcript context for the statement that the AGB needs to charge.*


**Stop or Escalate If:**

* Escalate if a red flashing indication is observed but does not align with the documented source meaning in the current system context.

---

### Step 4 — Record or communicate the interpreted state

**Responsible role:** operator

**Instruction:**
Record or communicate the low-battery charging state using only the source-backed meaning.

**Expected result:**
The condition is communicated as flashing red, under 30% battery, and needing charge.

**Stop or Escalate If:**

* Stop if additional corrective actions are being inferred beyond the source statement that it needs to charge.
* Escalate if the observed indication does not align with the documented source meaning in the current system context.

---

## Success Criteria

* The user identifies that a flashing red AGB indicates battery below 30%.
* The user identifies that the flashing red AGB needs to charge.
* Any communication of the condition stays within the source-backed meaning.

## Failure Conditions

* The AGB indication cannot be clearly observed.
* The flashing red indication is interpreted using unsupported thresholds or meanings.
* Additional corrective actions are inferred beyond the source-backed statement.

## Escalation Guidance

* Escalate if a red flashing indication is observed but does not align with the documented source meaning in the current system context.
* Escalate if the indication cannot be clearly observed or confidently interpreted from the source-backed meaning.

## Missing Details / Known Gaps

* The source does not provide a full charging procedure.
* The source does not provide a required follow-up workflow after identifying the flashing red condition.
* The source does not provide role boundaries beyond operator-level interpretation.
* The supplied artifact is transcript-adjacent and not a clearly visible image of the flashing red AGB indication itself.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_agb_low_battery_red_flash
- Source ID: `training_video_day1`
- Source Type: `training_video`
