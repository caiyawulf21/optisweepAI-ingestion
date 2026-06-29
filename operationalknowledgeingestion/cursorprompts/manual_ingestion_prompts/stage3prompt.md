Complete Stage 3 of the OptiSweep ingestion pipeline: **LLM Source Artifact Enrichment**.

Stage 1 and Stage 2 are already complete.

Current inputs:

```text
data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json
data/output/manual_optisweep_om_v3/stage_2_source_artifacts/source_artifacts.json
data/output/manual_optisweep_om_v3/stage_2_source_artifacts/artifact_extraction_report.json
```

Stage 3 should use an LLM to enrich the extracted source artifacts so they are easier to use in later operational context and runbook extraction.

Keep this simple.

Do not overbuild classification, validation, routing, workflows, or complex review logic.

## Goal

Read each source artifact and add a small set of useful enrichment fields:

```text
short_description
detailed_description
what_to_look_at
tags
retrieval_text
enrichment_notes
```

Write:

```text
data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/source_artifacts_enriched.json
data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/artifact_enrichment_report.json
```

Do not overwrite the original `source_artifacts.json`.

## Important rules

Do not create operational context records yet.

Do not create runbooks yet.

Do not create workflows.

Do not populate these fields yet:

```text
linked_context_ids
linked_runbook_ids
linked_procedure_ids
```

Leave them as empty lists.

Do not invent visual details. The LLM should only use:

```text
title
caption_text
nearby_text
image_type
page_number
section_id
source_refs
extraction_metadata
```

The image file exists, but for now the LLM does not need to inspect the image visually unless the current project already supports that cleanly.

Source text is the source of truth.

## Keep the enrichment schema simple

Update the source artifact schema only if needed.

Add these optional fields:

```python
short_description: str | None = None
detailed_description: str | None = None
what_to_look_at: list[str] = []
tags: list[str] = []
retrieval_text: str | None = None
enrichment_notes: list[str] = []
```

Do not add a large taxonomy yet.

Do not add lots of separate tag fields yet.

One simple `tags` list is enough for now.

Example tags:

```text
operator_station
hospital_station
system_hmi
operator_hmi
hospital_hmi
agv
rms
wcs
tipper
heartbeat
alarm
add_tote
remove_tote
fault_recovery
maintenance
scanner
stacklight
```

## LLM prompt behavior

Create:

```text
src/optisweep_ingestion/prompts/stage3_artifact_enrichment_prompt.md
```

Prompt:

```markdown
# OptiSweep Source Artifact Enrichment Prompt

You enrich source artifact records extracted from the OptiSweep Operation and Maintenance Manual.

Your job is to make each artifact useful for later retrieval, operational context extraction, and runbook extraction.

You do not create operational context records.
You do not create runbooks.
You do not create workflows.
You do not populate linked_context_ids, linked_runbook_ids, or linked_procedure_ids.

Use only the provided artifact fields:
- title
- caption_text
- nearby_text
- image_type
- page_number
- section_id
- source_refs
- extraction_metadata

Do not invent visual details that are not supported by the caption or nearby text.

Return JSON only with these fields:
{
  "short_description": "",
  "detailed_description": "",
  "what_to_look_at": [],
  "tags": [],
  "retrieval_text": "",
  "enrichment_notes": []
}

Field guidance:

short_description:
A one-sentence description of what this artifact is.

detailed_description:
A source-grounded paragraph explaining what the artifact represents and why it may be useful.

what_to_look_at:
A short list of fields, controls, areas, values, buttons, alarms, statuses, or components that a support user should inspect.

tags:
Simple lowercase tags useful for retrieval.

retrieval_text:
A rich search-friendly paragraph combining the title, source page, section, important terms, and nearby source facts.

enrichment_notes:
Use this only for uncertainty, missing context, low-confidence visual matching, or if the artifact may need human review.
```

## Implementation

Create or update:

```text
src/optisweep_ingestion/tools/artifact_enricher.py
scripts/stage3_enrich_source_artifacts.py
tests/test_artifact_enricher.py
```

The script should:

1. Load `source_artifacts.json`.
2. Load `artifact_extraction_report.json`.
3. For each artifact, send a compact artifact packet to the LLM.
4. Merge the returned enrichment fields back into the artifact.
5. Preserve all existing fields.
6. Preserve source refs exactly.
7. Preserve artifact IDs exactly.
8. Keep linked context/runbook/procedure IDs empty.
9. Write `source_artifacts_enriched.json`.
10. Write `artifact_enrichment_report.json`.

## CLI

Create:

```text
scripts/stage3_enrich_source_artifacts.py
```

Use Typer if the repo already uses Typer.

Example command:

```bash
python scripts/stage3_enrich_source_artifacts.py \
  --source-artifacts data/output/manual_optisweep_om_v3/stage_2_source_artifacts/source_artifacts.json \
  --artifact-report data/output/manual_optisweep_om_v3/stage_2_source_artifacts/artifact_extraction_report.json \
  --output-dir data/output/manual_optisweep_om_v3 \
  --llm
```

