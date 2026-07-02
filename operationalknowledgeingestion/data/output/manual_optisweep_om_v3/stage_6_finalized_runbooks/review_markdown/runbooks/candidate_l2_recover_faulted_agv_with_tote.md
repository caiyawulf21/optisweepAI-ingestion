# Recover a Faulted AGV With Tote

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_a_faulted_agv_with_tote_v1` |
| Title | Recover a Faulted AGV With Tote |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Restore RMS operation after an AGV faults while carrying a tote by E-stopping RMS, removing the AGV from RMS through AGV API Controls, taking the tote to the Hospital, removing the AGV through the Hospital HMI or Hospital station PC, adding the AGV back into RMS, and resuming RMS using the documented start/resume procedure.

## When To Use

Use when an AGV has faulted while still carrying a tote and the documented recovery sequence on page 91 applies.

## Do Not Use For

* Do not use for AGV bump fault recovery covered by the separate bump fault procedure.
* Do not use for no-empty-AGV zone recovery covered by the separate add-AGV-to-zone procedure.
* Do not use when a different documented RMS start or AGV recovery scenario applies.

## Safety And Operational Notes

* This procedure is not marked support-safe in the candidate.
* The procedure begins with E-stop RMS before AGV recovery actions.
* Only maintenance or a supervisor should remove an AGV from the system, according to the Hospital HMI Add/Remove AGV screen reference.

## Access Or Tools Needed

* Access to RMS E-stop control
* Access to AGV API Controls
* Access to the Hospital area
* Access to the Hospital HMI
* Access to the documented RMS start/resume procedure

## Related Operational Context

* ctx_manual_faulted_agv_with_tote_screen_v1
* ctx_manual_hospital_hmi_agv_management_v1
* ctx_manual_agv_api_controls_reference_v1
* ctx_manual_rms_estop_resume_reference_v1

## Procedure Steps

### Step 1 — E-stop RMS

**Responsible role:** L2_support

**Instruction:**
E-stop RMS.

**Expected result:**
RMS is E-stopped and recovery actions can proceed.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Faulted AGV with tote recovery context.*

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*System stopped or shut-down mode context related to start/resume references.*


**Stop or Escalate If:**

* RMS cannot be E-stopped.
* The system does not enter the expected stopped state for recovery.

---

### Step 2 — Remove the AGV from RMS using AGV API Controls

**Responsible role:** L2_support

**Instruction:**
Remove the AGV from RMS using the AGV API Controls.

**Expected result:**
The faulted AGV is removed from RMS.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls screen showing Remove AGV and Recover AGV controls.*

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Faulted AGV with tote scenario being recovered.*


**Stop or Escalate If:**

* AGV removal through AGV API Controls cannot be completed.

---

### Step 3 — Take the tote to the Hospital and remove the AGV via the Hospital HMI

**Responsible role:** L2_support

**Instruction:**
Take the tote to the Hospital and remove the AGV via the Hospital HMI.

**Expected result:**
The tote is taken to the Hospital and the AGV is removed through the Hospital HMI or Hospital station PC.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Screen showing a faulted AGV with a tote during the fault recovery procedure.*

![artifact_fig_4_37_hospital_hmi_add_remove_agv_screen](assets/artifact_fig_4_37_hospital_hmi_add_remove_agv_screen.png)

*Hospital HMI Add/Remove AGV screen used to remove an AGV from the system.*

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station tote handling context.*


**Stop or Escalate If:**

* The AGV cannot be removed via the Hospital HMI as referenced by the source.

---

### Step 4 — Add the AGV back into RMS using AGV API Controls

**Responsible role:** L2_support

**Instruction:**
Add the AGV back into RMS using the AGV API Controls.

**Expected result:**
The AGV is added back into RMS.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API Controls screen showing Recover AGV for adding an AGV back into the system.*


**Stop or Escalate If:**

* AGV addition through AGV API Controls cannot be completed.

---

### Step 5 — Press the E-Stop again

**Responsible role:** L2_support

**Instruction:**
Press the E-Stop again.

**Expected result:**
The documented second E-stop action is completed.

**Stop or Escalate If:**

* The E-stop cannot be actuated again as required by the documented sequence.

---

### Step 6 — Resume RMS using the documented system start or resume procedure

**Responsible role:** L2_support

**Instruction:**
Resume RMS using the documented system start/resume procedure.

**Expected result:**
RMS is resumed using the documented start/resume procedure.

**Screens / Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/artifact_fig_5_4_faulted_agv_with_tote_screen.jpeg)

*Faulted AGV with Tote recovery context for the resume step.*

![artifact_fig_5_1_system_in_shut_down_mode](assets/artifact_fig_5_1_system_in_shut_down_mode.jpeg)

*System state context associated with the Starting the System reference.*


**Stop or Escalate If:**

* RMS cannot be resumed using the documented start/resume procedure.

---

## Success Criteria

* The faulted AGV is removed from RMS.
* The tote is taken to the Hospital.
* The AGV is removed through the Hospital HMI or Hospital station PC.
* The AGV is added back into RMS.
* RMS is resumed using the documented start/resume procedure.

## Failure Conditions

* AGV removal through AGV API Controls cannot be completed.
* The AGV cannot be removed via the Hospital HMI.
* The AGV cannot be added back into RMS.
* RMS cannot be resumed using the documented start/resume procedure.

## Escalation Guidance

* Escalate if AGV removal or addition through AGV API Controls cannot be completed.
* Escalate if the AGV cannot be removed via the Hospital HMI as referenced by the source.
* Escalate if RMS cannot be resumed using the documented start/resume procedure.
* Escalate when role authorization is unclear, because the Hospital HMI reference states only maintenance or a supervisor should remove an AGV from the system.

## Missing Details / Known Gaps

* The source does not provide detailed validation checks after AGV removal, Hospital removal, AGV re-addition, or RMS resume.
* The source does not provide exact button names or field-by-field instructions for the page 91 recovery sequence beyond referenced interfaces.
* The source does not provide an estimated completion time.
* The source does not provide alternate recovery paths if the documented sequence fails.
* The source does not explicitly define whether LOTO is required.

## Source Lineage

- Candidate IDs: candidate_l2_recover_faulted_agv_with_tote
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
