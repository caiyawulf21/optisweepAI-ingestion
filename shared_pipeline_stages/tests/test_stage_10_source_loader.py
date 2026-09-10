from __future__ import annotations

import json
from pathlib import Path

from shared_pipeline_stages.stage_10.source_loader import (
    ARTIFACT_PATHS,
    load_source_roots_contexts_and_artifacts,
)


def _write(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_artifact_paths_cover_incidence_and_operational_layouts() -> None:
    joined = "\n".join(ARTIFACT_PATHS)
    assert "stage_2_ocr_artifacts/source_artifacts.json" in joined
    assert "stage_2_source_artifacts/source_artifacts.json" in joined
    assert "stage_3_artifact_enrichment/source_artifacts_enriched.json" in joined


def test_loads_operational_source_artifacts_layout(tmp_path: Path) -> None:
    root = tmp_path / "training_video_day1"
    _write(
        root / "stage_2_source_artifacts/source_artifacts.json",
        [
            {
                "artifact_id": "artifact_training_video_frame_1",
                "storage_path": "data/output/training_video_day1/images/frame_1.jpg",
            }
        ],
    )
    _contexts, artifacts, warnings = load_source_roots_contexts_and_artifacts([root])
    assert warnings == []
    assert len(artifacts) == 1
    assert artifacts[0]["artifact_id"] == "artifact_training_video_frame_1"
    assert artifacts[0]["source_id"] == "training_video_day1"


def test_loads_incidence_ocr_artifacts_layout(tmp_path: Path) -> None:
    root = tmp_path / "case_228086"
    _write(
        root / "stage_3_artifact_enrichment/source_artifacts_enriched.json",
        [{"artifact_id": "artifact_incident_228086_page_001", "storage_path": "x.png"}],
    )
    _contexts, artifacts, warnings = load_source_roots_contexts_and_artifacts([root])
    assert warnings == []
    assert artifacts[0]["artifact_id"] == "artifact_incident_228086_page_001"


def test_prefers_enriched_over_stage2_when_both_exist(tmp_path: Path) -> None:
    root = tmp_path / "manual_source"
    _write(
        root / "stage_3_artifact_enrichment/source_artifacts_enriched.json",
        [{"artifact_id": "from_stage3"}],
    )
    _write(
        root / "stage_2_source_artifacts/source_artifacts.json",
        [{"artifact_id": "from_stage2"}],
    )
    _contexts, artifacts, _warnings = load_source_roots_contexts_and_artifacts([root])
    assert [a["artifact_id"] for a in artifacts] == ["from_stage3"]


def test_real_training_video_day1_root_is_discoverable() -> None:
    root = (
        Path(__file__).resolve().parents[2]
        / "operationalknowledgeingestion/data/output/training_video_day1"
    )
    if not root.exists():
        return
    _contexts, artifacts, warnings = load_source_roots_contexts_and_artifacts([root])
    assert not any("No source artifacts found" in w for w in warnings)
    assert any(str(a.get("artifact_id", "")).startswith("artifact_training_video_") for a in artifacts)