For this stage, `--llm` is expected.

If the LLM client is not configured, fail clearly with a helpful error message.

Do not silently fall back to fake enrichment.

## Enrichment report

Write a simple report:

```json
{
  "input_artifact_count": 127,
  "enriched_artifact_count": 127,
  "llm_used": true,
  "failed_artifact_count": 0,
  "failed_artifacts": [],
  "priority_artifact_check": {
    "fig_4_20": {
      "artifact_found": true,
      "enriched": true,
      "has_what_to_look_at": true,
      "has_retrieval_text": true
    },
    "fig_4_22": {
      "artifact_found": true,
      "enriched": true,
      "has_what_to_look_at": true,
      "has_retrieval_text": true
    },
    "fig_4_28": {
      "artifact_found": true,
      "enriched": true,
      "has_what_to_look_at": true,
      "has_retrieval_text": true
    },
    "fig_4_30": {
      "artifact_found": true,
      "enriched": true,
      "has_what_to_look_at": true,
      "has_retrieval_text": true
    },
    "fig_4_31": {
      "artifact_found": true,
      "enriched": true,
      "has_what_to_look_at": true,
      "has_retrieval_text": true
    },
    "fig_4_32": {
      "artifact_found": true,
      "enriched": true,
      "has_what_to_look_at": true,
      "has_retrieval_text": true
    },
    "fig_5_2": {
      "artifact_found": true,
      "enriched": true,
      "has_what_to_look_at": true,
      "has_retrieval_text": true
    },
    "fig_5_4": {
      "artifact_found": true,
      "enriched": true,
      "has_what_to_look_at": true,
      "has_retrieval_text": true
    }
  },
  "heartbeat_check": {
    "figure_id": "fig_4_22",
    "artifact_found": true,
    "enriched": true,
    "retrieval_text_contains_heartbeat": true,
    "retrieval_text_contains_last": true,
    "retrieval_text_contains_max": true,
    "retrieval_text_contains_min": true,
    "retrieval_text_contains_10_seconds": true
  }
}
```

Keep this report simple.

## Priority artifacts

Make sure these are checked in the report:

```text
fig_4_20
fig_4_22
fig_4_28
fig_4_30
fig_4_31
fig_4_32
fig_5_2
fig_5_4
```

## Heartbeat artifact expectations

For `fig_4_22`, the enriched result should include:

```text
Heartbeat
Last
Max
Min
10 seconds
tipper
WCS
mis-synchronization
```

The `what_to_look_at` should include:

```text
Heartbeat section
Last value
Max value
Min value
RESET button
```

## Tests

Keep tests lightweight.

Add tests for:

1. LLM response parsing.
2. Merging enrichment fields into an artifact without deleting existing fields.
3. Preserving `artifact_id`.
4. Preserving `source_refs`.
5. Keeping linked IDs empty.
6. Heartbeat check logic.
7. Priority artifact report logic.

Do not require a real LLM call in unit tests. Mock the LLM response.

## README update

Add a simple Stage 3 section:

````markdown
## Current Stage: Stage 3 â€” LLM Source Artifact Enrichment

Stage 3 uses an LLM to enrich extracted source artifact records with descriptions, what-to-look-at guidance, tags, and retrieval text.

Inputs:

```text
data/output/manual_optisweep_om_v3/stage_2_source_artifacts/source_artifacts.json
data/output/manual_optisweep_om_v3/stage_2_source_artifacts/artifact_extraction_report.json
````

Outputs:

```text
data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/source_artifacts_enriched.json
data/output/manual_optisweep_om_v3/stage_3_artifact_enrichment/artifact_enrichment_report.json
```

Run:

```bash
python scripts/stage3_enrich_source_artifacts.py \
  --source-artifacts data/output/manual_optisweep_om_v3/stage_2_source_artifacts/source_artifacts.json \
  --artifact-report data/output/manual_optisweep_om_v3/stage_2_source_artifacts/artifact_extraction_report.json \
  --output-dir data/output/manual_optisweep_om_v3 \
  --llm
```

This stage does not create operational context, runbooks, workflows, or relationship links.

```

## Acceptance criteria

Stage 3 is complete when:

- `source_artifacts_enriched.json` is created.
- `artifact_enrichment_report.json` is created.
- Every artifact keeps its original fields.
- Every artifact has:
  - short_description
  - detailed_description
  - what_to_look_at
  - tags
  - retrieval_text
- Source refs are preserved.
- Artifact IDs are preserved.
- Linked context/runbook/procedure IDs remain empty.
- Priority artifacts are enriched.
- Heartbeat artifact includes Heartbeat, Last, Max, Min, and 10 seconds.
- No operational context records are created.
- No runbooks are created.
- No workflows are created.
- Tests pass.

Keep this stage simple. The purpose is only to make source artifacts more useful for the next extraction stage.
```


