Complete Stage 5 of the OptiSweep ingestion pipeline: **LLM Runbook Candidate Discovery**.

Stages 1–4 are complete.

Current inputs:

```text
data/output/manual_optisweep_om_v3/source_bundle.json
data/output/manual_optisweep_om_v3/source_artifacts_enriched.json
data/output/manual_optisweep_om_v3/operational_context.json
```

Stage 5 should use an LLM to identify reusable runbook/procedure candidates from the OptiSweep Operation and Maintenance Manual.

Keep this simple.

This stage should discover candidate runbooks only. It should not create final production runbooks yet.

## Goal

Create:

```text
data/output/manual_optisweep_om_v3/runbook_candidates.json
data/output/manual_optisweep_om_v3/runbook_candidate_extraction_report.json
```

A runbook candidate is a lightweight record that says:

```text
There appears to be a reusable procedure here.
This is what it is called.
This is what it is for.
This is who likely performs it.
These are the rough steps.
These are the relevant source refs and artifacts.
```

Final runbook drafting, step normalization, merging with existing runbooks, and validation can happen in later stages.

## Important rules

Do not create workflows.

Do not create decision trees.

Do not create trigger conditions.

Do not create routing logic.

Do not create ML labels.

Do not populate workflow links.

Do not write to Cosmos, PostgreSQL, Azure Search, or any external service.

Do not invent commands, service names, access paths, hostnames, SQL queries, API endpoints, or screenshots.

Do not create a new runbook for every workflow or every issue.

Runbooks/procedures are reusable instructional assets.

A runbook is not a workflow.

A workflow decides when to use a runbook later.

## What to extract

Extract reusable procedure candidates from the manual.

Examples of good candidates:

```text
Start OptiSweep System
Stop OptiSweep System
Start Operator Station
Stop Operator Station
Check Operator Station HMI Data Screen
Check Tipper Heartbeat Stats
Check Operator Station Alarms
Use Hospital Add Tote Screen
Use Hospital Remove Tote Screen
Review Hospital Status Messages
Recover AGV Bump Fault
Recover Faulted AGV With Tote
Initialize Tote With Sorter Scanner
Check AGV Status Screen
Reference Operator Station Axes
Review Operator Station IO Diagnostics
Perform Operator Station Lockout/Tagout
Perform Pneumatic LOTO
```

These are examples only. Do not hardcode this exact list. Let the source material drive the output.

Do not extract every maintenance replacement procedure in full detail yet unless the source clearly describes it as a reusable procedure and it is useful for support. It is acceptable to include maintenance candidates, but keep them lightweight.

Target output:

```text
15 to 35 runbook candidates
```

Prioritize operational and troubleshooting-useful procedures first.

## Candidate schema

Create or update:

```text
src/optisweep_ingestion/schemas/runbook_candidate.py
```

Use a simple Pydantic model:

```python
class RunbookCandidate(BaseModel):
    candidate_id: str
    title: str
    candidate_goal: str
    likely_procedure_type: str
    likely_role_required: str
    support_safe: bool | None = None
    summary: str

    rough_steps: list[str] = []
    expected_result: str | None = None
    failure_or_escalation_notes: list[str] = []

    access_or_tools_needed: list[str] = []
    related_context_ids: list[str] = []
    related_artifact_ids: list[str] = []
    source_refs: list[dict] = []

    confidence: str = "medium"
    candidate_status: str = "needs_review"
    extraction_notes: list[str] = []
    metadata: dict = {}
```

Allowed `likely_procedure_type` values:

```text
operation
diagnostic
recovery
reference
```

Allowed `likely_role_required` values:

```text
operator
L1_support
L2_support
L3_support
```

Allowed `confidence` values:

```text
high
medium
low
```

Default `candidate_status`:

```text
needs_review
```

## Role rules

Use only these roles:

```text
operator
L1_support
L2_support
L3_support
```

Role guidance:

```text
operator
= Site/floor user performing approved HMI, scanner, RMS, visual inspection, or normal operating actions.

L1_support
= Technical support operator guiding approved support-safe checks, collecting evidence, reviewing screenshots, and deciding whether escalation is needed.

L2_support
= Advanced support user who may use approved remote access, inspect logs/dashboards/application health, and perform documented support procedures.

L3_support
= Engineering, infrastructure, controls, database, code/configuration, or senior escalation owner.
```

