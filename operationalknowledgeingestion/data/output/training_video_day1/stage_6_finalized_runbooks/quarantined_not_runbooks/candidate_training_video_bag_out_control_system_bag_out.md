# Use Bag Out Control System to close destinations and exchange occupied totes/chutes

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_bag_out_control_system_close_destinations_exchange_totes_v1` |
| Title | Use Bag Out Control System to close destinations and exchange occupied totes/chutes |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `bag_out_or_closeout_state` |
| Access Surface | `wcs_api` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Run a Bag Out action in the OptiSweep Bag Out Control system so that destinations are closed and totes/chutes containing parcels are exchanged. The control supports system-wide bag out and also bag out scoped by sorter leg. For manual bag out, a cancel bag out option is available to cancel exchange tasks that are not in process.

## When To Use

Use when you need to end a sort cycle by closing destinations and exchanging totes/chutes that contain parcels, using the Bag Out Control system behavior described in the source.

## Safety And Operational Notes

* If performing a manual bag out, use the cancel bag out capability only for exchange tasks that are not in process; exchange tasks that are already in process must still finish.

## Access Or Tools Needed

* Bag out control system UI/control (as shown in the source training segment)

## Related Operational Context

* ctx_training_video_system_bag_out_overview_v1
* ctx_training_video_bag_out_by_sorter_leg_v1

## Procedure Steps

### Step 1 — Open the Bag Out control system screen/control

**Responsible role:** operator

**Instruction:**
Open the Bag Out control system UI/control shown in the source segment.

**Expected result:**
The Bag Out control system options are visible, including system bag out and the ability to choose bag out by leg of the sorter (and manual bag out options such as cancel bag out, if applicable).

---

### Step 2 — Select the system bag out option

**Responsible role:** operator

**Instruction:**
Select the system bag out option (the full-system option, not the sorter-leg-specific option).

**Expected result:**
The selected bag out scope is system-wide (not limited to a single sorter leg).

---

### Step 3 — Confirm the intended system-wide behavior (close all destinations; exchange totes/chutes with parcels)

**Responsible role:** operator

**Instruction:**
Confirm that the Bag Out control system indicates system bag out will close all destinations and exchange totes/chutes with parcels in them.

**Expected result:**
The control’s described behavior matches: destinations are closed and totes/chutes containing parcels are exchanged.

**Stop or Escalate If:**

* Stop and escalate if the observed behavior does not match the source-described outcomes (destinations not closing and/or parcels not being exchanged).

---

### Step 4 — If limiting scope, select bag out by leg of the sorter

**Responsible role:** operator

**Instruction:**
If the operation should be limited, select the bag out by leg of the sorter option.

**Expected result:**
The bag out scope is set to a sorter-leg level rather than system-wide.

---

### Step 5 — If performing manual bag out, use cancel bag out only for exchanges not in process

**Responsible role:** operator

**Instruction:**
If you are performing a manual bag out and need to cancel, use cancel bag out only to cancel exchange tasks that are not in process; do not cancel tasks that are already in an exchange.

**Expected result:**
Only exchange tasks not currently in process are canceled; any exchange task already in process continues to completion.

**Stop or Escalate If:**

* If performing a manual bag out, ensure you use the cancel bag out capability only as allowed by the source (cancel only exchange tasks not in process).

---

## Success Criteria

* Destinations are closed after the bag out action.
* Totes/chutes containing parcels are exchanged after the bag out action.
* If bag out is scoped by sorter leg, the scope matches the selected sorter leg (not system-wide).
* If manual bag out cancel is used, only exchange tasks not in process are canceled; in-process exchange tasks still finish.

## Failure Conditions

* Destinations do not close as expected.
* Parcels are not exchanged (totes/chutes with parcels are not exchanged).
* Manual cancel bag out cancels an exchange task that is already in process.

## Escalation Guidance

* Stop and escalate if the observed behavior does not match the source-described outcomes (destinations not closing and/or parcels not being exchanged).

## Missing Details / Known Gaps

* The source does not provide exact UI button/field labels for the bag out controls (e.g., the precise clickable control names).
* The source does not specify the exact live confirmation mechanism (e.g., which status indicator or screen field confirms destinations are closed and exchanges are completed).
* The source does not provide the exact procedure for choosing a specific sorter leg (e.g., how the leg is selected on the UI).

## Source Lineage

- Candidate IDs: candidate_training_video_bag_out_control_system_bag_out
- Source ID: `training_video_day1`
- Source Type: `training_video`
