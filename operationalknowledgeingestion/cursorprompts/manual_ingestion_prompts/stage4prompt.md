Complete Stage 4 of the OptiSweep ingestion pipeline: **LLM Operational Context Extraction**.

Stage 1, Stage 2, and Stage 3 are complete.

Current inputs:

```text
data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json
data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/source_artifacts_enriched.json
data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/artifact_enrichment_report.json
```

Stage 4 should use an LLM to extract stable operational context records from the OptiSweep Operation and Maintenance Manual.

Keep this simple.

Do not overbuild chunking, graph relationships, workflow logic, runbook extraction, or complex review states yet.

## Goal

Create a simple `operational_context.json` file containing reusable background knowledge about OptiSweep.

Operational context answers questions like:

```text
What is OptiSweep?
What does the Operator Station do?
What does the Hospital Station do?
What is the VISU_DATA screen?
What do Heartbeat Last, Max, and Min mean?
What does the Operator Station Alarms screen show?
What does the Hospital Add Tote screen do?
What does the Hospital Remove Tote screen do?
What is RMS?
What is WCS?
What do AGV fault screens show?
```

Operational context is **not** a procedure yet.

It explains systems, screens, metrics, alarms, statuses, components, and operating concepts.

## Outputs

Write:

```text
data/output/manual_optisweep_om_v3/stage_4_operational_context/operational_context.json
data/output/manual_optisweep_om_v3/operational_context_extraction_report.json
```

Do not overwrite prior stage outputs.

## Important rules

Do not create runbooks yet.

Do not create workflows.

Do not create troubleshooting decision trees.

Do not create trigger conditions.

Do not create ML labels.

Do not create routing rules.

Do not populate runbook/procedure/workflow links yet.

Do not write to Cosmos, PostgreSQL, Azure Search, or any external service.

Use the source bundle and enriched artifacts only.

## Simple context schema

Create or update:

```text
src/optisweep_ingestion/schemas/operational_context.py
```

Use a simple Pydantic model:

```python
class OperationalContext(BaseModel):
    context_id: str
    title: str
    context_type: str
    summary: str
    details: str
    applies_to: list[str] = []
    key_terms: list[str] = []
    related_artifact_ids: list[str] = []
    source_refs: list[dict] = []
    retrieval_text: str
    validation_status: str = "needs_review"
    metadata: dict = {}
```

Allowed `context_type` values:

```text
system_overview
component_reference
hmi_screen_reference
hmi_metric_reference
alarm_reference
status_reference
role_or_access_reference
safety_reference
glossary
troubleshooting_reference
operation_reference
maintenance_reference
```

Default `validation_status`:

```text
needs_review
```

Do not add complex approval states yet.

## What to extract

Use the manual text and enriched source artifacts to extract context records for important stable concepts.

Start with high-value records only.

Target around:

```text
20 to 40 operational context records
```

Do not try to extract hundreds of records.

Prioritize:

```text
OptiSweep system overview
AGV
Operator Station
Hospital Station
Tipper
WCS
RMS
System HMI
Operator Station HMI
Hospital HMI
System API screen
Operator Station VISU_DATA screen
Heartbeat Stats
Operator Station Alarms screen
Hospital Operations screen
Hospital Add Tote screen
Hospital Remove Tote screen
Hospital status messages
AGV Status screen
AGV Bump Fault screen
Faulted AGV with Tote screen
Alarms and Corrective Actions
Stacklights
Sorter Scanner / Tote Initialization
```

Do not hardcode exact records in the implementation. These are examples and priority concepts.

The LLM should decide records based on source evidence.

## Source packet preparation

Create simple source packets for the LLM.

Use:

```text
source_bundle pages/sections
source_artifacts_enriched records
```

Group by section where possible.

Each packet should include:

```text
section_id
section title if available
page numbers
section/page text
related enriched artifacts
artifact titles
artifact IDs
artifact retrieval text
source refs
```

Keep packets small enough for the LLM.

A simple approach is acceptable:

```text
one packet per important section
```

