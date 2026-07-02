# Verify Chute Unavailable State When A Tote Is Full

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_chute_unavailable_state_when_a_tote_is_full_v1` |
| Title | Verify Chute Unavailable State When A Tote Is Full |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-based reference check to confirm the documented relationship between a tote reaching the Full state and the chute being marked unavailable so packages do not continue coming down during an exchange.

## When To Use

Use when interpreting or verifying the documented system state for tote exchange conditions, specifically to confirm that a full tote corresponds to a chute-unavailable state intended to prevent additional packages from coming down during an exchange.

## Do Not Use For

* Do not use as a full tote exchange workflow.
* Do not use to determine the mechanism, interface, or corrective steps for how Chat is informed, because the source does not provide them.
* Do not use as a troubleshooting or repair procedure beyond comparing observed behavior to the documented relationship.

## Safety And Operational Notes

* This candidate is a procedural interpretation/reference and not a physical exchange procedure.
* Use only the source-provided wording for the full-tote and chute-unavailable relationship.
* Do not invent undocumented controls, interfaces, or corrective actions.

## Access Or Tools Needed

* Access to the documented tote and chute state information

## Related Operational Context

* ctx_training_video_chute_unavailable_on_full_tote_v1
* ctx_training_video_tote_fill_thresholds_v1

## Procedure Steps

### Step 1 — Identify the tote Full state

**Responsible role:** operator

**Instruction:**
Identify that the tote has reached the source-defined "Full" state rather than only "Pretty full."

**Expected result:**
The tote condition is recognized as Full according to the source thresholds.

**Screens / Images:**

![artifact_training_video_training_video_day1_0012_one_question_previous_like_the_two_primary_00_19_06_000](assets/c436919ae7797e5f.jpg)

*The slide text describing the two thresholds: "Pretty full" and "Full," and the wording that Full means no more product can be diverted until an exchange is done.*


**Stop or Escalate If:**

* Stop or escalate if the tote cannot be confirmed as being in the Full state using the source-supported thresholds.

---

### Step 2 — Check the documented chute unavailable behavior

**Responsible role:** operator

**Instruction:**
Check the documented system behavior that when a tote is full, Chat is told that the chute is unavailable.

**Expected result:**
The documented relationship between a full tote and chute unavailable is confirmed from the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0012_one_question_previous_like_the_two_primary_00_19_06_000](assets/c436919ae7797e5f.jpg)

*The statement on the slide that when a tote is full, the system tells Chat that the chute is unavailable.*


**Stop or Escalate If:**

* Escalate if the observed system behavior does not align with the documented full-tote and chute-unavailable relationship.

---

### Step 3 — Verify the intended meaning of chute unavailable

**Responsible role:** operator

**Instruction:**
Verify that the expected meaning of chute unavailable is that packages should not continue coming down while doing an exchange.

**Expected result:**
The chute unavailable state is understood as preventing packages from continuing to come down during the exchange.

**Screens / Images:**

![artifact_training_video_training_video_day1_0012_one_question_previous_like_the_two_primary_00_19_06_000](assets/c436919ae7797e5f.jpg)

*The wording that the chute is unavailable so that no packages come down while doing an exchange.*


**Stop or Escalate If:**

* Escalate if observed behavior does not align with the documented intent that no packages should come down during an exchange.

---

### Step 4 — Record the source-grounded relationship

**Responsible role:** operator

**Instruction:**
Record that the chute-unavailable state is tied to the full tote condition, using only the source-provided wording.

**Expected result:**
A source-grounded note is captured that a full tote causes the chute to be unavailable so packages do not continue coming down during an exchange.

**Screens / Images:**

![artifact_training_video_training_video_day1_0012_one_question_previous_like_the_two_primary_00_19_06_000](assets/c436919ae7797e5f.jpg)

*The slide section showing the statement that a full tote makes the chute unavailable during exchange.*


**Stop or Escalate If:**

* Stop if documenting the condition would require adding unsupported mechanism, interface, or corrective steps.
* Escalate if the observed system behavior does not align with the documented full-tote and chute-unavailable relationship.

---

## Success Criteria

* The user confirms from the source that a tote in the Full state is associated with the chute being marked unavailable.
* The user confirms from the source that the purpose of chute unavailable is to prevent packages from coming down during an exchange.
* The interpretation is documented using only source-supported wording.

## Failure Conditions

* The tote cannot be confirmed as Full using the source-supported thresholds.
* Observed behavior does not align with the documented relationship between full tote and chute unavailable.
* The interpretation requires unsupported assumptions about how Chat is informed or how the system should be corrected.

## Escalation Guidance

* Escalate if the observed system behavior does not align with the documented full-tote and chute-unavailable relationship.
* Escalate if additional mechanism, interface, or corrective detail is needed, because the source does not provide it.

## Missing Details / Known Gaps

* The source does not provide the mechanism or interface by which Chat is informed that the chute is unavailable.
* The source does not provide corrective actions if observed behavior does not match the documented relationship.
* The source does not provide a full tote exchange workflow in this candidate.
* The source does not provide a time estimate for performing this verification.

## Source Lineage

- Candidate IDs: candidate_training_video_verify_chute_unavailable_when_tote_full
- Source ID: `training_video_day1`
- Source Type: `training_video`
