"""Provider-neutral vision interface. Company policy (see
shared_pipeline_stages/azure_computer_vision.py): Azure Computer Vision is
the only vision backend permitted anywhere in this repo. VisionProvider
exists so callers depend on this interface, not the Azure SDK/REST shape
directly — a future non-Azure implementation would only need to satisfy
this contract, though none is planned.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from shared_pipeline_stages.azure_computer_vision import VisionDescription


class VisionProvider(ABC):
    @abstractmethod
    def gate_artifact(self, image_path: str | Path, criteria: dict) -> bool:
        """Keep/suppress decision for a candidate image artifact."""

    @abstractmethod
    def describe_image(self, image_path: str | Path, prompt: str = "") -> VisionDescription:
        """Caption/tags/objects/OCR-read description of one image."""

    @abstractmethod
    def extract_image_observations(self, image_path: str | Path) -> list[str]:
        """Flat list of textual observations (dense captions + OCR lines) for
        an image, suitable as raw material for extract_evidence."""
