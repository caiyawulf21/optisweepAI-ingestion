from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PublishManifest(BaseModel):
    publish_version_id: str
    generated_at: str
    embedding_model: str
    record_counts: dict[str, int] = Field(default_factory=dict)
    link_counts_by_type: dict[str, int] = Field(default_factory=dict)
    checksums: dict[str, str] = Field(default_factory=dict)
    cosmos: dict[str, str] = Field(default_factory=dict)
    containers: dict[str, str] = Field(default_factory=dict)
    source_paths: dict[str, str] = Field(default_factory=dict)
