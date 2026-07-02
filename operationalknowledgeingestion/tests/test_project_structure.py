from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_expected_project_structure_exists() -> None:
    expected_paths = [
        "README.md",
        "pyproject.toml",
        "docs/operational_knowledge_pipeline_architecture.md",
        "docs/development_log.md",
        "scripts/extract_operational_knowledge.py",
        "scripts/stage1_extract_source_bundle.py",
        "scripts/stage2_extract_source_artifacts.py",
        "scripts/stage3_enrich_source_artifacts.py",
        "scripts/stage4_extract_operational_context.py",
        "scripts/stage5_extract_runbook_candidates.py",
        "scripts/stage6_finalize_runbooks.py",
        "scripts/stage6_5_build_runbook_pool.py",
        "scripts/update_readme.py",
        "src/optisweep_ingestion",
        "src/optisweep_ingestion/stage_paths.py",
        "src/optisweep_ingestion/stage1_source_bundle.py",
        "src/optisweep_ingestion/stage2_source_artifacts.py",
        "src/optisweep_ingestion/stage3_artifact_enrichment.py",
        "src/optisweep_ingestion/stage4_operational_context.py",
        "src/optisweep_ingestion/stage5_runbook_candidates.py",
        "src/optisweep_ingestion/stage6_runbook_finalization.py",
        "src/optisweep_ingestion/stage6_5_runbook_pool.py",
        "src/optisweep_ingestion/graph",
        "src/optisweep_ingestion/tools",
        "src/optisweep_ingestion/schemas",
        "src/optisweep_ingestion/prompts/stage3_artifact_enrichment_prompt.md",
        "src/optisweep_ingestion/prompts/stage4_operational_context_extraction_prompt.md",
        "src/optisweep_ingestion/prompts/stage5_runbook_candidate_discovery_prompt.md",
        "../stage_prompts/stage_6/stage6_operational_runbook_finalization_prompt.md",
        "../stage_prompts/stage_6/stage6_runbook_finalization_structure_reference.md",
    ]

    missing = [path for path in expected_paths if not (ROOT / path).exists()]

    assert missing == []


def test_stage_script_names_are_numbered() -> None:
    exempt = {"extract_operational_knowledge.py", "update_readme.py"}
    scripts = [
        path.name
        for path in (ROOT / "scripts").glob("*.py")
        if path.name not in exempt and not path.name.startswith("__")
    ]

    unlabeled = [name for name in scripts if not name.startswith("stage")]

    assert unlabeled == []
