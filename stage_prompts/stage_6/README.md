# Stage 6 Prompts

Shared Stage 6 LLM prompts for both ingestion pipelines.

| File | Used by |
| --- | --- |
| `stage6_operational_runbook_finalization_prompt.md` | `operationalknowledgeingestion` |
| `stage6_incident_runbook_finalization_prompt.md` | `incidenceknowledgeingestion` |
| `stage6_runbook_finalization_structure_reference.md` | Both (appended to system prompt at runtime) |

Loaded by `shared/stage_prompts.py`.
