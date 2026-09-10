# Ingestion architecture

How OptiSweep ingestion turns manuals, training videos, support guides, incident PDFs, and Brain records into reviewable knowledge and a cumulative Cosmos corpus for the troubleshooting app.

Update this file when architecture changes. See [README_UPDATE.md](README_UPDATE.md). Handoff inventory lives in [HANDOFF.md](HANDOFF.md).
New-owner Azure recreation steps live in [AGENT_AZURE_HANDOFF.md](../AGENT_AZURE_HANDOFF.md).

## Current Architecture

```text
SharePoint library (optional)          local data/inbox/{incidents,manuals,videos}
  inbox/... --poll/sync--+                        |
  review/  <-SME md------+                        |
                         v                        v
                  orchestration (LangGraph watch / one-shot)
                    classify -> source Stages 1-8
                         |
                         v
                  shared_pipeline_stages
                    6.5 pool -> 7 merge -> 8 playbooks -> 8.5 links -> 9 validate -> 10 embed -> 11 publish
                         |
                         v
                  data/output/
                    sme_review/          # human review mirror (+ optional SharePoint review/)
                    cosmos_publish/      # cumulative bundle after gate/smoke
                         |
                         v
                  Azure Cosmos (+ Blob images)
                    newest publish_version_id <- app AUTO_PUBLISH_VERSION=true
```

Source-specific stages stay local and reviewable. Shared Stage 11 is the only path that writes a runtime partition to Cosmos.

| Lane | Stages | Produces |
| --- | --- | --- |
| Incidence | 1-6, 8 | Artifacts, incident record, timeline, runbook/playbook candidates, finalized source runbooks, per-source links |
| Operational | 1-8 | Artifacts, context, runbook candidates, finalized source runbooks, per-source links |
| Shared publish | 6.5-11 | Canonical runbooks, finalized playbooks, corpus links, embeddings, cumulative Cosmos publish |
| Brain | schemas/service/API | Source-agnostic evidence/entity/claim/relationship/capability/procedure/playbook records and app-facing HTTP routes |

## Why The Important Decisions Exist

### Cumulative Stage 11 publish

A thin pilot publish became the newest app corpus and hid previously available cases. Stage 11 now publishes prior corpus plus new or changed work. Dropping a case/playbook without explicit deprecation fails the pre-publish gate, and orchestration defaults to `publish_scope=all`.

Key code: `shared_pipeline_stages/stage_11/corpus_merge.py`, `publish_gate.py`, `cumulative_publish.py`, and orchestration's `publish_cosmos` node.

### Operator-language enrichment

Sparse user speech such as `AGVs stopped` does not match long SME descriptions unless playbooks carry short entry phrases. Stage 8 enriches `support_user_language_examples`, Stage 10 embeds entry-scoped playbook text, and Stage 11 gates/smokes retrieval quality before publishing.

Key code: `shared_pipeline_stages/stage_8/support_language.py`, `shared_pipeline_stages/stage_8/playbook_retrieval.py`, and Stage 11 smoke/gate utilities.

### Versioned gate phrase table

Keyword gating belongs with the same `publish_version_id` as playbooks. Stage 11 emits one `gate_phrases` document per publish into `gate_phrase_tables`; the app loads it on corpus reload and uses local YAML only as fallback.

Contract: `app_handoff_package/GATE_PHRASE_TABLE_CONTRACT.md`.

### Stage 2 incident artifact fallback

Nested screenshots in incident PDFs can be wrapped in chat/feed pages. Stage 2 promotes nested evidence when possible, then falls back to rendered pages/OpenCV crops when wrappers yield no nested artifacts.

Key code: `incidenceknowledgeingestion/src/optisweep_incidence_ingestion/stage2_ocr_artifacts.py`.

### Ontology-grounded Stage 5-8 linking

Ontology capability cards define support contracts for diagnostic/control surfaces, forbidden capability families, prerequisites, WCS availability, and UI-to-WCS mappings. Stage 5 records source-grounded evidence concepts; Stage 8 chooses current support surfaces and attaches only exact-fit runbooks, with honest catalog gaps when no match exists.

Key docs/code: `docs/ontology/`, `shared_pipeline_stages/ontology_rag.py`, `shared_pipeline_stages/stage_8/`.

