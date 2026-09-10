"""Provider-neutral LLM interface (newdesigndoc/OPTISWEEP_BRAIN_API_NEUTRAL_AGENT_PLAN.md
Step 2). Every ingestion/Brain tool calls an LLMProvider, never a vendor SDK directly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class LLMSchemaValidationError(RuntimeError):
    """Raised when an LLM's JSON response never validated against the requested
    schema within the allotted retries. Callers must handle this explicitly —
    generate_json() never returns a partially-valid or best-guess object."""

    def __init__(self, label: str, raw_response: dict, pydantic_errors: str) -> None:
        self.label = label
        self.raw_response = raw_response
        self.pydantic_errors = pydantic_errors
        super().__init__(f"{label}: response did not validate against schema: {pydantic_errors}")


class LLMProvider(ABC):
    @abstractmethod
    def generate_json(
        self,
        *,
        system_prompt: str,
        user_content: str,
        schema: type[SchemaT],
        label: str,
        max_attempts: int = 2,
    ) -> SchemaT:
        """Call the model, requesting JSON, and return it parsed and validated
        against `schema`. Schema conformance is retry-and-validate, not an
        API-level guarantee: on a pydantic ValidationError, the implementation
        may retry with the validation error appended to `user_content`.
        Raises LLMSchemaValidationError if `schema` is never satisfied within
        `max_attempts`."""

    @abstractmethod
    def generate_text(self, *, system_prompt: str, user_content: str, label: str) -> str:
        """Call the model and return free-form text. No schema enforcement."""
