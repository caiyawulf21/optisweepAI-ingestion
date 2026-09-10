# data/output delivery

Assembled handoff for SME review and Cosmos publish.

```text
data/output/
  sme_review/          # same shape as sme_review_runbooks/
  cosmos_publish/      # Stage 11 bundle — push to Cosmos from here
```

## SME review

- `active_agv_error_query_1`: 1 markdown, 6 images
- `manual_optisweep_om_v3`: 225 markdown, 113 images
- `training_video_day1`: 182 markdown, 71 images
- `case_218550`: 3 markdown, 21 images
- `case_223554`: 0 markdown, 37 images
- `case_228086`: 1 markdown, 50 images
- `case_228723`: 0 markdown, 19 images
- `stage_8_playbooks/prompt_a_one_per_incident`: 5 markdown, 88 images
- `stage_8_playbooks/prompt_b_multi_flow`: 7 markdown, 105 images

## Cosmos publish

- Copied: `True`
- Source: `C:\Users\caiyawulf\optisweepAI-ingestion\shared_pipeline_stages\data\output\shared\stage_11_cosmos_publish\cumulative_publish`
- Files: `30`

```powershell
python orchestration/scripts/assemble_output.py
python orchestration/scripts/publish_cosmos_from_output.py
```