If the source says “maintenance personnel,” map based on risk:

```text
operator
= only if the action is a normal site-safe HMI/scanner/visual action.

L2_support
= if it is advanced support/maintenance but documented and not clearly infrastructure/code/database/controls.

L3_support
= if it involves controls, server, database, software, unsafe recovery, infrastructure, or high-risk production changes.
```

Do not output `engineer`, `maintenance`, `infrastructure`, `SME`, or `support` as role values.

## Procedure type rules

Use:

```text
operation
diagnostic
recovery
reference
```

Definitions:

```text
operation
= normal operating procedure, such as starting/stopping the system or using a standard HMI/scanner flow.

diagnostic
= checking a screen, status, value, alarm, dashboard, or system behavior.

recovery
= recovering from a known fault or abnormal condition.

reference
= useful instructional guidance that is not a strict procedure yet.
```

Do not use `maintenance` as a procedure type.

If the source is maintenance-like, use one of the allowed types and reflect risk through role and notes.

## Source packet preparation

Create simple packets for the LLM using:

```text
source_bundle.json
source_artifacts_enriched.json
operational_context.json
```

Each packet should include:

```text
section_id
section/page text
related operational context records
related enriched artifact records
artifact IDs
artifact titles
artifact what_to_look_at
source refs
```

Do not send the entire manual as one giant prompt.

A simple packet strategy is enough:

```text
one packet per major section or high-value subsection
```

Good sections to include:

```text
Safety / LOTO
System Overview
System HMI Screens
Operator Station HMI Screens
Hospital HMI Screens
Alarms/Faults
System Operation
AGV Faults
Hospital Station Operation
Sorter Scanner Operation
Troubleshooting
Maintenance overview and selected support-relevant procedures
```

## LLM prompt

Create:

```text
src/optisweep_ingestion/prompts/runbook_candidate_discovery_prompt.md
```

Prompt:

```markdown
# OptiSweep Runbook Candidate Discovery Prompt

You identify reusable runbook/procedure candidates from OptiSweep source material.

A runbook/procedure is a reusable instructional asset.

A runbook answers:
- What is this procedure?
- What is the procedure goal?
- Who likely performs it?
- What tools, screens, or access are needed?
- What are the rough steps?
- What result should the user expect?
- When should the user stop or escalate?
- What source evidence and screenshots support it?

A runbook is not a workflow.
A runbook is not a decision tree.
A runbook does not contain trigger conditions.
A runbook does not contain routing logic.
A runbook does not contain ML labels.

You are discovering candidates only.
Do not write final polished runbooks yet.

Use only the provided source text, operational context, and artifact metadata.

Do not invent commands, access paths, service names, hostnames, SQL queries, API endpoints, or screenshots.

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
      "confidence": "medium",
      "candidate_status": "needs_review",
      "extraction_notes": [],
      "metadata": {
        "created_by": "runbook_candidate_discovery_agent",
        "source_quality": "official_manual"
      }
    }
  ]
}

Allowed likely_procedure_type values:
- operation
- diagnostic
- recovery
- reference

Allowed likely_role_required values:
- operator
- L1_support
- L2_support
- L3_support

Allowed confidence values:
- high
- medium
- low

Rules:
1. Extract only reusable procedures.
2. Do not create final runbooks yet.
3. Do not create workflows.
4. Do not include trigger conditions.
5. Do not include routing logic.
6. Do not include next-step branching.
7. Do not invent missing details.
8. Keep rough_steps brief and source-grounded.
9. Include related artifact IDs when screenshots/images support the candidate.
10. Include related context IDs when operational context supports the candidate.
11. Include source refs for every candidate.
12. If the source is unclear, either mark confidence low or skip the candidate.
13. If a procedure looks duplicate within the same packet, output it once.
```

## Example candidate

Example only. Do not hardcode this exact record.

