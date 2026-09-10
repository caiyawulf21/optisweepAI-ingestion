# Use the Hospital as a Reject Station to Address Unsorted Totes (Tipper issue handling)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_hospital_as_reject_station_v1` |
| Title | Use the Hospital as a Reject Station to Address Unsorted Totes (Tipper issue handling) |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tipper_station_fault`, `lane_or_chute_state` |
| Access Surface | `physical_floor`, `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

If a tipper problem prevents packages/totes from being sorted, route the affected totes to the Hospital (reject station) so an operator can address them and get the associated packages back onto the system for further processing.

## When To Use

Use when the system indicates a tipper issue and packages/totes “didn’t get sorted,” and the workflow directs the affected totes to the Hospital as a reject station for operator handling so packages can return to the system.

## Access Or Tools Needed

* Hospital/reject station physical access
* Operator ability to address totes at the Hospital station (as described in the segment)

## Related Operational Context

* ctx_training_video_hospital_reject_station_v1

## Procedure Steps

### Step 1 — Identify the tipper-related unsorted condition

**Responsible role:** operator

**Instruction:**
Use the scenario described in the segment: when “something’s wrong with Tipper” and the package “didn’t get sorted,” treat the affected totes/packages as needing Hospital reject-station handling.

**Expected result:**
You have identified that the current packages/totes were not sorted due to a tipper issue (the segment ties this directly to the Hospital reject-station workflow).

---

### Step 2 — Route the affected totes/packages to the Hospital reject station

**Responsible role:** operator

**Instruction:**
Follow the segment’s workflow that sends the affected totes to the Hospital: “ADV sent to hospital.” Bring the affected totes to the Hospital reject station so the operator can address them.

**Expected result:**
The affected totes/packages are at the Hospital reject station location for operator handling.

---

### Step 3 — Address the totes at the Hospital reject station

**Responsible role:** operator

**Instruction:**
At the Hospital reject station, perform the operator handling described in the segment: “takes the tote goes there and operate there something like that.”

**Expected result:**
The operator has addressed the totes at the Hospital reject station as part of the reject-station handling workflow.

**Stop or Escalate If:**

* If totes/packages cannot be addressed at the Hospital reject station as described, escalate for support (no additional troubleshooting steps are provided in the source beyond the reject-station concept).

---

### Step 4 — Verify packages are returned to the system for further processing

**Responsible role:** operator

**Instruction:**
Confirm the intended outcome described in the segment: the packages “have to make it on the system somewhere” and the Hospital handling ensures packages “get back.”

**Expected result:**
Packages associated with the addressed totes are returned “back” to the system for further processing.

**Stop or Escalate If:**

* If packages/totes do not return to the system after Hospital handling, escalate for support (source does not provide specific troubleshooting steps beyond the reject-station concept).

---

## Success Criteria

* Totes/packages that did not get sorted due to a tipper issue are handled at the Hospital reject station by the operator.
* Associated packages are returned “back” to the system for further processing.

## Failure Conditions

* Totes/packages cannot be addressed at the Hospital reject station as described.
* Packages do not return to the system after Hospital handling.

## Escalation Guidance

* If totes/packages cannot be addressed at the Hospital reject station as described, escalate for support. The source does not provide specific troubleshooting steps beyond the reject-station concept.

## Missing Details / Known Gaps

* The source does not name specific Hospital HMI screens/buttons or a step-by-step operator action sequence beyond the concept: “takes the tote goes there and operate there something like that.”
* The source does not provide observable system indicators (e.g., specific RMS/WCS/Helix DB fields or statuses) to confirm that packages returned to the system after Hospital handling.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_hospital_reject_station_operator_address_totes
- Source ID: `training_video_day1`
- Source Type: `training_video`
