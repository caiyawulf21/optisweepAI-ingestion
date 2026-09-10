# Use the training segment marker to identify the end of the RMS section during Day 1 training

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_training_segment_marker_to_identify_end_of_rms_section_day1_v1` |
| Title | Use the training segment marker to identify the end of the RMS section during Day 1 training |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | None |
| Access Surface | None |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Day 1 training video’s explicit RMS-section-end marker (the on-screen reference “Aveva Walkthrough 32” and the spoken cue “I think that ends the RMS section”) to recognize when the training transitions away from the RMS portion, including the break/pacing discussion.

## When To Use

When you are following UPSFORTNA OptiSweep Training Day 1 and need a grounded cue that the session is transitioning away from the RMS portion so you can prepare for the next topic (including break/pacing).

## Do Not Use For

* Do not use this as an operational troubleshooting procedure for RMS, WCS/Helix DB, or any live system behavior. This segment is a training-session transition marker only.

## Access Or Tools Needed

* UPSFORTNA OptiSweep Training Day 1 video player
* Ability to view the training video frame containing the text "Aveva Walkthrough 32"

## Related Operational Context

* ctx_training_video_rms_section_end_marker_v1
* ctx_training_video_aveva_walkthrough_slide_reference_v1
* ctx_training_video_session_break_discussion_v1

## Procedure Steps

### Step 1 — Locate the training video frame that shows the slide reference text "Aveva Walkthrough 32"

**Responsible role:** operator

**Instruction:**
In the UPSFORTNA OptiSweep Training Day 1 video, navigate to the frame captured in segment training_video_day1_segment_0051 and confirm the on-screen text reads "Aveva Walkthrough 32".

**Expected result:**
You can see the training frame with the OCR text "Aveva Walkthrough 32" at the RMS-section-end transition segment.

**Stop or Escalate If:**

* If you cannot find the "Aveva Walkthrough 32" frame, stop and ask the trainer for the correct timestamp/segment.

---

### Step 2 — Listen for the spoken cue indicating the RMS section is ending

**Responsible role:** operator

**Instruction:**
Listen in the same segment for the spoken phrase indicating the RMS section is ending (example cue: "I think that ends the RMS section").

**Expected result:**
You hear the spoken cue that the RMS section is ending ("I think that ends the RMS section").

**Stop or Escalate If:**

* If you cannot find the RMS-end spoken cue, stop and ask the trainer for the correct timestamp/segment.

---

### Step 3 — Follow the spoken transition discussion (break/pacing) to align with the training pace

**Responsible role:** operator

**Instruction:**
During the transition segment after the RMS-end cue, follow the discussion about taking a break and schedule status (e.g., whether to take a break and that the team is behind schedule).

**Expected result:**
You recognize that the session is transitioning and that the speakers discuss break/pacing (including being behind schedule).

**Stop or Escalate If:**

* If the segment does not contain the expected break/pacing discussion, stop and ask the trainer for the correct timestamp/segment.

---

## Success Criteria

* You identify the RMS-section-end transition using both the on-screen reference "Aveva Walkthrough 32" and the spoken cue "I think that ends the RMS section".
* You recognize the session transition and the break/pacing discussion (including being behind schedule) so you can prepare for the next topic.

## Failure Conditions

* The "Aveva Walkthrough 32" frame cannot be located.
* The spoken RMS-end cue cannot be found.
* The break/pacing discussion is missing or does not match the expected transition context.

## Escalation Guidance

* If you cannot find the RMS-end spoken cue or the "Aveva Walkthrough 32" frame, stop and ask the trainer for the correct timestamp/segment.

## Missing Details / Known Gaps

* This packet provides a training-session transition marker only; it does not include any live operational system checks, UI navigation steps, or commands for RMS/WCS/Helix DB.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_rms_section_end_transition
- Source ID: `training_video_day1`
- Source Type: `training_video`
