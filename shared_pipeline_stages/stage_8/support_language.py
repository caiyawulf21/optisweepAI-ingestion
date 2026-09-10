from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "after",
    "before",
    "reported",
    "report",
    "showing",
    "show",
    "unable",
    "being",
}

CASE_REQUIRED_EXAMPLES: dict[str, tuple[str, ...]] = {
    "228086": (
        "AGVs stopped",
        "robots stopped",
        "nothing is moving",
        "AGVs aren't moving",
        "no RMS alarms",
        "rms showing no alarms",
    ),
    "228723": (
        "zone unable to get a pair",
        "every AMR goes to the hospital",
        "AMRs going to hospital",
        "pairing failure",
        "robot not mapped",
    ),
    "218550": (
        "bag out stopped",
        "system stopped at bag-out",
        "manually bagging out",
        "hospital HMI fault",
    ),
    "223554": (
        "hospital can't add totes",
        "can't induct totes",
        "hospital induct blocked",
        "AGV doesn't belong here",
    ),
}

NARRATIVE_PREFIXES = (
    "affected zone reported as ",
    "site reports ",
    "site reported ",
    "acb system reported ",
    "issue reported after ",
    "issue began or worsened after ",
    "replacement or multiple amrs reported as ",
    "a reported robot may be ",
)


def enrich_support_user_language_examples(
    examples: list[str] | None,
    *,
    case_id: str | None = None,
    title: str | None = None,
    observed_entry_symptoms: list[str] | None = None,
    learned_phrases: list[str] | None = None,
) -> list[str]:
    cleaned = _dedupe_phrases(examples or [])
    cleaned = _dedupe_phrases(
        cleaned
        + _phrases_from_symptoms(observed_entry_symptoms or [])
        + list(CASE_REQUIRED_EXAMPLES.get(str(case_id or "").strip(), ()))
    )

    if learned_phrases:
        seed_text = " ".join(
            [
                str(title or ""),
                " ".join(observed_entry_symptoms or []),
                " ".join(cleaned),
            ]
        )
        seed_tokens = _tokenize(seed_text)
        for phrase in learned_phrases:
            if _token_overlap_ratio(seed_tokens, _tokenize(phrase)) >= 0.45:
                cleaned.append(phrase)
        cleaned = _dedupe_phrases(cleaned)

    if _is_stoppage_playbook(case_id=case_id, title=title):
        cleaned = _dedupe_phrases(cleaned + list(CASE_REQUIRED_EXAMPLES["228086"]))

    return cleaned


def enrich_playbook_record(
    playbook: dict[str, Any],
    *,
    learned_phrases: list[str] | None = None,
) -> dict[str, Any]:
    playbook["support_user_language_examples"] = enrich_support_user_language_examples(
        playbook.get("support_user_language_examples"),
        case_id=str(playbook.get("case_id") or ""),
        title=str(playbook.get("title") or ""),
        observed_entry_symptoms=list(playbook.get("observed_entry_symptoms") or []),
        learned_phrases=learned_phrases,
    )
    return playbook


def enrich_retrieval_card(
    card: dict[str, Any],
    *,
    learned_phrases: list[str] | None = None,
) -> dict[str, Any]:
    card["support_user_language_examples"] = enrich_support_user_language_examples(
        card.get("support_user_language_examples"),
        case_id=str(card.get("case_id") or ""),
        title=str(card.get("title") or ""),
        observed_entry_symptoms=list(card.get("observed_entry_symptoms") or []),
        learned_phrases=learned_phrases,
    )
    return card


def collect_learned_phrases_from_playbooks(playbooks: list[dict[str, Any]]) -> list[str]:
    phrases: list[str] = []
    for playbook in playbooks:
        phrases.extend(str(item) for item in playbook.get("support_user_language_examples") or [])
        phrases.extend(_phrases_from_symptoms(playbook.get("observed_entry_symptoms") or []))
    return _dedupe_phrases(phrases)


def load_learned_phrases(path: str | Path | None) -> list[str]:
    if path is None:
        return []
    phrase_path = Path(path)
    if not phrase_path.exists():
        return []
    payload = json.loads(phrase_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        rows = payload.get("phrases") or payload.get("learned_phrases") or []
    else:
        rows = payload
    if not isinstance(rows, list):
        return []
    return _dedupe_phrases([str(item) for item in rows])


def write_learned_phrases(path: str | Path, phrases: list[str]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(
            {
                "phrase_count": len(phrases),
                "phrases": _dedupe_phrases(phrases),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def symptom_example_coverage(
    symptoms: list[str] | None,
    examples: list[str] | None,
) -> float:
    symptom_rows = [str(item).strip() for item in symptoms or [] if str(item).strip()]
    example_rows = [str(item).strip() for item in examples or [] if str(item).strip()]
    if not symptom_rows:
        return 1.0 if example_rows else 0.0
    if not example_rows:
        return 0.0
    covered = 0
    for symptom in symptom_rows:
        symptom_tokens = _tokenize(symptom)
        if any(_token_overlap_ratio(symptom_tokens, _tokenize(example)) >= 0.34 for example in example_rows):
            covered += 1
    return covered / len(symptom_rows)


def _phrases_from_symptoms(symptoms: list[str]) -> list[str]:
    phrases: list[str] = []
    for raw in symptoms:
        text = str(raw).strip()
        if not text:
            continue
        lowered = text.casefold()
        for prefix in NARRATIVE_PREFIXES:
            if lowered.startswith(prefix):
                text = text[len(prefix) :].strip(" .")
                break
        text = re.sub(r"\s+", " ", text).strip(" .")
        if not text:
            continue
        if len(text.split()) <= 12:
            phrases.append(text)
        else:
            phrases.append(" ".join(text.split()[:8]))
    return phrases


def _is_stoppage_playbook(*, case_id: str | None, title: str | None) -> bool:
    if str(case_id or "").strip() != "228086":
        return False
    title_l = str(title or "").casefold()
    if "wcs" in title_l and "web" in title_l:
        return False
    if "application" in title_l and "fault" in title_l:
        return False
    return True


def _dedupe_phrases(phrases: list[str]) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in phrases:
        text = str(item).strip()
        if not text:
            continue
        key = text.casefold()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(text)
    return cleaned


def _tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9']+", text.casefold())
    return {token for token in tokens if token not in STOPWORDS and len(token) > 1}


def _token_overlap_ratio(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)
