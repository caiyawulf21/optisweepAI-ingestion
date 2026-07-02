# Recover an AGV That Lost a Tote Without an AGV Fault

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1` |
| Title | Recover an AGV That Lost a Tote Without an AGV Fault |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Restore the AGV and the missing tote to the system after an AGV loses a tote without the AGV itself faulting. The source sequence stops RMS, manually releases and moves the AGV to the Hospital, removes and re-adds the AGV at the Hospital station PC, power-cycles the AGV, repositions it at the Inbound Hospital Station QR code after its lights turn green, then removes and re-adds the missing tote.

## When To Use

Use when the AGV LOST TOTE NO FAULT recovery scenario applies and the AGV has lost a tote without the AGV itself faulting, using the recovery sequence documented in section 5.8.2.6.

## Do Not Use For

* Do not use for AGV fault scenarios not identified as "AGV LOST TOTE NO FAULT".
* Do not use if the referenced Add/Remove AGV, Remove Tote, or Add Tote procedures cannot be completed.

## Safety And Operational Notes

* This procedure is not marked support-safe in the candidate.
* The recovery includes E-stop use, brake release, manual AGV movement, and AGV/tote removal and re-addition actions.
* Only maintenance or a supervisor should remove an AGV from the system, per the Add/Remove AGV screen reference.

## Access Or Tools Needed

* Access to the RMS E-stop
* Physical access to the AGV that lost the tote
* Access to the AGV brake release
* Access to the Hospital area
* Hospital station PC
* Documented Add/Remove AGV procedure on page 52
* Documented Remove Tote procedure on page 47
* Documented Add Tote procedure on page 46
* Access to the Inbound Hospital Station QR code

## Related Operational Context

* ctx_manual_acb_api_screen_reference_v1
* ctx_manual_agv_green_lights_status_v1
* ctx_manual_agv_lost_tote_no_fault_recovery_v1
* ctx_manual_hospital_station_pc_agv_management_v1
* ctx_manual_inbound_hospital_station_qr_reference_v1
* ctx_manual_tote_api_controls_overview_v1

## Procedure Steps

### Step 1 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
E-stop the RMS.

**Expected result:**
RMS is E-stopped for recovery.

**Stop or Escalate If:**

* RMS cannot be E-stopped.
* The system state does not allow the documented recovery to proceed after E-stop.

---

### Step 2 — Release the AGV brake

**Responsible role:** L2_support

**Instruction:**
Press the brake release on the AGV that lost a tote.

**Expected result:**
The AGV brake is released so the AGV can be rolled manually.

**Stop or Escalate If:**

* The AGV cannot be moved with the brake release.

---

### Step 3 — Move the AGV to the Hospital

**Responsible role:** L2_support

**Instruction:**
Push the AGV over to the Hospital.

**Expected result:**
The AGV is physically moved to the Hospital area.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station area and tote handling location that may help identify the Hospital destination for the moved AGV.*


**Stop or Escalate If:**

* The AGV cannot be physically moved to the Hospital.

---

### Step 4 — Remove and re-add the AGV at the Hospital station PC

**Responsible role:** L2_support

**Instruction:**
At the Hospital station PC, remove the AGV, then add the AGV back into the system. Use the documented Add/Remove AGV procedure reference on page 52.

**Expected result:**
The AGV is removed and then added back into the system at the Hospital station PC.

**Screens / Images:**

![artifact_fig_4_37_hospital_hmi_add_remove_agv_screen](assets/artifact_fig_4_37_hospital_hmi_add_remove_agv_screen.png)

*Hospital HMI Add/Remove AGV screen used to remove an AGV from the system and insert it back into the system.*

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*AGV API controls reference showing Remove AGV and Recover AGV controls in the system context.*


**Stop or Escalate If:**

* The AGV cannot be removed at the Hospital station PC.
* The AGV cannot be added back into the system.
* The documented Add/Remove AGV procedure cannot be completed.

---

### Step 5 — Power-cycle the AGV

**Responsible role:** L2_support

**Instruction:**
Turn the AGV off, then turn it on again.

**Expected result:**
The AGV has been power-cycled.

**Stop or Escalate If:**

* The AGV does not power back on.
* The AGV does not proceed toward the documented green-light status.

---

### Step 6 — Wait for green lights and position the AGV at the Inbound Hospital Station QR code

**Responsible role:** L2_support

**Instruction:**
Wait until the AGV lights turn green, then roll the AGV over the QR code in front of the Inbound Hospital Station.

**Expected result:**
The AGV lights turn green and the AGV is rolled over the QR code in front of the Inbound Hospital Station.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station area that may help orient the Inbound Hospital Station location.*

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*Related hospital/add-tote context artifact that may help identify the station area used after AGV repositioning.*


**Stop or Escalate If:**

* The AGV lights do not turn green.
* The AGV cannot be rolled over the QR code in front of the Inbound Hospital Station.

---

### Step 7 — Remove the missing tote from the system at the Hospital

**Responsible role:** L2_support

**Instruction:**
Locate the missing tote and bring it to the Hospital to remove it from the system using the documented Remove Tote procedure reference on page 47.

**Expected result:**
The missing tote is located, brought to the Hospital, and removed from the system.

**Screens / Images:**

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/artifact_fig_4_32_hospital_hmi_remove_tote_screen.png)

*Hospital HMI Remove Tote screen used to scan the tote barcode and confirm removal from the system.*

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station tote handling area where the tote is brought for removal.*


**Stop or Escalate If:**

* The missing tote cannot be located.
* The tote cannot be brought to the Hospital.
* The documented Remove Tote procedure cannot be completed.

---

### Step 8 — Add the tote back into the system

**Responsible role:** L2_support

**Instruction:**
Add the tote back into the system using the documented Add Tote procedure reference on page 46.

**Expected result:**
The tote is added back into the system.

**Screens / Images:**

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*Hospital HMI Add Tote screen used to scan the tote barcode and confirm execution.*

![artifact_page_93_image_2](assets/artifact_page_93_image_2.png)

*Add Tote flow showing tote barcode scan, tote ID verification, and Confirm & Execute.*


**Stop or Escalate If:**

* The documented Add Tote procedure cannot be completed.
* The tote cannot be added back into the system.

---

## Success Criteria

* The AGV is restored to the system.
* The missing tote is removed and re-added in the system.
* The AGV should then take the tote back to the sorter.

## Failure Conditions

* The AGV lights do not turn green after power cycling.
* The AGV cannot be moved with the brake release.
* The AGV cannot be re-added at the Hospital station PC.
* The documented Add/Remove AGV procedure cannot be completed.
* The documented Remove Tote procedure cannot be completed.
* The documented Add Tote procedure cannot be completed.

## Escalation Guidance

* Stop and escalate if the AGV lights do not turn green; the source does not provide further escalation steps for this condition.
* Stop and escalate if the AGV cannot be moved with the brake release or cannot be re-added at the Hospital station PC; the source does not provide further escalation steps for these conditions.
* Stop and escalate if the documented Add/Remove AGV, Remove Tote, or Add Tote referenced procedures cannot be completed.

## Missing Details / Known Gaps

* The source does not provide estimated completion time.
* The source does not state whether production stop is required beyond the instruction to E-stop RMS.
* The source does not state whether LOTO is required.
* The source does not provide detailed escalation steps if the AGV lights do not turn green.
* The source does not provide detailed escalation steps if the AGV cannot be moved with the brake release.
* The source does not provide detailed escalation steps if the AGV cannot be re-added at the Hospital station PC.
* The source does not provide a direct image explicitly identifying the QR code location in front of the Inbound Hospital Station.
* The source does not provide a direct image explicitly showing the AGV being moved to the Hospital for this exact recovery sequence.

## Source Lineage

- Candidate IDs: candidate_l2_recover_agv_lost_tote_no_fault_via_hospital_and_tote_reentry
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