```json
{
  "candidate_id": "candidate_check_tipper_heartbeat_stats",
  "title": "Check Tipper Heartbeat Stats",
  "candidate_goal": "Check heartbeat timing values on the Operator Station HMI Data screen.",
  "likely_procedure_type": "diagnostic",
  "likely_role_required": "operator",
  "support_safe": true,
  "summary": "This candidate describes how a user can inspect the Heartbeat section of the Operator Station VISU_DATA screen to review Last, Max, and Min heartbeat timing values between the tipper and WCS.",
  "rough_steps": [
    "Open the Operator Station HMI Data screen.",
    "Locate the Heartbeat section.",
    "Review the Last, Max, and Min values.",
    "Note whether the Max value indicates a heartbeat signal longer than 10 seconds."
  ],
  "expected_result": "The user can see the most recent, longest, and shortest heartbeat timing values.",
  "failure_or_escalation_notes": [
    "A heartbeat signal longer than 10 seconds can cause operational issues due to mis-synchronization.",
    "Escalate if heartbeat values appear abnormal or the screen is unavailable."
  ],
  "access_or_tools_needed": [
    "Operator Station HMI access"
  ],
  "related_context_ids": [
    "ctx_heartbeat_stats_v1"
  ],
  "related_artifact_ids": [
    "artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats"
  ],
  "source_refs": [
    {
      "source_document_id": "optisweep_operation_and_maintenance_manual_final_1",
      "source_type": "official_manual",
      "page": 52,
      "section_id": "optisweep_operation_and_maintenance_manual_final_1_4_1_2_2_visu_data_screen",
      "figure_id": "fig_4_22",
      "figure_number": "Figure 4-22",
      "quote_or_summary": "The Heartbeat section provides Last, Max, and Min heartbeat timing values and warns that signals longer than 10 seconds can cause operational issues."
    }
  ],
  "confidence": "high",
  "candidate_status": "needs_review",
  "extraction_notes": [],
  "metadata": {
    "created_by": "runbook_candidate_discovery_agent",
    "source_quality": "official_manual"
  }
}
```

## Implementation files

Create or update:

```text
src/optisweep_ingestion/schemas/runbook_candidate.py
src/optisweep_ingestion/tools/runbook_candidate_extractor.py
src/optisweep_ingestion/prompts/runbook_candidate_discovery_prompt.md
scripts/extract_runbook_candidates.py
tests/test_runbook_candidate_extractor.py
README.md
```

## CLI

Create:

```text
scripts/extract_runbook_candidates.py
```

Use Typer if the repo already uses Typer.

Example:

```bash
python scripts/extract_runbook_candidates.py \
  --source-bundle data/output/manual_optisweep_om_v3/source_bundle.json \
  --source-artifacts data/output/manual_optisweep_om_v3/source_artifacts_enriched.json \
  --operational-context data/output/manual_optisweep_om_v3/operational_context.json \
  --output-dir data/output/manual_optisweep_om_v3 \
  --llm
```

For this stage, `--llm` is expected.

If the LLM client is not configured, fail clearly with a helpful error.

Do not silently generate fake runbook candidates.

## Simple validation

After LLM output, run simple validation:

1. Every candidate has `candidate_id`.
2. Every candidate has `title`.
3. Every candidate has `candidate_goal`.
4. Every candidate has allowed `likely_procedure_type`.
5. Every candidate has allowed `likely_role_required`.
6. Every candidate has `summary`.
7. Every candidate has at least one rough step unless the type is `reference`.
8. Every candidate has at least one `source_ref`.
9. Referenced artifact IDs exist in `source_artifacts_enriched.json`.
10. Referenced context IDs exist in `operational_context.json`.
11. `candidate_status` is `needs_review`.
12. No forbidden fields exist.

Forbidden fields:

```text
trigger_conditions
candidate_input_signals
produces_signals
resolved_signals
workflow_branch
decision_node
ml_label
routing_key
next_step_on_success
next_step_on_failure
workflow_id
workflow_step_id
```

If a candidate fails validation, either repair it with the LLM once or drop it and log it in the report.

Keep validation simple.

## Deduplication

After collecting candidates from all packets, run a simple dedupe pass.

Deduplicate when title and goal are substantially the same.

Simple deterministic dedupe is fine:

```text
normalize title
normalize goal
compare lowercase strings
merge source refs and artifact IDs
```

Do not overbuild semantic duplicate detection yet.

If two candidates are similar but not clearly duplicates, keep both and add an extraction note.

## Extraction report

Write:

```text
runbook_candidate_extraction_report.json
```

Simple report shape:

