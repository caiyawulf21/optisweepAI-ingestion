from __future__ import annotations

import json

import pytest

from optisweep_incidence_ingestion.stage3_artifact_enrichment import (
    AzureOpenAIIncidentArtifactClient,
    _failed_enrichment_defaults,
    _vision_description_to_dict,
    enrich_one_packet,
)
from shared_pipeline_stages.azure_computer_vision import ImageTag, VisionDescription


class FakeVisionClient:
    def __init__(self, description: VisionDescription | None):
        self._description = description

    def describe(self, image_path):
        return self._description


class FakeEnrichmentLLMClient:
    def __init__(self, response: dict):
        self._response = response

    def enrich(self, packet):
        return self._response


REQUIRED_AZURE_OPENAI_ENV = {
    "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com",
    "AZURE_OPENAI_API_KEY": "fake-key",
    "AZURE_OPENAI_DEPLOYMENT": "fake-deployment",
    "AZURE_OPENAI_API_VERSION": "2024-10-21",
}


def _set_required_env(monkeypatch):
    for key, value in REQUIRED_AZURE_OPENAI_ENV.items():
        monkeypatch.setenv(key, value)


def _description() -> VisionDescription:
    return VisionDescription(
        caption_text="a screenshot of a service status panel",
        caption_confidence=0.88,
        tags=[ImageTag(name="screenshot", confidence=0.95)],
        read_text="Service Status: Running",
        read_confidence=91.2,
    )


def _valid_enrichment_response(artifact_id: str = "a1") -> dict:
    return {
        "artifact_id": artifact_id,
        "short_description": "Service status panel",
        "detailed_description": "Shows the OptiSweep service as running.",
        "visual_observations": ["Green status indicator"],
        "contextual_interpretation": [],
        "source_supported_claims": [],
        "state_assessment": {
            "state": "healthy",
            "confidence": "high",
            "rationale": "Azure Computer Vision read text shows Running.",
            "visible_indicators": [],
            "context_indicators": [],
            "uncertainties": [],
        },
        "evidence_role": "diagnostic_evidence",
        "supports": {"canonical_incident_record": True, "timeline_event": False, "runbook_candidate": False},
        "candidate_support_hints": {"supports_runbook_candidate": False, "support_reason": "", "matched_terms": []},
        "what_to_look_at": ["Status indicator"],
        "ocr_highlights": {},
        "duplicate_analysis": {},
        "review_uncertainty": [],
        "quality_notes": [],
        "tags": [],
        "retrieval_text": "service status running",
        "validation_status": "needs_sme_review",
        "source_refs": [],
    }


def test_include_images_true_raises(monkeypatch):
    _set_required_env(monkeypatch)

    with pytest.raises(ValueError):
        AzureOpenAIIncidentArtifactClient(include_images=True, vision_client=FakeVisionClient(None))


def test_user_content_never_includes_image_url_block(monkeypatch):
    _set_required_env(monkeypatch)
    client = AzureOpenAIIncidentArtifactClient(vision_client=FakeVisionClient(_description()))

    content = client._user_content({"artifact_id": "a1"}, _description())

    assert isinstance(content, str)
    assert "image_url" not in content


def test_user_content_includes_azure_vision_description_fields(monkeypatch):
    _set_required_env(monkeypatch)
    client = AzureOpenAIIncidentArtifactClient(vision_client=FakeVisionClient(_description()))

    content = client._user_content({"artifact_id": "a1"}, _description())
    parsed = json.loads(content)

    vision = parsed["azure_vision_description"]
    assert vision["caption"] == "a screenshot of a service status panel"
    assert vision["tags"] == [{"name": "screenshot", "confidence": 0.95}]
    assert vision["read_text"] == "Service Status: Running"


def test_describe_artifact_image_skips_missing_image_path(monkeypatch, tmp_path):
    _set_required_env(monkeypatch)
    client = AzureOpenAIIncidentArtifactClient(vision_client=FakeVisionClient(_description()))

    assert client._describe_artifact_image({"artifact_id": "a1"}) is None
    assert client._describe_artifact_image({"artifact_id": "a1", "image_path": str(tmp_path / "missing.png")}) is None


def test_describe_artifact_image_writes_audit_json_when_dir_configured(monkeypatch, tmp_path):
    _set_required_env(monkeypatch)
    image_path = tmp_path / "artifact.png"
    image_path.write_bytes(b"fake-image-bytes")
    descriptions_dir = tmp_path / "vision_descriptions"

    client = AzureOpenAIIncidentArtifactClient(
        vision_client=FakeVisionClient(_description()),
        vision_descriptions_dir=descriptions_dir,
    )

    result = client._describe_artifact_image({"artifact_id": "a1", "image_path": str(image_path)})

    assert result is not None
    audit_path = descriptions_dir / "a1.json"
    assert audit_path.exists()
    audit_payload = json.loads(audit_path.read_text(encoding="utf-8"))
    assert audit_payload["caption"] == "a screenshot of a service status panel"


def test_enrich_one_packet_merges_vision_source_metadata():
    packet = {"artifact_id": "a1", "stage2_artifact_record": {}, "source_refs": []}
    llm_client = FakeEnrichmentLLMClient(_valid_enrichment_response())

    merged, error = enrich_one_packet(packet, llm_client)

    assert error is None
    assert merged["enrichment_metadata"]["vision_source"] == "azure_computer_vision_image_analysis"


def test_failed_enrichment_defaults_includes_azure_vision_read_text_key():
    defaults = _failed_enrichment_defaults({"artifact_id": "a1"}, "boom")

    assert "azure_vision_read_text" in defaults["ocr_highlights"]
    assert defaults["ocr_highlights"]["azure_vision_read_text"] == ""
    assert defaults["enrichment_metadata"]["vision_source"] is None


def test_vision_description_to_dict_handles_none():
    assert _vision_description_to_dict(None) is None
