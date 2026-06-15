# OptiSweep Ingestion

## Project Name

`optisweep-ingestion`

## Purpose

This repo is focused only on local OptiSweep data ingestion and data quality. It will eventually turn source material into clean local JSON outputs that can be reviewed before any production system or database is involved.

The first target source is the OptiSweep Operation and Maintenance Manual. The first proof case will be the heartbeat diagnostic example.

## Current Scope

- Organize source material for local ingestion.
- Define the planned output records.
- Prepare a clean Python project structure.
- Track the intended ingestion stages.
- Keep the README current as the project evolves.

## Current Stage: Stage 1 - Source Bundle

The current implementation builds a deterministic source bundle from a PDF manual.

Output:

```text
data/output/manual_optisweep_om_v3/source_bundle.json
```

Run:

```bash
python scripts/extract_manual.py \
  --source-pdf "data/input/manuals/OptiSweep Operation and Maintenance Manual - Final 1.pdf" \
  --output-dir data/output/manual_optisweep_om_v3
```

This stage does not use an LLM and does not extract actual images yet.

Stage 1 now includes quality checks for:
- conservative section heading detection
- front matter filtering
- canonical figure/table reference selection
- heartbeat detectability smoke checks

## Out of Scope For Now

- Running the production assistant.
- Writing to Cosmos or PostgreSQL.
- Connecting to Teams, SharePoint, Salesforce, Azure storage, or other runtime services.
- Implementing real parsing, LLM calls, data extraction, or LangGraph agents.

## Target Outputs

- Source artifacts, images, and manual references.
- Operational context records for retrieval.
- Reusable runbooks and procedures.
- Extraction reports.

## Planned Pipeline

LangGraph will be used later to orchestrate ingestion stages, but the graph is not implemented yet.

<!-- AUTO:INGESTION_PLAN_START -->
# Ingestion Plan

1. Build source bundle
2. Extract source artifacts / images / tables
3. Enrich source artifacts
4. Extract operational context
5. Discover runbook candidates
6. Draft or update runbooks
7. Link artifacts, context, and runbooks
8. Validate outputs
9. Write extraction report
<!-- AUTO:INGESTION_PLAN_END -->

## Folder Structure

```text
.
  README.md
  pyproject.toml
  .env.example
  .gitignore
  data/
    input/
    processed/
    output/
    review/
  docs/
  scripts/
  src/
    optisweep_ingestion/
  tests/
```

## Development Workflow

1. Add source files under `data/input/`.
2. Keep planned contracts and decisions in `docs/`.
3. Add ingestion code under `src/optisweep_ingestion/` only when the design is ready.
4. Write local JSON outputs under `data/output/`.
5. Review samples and validation reports under `data/review/`.

## README Update Hook

Run the README update hook after meaningful project changes:

```bash
python scripts/update_readme.py
```

The hook refreshes the marked pipeline and development log sections while preserving the rest of this README.

## Current Status

Stage 1 source bundle extraction is implemented. Later ingestion stages remain placeholders.

<!-- AUTO:DEVELOPMENT_LOG_START -->
# Development Log

## Unreleased

### Added
- Initial project scaffold.

### Changed
- None yet.

### Decisions
- Keep this repo focused on local ingestion and data quality before database writes.
- Use one future LangGraph pipeline with multiple stage nodes.
<!-- AUTO:DEVELOPMENT_LOG_END -->
