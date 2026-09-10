# Remove and unplug Controller PCA in a tipper station (Controller PCA Replacement — Removal)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_and_unplug_controller_pca_in_tipper_station_v1` |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Safely remove the Controller PCA from an OptiSweep tipper station by applying LOTO, accessing the controller box, loosening the controller box mounting screws, removing the ribbon cable retainer screws, and unplugging the PCA connections (FFC, ribbon cable, and three Molex connectors) so the assembly is ready for replacement.

## When To Use

When performing Controller PCA Replacement — Removal on an OptiSweep tipper station and you must remove/unplug the Controller PCA connections for replacement.

## Source Procedure References

- proc_remove_and_unplug_controller_pca_in_tipper_station_v1

## Safety And Operational Notes

- Apply LOTO to the tipper before touching internal components.

## Procedure Steps

### Step 1 — Apply LOTO to the tipper

**Responsible role:** operator

**Instruction:**
Perform LOTO on the tipper using the referenced "Operator Station Lockout/Tagout" procedure (page 2).

**Expected result:**
The tipper is locked out (LOTO confirmed) before proceeding to internal components.

---

### Step 2 — Remove the station side panel if needed to access the motor

**Responsible role:** operator

**Instruction:**
If necessary, use a 3/8-in. wrench or socket to remove the nine (9) self-tapping securing screws for the station side panel, then remove the station side panel to access the motor.

**Expected result:**
Station side panel is removed (when needed) and the motor access area is reachable.

---

### Step 3 — Loosen the four M8 button-head screws to release the controller box

**Responsible role:** operator

**Instruction:**
Loosen the four (4) M8 button-head screws that secure the controller box. Do not remove the fasteners—loosen them so the controller box can be lifted off the fasteners.

**Expected result:**
Controller box is released such that it can be lifted off after loosening the four (4) M8 button-head screws.

---

### Step 4 — Remove the two M3 socket-head screws holding the ribbon cable retainer

**Responsible role:** operator

**Instruction:**
Remove the two (2) M3 socket-head screws holding the ribbon cable retainer in place.

**Expected result:**
Ribbon cable retainer is released after removing the two (2) M3 socket-head screws.

---

### Step 5 — Unplug all PCA connections (FFC, ribbon cable, and three Molex connectors)

**Responsible role:** operator

**Instruction:**
Unplug all connections from the PCA: FFC, ribbon cable, and the three Molex connectors.

**Expected result:**
All PCA connections are unplugged: FFC and ribbon cable are disconnected, and three Molex connectors are unplugged.

---

## Success Criteria

- LOTO is applied to the tipper before internal access.
- Station side panel is removed (if needed) to access the motor/controller box area.
- Controller box is released after loosening four (4) M8 button-head screws (fasteners loosened, not removed).
- Ribbon cable retainer is released after removing two (2) M3 socket-head screws.
- All PCA connections are unplugged: FFC, ribbon cable, and three Molex connectors.

## Failure Conditions

- LOTO cannot be confirmed before touching internal components.
- Controller box cannot be lifted after loosening the four (4) M8 button-head screws.
- Ribbon cable retainer screws/retainer do not match the documented counts (2x M3).
- Any PCA connections cannot be unplugged without excessive force.

## Escalation Guidance

- Escalate to FORTNA support if any PCA connections cannot be unplugged without excessive force or if screws/retainers do not match the documented counts (4x M8, 2x M3).

## Missing Details / Known Gaps

- The candidate references a separate "Operator Station Lockout/Tagout" procedure on page 2, but the packet does not include the LOTO sub-steps themselves; follow that referenced procedure for the exact lockout/tagout actions.
