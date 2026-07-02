# Verify An AGB Floor Location Using Node Code Or Cell Code

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_an_agb_floor_location_using_node_code_or_cell_code_v1` |
| Title | Verify An AGB Floor Location Using Node Code Or Cell Code |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the node code or cell code for an AGB location to verify the physical floor location by matching it to the physical number on the floor QR code, then confirm or communicate that location.

## When To Use

Use when you need to verify where an AGB is physically located on the floor, or when you need to direct another person to that location using the node code or cell code that matches the floor QR code number.

## Do Not Use For

* Not for moving, restarting, or otherwise controlling an AGB.
* Not for determining system navigation steps or software workflows not provided in this source.

## Safety And Operational Notes

* This source describes a location verification reference process only.
* Do not assume any control action, movement action, or system change from this procedure unless supported by another approved source.

## Access Or Tools Needed

* Access to the AGB location reference containing the node code or cell code
* Physical access or visual access to the floor QR code marker

## Related Operational Context

* ctx_training_video_node_code_cell_location_reference_v1
* ctx_training_video_floor_qr_code_location_marker_v1

## Procedure Steps

### Step 1 — Obtain the node code or cell code

**Responsible role:** operator

**Instruction:**
Obtain the node code or cell code for the AGB location from the available location reference.

**Expected result:**
A node code or cell code is available for comparison.

**Screens / Images:**

![artifact_training_video_training_video_day1_0038_so_a_few_slides_ago_when_primary_01_31_42_500](assets/14114979d2d592ae.jpg)

*Transcript-aligned explanation that node code or cell code is the location reference used to match the floor marking.*


**Stop or Escalate If:**

* Stop or escalate if the node code or cell code cannot be obtained from the available reference.

---

### Step 2 — Find the floor QR code marking

**Responsible role:** operator

**Instruction:**
Go to the floor location and find the QR code marking with its physical number.

**Expected result:**
The floor QR code marker and its physical number are visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0038_so_a_few_slides_ago_when_primary_01_31_42_500](assets/14114979d2d592ae.jpg)

*Evidence that the floor QR code has a physical number on it and is used as the physical location marker.*


**Stop or Escalate If:**

* Stop or escalate if the floor QR code marker cannot be located.
* Stop or escalate if the physical number on the floor QR code cannot be read.

---

### Step 3 — Compare the code to the floor number

**Responsible role:** operator

**Instruction:**
Compare the node code or cell code to the physical number on the floor QR code.

**Expected result:**
You determine whether the node code or cell code matches the floor QR code number.

**Screens / Images:**

![artifact_training_video_training_video_day1_0038_so_a_few_slides_ago_when_primary_01_31_42_500](assets/14114979d2d592ae.jpg)

*The relationship between node code or cell code and the physical floor QR code number.*


**Stop or Escalate If:**

* Escalate if the floor QR code number does not match the provided node code or cell code.

---

### Step 4 — Verify or communicate the AGB location

**Responsible role:** operator

**Instruction:**
Verify that the AGB is at the matching location, or communicate that location to another person using the matched code.

**Expected result:**
The AGB location is confirmed or clearly communicated using the matched node code or cell code and floor QR code number.

**Screens / Images:**

![artifact_training_video_training_video_day1_0038_so_a_few_slides_ago_when_primary_01_31_42_500](assets/14114979d2d592ae.jpg)

*Transcript-aligned evidence that the matched code can be used to verify where the AGB is or direct someone to that location.*


**Stop or Escalate If:**

* Escalate if the AGB is not found at the verified location.

---

## Success Criteria

* The node code or cell code is matched to the physical number on the floor QR code.
* The AGB floor location is confirmed, or the verified location is communicated to another person.

## Failure Conditions

* The node code or cell code cannot be obtained.
* The floor QR code marker cannot be found or read.
* The floor QR code number does not match the provided node code or cell code.
* The AGB is not found at the verified location.

## Escalation Guidance

* Escalate if the floor QR code number does not match the provided node code or cell code.
* Escalate if the AGB is not found at the verified location.
* Escalate if the floor QR code marker cannot be located or read.

## Missing Details / Known Gaps

* The source does not specify where the node code or cell code is retrieved from within a system interface.
* The source does not provide a detailed escalation path or named escalation role.
* The source does not provide timing estimates.
* The source does not provide additional visual detail of the floor QR code beyond stating that it has a physical number.
* The attached artifact frame is primarily a different slide; its relevance is based on aligned transcript evidence rather than a dedicated floor QR code image.

## Source Lineage

- Candidate IDs: candidate_training_video_verify_agb_location_by_node_code
- Source ID: `training_video_day1`
- Source Type: `training_video`
