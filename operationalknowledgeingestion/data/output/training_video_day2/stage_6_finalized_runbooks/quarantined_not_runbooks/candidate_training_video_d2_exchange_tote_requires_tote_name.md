# ExchangeTote: exchange a specific tote using ToteName

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_exchange_tote_exchange_a_specific_tote_using_totenname_v1` |
| Title | ExchangeTote: exchange a specific tote using ToteName |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tote_exchange_sequence` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep/WCS API function ExchangeTote with the required parameter ToteName to exchange the specific tote identified by that ToteName.

## When To Use

When you need to exchange a specific tote and the API call requires ToteName to target that exact tote.

## Access Or Tools Needed

* OptiSweep/WCS API access (as implied by the source listing of tote-related APIs) via API Dog

## Related Operational Context

* ctx_training_video_tote_api_parameter_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0031_for_totes_we_have_exchange_sorter_primary_02_44_11_000](assets/54d41adfcf4b3f8f.jpg)

*Frame listing tote-related APIs including ExchangeTote and its required parameter ToteName.*

## Procedure Steps

### Step 1 — Prepare the ToteName for the tote you want to exchange

**Responsible role:** L1_support

**Instruction:**
Identify the ToteName value corresponding to the specific tote you intend to exchange, so you can supply it as the ToteName parameter to ExchangeTote.

**Expected result:**
You have a ToteName value ready to use as the ExchangeTote request parameter.

---

### Step 2 — Call ExchangeTote with the ToteName

**Responsible role:** L1_support

**Instruction:**
Using the OptiSweep/WCS API tooling (API Dog as referenced by the source), call ExchangeTote and set the required request parameter ToteName to the value prepared in the previous step.

**Expected result:**
The ExchangeTote request is issued with ToteName as the required parameter.

---

### Step 3 — Verify the exchange targets the specific tote identified by ToteName

**Responsible role:** L1_support

**Instruction:**
After the ExchangeTote call, verify that the exchange result corresponds to the specific tote identified by the ToteName you provided (i.e., the exchange is for that specific tote).

**Expected result:**
The specified tote (by ToteName) is exchanged.

**Stop or Escalate If:**

* If the wrong tote is exchanged or no exchange occurs, verify the ToteName and escalate if still incorrect.

---

## Success Criteria

* ExchangeTote is called with ToteName as the required parameter.
* The specified tote identified by ToteName is exchanged.

## Failure Conditions

* ExchangeTote is called without ToteName.
* The wrong tote is exchanged.
* No exchange occurs for the intended tote.

## Escalation Guidance

* If the wrong tote is exchanged or no exchange occurs, verify the ToteName and escalate if still incorrect.

## Missing Details / Known Gaps

* The packet does not specify the exact API Dog request/response fields or where to view the exchange verification result in the live system.
* The packet does not provide the exact verification mechanism (e.g., which UI/model/table/API endpoint shows the exchange outcome) beyond the statement that ExchangeTote exchanges the specific tote.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_exchange_tote_requires_tote_name
- Source ID: `training_video_day2`
- Source Type: `training_video`
