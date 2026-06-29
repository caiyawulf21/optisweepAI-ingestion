"""Shared source lineage fields for source knowledge extraction outputs."""

from __future__ import annotations

from pydantic import BaseModel, field_validator

ALLOWED_SOURCE_TYPES = {
    "manual",
    "training_slide",
    "training_transcript",
    "training_video",
    "incident",
    "sop",
    "sme_authored",
}


class SourceLineage(BaseModel):
    source_id: str
    source_type: str
    source_title: str
    source_version: str | None = None
    ingestion_batch_id: str
    source_document_id: str | None = None

    @field_validator("source_type")
    @classmethod
    def validate_source_type(cls, value: str) -> str:
        if value not in ALLOWED_SOURCE_TYPES:
            raise ValueError(f"Unsupported source_type: {value}")
        return value
