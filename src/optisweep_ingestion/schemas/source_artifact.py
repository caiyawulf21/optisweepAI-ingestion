"""Schemas for deterministic Stage 2 source artifacts."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


ALLOWED_ARTIFACT_TYPES = {
    "manual_figure",
    "manual_page_image",
    "manual_table_reference",
    "unknown_image",
}

ALLOWED_IMAGE_TYPES = {
    "hmi_screenshot",
    "rms_screenshot",
    "system_screen",
    "operator_station_screen",
    "hospital_station_screen",
    "agv_screen",
    "diagram",
    "photo",
    "maintenance_diagram",
    "unknown",
}


class SourceArtifact(BaseModel):
    artifact_id: str
    source_document_id: str
    source_bundle_id: str

    artifact_type: str
    image_type: str | None = None

    title: str | None = None
    figure_id: str | None = None
    figure_number: str | None = None
    table_id: str | None = None
    table_number: str | None = None

    page_number: int | None = None
    section_id: str | None = None

    storage_path: str | None = None
    file_name: str | None = None
    file_format: str | None = None

    caption_text: str | None = None
    nearby_text: str | None = None
    retrieval_text: str | None = None
    summary: str | None = None
    short_description: str | None = None
    detailed_description: str | None = None
    what_to_look_at: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    enrichment_notes: list[str] = Field(default_factory=list)

    linked_context_ids: list[str] = Field(default_factory=list)
    linked_runbook_ids: list[str] = Field(default_factory=list)
    linked_procedure_ids: list[str] = Field(default_factory=list)

    source_refs: list[dict] = Field(default_factory=list)
    extraction_metadata: dict = Field(default_factory=dict)

    @field_validator("artifact_type")
    @classmethod
    def validate_artifact_type(cls, value: str) -> str:
        if value not in ALLOWED_ARTIFACT_TYPES:
            raise ValueError(f"Unsupported artifact_type: {value}")
        return value

    @field_validator("image_type")
    @classmethod
    def validate_image_type(cls, value: str | None) -> str | None:
        if value is not None and value not in ALLOWED_IMAGE_TYPES:
            raise ValueError(f"Unsupported image_type: {value}")
        return value
