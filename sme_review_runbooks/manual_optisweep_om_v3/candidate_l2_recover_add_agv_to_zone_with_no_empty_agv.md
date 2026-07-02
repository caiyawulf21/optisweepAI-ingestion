# Add an AGV to a Zone When No Empty AGV Is Available

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_add_an_agv_to_a_zone_when_no_empty_agv_is_available_v1` |
| Title | Add an AGV to a Zone When No Empty AGV Is Available |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Restore operation by stopping RMS, moving an AGV into the zone under the tote rack, adding the AGV in RMS using the referenced Tote API Controls, confirming the AGV turns blue, verifying the HMI state is "szonestaging," and then resuming RMS using the documented system start procedure.

## When To Use

Use this recovery procedure when an AGV must be added to a zone and no empty AGV is available, as documented in manual section 5.8.2.2.

## Do Not Use For

* Do not use this procedure to accept an AGV state other than "szonestaging" as the recovery verification state.
* Do not use this procedure as a substitute for the separate documented system start procedure; the source explicitly refers the user to "Starting the System" for RMS resumption.

## Safety And Operational Notes

* This procedure includes E-stop use.
* This procedure includes physically moving an AGV into the zone under the tote rack.
* Do not resume RMS until the AGV has turned blue and the HMI status is verified as "szonestaging."

## Access Or Tools Needed

* RMS access
* Tote API Controls
* HMI access to AGV state/status
* Ability to view AGV color/status indication
* Physical access to move an AGV into the zone under the tote rack

## Related Operational Context

* ctx_manual_agv_status_screen_v1
* ctx_manual_agv_szonestaging_status_v1
* ctx_manual_agv_green_lights_status_v1

## Procedure Steps

### Step 1 — E-stop RMS

**Responsible role:** L2_support

**Instruction:**
E-stop RMS.

**Expected result:**
RMS is E-stopped and the recovery can proceed.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Use the figure associated with this recovery procedure for context on the no-empty-AGV recovery.*


**Stop or Escalate If:**

* Stop if RMS cannot be placed into the E-stopped condition required by the source procedure.

---

### Step 2 — Move an AGV into the zone under the tote rack

**Responsible role:** L2_support

**Instruction:**
Move an AGV into the zone under the tote rack.

**Expected result:**
An AGV is physically positioned in the target zone under the tote rack.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Reference the Add AGV to Zone with No Empty AGV screen and associated zone context for this recovery.*


**Stop or Escalate If:**

* Stop if the AGV cannot be moved into the zone under the tote rack.

---

### Step 3 — Add the AGV in RMS

**Responsible role:** L2_support

**Instruction:**
Add the AGV in RMS. See "Tote API Controls" on page 26.

**Expected result:**
The AGV is added in RMS.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Use the recovery figure associated with adding an AGV to a zone when no empty AGV is available.*


**Stop or Escalate If:**

* Stop if the AGV cannot be added in RMS using the documented controls.

---

### Step 4 — Wait for the AGV to turn blue

**Responsible role:** L2_support

**Instruction:**
Wait for the AGV to turn blue.

**Expected result:**
The AGV turns blue.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Use the procedure figure for the no-empty-AGV recovery while confirming the AGV reaches the documented visual state.*


**Stop or Escalate If:**

* Stop if the AGV does not turn blue.

---

### Step 5 — Verify AGV status is szonestaging on the HMI

**Responsible role:** L2_support

**Instruction:**
Verify AGV status is "szonestaging." Reference AGV state on HMI.

**Expected result:**
The HMI shows the AGV status/state as "szonestaging."

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Use the screen associated with this recovery procedure while verifying the AGV state.*


**Stop or Escalate If:**

* Stop if the AGV does not show the documented "szonestaging" state.
* Do not assume another AGV state is acceptable.

---

### Step 6 — Re-add the AGV if it is moving to the Hospital

**Responsible role:** L2_support

**Instruction:**
If the AGV is moving to the Hospital, remove the AGV and add it again.

**Expected result:**
The AGV is removed and re-added when the Hospital movement condition occurs.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Use the recovery figure associated with this procedure while checking for Hospital movement behavior.*


**Stop or Escalate If:**

* Stop if the AGV is moving to the Hospital and cannot be removed and added again as instructed.

---

### Step 7 — Press the E-stop again

**Responsible role:** L2_support

**Instruction:**
Press the E-stop again.

**Expected result:**
The documented second E-stop action is completed.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Use the procedure figure for context on the final recovery sequence.*


**Stop or Escalate If:**

* Stop if the documented second E-stop action cannot be completed.

---

### Step 8 — Resume RMS using the documented system start procedure

**Responsible role:** L2_support

**Instruction:**
Resume RMS. See "Starting the System" on page 65.

**Expected result:**
RMS is resumed after the AGV has been verified in the required state.

**Screens / Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*Reference the AGV system shut-down/start-up context associated with the documented resume/start procedure.*

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Use the no-empty-AGV recovery figure for the immediate procedure context before resuming RMS.*


**Stop or Escalate If:**

* Stop if the AGV has not been verified as blue and in "szonestaging" before resuming RMS.
* Stop if RMS cannot be resumed using the documented start procedure.

---

## Success Criteria

* The AGV is added to the zone.
* The AGV turns blue.
* The HMI shows the AGV status/state as "szonestaging."
* RMS is resumed using the documented system start procedure.

## Failure Conditions

* RMS cannot be E-stopped.
* The AGV cannot be moved into the zone under the tote rack.
* The AGV cannot be added in RMS.
* The AGV does not turn blue.
* The AGV does not show the documented "szonestaging" state on the HMI.
* The AGV moves to the Hospital and the remove/re-add action does not correct the condition.
* RMS cannot be resumed using the documented start procedure.

## Escalation Guidance

* Escalate if the AGV does not show the documented "szonestaging" state; do not assume another state is acceptable.
* If the AGV is moving to the Hospital, remove the AGV and add it again as instructed by the source.
* Escalate for review if E-stop use, physical AGV movement, or RMS resumption cannot be completed as documented.

## Missing Details / Known Gaps

* The packet does not provide the exact E-stop device/location or interface details.
* The packet does not provide the exact Tote API Controls screen sequence for adding the AGV.
* The packet does not provide the exact HMI navigation path used to verify "szonestaging" within this specific procedure excerpt.
* The packet does not state whether production stop or LOTO is formally required beyond the documented E-stop actions.
* The packet does not provide a time estimate for completing the procedure.

## Source Lineage

- Candidate IDs: candidate_l2_recover_add_agv_to_zone_with_no_empty_agv
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
