# Verify the AVEVA request-to-response tag flow via OPC-generated tags (Tag app / real-time tags)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_aveva_request_to_response_tag_flow_opc_v1` |
| Title | Verify the AVEVA request-to-response tag flow via OPC-generated tags (Tag app / real-time tags) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `apidog`, `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_smeme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Tag app to verify that an AVEVA-bound request is issued via an OPC tag, produces a response, and results in tags being created/updated that AVEVA can read. Confirm the mapping context that metrics are converted into AVEVA-readable tags in SYS1.

## When To Use

When you need to confirm the end-to-end AVEVA request/response/tag-creation flow that is driven by an OPC tag, and you want to validate the real-time tags visible in the Tag app and the SYS1 metrics-to-tags mapping context.

## Access Or Tools Needed

* Tag app (for checking real-time tags)
* Ability to locate the OPC tag entry point used for the request
* Visibility into SYS1 tag namespace/entries where metrics are converted into tags for AVEVA to read

## Related Operational Context

* ctx_training_video_aveva_api_tag_mapping_v1
* ctx_training_video_tag_app_realtime_tags_v1
* ctx_training_video_sys1_metrics_to_tags_v1

## Visual References

![artifact_training_video_training_video_day2_0038_this_is_how_veva_is_mapped_primary_03_01_43_000](assets/dafe63fee038fcc7.jpg)

*Frame showing the AVEVA request/response/tag-creation mapping via OPC tags and the SYS1 metrics-to-tags conversion context; also states real-time tags are checked through the tag app (not a Perspective project).*

## Procedure Steps

### Step 1 — Open the Tag app used for checking real-time tags

**Responsible role:** L2_support

**Instruction:**
Open the Tag app that is used to check real-time tags (the source states the tags are checked through the tag app, not a Perspective project).

**Expected result:**
The Tag app real-time tags view is open and ready to observe tag creation/updates.

---

### Step 2 — Locate the OPC tag entry point used to issue the request

**Responsible role:** L2_support

**Instruction:**
In the relevant OPC tag area, locate the OPC tag that is used as the request trigger (the source describes the request as “a tag in OPC” and then “they hit request”).

**Expected result:**
You have identified the OPC tag entry point that will be used to trigger the request.

---

### Step 3 — Trigger/issue the request associated with the OPC tag

**Responsible role:** L2_support

**Instruction:**
Trigger the “request” action/control associated with the identified OPC tag (the source states “they hit request”).

**Expected result:**
The request has been issued from the OPC tag request trigger.

---

### Step 4 — Observe that a response is generated

**Responsible role:** L2_support

**Instruction:**
After issuing the request, observe whether the system generates a response (the source states “it gets a response”).

**Expected result:**
A response is observed after the request is issued.

**Stop or Escalate If:**

* No response is observed after the request (stop and escalate for deeper API/OPC/tag-provider troubleshooting).

---

### Step 5 — Verify AVEVA-readable tags are created/updated in the Tag app real-time tags

**Responsible role:** L2_support

**Instruction:**
In the Tag app real-time tags view, check that tags are created/updated after the response, specifically the tags that AVEVA can read (the source states “tags are created that AVEVA can read”).

**Expected result:**
After the request/response, the Tag app shows newly created or updated tags that AVEVA can read.

**Stop or Escalate If:**

* If the expected AVEVA-readable tags are not created/updated in the tag app, stop and escalate for deeper API/OPC/tag-provider troubleshooting.

---

### Step 6 — Confirm SYS1 is the metrics-to-tags conversion location for AVEVA reads

**Responsible role:** L2_support

**Instruction:**
Confirm the SYS1 mapping context in the tag namespace/entries shown in the source: SYS1 is where all metrics are converted into tags for AVEVA to read.

**Expected result:**
SYS1 is identified as the location where metrics are converted into tags for AVEVA to read.

---

## Success Criteria

* After issuing the request via the OPC tag, a response is observed.
* After the response, the Tag app real-time tags show newly created/updated tags that AVEVA can read.
* SYS1 is confirmed as the metrics-to-tags conversion location for AVEVA reads.

## Failure Conditions

* No response is observed after the request.
* Expected AVEVA-readable tags are not created/updated in the Tag app real-time tags view.
* SYS1 metrics-to-tags conversion context cannot be confirmed.

## Escalation Guidance

* If no response is observed after the request, or if AVEVA-readable tags are not created/updated in the Tag app, stop and escalate for deeper API/OPC/tag-provider troubleshooting.

## Missing Details / Known Gaps

* The source does not name specific Tag app UI controls/buttons for issuing the request or for selecting the exact real-time tag namespace/filters to observe.
* The source does not provide the exact OPC tag name/path or the exact request control label used to trigger the request.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_veva_opc_request_tag_flow
- Source ID: `training_video_day2`
- Source Type: `training_video`
