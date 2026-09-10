# Use the Hospital Tags Model to map hospital controller tags to PLC communication (TagTypeParent in/out)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_hospital_tags_model_map_hospital_controller_tags_to_plc_v1` |
| Title | Use the Hospital Tags Model to map hospital controller tags to PLC communication (TagTypeParent in/out) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness`, `opc_connection_or_tipper_heartbeat`, `gateway_health` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `opc_connection_faulted`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify that the Hospital Tags Model is configured to process hospital controller data via a subscribed list of tags, and that TagTypeParent classifies tags as in vs out to determine which tags the system acts on for PLC communication (including Todd’s tippers and the hospital/display).

## When To Use

Use when you need to confirm how hospital controller data is represented as subscribed tags and how TagTypeParent (in/out) drives which tags are read/written for PLC communication (hospital and tipper PLC communication).

## Access Or Tools Needed

* Access to the configured hospital tags model (where the hospital tag list and TagTypeParent are defined)
* A way to view hospital tag configuration (database/config UI not specified in source)

## Related Operational Context

* ctx_training_video_hospital_tags_model_v1
* ctx_training_video_tag_type_parent_in_out_v1

## Visual References

![artifact_training_video_training_video_day2_0022_wait_do_we_need_to_stay_primary_01_54_40_000](assets/4b2d26c738220b4e.jpg)

*Frame showing: Hospital tags model processes hospital controller data via subscribed tags; TagTypeParent indicates in vs out; tags are used to communicate with the PLC (Todd’s tippers, hospital, and display).*

## Procedure Steps

### Step 1 — Identify the configured Hospital Tags Model used for hospital controller tag processing

**Responsible role:** L2_support

**Instruction:**
Open the configured Hospital Tags Model in the live environment (the model that processes data from the hospital controller via a subscribed list of tags).

**Expected result:**
You can point to the configured Hospital Tags Model that is described as processing hospital controller data using a list of tags that are subscribed to and actioned on.

**Stop or Escalate If:**

* Stop if the source evidence is insufficient to locate the actual configured tag list in the live system; request access to the relevant database/configuration view.

---

### Step 2 — Locate the subscribed hospital tag list that is actioned based on TagTypeParent

**Responsible role:** L2_support

**Instruction:**
In the Hospital Tags Model configuration, locate the list of hospital tags that are subscribed to and actioned on based on TagTypeParent.

**Expected result:**
The configuration shows a list of hospital tags that are subscribed to and that the system uses for PLC communication.

**Stop or Escalate If:**

* Stop if the source evidence is insufficient to locate the actual configured tag list in the live system; request access to the relevant database/configuration view.

---

### Step 3 — Confirm TagTypeParent is used to classify tags as in vs out

**Responsible role:** L2_support

**Instruction:**
In the Hospital Tags Model configuration, verify that TagTypeParent is present and explicitly indicates whether each tag is an in or out tag.

**Expected result:**
TagTypeParent is configured such that it classifies tags as in vs out.

**Stop or Escalate If:**

* If TagTypeParent is not being used as described (in/out classification), escalate to deeper configuration review by L2/L3 support.

---

### Step 4 — Confirm hospital tags are used for PLC communication via read/write actions

**Responsible role:** L2_support

**Instruction:**
Using the Hospital Tags Model configuration, confirm that the in/out-tag classification drives read/write actions to PLC-related tags used for Todd’s tippers and the hospital/display communication.

**Expected result:**
The configured hospital tags are described/linked to PLC communication actions (read/write) and include Todd’s tippers and the hospital/display.

**Stop or Escalate If:**

* If TagTypeParent is not being used as described (in/out classification), or the expected hospital tags list is missing/incorrect, escalate to deeper configuration review by L2/L3 support.

---

### Step 5 — If troubleshooting, record which tags should be in vs out based on TagTypeParent and expected hospital vs tipper communication

**Responsible role:** L2_support

**Instruction:**
When troubleshooting, use the Hospital Tags Model configuration to record the expected in/out tag sets based on TagTypeParent, and map them to the hospital controller vs tipper PLC communication described by the model (Todd’s tippers and the hospital/display).

**Expected result:**
You have a recorded expectation of which tags should be in vs out and which tags correspond to hospital controller vs tipper PLC communication.

**Stop or Escalate If:**

* If TagTypeParent is not being used as described (in/out classification), or the expected hospital tags list is missing/incorrect, escalate to deeper configuration review by L2/L3 support.

---

## Success Criteria

* Hospital Tags Model configuration is located and shows a subscribed list of hospital tags.
* TagTypeParent is present and classifies tags as in vs out.
* The configured hospital tags are used for PLC communication actions, including Todd’s tippers and the hospital/display.

## Failure Conditions

* TagTypeParent is missing, not populated, or does not classify tags as in vs out.
* Subscribed hospital tags list is missing/incorrect or cannot be located in the live configuration.
* Hospital tags model is not linked to PLC communication actions (read/write) for hospital/display and tipper tags.

## Escalation Guidance

* Escalate to deeper configuration review by L2/L3 support if TagTypeParent is not being used as described (in/out classification), or if the expected hospital tags list is missing/incorrect.

## Missing Details / Known Gaps

* The source does not name the exact live UI/DB tables/fields to inspect for the configured Hospital Tags Model and TagTypeParent values.
* The source does not specify the exact live configuration view/tool (e.g., SSMS table names, Helix DB model names, or a specific configuration UI path) to locate the subscribed hospital tag list.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_hospital_tags_model_map_tags_to_plc
- Source ID: `training_video_day2`
- Source Type: `training_video`
