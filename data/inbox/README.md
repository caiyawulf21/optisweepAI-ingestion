Drop source files here to trigger the LangGraph ingestion agent.

Architecture: [docs/architecture.md](../../docs/architecture.md).  
Orchestration: [orchestration/README.md](../../orchestration/README.md).

```text
incidents/   Case *.pdf
manuals/     operational manuals (*.pdf)
videos/      training recordings (*.mp4) + matching *.vtt
```

Start the watcher (shared Stages 6.5–10 **on by default**; scans files already in the folder):

```powershell
python orchestration/scripts/watch_inbox.py

# Full Cosmos publish too:
python orchestration/scripts/watch_inbox.py --publish-to-cosmos
```

Or run one file immediately:

```powershell
python orchestration/scripts/run_ingestion_agent.py `
  --source "data/inbox/incidents/Case 228086 Data.pdf" `
  --with-publish `
  --publish-to-cosmos `
  --publish-scope all
```

### SharePoint instead of local Explorer drops

Set `SHAREPOINT_SYNC_ROOT` to a OneDrive-synced SharePoint library (see `orchestration/README.md`). Operators upload under that library’s `inbox/…`; SME markdown appears under `review/`.
