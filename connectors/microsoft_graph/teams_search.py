"""Teams chat discovery correlated to a Salesforce case number + date window."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from connectors.microsoft_graph.client import GraphClient
from connectors.microsoft_graph.errors import CATEGORY_QUERY_FAILED, GraphProbeError

_HTML_TAG_RE = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class TeamsChatHit:
    chat_id: str
    topic: str
    chat_type: str
    source: str


@dataclass(frozen=True)
class TeamsMessageHit:
    chat_id: str
    message_id: str
    created_date_time: str
    from_name: str
    body_preview: str
    web_url: str
    source: str


@dataclass
class TeamsCaseSearchResult:
    case_number: str
    from_date: str
    to_date: str
    me: dict[str, str] = field(default_factory=dict)
    chats: list[TeamsChatHit] = field(default_factory=list)
    messages: list[TeamsMessageHit] = field(default_factory=list)
    output_dir: str = ""
    chat_topic: str = ""
    downloaded_images: list[str] = field(default_factory=list)


def get_me(client: GraphClient) -> dict[str, str]:
    payload = client.get_json("/me", context="GET /me")
    if not isinstance(payload, dict):
        raise GraphProbeError(CATEGORY_QUERY_FAILED, "GET /me returned unexpected payload.")
    return {
        "id": str(payload.get("id") or ""),
        "displayName": str(payload.get("displayName") or ""),
        "userPrincipalName": str(payload.get("userPrincipalName") or ""),
    }


def find_chats_by_topic(
    client: GraphClient,
    topic: str,
    *,
    exact: bool = True,
) -> list[TeamsChatHit]:
    """Find chats whose topic matches (exact by default, case-insensitive)."""
    needle = topic.strip().casefold()
    if not needle:
        raise GraphProbeError(CATEGORY_QUERY_FAILED, "Chat topic must not be empty.")

    chats = client.get_paged("/me/chats?$top=50", context="list chats", max_pages=40)
    hits: list[TeamsChatHit] = []
    for chat in chats:
        chat_topic = str(chat.get("topic") or "")
        chat_id = str(chat.get("id") or "")
        if not chat_id:
            continue
        hay = chat_topic.casefold()
        matched = hay == needle if exact else needle in hay
        if not matched:
            continue
        hits.append(
            TeamsChatHit(
                chat_id=chat_id,
                topic=chat_topic or "(no topic)",
                chat_type=str(chat.get("chatType") or ""),
                source="me/chats topic match",
            )
        )
    return hits


def find_chats_for_case(client: GraphClient, case_number: str) -> list[TeamsChatHit]:
    """List signed-in user's chats and keep ones whose topic mentions the case number."""
    needle = case_number.strip()
    chats = client.get_paged("/me/chats?$top=50", context="list chats", max_pages=40)
    hits: list[TeamsChatHit] = []
    for chat in chats:
        topic = str(chat.get("topic") or "")
        chat_id = str(chat.get("id") or "")
        if not chat_id:
            continue
        if needle and needle not in topic and needle.lstrip("0") not in topic:
            continue
        hits.append(
            TeamsChatHit(
                chat_id=chat_id,
                topic=topic or "(no topic)",
                chat_type=str(chat.get("chatType") or ""),
                source="me/chats topic match",
            )
        )
    return hits


