"""Site location metadata for incident ingestion lineage and citation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from optisweep_incidence_ingestion.utils.json_utils import read_json

DEFAULT_SITE_CODE = "ups_haslet_tx"

KNOWN_SITE_LOCATIONS: dict[str, dict[str, str]] = {
    "ups_haslet_tx": {
        "site_code": "ups_haslet_tx",
        "site_label": "UPS Haslet TX (TXRTH)",
        "customer": "UPS",
        "city": "Haslet",
        "state": "TX",
        "country": "US",
        "hub_code": "TXRTH",
        "region_label": "Fort Worth, TX",
    },
}


def resolve_site_location(
    *,
    site_code: str | None = None,
    site_location_json: str | Path | None = None,
    site_location: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if site_location:
        return normalize_site_location(site_location)
    if site_location_json:
        loaded = read_json(site_location_json)
        if not isinstance(loaded, dict):
            raise ValueError("site_location_json must contain a JSON object.")
        return normalize_site_location(loaded)
    code = (site_code or DEFAULT_SITE_CODE).strip().lower()
    known = KNOWN_SITE_LOCATIONS.get(code)
    if not known:
        known_codes = ", ".join(sorted(KNOWN_SITE_LOCATIONS))
        raise ValueError(f"Unknown site_code '{code}'. Known site codes: {known_codes}")
    return normalize_site_location(known)


def normalize_site_location(value: dict[str, Any]) -> dict[str, Any]:
    site_code = str(value.get("site_code") or "").strip().lower()
    if not site_code:
        raise ValueError("site_location.site_code is required.")
    site_label = str(value.get("site_label") or "").strip()
    customer = str(value.get("customer") or "").strip()
    city = str(value.get("city") or "").strip()
    state = str(value.get("state") or "").strip()
    country = str(value.get("country") or "").strip()
    hub_code = str(value.get("hub_code") or "").strip()
    region_label = str(value.get("region_label") or "").strip()
    if not site_label:
        parts = [customer, city, state]
        site_label = ", ".join(part for part in parts if part)
        if hub_code:
            site_label = f"{site_label} ({hub_code})" if site_label else hub_code
    return {
        "site_code": site_code,
        "site_label": site_label,
        "customer": customer,
        "city": city,
        "state": state,
        "country": country,
        "hub_code": hub_code,
        "region_label": region_label,
    }


def site_location_label(site_location: dict[str, Any] | None) -> str:
    if not site_location:
        return ""
    label = str(site_location.get("site_label") or "").strip()
    if label:
        return label
    parts = [
        str(site_location.get("customer") or "").strip(),
        str(site_location.get("city") or "").strip(),
        str(site_location.get("state") or "").strip(),
    ]
    return ", ".join(part for part in parts if part)


def site_ref_fields(site_location: dict[str, Any] | None) -> dict[str, str]:
    if not site_location:
        return {}
    fields: dict[str, str] = {}
    site_code = str(site_location.get("site_code") or "").strip()
    site_label = site_location_label(site_location)
    if site_code:
        fields["site_code"] = site_code
    if site_label:
        fields["site_label"] = site_label
    return fields


def apply_ingestion_site_to_canonical_record(
    record: dict[str, Any],
    *,
    site_location: dict[str, Any] | None,
) -> dict[str, Any]:
    if not site_location:
        return record
    updated = dict(record)
    site = dict(updated.get("site") or {}) if isinstance(updated.get("site"), dict) else {}
    site["ingestion_site"] = dict(site_location)
    if not str(site.get("primary_label") or "").strip():
        site["primary_label"] = site_location_label(site_location)
    observed = list(site.get("observed_location_text") or [])
    ingestion_label = site_location_label(site_location)
    if ingestion_label and ingestion_label not in observed:
        observed.insert(0, ingestion_label)
    site["observed_location_text"] = observed
    if not str(site.get("location_confidence") or "").strip() or site.get("location_confidence") == "unknown":
        site["location_confidence"] = "high"
    notes = str(site.get("notes") or "").strip()
    ingestion_note = (
        f"Ingestion metadata identifies this case as {ingestion_label} (site_code={site_location.get('site_code')})."
    )
    if ingestion_note not in notes:
        site["notes"] = f"{notes} {ingestion_note}".strip() if notes else ingestion_note
    updated["site"] = site
    if not str(updated.get("customer") or "").strip() and site_location.get("customer"):
        updated["customer"] = site_location["customer"]
    return updated
