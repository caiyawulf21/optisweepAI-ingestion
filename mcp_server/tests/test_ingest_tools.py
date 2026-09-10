"""ingest_incident_pdf/ingest_operational_source wrap the existing CLI
scripts as a subprocess -- these tests confirm the command line built is
correct (real flag names, BRAIN_INGESTION_ENABLED set) without actually
running a real pipeline (no source PDF, no Azure credentials needed)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mcp_server import tools


@pytest.fixture()
def fake_storage(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    from providers.local_storage import LocalStorageProvider

    storage = LocalStorageProvider(root=tmp_path)
    monkeypatch.setattr("mcp_server.tools.get_storage_provider", lambda: storage)
    return storage


def test_ingest_incident_pdf_builds_correct_command(monkeypatch: pytest.MonkeyPatch, fake_storage) -> None:
    captured = {}

    def fake_run(command, env, capture_output, text):
        captured["command"] = command
        captured["env"] = env
        return MagicMock(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr("mcp_server.tools.subprocess.run", fake_run)

    result = tools.tool_ingest_incident_pdf("C:/fake/Case 228086 Data.pdf", "228086")

    assert result["succeeded"] is True
    command = captured["command"]
    assert "--source" in command
    assert "C:/fake/Case 228086 Data.pdf" in command
    assert "--ocr-backend" in command
    assert "azure_cv" in command
    assert captured["env"]["BRAIN_INGESTION_ENABLED"] == "1"


def test_ingest_incident_pdf_reports_failure(monkeypatch: pytest.MonkeyPatch, fake_storage) -> None:
    monkeypatch.setattr(
        "mcp_server.tools.subprocess.run",
        lambda *a, **k: MagicMock(returncode=1, stdout="", stderr="boom"),
    )

    result = tools.tool_ingest_incident_pdf("C:/fake/Case 228086 Data.pdf", "228086")

    assert result["succeeded"] is False
    assert "boom" in result["stderr_tail"]


def test_ingest_incident_pdf_rejects_case_id_mismatch(monkeypatch: pytest.MonkeyPatch, fake_storage) -> None:
    called = False

    def fake_run(*a, **k):
        nonlocal called
        called = True
        return MagicMock(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr("mcp_server.tools.subprocess.run", fake_run)

    result = tools.tool_ingest_incident_pdf("C:/fake/unrelated.pdf", "228086")

    assert result["succeeded"] is False
    assert "case_id" in result["stderr_tail"]
    assert called is False


def test_ingest_incident_pdf_passes_publish_flags(monkeypatch: pytest.MonkeyPatch, fake_storage) -> None:
    captured = {}

    def fake_run(command, env, capture_output, text):
        captured["command"] = command
        return MagicMock(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr("mcp_server.tools.subprocess.run", fake_run)

    tools.tool_ingest_incident_pdf(
        "C:/fake/Case 228086 Data.pdf",
        "228086",
        run_shared_publish=True,
        publish_to_cosmos=True,
        publish_scope="case:228086",
    )

    command = captured["command"]
    assert "--with-publish" in command
    assert "--publish-to-cosmos" in command
    assert "--publish-scope" in command
    assert "case:228086" in command


def test_ingest_operational_source_builds_correct_command(monkeypatch: pytest.MonkeyPatch, fake_storage) -> None:
    captured = {}

    def fake_run(command, env, capture_output, text):
        captured["command"] = command
        return MagicMock(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr("mcp_server.tools.subprocess.run", fake_run)

    result = tools.tool_ingest_operational_source("C:/fake/manual.pdf", "manual_test_v1")

    assert result["succeeded"] is True
    command = captured["command"]
    assert "--source" in command
    assert "--source-id" in command
    assert "manual_test_v1" in command
    assert "--ocr-backend" in command
    assert "azure_cv" in command
