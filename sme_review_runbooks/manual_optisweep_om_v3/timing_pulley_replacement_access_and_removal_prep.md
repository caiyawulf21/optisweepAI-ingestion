# Prepare for timing pulley replacement and access the motor area

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_prepare_for_timing_pulley_replacement_and_access_the_motor_area_v1` |
| Title | Prepare for timing pulley replacement and access the motor area |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely prepare for timing pulley replacement by applying lockout/tagout to the tipper, gathering the specified replacement part, PPE, and tools, avoiding use of the round end of the hex wrench, and removing the station side panel if needed to access the motor. Figure 7-20 is used to identify the timing pulley assembly components and the referenced 8 mm (0.315 in.) gap.

## When To Use

Use this procedure when preparing for timing pulley replacement and when access to the motor area is required as part of the timing pulley removal activity described in section 7.3.19 / 7.3.19.1 of the OptiSweep Operation and Maintenance Manual.

## Do Not Use For

* Do not use this runbook as a complete timing pulley removal or installation procedure; the packet only contains the initial preparation and access steps.
* Do not use the round end of the hex wrench.

## Safety And Operational Notes

* LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure on page 2.
* Do not use the round end of the hex wrench.
* Stop if lockout/tagout cannot be completed using the referenced procedure.
* Stop if the side panel cannot be safely removed or the motor area cannot be accessed with the specified fasteners and tools.

## Access Or Tools Needed

* Replacement pulley
* Safety glasses
* Gloves
* Torque wrench
* 1/8-in. hex wrench
* 8-mm hex wrench
* 3/8-in. wrench or socket
* Access to the tipper and station side panel
* Operator Station Lockout/Tagout procedure

## Procedure Steps

### Step 1 — Gather replacement part, PPE, and tools

**Responsible role:** L2_support

**Instruction:**
Gather the listed replacement part, PPE, and tools: pulley, safety glasses, gloves, torque wrench, 1/8-in. hex wrench, 8-mm hex wrench, and 3/8-in. wrench or socket.

**Expected result:**
All listed parts, PPE, and tools are available at the work area.

**Screens / Images:**

![artifact_fig_7_20_timing_pulley](assets/artifact_fig_7_20_timing_pulley.png)

*Use the timing pulley figure as the visual reference for the assembly you are preparing to access.*


**Stop or Escalate If:**

* Required replacement part, PPE, or tools are not available.

---

### Step 2 — Avoid using the round end of the hex wrench

**Responsible role:** L2_support

**Instruction:**
Do not use the round end of the hex wrench.

**Expected result:**
Only the correct end of the hex wrench is used during the procedure.

**Stop or Escalate If:**

* There is uncertainty about which end of the hex wrench is acceptable to use.
* The round end of the hex wrench would be required to continue.

---

### Step 3 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure on page 2.

**Expected result:**
The tipper is locked out and tagged out in accordance with the referenced procedure.

**Stop or Escalate If:**

* Lockout/tagout cannot be completed using the referenced procedure.
* The tipper cannot be confirmed in a safe maintenance state.

---

### Step 4 — Remove the side panel fasteners if motor access is needed

**Responsible role:** L2_support

**Instruction:**
If necessary to access the motor, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel.

**Expected result:**
The nine self-tapping fasteners are removed when side panel access is required.

**Screens / Images:**

![artifact_fig_7_20_timing_pulley](assets/artifact_fig_7_20_timing_pulley.png)

*Use the timing pulley assembly figure as the maintenance visual for the motor-area access context during timing pulley replacement.*


**Stop or Escalate If:**

* The side panel fasteners cannot be safely removed.
* The specified 3/8-in. wrench or socket does not allow safe removal.
* Motor access still cannot be obtained after fastener removal.

---

### Step 5 — Remove the station side panel

**Responsible role:** L2_support

**Instruction:**
Remove the station side panel to access the motor.

**Expected result:**
The station side panel is removed and the motor area is accessible.

**Screens / Images:**

![artifact_fig_7_20_timing_pulley](assets/artifact_fig_7_20_timing_pulley.png)

*Reference the timing pulley assembly diagram while opening access to the motor area.*


**Stop or Escalate If:**

* The side panel cannot be safely removed.
* The motor area cannot be accessed after panel removal.

---

### Step 6 — Identify timing pulley assembly components in Figure 7-20

**Responsible role:** L2_support

**Instruction:**
Identify the timing pulley components shown in Figure 7-20, including the set screws, 1108 taper-lock bushing, timing pulley, gearbox pilot face, and the noted 8 mm (0.315 in.) gap.

**Expected result:**
The timing pulley assembly components and referenced gap are correctly identified from the source figure.

**Screens / Images:**

![artifact_fig_7_20_timing_pulley](assets/artifact_fig_7_20_timing_pulley.png)

*Set screws, 1108 taper-lock bushing, timing pulley, gearbox pilot face, and the 8 mm (0.315 in.) gap.*


**Stop or Escalate If:**

* The timing pulley components shown in Figure 7-20 cannot be matched to the equipment being serviced.
* The 8 mm (0.315 in.) gap reference cannot be identified from the source figure.

---

## Success Criteria

* The required replacement part, PPE, and tools are gathered.
* The tipper is locked out and tagged out using the referenced procedure.
* The station side panel is removed if needed for access.
* The motor area is accessible for further timing pulley replacement work.
* The timing pulley assembly components in Figure 7-20 are identified.

## Failure Conditions

* Lockout/tagout cannot be completed using the referenced procedure.
* Required tools, PPE, or replacement part are missing.
* The side panel cannot be safely removed.
* The motor area cannot be accessed.
* The round end of the hex wrench is used or would need to be used.
* The timing pulley components or referenced gap cannot be identified from Figure 7-20.

## Escalation Guidance

* Stop and escalate if lockout/tagout cannot be completed using the referenced Operator Station Lockout/Tagout procedure.
* Stop and escalate if the side panel cannot be safely removed or the motor area cannot be accessed with the specified fasteners and tools.
* Escalate for SME review if additional timing pulley removal or installation steps are needed, because they are not present in this packet.

## Missing Details / Known Gaps

* The packet does not include the full timing pulley removal procedure.
* The packet does not include installation or reassembly steps.
* The packet does not provide an estimated time for this procedure.
* The packet does not specify whether production stop is required beyond the need for LOTO.
* The source section text is not included in the packet; final wording is grounded from the candidate and artifact retrieval text only.

## Source Lineage

- Candidate IDs: timing_pulley_replacement_access_and_removal_prep
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
