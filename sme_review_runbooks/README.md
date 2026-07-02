# SME Review Runbooks

Copies of finalized runbook markdown files for easy SME review without navigating pipeline output folders.

Each source folder includes an `assets/` directory with the images referenced by the markdown files (`![](assets/...)`).

These files are snapshots copied from ingestion stage outputs. Edit and approve in the source pipeline outputs; refresh this folder when new runbooks are finalized.

## Sources

| Folder | Origin |
| --- | --- |
| `manual_optisweep_om_v3/` | Operational manual Stage 6 `review_markdown/runbooks/` |
| `training_video_day1/` | Training video Stage 6 `review_markdown/runbooks/` |
| `case_228086/` | Incident Case 228086 Stage 6 finalized runbook + Stage 5 candidate review |
| `case_228723/` | Incident Case 228723 Stage 5 runbook candidate review |

## File Types

- `*.md` in each source root (except `stage_5_runbook_candidates/`) are finalized runbook markdown from `review_markdown/runbooks/`.
- `stage_5_runbook_candidates/runbook_candidate_review.md` is the aggregated Stage 5 candidate review for incident cases.
- Do not use `*_review.md` wrapper files from stage output roots; those are review summaries, not the per-runbook markdown.

## Review Notes

- Each markdown file corresponds to one finalized runbook.
- Default validation status is `needs_sme_review` until explicitly approved.
- For full extraction reports and JSON records, see the source output paths documented in each ingestion area README.

## Refresh

From the repo root:

```powershell
python shared_pipeline_stages/scripts/sync_sme_review_runbooks.py
```
