# Switch RMS UI language to English using the top-right language selection icon

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_switch_rms_ui_language_to_english_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `fleet_system_status` |
| Access Surface | `rms_ui` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS top-right language selection control (third icon from the right) to switch the RMS interface from Chinese to English when the default login language appears in Chinese.

## When To Use

Use when the RMS / fleet status UI loads in Chinese and you need the interface labels in English to operate the RMS.

## Source Procedure References

- proc_switch_rms_ui_language_to_english_v1

## Procedure Steps

### Step 1 — Open RMS / fleet status UI and locate the top-right language selection icon

**Responsible role:** operator

**Instruction:**
In the RMS / fleet status UI (rms_ui) in your browser, look at the top-right corner and locate the language selection control (the third icon from the right).

**Expected result:**
You can visually identify the top-right language selection control (third icon from the right) on the RMS UI.

---

### Step 2 — Switch the RMS UI language from Chinese to English

**Responsible role:** operator

**Instruction:**
If the RMS UI is currently in Chinese, click the third icon from the right (language section) and switch the language to English.

**Expected result:**
RMS UI text and labels display in English (not Chinese) after selecting the English language option.

---

## Success Criteria

- RMS UI labels and text display in English rather than Chinese after using the top-right language selection control.

## Failure Conditions

- Language does not change after clicking the third icon from the right.

## Escalation Guidance

- If the language does not change after clicking the third icon from the right, stop and escalate to support. The source does not provide further troubleshooting steps.

## Missing Details / Known Gaps

- The source does not provide the exact visible label text for the English option in the language menu; success is validated by observable UI language change to English.
