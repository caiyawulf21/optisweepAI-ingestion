# Check Fleet-Level AGV Status on “Overall System AGV Status” (Top: all AGVs, Bottom: AGVs with errors)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_fleet_level_agv_status_overall_system_agv_status_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | None |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS / fleet status UI screen labeled “Overall System AGV Status” to review fleet-level AGV information. Confirm the Top Section lists all AGVs with columns for ID, Status, Destination, and Errors, then use the Bottom Section (“Only AGVs with errors”) to identify which AGVs currently have errors.

## When To Use

When you need a fleet-level view of AGV status and to quickly identify which AGVs currently show errors using the “Overall System AGV Status” screen’s two sections (Top: all AGVs; Bottom: only AGVs with errors).

## Source Procedure References

- proc_check_fleet_level_agv_status_overall_system_agv_status_v1

## Procedure Steps

### Step 1 — Open the RMS / fleet status UI and navigate to “Overall System AGV Status”

**Responsible role:** L1_support

**Instruction:**
Using the RMS / fleet status UI (rms_ui), open the screen labeled “Overall System AGV Status”.

**Expected result:**
The “Overall System AGV Status” screen loads and shows two sections: a Top Section for detailed info for all AGVs and a Bottom Section labeled for AGVs with errors.

---

### Step 2 — Confirm Top Section columns include ID, Status, Destination, and Errors

**Responsible role:** L1_support

**Instruction:**
In the Top Section (“Detailed info for all AGVs”), confirm the table/fields shown include: AGV ID, Status, Destination, and Errors.

**Expected result:**
The Top Section displays columns/fields labeled for ID, Status, Destination, and Errors.

---

### Step 3 — Scan Top Section rows for non-empty Errors values

**Responsible role:** L1_support

**Instruction:**
Scan the Top Section rows and observe which AGVs have non-empty values in the Errors column.

**Expected result:**
At least one AGV row shows a non-empty Errors value (if any errors are present in the fleet view).

---

### Step 4 — Inspect Bottom Section “Only AGVs with errors” and confirm it is filtered

**Responsible role:** L1_support

**Instruction:**
Scroll/inspect the Bottom Section labeled “Only AGVs with errors” and confirm it lists only AGVs that have errors.

**Expected result:**
The Bottom Section shows only AGVs with errors (i.e., the list is filtered to error-bearing AGVs).

---

## Success Criteria

- Top Section shows columns/fields for ID, Status, Destination, and Errors.
- Bottom Section (“Only AGVs with errors”) is filtered to only AGVs that have non-empty Errors values in the Top Section.
- If errors exist in the Top Section, the Bottom Section is not empty.

## Failure Conditions

- RMS/fleet status UI screen is blank/unreachable.
- Bottom Section is empty while Top Section shows multiple AGVs with non-empty Errors.
- Bottom Section does not reflect the Errors shown in the Top Section.

## Escalation Guidance

- If the Bottom Section is empty while the Top Section shows multiple AGVs with non-empty Errors, or if the screen is blank/unreachable, escalate for investigation of RMS/fleet status UI filtering/refresh behavior.

## Missing Details / Known Gaps

- The packet does not provide explicit RMS navigation clicks/menus to reach “Overall System AGV Status”; it only specifies the screen label and the expected two-section layout.
- The packet does not provide example row values (specific Status/Destination/Error text) to use as exact matching targets—only the presence of the fields and the filtered behavior of the Bottom Section.
