# Tipper Replacement - Installation (7.3.22.2)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_tipper_replacement_installation_7_3_22_2_v1` |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `physical_floor`, `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Install the new tipper onto the existing sub-plate, reconnect conduit/power/air/Ethernet to the column and control box, remount optional components if needed, reinstall side panels if necessary, and restart the operator station.

## When To Use

Use when a tipper has been removed and the area is prepared, and you need to install the replacement tipper and reconnect conduit/power/air/Ethernet so the operator station can be restarted.

## Source Procedure References

- proc_tipper_replacement_installation_7_3_22_2_v1

## Safety And Operational Notes

- PPE required by the procedure: safety glasses and gloves.

## Procedure Steps

### Step 1 — Install the new tipper onto the existing sub-plate

**Responsible role:** operator

**Instruction:**
Install the new tipper onto the existing sub-plate.

**Expected result:**
The new tipper is installed on the existing sub-plate.

---

### Step 2 — Reconnect conduit, power, air, and Ethernet to the column and control box

**Responsible role:** operator

**Instruction:**
Connect the conduit, power, air, and Ethernet to the column and control box.

**Expected result:**
Conduit/power/air/Ethernet are connected to the column and control box.

---

### Step 3 — Mount the gripper, if necessary

**Responsible role:** operator

**Instruction:**
Mount the gripper, if necessary (see "Gripper Replacement" on page 97).

**Expected result:**
If the gripper was removed or is not currently mounted, it is mounted.

---

### Step 4 — Reinstall top and/or bottom side panels, if necessary

**Responsible role:** operator

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Top and/or bottom side panels are reinstalled as needed.

---

### Step 5 — Re-start the operator station

**Responsible role:** operator

**Instruction:**
Re-start the operator station (see "Starting The Operator Station" on page 1).

**Expected result:**
The operator station is restarted.

---

## Success Criteria

- New tipper is installed on the existing sub-plate.
- Conduit/power/air/Ethernet are connected to the column and control box.
- Any necessary gripper and side panels are reinstalled.
- Operator station is restarted.

## Failure Conditions

- Operator station cannot be restarted after installation.

## Escalation Guidance

- If the operator station cannot be restarted after installation, stop and escalate per the manual’s operator station start guidance ("Starting The Operator Station" on page 1).

## Missing Details / Known Gaps

- This installation section does not specify exact reconnection details (e.g., connector types/locations) beyond 'conduit, power, air, and Ethernet to the column and control box.'
- The procedure references 'Starting The Operator Station' on page 1, but the specific restart actions/observables are not included in the provided source section.