```json
{
  "llm_used": true,
  "input_source_bundle": "data/output/manual_optisweep_om_v3/source_bundle.json",
  "input_source_artifacts": "data/output/manual_optisweep_om_v3/source_artifacts_enriched.json",
  "input_operational_context": "data/output/manual_optisweep_om_v3/operational_context.json",
  "candidate_count": 0,
  "candidate_counts_by_type": {},
  "candidate_counts_by_role": {},
  "candidates_with_artifacts": 0,
  "candidates_with_context": 0,
  "candidates_missing_source_refs": 0,
  "dropped_candidate_count": 0,
  "deduped_candidate_count": 0,
  "priority_candidate_check": {
    "check_tipper_heartbeat_stats": {
      "found": true,
      "has_artifact_ref": true,
      "has_context_ref": true,
      "mentions_last_max_min": true,
      "mentions_10_seconds": true
    },
    "check_operator_station_alarms": {
      "found": true,
      "has_artifact_ref": true
    },
    "use_hospital_add_tote": {
      "found": true,
      "has_artifact_ref": true
    },
    "use_hospital_remove_tote": {
      "found": true,
      "has_artifact_ref": true
    },
    "recover_agv_bump_fault": {
      "found": true,
      "has_artifact_ref": true
    }
  },
  "failed_packets": [],
  "warnings": []
}
```

## Priority candidate checks

Check whether these likely candidates were found:

```text
Check Tipper Heartbeat Stats
Check Operator Station Alarms
Use Hospital Add Tote Screen
Use Hospital Remove Tote Screen
Recover AGV Bump Fault
Recover Faulted AGV With Tote
Start OptiSweep System
Start Operator Station
Initialize Tote With Sorter Scanner
```

The report should not fail the whole extraction if one is missing, but it should make missing priority candidates visible.

## Tests

Keep tests lightweight.

Add tests for:

1. Parsing LLM JSON response.
2. Validating allowed procedure types.
3. Validating allowed role values.
4. Rejecting forbidden fields.
5. Verifying source refs are required.
6. Verifying related artifact IDs exist.
7. Verifying related context IDs exist.
8. Dedupe merges duplicate title/goal candidates.
9. Priority candidate report logic.
10. Heartbeat candidate check detects:

    * Last
    * Max
    * Min
    * 10 seconds
    * artifact ref
    * context ref

Do not require a real LLM call in unit tests. Mock the LLM response.

## README update

Add:

````markdown
## Current Stage: Stage 5 — LLM Runbook Candidate Discovery

Stage 5 uses the source bundle, enriched source artifacts, and operational context records to identify reusable runbook/procedure candidates.

A runbook candidate is not a final runbook. It is a lightweight record that identifies a reusable procedure opportunity, rough steps, likely role, likely procedure type, source refs, related context, and related artifacts.

This stage does not create workflows, routing rules, trigger conditions, or final approved runbooks.

Inputs:

```text
data/output/manual_optisweep_om_v3/source_bundle.json
data/output/manual_optisweep_om_v3/source_artifacts_enriched.json
data/output/manual_optisweep_om_v3/operational_context.json
````

Outputs:

```text
data/output/manual_optisweep_om_v3/runbook_candidates.json
data/output/manual_optisweep_om_v3/runbook_candidate_extraction_report.json
```

Run:

```bash
python scripts/extract_runbook_candidates.py \
  --source-bundle data/output/manual_optisweep_om_v3/source_bundle.json \
  --source-artifacts data/output/manual_optisweep_om_v3/source_artifacts_enriched.json \
  --operational-context data/output/manual_optisweep_om_v3/operational_context.json \
  --output-dir data/output/manual_optisweep_om_v3 \
  --llm
```

```

## Acceptance criteria

Stage 5 is complete when:

- `runbook_candidates.json` is created.
- `runbook_candidate_extraction_report.json` is created.
- Output contains roughly 15–35 useful runbook candidates.
- Candidates are source-grounded.
- Candidates include source refs.
- Candidates reference existing artifact IDs when relevant.
- Candidates reference existing context IDs when relevant.
- Heartbeat candidate is extracted correctly.
- Operator Station Alarms candidate is extracted.
- Hospital Add Tote candidate is extracted.
- Hospital Remove Tote candidate is extracted.
- AGV fault recovery candidate is extracted if supported by the source.
- No final runbooks are created.
- No workflows are created.
- No trigger/routing logic is created.
- No database writes occur.
- Tests pass.

Keep this stage simple. The goal is candidate discovery, not final runbook drafting.
```
