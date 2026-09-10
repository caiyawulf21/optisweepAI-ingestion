# Use Cell Selection to View Cell Code (Node Code) and Station/Workstation ID

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_cell_selection_view_cell_code_node_code_station_workstation_id_v1` |
| Title | Use Cell Selection to View Cell Code (Node Code) and Station/Workstation ID |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep map’s Cell Selection (QR code) view to click a map cell and read the displayed 8-digit cell code (node code / physical QR code number) for that location. For orange station cells, the UI also shows the workstation ID, which you can use to coordinate where to bring/push an AGB.

## When To Use

When you need the 8-digit cell code (node code / physical QR code number) for a map location, and when the selected cell is an orange station and you also need the workstation ID for coordination.

## Do Not Use For

* Do not use this procedure as a replacement for physical verification of the QR code on the floor when the map/UI values are not showing the expected cell code or station/workstation ID.

## Access Or Tools Needed

* OptiSweep map UI with “cell selection” mode (QR code view)
* Ability to click/select cells on the map
* On-screen cell information display showing the 8-digit cell code and (for orange station cells) workstation ID

## Related Operational Context

* ctx_training_video_cell_selection_qr_code_v1
* ctx_training_video_station_cell_workstation_id_v1
* ctx_training_video_cell_code_unique_identifier_v1

## Procedure Steps

### Step 1 — Open the map view where “cell selection” is available (QR code view)

**Responsible role:** L1_support

**Instruction:**
Open the OptiSweep map view and switch to the “cell selection” view (described as the QR code view).

**Expected result:**
The map is in Cell Selection (QR code) mode so that clicking a cell will display cell information including the QR code / node code.

---

### Step 2 — Select a cell on the map to view the cell information (QR code / node code)

**Responsible role:** L1_support

**Instruction:**
In Cell Selection mode, click/select the target cell on the map to display its cell information including the QR code.

**Expected result:**
The UI shows cell information for the selected map cell, including an 8-digit number.

---

### Step 3 — Read the 8-digit cell code (node code / physical QR code number)

**Responsible role:** L1_support

**Instruction:**
From the selected cell’s information, read the displayed 8-digit number and record it as the cell code (node code / physical QR code number) for that location.

**Expected result:**
You have an 8-digit cell code (node code / physical QR code number) corresponding to the selected map location.

**Stop or Escalate If:**

* If the selected cell does not show the expected 8-digit cell code, stop and escalate for assistance (no troubleshooting steps are provided in the source).

---

### Step 4 — If the selected cell is an orange station, confirm and record the workstation ID

**Responsible role:** L1_support

**Instruction:**
Check whether the selected cell is an orange cell (station). If it is orange, confirm the UI shows an additional workstation ID value along with the QR/cell code, and record that workstation ID.

**Expected result:**
For an orange station cell, the UI shows both the 8-digit cell code and an additional workstation ID value (example given: station ID 862).

**Stop or Escalate If:**

* If the selected cell is an orange station and it does not show the expected workstation ID, stop and escalate for assistance (no troubleshooting steps are provided in the source).

---

### Step 5 — Use the cell code (and workstation ID when applicable) to coordinate AGB movement

**Responsible role:** L1_support

**Instruction:**
If operator coordination is needed, use the recorded cell code to ask the operator to bring/push the AGB to that cell (example format given: “bring the AGB to cell … like 12345678”). If you recorded a workstation ID for an orange station cell, include it as part of the station reference as needed for coordination.

**Expected result:**
The operator receives a clear cell reference using the 8-digit cell code (node code / physical QR code number) for the target location.

---

## Success Criteria

* You can select a map cell in Cell Selection (QR code) mode and observe an 8-digit cell code (node code / physical QR code number) for that location.
* When the selected cell is an orange station cell, you can also observe and record the workstation ID shown by the UI.

## Failure Conditions

* Selected cell does not show the expected 8-digit cell code.
* Selected orange station cell does not show the workstation ID value.

## Escalation Guidance

* If the selected cell does not show the expected 8-digit cell code, stop and escalate for assistance (the source provides no troubleshooting steps).
* If the selected cell is an orange station and it does not show the workstation ID, stop and escalate for assistance (the source provides no troubleshooting steps).

## Missing Details / Known Gaps

* The packet does not specify the exact UI navigation path/menu name for enabling “cell selection” beyond describing it as the QR code view.
* The packet does not provide explicit troubleshooting steps for cases where the 8-digit cell code or workstation ID is missing.

## Source Lineage

- Candidate IDs: candidate_training_video_cell_selection_qr_node_code
- Source ID: `training_video_day1`
- Source Type: `training_video`
