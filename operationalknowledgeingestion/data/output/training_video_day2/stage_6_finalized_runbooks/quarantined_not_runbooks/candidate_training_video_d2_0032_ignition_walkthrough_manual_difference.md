# Use the Ignition Walkthrough context to clarify what a referenced “manual” differs from

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_ignition_walkthrough_context_to_clarify_manual_contrast_v1` |
| Title | Use the Ignition Walkthrough context to clarify what a referenced “manual” differs from |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | None |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When a Day 2 support discussion references a “manual” and then says it is different from what it is now, use the Ignition walkthrough context labeled “Ignition Walkthrough 120” to identify the current Ignition-based interface meaning being contrasted—rather than assuming the earlier “manual” reference refers to the same live surface.

## When To Use

Use during live support when a customer or internal speaker references a “manual” and then states that what it is now is different, and the segment includes an Ignition walkthrough context label (e.g., “Ignition Walkthrough 120”).

## Do Not Use For

* Do not use this procedure to determine the operational steps of the “manual” itself, because the segment does not name the manual or specify which live Ignition screen/controls it refers to beyond the contrast sentence.

## Access Or Tools Needed

* Training video playback for segment around 02:44:45–02:44:50
* Ability to view/confirm the “Ignition Walkthrough 120” frame

## Related Operational Context

* ctx_training_video_ignition_walkthrough_reference_v1
* ctx_training_video_manual_reference_discussion_v1

## Visual References

![artifact_training_video_training_video_day2_0032_so_you_mentioned_a_manual_but_primary_02_44_47_500](assets/a539cf26f0cab0e0.jpg)

*Frame showing the Ignition walkthrough context label “Ignition Walkthrough 120” and the contrast sentence: “So you mentioned a manual, but what that is now it's different from”.*

## Procedure Steps

### Step 1 — Locate the Ignition walkthrough reference in the segment

**Responsible role:** L1_support

**Instruction:**
In the referenced Day 2 segment, find the frame labeled “Ignition Walkthrough 120”.

**Expected result:**
You can point to the frame where the OCR text reads “Ignition Walkthrough 120”.

**Stop or Escalate If:**

* If the segment you have does not show “Ignition Walkthrough 120”, stop and request the correct segment/frame that contains the walkthrough label.

---

### Step 2 — Confirm the exact contrast statement about “manual” vs what it is now

**Responsible role:** L1_support

**Instruction:**
Listen to/confirm the contrast sentence in the segment: “So you mentioned a manual, but what that is now it's different from”.

**Expected result:**
You can quote or paraphrase the contrast sentence exactly as it appears in the segment transcript.

**Stop or Escalate If:**

* If you cannot confirm the contrast sentence, stop and request the correct segment/time range.

---

### Step 3 — Identify the live Ignition-based meaning being contrasted

**Responsible role:** L1_support

**Instruction:**
Treat the Ignition walkthrough context labeled “Ignition Walkthrough 120” as the current/updated Ignition-based interface meaning being contrasted against the earlier “manual” reference.

**Expected result:**
Your clarification states that the earlier “manual” reference is not the same as the current Ignition walkthrough context labeled “Ignition Walkthrough 120”.

**Stop or Escalate If:**

* If the segment does not specify what the “manual” is (which live surface/controls) or what it differs from beyond the single contrast sentence, stop and seek the next/previous segment that contains the missing details.

---

### Step 4 — Record the clarification you can support from the segment

**Responsible role:** L1_support

**Instruction:**
Record a clarification that the “manual” reference is not the same as the current Ignition walkthrough context shown in “Ignition Walkthrough 120”. Do not add details about what the “manual” specifically is unless another segment provides it.

**Expected result:**
Your recorded clarification contains only: (1) the existence of a “manual” reference, (2) the contrast sentence, and (3) the anchor that “what it is now” corresponds to “Ignition Walkthrough 120”.

**Stop or Escalate If:**

* If you need the specific identity of the “manual” or the exact difference beyond the contrast sentence, stop and request the next/previous segment.

---

## Success Criteria

* You can identify the Ignition walkthrough context label “Ignition Walkthrough 120” in the segment.
* You can confirm the contrast sentence: “So you mentioned a manual, but what that is now it's different from”.
* Your clarification states that the earlier “manual” reference is different from (not the same as) the current Ignition walkthrough context anchored by “Ignition Walkthrough 120”.

## Failure Conditions

* The segment does not include the “Ignition Walkthrough 120” label.
* The segment does not include the contrast sentence.
* You assert a specific “manual” identity or specific Ignition controls that are not named in the segment.

## Escalation Guidance

* If the training segment does not specify what the “manual” is or what it differs from beyond the single contrast sentence, stop and seek the next/previous segment that contains the missing details.

## Missing Details / Known Gaps

* The segment does not name the earlier “manual” reference (what it is, which live Ignition screen/controls it corresponds to).
* The segment does not specify the exact operational difference beyond the single contrast sentence.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_0032_ignition_walkthrough_manual_difference
- Source ID: `training_video_day2`
- Source Type: `training_video`
