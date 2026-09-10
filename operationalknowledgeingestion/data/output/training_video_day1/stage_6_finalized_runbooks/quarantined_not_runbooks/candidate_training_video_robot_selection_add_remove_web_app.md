# Use Geek Plus RMS Robot Selection screen to Add or Remove a robot by Robot ID

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_geek_plus_rms_robot_selection_add_remove_v1` |
| Title | Use Geek Plus RMS Robot Selection screen to Add or Remove a robot by Robot ID |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Geek Plus RMS web application Robot Selection screen to add (introduce) or remove a robot by entering its Robot ID (or selecting it from the list) and confirming the on-screen success message.

## When To Use

When support needs to introduce (add) or remove a robot in Geek Plus RMS during debug/support scenarios, using the Robot Selection screen’s Robot ID entry and Add/Remove actions.

## Safety And Operational Notes

* If you remove a robot while it is physically present/active on the floor, it can create a mismatch between the logical robot in RMS and the physical robot; the source notes this as a problem scenario (robot removal can lead to obstacle/crash risk if the physical robot remains).

## Access Or Tools Needed

* Geek Plus RMS web application access via OT network IP (local devices on OT net) or via authorized UPS VPN through Zscaler for remote support
* Robot Selection screen in the Geek Plus RMS web application
* Robot ID value(s) for the robot(s) being added/removed

## Related Operational Context

* ctx_training_video_robot_selection_add_remove_v1
* ctx_training_video_robot_id_entry_reference_v1

## Procedure Steps

### Step 1 — Open the Geek Plus RMS web application from the OT network

**Responsible role:** L1_support

**Instruction:**
From a device connected on the OT network, open the Geek Plus RMS web application using the site’s IP address.

**Expected result:**
The Geek Plus RMS web application loads and you can navigate to the Robot Selection screen.

**Stop or Escalate If:**

* If remote access is required and you cannot reach the Geek Plus RMS site, confirm you are authorized to use the UPS VPN through Zscaler and that you have the tenant ID/site authorization described in the source.

---

### Step 2 — Locate the Robot ID input area on the Robot Selection screen

**Responsible role:** L1_support

**Instruction:**
On the Robot Selection screen, find the Robot ID input area labeled for entering the corresponding robot ID.

**Expected result:**
The Robot ID field is visible and ready for entry.

---

### Step 3 — Add a robot by entering Robot ID and clicking Add

**Responsible role:** L1_support

**Instruction:**
Enter the corresponding robot ID into the Robot ID field, then click the "Add" button.

**Expected result:**
The Robot Selection screen displays an adding success confirmation message indicating the robot was added successfully.

**Stop or Escalate If:**

* If the system does not show the documented success confirmation after clicking Add, stop and escalate for support.

---

### Step 4 — Add using partial numeric entry when the robot is already introduced

**Responsible role:** L1_support

**Instruction:**
If the robot is already introduced, use partial numeric entry (e.g., typing digits ending in 188) so matching robots appear, then use the matching robot entry.

**Expected result:**
The Robot Selection screen shows matching robot(s) based on the partial numeric entry (e.g., robots ending in 188).

---

### Step 5 — Remove a robot by entering Robot ID or selecting it, then clicking Remove

**Responsible role:** L1_support

**Instruction:**
To remove a robot, enter the corresponding robot ID into the Robot ID field or select the robot from the list, then click the "Remove" button.

**Expected result:**
The Robot Selection screen displays a removal success confirmation message indicating the robot removal was successful.

**Stop or Escalate If:**

* If the system does not show the documented success confirmation after clicking Remove, stop and escalate for support.

---

## Success Criteria

* After clicking Add, the Robot Selection screen shows an adding success confirmation message.
* After clicking Remove, the Robot Selection screen shows a removal success confirmation message.

## Failure Conditions

* No adding success confirmation after clicking Add.
* No removal success confirmation after clicking Remove.

## Escalation Guidance

* If the system does not show the documented success confirmation after clicking Add or Remove, stop and escalate for support (the source provides success-confirmation behavior but does not specify error-handling steps).
* If remote access is required and you cannot reach the Geek Plus RMS site, confirm you are authorized to use the UPS VPN through Zscaler and that you have the tenant ID/site authorization described in the source.

## Missing Details / Known Gaps

* The source does not specify exact error messages, retry behavior, or what to do if Add/Remove fails beyond escalating.

## Source Lineage

- Candidate IDs: candidate_training_video_robot_selection_add_remove_web_app
- Source ID: `training_video_day1`
- Source Type: `training_video`
