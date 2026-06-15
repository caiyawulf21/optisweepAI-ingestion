"""Schemas for the deterministic Stage 1 source bundle."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SourceDocument(BaseModel):
    source_document_id: str
    title: str | None = None
    document_type: str | None = None
    version: str | None = None
    document_date: str | None = None
    source_type: str
    source_path: str


class SourcePage(BaseModel):
    page_number: int
    text: str = ""
    text_length: int = 0
    section_id: str | None = None
    section_ids: list[str] = Field(default_factory=list)


class SourceSection(BaseModel):
    section_id: str
    title: str
    level: int
    page_start: int | None = None
    page_end: int | None = None
    parent_section_id: str | None = None
    text_preview: str | None = None


class SourceFigureRef(BaseModel):
    figure_id: str
    figure_number: str | None = None
    title: str | None = None
    page_number: int | None = None
    section_id: str | None = None
    caption_text: str | None = None


class SourceTableRef(BaseModel):
    table_id: str
    table_number: str | None = None
    title: str | None = None
    page_number: int | None = None
    section_id: str | None = None
    caption_text: str | None = None


class SourceBundle(BaseModel):
    source_bundle_id: str
    source_document: SourceDocument
    pages: list[SourcePage] = Field(default_factory=list)
    sections: list[SourceSection] = Field(default_factory=list)
    figure_refs: list[SourceFigureRef] = Field(default_factory=list)
    table_refs: list[SourceTableRef] = Field(default_factory=list)
    build_metadata: dict = Field(default_factory=dict)
