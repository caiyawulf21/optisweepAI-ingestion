# Check HMI visibility and activity/system active error evidence for a stuck AGV or stuck task

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_hmi_visibility_and_activity_system_active_error_evidence_for_stuck_agv_or_stuck_task_v1` |
| Title | Check HMI visibility and activity/system active error evidence for a stuck AGV or stuck task |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this incident-derived diagnostic when bag-out or related flow issues may involve a stuck task or AGV inactivity and the needed screen is not visible in Aveva. The incident evidence supports checking alternate visibility paths: reviewing system activity or system active error information for an AGV that has not moved for an extended period, and checking the site HMI for a stuck-task error that may only be visible there.

## When To Use

Use when troubleshooting a bag-out or related AGV/task issue at the incident site and Aveva does not show the needed screen or visibility is otherwise limited. This runbook is appropriate for gathering diagnostic evidence about whether an AGV has been inactive for an extended period or whether a stuck-task error is visible only on the HMI.

## Do Not Use For

* Do not use this as a recovery procedure for clearing a stuck task; the incident references the need for a recovery process but does not provide one.
* Do not use this to make undocumented configuration, HMI deployment, or AGV recovery changes.
* Do not use this when exact navigation or controls are required beyond what is shown in the incident evidence.

## Safety And Operational Notes

* This source supports inspection and interpretation only; it does not support performing recovery actions.
* If the needed HMI visibility is unavailable because the latest HMI project has not been pushed or the error cannot be seen, stop and escalate rather than making undocumented changes.
* Do not perform undocumented recovery changes based only on suspicion.

## Access Or Tools Needed

* Aveva screen visibility if available
* Access to system activity or system active error information
* Access to the site HMI that shows stuck-task errors
* Support-level access to review AGV activity

## Procedure Steps

### Step 1 — Check whether the needed screen is visible in Aveva

**Responsible role:** L2_support

**Instruction:**
Check whether the relevant troubleshooting screen can be seen in Aveva. If the screen is not visible, continue with alternate checks using system activity or system active error information and the site HMI.

**Expected result:**
You determine whether Aveva can be used for this diagnostic or whether alternate visibility is required.

**Stop or Escalate If:**

* Aveva visibility is unavailable and no alternate supported view can be accessed
* The team cannot confirm what screen or view should be inspected from the available incident evidence

---

### Step 2 — Review system activity or system active error for AGV inactivity

**Responsible role:** L2_support

**Instruction:**
Open the system activity or system active error view referenced in the incident and check for an AGV that has not moved for an extended period. In this incident, support reported seeing an AGV that did not move for about 3 hours.

**Expected result:**
You identify whether activity or active error information shows an AGV with prolonged inactivity.

**Stop or Escalate If:**

* The activity or system active error view cannot be accessed
* The data is insufficient to determine whether an AGV has been inactive for an extended period
* An AGV appears inactive for an extended period but no supported recovery procedure is available in this source

---

### Step 3 — Check the site HMI for stuck-task error visibility

**Responsible role:** L2_support

**Instruction:**
Check the site HMI for errors that may only be visible there, including a stuck-task condition. The incident specifically states that one of the previous night's stuck-task errors was only visible on that HMI.

**Expected result:**
You determine whether the HMI shows a stuck-task or related error not visible elsewhere.

**Stop or Escalate If:**

* The HMI cannot be accessed
* The needed HMI project or visibility is unavailable
* The error is believed to be HMI-only but cannot be confirmed from the available HMI view

---

### Step 4 — Compare HMI findings with activity or active error findings

**Responsible role:** L2_support

**Instruction:**
Compare what is visible on the HMI with what is visible in system activity or system active error information to determine whether the issue appears to be a stuck task, AGV inactivity, or both.

**Expected result:**
You have a documented diagnostic conclusion supported by the available incident-style evidence.

**Stop or Escalate If:**

* The HMI and activity findings cannot be reconciled
* The evidence suggests a stuck task or AGV inactivity but no documented recovery procedure is available in this source
* The conclusion would require undocumented changes or assumptions

---

### Step 5 — Stop and escalate if HMI visibility is unavailable or incomplete

**Responsible role:** L2_support

**Instruction:**
If the needed HMI visibility is unavailable because the latest HMI project has not been pushed or the error cannot be seen, stop the diagnostic at the evidence-gathering stage and escalate rather than making undocumented changes.

**Expected result:**
The issue is escalated with documented limitations instead of proceeding with unsupported actions.

**Stop or Escalate If:**

* The latest HMI project is present but has not been pushed at the site
* The error cannot be seen on the HMI
* Aveva visibility is unavailable and the HMI does not expose the needed error
* Any next step would require undocumented recovery changes

---

## Success Criteria

* Support determines whether the issue is visible only on the HMI and/or whether activity shows an AGV that did not move for about 3 hours.
* The diagnostic conclusion is supported by incident evidence from Aveva visibility limitations, activity or active error review, and HMI observations.
* Unsupported recovery actions are avoided when visibility is incomplete.

## Failure Conditions

* Aveva visibility is unavailable and alternate supported views are insufficient.
* System activity or system active error information shows an AGV that has not moved for about 3 hours.
* A stuck-task error is visible only on the HMI.
* The latest HMI project or visibility needed for confirmation is unavailable.

## Escalation Guidance

* Escalate if Aveva visibility is unavailable and the HMI does not expose the needed error.
* Escalate if the required HMI visibility is unavailable because the latest HMI project has not been pushed or the error cannot be seen.
* Escalate instead of making undocumented recovery changes when evidence suggests a stuck task or AGV inactivity but this source does not provide a supported recovery procedure.

## Missing Details / Known Gaps

* The incident does not provide exact navigation steps or screen names for system activity or system active error views.
* No artifact IDs were supplied for HMI or activity screenshots, so no structured image attachments could be added.
* The incident does not provide a documented stuck-task recovery procedure.
* The incident does not provide exact escalation target names or routing instructions.
* The incident does not provide a supported time estimate for completing this diagnostic.

## Source Lineage

- Candidate IDs: candidate_incident_218550_check_hmi_or_activity_for_stuck_task_visibility
- Source ID: `source_case_218550`
- Source Type: `incident_case`
