# Check OPC connection status for tipper tags in Ignition Gateway (Config > OPC > OPC Connections)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_opc_connection_status_tipper_tags_ignition_gateway_v1` |
| Title | Check OPC connection status for tipper tags in Ignition Gateway (Config > OPC > OPC Connections) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | None |
| Access Surface | `ignition_gateway`, `tipper_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Ignition Gateway web view to view current OPC connection entries for tipper tags. The source example shows tipper 7 and tipper 8 entries as Faulted when the tippers are powered off.

## When To Use

When you need to confirm the current OPC connection status shown for specific tipper tags (example: tipper 7 and tipper 8) using the Ignition Gateway web view.

## Access Or Tools Needed

* Ignition Gateway web view access
* Access to the Config > OPC > OPC Connections screen

## Related Operational Context

* ctx_training_video_opc_connections_web_view_v1
* ctx_training_video_designer_vs_web_view_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0039_or_is_there_a_different_place_primary_03_02_32_000](assets/fdac78df358b2247.jpg)

*Ignition Gateway UI path showing Config > OPC > OPC Connections and example where tipper 7 and 8 show Faulted when powered off.*

## Procedure Steps

### Step 1 — Open Ignition Gateway web view and navigate to Config > OPC > OPC Connections

**Responsible role:** L1_support

**Instruction:**
In the Ignition Gateway web view, navigate to Config > OPC > OPC Connections.

**Expected result:**
The Config > OPC > OPC Connections page loads and is ready to display the current OPC connection entries.

**Stop or Escalate If:**

* If you cannot access the Config > OPC > OPC Connections page, stop and escalate for deeper investigation.

---

### Step 2 — Locate the entries for the relevant tipper tags (example: tipper 7 and tipper 8)

**Responsible role:** L1_support

**Instruction:**
On the OPC Connections view, locate the entries for the referenced tipper tags (the source example references tipper 7 and tipper 8).

**Expected result:**
You can find the OPC connection entries for the referenced tipper tags (e.g., tipper 7 and tipper 8) within the OPC Connections list.

**Stop or Escalate If:**

* If the OPC Connections page does not show the expected tipper entries, stop and escalate to support for deeper investigation.

---

### Step 3 — Check the displayed connection status for each tipper entry

**Responsible role:** L1_support

**Instruction:**
For each referenced tipper entry (example: tipper 7 and tipper 8), read the displayed connection status on the OPC Connections page.

**Expected result:**
The OPC Connections view shows a connection status such as Faulted for the referenced tipper entries when they are powered off (as in the source example for tipper 7 and tipper 8).

**Stop or Escalate If:**

* If the OPC Connections page does not show a status consistent with the source example (Faulted when powered off), stop and escalate to support for deeper investigation.

---

### Step 4 — Compare what you see in the web view to the expected status for the referenced tipper tags

**Responsible role:** L1_support

**Instruction:**
Compare the connection status you read for the referenced tipper entries in the Ignition Gateway web view to the expected status from the source example (Faulted when powered off).

**Expected result:**
Your observed status for tipper 7 and tipper 8 matches the expected condition (Faulted when powered off) from the source example.

**Stop or Escalate If:**

* If the OPC Connections page does not show the expected tipper entries or does not show a status consistent with the source example, stop and escalate to support for deeper investigation.

---

## Success Criteria

* You can access Ignition Gateway web view Config > OPC > OPC Connections.
* The OPC Connections list contains entries for the referenced tipper tags (example: tipper 7 and tipper 8).
* The displayed connection status for those entries matches the expected condition being validated (Faulted when powered off, per the source example).

## Failure Conditions

* OPC Connections page does not show the expected tipper entries.
* OPC Connections page does not show a status consistent with the expected condition being validated (per the source example).

## Escalation Guidance

* If the OPC Connections page does not show the expected tipper entries or does not show a status consistent with the source example, stop and escalate to support for deeper investigation.

## Missing Details / Known Gaps

* The source does not provide the exact Ignition Gateway URL/host for the Config > OPC > OPC Connections page (only that it is accessible via the web view).
* The source does not define the full set of possible connection status values beyond the example 'Faulted'.
* The source does not specify how to map a specific tipper tag name/ID to the corresponding row label in the OPC Connections list beyond the example of tipper 7 and tipper 8.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_ignition_opc_connections_faulted_tipper_tags
- Source ID: `training_video_day2`
- Source Type: `training_video`
