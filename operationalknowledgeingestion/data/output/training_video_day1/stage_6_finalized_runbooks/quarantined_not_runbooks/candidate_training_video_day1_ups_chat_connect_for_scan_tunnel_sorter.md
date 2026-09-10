# Connect OptiSweep communication to UPS Chat to enable scan tunnel/tipper/sorter communication

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_connect_optsweep_communication_to_ups_chat_v1` |
| Title | Connect OptiSweep communication to UPS Chat to enable scan tunnel/tipper/sorter communication |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify that the OptiSweep system is connected to the UPS Chat communication layer (possibly previously called “chat XLE”), because OptiSweep must connect to this chat for communication with the scan tunnel and the tipper/sorter.

## When To Use

Use when scan tunnel, tote tipper/tote tip stations, or sorter interactions are not working as expected and you need to confirm the required upstream communication layer is connected: UPS Chat (chat XLE).

## Do Not Use For

* Do not use this procedure as a substitute for physical safety actions (e.g., E-stop).
* Do not use this procedure if you cannot verify any live OptiSweep communication/configuration state related to UPS Chat; the source does not provide the exact OptiSweep UI fields to check.

## Access Or Tools Needed

* OptiSweep software (live configuration/status view for the UPS Chat connection state; exact UI not provided in the source)

## Related Operational Context

* ctx_training_video_ups_chat_standard_communication_v1
* ctx_training_video_optisweep_integration_role_v1
* ctx_training_video_core_elements_architecture_v1

## Procedure Steps

### Step 1 — Identify the required building communication layer as UPS Chat (possibly “chat XLE”)

**Responsible role:** L2_support

**Instruction:**
In your live troubleshooting context, treat UPS Chat as the standard building communication layer used across UPS buildings (the source notes it may have been called “chat XLE”).

**Expected result:**
You can state the required upstream communication layer for this integration check as UPS Chat (chat XLE).

---

### Step 2 — Verify OptiSweep is configured/connected to UPS Chat as the communication path

**Responsible role:** L2_support

**Instruction:**
In OptiSweep, check the live configuration/status that indicates the system is connected to UPS Chat (chat XLE) as the communication path used by the sorters for interactions involving the scan tunnel and the tipper/sorter.

**Expected result:**
You can verify from live OptiSweep configuration/status that OptiSweep is connected to UPS Chat.

**Stop or Escalate If:**

* Stop and escalate if you cannot verify that OptiSweep is connected to UPS Chat, since the source states this connection is required for scan tunnel and tipper/sorter communication.

---

### Step 3 — Confirm the UPS Chat path is intended to support scan tunnel and tipper/sorter interactions

**Responsible role:** L2_support

**Instruction:**
Use the live system context to confirm that the UPS Chat connection you verified is the one used for communication involving the scan tunnel and the tipper/sorter (as described by the source).

**Expected result:**
Your verification ties UPS Chat connectivity to scan tunnel and tipper/sorter communication needs.

---

### Step 4 — If communication is not working, narrow scope to the chat connection layer vs downstream components

**Responsible role:** L2_support

**Instruction:**
If you determine UPS Chat connectivity is not established or cannot be verified, focus troubleshooting on the UPS Chat connection layer first, then only consider downstream components (scan tunnel, tote tip stations/tipper, sorter) after the chat connection is confirmed.

**Expected result:**
Troubleshooting focus is correctly narrowed to the UPS Chat connection layer when the required communication path is not verified.

**Stop or Escalate If:**

* Stop and escalate if you cannot verify that OptiSweep is connected to UPS Chat.

---

## Success Criteria

* Live verification shows OptiSweep is connected to UPS Chat (chat XLE), the required communication layer for scan tunnel and tipper/sorter communication.

## Failure Conditions

* You cannot verify OptiSweep is connected to UPS Chat, despite needing scan tunnel and tipper/sorter communication.

## Escalation Guidance

* Escalate if you cannot verify OptiSweep is connected to UPS Chat, since the source states this connection is required for scan tunnel and tipper/sorter communication.

## Missing Details / Known Gaps

* The source does not provide the exact OptiSweep UI screen/field names or a specific live status indicator to confirm UPS Chat connection state.
* The source does not provide explicit troubleshooting actions/controls to remediate a missing UPS Chat connection (only the requirement to connect is stated).

## Source Lineage

- Candidate IDs: candidate_training_video_day1_ups_chat_connect_for_scan_tunnel_sorter
- Source ID: `training_video_day1`
- Source Type: `training_video`
