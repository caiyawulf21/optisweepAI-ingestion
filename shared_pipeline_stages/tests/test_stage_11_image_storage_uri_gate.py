from __future__ import annotations

import pytest

from shared_pipeline_stages.stage_11.corpus_merge import _merge_canonical_images, _merge_image_row
from shared_pipeline_stages.stage_11.image_blob_publisher import (
    assert_canonical_images_renderable,
    canonical_images_missing_storage_uri,
)


def test_merge_image_row_keeps_baseline_https_uri() -> None:
    baseline = {
        "id": "image_a",
        "image_id": "artifact_a",
        "storage_uri": "https://example.test/a.jpg?sas=1",
        "blob_path": "publish_old/artifact_a.jpg",
        "title": "old title",
    }
    candidate = {
        "id": "image_a",
        "image_id": "artifact_a",
        "storage_uri": "",
        "blob_path": "publish_new/artifact_a.jpg",
        "title": "new title",
    }
    merged = _merge_image_row(baseline, candidate)
    assert merged["title"] == "new title"
    assert merged["storage_uri"].startswith("https://")
    assert merged["blob_path"] == "publish_old/artifact_a.jpg"


def test_merge_canonical_images_prefers_renderable_uri() -> None:
    baseline = [
        {
            "id": "image_a",
            "image_id": "artifact_a",
            "storage_uri": "https://example.test/a.jpg",
            "blob_path": "old/a.jpg",
        }
    ]
    candidate = [
        {
            "id": "image_a",
            "image_id": "artifact_a",
            "storage_uri": "",
            "blob_path": "new/a.jpg",
            "title": "updated",
        }
    ]
    merged, kept, added = _merge_canonical_images(
        candidate,
        baseline,
        publish_version_id="publish_next",
    )
    assert kept == 1
    assert added == 0
    assert len(merged) == 1
    assert merged[0]["publish_version_id"] == "publish_next"
    assert merged[0]["storage_uri"].startswith("https://")
    assert merged[0]["title"] == "updated"


def test_assert_canonical_images_renderable_fails_on_empty_uri() -> None:
    with pytest.raises(ValueError, match="storage_uri"):
        assert_canonical_images_renderable(
            [{"image_id": "artifact_a", "storage_uri": "", "blob_path": "x/a.jpg"}]
        )


def test_canonical_images_missing_storage_uri() -> None:
    missing = canonical_images_missing_storage_uri(
        [
            {"image_id": "ok", "storage_uri": "https://example.test/ok.jpg"},
            {"image_id": "bad", "storage_uri": ""},
        ]
    )
    assert missing == ["bad"]
