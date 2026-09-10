# Perform Full Replacement of the Z-Axis Cable Carrier (without replacing air line or FFC)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_perform_full_replacement_of_the_z_axis_cable_carrier_v1` |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `physical_floor`, `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Replace the Z-axis cable carrier end-to-end while preserving the existing air line and FFC, then verify the carrier is seated (cross bars closed, dividers clear of the FFC, joints fully seated/uniform end-to-end) and restart the operator station.

## When To Use

Use when the Z-axis cable carrier must be fully replaced end-to-end while keeping the existing air line and FFC.

## Source Procedure References

- proc_perform_full_replacement_of_the_z_axis_cable_carrier_v1

## Safety And Operational Notes

- Apply LOTO to the tipper before starting work (manual references “Operator Station Lockout/Tagout” on page 2).

## Procedure Steps

### Step 1 — Apply LOTO to the tipper

**Responsible role:** operator

**Instruction:**
Apply LOTO to the tipper using the manual’s “Operator Station Lockout/Tagout” method.

**Expected result:**
The tipper is under lockout/tagout (LOTO) and safe to service.

---

### Step 2 — Remove the station side panel to access the motor (if necessary)

**Responsible role:** operator

**Instruction:**
If necessary, use a 3/8-in. wrench or socket to remove the nine (9) self-tapping securing the station side panel, then remove the station side panel to access the motor.

**Expected result:**
Station side panel is removed and motor area is accessible.

---

### Step 3 — Mark the air line and FFC entry/exit points

**Responsible role:** operator

**Instruction:**
Mark the air line and FFC at both ends where they enter and exit the cable carrier using marker or tape.

**Expected result:**
Clear marks exist on the air line and FFC at both ends (entry/exit points).

---

### Step 4 — Document air line tie method and cut wire ties

**Responsible role:** operator

**Instruction:**
Note how the air line is tied to the cable carrier (take a picture) and cut the wire ties.

**Expected result:**
Air line tie points are documented and wire ties are cut so the carrier can be detached.

---

### Step 5 — Remove M3 screws holding FFC clamps in place (at both ends)

**Responsible role:** operator

**Instruction:**
At both ends of the cable carrier, remove the M3 socket-head screws holding the FFC clamps in place. Confirm the clamps should stay in place on the FFC; if they fall off, mark the FFC.

**Expected result:**
FFC clamps are released from the cable carrier; clamps remain on the FFC or the FFC is marked if clamps fall off.

---

### Step 6 — Detach the cable carrier by removing M3 screws at both ends

**Responsible role:** operator

**Instruction:**
Detach the cable carrier by removing the four M3 screws at both ends of the cable carrier.

**Expected result:**
Cable carrier is mechanically detached from both ends.

---

### Step 7 — Open cross bars and remove the old cable carrier

**Responsible role:** operator

**Instruction:**
Open all the cross bars on the outside of the cable carrier, and remove it from the FFC and air line. You may have to snap one end of the cable carrier off to fully remove it.

**Expected result:**
Old cable carrier is removed from the FFC and air line.

---

### Step 8 — Position the new cable carrier with dividers against the air line

**Responsible role:** operator

**Instruction:**
Open all the cross bars on the new cable carrier and probably one end. Put the new cable carrier roughly in place while positioning the internal dividers all the way to one side, against the air line.

**Expected result:**
New carrier is positioned roughly in place with internal dividers positioned against the air line.

---

### Step 9 — Snap cross bars closed ensuring dividers do not press on the FFC

**Responsible role:** operator

**Instruction:**
“Snap” all the cross bars closed, ensuring none of the dividers are pressing on the FFC; snap the end back on if necessary.

**Expected result:**
All cross bars are snapped closed and dividers are not pressing on the FFC.

---

### Step 10 — Mount both ends of the cable carrier with M3 flat-head screws

**Responsible role:** operator

**Instruction:**
Mount both ends using four M3 flat-head screws.

**Expected result:**
Both ends are mounted with four M3 flat-head screws.

---

### Step 11 — Attach FFC clamps using M3 socket-head screws aligned to marks

**Responsible role:** operator

**Instruction:**
Attach the FFC clamps using the M3 socket-head screws at both cable carrier ends; ensure the FFC clamps align with the marks from Step 1.

**Expected result:**
FFC clamps are secured at both ends and aligned to the previously applied marks.

---

### Step 12 — Wire-tie the air line in the cable carrier using marks

**Responsible role:** operator

**Instruction:**
Position the air line in the cable carrier using the marks from Step 1 and wire tie it in place.

**Expected result:**
Air line is positioned according to Step 1 marks and secured with wire ties.

---

### Step 13 — Inspect cable carrier seating, clearance, and joint uniformity

**Responsible role:** operator

**Instruction:**
Inspect the cable carrier: verify all cross bars are closed, the dividers are not pressing on the FFC, and all the cable carrier joints are fully seated. The cable carrier should look very uniform end to end.

**Expected result:**
Cross bars are closed; dividers are not pressing on the FFC; joints are fully seated; carrier appears uniform end-to-end.

---

### Step 14 — Reinstall top and/or bottom side panels (if necessary)

**Responsible role:** operator

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Top and/or bottom side panels are reinstalled as required.

---

### Step 15 — Restart the operator station

**Responsible role:** operator

**Instruction:**
Re-start the operator station (see “Starting The Operator Station” on page 66).

**Expected result:**
Operator station restarts successfully.

---

## Success Criteria

- New Z-axis cable carrier installed with all cross bars closed.
- Dividers are not pressing on the FFC.
- Cable carrier joints are fully seated and carrier looks uniform end to end.
- Operator station restarts successfully.

## Failure Conditions

- Dividers press on the FFC.
- Cable carrier joints not fully seated or non-uniform end-to-end appearance.
- FFC clamps misaligned (not aligned to Step 1 marks).
- Operator station does not restart after reassembly.

## Escalation Guidance

- If the operator station does not restart after reassembly, escalate to the appropriate support process referenced by the manual’s “Starting The Operator Station” on page 66.

## Missing Details / Known Gaps

- The manual section provided references “Starting The Operator Station” on page 66, but the specific restart control/sequence is not included in the provided source text; operator must follow the referenced page for the exact restart actions.
