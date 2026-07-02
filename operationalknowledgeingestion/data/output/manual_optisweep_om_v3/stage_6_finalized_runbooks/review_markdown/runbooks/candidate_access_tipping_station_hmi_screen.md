# Access the Tipping Station HMI Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_access_the_tipping_station_hmi_screen_v1` |
| Title | Access the Tipping Station HMI Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Navigate through the system HMI by pressing SMALLS, selecting ACB, selecting ACB1 - AMT TT, and pressing the tipper button to open the Tipping Station screen for viewing bag completion counts, errors, and task timing information.

## When To Use

Use this procedure when an operator needs to open the Tipping Station HMI screen for the ACB1 - AMT TT tipper view to review completed bags, errors, and task duration information.

## Safety And Operational Notes

* Use only the documented HMI navigation path from the manual.
* Stop if the documented menu options or button are not present as described in the source.

## Access Or Tools Needed

* Access to the system HMI
* Ability to press SMALLS and use the drop-down menu
* Tipping Station screen navigation path from the manual

## Related Operational Context

* ctx_manual_tipping_station_screen_overview_v1

## Procedure Steps

### Step 1 — Press SMALLS

**Responsible role:** operator

**Instruction:**
On the system HMI, press SMALLS.

**Expected result:**
The SMALLS navigation view opens and allows further selection of ACB options.

**Screens / Images:**

![artifact_fig_4_4_smalls_system_overview_screen](assets/artifact_fig_4_4_smalls_system_overview_screen.jpeg)

*The SMALLS overview screen and the SMALLS entry point used to begin navigation.*

![artifact_fig_4_7_tipping_station_screen](assets/artifact_fig_4_7_tipping_station_screen.jpeg)

*Reference destination screen for the Tipping Station view that this navigation path is intended to reach.*


**Stop or Escalate If:**

* Stop if the documented menu options or button are not present as described in the source.
* Escalate if the user cannot reach the Tipping Station screen using the documented navigation path.

---

### Step 2 — Select ACB from the drop-down menu

**Responsible role:** operator

**Instruction:**
From the drop-down menu, select "ACB".

**Expected result:**
The HMI is set to the ACB selection context.

**Screens / Images:**

![artifact_page_31_image_2](assets/artifact_page_31_image_2.jpeg)

*The ACB system overview-related selection context associated with SMALLS > ACB > ACB1 - AMT TT.*


**Stop or Escalate If:**

* Stop if the documented menu options or button are not present as described in the source.
* Escalate if the user cannot reach the Tipping Station screen using the documented navigation path.

---

### Step 3 — Select ACB1 - AMT TT

**Responsible role:** operator

**Instruction:**
Select "ACB1 - AMT TT" from the available options.

**Expected result:**
The HMI is set to the ACB1 - AMT TT context.

**Screens / Images:**

![artifact_page_31_image_2](assets/artifact_page_31_image_2.jpeg)

*The ACB1 - AMT TT selection context referenced by the manual for reaching the tipper view.*


**Stop or Escalate If:**

* Stop if the documented menu options or button are not present as described in the source.
* Escalate if the user cannot reach the Tipping Station screen using the documented navigation path.

---

### Step 4 — Press the tipper button

**Responsible role:** operator

**Instruction:**
Press the tipper button on the right side of the screen.

**Expected result:**
The HMI opens the Tipping Station screen.

**Screens / Images:**

![artifact_page_31_image_2](assets/artifact_page_31_image_2.jpeg)

*The ACB/ACB1 - AMT TT navigation context before opening the tipper view.*

![artifact_fig_4_7_tipping_station_screen](assets/artifact_fig_4_7_tipping_station_screen.jpeg)

*The destination Tipping Station screen that should open after pressing the tipper button.*


**Stop or Escalate If:**

* Stop if the documented menu options or button are not present as described in the source.
* Escalate if the user cannot reach the Tipping Station screen using the documented navigation path.

---

### Step 5 — Verify the Tipping Station screen is displayed

**Responsible role:** operator

**Instruction:**
Verify that the "Tipping Station" screen is displayed.

**Expected result:**
The Tipping Station screen is visible and available for viewing.

**Screens / Images:**

![artifact_fig_4_7_tipping_station_screen](assets/artifact_fig_4_7_tipping_station_screen.jpeg)

*The Tipping Station screen layout and the information shown for completed bags, errors, and task duration.*


**Stop or Escalate If:**

* Escalate if the user cannot reach the Tipping Station screen using the documented navigation path.

---

## Success Criteria

* The Tipping Station screen opens successfully.
* The operator can view information about completed bags, errors, and task duration.

## Failure Conditions

* The documented menu options or button are not present as described in the source.
* The operator cannot reach the Tipping Station screen using the documented navigation path.
* The displayed screen does not match the expected Tipping Station screen.

## Escalation Guidance

* Stop if the documented menu options or button are not present as described in the source.
* Escalate if the user cannot reach the Tipping Station screen using the documented navigation path.

## Missing Details / Known Gaps

* The source packet does not provide an estimated completion time.
* The source packet does not state whether production must be stopped.
* The source packet does not state whether lockout/tagout is required.
* The source packet does not provide explicit role boundaries beyond operator use.
* The source packet does not provide a dedicated artifact that explicitly shows the tipper button on the right side within the ACB1 - AMT TT selection context.

## Source Lineage

- Candidate IDs: candidate_access_tipping_station_hmi_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