Important sections include:

```text
System Overview
Controls
System HMI Screens
Operator Station HMI Screens
Hospital HMI Screens
Alarms/Faults
System Operation
AGV Faults
Hospital Station Operation
Sorter Scanner Operation
Troubleshooting
Maintenance overview
```

## LLM prompt

Create:

```text
src/optisweep_ingestion/prompts/stage4_operational_context_extraction_prompt.md
```

Prompt:

```markdown
# OptiSweep Operational Context Extraction Prompt

You extract stable operational context records from OptiSweep source material.

Operational context explains systems, components, screens, metrics, statuses, alarms, and operating concepts.

You do not create runbooks.
You do not create workflows.
You do not create decision trees.
You do not create trigger conditions.
You do not create routing rules.
You do not create ML labels.

Use only the provided source text and artifact metadata.

Each context record must be source-grounded.

Return JSON only.

Output format:

{
  "contexts": [
    {
      "context_id": "",
      "title": "",
      "context_type": "",
      "summary": "",
      "details": "",
      "applies_to": [],
      "key_terms": [],
      "related_artifact_ids": [],
      "source_refs": [],
      "retrieval_text": "",
      "validation_status": "needs_review",
      "metadata": {
        "created_by": "operational_context_extraction_agent",
        "source_quality": "official_manual"
      }
    }
  ]
}

Allowed context_type values:
- system_overview
- component_reference
- hmi_screen_reference
- hmi_metric_reference
- alarm_reference
- status_reference
- role_or_access_reference
- safety_reference
- glossary
- troubleshooting_reference
- operation_reference
- maintenance_reference

Rules:
1. Use only source-grounded facts.
2. Do not invent site-specific details.
3. Do not invent commands.
4. Do not invent access paths.
5. Do not create step-by-step procedures.
6. Do not create troubleshooting branches.
7. Do not create trigger conditions.
8. Keep records reusable across incidents and workflows.
9. Include artifact IDs when a source artifact clearly supports the context.
10. Include source refs for every record.
11. If the source is unclear, skip the record instead of guessing.
```

## Example context record

Example only. Do not hardcode this exact record.

```json
{
  "context_id": "ctx_heartbeat_stats_v1",
  "title": "Operator Station Heartbeat Stats",
  "context_type": "hmi_metric_reference",
  "summary": "Heartbeat Stats show timing values for heartbeat signals between the tipper and WCS.",
  "details": "The manual explains that the Heartbeat section provides Last, Max, and Min timing values in milliseconds. Last is the most recent signal timing between the tipper and WCS. Max is the longest signal timing. Min is the shortest signal timing. A heartbeat signal longer than 10 seconds can cause operational issues with the tipper due to mis-synchronization.",
  "applies_to": [
    "Operator Station HMI",
    "Tipper",
    "WCS"
  ],
  "key_terms": [
    "Heartbeat",
    "Last",
    "Max",
    "Min",
    "10 seconds",
    "mis-synchronization"
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
  "retrieval_text": "Operator Station Heartbeat Stats on the VISU_DATA screen show Last, Max, and Min heartbeat timing values between the tipper and WCS. A heartbeat signal longer than 10 seconds can cause tipper operational issues due to mis-synchronization.",
  "validation_status": "needs_review",
  "metadata": {
    "created_by": "operational_context_extraction_agent",
    "source_quality": "official_manual"
  }
}
```

## Implementation files

Create or update:

```text
src/optisweep_ingestion/schemas/operational_context.py
src/optisweep_ingestion/tools/operational_context_extractor.py
src/optisweep_ingestion/prompts/stage4_operational_context_extraction_prompt.md
scripts/stage4_extract_operational_context.py
tests/test_operational_context_extractor.py
README.md
```

## CLI

Create:

```text
scripts/stage4_extract_operational_context.py
```

Use Typer if the repo already uses Typer.

Example:

```bash
python scripts/stage4_extract_operational_context.py \
  --source-bundle data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json \
  --source-artifacts data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/source_artifacts_enriched.json \
  --output-dir data/output/manual_optisweep_om_v3 \
  --llm
```

