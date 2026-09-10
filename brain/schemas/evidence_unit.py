from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from brain.schemas.common import BrainRecord, RecordType


class EvidenceKind(str, Enum):
    DOCUMENT_SECTION = "document_section"
    TRAINING_VIDEO_SEGMENT = "training_video_segment"
    SLIDE_SEGMENT = "slide_segment"
    IMAGE_OR_OCR_REGION = "image_or_ocr_region"
    INCIDENT_TIMELINE_EVENT = "incident_timeline_event"
    INCIDENT_FINDING = "incident_finding"
    RCA_FINDING = "rca_finding"
    SME_NOTE = "sme_note"
    RUNTIME_INTERACTION_EVIDENCE = "runtime_interaction_evidence"


class EvidenceContent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str | None = None
    is_verbatim: bool
    content_hash: str
    structured_payload: dict[str, Any] | None = None

    @model_validator(mode="after")
    def _content_hash_not_empty(self) -> "EvidenceContent":
        if not self.content_hash.strip():
            raise ValueError("content_hash must not be empty")
        return self


class EvidenceLocator(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int | None = None
    section: str | None = None
    slide: int | None = None
    video_start_seconds: float | None = None
    video_end_seconds: float | None = None
    timeline_event_order: int | None = None
    artifact_ids: list[str] = Field(default_factory=list)


class EvidenceUnit(BrainRecord):
    type: RecordType = RecordType.EVIDENCE_UNIT

    evidence_kind: EvidenceKind
    source_type: str
    source_id: str
    ingestion_run_id: str | None = None

    content: EvidenceContent
    locator: EvidenceLocator = Field(default_factory=EvidenceLocator)

    @model_validator(mode="after")
    def _text_required_for_textual_kinds(self) -> "EvidenceUnit":
        textual_kinds = {
            EvidenceKind.DOCUMENT_SECTION,
            EvidenceKind.TRAINING_VIDEO_SEGMENT,
            EvidenceKind.SLIDE_SEGMENT,
            EvidenceKind.IMAGE_OR_OCR_REGION,
            EvidenceKind.INCIDENT_TIMELINE_EVENT,
            EvidenceKind.INCIDENT_FINDING,
            EvidenceKind.RCA_FINDING,
            EvidenceKind.SME_NOTE,
        }
        if self.evidence_kind in textual_kinds and not (self.content.text and self.content.text.strip()):
            raise ValueError(
                f"content.text is required when evidence_kind is {self.evidence_kind.value!r}"
            )
        return self
