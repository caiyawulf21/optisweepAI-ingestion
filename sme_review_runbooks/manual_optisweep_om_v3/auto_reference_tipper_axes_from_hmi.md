# Automatically reference all tipper axes from the HMI

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_automatically_reference_all_tipper_axes_from_the_hmi_v1` |
| Title | Automatically reference all tipper axes from the HMI |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station HMI controls to automatically reference all tipper axes, confirm completion by verifying the reference status indicators show green "R" icons, then return the system to AUTO and restart operation.

## When To Use

Use this procedure when tipper axes need to be automatically referenced from the HMI and the system must be returned to operation after referencing completes.

## Do Not Use For

* Do not use this procedure to return the system to AUTO or press CYCLE START before referencing is completed and the "R" icons have turned green.
* Do not use this procedure as a substitute for re-commissioning after any part is replaced; the surrounding maintenance note states that a tipper needs to be re-commissioned after any part is replaced.

## Safety And Operational Notes

* Do not continue to AUTO and CYCLE START until referencing is completed and the "R" icons have turned green.
* The surrounding maintenance note states that a tipper needs to be re-commissioned after any part is replaced.

## Access Or Tools Needed

* Access to the HMI or operator controls with RESET, AUTO REF, AUTO, and CYCLE START
* Ability to observe the 'R' status icons during referencing

## Procedure Steps

### Step 1 — Press RESET

**Responsible role:** L2_support

**Instruction:**
Press RESET on the HMI or operator controls.

**Expected result:**
The system accepts the reset input so the automatic referencing sequence can proceed.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI/operator controls associated with the referencing procedure context.*


**Stop or Escalate If:**

* RESET cannot be performed from the HMI/operator controls.
* The system does not allow progression to AUTO REF after RESET.

---

### Step 2 — Start automatic axis referencing

**Responsible role:** L2_support

**Instruction:**
Press AUTO REF to reference all of the axes of the tippers.

**Expected result:**
The system begins automatically referencing all tipper axes.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*HMI/operator station screen area used for axis referencing controls, including AUTO REF.*

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*Nearby startup context mentioning homing axes using AUTO REF.*


**Stop or Escalate If:**

* AUTO REF is unavailable or does not initiate referencing.
* Not all tipper axes appear to enter the referencing process.

---

### Step 3 — Verify referencing completion

**Responsible role:** L2_support

**Instruction:**
Verify that the "R" icons turn green to confirm referencing is completed.

**Expected result:**
The reference status indicators show green "R" icons, confirming referencing is complete.

**Screens / Images:**

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Axis reference status indicators on the operator station HMI; confirm the 'R' icons are green.*

![artifact_page_103_image_3](assets/artifact_page_103_image_3.png)

*Operator station HMI view associated with nearby axis referencing context; look for the reference status indicators and green 'R' icons.*


**Stop or Escalate If:**

* The "R" icons do not turn green.
* Referencing completion cannot be visually confirmed on the HMI.
* Do not continue to AUTO and CYCLE START until referencing is completed and the "R" icons have turned green.

---

### Step 4 — Return the system to AUTO

**Responsible role:** L2_support

**Instruction:**
When referencing is completed, press AUTO.

**Expected result:**
The system is returned to AUTO mode.

**Screens / Images:**

![artifact_page_86_image_13](assets/artifact_page_86_image_13.png)

*Operator station controls associated with AUTO mode selection.*

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI/operator controls used to continue from referencing completion to AUTO.*


**Stop or Escalate If:**

* Referencing has not been confirmed complete by green "R" icons.
* AUTO cannot be selected from the HMI/operator controls.

---

### Step 5 — Restart operation

**Responsible role:** L2_support

**Instruction:**
Press CYCLE START to restart operation.

**Expected result:**
Operation restarts after CYCLE START is pressed.

**Screens / Images:**

![artifact_page_86_image_13](assets/artifact_page_86_image_13.png)

*Operator station controls associated with CYCLE START.*

![artifact_page_103_image_2](assets/artifact_page_103_image_2.jpeg)

*Operator station HMI/operator controls used to restart operation after referencing.*


**Stop or Escalate If:**

* Referencing has not been confirmed complete by green "R" icons.
* AUTO mode has not been selected.
* CYCLE START does not restart operation.

---

## Success Criteria

* All tipper axes are referenced.
* The "R" icons are green.
* The system is returned to AUTO.
* Operation restarts after CYCLE START is pressed.

## Failure Conditions

* The system does not accept RESET or AUTO REF.
* The "R" icons do not turn green.
* Referencing completion cannot be confirmed.
* AUTO or CYCLE START cannot be performed successfully.
* Operation does not restart after CYCLE START is pressed.

## Escalation Guidance

* Stop and do not continue to AUTO or CYCLE START until referencing is completed and the "R" icons have turned green.
* If referencing cannot be completed or confirmed, escalate for further maintenance review.
* If any part has been replaced, follow the required re-commissioning process rather than relying only on this referencing procedure.

## Missing Details / Known Gaps

* The supplied source_sections text is empty, so step wording is grounded primarily in the candidate and artifact retrieval text.
* The packet does not provide an explicit estimated time.
* The packet does not explicitly state whether production stop or LOTO is required.
* The packet does not identify a specific HMI screen name for the automatic referencing sequence.
* No direct screenshot artifact explicitly labeled with the green 'R' icons was provided; nearby page 103 operator station artifacts were attached as best-fit visual support.

## Source Lineage

- Candidate IDs: auto_reference_tipper_axes_from_hmi
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
