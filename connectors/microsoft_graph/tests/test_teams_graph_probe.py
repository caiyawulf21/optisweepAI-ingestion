"""Lightweight unit tests for Microsoft Graph / Teams probe helpers."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from connectors.microsoft_graph.auth import GraphToken, load_graph_credentials
from connectors.microsoft_graph.client import GraphClient
from connectors.microsoft_graph.errors import CATEGORY_MISSING_ENV, GraphProbeError
from connectors.microsoft_graph.teams_search import infer_case_window_from_salesforce_probe


def test_missing_graph_env() -> None:
    with pytest.raises(GraphProbeError) as exc_info:
        load_graph_credentials({})
    assert exc_info.value.category == CATEGORY_MISSING_ENV


def test_infer_window_from_salesforce_probe(tmp_path: Path, monkeypatch) -> None:
    case_dir = tmp_path / "data" / "output" / "salesforce_probe" / "case_00233681"
    case_dir.mkdir(parents=True)
    (case_dir / "case_feed.json").write_text(
        json.dumps(
            {
                "feed": [
                    {"created_date": "2026-08-22T10:04:36.000+0000"},
                    {"created_date": "2026-08-25T21:19:16.000+0000"},
                ],
                "emails": [],
            }
        ),
        encoding="utf-8",
    )
    window = infer_case_window_from_salesforce_probe("00233681", tmp_path)
    assert window == (date(2026, 8, 22), date(2026, 8, 25))


def test_pull_chat_messages_by_topic(tmp_path: Path, monkeypatch) -> None:
    from connectors.microsoft_graph.teams_search import pull_chat_messages_by_topic

    token = GraphToken(access_token="tok")
    pages = {
        "me": {
            "id": "u1",
            "displayName": "Test User",
            "userPrincipalName": "test@fortna.com",
        },
        "chats": {
            "value": [
                {
                    "id": "chat-haslet",
                    "topic": "Support chat for Haslet",
                    "chatType": "group",
                }
            ]
        },
        "messages": {
            "value": [
                {
                    "id": "m1",
                    "createdDateTime": "2026-08-22T12:00:00Z",
                    "from": {"user": {"displayName": "Mitchel Flynn"}},
                    "body": {"content": "commlost"},
                    "webUrl": "",
                    "attachments": [],
                },
                {
                    "id": "m0",
                    "createdDateTime": "2026-08-01T12:00:00Z",
                    "from": {"user": {"displayName": "Old"}},
                    "body": {"content": "too old"},
                    "webUrl": "",
                },
            ]
        },
        "hosted": {
            "value": [
                {"id": "hc1", "contentType": "image/png"},
            ]
        },
    }

    def fake_request(method, url, *, data=None, content_type=None, context=""):
        if url.rstrip("/").endswith("/me"):
            return 200, pages["me"]
        if "/me/chats?" in url or url.endswith("/me/chats"):
            return 200, pages["chats"]
        if "/hostedContents" in url and not url.endswith("/$value"):
            return 200, pages["hosted"]
        if "/messages" in url:
            return 200, pages["messages"]
        raise AssertionError((method, url))

    def fake_bytes(path_or_url, *, context=""):
        assert "/hostedContents/" in path_or_url and path_or_url.endswith("/$value")
        return b"\x89PNG\r\n\x1a\nfake", "image/png"

    client = GraphClient(token)
    monkeypatch.setattr(client, "_request", fake_request)
    monkeypatch.setattr(client, "get_bytes", fake_bytes)
    result = pull_chat_messages_by_topic(
        client,
        "Support chat for Haslet",
        from_date=date(2026, 8, 22),
        to_date=date(2026, 8, 25),
        output_dir=tmp_path / "out",
    )
    assert result.chat_topic == "Support chat for Haslet"
    assert len(result.chats) == 1
    assert len(result.messages) == 1
    assert result.messages[0].body_preview == "commlost"
    assert len(result.downloaded_images) == 1
    assert (tmp_path / "out" / "images" / "m1_1.png").exists()