def search_messages_for_case(
    client: GraphClient,
    case_number: str,
    *,
    from_date: date,
    to_date: date,
    size: int = 25,
) -> list[TeamsMessageHit]:
    """Use Graph Search API over chatMessage with case number + sent date KQL."""
    # Inclusive end date: Graph `sent` is day-based; bump to_date by 1 day with < next day.
    end_exclusive = to_date + timedelta(days=1)
    query_string = (
        f"{case_number} sent>={from_date.isoformat()} sent<{end_exclusive.isoformat()}"
    )
    body = {
        "requests": [
            {
                "entityTypes": ["chatMessage"],
                "query": {"queryString": query_string},
                "from": 0,
                "size": size,
                "enableTopResults": True,
            }
        ]
    }
    try:
        payload = client.post_json("/search/query", body, context="search chatMessage")
    except GraphProbeError as exc:
        # Some tenants/apps lack Search permissions; caller can still use chat topic matches.
        if "authorization" in exc.category or "Forbidden" in str(exc) or "AuthenticationError" in str(exc):
            raise GraphProbeError(
                exc.category,
                "Teams message search failed (permission or Search API access). "
                "Chat topic matching may still work. Details: " + str(exc.args[0]),
            ) from None
        raise

    hits: list[TeamsMessageHit] = []
    for response in payload.get("value") or []:
        if not isinstance(response, dict):
            continue
        container = response.get("hitsContainers") or []
        for bucket in container:
            if not isinstance(bucket, dict):
                continue
            for hit in bucket.get("hits") or []:
                if not isinstance(hit, dict):
                    continue
                resource = hit.get("resource") or {}
                if not isinstance(resource, dict):
                    continue
                hits.append(_message_from_search_resource(resource, source="search/query"))
    return hits


def fetch_messages_in_window(
    client: GraphClient,
    chat_id: str,
    *,
    from_date: date,
    to_date: date,
    max_pages: int = 100,
) -> list[TeamsMessageHit]:
    hits, _raws = fetch_messages_in_window_with_raw(
        client,
        chat_id,
        from_date=from_date,
        to_date=to_date,
        max_pages=max_pages,
    )
    return hits


def fetch_messages_in_window_with_raw(
    client: GraphClient,
    chat_id: str,
    *,
    from_date: date,
    to_date: date,
    max_pages: int = 100,
) -> tuple[list[TeamsMessageHit], list[dict[str, Any]]]:
    """Pull messages for one chat inside the date window, keeping raw Graph records."""
    from urllib.parse import quote

    start = datetime(from_date.year, from_date.month, from_date.day, tzinfo=timezone.utc)
    end = datetime(to_date.year, to_date.month, to_date.day, tzinfo=timezone.utc) + timedelta(days=1)
    url: str | None = f"/me/chats/{quote(chat_id, safe='')}/messages?$top=50"
    hits: list[TeamsMessageHit] = []
    raws: list[dict[str, Any]] = []
    pages = 0
    try:
        while url and pages < max_pages:
            payload = client.get_json(url, context=f"chat messages {chat_id}")
            if not isinstance(payload, dict):
                raise GraphProbeError(CATEGORY_QUERY_FAILED, "Unexpected chat messages payload.")
            records = [item for item in (payload.get("value") or []) if isinstance(item, dict)]
            if not records:
                break
            reached_before_window = False
            for record in records:
                created_raw = str(record.get("createdDateTime") or "")
                created = _parse_dt(created_raw)
                if created is None:
                    continue
                if created < start:
                    reached_before_window = True
                    continue
                if created >= end:
                    continue
                hits.append(
                    _message_from_chat_message(record, chat_id=chat_id, source="chat messages")
                )
                raws.append(record)
            next_link = payload.get("@odata.nextLink")
            url = str(next_link) if next_link and not reached_before_window else None
            pages += 1
    except GraphProbeError as exc:
        raise GraphProbeError(
            CATEGORY_QUERY_FAILED,
            f"Failed reading messages for chat: {exc.args[0]}",
        ) from None
    return hits, raws


