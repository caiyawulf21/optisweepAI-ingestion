from __future__ import annotations

from typing import Literal, TypedDict


SourceType = Literal["incident", "manual", "training_video", "unknown"]
RunStatus = Literal["pending", "running", "succeeded", "failed", "skipped"]


class IngestionState(TypedDict, total=False):
    source_path: str
    companion_paths: list[str]
    source_type: SourceType
    case_id: str | None
    source_id: str | None
    source_title: str | None
    output_dir: str
    source_stages: str
    shared_stages: str
    use_llm: bool
    run_shared_publish: bool
    publish_to_cosmos: bool
    publish_scope: str
    shared_publish_scope: str
    ocr_backend: str
    max_workers: int
    status: RunStatus
    current_node: str
    errors: list[str]
    messages: list[str]
    source_roots: list[str]
