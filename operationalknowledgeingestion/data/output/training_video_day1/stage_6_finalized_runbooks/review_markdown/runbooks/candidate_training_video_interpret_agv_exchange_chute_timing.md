# Interpret Chute Opening Timing During An AGV Exchange

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_chute_opening_timing_during_an_agv_exchange_v1` |
| Title | Interpret Chute Opening Timing During An AGV Exchange |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Reference guidance for understanding documented chute opening timing during an AGV tote exchange. The source states that the chute opens when the AGV moves in, not when it drops a tote, and explains that this behavior is intentional to support faster exchanges and strict KPI targets.

## When To Use

Use this reference when observing or reviewing AGV tote exchange behavior and you need to confirm whether chute opening timing matches the documented training explanation.

## Do Not Use For

* Not for defining corrective actions if timing differs from the source description.
* Not for inferring timing thresholds, control logic details, or light-status meanings beyond what the source states.
* Not for operating, maintenance, or fault-recovery steps not described in this source.

## Safety And Operational Notes

* Use observation only; the source does not provide intervention steps.
* Do not infer corrective actions or timing thresholds beyond what the source states.

## Access Or Tools Needed

* Visibility of chute behavior during AGV exchange
* Source training material describing chute timing

## Related Operational Context

* ctx_training_video_chute_open_timing_kpi_reference_v1

## Procedure Steps

### Step 1 — Observe chute timing during the AGV exchange

**Responsible role:** operator

**Instruction:**
Observe the tote exchange and watch for when the chute opens relative to AGV movement.

**Expected result:**
The observer can identify the point in the exchange when the chute opens.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look at the exchange sequence description and chute timing explanation tied to AGV move-in behavior.*


**Stop or Escalate If:**

* Escalate if chute timing does not match the documented behavior in the source.

---

### Step 2 — Check for chute opening on AGV move-in

**Responsible role:** operator

**Instruction:**
Check whether the chute opens when the AGV moves into position rather than waiting until the tote is dropped.

**Expected result:**
The observer can determine whether chute opening aligns with AGV move-in rather than tote drop.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the statement that chute opening occurs when the AGV moves in, not when it drops a tote.*


**Stop or Escalate If:**

* Escalate if chute timing does not match the documented behavior in the source.

---

### Step 3 — Compare observation to documented behavior

**Responsible role:** operator

**Instruction:**
Compare the observed timing to the documented behavior that chute opening occurs when the AGV moves in.

**Expected result:**
The observer can state whether the observed timing matches the documented behavior.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Use the exchange-process frame as the reference for documented chute timing behavior.*


**Stop or Escalate If:**

* Escalate if chute timing does not match the documented behavior in the source.

---

### Step 4 — Record the documented intent of the timing

**Responsible role:** operator

**Instruction:**
Record that this timing is intentional and is described as supporting strict KPI targets for faster exchanges.

**Expected result:**
The observer documents that the timing is intentional per the source and tied to exchange-speed KPI expectations.

**Screens / Images:**

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the explanation that the behavior is on purpose to speed up exchanges and meet strict KPI targets.*


**Stop or Escalate If:**

* Do not infer corrective actions or timing thresholds beyond what the source states.

---

## Success Criteria

* The observer confirms whether chute opening timing matches the documented behavior.
* The observer understands that chute opening on AGV move-in is described as intentional.
* The KPI-related reason for the timing is recorded without adding unsupported interpretation.

## Failure Conditions

* Chute timing does not match the documented behavior in the source.
* The observer cannot determine chute timing relative to AGV movement.
* Additional control logic, thresholds, or corrective actions are inferred without source support.

## Escalation Guidance

* Escalate if chute timing does not match the documented behavior in the source.
* Escalate for SME review if the observed behavior cannot be reconciled with the training explanation.
* Do not propose corrective actions or timing thresholds unless supported by another approved source.

## Missing Details / Known Gaps

* The source does not define the referenced light or provide a formal status mapping.
* The source does not provide corrective actions if observed timing differs.
* The source does not provide timing thresholds, control parameters, or quantitative KPI limits.
* The source does not specify supporting roles beyond the operator-level observation context.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_agv_exchange_chute_timing
- Source ID: `training_video_day1`
- Source Type: `training_video`
