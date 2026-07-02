# Verify Whether Direct RMS Or External API Actions May Have Bypassed OptiSweep Tracking

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_whether_direct_rms_or_external_api_actions_may_have_bypassed_optisweep_tracking_v1` |
| Title | Verify Whether Direct RMS Or External API Actions May Have Bypassed OptiSweep Tracking |
| Procedure Type | `reference` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-based reference check when reviewing an issue to determine whether support or troubleshooting activity may have bypassed the normal OptiSweep software flow through direct RMS or external API interaction. The source warns that bypassing OptiSweep can leave the software unaware of what happened and create out-of-sync conditions.

## When To Use

Use when investigating missing visibility, unexplained state differences, or suspected support actions involving RMS, Geek Plus, REST API, or other external API interaction outside the normal OptiSweep software flow.

## Do Not Use For

* Do not use this runbook as authorization to perform direct RMS or external API actions.
* Do not use this runbook as a recovery procedure to resynchronize OptiSweep after bypass activity.
* Do not use this runbook to execute unsupported troubleshooting steps not explicitly provided by the source.

## Safety And Operational Notes

* The source explicitly warns against bypassing the OptiSweep software flow.
* Direct API activity may leave OptiSweep without knowledge of the transaction and create an out-of-sync condition.
* This source does not provide a recovery method after bypass activity.

## Access Or Tools Needed

* Incident details or operator/support report describing what actions were taken
* Awareness of the documented OptiSweep-to-RMS integration boundary

## Related Operational Context

* ctx_training_video_rms_optisweep_api_integration_v1
* ctx_training_video_optisweep_sync_boundary_with_rms_v1

## Procedure Steps

### Step 1 — Confirm whether direct RMS or API interaction was attempted

**Responsible role:** L2_support

**Instruction:**
Review the incident details or support report and confirm whether anyone attempted direct interaction with Geek Plus, RMS, REST API, or other external APIs outside the normal OptiSweep software flow.

**Expected result:**
A clear yes/no determination is made on whether direct external interaction was attempted.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*RMS overview context and transcript references to API communication between RMS and OptiSweep.*


**Stop or Escalate If:**

* Direct API use is suspected and system state is unclear.

---

### Step 2 — Identify whether the action bypassed the OptiSweep service

**Responsible role:** L2_support

**Instruction:**
Identify whether the reported action was intended to bypass the OptiSweep service or directly trigger behavior through external APIs instead of going through the OptiSweep software flow.

**Expected result:**
The action is classified as either within the OptiSweep flow or a bypass of the OptiSweep service.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*Transcript context describing RMS access and API communication, used to interpret whether the reported action was outside OptiSweep.*


**Stop or Escalate If:**

* The reported action appears to have bypassed the OptiSweep service.
* It is not possible to determine whether the action used the supported OptiSweep path.

---

### Step 3 — Compare the action against the source warning

**Responsible role:** L2_support

**Instruction:**
Compare the reported action against the source warning that bypassing OptiSweep can leave the software unaware of what happened and can cause systems to get out of sync.

**Expected result:**
You determine whether the source warning plausibly explains the observed issue.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*Warning context in the transcript about bypassing OptiSweep and causing out-of-sync conditions.*


**Stop or Escalate If:**

* The source warning matches the reported action and current system state is unclear.

---

### Step 4 — Record the synchronization risk

**Responsible role:** L2_support

**Instruction:**
Record that suspected or confirmed direct API activity may have left OptiSweep without knowledge of the transaction and may have created an out-of-sync condition.

**Expected result:**
The case record reflects the source-supported explanation for missing visibility or synchronization issues.

**Stop or Escalate If:**

* Direct API use is suspected and there is no clear recovery path from the source.

---

### Step 5 — Do not perform direct API actions from this source

**Responsible role:** L2_support

**Instruction:**
Stop short of performing direct RMS or external API actions based on this source alone. Treat this segment as a warning and interpretation boundary, not as authorization or a recovery method.

**Expected result:**
No unsupported direct API action is taken from this source guidance alone.

**Stop or Escalate If:**

* A direct API action is being considered without separate approved procedure.
* System state is unclear after suspected bypass activity.

---

## Success Criteria

* Support determines whether direct RMS or external API activity may have bypassed OptiSweep.
* The issue record documents the source-supported risk that OptiSweep may not know what happened.
* No unsupported direct API action is taken from this source alone.

## Failure Conditions

* Direct API or RMS bypass activity is suspected or confirmed.
* OptiSweep may lack knowledge of the transaction.
* System state is unclear and the source provides no recovery method.

## Escalation Guidance

* Escalate if direct API use is suspected and system state is unclear.
* Escalate rather than performing direct API actions from this source alone.
* Note that the source does not provide a recovery method for resynchronizing systems after bypass activity.

## Missing Details / Known Gaps

* The source does not provide a recovery or resynchronization procedure after bypass activity.
* The source does not define exact logging location or case documentation format for recording suspected bypass activity.
* The source does not specify role boundaries beyond support-oriented interpretation.
* The source does not provide commands, API endpoints, or approved direct-action procedures.

## Source Lineage

- Candidate IDs: candidate_training_video_verify_support_boundary_for_direct_rms_api_use
- Source ID: `training_video_day1`
- Source Type: `training_video`