def pull_chat_messages_by_topic(
    client: GraphClient,
    chat_topic: str,
    *,
    from_date: date,
    to_date: date,
    output_dir: Path | None = None,
    exact_topic: bool = True,
    download_images: bool = True,
) -> TeamsCaseSearchResult:
    """Resolve one chat by topic and pull all messages in the date window (no case search)."""
    from connectors.microsoft_graph.chat_images import download_images_for_message

    me = get_me(client)
    chats = find_chats_by_topic(client, chat_topic, exact=exact_topic)
    if not chats and exact_topic:
        chats = find_chats_by_topic(client, chat_topic, exact=False)
    if not chats:
        raise GraphProbeError(
            CATEGORY_QUERY_FAILED,
            f"No chat found with topic matching {chat_topic!r}. "
            "Confirm you are a member of that chat under this account.",
        )
    if len(chats) > 1:
        topics = ", ".join(repr(c.topic) for c in chats[:5])
        raise GraphProbeError(
            CATEGORY_QUERY_FAILED,
            f"Multiple chats matched topic {chat_topic!r}: {topics}. Pass a more exact topic.",
        )

    chat = chats[0]
    messages, raws = fetch_messages_in_window_with_raw(
        client,
        chat.chat_id,
        from_date=from_date,
        to_date=to_date,
    )
    messages = _dedupe_messages(messages)
    downloaded: list[str] = []
    if output_dir is not None and download_images:
        images_dir = output_dir / "images"
        # Re-align raws to deduped messages by message id.
        raw_by_id = {str(raw.get("id") or ""): raw for raw in raws}
        for msg in messages:
            raw = raw_by_id.get(msg.message_id) or {"id": msg.message_id}
            try:
                downloaded.extend(
                    download_images_for_message(
                        client,
                        msg.chat_id,
                        msg.message_id,
                        raw,
                        images_dir,
                    )
                )
            except GraphProbeError:
                continue

    result = TeamsCaseSearchResult(
        case_number="",
        chat_topic=chat.topic,
        from_date=from_date.isoformat(),
        to_date=to_date.isoformat(),
        me=me,
        chats=[chat],
        messages=messages,
        downloaded_images=downloaded,
    )
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        result.output_dir = str(output_dir)
        _write_artifacts(output_dir, result, search_error=None)
    return result


def search_teams_for_case(
    client: GraphClient,
    case_number: str,
    *,
    from_date: date,
    to_date: date,
    output_dir: Path | None = None,
    pull_matched_chat_messages: bool = True,
) -> TeamsCaseSearchResult:
    me = get_me(client)
    chats = find_chats_for_case(client, case_number)

    messages: list[TeamsMessageHit] = []
    search_error: str | None = None
    try:
        messages.extend(
            search_messages_for_case(
                client,
                case_number,
                from_date=from_date,
                to_date=to_date,
            )
        )
    except GraphProbeError as exc:
        search_error = str(exc)

    if pull_matched_chat_messages:
        for chat in chats:
            try:
                messages.extend(
                    fetch_messages_in_window(
                        client,
                        chat.chat_id,
                        from_date=from_date,
                        to_date=to_date,
                    )
                )
            except GraphProbeError:
                continue

    messages = _dedupe_messages(messages)
    result = TeamsCaseSearchResult(
        case_number=case_number,
        from_date=from_date.isoformat(),
        to_date=to_date.isoformat(),
        me=me,
        chats=chats,
        messages=messages,
    )
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        result.output_dir = str(output_dir)
        _write_artifacts(output_dir, result, search_error=search_error)
    elif search_error:
        # Surface soft search failure in empty-result cases by attaching note via markdown-less path.
        result.me = {**me, "search_warning": search_error}
    return result


def infer_case_window_from_salesforce_probe(
    case_number: str,
    repo_root: Path,
) -> tuple[date, date] | None:
    feed_path = repo_root / "data" / "output" / "salesforce_probe" / f"case_{case_number}" / "case_feed.json"
    if not feed_path.exists():
        return None
    payload = json.loads(feed_path.read_text(encoding="utf-8"))
    dates: list[date] = []
    for entry in payload.get("feed") or []:
        raw = str((entry or {}).get("created_date") or "")
        parsed = _parse_dt(raw)
        if parsed:
            dates.append(parsed.date())
    for email in payload.get("emails") or []:
        raw = str((email or {}).get("message_date") or "")
        parsed = _parse_dt(raw)
        if parsed:
            dates.append(parsed.date())
    if not dates:
        return None
    return min(dates), max(dates)


