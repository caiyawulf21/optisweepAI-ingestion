# Check Geek+ RMS page for system faults (left) vs AGV system faults (right) and relate to commanded-move/communication-loss symptoms

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` |
| Title | Check Geek+ RMS page for system faults (left) vs AGV system faults (right) and relate to commanded-move/communication-loss symptoms |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `gateway_unhealthy`, `api_unresponsive`, `web_app_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Geek+ “Overall System RMS” web page to determine whether the observed fault symptom is categorized as a general “system faults” issue (left side) or an “active AGV faults / AGV system faults” issue (right side). The source’s examples map communication loss to the left and “AGV told to move but not reaching in-progress” to the right. If the RMS page appears blank, the source attributes this to the firewall not being open.

## When To Use

When a caller reports an issue and you need to quickly categorize what the Geek+ RMS “Overall System RMS” page is showing—specifically whether faults appear under the left “system faults” area or the right “active AGV faults / AGV system faults” area—using the source’s symptom mapping (communication loss vs commanded move not reaching in-progress).

## Access Or Tools Needed

* Geek+ RMS web page access for the “Overall System RMS” page
* Ability to view the left “system faults” and right “AGV system faults / active AGV faults” areas
* If the RMS page is blank due to firewall visibility, the source indicates using an API Dog or the database to see what is on the screen

## Related Operational Context

* ctx_training_video_system_faults_vs_agv_faults_v1
* ctx_training_video_rms_visibility_on_thin_clients_v1

## Procedure Steps

### Step 1 — Open the Geek+ RMS “Overall System RMS” page

**Responsible role:** L1_support

**Instruction:**
Open the Geek+ RMS web page corresponding to “Overall System RMS”.

**Expected result:**
The “Overall System RMS” page loads and shows two fault areas: left “system faults” and right “AGV system faults / active AGV faults”.

**Stop or Escalate If:**

* If the page is blank, do not assume there are no faults; treat it as a firewall/visibility issue per the source and proceed to Step 5.

---

### Step 2 — Check the left-side “system faults” entries

**Responsible role:** L1_support

**Instruction:**
On the “Overall System RMS” page, look at the left side under “system faults”.

**Expected result:**
If the symptom is communication loss, the relevant fault appears under the left-side “system faults” area.

---

### Step 3 — Check the right-side “AGV system faults / active AGV faults” entries

**Responsible role:** L1_support

**Instruction:**
On the “Overall System RMS” page, look at the right side under “AGV system faults” / “active AGV faults”.

**Expected result:**
If the symptom is an AGV commanded to move but it has not reached “in progress”, the relevant fault appears under the right-side “AGV system faults / active AGV faults” area.

---

### Step 4 — Relate observed fault placement to the reported symptom

**Responsible role:** L1_support

**Instruction:**
Use the source’s mapping: communication loss → left “system faults”; AGV told to move but not reaching “in progress” → right “AGV system faults / active AGV faults”.

**Expected result:**
The observed fault placement matches the source’s examples (left for communication loss; right for commanded move not reaching in-progress).

**Stop or Escalate If:**

* If faults do not appear in either expected area (left “system faults” / right “AGV system faults / active AGV faults”), stop and escalate for deeper investigation using the source’s stated alternatives (API Dog or database).

---

### Step 5 — Handle blank RMS page (firewall not open) and use alternatives

**Responsible role:** L1_support

**Instruction:**
If the “Overall System RMS” page appears blank, treat it as a firewall visibility issue. Then use the source’s stated alternatives (API Dog or database) to determine what is on the screen.

**Expected result:**
You do not conclude “no faults” from a blank page; instead you proceed using API Dog or database visibility per the source.

**Stop or Escalate If:**

* If you cannot retrieve fault information via API Dog or database after the page is blank, escalate for deeper investigation (per the candidate’s escalation note).

---

## Success Criteria

* Faults are categorized correctly by placement: communication loss appears under left “system faults”, and commanded move not reaching “in progress” appears under right “AGV system faults / active AGV faults”.
* If the RMS page is blank, the investigation does not stop; you proceed using API Dog or database visibility per the source.

## Failure Conditions

* RMS page is blank and you incorrectly conclude there are no faults.
* Faults do not appear in either expected area (left “system faults” or right “AGV system faults / active AGV faults”) for the reported symptom.

## Escalation Guidance

* If faults do not appear in either expected area (left “system faults” / right “AGV system faults / active AGV faults”), escalate for deeper investigation using the source’s stated alternatives (API Dog or database).

## Missing Details / Known Gaps

* The source does not provide exact Geek+ RMS UI control names beyond the left/right labels (“system faults” and “AGV system faults / active AGV faults”).
* The source mentions alternatives (“API dog” or database) but does not provide the specific procedure, endpoints, or database tables to use.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_check_rms_system_faults_agv_faults
- Source ID: `training_video_day1`
- Source Type: `training_video`