### Brain layer remains distinct

`brain/`, `brain_service/`, `http_server/`, `mcp_server/`, and `providers/` define the newer source-agnostic Brain contract and service surface. They do not replace the stage pipelines yet; pipeline hooks/adapters are active integration points, and current behavior should be checked in `brain/README.md` and tests.

### Brain relationships are graph-ready, not yet a domain KG

Brain stores typed `Relationship` edges and can traverse them in-process, but the local corpus is dominated by evidence `supports` / citation links rather than a dense OptiSweep domain graph (systems, components, failure patterns, capabilities, procedures). Turning that into a usable domain KG is a curation and extraction problem first: separate provenance from domain edges, freeze a closed taxonomy, emit high-signal edges from Stages 5–8, fix incident relationship writes, promote only approved edges into retrieval/Stage 8 linking, and defer a native graph DB until that subgraph is useful. Next-step sequence: [HANDOFF.md](HANDOFF.md#next-steps-optisweep-domain-knowledge-graph).

## Runtime Contract For The App

1. Load newest publish with embeddings, or pin `PUBLISH_VERSION_ID`.
2. Hybrid retrieve over playbook/runbook embeddings using entry-scoped playbook text.
3. Load `gate_phrases` from `gate_phrase_tables` for the same version; YAML is fallback only.
4. Follow playbook-to-runbook relationship links; resolve images through Blob plus source artifact links.

Do not paper over a thin publish with app-side phrase hardcoding, local sample data, Azure AI Search, or lowered pin thresholds.

## New-Owner Azure Handoff

Azure resources must be reproducible in a new owner's subscription. The
handoff path keeps generated outputs intact and uses them to recreate runtime
state without depending on the previous owner's account:

1. Recreate Cosmos, Blob Storage, Azure OpenAI/embeddings, Azure Computer
   Vision, and optional Brain HTTP hosting from `AGENT_AZURE_HANDOFF.md`.
2. Upload the retained Stage 11 bundle from `data/output/cosmos_publish/` into
   the new Stage 11 app-publish containers.
3. Provision Brain `brain_*` containers and sync retained `brain/data/local/`
   records and embeddings if Brain HTTP or Brain tools should use Azure
   storage.
4. Point the separate OptiSweep Phase 0 app at the new Cosmos endpoint,
   container names, Blob settings, embedding deployment, and
   `PUBLISH_VERSION_ID`.

`HANDOFF_AZURE_BOOTSTRAP.zip` is the portable package at the repo root. It
contains curated publish outputs and Cosmos shape docs; `HANDOFF_DATA_INVENTORY.md`
lists larger retained output trees that may need separate transfer.

## Phase 0 App Boundary

The Phase 0 app lives in a separate codebase. This ingestion repo publishes
Cosmos documents and Brain service contracts; the app consumes them for
retrieval, scoring, UI, and session orchestration.

The app-facing Cosmos surface is the Stage 11 publish set: runbooks, Prompt A/B
playbooks, embeddings, relationship graph shards, operational context, source
artifact RAG records, canonical images, and gate phrase tables. The authoritative
integration docs are in `app_handoff_package/`, especially
`COSMOS_DATA_MAP.md`, `GATE_PHRASE_TABLE_CONTRACT.md`, and
`retrieval/ALGORITHMS.md`.

## Primary READMEs

| Doc | Owns |
| --- | --- |
| [HANDOFF.md](HANDOFF.md) | New-owner inventory and read order |
| [README.md](../README.md) | Repo overview and generated status |
| [orchestration/README.md](../orchestration/README.md) | LangGraph agent, intake, and publish flags |
| [shared_pipeline_stages/README.md](../shared_pipeline_stages/README.md) | Shared 6.5-11 detail |
| [incidenceknowledgeingestion/README.md](../incidenceknowledgeingestion/README.md) | Incident Stages 1-8 |
| [operationalknowledgeingestion/README.md](../operationalknowledgeingestion/README.md) | Operational Stages 1-8 |
| [app_handoff_package/README.md](../app_handoff_package/README.md) | App Cosmos load and gate phrases |
| [brain/README.md](../brain/README.md) | Brain schema/service boundary |
