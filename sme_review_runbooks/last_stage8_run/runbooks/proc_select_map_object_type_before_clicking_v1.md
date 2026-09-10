# Select Map Object Type (Robot/Container/Cell/Charger) Before Clicking on the Map

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_select_map_object_type_before_clicking_v1` |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Capability Tags | `device_roster_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

In the RMS / fleet status UI Map Monitor, multiple object types are clickable. Select the correct Quick Select object selection mode (Robot/Container/Cell/Charger) on the left panel before clicking a map item so you inspect the intended object type.

## When To Use

Use when you need to inspect a specific object type on the RMS Map Monitor map (robot vs container vs cell vs charger) and you want the map click to target the correct type.

## Source Procedure References

- proc_select_map_object_type_before_clicking_v1

## Procedure Steps

### Step 1 — Open RMS Map Monitor and locate Quick Select object selection icons

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (Map Monitor). On the left panel, locate the Quick Select object selection icons for Robot, Container (if present), Cell, and Charger.

**Expected result:**
The left-side Quick Select icons for object selection modes are visible (Robot Selection, Cell Selection, Charger Selection; container selection icon if present).

---

### Step 2 — Choose the object type you want to inspect

**Responsible role:** L1_support

**Instruction:**
Decide whether you want to inspect a robot, container, cell, or charger.

**Expected result:**
You have selected the intended object type to inspect (robot vs container vs cell vs charger).

---

### Step 3 — Select the corresponding Quick Select icon for the chosen object type

**Responsible role:** L1_support

**Instruction:**
On the left panel, click the Quick Select icon that matches your chosen object type (e.g., click “Robot Selection” to inspect robots).

**Expected result:**
The Quick Select mode corresponding to the chosen object type is selected (e.g., Robot Selection for robots).

---

### Step 4 — Click the target object on the map

**Responsible role:** L1_support

**Instruction:**
Click the target object on the map.

**Expected result:**
The clicked map item is inspected as the selected object type (robot/container/cell/charger).

---

### Step 5 — Verify the click inspects the intended object type; re-select mode if not

**Responsible role:** L1_support

**Instruction:**
Verify that the clicked object responds as the selected type (robot vs container vs cell vs charger). If it does not, stop and re-select the correct object type icon before clicking again.

**Expected result:**
You confirm the clicked object is inspected as the intended object type; otherwise you re-select the correct mode and repeat the click.

---

## Success Criteria

- After selecting the correct Quick Select object selection icon, clicking a map item inspects that chosen object type (robot/container/cell/charger).

## Failure Conditions

- A map click inspects a different object type than the selected Quick Select mode.
- User proceeds to click without selecting the intended object type icon first.

## Escalation Guidance

- If you cannot get the map click to inspect the intended object type even after re-selecting the correct Quick Select icon, stop and escalate to the appropriate support team/site process (no further escalation steps are specified in the provided source).

## Missing Details / Known Gaps

- The source requests image support for the exact UI feedback after selecting a mode and for the map interaction showing that selection mode changes what becomes inspectable; those specific feedback/interaction images are not provided in the packet for this runbook.
