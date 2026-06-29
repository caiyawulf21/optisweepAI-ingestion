"""Shared stage directory names for operational knowledge ingestion."""

from __future__ import annotations

from pathlib import Path


STAGE_DIR_NAMES = {
    "1": "stage_1_source_bundle",
    "2": "stage_2_source_artifacts",
    "3": "stage_3_artifact_enrichment",
    "4": "stage_4_operational_context",
    "5": "stage_5_runbook_candidates",
    "6": "stage_6_candidate_pool",
    "7": "stage_7_canonical_runbooks",
    "8": "stage_8_relationship_linking",
    "9": "stage_9_validation_repair",
    "10": "stage_10_final_outputs",
    "11": "stage_11_embeddings",
    "12": "stage_12_knowledge_graph",
}


def stage_dir(output_dir: Path, stage: str) -> Path:
    """Return the stage-scoped output directory for a pipeline output root."""

    return output_dir / STAGE_DIR_NAMES[normalize_stage(stage)]


def normalize_stage(value: str) -> str:
    stage = value.strip().lower().replace("stage_", "").replace("stage", "")
    stage = stage.replace("-", "_")
    if stage in STAGE_DIR_NAMES:
        return stage
    raise ValueError(f"Unsupported stage '{value}'. Supported stages: {', '.join(STAGE_DIR_NAMES)}")
