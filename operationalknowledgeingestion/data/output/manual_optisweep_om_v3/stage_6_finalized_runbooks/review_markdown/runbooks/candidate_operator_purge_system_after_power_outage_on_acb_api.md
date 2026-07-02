# Purge the System From the ACB API Screen After a Power Outage

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_purge_the_system_from_the_acb_api_screen_after_a_power_outage_v1` |
| Title | Purge the System From the ACB API Screen After a Power Outage |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the System HMI ACB API screen to purge the system after a power outage during a sort that lasts long enough for systems to lose communication. This sends AGVs with totes to operator stations so totes can be emptied, and packages must then be re-circulated to the sorter lane because bag labels will not be printed.

## When To Use

Use after a power outage in the middle of a sort when the outage is long enough for systems to lose communication.

## Do Not Use For

* Do not use when the source condition of a power outage during a sort with communication loss is not present.
* Do not use as a substitute for other recovery steps not provided by the source when the ACB API screen or SYSTEM PURGE action is unavailable.

## Safety And Operational Notes

* Use only the documented HMI recovery action from the source.
* The source does not provide additional recovery steps if the ACB API screen or SYSTEM PURGE action is unavailable.

## Access Or Tools Needed

* Access to the System HMI
* ACB API screen on the System HMI
* SYSTEM PURGE control in the System section
* Access to operator stations to empty totes

## Procedure Steps

### Step 1 — Navigate to the ACB API screen

**Responsible role:** operator

**Instruction:**
On the System HMI, navigate to the "ACB API" screen.

**Expected result:**
The ACB API screen is displayed on the System HMI.

**Screens / Images:**

![artifact_page_212_image_2](assets/artifact_page_212_image_2.jpeg)

*The System HMI ACB API screen referenced for post-power-outage recovery.*

![artifact_fig_4_9_system_api_controls](assets/artifact_fig_4_9_system_api_controls.jpeg)

*The System section of the API screen where system controls, including System Purge, are located.*


**Stop or Escalate If:**

* The ACB API screen is unavailable.
* The source provides no alternate recovery path if the ACB API screen cannot be accessed.

---

### Step 2 — Press SYSTEM PURGE in the System section

**Responsible role:** operator

**Instruction:**
In the "System" section of the ACB API screen, press "SYSTEM PURGE."

**Expected result:**
The system purge action is initiated from the System section.

**Screens / Images:**

![artifact_page_212_image_2](assets/artifact_page_212_image_2.jpeg)

*The ACB API screen used for the SYSTEM PURGE action after a power outage.*

![artifact_fig_4_9_system_api_controls](assets/artifact_fig_4_9_system_api_controls.jpeg)

*The System Purge control in the System section of the API screen.*


**Stop or Escalate If:**

* SYSTEM PURGE is not available on the screen.
* The source provides no additional recovery steps if the SYSTEM PURGE action is unavailable.

---

### Step 3 — Allow AGVs with totes to go to operator stations and empty totes

**Responsible role:** operator

**Instruction:**
Allow the AGVs with totes to go to operator stations so the totes can be emptied.

**Expected result:**
AGVs with totes arrive at operator stations and the totes are emptied.

**Stop or Escalate If:**

* AGVs with totes do not go to operator stations.
* Totes cannot be emptied.
* The source does not provide an escalation path if AGVs do not go to operator stations or totes are not emptied.

---

### Step 4 — Re-circulate packages to the sorter lane

**Responsible role:** operator

**Instruction:**
Re-circulate the packages to the sorter lane because labels will not be printed for bags.

**Expected result:**
Packages are re-circulated to the sorter lane.

**Stop or Escalate If:**

* Packages cannot be re-circulated to the sorter lane.
* The source does not provide additional recovery or escalation guidance for this condition.

---

## Success Criteria

* The ACB API screen is accessed on the System HMI.
* SYSTEM PURGE is executed from the System section.
* AGVs with totes go to operator stations.
* Totes are emptied at operator stations.
* Packages are re-circulated to the sorter lane because bag labels are not printed.

## Failure Conditions

* The ACB API screen is unavailable.
* The SYSTEM PURGE action is unavailable or cannot be executed.
* AGVs with totes do not go to operator stations.
* Totes are not emptied.
* Packages are not re-circulated to the sorter lane.
* The source provides no alternate recovery path or escalation path for these failures.

## Escalation Guidance

* If the ACB API screen or SYSTEM PURGE action is unavailable, stop and escalate because the source does not provide additional recovery steps.
* If AGVs do not go to operator stations or totes are not emptied, stop and escalate because the source does not provide an escalation path.

## Missing Details / Known Gaps

* The source does not provide estimated completion time.
* The source does not specify supporting roles.
* The source does not provide additional recovery steps if the ACB API screen or SYSTEM PURGE action is unavailable.
* The source does not provide an escalation contact or path if AGVs do not go to operator stations or totes are not emptied.
* The source does not provide explicit verification indicators on the HMI after SYSTEM PURGE is pressed.

## Source Lineage

- Candidate IDs: candidate_operator_purge_system_after_power_outage_on_acb_api
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