For this stage, `--llm` is expected.

If the LLM client is not configured, fail clearly with a helpful error.

Do not silently generate fake records.

## Extraction report

Write:

```text
operational_context_extraction_report.json
```

Simple report shape:

```json
{
  "llm_used": true,
  "input_source_bundle": "data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json",
  "input_source_artifacts": "data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/source_artifacts_enriched.json",
  "context_count": 0,
  "context_counts_by_type": {},
  "records_with_artifacts": 0,
  "records_without_artifacts": 0,
  "records_missing_source_refs": 0,
  "priority_context_check": {
    "heartbeat_stats": {
      "found": true,
      "has_artifact_ref": true,
      "mentions_last_max_min": true,
      "mentions_10_seconds": true
    },
    "operator_station_hmi": {
      "found": true,
      "has_artifact_ref": true
    },
    "hospital_add_tote": {
      "found": true,
      "has_artifact_ref": true
    },
    "hospital_remove_tote": {
      "found": true,
      "has_artifact_ref": true
    },
    "agv_bump_fault": {
      "found": true,
      "has_artifact_ref": true
    }
  },
  "failed_packets": [],
  "warnings": []
}
```

## Simple validation

After LLM output, run simple validation:

1. Every record has `context_id`.
2. Every record has `title`.
3. Every record has allowed `context_type`.
4. Every record has `summary`.
5. Every record has `details`.
6. Every record has `retrieval_text`.
7. Every record has at least one `source_ref`.
8. Referenced `artifact_ids` exist in `source_artifacts_enriched.json`.
9. `validation_status` is `needs_review`.
10. No forbidden fields exist.

Forbidden fields:

```text
trigger_conditions
workflow_branch
decision_node
ml_label
routing_key
procedure_steps
runbook_steps
commands
next_step_on_success
next_step_on_failure
```

If a record fails validation, either repair it with the LLM once or drop it and log it in the report.

Keep this simple.

## Tests

Keep tests lightweight.

Add tests for:

1. Parsing LLM JSON response.
2. Validating allowed context types.
3. Rejecting forbidden fields.
4. Verifying source refs are required.
5. Verifying related artifact IDs exist.
6. Building priority context report.
7. Heartbeat context check detects:

   * Last
   * Max
   * Min
   * 10 seconds
   * artifact ref

Do not require a real LLM call in unit tests. Mock the LLM response.

## README update

Add:

````markdown
## Current Stage: Stage 4 â€” LLM Operational Context Extraction

Stage 4 uses the source bundle and enriched source artifacts to extract reusable operational context records.

Operational context explains systems, components, screens, metrics, alarms, statuses, and stable operating concepts.

It does not create runbooks, procedures, workflows, routing rules, or trigger conditions.

Inputs:

```text
data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json
data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/source_artifacts_enriched.json
````

Outputs:

```text
data/output/manual_optisweep_om_v3/stage_4_operational_context/operational_context.json
data/output/manual_optisweep_om_v3/operational_context_extraction_report.json
```

Run:

```bash
python scripts/stage4_extract_operational_context.py \
  --source-bundle data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json \
  --source-artifacts data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/source_artifacts_enriched.json \
  --output-dir data/output/manual_optisweep_om_v3 \
  --llm
```

```

## Acceptance criteria

Stage 4 is complete when:

- `operational_context.json` is created.
- `operational_context_extraction_report.json` is created.
- Output contains roughly 20â€“40 useful context records.
- Records are source-grounded.
- Records include source refs.
- Records reference existing artifact IDs when relevant.
- Heartbeat context is extracted correctly.
- Operator Station HMI context is extracted.
- Hospital HMI context is extracted.
- AGV fault context is extracted.
- No runbooks are created.
- No workflows are created.
- No trigger/routing logic is created.
- No database writes occur.
- Tests pass.

Keep this stage simple. The goal is stable operational knowledge, not procedures yet.
```


