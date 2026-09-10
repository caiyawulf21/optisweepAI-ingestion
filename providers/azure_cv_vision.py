"""Azure Computer Vision implementation of VisionProvider.

Wraps the existing, working clients directly rather than re-deriving their
logic:
- shared_pipeline_stages.azure_computer_vision.AzureComputerVisionDescriptionClient
  for describe_image/extract_image_observations.
- incidenceknowledgeingestion's AzureComputerVisionArtifactGate for
  gate_artifact, since that gate's keep/suppress rule engine (evidence-tag
  scoring, word-count heuristics) already exists and company policy
  requires Azure Computer Vision as the sole vision backend — no reason to
  write a second gate.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from providers.vision import VisionProvider
from shared_pipeline_stages.azure_computer_vision import (
    AzureComputerVisionDescriptionClient,
    VisionDescription,
)


class AzureCVVisionProvider(VisionProvider):
    def __init__(
        self,
        description_client: AzureComputerVisionDescriptionClient | None = None,
        gate_min_confidence: float = 0.55,
    ) -> None:
        self._description_client = description_client or AzureComputerVisionDescriptionClient()
        self._gate_min_confidence = gate_min_confidence
        self._gate: Any | None = None

    def _artifact_gate(self) -> Any:
        if self._gate is None:
            from incidenceknowledgeingestion.src.optisweep_incidence_ingestion.stage2_ocr_artifacts import (
                AzureComputerVisionArtifactGate,
            )

            self._gate = AzureComputerVisionArtifactGate(
                vision_client=self._description_client,
                min_confidence=self._gate_min_confidence,
            )
        return self._gate

    def gate_artifact(self, image_path: str | Path, criteria: dict) -> bool:
        decision = self._artifact_gate().decide(
            image_path=Path(image_path),
            candidate_kind=criteria.get("candidate_kind", "unknown"),
            page_number=criteria.get("page_number", 0),
            ocr=criteria.get("ocr", {}),
            parent_ocr=criteria.get("parent_ocr"),
        )
        return bool(decision.keep)

    def describe_image(self, image_path: str | Path, prompt: str = "") -> VisionDescription:
        return self._description_client.describe(image_path)

    def extract_image_observations(self, image_path: str | Path) -> list[str]:
        description = self._description_client.describe(image_path)
        observations: list[str] = []
        if description.caption_text:
            observations.append(description.caption_text)
        observations.extend(caption.text for caption in description.dense_captions if caption.text)
        if description.read_text:
            observations.extend(line for line in description.read_text.splitlines() if line.strip())
        return observations
