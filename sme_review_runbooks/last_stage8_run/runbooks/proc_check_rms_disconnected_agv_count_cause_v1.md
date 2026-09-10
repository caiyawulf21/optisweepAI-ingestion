# Check RMS disconnected AGV count and identify likely disconnect cause (lost RMS comms vs turned off)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_rms_disconnected_agv_count_cause_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `agv_active_errors` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_smeme_review` |
| Merge Status | `pass_through` |

## Summary

On the RMS / fleet status UI map monitor summary, read the “count of AGVs disconnected” metric. Use the training’s definition to interpret “disconnected” as AGVs that have lost communication from RMS (RMS runs on the server; AGVs are on Wi‑Fi), then correlate the disconnected count with likely causes: Wi‑Fi/RMS communication loss vs AGVs being turned off.

## When To Use

When you need a first-pass diagnostic using RMS’s disconnected AGV count to understand whether AGVs are likely disconnected due to lost RMS/Wi‑Fi communication versus being turned off.

## Source Procedure References

- proc_check_rms_disconnected_agv_count_cause_v1

## Procedure Steps

### Step 1 — Open RMS / fleet status UI map monitor summary area

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the map monitor summary/message panel area that includes the “count of AGVs disconnected” metric.

**Expected result:**
The RMS UI shows the map monitor summary/message panel with a visible “count of AGVs disconnected” value.

---

### Step 2 — Read the “count of AGVs disconnected” value

**Responsible role:** L1_support

**Instruction:**
In the RMS map monitor summary/message panel, locate and read the “count of AGVs disconnected” value.

**Expected result:**
You have the numeric value for “count of AGVs disconnected” as shown in the RMS UI.

---

### Step 3 — Interpret “disconnected” as lost RMS communication (RMS server + AGVs on Wi‑Fi)

**Responsible role:** L1_support

**Instruction:**
Use the definition: treat “disconnected” as AGVs that have lost communication from RMS (RMS is the application running on the server; AGVs are on the Wi‑Fi).

**Expected result:**
Your interpretation of the disconnected count is explicitly tied to lost communication from RMS to AGVs over Wi‑Fi.

---

### Step 4 — Correlate disconnected count with likely causes: Wi‑Fi/RMS comms loss vs AGV turned off

**Responsible role:** L1_support

**Instruction:**
Correlate the disconnected count with likely causes: (1) AGVs lost communication with the Wi‑Fi on site, or (2) the AGV was turned off.

**Expected result:**
You produce a likely cause hypothesis that matches one of the two causes explicitly described: Wi‑Fi/RMS communication loss or AGV turned off.

---

## Success Criteria

- You can read the RMS “count of AGVs disconnected” metric from the RMS / fleet status UI.
- You interpret “disconnected” as lost communication from RMS to AGVs over Wi‑Fi.
- You correlate the disconnected count to one of the two explicitly described likely causes: Wi‑Fi/RMS communication loss or AGV turned off.

## Failure Conditions

- Disconnected count is high and you cannot determine whether the cause is communication loss vs AGVs being turned off using only this metric.

## Escalation Guidance

- If the disconnected count is high and you cannot determine whether the cause is communication loss vs AGVs being turned off, stop and escalate for additional evidence beyond this metric (involve L2_support).

## Missing Details / Known Gaps

- The packet does not provide a separate live UI check (beyond the disconnected count metric) to confirm whether the disconnected AGVs were turned off vs Wi‑Fi/RMS communication loss; escalation is required when the cause cannot be determined from this metric alone.
