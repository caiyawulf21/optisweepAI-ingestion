from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_expected_project_structure_exists() -> None:
    expected_paths = [
        "README.md",
        "pyproject.toml",
        "docs/operational_knowledge_pipeline_architecture.md",
        "docs/development_log.md",
        "scripts/update_readme.py",
        "src/optisweep_ingestion",
        "src/optisweep_ingestion/graph",
        "src/optisweep_ingestion/tools",
        "src/optisweep_ingestion/schemas",
    ]

    missing = [path for path in expected_paths if not (ROOT / path).exists()]

    assert missing == []
