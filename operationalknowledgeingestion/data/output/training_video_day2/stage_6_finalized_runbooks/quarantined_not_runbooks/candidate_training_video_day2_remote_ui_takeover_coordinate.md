# Coordinate remote UI takeover with on-site operator during tipper operation

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_coordinate_remote_ui_takeover_with_on_site_operator_during_tipper_operation_v1` |
| Title | Coordinate remote UI takeover with on-site operator during tipper operation |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `system_fault`, `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When a remote user logs into the tipper/operator UI and takes over control, coordinate with the on-site operator so only one person performs active UI actions at a time. Confirm the on-site operator sees the same screen changes made remotely, and ensure any mentioned technology alarms/faults have cleared after your actions.

## When To Use

Use when you (remote) have logged into the tipper/operator UI and need to operate it while an on-site operator is also present and could interact with the same UI.

## Do Not Use For

* Do not continue operating the shared UI if the on-site operator is actively interacting with the UI at the same time—re-coordinate first to prevent conflicting actions.

## Safety And Operational Notes

* Coordinate shared-control: the person on the other side might also be trying to do the same thing, so communicate takeover to prevent conflicting actions.

## Access Or Tools Needed

* Remote login capability to the tipper UI
* Ability for on-site operator to observe the same screen/UI changes you make remotely

## Related Operational Context

* ctx_training_video_remote_ui_takeover_v1
* ctx_training_video_remote_ui_coordination_v1

## Procedure Steps

### Step 1 — Confirm remote takeover of the tipper/operator UI

**Responsible role:** L1_support

**Instruction:**
Confirm you are remotely logged into the tipper/operator UI and have taken over the UI.

**Expected result:**
You are actively operating the tipper/operator UI remotely (takeover state is established).

**Stop or Escalate If:**

* If you cannot confirm takeover, stop and re-establish remote takeover before proceeding.

---

### Step 2 — Communicate takeover to the on-site operator to prevent conflicting actions

**Responsible role:** L1_support

**Instruction:**
Tell the on-site person that you are remotely logged into the tipper and have taken over the UI so they do not perform different actions at the same time.

**Expected result:**
The on-site operator is aware you have taken over the UI and refrains from making conflicting UI changes.

**Stop or Escalate If:**

* If the on-site operator is also interacting with the UI, stop and re-coordinate before continuing.

---

### Step 3 — Operate the tipper/operator UI remotely while on-site refrains from conflicting changes

**Responsible role:** L1_support

**Instruction:**
Proceed with the UI actions you need to perform remotely, while the on-site operator refrains from making conflicting changes.

**Expected result:**
Your remote UI actions are the only active changes being made to the shared UI.

**Stop or Escalate If:**

* If the on-site operator begins interacting with the UI, stop and re-coordinate immediately.

---

### Step 4 — Verify on-site operator sees the same remote screen changes

**Responsible role:** L1_support

**Instruction:**
After you change the screen/UI remotely, verify the on-site operator can see the screen change on their side.

**Expected result:**
The on-site operator observes the same screen/UI changes you made remotely.

**Stop or Escalate If:**

* If the on-site operator cannot see the screen change, stop further UI changes and re-check coordination/connection before continuing.

---

### Step 5 — Ensure technology alarms/faults have gone away after your actions

**Responsible role:** L1_support

**Instruction:**
If the source mentions technology alarms/faults, ensure the relevant faults have gone away after your actions.

**Expected result:**
The technology alarms/fault indicators you targeted are cleared (faults have gone away).

**Stop or Escalate If:**

* If technology alarms/faults do not clear after your actions, escalate for further troubleshooting rather than continuing conflicting operations.

---

## Success Criteria

* On-site and remote users are aligned such that only the remote user performs active UI operation while the on-site operator refrains from conflicting changes.
* On-site operator sees the same screen/UI changes made remotely.
* Any mentioned technology alarms/faults are cleared after the remote UI actions.

## Failure Conditions

* On-site operator is also interacting with the UI at the same time as the remote user.
* On-site operator does not see the screen changes made remotely.
* Technology alarms/faults do not clear after remote UI actions.

## Escalation Guidance

* If technology alarms/faults do not clear after your remote UI actions, escalate for further troubleshooting rather than continuing conflicting operations.

## Missing Details / Known Gaps

* The packet does not name specific tipper UI screens/buttons/fields to click; steps therefore focus on coordination, shared-screen visibility, and fault-clearing validation.
* The packet does not specify the exact UI location/label for “technology alarms/faults”; only the requirement to ensure faults have gone away is provided.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_remote_ui_takeover_coordinate
- Source ID: `training_video_day2`
- Source Type: `training_video`
