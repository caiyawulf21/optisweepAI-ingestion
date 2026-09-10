# Check Overall System state on the AVEVA API page (System State / System Startup / Bag Out / Shutdown / Purge)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_overall_system_state_on_aveva_api_page_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `fleet_system_status` |
| Access Surface | `aveva_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the AVEVA HMI “Overall System” / “API page” to verify the current OptiSweep system lifecycle state shown in the “System State” field, and confirm the presence/meaning of the system-level lifecycle actions: System Startup, System Bag Out, System Shutdown, and System Purge.

## When To Use

When you need to confirm the current OptiSweep system lifecycle phase and verify that the AVEVA “API page” is showing the expected system-level lifecycle controls (System Startup / Bag Out / Shutdown / Purge) and the “System State” value.

## Source Procedure References

- proc_check_overall_system_state_on_aveva_api_page_v1

## Procedure Steps

### Step 1 — Open the AVEVA HMI Overall System / API page view

**Responsible role:** L1_support

**Instruction:**
Open the AVEVA HMI “Overall System” / “API page” view that shows the left-side items labeled: System State, System Startup, System Bag Out, System Shutdown, and System Purge.

**Expected result:**
The AVEVA “API page” is visible with the left-side panel containing the labeled sections for System State, System Startup, System Bag Out, System Shutdown, and System Purge.

---

### Step 2 — Read the System State value

**Responsible role:** L1_support

**Instruction:**
On the AVEVA “API page”, locate the “System State” field and read the value shown there.

**Expected result:**
The “System State” field shows the current system lifecycle state.

---

### Step 3 — Confirm lifecycle action sections are present (Startup / Bag Out / Shutdown / Purge)

**Responsible role:** L1_support

**Instruction:**
Confirm the AVEVA “API page” left-side panel displays the labeled sections for: System Startup, System Bag Out, System Shutdown, and System Purge.

**Expected result:**
The left-side panel contains the labeled sections for System Startup, System Bag Out, System Shutdown, and System Purge.

---

### Step 4 — Sanity-check lifecycle context using the displayed lifecycle meanings

**Responsible role:** L1_support

**Instruction:**
Using the lifecycle meanings shown for each section on the AVEVA “API page”, sanity-check the lifecycle context implied by the current “System State” value:

**Expected result:**
You can map the current “System State” to the lifecycle context described for System Startup / Bag Out / Shutdown / Purge.

---

### Step 5 — Stop and escalate on missing fields/labels or unexpected lifecycle state

**Responsible role:** L1_support

**Instruction:**
If any of the following conditions occur, stop the check and escalate.

**Expected result:**
Escalation is triggered when the AVEVA “API page” is missing expected UI elements or when “System State” appears inconsistent with the operational lifecycle phase.

---

## Success Criteria

- On the AVEVA “API page”, the “System State” field is present and shows a current system lifecycle state value.
- The left-side panel contains the labeled sections for System Startup, System Bag Out, System Shutdown, and System Purge.
- The current “System State” value can be sanity-checked against the lifecycle meanings without indicating an unexpected lifecycle phase for the operational moment.

## Failure Conditions

- AVEVA “API page” missing the “System State” field.
- AVEVA “API page” missing one or more left-side lifecycle labels/sections (System Startup / Bag Out / Shutdown / Purge).
- System State value appears inconsistent with the expected lifecycle phase for the current operational moment.

## Escalation Guidance

- Escalate if the AVEVA “API page” does not display the expected “System State” field and/or the left-side lifecycle labels (System Startup / Bag Out / Shutdown / Purge), or if the “System State” value appears inconsistent with the expected lifecycle phase.

## Missing Details / Known Gaps

- No explicit click-path/navigation steps are provided in the packet transcript/OCR for how to reach the AVEVA “Overall System” / “API page” from a starting screen; the procedure assumes the operator can open the correct AVEVA view.
