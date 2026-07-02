# Gather Required Fault Information Before Entering the Grid for AGV Recovery

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_gather_required_fault_information_before_entering_the_grid_for_agv_recovery_v1` |
| Title | Gather Required Fault Information Before Entering the Grid for AGV Recovery |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Collect the source-required AGV and RMS details before going inside the grid (Dance Floor) to perform fault recovery.

## When To Use

Use before going inside the grid (also called the Dance Floor) for AGV fault recovery, to ensure the required Robot ID, RMS fault description, bin/tote status, tote ID when applicable, and under-rack empty-AGV zone status have been gathered.

## Do Not Use For

* Do not use this runbook as the physical AGV recovery procedure inside the grid.
* Do not proceed into the grid without the documented information.

## Safety And Operational Notes

* Entering the grid (Dance Floor) implies elevated operational risk per the candidate context.
* Before going inside the grid, make sure to have the required Robot ID, fault description from RMS, bin/tote status, tote ID when applicable, and under-rack empty-AGV zone status.
* Do not proceed into the grid without the documented information.

## Access Or Tools Needed

* Access to RMS
* Ability to identify the faulted AGV and Robot ID
* Access to zone and AGV status information

## Related Operational Context

* ctx_manual_fault_recovery_prereq_info_v1

## Procedure Steps

### Step 1 — Identify the Robot ID for the faulted AGV

**Responsible role:** L2_support

**Instruction:**
Identify and record the Robot ID for the faulted AGV before going inside the grid.

**Expected result:**
The Robot ID for the faulted AGV is known and recorded.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*Look for the AGV fault interface context associated with Robot ID and fault recovery information.*

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*Look for AGV details/status context that may support identifying the affected AGV.*


**Stop or Escalate If:**

* Stop if the Robot ID for the faulted AGV cannot be confirmed.
* Do not proceed into the grid without the documented information.

---

### Step 2 — Obtain the fault description from RMS

**Responsible role:** L2_support

**Instruction:**
Access RMS and obtain the fault description for the faulted AGV.

**Expected result:**
The RMS fault description for the faulted AGV is available and recorded.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*Look for the AGV fault screen context referenced for RMS fault description during fault recovery.*


**Stop or Escalate If:**

* Stop if the RMS fault description cannot be confirmed.
* Do not proceed into the grid without the documented information.

---

### Step 3 — Check whether RMS indicates the AGV is holding a bin

**Responsible role:** L2_support

**Instruction:**
Check in RMS whether the faulted AGV is indicated as holding a bin.

**Expected result:**
The bin/tote holding status of the faulted AGV is known.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*Look for fault recovery screen context related to RMS fault and tote/bin status.*


**Stop or Escalate If:**

* Stop if RMS does not clearly indicate whether the AGV is holding a bin.
* Do not proceed into the grid without the documented information.

---

### Step 4 — Record the tote ID if the AGV is holding a bin

**Responsible role:** L2_support

**Instruction:**
If RMS indicates the faulted AGV is holding a bin, record the tote ID.

**Expected result:**
The tote ID is recorded when the faulted AGV is holding a bin.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*Look for screen context related to tote ID during AGV fault recovery.*

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Look for a faulted AGV with tote context that may help interpret tote-related recovery information.*


**Stop or Escalate If:**

* Stop if the AGV is shown as holding a bin but the tote ID cannot be confirmed.
* Do not proceed into the grid without the documented information.

---

### Step 5 — Verify under-rack empty-AGV zone status when applicable

**Responsible role:** L2_support

**Instruction:**
If the faulted AGV is under a rack, verify whether that AGV is the empty AGV for that zone.

**Expected result:**
The under-rack empty-AGV zone status is confirmed when applicable.

**Screens / Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen.jpeg)

*Look for no-empty-AGV zone context relevant to determining whether the under-rack AGV is the empty AGV for that zone.*

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*Look for AGV positioning and zone context that may help interpret under-rack AGV status.*


**Stop or Escalate If:**

* Stop if the faulted AGV is under a rack and its empty-AGV zone status cannot be confirmed.
* Do not proceed into the grid without the documented information.

---

### Step 6 — Confirm all required information before entering the grid

**Responsible role:** L2_support

**Instruction:**
Confirm that you have the Robot ID, RMS fault description, bin/tote status, tote ID when applicable, and under-rack empty-AGV zone status when applicable before going inside the grid.

**Expected result:**
All source-required pre-entry information has been collected and confirmed.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*Use as a reference for AGV fault recovery context while confirming the collected information.*


**Stop or Escalate If:**

* Stop if any required information is missing or cannot be confirmed.
* Do not proceed into the grid without the documented information.
* The source does not provide further action if any required information cannot be confirmed.

---

## Success Criteria

* The Robot ID for the faulted AGV is documented.
* The RMS fault description is documented.
* The AGV bin/tote holding status is documented.
* The tote ID is documented when RMS indicates the AGV is holding a bin.
* The under-rack empty-AGV zone status is documented when applicable.
* The information is confirmed before entering the grid.

## Failure Conditions

* Robot ID cannot be confirmed.
* RMS fault description cannot be obtained.
* Bin/tote holding status cannot be determined.
* Tote ID cannot be confirmed when the AGV is holding a bin.
* Under-rack empty-AGV zone status cannot be confirmed when applicable.
* Any required information is missing before grid entry.

## Escalation Guidance

* Do not proceed into the grid without the documented information.
* If any required information cannot be confirmed, stop and seek SME review because the source does not provide further action.

## Missing Details / Known Gaps

* The source packet does not provide the exact RMS navigation path or screen sequence for locating the Robot ID and fault description.
* The source packet does not specify how to determine under-rack empty-AGV zone status beyond requiring that it be known before entry.
* The source packet does not provide further action if any required information cannot be confirmed.
* The source packet does not provide an estimated completion time.
* The source packet does not state whether production stop or LOTO is required for this information-gathering procedure.

## Source Lineage

- Candidate IDs: candidate_l2_prepare_fault_recovery_information_before_entering_grid
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
