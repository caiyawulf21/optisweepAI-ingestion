# Explain and verify the OTNet → UPS network boundary path: WCS/OptiSweep talks to UPS Chat XLE through S-Tunnel (secure channel)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_explain_verify_otnet_to_ups_chatxle_via_s_tunnel_v1` |
| Title | Explain and verify the OTNet → UPS network boundary path: WCS/OptiSweep talks to UPS Chat XLE through S-Tunnel (secure channel) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the source-described network boundary and secure channel components to determine where WCS/OptiSweep obtains UPS order/destination information across the OTNet and UPS network “islands.” The source states that OTNet is separate from the UPS network, and WCS must talk from the OT island to the UPS island by connecting to UPS Chat XLE through S-Tunnel as a secure channel.

## When To Use

When you need to explain or troubleshoot which network boundary component is responsible for missing/incorrect UPS order/destination information that WCS/OptiSweep uses to determine the next sortable destination for packages.

## Do Not Use For

* Do not use this procedure as a live connectivity test plan for RMS/SSMS/Helix DB, because the source packet provides only conceptual mapping of OTNet/UPS islands and the S-Tunnel secure channel (no live UI/API/DB verification steps are provided).

## Access Or Tools Needed

* Source evidence that names the OTNet vs UPS network boundary, WCS/OptiSweep, UPS Chat XLE, and S-Tunnel as the secure channel.

## Related Operational Context

* ctx_training_video_chatxle_stunnel_network_boundary_v1

## Procedure Steps

### Step 1 — Review the source-described network boundary: treat OTNet and the UPS network as separate “islands”

**Responsible role:** L1_support

**Instruction:**
Use the source evidence to identify that OptiSweep operates on OT net (customer OT net) separate from the UPS network, and that OT net is described as an island separate from the UPS island.

**Expected result:**
You can state the boundary model as: OTNet is separate from the UPS network, and OTNet is an island.

---

### Step 2 — Identify the cross-boundary communication target: WCS/OptiSweep must talk from the OT island to the UPS island to determine the next sortable destination

**Responsible role:** L1_support

**Instruction:**
Use the source evidence to identify that WCS needs to talk from the OT island to the UPS island to determine “what the next sortable destination is” for packages.

**Expected result:**
You can state that WCS/OptiSweep must communicate from the OT island to the UPS island to determine the next sortable destination.

---

### Step 3 — Confirm the secure channel mechanism: WCS/OptiSweep talks to UPS through S-Tunnel as a secure channel

**Responsible role:** L1_support

**Instruction:**
Use the source evidence to confirm that WCS/OptiSweep talks to UPS through S-Tunnel, described as a secure channel, to reach UPS Chat XLE.

**Expected result:**
You can state the secure channel path as: WCS/OptiSweep → S-Tunnel (secure channel/encryption from OTNet to UPS Corp) → UPS Chat XLE.

---

### Step 4 — If order/destination information is missing or incorrect, map the implicated boundary component (S-Tunnel vs UPS Chat XLE vs WCS-side destination need)

**Responsible role:** L1_support

**Instruction:**
Use the source mapping to decide whether the issue is more likely on the secure channel mechanism (S-Tunnel), the UPS communications endpoint (Chat XLE), or the WCS-side need for destination data across the OTNet/UPS islands.

**Expected result:**
You can articulate a triage hypothesis using the three named elements from the source mapping: S-Tunnel (secure channel), Chat XLE (UPS communications chat endpoint), and WCS/OptiSweep (OT island side needing destination/order info).

**Stop or Escalate If:**

* If live evidence indicates communication is not using S-Tunnel or not reaching Chat XLE as described, stop and escalate for deeper system-specific investigation.

---

## Success Criteria

* You can describe the boundary path as OTNet island → S-Tunnel secure channel → UPS Chat XLE, and that WCS/OptiSweep uses this to determine the next sortable destination.
* When destination/order information is missing or incorrect, you can name which boundary component (S-Tunnel vs Chat XLE vs WCS-side destination need) is implicated using the source mapping.

## Failure Conditions

* You cannot map destination/order information dependency to UPS Chat XLE via S-Tunnel across the OTNet/UPS islands.
* Live evidence contradicts the source-described path (not using S-Tunnel or not reaching Chat XLE), requiring escalation.

## Escalation Guidance

* Stop and escalate for deeper system-specific investigation if live evidence indicates communication is not using S-Tunnel or not reaching Chat XLE as described.

## Missing Details / Known Gaps

* No live verification steps are provided in the packet (no RMS/SSMS/Helix DB/API Dog request/response checks, no specific endpoints, and no observable fields/statuses to confirm S-Tunnel vs Chat XLE connectivity). This runbook is therefore limited to source-grounded diagnostic mapping.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_network_boundary_wcs_to_ups_chatxle_via_s_tunnel
- Source ID: `training_video_day1`
- Source Type: `training_video`
