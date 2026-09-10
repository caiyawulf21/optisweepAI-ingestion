"""Tool 1 -- extract_evidence (AGENT_DESIGN_NOTES.md §4.2).

Turns one bounded raw source packet into EvidenceUnit candidates and raw
claim candidates. Never judges truth, never resolves an entity id, never
decides anything is a duplicate.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from providers.llm import LLMProvider
from brain_service.types import ExtractEvidenceResult

_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "extract_evidence.md"


def _load_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def extract_evidence(llm: LLMProvider, source_packet: dict[str, Any]) -> ExtractEvidenceResult:
    import json

    return llm.generate_json(
        system_prompt=_load_prompt(),
        user_content=json.dumps(source_packet, ensure_ascii=False),
        schema=ExtractEvidenceResult,
        label="extract_evidence",
    )
