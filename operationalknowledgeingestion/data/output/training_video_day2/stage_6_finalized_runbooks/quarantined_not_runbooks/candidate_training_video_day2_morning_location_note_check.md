# Confirm the correct morning location before starting FORTNA OptiSweep Training Day 2

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_confirm_correct_morning_location_before_fortna_optiSweep_training_day2_v1` |
| Title | Confirm the correct morning location before starting FORTNA OptiSweep Training Day 2 |
| Procedure Type | `operation` |
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

Before beginning FORTNA OptiSweep Training Day 2, confirm you are physically at the correct morning location. The training video title slide includes the note: "[NOTE: Morning Location is Different]".

## When To Use

Use this pre-start check immediately before starting FORTNA OptiSweep Training Day 2 when the training title slide indicates the morning location is different.

## Access Or Tools Needed

* Access to the Day 2 training title slide (or the training video frame containing the note)

## Related Operational Context

* ctx_training_video_day2_training_session_day2_v1
* ctx_training_video_day2_morning_location_note_v1

## Visual References

![artifact_training_video_training_video_day2_0001_00_00_00_000_primary_00_00_01_500](assets/1adca5fdc8da67ad.jpg)

*Training video title slide frame showing: "FORTNA OptiSweep Training - Day 2 [NOTE: Morning Location is Different]"*

## Procedure Steps

### Step 1 — Review the Day 2 training title slide note

**Responsible role:** operator

**Instruction:**
Open the FORTNA OptiSweep Training Day 2 title slide (or the training video frame) and read the note shown on the slide.

**Expected result:**
The note "[NOTE: Morning Location is Different]" is visible on the Day 2 title slide.

---

### Step 2 — Verify you are physically at the correct morning location

**Responsible role:** operator

**Instruction:**
Before beginning the training session, confirm your physical presence at the correct morning location for FORTNA OptiSweep Training Day 2.

**Expected result:**
You are physically at the correct morning location for Day 2.

---

### Step 3 — If not at the correct location, stop and confirm with the training organizer

**Responsible role:** operator

**Instruction:**
If you cannot confirm you are at the correct morning location, stop before beginning Day 2 and confirm the correct location with the training organizer/instructor.

**Expected result:**
Either (a) you confirm you are at the correct location and proceed, or (b) you stop and confirm the correct location with the training organizer/instructor.

**Stop or Escalate If:**

* You cannot confirm the correct morning location.

---

## Success Criteria

* You are physically at the correct morning location for FORTNA OptiSweep Training Day 2.

## Failure Conditions

* You cannot confirm the correct morning location and proceed anyway.
* The title slide note cannot be found/verified.

## Escalation Guidance

* Escalate to the training organizer/instructor if you cannot confirm the correct morning location.

## Missing Details / Known Gaps

* The packet does not specify the actual morning location name/address—only that it is different—so the organizer/instructor confirmation is required when you cannot determine the correct location.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_morning_location_note_check
- Source ID: `training_video_day2`
- Source Type: `training_video`
