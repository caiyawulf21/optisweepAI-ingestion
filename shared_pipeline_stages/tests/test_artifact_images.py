from __future__ import annotations

from pathlib import Path

from shared_pipeline_stages.stage_7.artifact_images import (
    build_review_image_figures,
    resolve_artifact_image_path,
)
from shared_pipeline_stages.stage_7.artifact_loader import load_artifact_index_from_pool


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_resolve_training_video_storage_path() -> None:
    raw = (
        "data\\output\\training_video_day1\\stage_1_source_bundle\\images\\"
        "artifact_training_video_training_video_day1_0063_do_you_have_any_system_faults_primary_02_15_57_000.jpg"
    )
    resolved = resolve_artifact_image_path(raw, repo_root=REPO_ROOT)
    assert resolved is not None
    assert resolved.is_file()


def test_resolve_incident_storage_path() -> None:
    raw = (
        "incidenceknowledgeingestion\\data\\output\\incidents\\case_228086\\"
        "stage_2_ocr_artifacts\\images\\embedded\\artifact_incident_228086_page_003_embedded_image_01.jpeg"
    )
    resolved = resolve_artifact_image_path(raw, repo_root=REPO_ROOT)
    assert resolved is not None
    assert resolved.is_file()


def test_build_review_image_figures_copies_asset(tmp_path: Path) -> None:
    pool_dir = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool"
    if not (pool_dir / "runbook_pool.json").is_file():
        return
    artifact_index = load_artifact_index_from_pool(pool_dir)
    artifact_id = "artifact_training_video_training_video_day1_0063_do_you_have_any_system_faults_primary_02_15_57_000"
    if artifact_id not in artifact_index:
        return
    review_path = tmp_path / "playbook.html"
    figures = build_review_image_figures(
        [{"artifact_id": artifact_id, "what_to_look_at": "Overall System RMS page"}],
        artifact_index=artifact_index,
        review_output_path=review_path,
        repo_root=REPO_ROOT,
    )
    assert len(figures) == 1
    assert figures[0].found is True
    assert figures[0].src.startswith("assets/")
    copied = tmp_path / "assets"
    assert copied.is_dir()
    assert any(copied.iterdir())
