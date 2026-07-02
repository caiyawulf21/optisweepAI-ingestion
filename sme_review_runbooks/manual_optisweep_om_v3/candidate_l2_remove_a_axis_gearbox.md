# Remove the A-Axis Gearbox

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_the_a_axis_gearbox_v1` |
| Title | Remove the A-Axis Gearbox |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Remove the A-axis gearbox from the carriage using the documented mechanical removal procedure. The source-backed procedure includes lockout/tagout, PPE and tool preparation, side panel removal for access, gripper removal, management of counter-balance drift, optional motor removal for access using a referenced procedure, removal of the gearbox mounting screws, and gearbox removal.

## When To Use

Use when the A-axis gearbox must be removed from the carriage as part of documented maintenance, replacement, or recovery work on the OptiSweep system.

## Do Not Use For

* Do not use for operator execution; the candidate identifies this procedure as not support-safe.
* Do not improvise motor removal; if motor removal is needed for access, use the referenced Motor Removal procedure on page 106.
* Do not use this runbook as a substitute for the referenced Operator Station Lockout/Tagout or gripper removal procedures.

## Safety And Operational Notes

* Perform the referenced Operator Station Lockout/Tagout procedure before beginning work.
* Wear safety glasses and gloves.
* Most fasteners in the A-axis gearbox have Loctite 277, so removal may be difficult.
* After gripper removal, the system is out of balance and the counter-balance may drift down to the lower hard stop.
* This is not a support-safe operator procedure because it includes LOTO and mechanical disassembly with out-of-balance counter-balance behavior.

## Access Or Tools Needed

* LOTO access
* Safety glasses
* Gloves
* Torque wrench
* 4-mm hex wrench
* 3/8-in. wrench or socket
* Standard screwdriver
* Access to the station side panel, motor area, gripper, counter-balance area, and gearbox mounting location
* Referenced procedures: Operator Station Lockout/Tagout, gripper removal, and motor removal
* Replacement part: Gearbox

## Procedure Steps

### Step 1 — Lock out and tag out the system

**Responsible role:** L2_support

**Instruction:**
LOTO the system using the referenced "Operator Station Lockout/Tagout" procedure on page 2.

**Expected result:**
The system is in the documented lockout/tagout state and safe for maintenance access.

**Stop or Escalate If:**

* The referenced LOTO procedure cannot be completed.
* Safe maintenance isolation cannot be confirmed.

---

### Step 2 — Put on PPE and gather tools and replacement gearbox

**Responsible role:** L2_support

**Instruction:**
Put on safety glasses and gloves, and gather the listed tools and replacement part: torque wrench, 4-mm hex wrench, 3/8-in. wrench or socket, standard screwdriver, and gearbox.

**Expected result:**
Required PPE is worn and all listed tools and the gearbox are available at the work area.

**Stop or Escalate If:**

* Required PPE is unavailable.
* Any listed tool or the gearbox is unavailable.

---

### Step 3 — Remove the station side panel

**Responsible role:** L2_support

**Instruction:**
Use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel, then remove the station side panel to access the motor.

**Expected result:**
The station side panel is removed and the motor access area is exposed.

**Screens / Images:**

![artifact_fig_7_6_gearbox](assets/artifact_fig_7_6_gearbox.png)

*A-axis gearbox area, side panel access area, and adjacent motor location.*


**Stop or Escalate If:**

* The nine self-tapping fasteners cannot be removed.
* The side panel cannot be removed without damage or access remains blocked.

---

### Step 4 — Remove the gripper

**Responsible role:** L2_support

**Instruction:**
Remove the gripper using the referenced "Removal" procedure on page 97.

**Expected result:**
The gripper has been removed per the referenced procedure.

**Stop or Escalate If:**

* The gripper cannot be removed using the referenced procedure.
* The referenced gripper removal procedure is unavailable.

---

### Step 5 — Manage counter-balance drift after gripper removal

**Responsible role:** L2_support

**Instruction:**
With the gripper removed, account for the system being out of balance and the counter-balance wanting to drift down; allow it to drift to the lower hard stop, or optionally remove the counter-balance weight to help balance the system.

**Expected result:**
The out-of-balance condition is acknowledged and the counter-balance is allowed to settle to the lower hard stop or is balanced by removing the counter-balance weight.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Counterbalance carriage or counterbalance components referenced by the source.*


**Stop or Escalate If:**

* The counter-balance behavior cannot be controlled.
* The out-of-balance condition creates unsafe movement.
* Counter-balance weight removal is needed but the referenced context is insufficient to proceed safely.

---

### Step 6 — Remove the motor only if needed for access

**Responsible role:** L2_support

**Instruction:**
Remove the gearbox without removing the motor, but remove the motor if needed for fastener access using the referenced "Motor Removal" procedure on page 106.

**Expected result:**
The gearbox remains accessible for removal, with the motor left in place unless documented motor removal is required for access.

**Screens / Images:**

![artifact_fig_7_6_gearbox](assets/artifact_fig_7_6_gearbox.png)

*Gearbox and adjacent motor location to judge whether motor removal is needed for fastener access.*


**Stop or Escalate If:**

* Fastener access is blocked and the referenced motor removal procedure is unavailable.
* Motor removal would require improvisation.

---

### Step 7 — Remove the gearbox mounting screws

**Responsible role:** L2_support

**Instruction:**
Remove the eight M5x18 socket-head screws mounting the gearbox to the carriage.

**Expected result:**
All eight gearbox mounting screws are removed from the carriage.

**Screens / Images:**

![artifact_fig_7_6_gearbox](assets/artifact_fig_7_6_gearbox.png)

*Gearbox mounting location and the eight M5x18 screws.*


**Stop or Escalate If:**

* The mounting screws cannot be removed.
* Fastener removal is unusually difficult due to Loctite 277.

---

### Step 8 — Remove the gearbox

**Responsible role:** L2_support

**Instruction:**
Remove the gearbox.

**Expected result:**
The A-axis gearbox is removed from the carriage.

**Screens / Images:**

![artifact_fig_7_6_gearbox](assets/artifact_fig_7_6_gearbox.png)

*A-axis gearbox identification and removal location.*


**Stop or Escalate If:**

* The gearbox does not separate after the documented mounting screws are removed.
* Additional undocumented disassembly appears necessary.

---

## Success Criteria

* The A-axis gearbox is removed from the carriage.
* The documented mounting fasteners and required access components have been removed as required.
* Referenced prerequisite procedures were used where the source directs them.

## Failure Conditions

* LOTO is not completed before work begins.
* Required PPE, tools, or replacement gearbox are unavailable.
* The side panel or gearbox fasteners cannot be removed.
* Counter-balance drift creates an uncontrolled or unsafe condition.
* Motor removal is attempted without using the referenced procedure.
* The gearbox cannot be removed after documented steps are completed.

## Escalation Guidance

* Escalate if the referenced LOTO, gripper removal, or motor removal procedures are unavailable or cannot be completed.
* Escalate if counter-balance movement cannot be controlled safely.
* Escalate if fastener removal is blocked or unusually difficult due to Loctite 277.
* Escalate if the gearbox cannot be removed without additional undocumented disassembly.

## Missing Details / Known Gaps

* The packet does not provide the full OCR text of section 7.3.6.1, so step wording is finalized from the candidate and artifact summaries rather than direct section quotes.
* No estimated task duration is provided in the packet for this procedure.
* The packet does not provide explicit production stop guidance.
* The packet references external procedures for LOTO, gripper removal, and motor removal but does not include their full contents.
* No explicit torque values, reinstallation details, or post-removal handling instructions are provided for this removal-only runbook.

## Source Lineage

- Candidate IDs: candidate_l2_remove_a_axis_gearbox
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
