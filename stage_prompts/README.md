# Shared Stage Prompts

Repo-root prompt files used by both ingestion pipelines at runtime.

```text
stage_prompts/
  shared/
    role_component_access_matrix.md
  stage_6/
    stage6_operational_runbook_finalization_prompt.md
    stage6_incident_runbook_finalization_prompt.md
    stage6_runbook_finalization_structure_reference.md
  stage_7/
    stage7_runbook_merge_prompt.md
  stage_8/
    stage8_playbook_linking_prompt.md
```

Resolved by `shared_pipeline_stages/stage_prompts.py`.

Stage 6/7 system prompts append the structure reference and the role/component
access matrix at runtime. Stage 5 runbook/playbook prompts that emit roles
include the same matrix inline.
