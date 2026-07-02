# Direct Customer To Preferred Interfaces Instead Of Performing Removal In Geek

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_direct_customer_to_preferred_interfaces_instead_of_performing_removal_in_geek_v1` |
| Title | Direct Customer To Preferred Interfaces Instead Of Performing Removal In Geek |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When a customer needs a removal-related action, direct the customer to use AVEVA or the host/hospital interface instead of performing the removal directly in Geek. The source states that removing a box in Geek does not send all the information.

## When To Use

Use this guidance when handling a customer discussion or request involving a removal-related action and the action is being considered directly in Geek.

## Do Not Use For

* Do not use this as a procedure for performing the removal directly in Geek.
* Do not use this as a detailed operating procedure for AVEVA or the host/hospital interface, because those detailed steps are not provided in the source.
* Do not use this to explain additional system behavior beyond the source statement that removing a box in Geek does not send all the information.

## Safety And Operational Notes

* Use only the source-supported guidance: direct the customer to AVEVA or the host/hospital interface instead of performing the removal directly in Geek.
* Do not invent additional removal steps, controls, or system effects not stated in the source.

## Access Or Tools Needed

* Customer communication channel
* Knowledge of the preferred interfaces named in the source: AVEVA or host/hospital
* Awareness of whether the action is being attempted in Geek

## Related Operational Context

* ctx_training_video_operation_preferred_customer_interfaces_v1

## Procedure Steps

### Step 1 — Identify whether the removal-related action is being considered in Geek

**Responsible role:** L1_support

**Instruction:**
During the customer discussion, confirm whether the requested removal-related action is being considered directly in Geek.

**Expected result:**
It is clear whether the action is being considered in Geek.

**Screens / Images:**

![artifact_training_video_training_video_day1_0045_i_i_would_say_like_the_primary_01_37_38_000](assets/f6cb873cf13e9adf.jpg)

*The training frame and associated discussion about not removing items directly in this interface and instead directing customers to approved tools.*


**Stop or Escalate If:**

* Escalate if the required customer-facing interface is unavailable or unclear from the current situation.

---

### Step 2 — Direct the customer to the preferred interface

**Responsible role:** L1_support

**Instruction:**
Direct the customer to use AVEVA or the host/hospital interface instead of performing the removal directly in Geek.

**Expected result:**
The customer is redirected to one of the preferred interfaces named in the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0045_i_i_would_say_like_the_primary_01_37_38_000](assets/f6cb873cf13e9adf.jpg)

*The associated training discussion advising support to direct customers to AVEVA or the portal/hospital workflow rather than removing items directly in this interface.*


**Stop or Escalate If:**

* Escalate if the required customer-facing interface is unavailable or unclear from the current situation.

---

### Step 3 — Explain why Geek should not be used for this removal

**Responsible role:** L1_support

**Instruction:**
Explain that removing a box in Geek does not send all the information.

**Expected result:**
The customer receives the source-supported reason for using the preferred interface.

**Stop or Escalate If:**

* Stop and avoid further explanation if doing so would require inventing additional system behavior beyond the source statement.

---

### Step 4 — Record that the customer was directed to the preferred interface

**Responsible role:** L1_support

**Instruction:**
Record that the customer was directed to the preferred interface named in the source.

**Expected result:**
A record exists that the customer was directed to AVEVA or the host/hospital interface.

---

## Success Criteria

* The customer is directed to use AVEVA or the host/hospital interface.
* The removal-related action is not performed directly in Geek when this source guidance applies.
* The source-supported reason is communicated: removing a box in Geek does not send all the information.
* The interaction is recorded as having directed the customer to the preferred interface.

## Failure Conditions

* The action is performed directly in Geek despite the source guidance.
* The preferred interface is unavailable or unclear.
* Support adds unsupported claims about system behavior.
* The customer direction is not documented.

## Escalation Guidance

* Escalate if the required customer-facing interface is unavailable or unclear from the current situation.
* Escalate rather than inventing additional system behavior or unsupported instructions.

## Missing Details / Known Gaps

* The source does not provide detailed steps inside AVEVA.
* The source does not provide detailed steps inside the host/hospital interface.
* The source does not define the exact documentation system or record format for recording that the customer was directed to the preferred interface.
* The source does not specify whether AVEVA and host/hospital are interchangeable in all cases or how to choose between them.
* The source does not provide a time estimate.

## Source Lineage

- Candidate IDs: candidate_training_video_direct_customer_to_preferred_interfaces_for_removal_requests
- Source ID: `training_video_day1`
- Source Type: `training_video`
