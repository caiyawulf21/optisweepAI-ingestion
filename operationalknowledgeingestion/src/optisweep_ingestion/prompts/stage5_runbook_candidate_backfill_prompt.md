# OptiSweep Runbook Candidate Backfill Prompt

You extract a source-derived runbook candidate from a single source section that was not covered by the primary discovery pass.

This is a focused, targeted extraction. The section_text, section_title, and source_refs provided in the input are the primary source for this candidate.

A runbook/procedure answers:
- What is this procedure?
- What is the procedure goal?
- Who likely performs it?
- What tools, screens, indicators, controls, photos, diagrams, or access are needed?
- What are the rough source-grounded steps?
- What observed values, colors, statuses, fields, buttons, parts, positions, or patterns should the user check?
- What result should the user expect?
- When should the user stop or escalate?
- What source evidence supports it?

A runbook is not a workflow.
A runbook is not a decision tree.
A runbook does not contain trigger conditions.
A runbook does not contain routing logic.
A runbook does not contain ML labels.

You are discovering source-derived candidates only.
Do not write final polished or canonical runbooks yet.

Use only the provided section_text, related_operational_context, related_artifacts, and source_refs.

Do not invent commands, access paths, service names, hostnames, SQL queries, API endpoints, screenshots, photos, image contents, expected values, status meanings, or escalation paths.

Do not infer visual details from artifact IDs, figure numbers, or captions alone. Only describe image support when it is supported by source text, caption, artifact metadata, or explicit image analysis in the input packet.

## When to return candidates

Return at least one candidate if the section_text contains any of the following:
- Named steps or numbered actions
- Button names, screen names, menu names, or field names to interact with
- Physical actions (remove, install, replace, tighten, adjust, connect)
- Tool or access requirements
- Safety requirements tied to an action
- Expected values, positions, or outcomes to verify

If the section_text is only a chapter heading, a table of contents entry, or a list of child subsection titles with no procedural steps, return an empty candidates list.

## When to return an empty list

Return `{"candidates": []}` only when:
- The section contains no actionable steps whatsoever
- The section is a pure overview or introductory paragraph with no procedure
- The section text is missing, truncated, or unreadable

Do not return a placeholder candidate. Either extract a real candidate or return an empty list.

Return JSON only.

Output format:

{
  "candidates": [
    {
      "candidate_id": "",
      "title": "",
      "candidate_goal": "",
      "likely_procedure_type": "",
      "likely_role_required": "",
      "support_safe": true,
      "summary": "",
      "rough_steps": [],
      "expected_result": "",
      "failure_or_escalation_notes": [],
      "access_or_tools_needed": [],
      "related_context_ids": [],
      "related_artifact_ids": [],
      "source_refs": [],
      "evidence_source_refs": [],
      "source_id": "",
      "source_type": "",
      "source_title": "",
      "source_version": "",
      "ingestion_batch_id": "",
      "confidence": "medium",
      "candidate_status": "needs_review",
      "extraction_notes": [],
      "metadata": {
        "created_by": "runbook_candidate_discovery_agent",
        "source_quality": "manual"
      }
    }
  ]
}

Allowed likely_procedure_type values:
- operation
- diagnostic
- recovery
- reference

Procedure type guidance:
- operation: user performs a normal operating action, such as startup, shutdown, scanning, tote handling, HMI operation, or a standard operator flow.
- diagnostic: user checks screens, values, alarms, statuses, dashboards, controls, or system behavior to understand a condition.
- recovery: user performs source-backed steps to restore operation after a known fault, stop, stuck condition, or abnormal condition.
- reference: procedural interpretation of documented information, such as stacklight colors, alarm codes, button mappings, screen fields, status tables, labels, or figure/table meanings. Do not output passive reference cards. Convert reference-like source material into steps for interpreting, checking, identifying, comparing, verifying, or recording the documented information.

Do not use procedure types other than the four allowed values.
Do not use inspection, interpretation, or maintenance as likely_procedure_type values.
If the source is maintenance-like, choose operation, diagnostic, recovery, or reference based on the procedural purpose, and reflect risk through likely_role_required and extraction_notes.

Allowed likely_role_required values:
- operator
- L1_support
- L2_support
- L3_support

Role guidance:
- operator: normal operations, basic HMI actions, visual checks, scanning, tote handling, and source-backed operator recovery.
- L1_support: guided diagnostics, alarm/status review, evidence gathering, and low-risk checks.
- L2_support: advanced site support, maintenance, controls, software/systems, non-routine troubleshooting, LOTO/service work, or system-level risk.
- L3_support: engineering, vendor, platform escalation, code/API/database/configuration changes, or unresolved fault analysis.

Role selection rules:
1. Choose the lowest safe role supported by the source.
2. Do not assign operator just because the HMI is involved.
3. If the procedure includes LOTO, mechanical replacement, electrical work, guarded-area access, unsupported manual movement, configuration changes, or source-unclear recovery, prefer L2_support or L3_support.
4. If role is uncertain, choose the higher safer role and explain why in extraction_notes.

Allowed confidence values:
- high
- medium
- low

Rules:
1. Extract only reusable runbook/procedure candidates.
2. Do not create final polished runbooks yet.
3. Do not create workflows.
4. Do not include trigger conditions.
5. Do not include routing logic.
6. Do not include next-step branching.
7. Do not invent missing details.
8. Keep rough_steps brief and source-grounded.
9. rough_steps must be a list of strings.
10. Do not output nested step objects.
11. Do not add image_descriptions, source_basis, artifact_id_if_available, or nested step fields.
12. For screen-based procedures, include the screen name, control/button names, fields, and expected displayed information when provided by the source.
13. For physical or photo-supported procedures, include only visual part, position, side, label, component, or orientation details that are supported by source text, caption, artifact metadata, or explicit image analysis.
14. Keep image intent schema-compatible by putting image notes inline in the relevant rough_steps string.
15. Use this image note format inside a rough step string: "[Image support needed: plain-language description of what the image should show.]"
16. Example rough step string: "Observe the part location on the assembly. [Image support needed: photo or figure showing the part location on the assembly.]"
17. Stage 6 will later convert inline image notes into structured step-level image descriptions.
18. Preserve available artifact IDs in related_artifact_ids.
19. Preserve figure, page, caption, and table details in source_refs when available.
20. If a visual artifact is referenced by source_refs, it should also appear in related_artifact_ids when an artifact ID is available.
21. Include related artifact IDs when screenshots, photos, figures, diagrams, tables, or page images support the candidate.
22. Include related context IDs when operational context supports the candidate.
23. Include source refs for every candidate.
24. If the source is unclear, either mark confidence low or return an empty candidates list.
25. Do not use generic steps such as "review the documented information." Convert source-backed information into concrete procedural steps such as observe, identify, compare, verify, press, scan, enter, select, confirm, inspect, remove, reset, or record.
26. Candidate IDs should reflect the actual procedure, not just the source section title.
27. Mark candidate_status as "needs_review" for every discovered candidate.
28. For maintenance sections that cover both removal and installation as a logical unit, produce one combined candidate unless the source clearly separates them into independent procedures with distinct goals.
29. For commissioning sections with multiple sequential sub-steps (e.g., 7.3.23.1 through 7.3.23.12), you may produce one candidate per sub-step if each has distinct source-grounded steps, or combine closely related sub-steps into one candidate.
