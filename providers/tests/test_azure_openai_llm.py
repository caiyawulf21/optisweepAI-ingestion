from __future__ import annotations

import pytest
from pydantic import BaseModel

from providers.azure_openai_llm import AzureOpenAILLMProvider
from providers.llm import LLMSchemaValidationError


class _Schema(BaseModel):
    name: str
    count: int


@pytest.fixture()
def provider(monkeypatch: pytest.MonkeyPatch) -> AzureOpenAILLMProvider:
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://fake.openai.azure.com")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "fake-key")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "fake-deployment")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
    return AzureOpenAILLMProvider()


def test_missing_env_vars_raise_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    # A real .env file exists in this repo (real Azure credentials for
    # manual runs) -- AzureOpenAILLMProvider.__init__ calls load_dotenv()
    # itself, which would silently repopulate the env vars this test just
    # deleted. Patching load_dotenv to a no-op is what actually isolates
    # this test from that file, not delenv alone.
    monkeypatch.setattr("providers.azure_openai_llm.load_dotenv", lambda: None)
    monkeypatch.delenv("AZURE_OPENAI_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_DEPLOYMENT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_API_VERSION", raising=False)
    with pytest.raises(RuntimeError, match="Azure OpenAI is not configured"):
        AzureOpenAILLMProvider()


def test_generate_json_returns_validated_schema_on_first_try(
    monkeypatch: pytest.MonkeyPatch, provider: AzureOpenAILLMProvider
) -> None:
    def fake_request(**kwargs):
        return {"name": "widget", "count": 3}

    monkeypatch.setattr("providers.azure_openai_llm.request_azure_chat_json", fake_request)

    result = provider.generate_json(
        system_prompt="test", user_content="test", schema=_Schema, label="test"
    )
    assert result == _Schema(name="widget", count=3)


def test_generate_json_retries_on_validation_failure_then_succeeds(
    monkeypatch: pytest.MonkeyPatch, provider: AzureOpenAILLMProvider
) -> None:
    responses = [{"name": "widget"}, {"name": "widget", "count": 3}]  # first invalid, second valid

    def fake_request(**kwargs):
        return responses.pop(0)

    monkeypatch.setattr("providers.azure_openai_llm.request_azure_chat_json", fake_request)

    result = provider.generate_json(
        system_prompt="test", user_content="test", schema=_Schema, label="test", max_attempts=2
    )
    assert result == _Schema(name="widget", count=3)


def test_generate_json_raises_after_exhausting_attempts(
    monkeypatch: pytest.MonkeyPatch, provider: AzureOpenAILLMProvider
) -> None:
    def fake_request(**kwargs):
        return {"name": "widget"}  # always missing 'count'

    monkeypatch.setattr("providers.azure_openai_llm.request_azure_chat_json", fake_request)

    with pytest.raises(LLMSchemaValidationError) as exc_info:
        provider.generate_json(
            system_prompt="test", user_content="test", schema=_Schema, label="test", max_attempts=2
        )
    assert exc_info.value.label == "test"
    assert exc_info.value.raw_response == {"name": "widget"}


def test_generate_text_returns_text_field_when_present(
    monkeypatch: pytest.MonkeyPatch, provider: AzureOpenAILLMProvider
) -> None:
    monkeypatch.setattr(
        "providers.azure_openai_llm.request_azure_chat_json", lambda **kwargs: {"text": "hello"}
    )
    assert provider.generate_text(system_prompt="s", user_content="u", label="test") == "hello"


def test_generate_text_falls_back_to_json_dump(
    monkeypatch: pytest.MonkeyPatch, provider: AzureOpenAILLMProvider
) -> None:
    monkeypatch.setattr(
        "providers.azure_openai_llm.request_azure_chat_json", lambda **kwargs: {"other": "value"}
    )
    result = provider.generate_text(system_prompt="s", user_content="u", label="test")
    assert "other" in result
