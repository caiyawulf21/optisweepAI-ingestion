# Replace a Tipper End Stop Assembly

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_replace_a_tipper_end_stop_assembly_v1` |
| Title | Replace a Tipper End Stop Assembly |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Remove a damaged tipper end stop and install a new end stop using two new M8x40 socket-head cap screws and Loctite®, inspect the opposite end stop for damage, reinstall any removed panels, and restart the operator station using the referenced procedures.

## When To Use

Use this procedure when a tipper end stop assembly is damaged and must be replaced to return the station to service.

## Do Not Use For

* Do not use this runbook as a substitute for the detailed Operator Station Lockout/Tagout procedure.
* Do not use this runbook as a substitute for the detailed Starting The Operator Station procedure.
* Do not use this runbook for post-restart verification beyond restarting the operator station, because the source does not provide those details.

## Safety And Operational Notes

* This procedure includes lockout/tagout and physical component replacement.
* Use safety glasses and gloves.
* End stops typically work in pairs; a damaged bottom end stop may indicate one of the top end stops is also damaged, except in the event of a belt failure.

## Access Or Tools Needed

* Access to the tipper
* Operator Station Lockout/Tagout procedure
* Starting The Operator Station procedure
* Replacement end stop
* Two M8x40 socket-head cap screws per end stop
* Safety glasses
* Gloves
* 3/8-in. wrench or socket
* 6-mm hex wrench
* Loctite®

## Procedure Steps

### Step 1 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure.

**Expected result:**
The tipper is in the lockout/tagout state required for maintenance.

**Stop or Escalate If:**

* The tipper cannot be placed in the required lockout/tagout state.
* Safe maintenance state cannot be confirmed.

---

### Step 2 — Gather replacement parts, PPE, and tools

**Responsible role:** L2_support

**Instruction:**
Gather the documented replacement parts, PPE, and tools: end stop, two new M8x40 socket-head cap screws per end stop, safety glasses, gloves, 3/8-in. wrench or socket, 6-mm hex wrench, and Loctite®.

**Expected result:**
All required parts, PPE, and tools are available at the work area.

**Stop or Escalate If:**

* The replacement end stop is not available.
* New M8x40 socket-head cap screws are not available.
* Required PPE or tools are not available.

---

### Step 3 — Remove the side panel if needed for access

**Responsible role:** L2_support

**Instruction:**
If necessary for access, use a 3/8-in. wrench or socket to remove the nine self-tapping screws securing the side panel, then remove the station side panel to access the motor.

**Expected result:**
The side panel is removed when needed and access to the service area is available.

**Screens / Images:**

![artifact_fig_7_12_end_stop](assets/artifact_fig_7_12_end_stop.png)

*Use the end stop maintenance diagram for orientation to the end stop service area during access and replacement.*


**Stop or Escalate If:**

* The side panel cannot be removed safely.
* Fasteners cannot be removed.
* Required access to the motor/end stop area is still not available.

---

### Step 4 — Remove the damaged end stop

**Responsible role:** L2_support

**Instruction:**
Remove the two M8 socket-head screws holding the end stop in place.

**Expected result:**
The damaged end stop is removed from the tipper.

**Screens / Images:**

![artifact_fig_7_12_end_stop](assets/artifact_fig_7_12_end_stop.png)

*Locate the end stop and the two M8x40 socket-head screws used to secure it.*


**Stop or Escalate If:**

* The two M8 socket-head screws cannot be removed.
* The end stop cannot be removed from its mounting location.

---

### Step 5 — Install the new end stop

**Responsible role:** L2_support

**Instruction:**
Mount the new end stop using two new M8 socket-head screws and Loctite®.

**Expected result:**
The new end stop is installed using new hardware and Loctite®.

**Screens / Images:**

![artifact_fig_7_12_end_stop](assets/artifact_fig_7_12_end_stop.png)

*Use the end stop diagram to confirm the replacement end stop mounting location.*


**Stop or Escalate If:**

* The new end stop cannot be mounted securely.
* New M8 socket-head screws are not available.
* Loctite® is not available.

---

### Step 6 — Inspect the opposite end stop and replace if needed

**Responsible role:** L2_support

**Instruction:**
Check the opposite end stop for damage and replace it if necessary, noting that end stops typically work in pairs and a bottom collision often means one of the top end stops is also damaged, except in the event of a belt failure.

**Expected result:**
The opposite end stop is inspected and replaced if damage is found.

**Screens / Images:**

![artifact_fig_7_12_end_stop](assets/artifact_fig_7_12_end_stop.png)

*Use the end stop figure to identify paired end stop locations and mounting points.*


**Stop or Escalate If:**

* The opposite end stop is damaged and replacement cannot be completed.
* The condition of the opposite end stop cannot be determined.

---

### Step 7 — Reinstall removed side panels

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and/or bottom side panels if they were removed.

**Expected result:**
Any removed side panels are reinstalled.

**Stop or Escalate If:**

* Any removed panel cannot be reinstalled.

---

### Step 8 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced Starting The Operator Station procedure.

**Expected result:**
The operator station is restarted using the referenced procedure.

**Stop or Escalate If:**

* The operator station cannot be restarted.
* Post-restart condition cannot be confirmed from this source.

---

## Success Criteria

* The damaged end stop is replaced.
* The new end stop is installed using two new M8x40 socket-head cap screws and Loctite®.
* The opposite end stop is checked for damage and replaced if necessary.
* Any removed side panels are reinstalled.
* The operator station is restarted using the referenced procedure.

## Failure Conditions

* The tipper cannot be placed in the required lockout/tagout state.
* Required replacement parts, PPE, or tools are missing.
* The side panel cannot be removed when access is needed.
* The end stop mounting screws cannot be removed.
* The new end stop cannot be installed correctly.
* The opposite end stop is damaged and cannot be replaced.
* Removed panels cannot be reinstalled.
* The operator station cannot be restarted.
* Post-restart verification details are not provided by the source.

## Escalation Guidance

* Escalate if lockout/tagout cannot be completed or safe maintenance state cannot be confirmed.
* Escalate if required replacement parts, new M8x40 socket-head cap screws, PPE, or tools are unavailable.
* Escalate if the opposite end stop is also damaged and cannot be replaced during the same maintenance activity.
* Escalate if the operator station cannot be restarted using the referenced procedure.
* Escalate for any required post-restart verification because this source does not provide those details.

## Missing Details / Known Gaps

* The packet does not provide the detailed steps of the referenced Operator Station Lockout/Tagout procedure.
* The packet does not provide the detailed steps of the referenced Starting The Operator Station procedure.
* The source does not provide a time estimate for this procedure in the packet.
* The source does not provide torque values for the end stop screws in the packet.
* The source does not provide post-restart verification steps beyond restarting the operator station.
* No source OCR text was supplied in the section bundle text field; finalization relies on candidate content, source refs, and artifact metadata from this packet.

## Source Lineage

- Candidate IDs: candidate_l2_replace_tipper_end_stop_assembly
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
