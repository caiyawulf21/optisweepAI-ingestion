# Map OptiSweep software data flow: OptiSweep → Ignition (OPC server) → AVEVA (HMI) and tippers via OPC

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_map_optisweep_data_flow_opc_ignition_aveva_v1` |
| Title | Map OptiSweep software data flow: OptiSweep → Ignition (OPC server) → AVEVA (HMI) and tippers via OPC |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep software stack mapping to identify where OPC-based communication originates (Ignition as the OPC server) and where data is consumed (AVEVA as the HMI). The source also states that Ignition communicates through the tippers via OPC and feeds data to AVEVA via direct OPC integration.

## When To Use

When you need to explain or reason about which layer is responsible for OPC-based communication and AVEVA data visibility, using the source-described responsibilities: Ignition as the OPC server (including OPC communication through the tippers) and AVEVA as the HMI consuming data via direct OPC integration.

## Do Not Use For

* Do not use this procedure as a live system troubleshooting guide for RMS/SSMS/WCS database state, because the packet does not provide live UI/DB/API check steps or commands for those systems.

## Access Or Tools Needed

* Ability to reference the source-described software stack mapping (OptiSweep, AVEVA - HMI, Ignition - OPC Server, and the tippers via OPC) during troubleshooting discussions

## Related Operational Context

* ctx_training_video_optisweep_software_overview_v1
* ctx_training_video_ignition_opc_server_reference_v1
* ctx_training_video_aveva_hmi_reference_v1

## Procedure Steps

### Step 1 — Review the OptiSweep software stack mapping (OptiSweep, Ignition - OPC Server, AVEVA - HMI)

**Responsible role:** L1_support

**Instruction:**
Use the source-described stack mapping: OptiSweep integrates the system; Ignition is the OPC server; AVEVA is the HMI. When discussing the mapping, reference the labeled components shown in the source frame.

**Expected result:**
You can state (based on the source mapping) that Ignition is the OPC server and AVEVA is the HMI in the OptiSweep software stack.

---

### Step 2 — Confirm the OPC communication path: Ignition communicates through the tippers via OPC

**Responsible role:** L1_support

**Instruction:**
Use the source-described responsibility that Ignition communicates through the tippers through OPC.

**Expected result:**
You can state that Ignition is the component that communicates through the tippers via OPC.

---

### Step 3 — Confirm the data consumption path: Ignition feeds data to AVEVA via direct OPC integration

**Responsible role:** L1_support

**Instruction:**
Use the source-described responsibility that Ignition feeds data to AVEVA because AVEVA can directly integrate with the OPC server.

**Expected result:**
You can state that Ignition feeds data to AVEVA and that AVEVA integrates directly with the OPC server.

**Stop or Escalate If:**

* If live system evidence contradicts the source mapping (e.g., AVEVA is not integrating with the OPC server as described), stop and escalate for deeper system-specific investigation.

---

### Step 4 — Use the mapping to guide troubleshooting attribution for AVEVA data visibility issues (Ignition vs AVEVA layer)

**Responsible role:** L1_support

**Instruction:**
When AVEVA data visibility is reported, use the source-described responsibilities to state whether the issue is more likely in the OPC server layer (Ignition) versus the HMI consumption layer (AVEVA): Ignition is responsible for OPC communication (including through the tippers) and feeding data to AVEVA; AVEVA is the HMI that integrates directly with the OPC server.

**Expected result:**
You can articulate a source-backed attribution: OPC delivery/communication issues are more likely in Ignition (OPC server), while HMI consumption/integration issues are more likely in AVEVA.

**Stop or Escalate If:**

* If live system evidence contradicts the source mapping, stop and escalate for deeper system-specific investigation.

---

## Success Criteria

* You can correctly identify Ignition as the OPC server and AVEVA as the HMI consumer per the source mapping.
* You can correctly explain that Ignition communicates through the tippers via OPC and feeds data to AVEVA via direct OPC integration.
* For an AVEVA data visibility issue, you can provide a source-grounded attribution of likely layer (Ignition vs AVEVA) without contradicting the source responsibilities.

## Failure Conditions

* Attribution contradicts the source mapping (e.g., claiming AVEVA is the OPC server or that AVEVA does not integrate with the OPC server).
* Live evidence contradicts the source mapping; escalation is required.

## Escalation Guidance

* If live system evidence contradicts the source mapping (e.g., AVEVA is not integrating with the OPC server as described), stop and escalate for deeper system-specific investigation.

## Missing Details / Known Gaps

* The packet does not provide live AVEVA UI checks, Ignition OPC server status checks, or any commands/queries to validate OPC connectivity or data points on the running system.
* The packet does not specify which exact AVEVA screens/tags correspond to which OPC items, so the runbook cannot map a specific missing AVEVA display to a specific OPC server component beyond the layer attribution.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_software_map_optisweep_ignition_opc_aveva
- Source ID: `training_video_day1`
- Source Type: `training_video`
