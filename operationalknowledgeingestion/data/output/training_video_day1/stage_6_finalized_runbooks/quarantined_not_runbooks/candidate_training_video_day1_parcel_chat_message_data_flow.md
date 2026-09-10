# Verify OptiSweep parcel data message flow from Chat (tracking ID, dimensions, package type) into sorter induction

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_optsweep_parcel_chat_message_flow_into_sorter_induction_v1` |
| Title | Verify OptiSweep parcel data message flow from Chat (tracking ID, dimensions, package type) into sorter induction |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this lightweight diagnostic to confirm the source-described parcel messaging sequence: parcels move from trailer-unloading belts to sorter induction, then Chat sends a first message containing tracking ID, dimensions, and package type; if that first message fails for an unknown inducted parcel, OptiSweep assigns default dimensions; then a second Chat message provides tracking ID, barcode data, dimensional data, and potential destination data. When the parcel is on the sorter, dimensional data and destination indication should be present.

## When To Use

Use when you need to interpret whether the parcel’s data association into sorter induction matches the source-described Chat message flow (first message fields, default-dimensions behavior on failure, then second message fields) and to map what data should exist when a parcel is on the sorter.

## Do Not Use For

* Do not use this procedure as a substitute for deeper database/message-flow troubleshooting beyond the source-described Chat message field expectations.

## Access Or Tools Needed

* Access to the system surface that shows Chat messages and their payload fields (tracking ID, dimensions, package type; then barcode data, dimensional data, potential destination data) as referenced by the source
* Training video frame evidence for the described fields (artifact_training_video_training_video_day1_0011_so_before_a_parcel_reaches_our_primary_00_17_45_500)

## Related Operational Context

* ctx_training_video_parcel_lifecycle_overview_v1
* ctx_training_video_first_chat_message_reference_v1
* ctx_training_video_unknown_inducted_default_dimensions_v1
* ctx_training_video_second_chat_message_reference_v1

## Procedure Steps

### Step 1 — Identify the parcel lifecycle stage described by the source (belts leading to sorter induction)

**Responsible role:** L1_support

**Instruction:**
Confirm you are working with the parcel stage where parcels are unloaded from trailers in bulk onto a series of belts that lead to sorter inductions (the stage that triggers the first Chat message).

**Expected result:**
You can associate the current parcel situation to the source-described stage: parcels are on belts leading to sorter induction (i.e., the stage that triggers Chat messaging).

---

### Step 2 — Confirm the first Chat message fields (tracking ID, dimensions, package type)

**Responsible role:** L1_support

**Instruction:**
Check the Chat message payload for the first message triggered by the pre-sort induction stage and confirm it includes: tracking ID, dimensions, and package type.

**Expected result:**
The first Chat message includes tracking ID, dimensions, and package type for the parcel.

---

### Step 3 — If the first Chat message fails, confirm unknown inducted parcels use OptiSweep default dimensions

**Responsible role:** L1_support

**Instruction:**
If the first Chat message fails and the parcel is treated as unknown inducted, confirm that OptiSweep assigns default dimensions to that parcel.

**Expected result:**
For an unknown inducted parcel with a failed first message, the parcel is associated with default dimensions by OptiSweep.

**Stop or Escalate If:**

* If you observe a first-message failure but the parcel is not associated to default dimensions for an unknown inducted parcel, treat it as a messaging/data-association issue and escalate for deeper investigation.

---

### Step 4 — Confirm the second Chat message fields (tracking ID, barcode data, dimensional data, potential destination data)

**Responsible role:** L1_support

**Instruction:**
Check the Chat message payload for the second message triggered after the first-message stage and confirm it includes: tracking ID, barcode data, dimensional data, and potential destination data.

**Expected result:**
The second Chat message includes tracking ID + barcode data + dimensional data + potential destination data.

**Stop or Escalate If:**

* If observed parcel data does not match the source-described fields for the first or second Chat messages, treat it as a messaging/data-association issue and escalate for deeper investigation.

---

### Step 5 — At sorter induction: verify dimensional data and destination indication are present

**Responsible role:** L1_support

**Instruction:**
When the parcel is on the sorter, verify that dimensional data exists and there is an indication of where it could be going (destination indication).

**Expected result:**
For a parcel on the sorter, dimensional data is present and destination indication is present.

**Stop or Escalate If:**

* If on-sorter dimensional data and destination indication are not present as expected, treat it as a messaging/data-association issue and escalate for deeper investigation.

---

## Success Criteria

* First Chat message payload includes tracking ID, dimensions, and package type.
* If the first Chat message fails for an unknown inducted parcel, OptiSweep assigns default dimensions.
* Second Chat message payload includes tracking ID, barcode data, dimensional data, and potential destination data.
* When the parcel is on the sorter, dimensional data and destination indication are present.

## Failure Conditions

* First Chat message missing required fields or fails.
* Unknown inducted parcels do not show default dimensions when the first message fails.
* Second Chat message missing required fields (tracking ID, barcode data, dimensional data, potential destination data).
* On-sorter parcel state lacks dimensional data and/or destination indication.

## Escalation Guidance

* If observed parcel data does not match the source-described fields for the first or second Chat messages, treat it as a messaging/data-association issue and escalate for deeper investigation.

## Missing Details / Known Gaps

* The packet does not name the exact live system surface (UI/API/module) where Chat messages are viewed; the procedure therefore keeps the access step generic to 'Chat message visibility' as referenced by the source.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_parcel_chat_message_data_flow
- Source ID: `training_video_day1`
- Source Type: `training_video`
