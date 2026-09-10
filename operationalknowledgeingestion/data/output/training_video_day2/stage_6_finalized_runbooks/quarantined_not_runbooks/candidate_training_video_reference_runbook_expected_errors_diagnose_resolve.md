# Use support runbooks: map expected errors to diagnostic and resolution steps

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_support_runbooks_map_expected_errors_diagnose_resolve_v1` |
| Title | Use support runbooks: map expected errors to diagnostic and resolution steps |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the support runbook that matches the expected error/fatal category you are investigating, then follow its prescribed diagnostic steps and resolution steps. If the observed error/fatal does not fit any expected error type in the runbook, use the support handoff approach: consult RCA documentation in Confluence and then resolve (optionally updating the RCA with new information).

## When To Use

When you are investigating an observed error/fatal and need a support-oriented path that maps the error category to (1) expected error types, (2) steps to diagnose, and (3) steps to resolve.

## Do Not Use For

* Do not proceed with runbook steps if the observed error/fatal does not match any expected error type in the runbook; instead use the RCA/Confluence handoff approach described in the source.

## Access Or Tools Needed

* Support runbook documentation (as referenced by the source)
* Confluence (for RCA documentation, as referenced by the source)

## Related Operational Context

* ctx_training_video_runbook_definition_support_v1
* ctx_training_video_support_handoff_rca_confluence_v1

## Visual References

![artifact_training_video_training_video_day2_0056_so_just_as_they_you_will_primary_03_22_16_000](assets/d5ba44f9f1db5255.jpg)

*Frame showing the source description of runbooks as support-oriented (expected errors, steps to diagnose, steps to resolve) and the handoff approach using RCA in Confluence.*

## Procedure Steps

### Step 1 — Open the support runbook that corresponds to the error/fatal type you are investigating

**Responsible role:** L1_support

**Instruction:**
Open the support runbook that corresponds to the error/fatal type you are investigating.

**Expected result:**
You have the relevant runbook open that contains a section listing the “types of errors expected” and associated diagnostic and resolution steps.

---

### Step 2 — Identify the “types of errors expected” section and confirm the observed error/fatal matches an expected error category

**Responsible role:** L1_support

**Instruction:**
In the opened runbook, locate the section that lists the “types of errors expected” and confirm your observed error/fatal matches one of the expected error categories.

**Expected result:**
Your observed error/fatal is mapped to a specific expected error category listed in the runbook’s “types of errors expected” section.

**Stop or Escalate If:**

* If the observed error/fatal does not match any expected error type in the runbook, stop and use the RCA/Confluence handoff process described in the source.

---

### Step 3 — Follow the runbook’s “steps to diagnose” for the matching expected error type

**Responsible role:** L1_support

**Instruction:**
Follow the runbook’s “steps to diagnose” for the expected error type/category that matches your observed error/fatal.

**Expected result:**
You complete the runbook’s diagnostic steps associated with the mapped expected error category.

---

### Step 4 — Follow the runbook’s “steps to resolve” for the matching expected error type

**Responsible role:** L1_support

**Instruction:**
Follow the runbook’s “steps to resolve” for that expected error type/category.

**Expected result:**
You complete the runbook’s resolution steps associated with the mapped expected error category.

---

### Step 5 — If the runbook is incomplete or the error/fatal does not match, use the RCA/Confluence handoff approach and then resolve (optionally update RCA)

**Responsible role:** L1_support

**Instruction:**
If the runbook information is incomplete or the observed error/fatal does not match any expected error type in the runbook, use the source-described support handoff approach: consult RCA documentation in Confluence and then resolve; optionally update RCA with new information.

**Expected result:**
You consult RCA in Confluence and use it to drive resolution; if new information is discovered, you update the RCA as described by the source.

**Stop or Escalate If:**

* If the observed error/fatal does not match any expected error type in the runbook, stop and use the RCA/Confluence handoff process described in the source.

---

## Success Criteria

* Observed error/fatal is mapped to a runbook expected error category (when a match exists).
* Diagnostic steps and resolution steps executed correspond to the mapped expected error category in the runbook.
* If no match exists or runbook info is incomplete, RCA in Confluence is consulted and used to drive resolution (with optional RCA updates).

## Failure Conditions

* Observed error/fatal does not match any expected error type in the runbook and you do not switch to the RCA/Confluence handoff approach.
* You execute diagnose/resolve steps that do not correspond to the mapped expected error category.

## Escalation Guidance

* If the observed error/fatal does not match any expected error type in the runbook, stop and use the RCA/Confluence handoff process described in the source (consult RCA in Confluence, then resolve; optionally update RCA).

## Missing Details / Known Gaps

* The source does not provide specific runbook locations, UI controls, or navigation steps to open a particular runbook.
* The source does not provide concrete diagnostic/resolution actions for specific error categories—only the general runbook structure and the RCA/Confluence fallback approach.

## Source Lineage

- Candidate IDs: candidate_training_video_reference_runbook_expected_errors_diagnose_resolve
- Source ID: `training_video_day2`
- Source Type: `training_video`
