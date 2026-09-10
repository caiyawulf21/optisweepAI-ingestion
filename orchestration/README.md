# OptiSweep ingestion orchestration

LangGraph agent that routes uploaded sources into the existing operational,
incidence, and shared publish pipelines.

Architecture: [docs/architecture.md](../docs/architecture.md).  
README updates: [docs/README_UPDATE.md](../docs/README_UPDATE.md).  
Env template: [`.env.example`](../.env.example).

## Happy path (new operators)

```powershell
# 1) Env
copy .env.example .env   # fill Azure OpenAI mini, embeddings, Cosmos, blob

# 2) Deps
pip install -r orchestration/requirements.txt

# 3a) One file end-to-end (shared 6.5-10 + Cosmos)
python orchestration/scripts/run_ingestion_agent.py `
  --source "data/inbox/incidents/Case 228086 Data.pdf" `
  --with-publish `
  --publish-to-cosmos `
  --publish-scope all

# 3b) Watch local inbox (shared publish ON by default; Cosmos opt-in)
python orchestration/scripts/watch_inbox.py --publish-to-cosmos

# 3c) SharePoint-synced library (see SharePoint section below)
$env:SHAREPOINT_SYNC_ROOT="C:\Users\<you>\Contoso\OptiSweep Ingestion - Documents"
python orchestration/scripts/watch_inbox.py --publish-to-cosmos
```

Review outputs land in `data/output/sme_review/` and, when SharePoint is configured, also under `<sync>/review/`.

## Quick start

```powershell
pip install -r orchestration/requirements.txt

# One-shot for a single file (source stages only unless flags set)
python orchestration/scripts/run_ingestion_agent.py `
  --source "data/inbox/incidents/Case 228086 Data.pdf"

# Watch folder mode — shared Stages 6.5-10 run by default
python orchestration/scripts/watch_inbox.py
```

Drop files into:

```text
data/inbox/incidents/   # Case PDFs  -> incidence Stages 1-8
data/inbox/manuals/     # Manual PDFs -> operational Stages 1-8
data/inbox/videos/      # .mp4 + .vtt -> training video Stages 1-2, then 4-6,8
```

Processed files move to `data/inbox/_processed/`. Failures go to `data/inbox/_failed/`.

The watcher **scans files already present** on start (previous versions only reacted to new create events, which often looked like “inbox did nothing”).

## Graph shape

```text
START
  -> classify_source
      -> run_incident | run_manual | run_training_video | fail_unknown
          -> [optional] run_shared_publish   # Stages 6.5-10 (default ON for watch_inbox)
              -> assemble_delivery           # data/output/sme_review (+ cosmos_publish if Stage 11 ran)
                  -> [optional] publish_cosmos   # Stage 11 bundle + upload
                      -> finalize
                          -> END
```

Ingest path = source Stages 1–8 + shared 6.5–10. Stage 11 is Cosmos-only (`--publish-to-cosmos`).
Shared publish always rebuilds Stage **6.5** when Stages 7+ are selected so the runbook pool cannot stay stale after a Stage 6 regen.

## Delivery output (`data/output/`)

After a successful run the orchestrator assembles:

```text
data/output/
  sme_review/          # SME-facing markdown mirror (same shape as sme_review_runbooks/)
  cosmos_publish/      # Stage 11 bundle + manifest + review sheet
```

Cosmos upload always reads from `data/output/cosmos_publish/`, not from scattered stage folders.

```powershell
# Assemble from current corpus (no new ingest)
python orchestration/scripts/assemble_output.py

# Push assembled bundle
python orchestration/scripts/publish_cosmos_from_output.py
```

## Options

| Flag | Meaning |
| --- | --- |
| `--no-llm` | Skip Azure OpenAI-backed stages |
| `--no-publish` | Watch mode: skip shared Stages 6.5-10 (they are **on by default**) |
| `--with-publish` | One-shot agent: run shared 6.5-10 after source Stages 1-8 |
| `--publish-to-cosmos` | Stage 11 bundle + Cosmos upload when `COSMOS_*` env vars are set |
| `--publish-scope` | Prefer `all` (default). Scoped `case:<id>` is blocked for new partitions unless explicitly allowed |
| `--sharepoint-poll-seconds` | Watch mode SharePoint poll interval (default 30) |
| `--no-sharepoint-review` | Do not mirror SME review back to SharePoint |

Recommended publish (cumulative corpus + operator-language enrichment):

```powershell
python orchestration/scripts/run_ingestion_agent.py `
  --source "data/inbox/incidents/Case 228086 Data.pdf" `
  --with-publish `
  --publish-to-cosmos `
  --publish-scope all
```

LangGraph Stage 11: assemble candidate → merge prior Cosmos baseline → enrich `support_user_language_examples` for **all** playbooks → gate → smoke → upload `scope=all`.

Stage 11 also publishes `gate_phrase_tables` (one `gate_phrases` doc per `publish_version_id`). Contract: `app_handoff_package/GATE_PHRASE_TABLE_CONTRACT.md`.

## SharePoint intake + review outbox

Yes — operators can drop files in a SharePoint library and pick up reviewable markdown there.

### Mode A — OneDrive-synced folder (recommended)

1. Sync a SharePoint document library to Windows (OneDrive).
2. Set in `.env`:

```powershell
SHAREPOINT_SYNC_ROOT=C:\Users\<you>\Contoso\OptiSweep Ingestion - Documents
```

3. Create (or let the watcher create) this layout:

```text
SHAREPOINT_SYNC_ROOT/
  inbox/incidents/
  inbox/manuals/
  inbox/videos/
  review/                 # SME markdown mirrored here after each success
  _processed/             # remote files moved after pull
```

4. Run:

```powershell
python orchestration/scripts/watch_inbox.py --publish-to-cosmos
```

One-shot sync without watching:

```powershell
python orchestration/scripts/sync_sharepoint_review.py --pull-inbox --push-review
```

### Mode B — Microsoft Graph app

Register an Entra app with `Sites.Selected` (or `Sites.ReadWrite.All`) + `Files.ReadWrite.All`, grant the site, then set:

```text
SHAREPOINT_TENANT_ID=
SHAREPOINT_CLIENT_ID=
SHAREPOINT_CLIENT_SECRET=
SHAREPOINT_SITE_URL=https://contoso.sharepoint.com/sites/OptiSweep
SHAREPOINT_LIBRARY=Documents
SHAREPOINT_INBOX_FOLDER=inbox
SHAREPOINT_REVIEW_FOLDER=review
```

Same `watch_inbox.py` / `sync_sharepoint_review.py` commands. Graph mode downloads into `data/inbox/` and uploads `data/output/sme_review/` to the remote `review/` folder.

## Package layout

```text
orchestration/
  graph/           LangGraph definition + nodes
  runners/         Thin wrappers around existing stage scripts
  intake/          Local watch folder + SharePoint adapter
  scripts/         CLI entry points
  routing.py       Source-type classification
  state.py         Shared graph state
  paths.py         Repo path helpers
```

## Docs to update when this package changes

Edit this README plus `docs/architecture.md` if publish semantics change, then refresh root status via `python shared_pipeline_stages/scripts/update_readme.py` when milestones move. Checklist: `docs/README_UPDATE.md`.
