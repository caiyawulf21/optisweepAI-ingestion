# Determine Whether Hospital Use Matches Reject Handling or AGV Initialization

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_determine_whether_hospital_use_matches_reject_handling_or_agv_initialization_v1` |
| Title | Determine Whether Hospital Use Matches Reject Handling or AGV Initialization |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training explanation of hospital purpose to interpret why an AGV is being routed through the hospital area. The source describes hospital use for reject handling when an AGV cannot tip, for initializing new AGVs, and as a home-base style location, so hospital routing alone should not be interpreted as meaning the AGV is "sick."

## When To Use

Use when an AGV is observed or reported as being routed through the hospital area and the user needs to interpret whether that routing matches the training-described purposes of reject handling, initialization of a new AGV, or home-base style handling.

## Do Not Use For

* Do not use this runbook to diagnose a specific AGV fault state beyond the source-described meanings of hospital use.
* Do not use this runbook to conclude that an AGV is "sick" based only on hospital routing.
* Do not use this runbook as a corrective recovery procedure, because the source provides interpretation of hospital purpose rather than a full corrective workflow.

## Safety And Operational Notes

* This is an interpretive reference procedure only; the source does not provide physical intervention steps.
* Do not assume undocumented fault states from hospital routing alone.

## Access Or Tools Needed

* Access to the training explanation of hospital purpose
* Ability to observe or confirm that the AGV is routed through the hospital area

## Related Operational Context

* ctx_training_video_hospital_reject_and_home_base_v1

## Procedure Steps

### Step 1 — Confirm hospital routing is the observed condition

**Responsible role:** L1_support

**Instruction:**
Identify that the AGV is being routed through the hospital area rather than directly tipping or charging.

**Expected result:**
The observed condition is confirmed as hospital routing.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Hospital area and queue flow relative to tipper and charger areas.*


**Stop or Escalate If:**

* Stop interpretation if hospital routing cannot be confirmed.

---

### Step 2 — Compare the situation to source-described hospital purposes

**Responsible role:** L1_support

**Instruction:**
Compare the observed situation to the source-described hospital purposes: reject handling when an AGV cannot tip at the tipper, initialization of a new AGV, or home-base style handling.

**Expected result:**
The observed hospital routing is compared against the source-supported reasons for hospital use.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Hospital flow depiction and training context describing reject handling, initialization, and home-base behavior.*


**Stop or Escalate If:**

* Escalate if hospital routing is observed but does not align with the source-described reject or initialization/home-base uses.

---

### Step 3 — Confirm hospital use does not by itself indicate a sick AGV

**Responsible role:** L1_support

**Instruction:**
Verify from the source wording that hospital use does not by itself mean the AGV is "sick."

**Expected result:**
The interpretation remains limited to the source-supported meanings of hospital use.

**Stop or Escalate If:**

* Stop interpretation if the only basis for concluding the AGV is "sick" is that it is routed through the hospital.

---

### Step 4 — Record the source-supported interpretation

**Responsible role:** L1_support

**Instruction:**
Record whether the observed hospital use appears to match reject-related handling or initialization/home-base behavior.

**Expected result:**
A source-supported interpretation is documented.

**Stop or Escalate If:**

* Escalate if no source-supported interpretation can be documented.

---

### Step 5 — Escalate when hospital routing does not match source-described purposes

**Responsible role:** L1_support

**Instruction:**
If the observed reason for hospital routing cannot be matched to the source-described purposes, stop interpretation and escalate.

**Expected result:**
Unsupported interpretations are stopped and the issue is escalated for further review.

**Stop or Escalate If:**

* Hospital routing is observed but does not align with the source-described reject or initialization/home-base uses.
* Additional conclusions would require information not present in the source.

---

## Success Criteria

* The observed hospital routing is interpreted using only the source-described meanings of reject handling, initialization of a new AGV, or home-base style handling.
* No unsupported conclusion is made that hospital routing alone means the AGV is "sick."
* Cases that do not match the source-described purposes are escalated.

## Failure Conditions

* Hospital routing cannot be matched to any source-described purpose.
* Hospital routing is interpreted as a sickness indicator without source support.
* The observed condition cannot be confirmed as hospital routing.

## Escalation Guidance

* Escalate if hospital routing is observed but does not align with the source-described reject or initialization/home-base uses.
* Escalate if additional diagnosis is needed beyond the training source's interpretive explanation.

## Missing Details / Known Gaps

* The source does not provide a formal logging location or documentation format for recording the interpretation.
* The source does not define a specific escalation target or routing path.
* The source does not provide corrective actions for hospital-routed AGVs in this segment.
* The source section text field is empty in the packet, so grounding relies on candidate refs, artifact retrieval text, and context records.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_hospital_use_for_reject_and_initialization
- Source ID: `training_video_day1`
- Source Type: `training_video`
