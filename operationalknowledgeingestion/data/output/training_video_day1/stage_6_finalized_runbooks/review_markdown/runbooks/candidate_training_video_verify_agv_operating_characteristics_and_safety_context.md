# Verify AGV Operating Characteristics And Safety Context From Training Material

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_agv_operating_characteristics_and_safety_context_from_training_material_v1` |
| Title | Verify AGV Operating Characteristics And Safety Context From Training Material |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training material to verify documented AGV operating characteristics relevant to movement guidance and safety context. This runbook is limited to confirming what the training source states: AGVs operate over QR codes, are directly controlled by Geek+ RMS, Geek+ handles movement and route determination, AGVs have forward collision sensors, and this version is intended to operate in a fenced system.

## When To Use

Use when you need to confirm the AGV operating characteristics and safety-related context exactly as documented in the supplied training material, especially for reference, documentation verification, or training review.

## Do Not Use For

* Do not use this runbook to infer additional safety procedures, controls, or behaviors not explicitly stated in the training source.
* Do not use this runbook as a field troubleshooting or corrective-action procedure.
* Do not use the fenced-system statement alone to derive undocumented safety rules.

## Safety And Operational Notes

* This runbook is reference-only and does not authorize system changes or guarded-area actions.
* The source states this AGV version is intended to operate in a fenced system.
* Do not infer additional safety procedures from the fenced-system statement alone.
* Escalate if observed field behavior appears inconsistent with the documented training description, because the source is a high-level training segment only.

## Access Or Tools Needed

* Access to the training slide or artifact
* Ability to review AGV training content

## Related Operational Context

* ctx_training_video_agv_rms_system_overview_v1
* ctx_training_video_agv_safety_fenced_system_v1

## Procedure Steps

### Step 1 — Review the AGV training slide

**Responsible role:** operator

**Instruction:**
Open and review the training slide or artifact covering automated guided vehicles and Geek+ RMS responsibilities.

**Expected result:**
The relevant training slide or frame is available for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*Slide text and discussion describing AGV operating characteristics and Geek+ RMS responsibilities.*


**Stop or Escalate If:**

* The training artifact is unavailable.
* The artifact does not contain the AGV characteristic statements needed for verification.

---

### Step 2 — Confirm QR-code operation

**Responsible role:** operator

**Instruction:**
Confirm that the training material states the AGVs operate over QR codes.

**Expected result:**
The AGV navigation characteristic is verified exactly as documented.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*Text stating that Geek+ AGVs operate over QR codes.*


**Stop or Escalate If:**

* The QR-code operation statement cannot be found in the supplied source.

---

### Step 3 — Confirm RMS direct control and movement responsibility

**Responsible role:** operator

**Instruction:**
Confirm that the training material states the AGVs are directly controlled by Geek+ RMS and that Geek+ handles all movement. Also verify that the system determines the best route from point A to point B when that statement is present in the same source content.

**Expected result:**
The RMS control and movement responsibility statements are verified exactly as documented.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*Text describing direct Geek+ RMS control, movement handling, and route determination.*


**Stop or Escalate If:**

* The source wording about RMS control or movement responsibility is unclear.
* Observed field behavior appears inconsistent with the documented training description.

---

### Step 4 — Confirm forward collision sensors

**Responsible role:** operator

**Instruction:**
Check that the training slide states the AGVs have forward collision sensors.

**Expected result:**
The forward collision sensor statement is verified exactly as documented.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*Training slide text listing AGV characteristics including forward collision sensors.*


**Stop or Escalate If:**

* The forward collision sensor statement cannot be confirmed from the supplied source.
* Observed field behavior appears inconsistent with the documented training description.

---

### Step 5 — Confirm fenced-system intent

**Responsible role:** operator

**Instruction:**
Check that the training slide states this AGV version is intended to operate in a fenced system.

**Expected result:**
The fenced-system statement is verified exactly as documented.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*Text stating that this AGV version is intended to operate in a fenced system.*


**Stop or Escalate If:**

* The fenced-system statement cannot be confirmed from the supplied source.
* Additional safety rules are being inferred beyond what the source states.

---

### Step 6 — Record the verified characteristics exactly as documented

**Responsible role:** operator

**Instruction:**
Record the verified operating characteristics exactly as documented in the training source without adding undocumented safety rules, behaviors, commands, or controls.

**Expected result:**
A source-faithful record of the AGV operating characteristics is produced.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*The full set of AGV characteristic statements to be transcribed accurately.*


**Stop or Escalate If:**

* There is uncertainty about whether a statement is explicitly supported by the source.
* Observed field behavior appears inconsistent with the documented training description, because the source is a high-level training segment only.

---

## Success Criteria

* The training source has been reviewed.
* The following characteristics are verified from the source: AGVs operate over QR codes; AGVs are directly controlled by Geek+ RMS; Geek+ handles all movement; the system determines the best route from point A to point B; AGVs have forward collision sensors; this version is intended to operate in a fenced system.
* The verified characteristics are recorded exactly as documented without unsupported additions.

## Failure Conditions

* The required training artifact cannot be accessed.
* One or more AGV characteristic statements cannot be confirmed from the supplied source.
* Recorded notes include unsupported interpretation or undocumented safety rules.
* Observed field behavior appears inconsistent with the documented training description.

## Escalation Guidance

* Escalate if field behavior appears inconsistent with the documented training description, because the source is a high-level training segment only.
* Escalate if any required AGV characteristic cannot be confirmed from the supplied source artifact.
* Escalate for SME review if additional safety procedures or operational controls are needed beyond what this training source states.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not define supporting roles beyond the operator-level verification use case.
* The source is a high-level training segment and does not provide field validation steps beyond reviewing the documented statements.
* The source does not provide commands, system paths, or corrective actions.

## Source Lineage

- Candidate IDs: candidate_training_video_verify_agv_operating_characteristics_and_safety_context
- Source ID: `training_video_day1`
- Source Type: `training_video`
