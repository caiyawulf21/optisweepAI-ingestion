"""Confirms the MCP server itself boots and registers all 15 tools --
distinct from test_tools.py, which tests the underlying functions
directly. This is the one check that exercises the actual `mcp` SDK
integration (decorator registration, schema inference)."""

from __future__ import annotations

import asyncio

EXPECTED_TOOL_NAMES = {
    "extract_evidence",
    "classify_candidate",
    "reconcile_candidate",
    "validate_and_prepare_for_review",
    "find_audit_candidates",
    "resolve_audit_candidate",
    "run_migration_batch",
    "draft_procedure",
    "draft_playbook",
    "get_brain_context",
    "validate_brain_records",
    "prepare_sme_review",
    "get_ingestion_run",
    "ingest_incident_pdf",
    "ingest_operational_source",
}


def test_server_registers_all_expected_tools() -> None:
    from mcp_server.server import server

    tool_list = asyncio.run(server.list_tools())
    registered_names = {tool.name for tool in tool_list}

    assert registered_names == EXPECTED_TOOL_NAMES


def test_server_tools_have_descriptions() -> None:
    from mcp_server.server import server

    tool_list = asyncio.run(server.list_tools())
    missing_descriptions = [tool.name for tool in tool_list if not tool.description]

    assert missing_descriptions == []
