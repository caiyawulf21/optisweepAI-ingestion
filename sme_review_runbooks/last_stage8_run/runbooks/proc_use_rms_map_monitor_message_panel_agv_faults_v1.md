# Use RMS Map Monitor Message Panel to view AGV fault list, fault details, and locate a faulted AGV

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_rms_map_monitor_message_panel_agv_faults_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `agv_active_errors` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS / fleet status UI Map Monitor message panel to identify faulted/disconnected AGVs, view the selected fault’s details, and use the “Locate Faulted AGV” control to bring up the corresponding location cue.

## When To Use

When you need to determine which AGVs are faulted and/or disconnected and then inspect the fault details and locate the affected AGV using the RMS Map Monitor message panel.

## Source Procedure References

- proc_use_rms_map_monitor_message_panel_agv_faults_v1

## Procedure Steps

### Step 1 — Open the RMS / fleet status UI and navigate to the Map Monitor message panel

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the Map Monitor message panel on the right side of the interface.

**Expected result:**
The Map Monitor message panel is visible on the right side and shows the labeled items: “Count of active Robots”, “Count of Robots charging”, “Drop down to show AGV faults”, “Count of AGVs disconnected”, “Inspection to view details of fault”, and “Locate Faulted AGV”.

---

### Step 2 — Verify the active robot and charging count metrics

**Responsible role:** L1_support

**Instruction:**
On the Map Monitor message panel, locate and verify the fields labeled “Count of active Robots” and “Count of Robots charging”.

**Expected result:**
Both count fields are displayed on the panel.

---

### Step 3 — Open the AGV faults dropdown to display the fault list

**Responsible role:** L1_support

**Instruction:**
Use the dropdown labeled “Drop down to show AGV faults” to display the AGV fault list.

**Expected result:**
The AGV faults dropdown expands and shows fault entries.

---

### Step 4 — Check the count of AGVs disconnected

**Responsible role:** L1_support

**Instruction:**
On the same Map Monitor message panel, locate and check the field labeled “Count of AGVs disconnected”.

**Expected result:**
A numeric value is shown for “Count of AGVs disconnected”.

---

### Step 5 — Select a fault entry and confirm fault details update

**Responsible role:** L1_support

**Instruction:**
In the AGV faults list, select a fault entry and use the “Inspection to view details of fault” area to confirm the fault details update for the selected entry.

**Expected result:**
The “Inspection to view details of fault” area updates to show details for the selected fault entry.

---

### Step 6 — Locate the faulted AGV using the “Locate Faulted AGV” control

**Responsible role:** L1_support

**Instruction:**
Use “Locate Faulted AGV” to bring up the faulted AGV location cue (e.g., map highlight/selection) and confirm the located AGV corresponds to the selected fault.

**Expected result:**
A location cue appears for the faulted AGV after using “Locate Faulted AGV”, and it corresponds to the selected fault entry.

---

## Success Criteria

- The Map Monitor message panel shows “Count of active Robots” and “Count of Robots charging”.
- The “Drop down to show AGV faults” displays fault entries.
- Selecting a fault entry updates the “Inspection to view details of fault” area.
- Using “Locate Faulted AGV” produces a location cue that corresponds to the selected faulted AGV.

## Failure Conditions

- AGV faults dropdown shows no fault entries while AGV issues are reported.
- Fault details do not update after selecting a fault entry.
- Locate Faulted AGV location cue does not correspond to the selected fault.

## Escalation Guidance

- If the AGV faults dropdown shows no fault entries while the site reports AGV issues, escalate for deeper RMS/WCS API/DB corroboration.
- If “Inspection to view details of fault” does not update after selecting a fault entry, escalate for UI/API data issues.

## Missing Details / Known Gaps

- The source does not provide exact click/field interaction behavior beyond the labeled panel elements; if the UI differs, follow the closest matching labeled controls on the live RMS Map Monitor message panel.
- The source does not specify the exact visual form of the “Locate Faulted AGV” cue (e.g., map highlight color/shape); confirm correspondence by matching the located AGV to the selected fault entry.
