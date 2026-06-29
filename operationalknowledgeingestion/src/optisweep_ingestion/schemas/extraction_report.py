"""Schema for unified source extraction reports."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RecordsCreated(BaseModel):
    artifacts: int = 0
    operational_context: int = 0
    runbook_candidates: int = 0


class LineageValidation(BaseModel):
    missing_source_id_count: int = 0
    missing_source_refs_count: int = 0


class SourceExtractionReport(BaseModel):
    source_id: str = ""
    source_type: str = ""
    ingestion_batch_id: str = ""
    records_created: RecordsCreated = Field(default_factory=RecordsCreated)
    lineage_validation: LineageValidation = Field(default_factory=LineageValidation)
    duplicate_candidate_count: int = 0
    placeholder_candidate_count: int = 0
    missing_artifact_reference_count: int = 0
    missing_context_reference_count: int = 0
    schema_validation_failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
