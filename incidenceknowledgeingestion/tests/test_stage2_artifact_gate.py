from __future__ import annotations

from pathlib import Path

from optisweep_incidence_ingestion.stage2_ocr_artifacts import (
    AzureComputerVisionArtifactGate,
    _gate_metadata,
)
from shared_pipeline_stages.azure_computer_vision import ImageTag, VisionDescription


class FakeVisionClient:
    def __init__(self, description: VisionDescription):
        self._description = description

    def describe(self, image_path):
        return self._description


class RaisingVisionClient:
    def describe(self, image_path):
        raise RuntimeError("Azure Computer Vision is unreachable")


def _description(**overrides) -> VisionDescription:
    defaults = dict(
        caption_text=None,
        caption_confidence=None,
        dense_captions=[],
        tags=[],
        objects=[],
        read_text="",
        read_confidence=None,
    )
    defaults.update(overrides)
    return VisionDescription(**defaults)


def test_azure_cv_gate_keeps_evidence_like_image():
    description = _description(tags=[ImageTag(name="screenshot", confidence=0.95)])
    gate = AzureComputerVisionArtifactGate(vision_client=FakeVisionClient(description))

    decision = gate.decide(
        image_path=Path("artifact.png"),
        candidate_kind="embedded_pdf_image",
        page_number=1,
        ocr={"word_count": 0},
    )

    assert decision.keep is True
    assert decision.category == "attached_evidence_image"


def test_azure_cv_gate_suppresses_high_word_count_no_evidence_tags():
    description = _description(tags=[ImageTag(name="text", confidence=0.7)])
    gate = AzureComputerVisionArtifactGate(vision_client=FakeVisionClient(description))

    decision = gate.decide(
        image_path=Path("artifact.png"),
        candidate_kind="nested_candidate_image",
        page_number=1,
        ocr={"word_count": 60},
    )

    assert decision.keep is False
    assert decision.category == "plain_text_update"


def test_azure_cv_gate_suppresses_empty_vision_result():
    description = _description()
    gate = AzureComputerVisionArtifactGate(vision_client=FakeVisionClient(description))

    decision = gate.decide(
        image_path=Path("artifact.png"),
        candidate_kind="nested_candidate_image",
        page_number=1,
        ocr={"word_count": 0},
    )

    assert decision.keep is False
    assert decision.category == "not_evidence"


def test_azure_cv_gate_fails_open_on_vision_client_error():
    gate = AzureComputerVisionArtifactGate(vision_client=RaisingVisionClient())

    decision = gate.decide(
        image_path=Path("artifact.png"),
        candidate_kind="embedded_pdf_image",
        page_number=1,
        ocr={"word_count": 0},
    )

    assert decision.keep is True
    assert decision.category == "gate_unavailable"


def test_gate_metadata_uses_correct_gate_name_for_azure_cv():
    description = _description(tags=[ImageTag(name="screenshot", confidence=0.95)])
    gate = AzureComputerVisionArtifactGate(vision_client=FakeVisionClient(description))
    decision = gate.decide(
        image_path=Path("artifact.png"),
        candidate_kind="embedded_pdf_image",
        page_number=1,
        ocr={"word_count": 0},
    )

    metadata = _gate_metadata(decision, getattr(gate, "gate_name", "azure_cv"))

    assert metadata["artifact_gate"] == "azure_cv"
    assert metadata["artifact_gate_decision"]["keep"] is True


def test_gate_metadata_none_decision_reports_none():
    assert _gate_metadata(None) == {"artifact_gate": "none"}
