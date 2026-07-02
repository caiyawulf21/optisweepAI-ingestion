# Interpret The Disconnected AGV Count On The Map Monitor

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_the_disconnected_agv_count_on_the_map_monitor_v1` |
| Title | Interpret The Disconnected AGV Count On The Map Monitor |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the map monitor disconnected AGV count to understand how many AGVs the RMS considers disconnected, and compare that count against source-described causes such as Wi-Fi communication loss or an AGV being turned off.

## When To Use

Use when reviewing the map monitor summary area to understand the meaning of the disconnected AGV count and to compare the displayed count against source-described disconnect causes.

## Do Not Use For

* Do not use this runbook to prove the exact root cause of a disconnect when the source only provides possible reasons.
* Do not use logs alone to conclude that an AGV was turned off; the source states logs may show disconnecting but may not show whether the AGV was turned off.
* Do not use this runbook as a recovery procedure to restore AGV communication.

## Safety And Operational Notes

* This is a reference and interpretation procedure only; it does not direct physical intervention.
* Do not over-interpret the disconnected count or logs beyond what is directly supported by the source and site observation.

## Access Or Tools Needed

* Access to the map monitor summary area
* Visibility into AGV operating state or site observation

## Related Operational Context

* ctx_training_video_disconnected_agv_count_v1

## Procedure Steps

### Step 1 — Locate the disconnected AGV count

**Responsible role:** L1_support

**Instruction:**
Open or view the map monitor summary area and locate the disconnected AGV count indicator.

**Expected result:**
The disconnected AGV count field is visible in the map monitor summary area.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*The map monitor summary area showing the disconnected AGV count among the summary indicators.*


**Stop or Escalate If:**

* Escalate if the disconnected AGV count cannot be located in the visible map monitor summary area.

---

### Step 2 — Read the displayed disconnected count

**Responsible role:** L1_support

**Instruction:**
Read the displayed disconnected AGV count from the map monitor summary area.

**Expected result:**
A numeric disconnected AGV count is identified from the display.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*The disconnected AGV count value in the map monitor summary area.*


**Stop or Escalate If:**

* Escalate if the displayed count cannot be read or confirmed.

---

### Step 3 — Interpret what the count means

**Responsible role:** L1_support

**Instruction:**
Interpret the displayed count as the number of AGVs that have lost communication from RMS. Use the source explanation that RMS is the application running on the server and that AGVs communicate over Wi-Fi.

**Expected result:**
The disconnected count is understood as a communication-state indicator from RMS, not just a generic AGV status number.

**Stop or Escalate If:**

* Escalate if the displayed count cannot be reconciled with the source definition of disconnected AGVs.

---

### Step 4 — Compare against source-described possible causes

**Responsible role:** L1_support

**Instruction:**
Check whether the disconnected condition could match source-described causes such as AGV Wi-Fi communication loss or an AGV being turned off. Treat these as possible causes only unless directly supported by observation.

**Expected result:**
Any observed possible cause is limited to source-supported explanations and is not overstated.

**Stop or Escalate If:**

* Escalate if the disconnected count cannot be reconciled with visible AGV state or known site observations.
* Stop interpretation if the only available evidence is logs that show disconnecting but do not show whether the AGV was turned off.

---

### Step 5 — Record the count and directly supported observation

**Responsible role:** L1_support

**Instruction:**
Record the disconnected AGV count and the observed possible cause if it is directly supported by site observation. Do not record an unsupported root-cause conclusion.

**Expected result:**
The disconnected count is documented with only source-supported and observation-supported interpretation.

**Stop or Escalate If:**

* Escalate if the disconnected count cannot be reconciled with visible AGV state or known site observations.
* Do not finalize a cause statement if the source limitation about logs prevents confirmation.

---

## Success Criteria

* The disconnected AGV count is located and read from the map monitor summary area.
* The count is interpreted as the number of AGVs that RMS considers disconnected due to lost communication.
* Any possible cause noted is limited to source-described possibilities and direct site observation.
* The count and any directly supported observation are documented without over-interpreting logs.

## Failure Conditions

* The disconnected AGV count cannot be located or read.
* The count cannot be reconciled with visible AGV state or known site observations.
* Logs are used to infer a turned-off AGV when the source does not support that conclusion.
* An unsupported root cause is assigned.

## Escalation Guidance

* Escalate if the disconnected count cannot be reconciled with visible AGV state or known site observations.
* Escalate when the available evidence is insufficient to distinguish between communication loss and a powered-off AGV.
* Do not over-interpret logs; if logs only show disconnecting, document that limitation and escalate as needed.

## Missing Details / Known Gaps

* The source does not provide a numeric threshold for when the disconnected AGV count is abnormal.
* The source does not provide a recovery action to restore communication.
* The source does not define a required documentation system or record format.
* The source does not specify exact escalation destination or timing.
* The source does not provide a time estimate for this reference procedure.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_disconnected_agv_count
- Source ID: `training_video_day1`
- Source Type: `training_video`
