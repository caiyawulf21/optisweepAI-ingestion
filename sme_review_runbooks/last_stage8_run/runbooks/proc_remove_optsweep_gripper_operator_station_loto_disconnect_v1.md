# Remove OptiSweep Gripper at the Operator Station (LOTO + Disconnect Valve/Air/Cables)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_optsweep_gripper_operator_station_loto_disconnect_v1` |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi`, `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Safely stop the OptiSweep tipper cycle from the operator station HMI, lock out the tipper at the station e-panel, and disconnect the gripper hardware (valve cover, supply air line, four M8 connectors, and the A-axis cable carrier routed through the grommet) to prepare for gripper replacement.

## When To Use

Use when performing OptiSweep gripper replacement removal at the operator station and you must stop the cycle, LOTO the tipper, and disconnect the gripper’s valve/air/electrical connections and A-axis cable carrier.

## Source Procedure References

- proc_remove_optsweep_gripper_operator_station_loto_disconnect_v1

## Safety And Operational Notes

- CAUTION HEAVY EQUIPMENT: Components may be heavy. Use caution when lifting. Failure to follow these instructions can result in injury or equipment damage.

## Procedure Steps

### Step 1 — Navigate to Visu_MCP_Dual on the operator station HMI

**Responsible role:** operator

**Instruction:**
At the operator station HMI, navigate to the "Visu_MCP_Dual" screen.

**Expected result:**
The "Visu_MCP_Dual" screen is displayed and ready for control inputs.

---

### Step 2 — Stop the cycle and enable manual tipper control

**Responsible role:** operator

**Instruction:**
Press CYCLE STOP to stop the cycle, then press JOG to manually control the tipper.

**Expected result:**
The cycle is stopped and manual control is enabled via JOG.

---

### Step 3 — Move the gripper to the desired location using axis buttons

**Responsible role:** operator

**Instruction:**
Use the axis buttons for the corresponding tipper to move the gripper to the desired location.

**Expected result:**
The gripper is positioned at the desired location using the axis buttons.

---

### Step 4 — Support carriages if gripper is moved from home position

**Responsible role:** operator

**Instruction:**
If the gripper is moved from its home position, thread screws into the threaded holes in the column to support the carriages between the pair or holes.

**Expected result:**
Screws are threaded into the column threaded holes to support the carriages between the pair or holes.

---

### Step 5 — LOTO the tipper at the station e-panel

**Responsible role:** operator

**Instruction:**
LOTO the tipper at the station e-panel (see "Operator Station Lockout/Tagout" on page 2).

**Expected result:**
The tipper is locked out at the station e-panel.

---

### Step 6 — Verify correct gripper selection (left vs right)

**Responsible role:** operator

**Instruction:**
Verify the correct gripper has been selected (i.e., left gripper or right gripper).

**Expected result:**
You confirm whether the left or right gripper is selected for the removal/disconnection work.

---

### Step 7 — Remove valve cover (four M4x50 socket-head screws)

**Responsible role:** operator

**Instruction:**
Remove the four (4) M4x50 socket-head screws from the valve cover, then remove the valve cover.

**Expected result:**
The valve cover is removed after removing the four M4x50 socket-head screws.

---

### Step 8 — Disconnect all four M8 connectors

**Responsible role:** operator

**Instruction:**
Disconnect all four (4) M8 connectors.

**Expected result:**
All four M8 connectors are disconnected from the valve/gripper assembly.

---

### Step 9 — Disconnect the supply air line on top of the valve

**Responsible role:** operator

**Instruction:**
Disconnect the supply air line on the top of the valve.

**Expected result:**
The supply air line is disconnected from the top of the valve.

---

### Step 10 — Plug fitting and cap air line to prevent debris entry

**Responsible role:** operator

**Instruction:**
Plug the fitting and cap the air line to prevent debris from entering either; if plugs/caps are not available, use tape to protect both.

**Expected result:**
The fitting is plugged and the air line is capped (or protected with tape if plugs/caps are unavailable).

---

### Step 11 — Feed capped air line through the grommet

**Responsible role:** operator

**Instruction:**
Feed the capped air line through the grommet.

**Expected result:**
The capped air line is routed through the grommet.

---

### Step 12 — Pull jacketed cable out of the grommet

**Responsible role:** operator

**Instruction:**
Pull the jacketed part of the cable out of the grommet.

**Expected result:**
The jacketed part of the cable is pulled out of the grommet.

---

### Step 13 — Feed all M8 connectors through the grommet one at a time

**Responsible role:** operator

**Instruction:**
Feed all of the M8 connectors through the grommet one at a time.

**Expected result:**
All four M8 connectors are routed through the grommet.

---

### Step 14 — Detach A-axis cable carrier by removing two M3x8 screws (save screws)

**Responsible role:** operator

**Instruction:**
Detach the A-axis cable carrier from the gripper by removing the two (2) M3x8 screws holding the cable carrier end. Save the screws.

**Expected result:**
A-axis cable carrier is detached from the gripper; the two M3x8 screws are removed and saved.

---

### Step 15 — Reinstall valve cover using four M4x50 socket-head screws

**Responsible role:** operator

**Instruction:**
Install the valve cover using the four (4) M4x50 socket-head screws.

**Expected result:**
Valve cover is reinstalled and secured with four M4x50 socket-head screws.

---

### Step 16 — Remove gripper-to-gearbox attachment screws (M6x20) and support counter-balance

**Responsible role:** operator

**Instruction:**
Remove the 10 M6x20 socket-head screws attaching the gripper to the gearbox (suggested: fully remove nine (9) screws). Ensure the counter-balance is supported.

**Expected result:**
The gripper-to-gearbox attachment screws are removed (with the suggested approach of fully removing nine), and the counter-balance is supported.

---

## Success Criteria

- Cycle is stopped and tipper is LOTO’d.
- Gripper is positioned as required.
- Valve cover is removed (then reinstalled per procedure).
- Four M8 connectors are disconnected.
- Supply air line is disconnected and protected (plugged/capped or taped).
- Air line and cable are routed through the grommet.
- A-axis cable carrier is detached by removing two M3x8 screws (saved).
- Gripper-to-gearbox attachment screws (M6x20) are removed with counter-balance supported.

## Failure Conditions

- Cannot confirm correct gripper selection (left vs right) before disconnecting hardware.
- Counter-balance cannot be supported while removing gripper-to-gearbox screws.
- Cannot apply plugs/caps (or tape protection) to prevent debris entering the air line/fitting.
- Valve cover cannot be removed/reinstalled as specified (screws not removed/installed).
- Any M8 connector cannot be disconnected or routed through the grommet.

## Escalation Guidance

- If you cannot confirm correct gripper selection (left vs right) before disconnecting hardware, stop work and escalate.
- If you cannot support the counter-balance while removing the gripper-to-gearbox screws, stop work and escalate.
- If plugs/caps (or tape protection) cannot be applied to prevent debris entering the air line/fitting, stop work and escalate.
- If you cannot perform LOTO safely at the station e-panel, stop work and escalate.

## Missing Details / Known Gaps

- The manual references "Operator Station Lockout/Tagout" on page 2, but the LOTO procedure content and the exact e-panel lockout/tagout label/location are not included in this packet; operators must follow the referenced LOTO procedure.
