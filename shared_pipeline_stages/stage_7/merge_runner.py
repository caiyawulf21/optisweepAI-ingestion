from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol
import json
import os
import re
import sys

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared_pipeline_stages.llm_pacing import default_azure_api_version, request_azure_chat_json

from shared_pipeline_stages.stage_prompts import compose_stage7_system_prompt, load_prompt_file, resolve_stage7_prompt_path


class RunbookMergeClient(Protocol):
    def merge(self, packet: dict[str, Any]) -> dict[str, Any]:
        ...


class AzureOpenAIRunbookMergeClient:
    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        prompt_path: str | Path | None = None,
    ) -> None:
        load_dotenv()
        env_config = _resolve_stage7_azure_config()
        self.endpoint = _clean_env_value(endpoint or env_config["endpoint"]).rstrip("/")
        self.api_key = _clean_env_value(api_key or env_config["api_key"])
        self.deployment = _clean_env_value(deployment or env_config["deployment"])
        env_api_version = _clean_env_value(env_config["api_version"])
        self.api_version = _clean_env_value(api_version) or default_azure_api_version(self.endpoint, env_api_version)
        self.prompt = compose_stage7_system_prompt(load_prompt_file(prompt_path or resolve_stage7_prompt_path()))
        missing = [
            name
            for name, value in [
                (env_config["endpoint_name"], self.endpoint),
                (env_config["api_key_name"], self.api_key),
                (env_config["deployment_name"], self.deployment),
                (env_config["api_version_name"], self.api_version),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError("Azure OpenAI is not configured. Set these environment variables: " + ", ".join(missing))

    def merge(self, packet: dict[str, Any]) -> dict[str, Any]:
        response = request_azure_chat_json(
            endpoint=self.endpoint,
            api_key=self.api_key,
            deployment=self.deployment,
            api_version=self.api_version,
            system_prompt=self.prompt,
            user_content=json.dumps(packet, ensure_ascii=False),
            label="Stage 7",
            timeout=300,
        )
        return parse_merge_response(response)


def parse_merge_response(content: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(content, dict):
        return content
    text = content.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    return json.loads(text)


def _resolve_stage7_azure_config() -> dict[str, str]:
    # Mirrors shared_pipeline_stages.stage_8.linking_runner._resolve_stage8_azure_config:
    # prefer the AZURE_MINI_OPENAI_* deployment when it is fully configured, since that is
    # the endpoint/deployment/api-version combination actually verified working for LLM
    # merge/link calls in this environment; fall back to AZURE_OPENAI_* otherwise.
    mini = {
        "endpoint": _clean_env_value(os.getenv("AZURE_MINI_OPENAI_ENDPOINT")),
        "api_key": _clean_env_value(os.getenv("AZURE_MINI_OPENAI_API_KEY")),
        "deployment": _clean_env_value(os.getenv("AZURE_MINI_OPENAI_DEPLOYMENT")),
        "api_version": _clean_env_value(os.getenv("AZURE_MINI_OPENAI_API_VERSION")),
        "endpoint_name": "AZURE_MINI_OPENAI_ENDPOINT",
        "api_key_name": "AZURE_MINI_OPENAI_API_KEY",
        "deployment_name": "AZURE_MINI_OPENAI_DEPLOYMENT",
        "api_version_name": "AZURE_MINI_OPENAI_API_VERSION",
    }
    if all(mini[name] for name in ("endpoint", "api_key", "deployment", "api_version")):
        return mini
    return {
        "endpoint": _clean_env_value(os.getenv("AZURE_OPENAI_ENDPOINT")),
        "api_key": _clean_env_value(os.getenv("AZURE_OPENAI_API_KEY")),
        "deployment": _clean_env_value(os.getenv("AZURE_OPENAI_DEPLOYMENT")),
        "api_version": _clean_env_value(os.getenv("AZURE_OPENAI_API_VERSION")),
        "endpoint_name": "AZURE_OPENAI_ENDPOINT",
        "api_key_name": "AZURE_OPENAI_API_KEY",
        "deployment_name": "AZURE_OPENAI_DEPLOYMENT",
        "api_version_name": "AZURE_OPENAI_API_VERSION",
    }


def _clean_env_value(value: str | None) -> str:
    return (value or "").strip().strip('"').strip("'")
