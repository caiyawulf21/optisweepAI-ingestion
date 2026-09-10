# Check Tipper OPC Connection Status in Ignition Gateway

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_tipper_opc_connection_status_in_ignition_gateway_v1` |
| Title | Check Tipper OPC Connection Status in Ignition Gateway |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | `L2_support` |
| Support Safe | Yes |
| Capability Tags | `opc_connection_or_tipper_heartbeat`, `gateway_health` |
| Access Surface | `ignition_gateway`, `site_interview` |
| Audience Roles | `L1_support`, `L2_support` |
| Failure Pattern Tags | `opc_connection_faulted` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Ignition gateway Config > OPC > OPC Connections view to inspect current tipper OPC connection states and compare each displayed status with the observed or site-confirmed powered state.

## When To Use

Use this diagnostic when checking whether tipper OPC connections in the Ignition gateway currently show Connected or Faulted, especially when the displayed state needs to be compared with the live or site-confirmed powered state of the tipper.

## Do Not Use For

* Do not use this check alone to infer a broader system failure.
* Do not use this procedure as a repair, restart, or recovery procedure; the source does not provide remediation steps.

## Access Or Tools Needed

* Ignition gateway
* Ignition gateway Config > OPC > OPC Connections view
* Live or site-confirmed tipper powered state

## Related Operational Context

* ctx_training_video_ignition_opc_connections_ui_v1
* ctx_training_video_opc_connection_statuses_v1

## Procedure Steps

### Step 1 — Open the Ignition gateway OPC Connections view

**Responsible role:** L1_support

**Instruction:**
In the Ignition gateway, navigate to Config > OPC > OPC Connections.

**Expected result:**
The Ignition gateway OPC Connections page opens and displays the current connection entries with their status values.

**Stop or Escalate If:**

* The Ignition gateway OPC Connections page is unavailable or does not display current connection entries.

---

### Step 2 — Review the displayed OPC connection states

**Responsible role:** L1_support

**Instruction:**
In the Ignition gateway Config > OPC > OPC Connections list, review the displayed status for the relevant connections and distinguish Connected from Faulted.

**Expected result:**
Each relevant connection has a visible status, such as Connected or Faulted.

**Stop or Escalate If:**

* A relevant connection displays Faulted and the corresponding tipper powered state has not yet been confirmed.
* The displayed status is missing, ambiguous, or cannot be matched to the relevant tipper connection.

---

### Step 3 — Compare tipper OPC status with the powered state

**Responsible role:** L1_support

**Instruction:**
For each relevant tipper connection in the Ignition gateway Config > OPC > OPC Connections view, compare the displayed status with the live or site-confirmed powered state. In the documented example, tipper 7 and tipper 8 are powered off and display Faulted.

**Expected result:**
The displayed OPC state is recorded together with the corresponding tipper powered state, including whether a Faulted state occurs while the tipper is powered off.

**Stop or Escalate If:**

* A connection displays Faulted without the corresponding tipper being powered off.
* The displayed OPC state does not match the observed live equipment state.
* Record the affected connection and displayed status, then escalate for deeper support.

---

## Success Criteria

* The Ignition gateway Config > OPC > OPC Connections page is reached.
* The relevant tipper connection entries and their displayed Connected or Faulted states are identified.
* Each displayed state is compared with the live or site-confirmed powered state.
* Any mismatch is recorded with the affected connection and escalated rather than interpreted as a broader system failure from this check alone.

## Failure Conditions

* A relevant OPC connection displays Faulted while the corresponding tipper is powered on.
* The displayed connection state does not match the observed live equipment state.
* The Ignition gateway OPC Connections page or current connection entries are unavailable.

## Escalation Guidance

* Escalate to L2_support when a connection displays Faulted without the corresponding tipper being powered off.
* Escalate when the displayed OPC state does not match the observed live equipment state.
* Include the affected connection and displayed status in the follow-up.
* Do not infer a broader system failure from this check alone.
* The source does not provide connection repair, restart, or recovery instructions.

## Missing Details / Known Gaps

* No enriched related artifact was supplied for the requested Ignition gateway screenshot, so no visual artifact is attached.
* The source does not specify the exact Ignition gateway URL, authentication method, connection naming convention, or a repair/restart procedure.
* The source does not define the complete set of conditions represented by Connected or Faulted beyond the documented powered-off tipper example.

## Source Lineage

- Candidate IDs: candidate_training_video_ignition_opc_connection_status_check
- Source ID: `training_video_day2`
- Source Type: `training_video`
