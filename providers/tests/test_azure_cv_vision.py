from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

from shared_pipeline_stages.azure_computer_vision import DenseCaption, VisionDescription
from providers.azure_cv_vision import AzureCVVisionProvider


def _fake_description(
    caption_text: str = "a screenshot of a control panel",
    dense_captions: list[str] | None = None,
    read_text: str = "",
) -> VisionDescription:
    return VisionDescription(
        caption_text=caption_text,
        caption_confidence=0.9,
        dense_captions=[DenseCaption(text=text, confidence=0.8) for text in (dense_captions or [])],
        tags=[],
        objects=[],
        read_text=read_text,
        read_confidence=None,
    )


def test_describe_image_passes_through_client_result(tmp_path: Path) -> None:
    fake_client = MagicMock()
    fake_client.describe.return_value = _fake_description()
    provider = AzureCVVisionProvider(description_client=fake_client)

    image_path = tmp_path / "fake.png"
    result = provider.describe_image(image_path)

    fake_client.describe.assert_called_once_with(image_path)
    assert result.caption_text == "a screenshot of a control panel"


def test_extract_image_observations_combines_caption_dense_captions_and_ocr(tmp_path: Path) -> None:
    fake_client = MagicMock()
    fake_client.describe.return_value = _fake_description(
        caption_text="main caption",
        dense_captions=["a dense caption"],
        read_text="line one\nline two",
    )
    provider = AzureCVVisionProvider(description_client=fake_client)

    observations = provider.extract_image_observations(tmp_path / "fake.png")

    assert observations == ["main caption", "a dense caption", "line one", "line two"]


def test_extract_image_observations_handles_empty_description(tmp_path: Path) -> None:
    fake_client = MagicMock()
    fake_client.describe.return_value = _fake_description(caption_text=None, dense_captions=[], read_text="")
    provider = AzureCVVisionProvider(description_client=fake_client)

    assert provider.extract_image_observations(tmp_path / "fake.png") == []


def test_gate_artifact_delegates_to_artifact_gate(monkeypatch, tmp_path: Path) -> None:
    fake_client = MagicMock()
    provider = AzureCVVisionProvider(description_client=fake_client)

    fake_gate = MagicMock()
    fake_gate.decide.return_value = MagicMock(keep=True)
    monkeypatch.setattr(provider, "_artifact_gate", lambda: fake_gate)

    kept = provider.gate_artifact(
        tmp_path / "fake.png",
        criteria={"candidate_kind": "screenshot", "page_number": 1, "ocr": {"word_count": 5}},
    )

    assert kept is True
    fake_gate.decide.assert_called_once()
    _, kwargs = fake_gate.decide.call_args
    assert kwargs["candidate_kind"] == "screenshot"
    assert kwargs["page_number"] == 1