def _write_artifacts(
    output_dir: Path,
    result: TeamsCaseSearchResult,
    *,
    search_error: str | None,
) -> None:
    payload = {
        "case_number": result.case_number,
        "chat_topic": result.chat_topic,
        "from_date": result.from_date,
        "to_date": result.to_date,
        "me": result.me,
        "search_error": search_error,
        "chats": [asdict(c) for c in result.chats],
        "messages": [asdict(m) for m in result.messages],
        "downloaded_images": result.downloaded_images,
    }
    (output_dir / "teams_hits.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    title = result.chat_topic or (f"Case {result.case_number}" if result.case_number else "Teams chat")
    lines = [
        f"# Teams hits for {title}",
        "",
        f"- Window: {result.from_date} .. {result.to_date}",
        f"- Signed in as: {result.me.get('displayName')} <{result.me.get('userPrincipalName')}>",
        f"- Chats: {len(result.chats)}",
        f"- Messages: {len(result.messages)}",
        f"- Images downloaded: {len(result.downloaded_images)}",
        "",
    ]
    if search_error:
        lines.extend([f"> Search API warning: {search_error}", ""])

    lines.extend(["## Chats", ""])
    if not result.chats:
        lines.append("(none matched)")
        lines.append("")
    for chat in result.chats:
        lines.append(f"- `{chat.chat_type}` | {chat.topic} | `{chat.chat_id}`")
    lines.append("")

    lines.extend(["## Messages", ""])
    if not result.messages:
        lines.append("(none found in window)")
        lines.append("")
    for msg in result.messages:
        lines.append(f"### {msg.created_date_time} | {msg.from_name}")
        lines.append(msg.body_preview or "(no body)")
        if msg.web_url:
            lines.append(f"Link: {msg.web_url}")
        lines.append("")

    if result.downloaded_images:
        lines.extend(["## Images", ""])
        for relative in result.downloaded_images:
            lines.append(f"- `{relative}`")
        lines.append("")

    (output_dir / "teams_hits.md").write_text("\n".join(lines), encoding="utf-8")


def _message_from_search_resource(resource: dict[str, Any], *, source: str) -> TeamsMessageHit:
    from_block = resource.get("from") or {}
    from_name = ""
    if isinstance(from_block, dict):
        email = from_block.get("emailAddress") or {}
        if isinstance(email, dict):
            from_name = str(email.get("name") or email.get("address") or "")
        user = from_block.get("user") or {}
        if not from_name and isinstance(user, dict):
            from_name = str(user.get("displayName") or "")
    body = resource.get("body") or {}
    preview = ""
    if isinstance(body, dict):
        preview = _html_to_text(str(body.get("content") or ""))
    summary = str(resource.get("summary") or "")
    if summary and not preview:
        preview = summary
    return TeamsMessageHit(
        chat_id=str(resource.get("chatId") or resource.get("id") or ""),
        message_id=str(resource.get("id") or ""),
        created_date_time=str(resource.get("createdDateTime") or ""),
        from_name=from_name,
        body_preview=preview[:1000],
        web_url=str(resource.get("webLink") or resource.get("webUrl") or ""),
        source=source,
    )


def _message_from_chat_message(record: dict[str, Any], *, chat_id: str, source: str) -> TeamsMessageHit:
    from_block = record.get("from") or {}
    from_name = ""
    if isinstance(from_block, dict):
        user = from_block.get("user") or {}
        if isinstance(user, dict):
            from_name = str(user.get("displayName") or "")
    body = record.get("body") or {}
    preview = ""
    if isinstance(body, dict):
        preview = _html_to_text(str(body.get("content") or ""))
    return TeamsMessageHit(
        chat_id=chat_id,
        message_id=str(record.get("id") or ""),
        created_date_time=str(record.get("createdDateTime") or ""),
        from_name=from_name,
        body_preview=preview[:1000],
        web_url=str(record.get("webUrl") or ""),
        source=source,
    )


def _dedupe_messages(messages: list[TeamsMessageHit]) -> list[TeamsMessageHit]:
    seen: set[str] = set()
    out: list[TeamsMessageHit] = []
    for msg in messages:
        key = msg.message_id or f"{msg.chat_id}:{msg.created_date_time}:{msg.body_preview[:80]}"
        if key in seen:
            continue
        seen.add(key)
        out.append(msg)
    out.sort(key=lambda item: item.created_date_time)
    return out


def _parse_dt(raw: str) -> datetime | None:
    if not raw:
        return None
    text = raw.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _html_to_text(value: str) -> str:
    if not value:
        return ""
    text = value.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    text = text.replace("</p>", "\n").replace("<p>", "")
    text = _HTML_TAG_RE.sub("", text)
    return text.strip()
