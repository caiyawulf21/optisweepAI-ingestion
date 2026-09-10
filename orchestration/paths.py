from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

INBOX_ROOT = REPO_ROOT / "data" / "inbox"
INBOX_INCIDENTS = INBOX_ROOT / "incidents"
INBOX_MANUALS = INBOX_ROOT / "manuals"
INBOX_VIDEOS = INBOX_ROOT / "videos"
INBOX_PROCESSING = INBOX_ROOT / "_processing"
INBOX_PROCESSED = INBOX_ROOT / "_processed"
INBOX_FAILED = INBOX_ROOT / "_failed"

OUTPUT_ROOT = REPO_ROOT / "data" / "output"
OUTPUT_SME_REVIEW = OUTPUT_ROOT / "sme_review"
OUTPUT_COSMOS_PUBLISH = OUTPUT_ROOT / "cosmos_publish"

OPERATIONAL_ROOT = REPO_ROOT / "operationalknowledgeingestion"
INCIDENCE_ROOT = REPO_ROOT / "incidenceknowledgeingestion"
SHARED_ROOT = REPO_ROOT / "shared_pipeline_stages"

OPERATIONAL_SCRIPT = OPERATIONAL_ROOT / "scripts" / "extract_operational_knowledge.py"
INCIDENT_SCRIPT = INCIDENCE_ROOT / "scripts" / "extract_incident_knowledge.py"
TRAINING_STAGE1_SCRIPT = OPERATIONAL_ROOT / "scripts" / "stage1_build_training_video_bundle.py"
TRAINING_STAGE2_SCRIPT = OPERATIONAL_ROOT / "scripts" / "stage2_prepare_training_video_for_extraction.py"

SHARED_SCRIPTS = SHARED_ROOT / "scripts"
SHARED_OUTPUT = SHARED_ROOT / "data" / "output" / "shared"

DEFAULT_INCIDENT_STAGES = "1,2,2.5,3,4,5,6,8"
DEFAULT_OPERATIONAL_STAGES = "1,2,3,4,5,6,8"
# Ingest path includes shared corpus stages through embeddings.
# Stage 11 (Cosmos publish bundle + upload) stays separate.
DEFAULT_SHARED_STAGES = "6.5,7,8,8.5,9,10"


def ensure_inbox_layout() -> None:
    for path in (
        INBOX_INCIDENTS,
        INBOX_MANUALS,
        INBOX_VIDEOS,
        INBOX_PROCESSING,
        INBOX_PROCESSED,
        INBOX_FAILED,
    ):
        path.mkdir(parents=True, exist_ok=True)


def ensure_output_layout() -> None:
    for path in (OUTPUT_ROOT, OUTPUT_SME_REVIEW, OUTPUT_COSMOS_PUBLISH):
        path.mkdir(parents=True, exist_ok=True)


def default_operational_output_dir(source_stem: str) -> Path:
    safe = _slug(source_stem)
    return OPERATIONAL_ROOT / "data" / "output" / safe


def default_incident_output_dir(case_id: str) -> Path:
    return INCIDENCE_ROOT / "data" / "output" / "incidents" / f"case_{case_id}"


def discover_source_roots() -> list[Path]:
    roots: list[Path] = []
    op_output = OPERATIONAL_ROOT / "data" / "output"
    if op_output.exists():
        for child in sorted(op_output.iterdir()):
            if child.is_dir() and (child / "stage_6_finalized_runbooks").exists():
                roots.append(child)
    inc_output = INCIDENCE_ROOT / "data" / "output" / "incidents"
    if inc_output.exists():
        for child in sorted(inc_output.iterdir()):
            if child.is_dir() and (
                (child / "stage_6_finalized_runbooks").exists()
                or (child / "stage_5_runbook_candidates").exists()
            ):
                roots.append(child)
    return roots


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in value.strip())
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_") or "source"
