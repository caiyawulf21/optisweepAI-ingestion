$ErrorActionPreference = "Stop"
Set-Location "C:\Users\caiyawulf\optisweepAI-ingestion"
$env:PYTHONUNBUFFERED = "1"

$SharedOut = "shared_pipeline_stages\data\output\shared"
$Sources65 = @(
  "operationalknowledgeingestion\data\output\manual_optisweep_om_v3",
  "operationalknowledgeingestion\data\output\training_video_day1",
  "incidenceknowledgeingestion\data\output\incidents\case_218550",
  "incidenceknowledgeingestion\data\output\incidents\case_228086"
)
$Sources85 = $Sources65 + @(
  "incidenceknowledgeingestion\data\output\incidents\case_228723"
)
$Sources11 = $Sources85

function Invoke-Stage {
  param([string]$Name, [string[]]$CommandArgs)
  Write-Host ""
  Write-Host "======== $Name ========" -ForegroundColor Cyan
  Write-Host ("python " + ($CommandArgs -join " "))
  & python @CommandArgs
  if ($LASTEXITCODE -ne 0) {
    throw "Stage failed: $Name (exit $LASTEXITCODE)"
  }
  Write-Host "======== $Name OK ========" -ForegroundColor Green
}

$src65Args = @()
foreach ($s in $Sources65) { $src65Args += @("--source-root", $s) }

Invoke-Stage "Shared 6.5 runbook pool" (@(
  "shared_pipeline_stages\scripts\stage6_5_build_runbook_pool.py"
) + $src65Args + @("--output-dir", $SharedOut))

Invoke-Stage "Shared 7 merge runbooks" @(
  "shared_pipeline_stages\scripts\stage7_merge_runbooks.py",
  "--pool-dir", "$SharedOut\stage_6_5_runbook_pool",
  "--output-dir", $SharedOut,
  "--llm"
)

Invoke-Stage "Shared 8 finalize playbooks" @(
  "shared_pipeline_stages\scripts\stage8_finalize_playbooks.py",
  "--pool-dir", "$SharedOut\stage_6_5_runbook_pool",
  "--stage7-dir", "$SharedOut\stage_7_merged_runbooks",
  "--incidents-root", "incidenceknowledgeingestion\data\output\incidents",
  "--output-dir", $SharedOut,
  "--case-id", "218550",
  "--case-id", "228086",
  "--case-id", "228723",
  "--llm"
)

$src85Args = @()
foreach ($s in $Sources85) { $src85Args += @("--source-root", $s) }

Invoke-Stage "Shared 8.5 corpus links" (@(
  "shared_pipeline_stages\scripts\stage8_5_link_relationships.py"
) + $src85Args + @(
  "--stage7-dir", "$SharedOut\stage_7_merged_runbooks",
  "--stage8-dir", "$SharedOut\stage_8_finalized_playbooks",
  "--output-dir", $SharedOut
))

Invoke-Stage "Shared 9 validate corpus" @(
  "shared_pipeline_stages\scripts\stage9_validate_corpus.py",
  "--stage7-dir", "$SharedOut\stage_7_merged_runbooks",
  "--stage8-dir", "$SharedOut\stage_8_finalized_playbooks",
  "--stage85-dir", "$SharedOut\stage_8_5_relationship_linking",
  "--output-dir", $SharedOut
)

Invoke-Stage "Shared 10 embeddings" @(
  "shared_pipeline_stages\scripts\stage10_generate_embeddings.py",
  "--stage7-dir", "$SharedOut\stage_7_merged_runbooks",
  "--stage8-dir", "$SharedOut\stage_8_finalized_playbooks",
  "--output-dir", $SharedOut
)

$src11Args = @()
foreach ($s in $Sources11) { $src11Args += @("--source-root", $s) }

Invoke-Stage "Shared 11 cosmos publish bundle" (@(
  "shared_pipeline_stages\scripts\stage11_publish_cosmos.py",
  "--stage7-dir", "$SharedOut\stage_7_merged_runbooks",
  "--stage8-dir", "$SharedOut\stage_8_finalized_playbooks",
  "--stage10-dir", "$SharedOut\stage_10_embeddings",
  "--stage85-dir", "$SharedOut\stage_8_5_relationship_linking",
  "--stage9-dir", "$SharedOut\stage_9_validation",
  "--output-dir", $SharedOut
) + $src11Args + @("--publish"))

Write-Host ""
Write-Host "All shared stages completed." -ForegroundColor Green
