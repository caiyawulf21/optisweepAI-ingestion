Create a new clean Python project scaffold for the OptiSweep data ingestion codebase.

Goal:
This repo is only for the new OptiSweep knowledge/data ingestion pipeline. Do not build the actual ingestion logic yet. Do not implement LangGraph agents yet. Do not connect to Cosmos, PostgreSQL, Azure, SharePoint, Teams, Salesforce, or any runtime assistant code yet.

Right now, only create the project structure, README, placeholder files, and a simple README update hook so the README can stay current as we build.

Project purpose:
This codebase will eventually ingest OptiSweep source material and produce high-quality local JSON outputs:

* source artifacts / images / manual references
* operational context records for retrieval
* reusable runbooks / procedures
* extraction reports

Keep the structure simple and focused on getting the data right.

Create this folder/file structure:

```text
optisweep-ingestion/
  README.md
  pyproject.toml
  .env.example
  .gitignore

  data/
    input/
      manuals/
      incidents/
      slides/
      exports/

    processed/
      source_bundles/

    output/

    review/
      samples/
      validation_reports/

  docs/
    ingestion_plan.md
    data_contracts.md
    development_log.md

  src/
    optisweep_ingestion/
      __init__.py
      main.py

      config/
        __init__.py
        settings.py

      graph/
        __init__.py
        manual_ingestion_graph.py
        graph_state.py
        nodes.py

      agents/
        __init__.py
        manual_knowledge_agent.py

      tools/
        __init__.py
        pdf_parser.py
        docx_parser.py
        source_bundle_builder.py
        artifact_extractor.py
        artifact_enricher.py
        operational_context_extractor.py
        runbook_candidate_extractor.py
        runbook_drafter.py
        relationship_linker.py
        validators.py
        report_writer.py

      prompts/
        master_manual_ingestion_prompt.md
        artifact_enrichment_prompt.md
        operational_context_prompt.md
        runbook_candidate_prompt.md
        runbook_drafting_prompt.md
        relationship_linking_prompt.md
        validation_repair_prompt.md

      schemas/
        __init__.py
        source_bundle.py
        source_artifact.py
        manual_reference.py
        operational_context.py
        runbook.py
        extraction_report.py

      services/
        __init__.py
        llm_client.py
        file_store.py
        id_generator.py
        source_ref_service.py
        image_ref_service.py

      utils/
        __init__.py
        json_utils.py
        text_utils.py
        logging_utils.py

  scripts/
    extract_manual.py
    validate_output.py
    inspect_output.py
    update_readme.py

  tests/
    test_project_structure.py
```

Important:

* Create placeholder Python files with short docstrings only.
* Do not implement real parsing, LLM calls, LangGraph logic, or data extraction yet.
* Placeholder files should make it clear what each module will eventually do.
* Keep comments practical and brief.
* Make the project installable later, but keep dependencies minimal for now.

Set up `pyproject.toml` with:

* project name: `optisweep-ingestion`
* Python version: `>=3.11`
* basic dependencies only:

  * `pydantic`
  * `python-dotenv`
  * `typer`
  * `rich`
* add future/commented optional dependencies section or note for:

  * `langgraph`
  * `langchain-openai`
  * `pymupdf`
  * `pdfplumber`

Create `.env.example` with placeholders:

```text
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=
```

Create `.gitignore` that excludes:

```text
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
data/input/
data/processed/
data/output/
data/review/
```

Create a strong but simple `README.md` with these sections:

1. Project Name
2. Purpose
3. Current Scope
4. Out of Scope For Now
5. Target Outputs
6. Planned Pipeline
7. Folder Structure
8. Development Workflow
9. README Update Hook
10. Current Status

The README should clearly say:

* This repo is focused only on local data ingestion and data quality.
* It does not run the production assistant.
* It does not write to Cosmos or PostgreSQL yet.
* It does not connect to Teams, SharePoint, Salesforce, or Azure storage yet.
* The first target source is the OptiSweep Operation and Maintenance Manual.
* The first proof case will be the heartbeat diagnostic example.
* LangGraph will be used later to orchestrate ingestion stages, but do not implement the graph yet.

Create `docs/ingestion_plan.md` with the planned stage order:

```text
1. Build source bundle
2. Extract source artifacts / images / tables
3. Enrich source artifacts
4. Extract operational context
5. Discover runbook candidates
6. Draft or update runbooks
7. Link artifacts, context, and runbooks
8. Validate outputs
9. Write extraction report
```

Create `docs/data_contracts.md` with brief descriptions of the planned output records:

* SourceBundle
* SourceArtifact
* ManualReference
* OperationalContext
* Runbook
* ExtractionReport

Do not create full schemas yet. Just describe the purpose of each record.

Create `docs/development_log.md` with a simple changelog format:

```markdown
# Development Log

## Unreleased

### Added
- Initial project scaffold.

### Changed
- None yet.

### Decisions
- Keep this repo focused on local ingestion and data quality before database writes.
- Use one future LangGraph pipeline with multiple stage nodes.
```

Create `scripts/update_readme.py`.

This script should be simple. It should:

* read `docs/development_log.md`
* read `docs/ingestion_plan.md`
* update clearly marked sections inside `README.md`
* preserve the rest of the README
* use markers like:

```markdown
<!-- AUTO:INGESTION_PLAN_START -->
...
<!-- AUTO:INGESTION_PLAN_END -->
```

and

```markdown
<!-- AUTO:DEVELOPMENT_LOG_START -->
...
<!-- AUTO:DEVELOPMENT_LOG_END -->
```

Add instructions in the README saying:

```bash
python scripts/update_readme.py
```

should be run after meaningful project changes.

Create `tests/test_project_structure.py`.

This test should verify that the expected key folders/files exist:

* README.md
* pyproject.toml
* docs/ingestion_plan.md
* docs/development_log.md
* scripts/update_readme.py
* src/optisweep_ingestion/
* src/optisweep_ingestion/graph/
* src/optisweep_ingestion/tools/
* src/optisweep_ingestion/schemas/

Do not overbuild the tests.

After creating the scaffold, print a concise summary of what was created and the next recommended step.

Do not implement the real ingestion pipeline yet.
