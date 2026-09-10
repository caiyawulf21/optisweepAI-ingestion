"""Azure OpenAI / Foundry implementation of LLMProvider.

Delegates the actual HTTP call to shared_pipeline_stages.llm_pacing.
request_azure_chat_json, which already handles all 3 Azure endpoint shapes
(classic, Foundry project, Foundry /v1/responses), 429 pacing/backoff, and
JSON-fence-tolerant response parsing. This module adds nothing on top of
that except schema enforcement (retry + pydantic validation) and the
provider interface shape.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import ValidationError

from providers.llm import LLMProvider, LLMSchemaValidationError, SchemaT
from shared_pipeline_stages.llm_pacing import default_azure_api_version, request_azure_chat_json


def _clean_env_value(value: str | None) -> str:
    return (value or "").strip().strip('"').strip("'")


class AzureOpenAILLMProvider(LLMProvider):
    """Mirrors stage4_operational_context.AzureOpenAIContextClient's env-var
    loading pattern exactly (same variable names, same missing-var error
    shape) rather than inventing a parallel convention."""

    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
    ) -> None:
        load_dotenv()
        self.endpoint = _clean_env_value(endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")).rstrip("/")
        self.api_key = _clean_env_value(api_key or os.getenv("AZURE_OPENAI_API_KEY"))
        self.deployment = _clean_env_value(deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT"))
        env_api_version = _clean_env_value(os.getenv("AZURE_OPENAI_API_VERSION"))
        self.api_version = _clean_env_value(api_version) or default_azure_api_version(self.endpoint, env_api_version)
        missing = [
            name
            for name, value in [
                ("AZURE_OPENAI_ENDPOINT", self.endpoint),
                ("AZURE_OPENAI_API_KEY", self.api_key),
                ("AZURE_OPENAI_DEPLOYMENT", self.deployment),
                ("AZURE_OPENAI_API_VERSION", self.api_version),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError(
                "Azure OpenAI is not configured. Set these environment variables: " + ", ".join(missing)
            )

    def generate_json(
        self,
        *,
        system_prompt: str,
        user_content: str,
        schema: type[SchemaT],
        label: str,
        max_attempts: int = 2,
    ) -> SchemaT:
        schema_hint = json.dumps(schema.model_json_schema())
        prompt = f"{system_prompt}\n\nRespond with a single JSON object matching this schema:\n{schema_hint}"
        content = user_content
        raw: dict[str, Any] = {}
        last_error: ValidationError | None = None
        for _ in range(max(1, max_attempts)):
            raw = request_azure_chat_json(
                endpoint=self.endpoint,
                api_key=self.api_key,
                deployment=self.deployment,
                api_version=self.api_version,
                system_prompt=prompt,
                user_content=content,
                label=label,
            )
            try:
                return schema.model_validate(raw)
            except ValidationError as exc:
                last_error = exc
                content = (
                    f"{user_content}\n\nYour previous response failed schema validation:\n{exc}\n"
                    "Return corrected JSON matching the schema exactly."
                )
        raise LLMSchemaValidationError(label, raw, str(last_error))

    def generate_text(self, *, system_prompt: str, user_content: str, label: str) -> str:
        raw = request_azure_chat_json(
            endpoint=self.endpoint,
            api_key=self.api_key,
            deployment=self.deployment,
            api_version=self.api_version,
            system_prompt=system_prompt,
            user_content=user_content,
            label=label,
        )
        if "text" in raw and isinstance(raw["text"], str):
            return raw["text"]
        return json.dumps(raw, ensure_ascii=False)
