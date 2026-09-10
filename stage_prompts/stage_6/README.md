# Stage 6 Prompts

Shared Stage 6 LLM prompts for both ingestion pipelines.

| File | Used by |
| --- | --- |
| `stage6_operational_runbook_finalization_prompt.md` | `operationalknowledgeingestion` |
| `stage6_incident_runbook_finalization_prompt.md` | `incidenceknowledgeingestion` |
| `stage6_runbook_finalization_structure_reference.md` | Both (appended to system prompt at runtime) |

Also appended at runtime for Stage 6/7: `../shared/role_component_access_matrix.md`.
Stage 6 also appends the frozen capability taxonomy IDs (`capability_tags`, `access_surface`, `audience_roles`, `failure_pattern_tags`) from `docs/ontology/taxonomy/`.

Loaded by `shared_pipeline_stages/stage_prompts.py`.
