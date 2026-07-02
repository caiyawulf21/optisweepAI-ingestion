# Install A-Axis Sensor And Connect Wiring To PCA

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_a_axis_sensor_and_connect_to_pca_v1` |
| Title | Install A-Axis Sensor And Connect Wiring To PCA |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Mount the A-axis sensor on the rear side, route the A-axis wire around the gearbox, connect the wire to the PCA, and then restart the operator station using the referenced startup procedure.

## When To Use

Use this procedure when installing the A-axis sensor and connecting its wiring to the PCA as documented in the OptiSweep Operation and Maintenance Manual section 7.3.2.1.2 Installation.

## Do Not Use For

* Do not use this runbook for Z-axis sensor wiring or CLINK connections.
* Do not use this runbook when the operator station restart procedure on page 66 is unavailable.

## Safety And Operational Notes

* This procedure is not marked support-safe in the candidate.
* Do not proceed if the rear wire routing hole, gearbox routing path, or PCA connection point cannot be positively identified from the available source material.

## Access Or Tools Needed

* Physical access to the sensor mounting location
* Access to the rear-side wire routing hole
* Access to the gearbox area and PCA
* M3 button-head screw
* Figure 7-3: A-Axis PCA Connections
* Referenced procedure: Starting The Operator Station

## Procedure Steps

### Step 1 — Mount the A-axis sensor at the rear wire routing hole

**Responsible role:** L2_support

**Instruction:**
Feed the sensor through the wire routing hole on the rear side and fasten it in place using the M3 button-head screw.

**Expected result:**
The A-axis sensor is installed at the rear-side mounting location and secured with the M3 button-head screw.

**Screens / Images:**

![artifact_fig_7_3_a_axis_pca_connections](assets/artifact_fig_7_3_a_axis_pca_connections.jpeg)

*Use the A-axis PCA connections figure as the packet-supported visual reference associated with this installation section.*


**Stop or Escalate If:**

* The installer cannot identify the rear wire routing hole from the available source material.
* The installer cannot identify the sensor mounting location from the available source material.

---

### Step 2 — Route the A-axis wire around the gearbox

**Responsible role:** L2_support

**Instruction:**
Route the A-axis wire around the gearbox.

**Expected result:**
The A-axis wire follows the documented routing path around the gearbox.

**Screens / Images:**

![artifact_fig_7_3_a_axis_pca_connections](assets/artifact_fig_7_3_a_axis_pca_connections.jpeg)

*Look for the A-axis wire routing path around the gearbox shown in Figure 7-3.*


**Stop or Escalate If:**

* The installer cannot identify the gearbox routing path from the available source material.

---

### Step 3 — Plug the A-axis wire into the PCA

**Responsible role:** L2_support

**Instruction:**
Plug the A-axis wire into the PCA.

**Expected result:**
The A-axis wire is connected to the PCA at the documented connection point.

**Screens / Images:**

![artifact_fig_7_3_a_axis_pca_connections](assets/artifact_fig_7_3_a_axis_pca_connections.jpeg)

*Look for the PCA connection point for the A-axis wire in Figure 7-3.*


**Stop or Escalate If:**

* The installer cannot identify the PCA connection point from the available source material.

---

### Step 4 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced startup procedure on page 66.

**Expected result:**
The operator station is restarted using the referenced startup procedure.

**Stop or Escalate If:**

* The referenced operator station restart procedure is not available.

---

## Success Criteria

* The A-axis sensor is mounted at the rear-side location.
* The A-axis wire is routed around the gearbox.
* The A-axis wire is plugged into the PCA.
* The operator station is restarted using the referenced startup procedure.

## Failure Conditions

* Rear wire routing hole cannot be identified from the available source material.
* Gearbox routing path cannot be identified from the available source material.
* PCA connection point cannot be identified from the available source material.
* Referenced operator station restart procedure is not available.

## Escalation Guidance

* Escalate if the installer cannot identify the rear wire routing hole, gearbox routing path, or PCA connection point from the available source material.
* Escalate if the referenced operator station restart procedure is not available.

## Missing Details / Known Gaps

* The source packet does not provide the full body text of section 7.3.2.1.2 Installation.
* The source does not provide additional connector labels or verification values for the PCA connection in this section.
* The source does not provide a time estimate for this procedure.
* The source does not state whether production stop or LOTO is required for this specific procedure.
* The restart step depends on a referenced procedure on page 66 that is not included in this packet.

## Source Lineage

- Candidate IDs: candidate_l2_install_a_axis_sensor_and_connect_to_pca
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
