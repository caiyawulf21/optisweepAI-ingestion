# Acknowledge hospital HMI fault and retry tote operation

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_acknowledge_hospital_hmi_fault_and_retry_hospital_tote_v1` |
| Title | Acknowledge hospital HMI fault and retry tote operation |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Source-specific incident recovery for a hospital-area HMI fault at UPS Haslet TX (TXRTH). The incident evidence supports opening the hospital HMI where the fault is shown, not unplugging the HMI, using the acknowledge control, retrying the operation, confirming the tote at the hospital is tote ID 28, and verifying the area is back to normal.

## When To Use

Use when the hospital-area HMI is showing a fault and the source-supported recovery path is to acknowledge the fault on the HMI, retry the operation, confirm the tote identity at the hospital area, and verify the issue is cleared.

## Do Not Use For

* Do not use this procedure as guidance to unplug the HMI.
* Do not use this procedure for faults that do not clear after acknowledge and retry, because the incident does not provide additional safe recovery steps.
* Do not use this procedure to perform undocumented HMI changes, configuration changes, or other unsupported recovery actions.

## Safety And Operational Notes

* Do not unplug the HMI when this fault is shown; the incident explicitly advised against unplugging it.
* Do not perform undocumented changes beyond acknowledge, retry, tote ID confirmation, and status verification supported by the incident evidence.

## Access Or Tools Needed

* Access to the hospital-area HMI
* Ability to view the tote ID at the hospital area
* Support communication channel if the retry does not clear the fault

## Procedure Steps

### Step 1 — Open the hospital-area HMI showing the fault

**Responsible role:** operator

**Instruction:**
Go to the hospital area and open or view the HMI that is currently showing the fault condition.

**Expected result:**
The operator is viewing the hospital-area HMI where the fault is displayed.

**Stop or Escalate If:**

* The HMI cannot be accessed or the reported fault cannot be confirmed on the hospital-area screen.

---

### Step 2 — Do not unplug the HMI; use acknowledge

**Responsible role:** operator

**Instruction:**
Do not unplug the HMI. Use the on-screen acknowledge control for the displayed fault.

**Expected result:**
The operator avoids unplugging the HMI and selects the acknowledge option on the fault screen.

**Stop or Escalate If:**

* The HMI does not present an acknowledge option.
* The only apparent next action would be unplugging the HMI.
* The operator cannot safely proceed using the on-screen acknowledge control.

---

### Step 3 — Acknowledge the fault and retry the operation

**Responsible role:** operator

**Instruction:**
Hit acknowledge on the HMI and try the operation again from the HMI or associated tote flow.

**Expected result:**
The fault is cleared or the operation is retried successfully after acknowledge.

**Stop or Escalate If:**

* The fault does not clear after acknowledge and retry.
* The same fault immediately returns after retry.
* The operation cannot be retried from the HMI or associated tote flow.

---

### Step 4 — Confirm the tote ID at the hospital area

**Responsible role:** operator

**Instruction:**
Check the tote at the hospital area and confirm whether it is tote ID 28.

**Expected result:**
The tote at the hospital area is positively identified.

**Stop or Escalate If:**

* The tote ID cannot be confirmed.
* The tote at the hospital is not tote ID 28.
* The tote identity is ambiguous after retry.

---

### Step 5 — Confirm recovery status is all good

**Responsible role:** operator

**Instruction:**
Confirm that the issue is cleared and the hospital area is back to normal before ending the procedure.

**Expected result:**
The operator confirms the area is 'all good' after the retry.

**Stop or Escalate If:**

* The operator cannot confirm the area is all good.
* Any fault indication remains on the HMI after retry.
* Normal tote operation is not restored.

---

## Success Criteria

* The hospital-area HMI fault is acknowledged without unplugging the HMI.
* The operation can be retried after acknowledge.
* The tote at the hospital area is confirmed as tote ID 28.
* The operator confirms the area is 'all good' after retry.

## Failure Conditions

* The fault does not clear after acknowledge and retry.
* The HMI cannot be safely recovered using the on-screen acknowledge control.
* The tote ID at the hospital cannot be confirmed as part of validation.
* The operator cannot confirm the area is back to normal.

## Escalation Guidance

* If the fault does not clear after acknowledge and retry, stop and escalate; the incident does not provide further safe recovery steps.
* Escalate if the acknowledge option is unavailable or the HMI cannot be used without unplugging it.
* Escalate if tote ID validation at the hospital area cannot be completed.

## Missing Details / Known Gaps

* The incident does not provide the exact HMI acknowledge button label beyond 'acknowledge'.
* The incident does not provide a detailed retry sequence beyond 'try again'.
* No artifact IDs were supplied for attaching HMI screenshots as structured image references.
* The incident does not identify role boundaries beyond an operator-facing recovery sequence.
* The incident does not provide estimated completion time, production stop requirements, or LOTO requirements.

## Source Lineage

- Candidate IDs: candidate_incident_218550_acknowledge_hmi_fault_and_retry_hospital_tote
- Source ID: `source_case_218550`
- Source Type: `incident_case`
