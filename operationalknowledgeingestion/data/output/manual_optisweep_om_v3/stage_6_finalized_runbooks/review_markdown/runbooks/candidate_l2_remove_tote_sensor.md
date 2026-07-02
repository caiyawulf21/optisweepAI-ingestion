# Remove Tote Sensor

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_tote_sensor_v1` |
| Title | Remove Tote Sensor |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely remove the tote sensor from the tipper by first performing lockout/tagout using the referenced Operator Station Lockout/Tagout procedure, then disconnecting the M8 connector and M3 socket-head screw, and finally pulling the sensor out.

## When To Use

Use this procedure when the tote sensor must be removed from the tipper as documented in the source manual.

## Do Not Use For

* Do not use this procedure without first applying the referenced Operator Station Lockout/Tagout procedure.
* Do not use this procedure for tote sensor installation; this runbook only covers removal.

## Safety And Operational Notes

* Lock out/tag out the tipper before disconnecting or removing the tote sensor.
* Use safety glasses and gloves.
* Do not proceed without the referenced Operator Station Lockout/Tagout procedure.

## Access Or Tools Needed

* Access to the tipper
* Operator Station Lockout/Tagout procedure on page 2
* Replacement part: Tote sensor
* PPE: Safety glasses, gloves
* Tools needed: 1.5-mm hex wrench, 6-mm hex wrench

## Procedure Steps

### Step 1 — Lock out/tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced "Operator Station Lockout/Tagout" procedure on page 2 before performing any tote sensor removal work.

**Expected result:**
The tipper is locked out/tagged out in accordance with the referenced procedure.

**Stop or Escalate If:**

* The referenced Operator Station Lockout/Tagout procedure is unavailable.
* Lockout/tagout cannot be completed or verified.

---

### Step 2 — Disconnect the connector and retaining screw

**Responsible role:** L2_support

**Instruction:**
Disconnect the M8 connector and the M3 socket-head screw.

**Expected result:**
The tote sensor is electrically disconnected and no longer secured by the M3 socket-head screw.

**Screens / Images:**

![artifact_fig_7_9_pneumatic_valve](assets/artifact_fig_7_9_pneumatic_valve.png)

*Reference the example M8 electrical connector depiction and general tipper maintenance access context; this artifact is related but not confirmed as the tote sensor image.*


**Stop or Escalate If:**

* The M8 connector cannot be disconnected.
* The M3 socket-head screw cannot be released or removed using the documented steps.

---

### Step 3 — Remove the tote sensor

**Responsible role:** L2_support

**Instruction:**
Pull the sensor out.

**Expected result:**
The tote sensor is removed from the tipper.

**Stop or Escalate If:**

* The sensor cannot be removed after disconnecting the connector and screw.
* Removal appears to require undocumented steps or excessive force.

---

## Success Criteria

* The tipper was locked out/tagged out before maintenance began.
* The M8 connector is disconnected.
* The M3 socket-head screw is disconnected or removed as required.
* The tote sensor is fully removed from the tipper.

## Failure Conditions

* The referenced lockout/tagout procedure is unavailable or not completed.
* The M8 connector cannot be disconnected.
* The M3 socket-head screw cannot be disconnected or removed.
* The sensor cannot be removed using the documented steps.

## Escalation Guidance

* Stop and escalate if the referenced Operator Station Lockout/Tagout procedure is not available.
* Escalate if the sensor cannot be disconnected using the documented steps.
* Escalate if the sensor cannot be removed using the documented steps.

## Missing Details / Known Gaps

* The supplied source section text is empty, so the finalized runbook relies on the candidate content and packet metadata rather than direct OCR text from page 109.
* No source-supported estimated time was provided for this specific tote sensor removal procedure.
* No source-supported confirmation of whether production stop is required was provided.
* No source-supported tote sensor-specific figure or image was provided in the packet.
* The candidate notes that sensor locations are referenced on page 89, but no location details were included in this packet.

## Source Lineage

- Candidate IDs: candidate_l2_remove_tote_sensor
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
