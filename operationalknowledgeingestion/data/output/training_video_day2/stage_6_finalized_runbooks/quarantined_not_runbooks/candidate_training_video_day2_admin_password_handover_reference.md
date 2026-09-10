# Retrieve the Admin Password From Handover Documentation (Admin Password Reference)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_retrieve_admin_password_from_handover_documentation_v1` |
| Title | Retrieve the Admin Password From Handover Documentation (Admin Password Reference) |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `site_interview` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the handover documentation as the source of truth for the OptiSweep admin password. If the password is not present, coordinate with Michael Thomas and follow the referenced handover forms/links and handover checklist timing (checklist completed in January of last year).

## When To Use

When you need the documented OptiSweep admin password for accessing/administering the system and the source indicates it should be contained in the handover documentation.

## Do Not Use For

* Do not guess or attempt alternative passwords if the admin password is not found in the handover documentation.

## Access Or Tools Needed

* Handover documentation (including handover checklist)
* Contact path to Michael Thomas (as referenced by the source)

## Related Operational Context

* ctx_training_video_handover_admin_password_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0036_works_but_in_real_time_having_primary_02_59_48_000](assets/e0fc5fc6c1fb24ec.jpg)

*Video frame containing the spoken instruction that the admin password should be in the handover documentation and to get with Michael Thomas if needed (includes mention of forms/links and January handover checklist timing).*

## Procedure Steps

### Step 1 — Locate the handover documentation and handover checklist referenced by the source

**Responsible role:** L1_support

**Instruction:**
Open/access the handover documentation and the handover checklist referenced by the handover materials for the system.

**Expected result:**
You have the handover documentation available to search for the admin password entry.

**Stop or Escalate If:**

* If the handover documentation/handover checklist cannot be found or accessed, escalate/coordinate with Michael Thomas per the source guidance.

---

### Step 2 — Search within the handover documentation for the “admin password” entry

**Responsible role:** L1_support

**Instruction:**
Within the handover documentation, search for the entry labeled “admin password”.

**Expected result:**
The handover documentation contains an “admin password” entry that you can use.

**Stop or Escalate If:**

* If the admin password is not present in the handover documentation, do not guess passwords; coordinate with Michael Thomas per the source guidance.

---

### Step 3 — If the admin password is not present, coordinate with Michael Thomas as suggested by the source

**Responsible role:** L1_support

**Instruction:**
If the admin password is not found, contact Michael Thomas and follow the referenced process that includes filling out forms and providing links; note that the handover checklist was done in January of last year.

**Expected result:**
You have a clear path/contact (Michael Thomas) to retrieve the admin password when it is not in the handover documentation.

**Stop or Escalate If:**

* Stop if the admin password cannot be found in the handover documentation and do not guess passwords.
* Escalate/coordinate to Michael Thomas per the source if the documentation does not contain the password.

---

### Step 4 — Record the admin password from the handover documentation for use in the appropriate admin access context

**Responsible role:** L1_support

**Instruction:**
Once found in the handover documentation, record the admin password for use in the appropriate admin access context.

**Expected result:**
You have the admin password recorded from the handover documentation (or you have confirmed who to contact to retrieve it if missing).

**Stop or Escalate If:**

* If the admin password was not found and you have not coordinated with Michael Thomas, stop and follow the escalation guidance.

---

## Success Criteria

* Admin password is obtained from the handover documentation, OR the named contact (Michael Thomas) is identified/engaged to retrieve it when missing.

## Failure Conditions

* Admin password is not found in the handover documentation and passwords are guessed.
* No escalation/coordination occurs when the password is missing.

## Escalation Guidance

* If the admin password cannot be found in the handover documentation, coordinate with Michael Thomas as referenced (including filling out forms and providing links).

## Missing Details / Known Gaps

* The source does not specify the exact handover document name(s), file location, or where within the handover checklist/forms the “admin password” entry appears.
* The source does not provide a direct contact method for Michael Thomas (only that you should “get with Michael Thomas”).

## Source Lineage

- Candidate IDs: candidate_training_video_day2_admin_password_handover_reference
- Source ID: `training_video_day2`
- Source Type: `training_video`
