# Verify Parcel Potential Destination Data Flow During Sorter Induction (Chat messages)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_parcel_potential_destination_data_flow_during_sorter_induction_chat_messages_v1` |
| Title | Verify Parcel Potential Destination Data Flow During Sorter Induction (Chat messages) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Trace the two-step Chat messaging sequence used during sorter induction to confirm how OptiSweep receives parcel data (tracking ID, dimensions, package type; then barcode data, dimensional data, and potential destination data). Confirm that “potential destination” represents a sortable/sorted destination set (not a ZIP code) and that default dimensions are assigned when the first message fails for an unknown inducted parcel.

## When To Use

Use when you need to explain or troubleshoot the parcel induction messaging lifecycle—specifically whether OptiSweep is receiving the first and second Chat messages and whether “potential destination” is being interpreted as a sortable destination set (not a ZIP code).

## Access Or Tools Needed

* Access to the “Chat” messaging/data surfaces referenced by the source (exact live tool/screen not specified in the packet).

## Related Operational Context

* ctx_training_video_parcel_lifecycle_messages_v1
* ctx_training_video_default_dimensions_unknown_inducted_v1
* ctx_training_video_potential_destination_concept_v1
* ctx_training_video_zip_to_destination_mapping_v1

## Procedure Steps

### Step 1 — Identify the sorter induction lifecycle and the two Chat messages

**Responsible role:** L1_support

**Instruction:**
On the live “Chat” messaging/data surface you use for induction, confirm you are looking for the two-step sequence tied to sorter induction: (1) first Chat message triggered before parcels reach the system, and (2) second Chat message triggered after the first message (including the fallback behavior).

**Expected result:**
You can describe the expected two-step sequence for a parcel at sorter induction: first message includes tracking ID, dimensions, and package type; second message includes tracking ID, barcode data, dimensional data, and potential destination data.

---

### Step 2 — Confirm the first Chat message contains tracking ID, dimensions, and package type

**Responsible role:** L1_support

**Instruction:**
For the parcel you are investigating, check the first Chat message content on the live “Chat” messaging/data surface and confirm it includes: tracking ID, dimensions, and package type.

**Expected result:**
The first Chat message for the parcel includes tracking ID, dimensions, and package type.

**Stop or Escalate If:**

* Escalate if the first Chat message is missing or does not include the fields described in the source (tracking ID, dimensions, package type).

---

### Step 3 — If the first message fails for an unknown inducted parcel, confirm OptiSweep assigns default dimensions

**Responsible role:** L1_support

**Instruction:**
If you observe a failure of the first Chat message and the parcel is inducted as “unknown,” verify that OptiSweep assigns default dimensions for that parcel.

**Expected result:**
When the first message fails for an unknown inducted parcel, OptiSweep assigns default dimensions.

**Stop or Escalate If:**

* Escalate if default dimensions are not applied when the first message fails and an unknown parcel is inducted.

---

### Step 4 — Confirm the second Chat message contains tracking ID, barcode data, dimensional data, and potential destination data

**Responsible role:** L1_support

**Instruction:**
For the same parcel, check the second Chat message content on the live “Chat” messaging/data surface and confirm it includes: tracking ID, barcode data, dimensional data, and potential destination data.

**Expected result:**
The second Chat message includes tracking ID, barcode data, dimensional data, and potential destination data.

**Stop or Escalate If:**

* Escalate if the second Chat message (with potential destination data) is missing or does not include the fields described in the source.

---

### Step 5 — Interpret “potential destination” as a sortable destination set (not a ZIP code)

**Responsible role:** L1_support

**Instruction:**
When explaining or validating the parcel’s “potential destination” data, confirm you treat it as a sorted/sortable destination set (multiple destinations may be provided), not as a ZIP code.

**Expected result:**
Potential destination is understood and communicated as a sorted destination set (sortable destination options), not a ZIP code.

---

### Step 6 — If needed, explain upstream ZIP-to-destination mapping vs local destination knowledge

**Responsible role:** L1_support

**Instruction:**
If you need to explain the relationship between ZIP codes and potential destination, use the source-backed mapping concept: UPS internally maps a ZIP code to one or multiple destinations via an upstream mapping file/system (ASX), while the local system “only knows destinations.”

**Expected result:**
You can explain that ZIP-to-destination mapping is upstream (ASX mapping file) and that the local system uses destination values rather than ZIP code logic.

---

## Success Criteria

* For the investigated parcel, the first Chat message is present and contains tracking ID, dimensions, and package type.
* If the first message fails for an unknown inducted parcel, default dimensions are assigned by OptiSweep.
* The second Chat message is present and contains tracking ID, barcode data, dimensional data, and potential destination data.
* Potential destination is interpreted as a sorted/sortable destination set (not a ZIP code).

## Failure Conditions

* First Chat message is missing or lacks tracking ID, dimensions, or package type.
* Default dimensions are not assigned when the first message fails for an unknown inducted parcel.
* Second Chat message is missing or lacks tracking ID, barcode data, dimensional data, or potential destination data.
* Potential destination is misinterpreted as a ZIP code.

## Escalation Guidance

* Escalate if the second Chat message (with potential destination data) is missing or does not include the fields described in the source.
* Escalate if default dimensions are not applied when the first message fails and an unknown parcel is inducted.

## Missing Details / Known Gaps

* The packet does not specify the exact live tool/screen where “Chat” messages are viewed, so step instructions reference the live “Chat” messaging/data surface without naming a specific UI/API endpoint.

## Source Lineage

- Candidate IDs: candidate_training_video_parcel_potential_destination_message_lifecycle
- Source ID: `training_video_day1`
- Source Type: `training_video`
