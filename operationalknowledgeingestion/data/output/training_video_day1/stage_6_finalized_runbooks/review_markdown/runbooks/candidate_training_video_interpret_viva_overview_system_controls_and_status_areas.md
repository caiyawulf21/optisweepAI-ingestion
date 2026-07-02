# Identify Available System Controls and Status Areas on the Viva Overview

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_available_system_controls_and_status_areas_on_the_viva_overview_v1` |
| Title | Identify Available System Controls and Status Areas on the Viva Overview |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Viva overview screen to locate the documented high-level control actions and visible status or metrics areas shown in the source. This runbook is for identifying screen regions and labels only, not for executing startup, shutdown, purge, bag out, resume, pause, or other control actions.

## When To Use

Use when a user needs to identify where the Viva main overview displays the right-hand control area, named system control actions, metrics or destination information, and AGV status areas on the overview screen.

## Do Not Use For

* Do not use this runbook to execute startup, shutdown, bag out, purge, resume, pause all AGVs, or Start/Stop system actions.
* Do not assume undocumented meanings, button behavior, confirmation behavior, or control sequences from this source segment alone.

## Safety And Operational Notes

* This source segment is a screen-orientation reference only.
* Do not perform control actions based on this runbook alone because the source identifies controls but does not provide execution steps.
* If expected controls or status areas are not visible, escalate to verify screen version or access.

## Access Or Tools Needed

* Access to the Viva HMI main overview screen
* Visual access to the right-hand control area
* Visible metrics or destination information area
* Visible AGV status area

## Related Operational Context

* ctx_training_video_viva_main_overview_v1
* ctx_training_video_viva_system_controls_panel_v1

## Procedure Steps

### Step 1 — Open the Viva main overview and focus on the right-hand control area

**Responsible role:** operator

**Instruction:**
Open the Viva main overview screen and visually focus on the right-hand side control area shown on the overview.

**Expected result:**
The Viva main overview is visible and the right-hand control area can be identified.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*The Viva main overview home screen and the right-hand side control area.*


**Stop or Escalate If:**

* The displayed screen does not match the Viva main overview.
* The right-hand control area is not visible.

---

### Step 2 — Locate the named control actions

**Responsible role:** operator

**Instruction:**
On the right-hand control area, locate the control actions named in the source: startup, shutdown, bag out, purge, resume, and pause all AGVs.

**Expected result:**
The named control actions can be visually identified on the overview screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*The right-hand control list containing startup, shutdown, bag out, purge, resume, and pause all AGVs.*


**Stop or Escalate If:**

* Expected named controls are missing from the visible screen.
* The screen appears to be a different version or access level than the one shown in the source.

---

### Step 3 — Identify any Start/Stop system wording

**Responsible role:** operator

**Instruction:**
Inspect the overview screen for any Start/Stop system wording shown in the displayed screen content, and note it only if it is visibly present.

**Expected result:**
Any visible Start/Stop system wording on the overview is identified.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*Any Start/Stop system wording visible within the overview control area.*


**Stop or Escalate If:**

* The relevant screen area is not readable enough to confirm whether Start/Stop system wording is present.

---

### Step 4 — Locate the metrics or destination information area

**Responsible role:** operator

**Instruction:**
Locate the metrics or destination information area referenced by the source on the Viva overview screen.

**Expected result:**
The metrics or destination information area is visually identified on the overview.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*The overview area described as showing metrics or destinations.*


**Stop or Escalate If:**

* The metrics or destination information area is not visible on the current screen.

---

### Step 5 — Locate the AGV status area

**Responsible role:** operator

**Instruction:**
Locate the AGV status area referenced by the source on the Viva overview screen.

**Expected result:**
The AGV status area is visually identified on the overview.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*The overview area referenced as AGV status.*


**Stop or Escalate If:**

* The AGV status area is not visible on the current screen.

---

### Step 6 — Record visible controls and status areas without assuming behavior

**Responsible role:** operator

**Instruction:**
Record which of the documented controls and status areas are visible on the current overview screen without assuming undocumented meanings or actions.

**Expected result:**
A source-grounded record exists of which controls and status areas are visible on the current screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*Use the overview frame as the reference for what screen regions and labels are documented by the source.*


**Stop or Escalate If:**

* Expected controls or status areas are not visible and screen version or access may need verification.
* You are being asked to perform a control action based only on this reference runbook.

---

## Success Criteria

* The user can identify the Viva main overview screen.
* The right-hand control area is located.
* The named controls documented by the source are identified if visible.
* Metrics or destination information and AGV status areas are identified if visible.
* Visible items are recorded without adding unsupported meanings or execution steps.

## Failure Conditions

* The Viva main overview cannot be opened or recognized.
* The right-hand control area is missing or not visible.
* Expected controls or status areas are not visible on the current screen.
* The screen appears to be a different version or access level than the one shown in the source.
* The user attempts to infer undocumented control behavior from this reference alone.

## Escalation Guidance

* Escalate for help verifying screen version or user access if expected controls or status areas are not visible.
* Escalate to a qualified support resource if execution of startup, shutdown, bag out, purge, resume, pause all AGVs, or Start/Stop system actions is requested, because this source does not provide execution steps.

## Missing Details / Known Gaps

* The source does not provide execution steps for startup, shutdown, bag out, purge, resume, pause all AGVs, or Start/Stop system.
* The source does not provide confirmation behavior, expected button responses, or control prerequisites.
* The source does not provide a time estimate.
* The source does not define exact screen coordinates or exact labels beyond the documented wording captured in the packet.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_viva_overview_system_controls_and_status_areas
- Source ID: `training_video_day1`
- Source Type: `training_video`
