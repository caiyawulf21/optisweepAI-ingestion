# Replace an OptiSweep Operator Station Tipper (LOTO, disconnect power/Ethernet/air, remove and reinstall)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_replace_optiSweep_operator_station_tipper_loto_disconnect_reconnect_v1` |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `physical_floor`, `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Safely replace a failed/replaced OptiSweep operator station tipper by performing LOTO, disconnecting the tipper’s power (6-pin Molex), Ethernet (ClearLink controller), and air line (quick disconnect), removing the old tipper from the sub-plate, installing the new tipper onto the existing sub-plate, reconnecting conduit/power/air/Ethernet, and restarting the operator station.

## When To Use

Use when an OptiSweep operator station tipper must be removed and replaced, requiring LOTO and physical disconnection/reconnection of the tipper’s power (6-pin Molex), Ethernet (ClearLink controller), and air line (quick disconnect), followed by reinstall and operator station restart.

## Source Procedure References

- proc_replace_optiSweep_operator_station_tipper_loto_disconnect_reconnect_v1

## Safety And Operational Notes

- Perform LOTO on the tipper before disconnecting power/air/Ethernet.
- Use PPE: safety glasses and gloves.

## Procedure Steps

### Step 1 — Perform LOTO on the tipper

**Responsible role:** operator

**Instruction:**
Perform LOTO on the tipper using the method referenced as "Operator Station Lockout/Tagout".

**Expected result:**
The tipper is in a locked-out state prior to disconnecting the control box and tipper connections.

---

### Step 2 — Remove the station side panel (if necessary) to access the motor

**Responsible role:** operator

**Instruction:**
If necessary, use a 3/8-in. wrench or socket to remove the nine (9) self-tapping securing screws for the station side panel, then remove the station side panel to access the motor.

**Expected result:**
Station side panel is removed (when needed) and the motor area is accessible.

---

### Step 3 — Disconnect tipper power (6-pin Molex) at the control box and route cable into the column

**Responsible role:** operator

**Instruction:**
Remove the control box and disconnect the power cable from the tipper (6-pin Molex connector), then push the cable into the column.

**Expected result:**
6-pin Molex power cable is disconnected from the tipper and the cable is pushed into the column.

---

### Step 4 — Unplug Ethernet from the ClearLink controller and route into the column

**Responsible role:** operator

**Instruction:**
Unplug the Ethernet cable from the ClearLink controller and push the Ethernet cable into the column.

**Expected result:**
Ethernet cable is unplugged from the ClearLink controller and routed into the column.

---

### Step 5 — Disconnect air line at the quick disconnect (leave quick disconnect on tipper side)

**Responsible role:** operator

**Instruction:**
Disconnect the air line at the quick disconnect at the bottom of the column, leaving the quick disconnect with the tipper side of the air line.

**Expected result:**
Air line is disconnected at the quick disconnect, with the quick disconnect remaining on the tipper side of the air line.

---

### Step 6 — Tape air line and quick disconnect to prevent debris entry

**Responsible role:** operator

**Instruction:**
Add tape over the air line and quick disconnect to prevent debris from entering either side of the air line.

**Expected result:**
Tape is applied over the air line and quick disconnect on both sides to block debris entry.

---

### Step 7 — Fully disconnect conduit bringing power, air, and Ethernet to the column and free cables from the tipper

**Responsible role:** operator

**Instruction:**
Fully disconnect the conduit bringing power, air, and Ethernet to the column and pull these cables free from the tipper.

**Expected result:**
Conduit is disconnected and power/air/Ethernet cables are free from the tipper.

---

### Step 8 — Optional: remove gripper and counter-balance weights

**Responsible role:** operator

**Instruction:**
Optional but recommended: remove the gripper (see "Gripper Replacement" on page 97) and the counter-balance weights (see "Counter-balance weights" on page 95).

**Expected result:**
Gripper and counter-balance weights are removed if you choose to follow the optional recommendation.

---

### Step 9 — Remove the old tipper from the sub-plate

**Responsible role:** operator

**Instruction:**
With the tipper supported, remove the four (4) hex head screws holding the tipper to the sub-plate.

**Expected result:**
Four (4) hex head screws are removed and the old tipper is free from the sub-plate.

---

### Step 10 — Install the new tipper onto the existing sub-plate

**Responsible role:** operator

**Instruction:**
Install the new tipper onto the existing sub-plate.

**Expected result:**
New tipper is positioned on the existing sub-plate mounting interface.

---

### Step 11 — Reconnect conduit, power, air, and Ethernet to the column and control box

**Responsible role:** operator

**Instruction:**
Connect the conduit, power, air, and Ethernet to the column and control box.

**Expected result:**
Conduit/power/air/Ethernet are reconnected to the column and control box.

---

### Step 12 — Mount the gripper if necessary

**Responsible role:** operator

**Instruction:**
Mount the gripper, if necessary (see "Gripper Replacement" on page 97).

**Expected result:**
Gripper is mounted if it was removed.

---

### Step 13 — Reinstall top and/or bottom side panels if necessary

**Responsible role:** operator

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Side panels are reinstalled if they were removed.

---

### Step 14 — Re-start the operator station

**Responsible role:** operator

**Instruction:**
Re-start the operator station (see "Starting The Operator Station" on page 1).

**Expected result:**
Operator station is restarted after the tipper replacement and reconnections.

---

## Success Criteria

- Old tipper is removed from the sub-plate after disconnecting power (6-pin Molex), Ethernet (ClearLink controller), and air (quick disconnect).
- New tipper is installed on the existing sub-plate.
- Conduit/power/air/Ethernet are reconnected to the column and control box.
- Operator station is restarted.

## Failure Conditions

- LOTO cannot be completed before disconnecting power/air/Ethernet.
- Air line quick disconnect cannot be left on the tipper side as specified.
- Debris protection (tape) cannot be applied to both sides of the air line/quick disconnect.
- Four hex head screws cannot be removed/installed while the tipper is properly supported.
- Operator station cannot be restarted after replacement.

## Escalation Guidance

- If any stop condition is met (LOTO not possible, air quick disconnect side cannot be preserved, debris protection cannot be applied, or mounting screws cannot be removed/installed while supported), stop work and escalate rather than proceeding with disassembly/reassembly.

## Missing Details / Known Gaps

- The packet does not include the referenced "Operator Station Lockout/Tagout" page 2 procedure details (exact lockout points/steps).
- The packet does not include the referenced "Starting The Operator Station" page 1 restart procedure details (exact UI/power switch steps).
- The packet does not provide the exact mechanical steps for reinstalling the four (4) hex head screws during installation (it only states removal and that the tipper is installed).
