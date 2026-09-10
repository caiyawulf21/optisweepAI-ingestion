# How to update READMEs (every chat)

Architecture and status docs must stay current. Treat README updates as part of the same change set as code — not a follow-up.

## When to update

Update docs in the **same chat** whenever you:

- Add/change a stage, gate, publish rule, or Cosmos container
- Change retrieval contracts (playbook examples, gate phrases, embed text)
- Fix Stage 2 / image / linking behavior that SMEs or the app depend on
- Land a new publish version or demo finding worth recording

## What to edit

| Change type | Edit these |
| --- | --- |
| Architecture / “why” | `docs/architecture.md` + the area README that owns the stage |
| Shared Stages 6.5–11 | `shared_pipeline_stages/README.md` |
| LangGraph / publish flags | `orchestration/README.md` |
| Incident Stages 1–8 | `incidenceknowledgeingestion/docs/development_status.md` then run its hook |
| Operational Stages 1–6 | `operationalknowledgeingestion` status source + its hook |
| Root status blurb | `docs/development_status.md` then run root hook |
| App Cosmos / phrases | `app_handoff_package/README.md` (+ contract MD if shape changed) |
| Demo session | Append `docs/demo_testing_report.md` |

Keep “why it changed” in `docs/architecture.md`. Keep run commands and file layouts in the area READMEs.

## Hooks (generated sections)

Root README status block:

```powershell
# 1) Edit docs/development_status.md
# 2) Refresh README.md AUTO:DEVELOPMENT_STATUS section
python shared_pipeline_stages/scripts/update_readme.py
```

Incidence README status block:

```powershell
# 1) Edit incidenceknowledgeingestion/docs/development_status.md
# 2) Refresh incidenceknowledgeingestion/README.md
python incidenceknowledgeingestion/scripts/update_readme.py
```

Operational README log (if that area changed):

```powershell
python operationalknowledgeingestion/scripts/update_readme.py
```

Markers look like `<!-- AUTO:DEVELOPMENT_STATUS_START -->` … `_END -->`. Do not hand-edit inside those markers; edit the source `.md` and run the hook.

## Agent checklist (end of chat)

1. Diff what changed → map to the table above.
2. Patch `docs/architecture.md` if behavior or rationale changed.
3. Patch the owning README(s).
4. Patch status source(s) + run the matching `update_readme.py`.
5. Mention in the chat summary which docs were updated.

## Cursor rule

Project rule: `.cursor/rules/readme-architecture-updates.mdc` — agents must follow this every chat that changes pipeline behavior.
