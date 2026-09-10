from __future__ import annotations

import json
import urllib.error

import pytest

from shared_pipeline_stages.azure_computer_vision import (
    AzureComputerVisionDescriptionClient,
    azure_cv_min_interval_sec,
    post_image_bytes_with_retry,
)


def _client() -> AzureComputerVisionDescriptionClient:
    return AzureComputerVisionDescriptionClient(
        endpoint="https://example.cognitiveservices.azure.com",
        api_key="fake-key",
        api_version="2023-10-01",
    )


def test_vision_description_parses_full_payload(tmp_path):
    payload = {
        "captionResult": {"text": "a screenshot of a control panel", "confidence": 0.91},
        "denseCaptionsResult": {
            "values": [
                {"text": "a dialog box", "confidence": 0.5, "boundingBox": {"x": 0, "y": 0, "w": 10, "h": 10}}
            ]
        },
        "tagsResult": {"values": [{"name": "screenshot", "confidence": 0.99}]},
        "objectsResult": {
            "values": [
                {"tags": [{"name": "monitor", "confidence": 0.8}], "boundingBox": {"x": 1, "y": 1, "w": 2, "h": 2}}
            ]
        },
        "readResult": {
            "blocks": [
                {
                    "lines": [
                        {
                            "text": "Service Status: Running",
                            "boundingPolygon": [],
                            "words": [{"text": "Service", "confidence": 0.9}, {"text": "Status:", "confidence": 0.95}],
                        }
                    ]
                }
            ]
        },
    }
    client = _client()
    image_path = tmp_path / "artifact.png"
    image_path.write_bytes(b"fake-image-bytes")

    description = client._parse(payload, image_path)

    assert description.caption_text == "a screenshot of a control panel"
    assert description.caption_confidence == 0.91
    assert len(description.dense_captions) == 1
    assert description.dense_captions[0].text == "a dialog box"
    assert len(description.tags) == 1
    assert description.tags[0].name == "screenshot"
    assert len(description.objects) == 1
    assert description.objects[0].name == "monitor"
    assert description.objects[0].confidence == 0.8
    assert description.read_text == "Service Status: Running"
    assert description.read_confidence == pytest.approx(92.5, rel=1e-3)
    assert description.provenance["backend"] == "azure_computer_vision_image_analysis"
    assert description.provenance["source_image_path"] == str(image_path)


def test_vision_description_parses_missing_sections_gracefully(tmp_path):
    client = _client()
    image_path = tmp_path / "artifact.png"
    image_path.write_bytes(b"fake-image-bytes")

    description = client._parse({}, image_path)

    assert description.caption_text is None
    assert description.caption_confidence is None
    assert description.dense_captions == []
    assert description.tags == []
    assert description.objects == []
    assert description.read_text == ""
    assert description.read_confidence is None


def test_post_image_bytes_with_retry_retries_on_429(monkeypatch):
    calls = {"count": 0}

    class FakeHTTPResponse:
        def __init__(self, body: bytes):
            self._body = body

        def read(self):
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, *exc_info):
            return False

    def fake_urlopen(request, timeout):
        calls["count"] += 1
        if calls["count"] == 1:
            raise urllib.error.HTTPError(
                url="https://example.com",
                code=429,
                msg="Too Many Requests",
                hdrs={"Retry-After": "0"},
                fp=None,
            )
        return FakeHTTPResponse(json.dumps({"ok": True}).encode("utf-8"))

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    monkeypatch.setenv("AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC", "0")

    result = post_image_bytes_with_retry(
        "https://example.com/analyze",
        {"Content-Type": "application/octet-stream"},
        b"fake-bytes",
        max_attempts=3,
    )

    assert result == {"ok": True}
    assert calls["count"] == 2


def test_azure_cv_min_interval_sec_reads_env_default_and_override(monkeypatch):
    monkeypatch.delenv("AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC", raising=False)
    assert azure_cv_min_interval_sec() == 3.5

    monkeypatch.setenv("AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC", "1.25")
    assert azure_cv_min_interval_sec() == 1.25

    monkeypatch.setenv("AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC", "not-a-number")
    assert azure_cv_min_interval_sec() == 3.5
