from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EmbeddingRecord(BaseModel):
    record_id: str
    record_type: str
    source_record_id: str
    source_type: str = ""
    embedded_text: str
    vector: list[float] = Field(default_factory=list)
    embedding_model: str
    embedding_dimensions: int
    retrieval_text_hash: str
    filter_metadata: dict[str, Any] = Field(default_factory=dict)
    source_refs: list[Any] = Field(default_factory=list)
