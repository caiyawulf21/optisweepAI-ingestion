from pathlib import Path

import pytest

from optisweep_incidence_ingestion.services.site_location import (
    apply_ingestion_site_to_canonical_record,
    resolve_site_location,
    site_location_label,
    site_ref_fields,
)
from optisweep_incidence_ingestion.stage1_source_package import build_incident_source_ref


def test_resolve_known_site_code_defaults_to_haslet():
    site = resolve_site_location(site_code="ups_haslet_tx")
    assert site["site_code"] == "ups_haslet_tx"
    assert site["customer"] == "UPS"
    assert site["hub_code"] == "TXRTH"
    assert "Haslet" in site_location_label(site)


def test_resolve_unknown_site_code_raises():
    with pytest.raises(ValueError, match="Unknown site_code"):
        resolve_site_location(site_code="unknown_site")


def test_site_ref_fields_include_code_and_label():
    site = resolve_site_location(site_code="ups_haslet_tx")
    assert site_ref_fields(site) == {
        "site_code": "ups_haslet_tx",
        "site_label": "UPS Haslet TX (TXRTH)",
    }


def test_build_incident_source_ref_carries_site_fields():
    site = resolve_site_location(site_code="ups_haslet_tx")
    ref = build_incident_source_ref(
        source_id="source_case_228086",
        source_title="Case 228086 Data",
        ingestion_batch_id="batch_test",
        case_id="228086",
        page_number=1,
        site_location=site,
    )
    assert ref["site_code"] == "ups_haslet_tx"
    assert ref["site_label"] == "UPS Haslet TX (TXRTH)"


def test_apply_ingestion_site_to_canonical_record(tmp_path: Path):
    site = resolve_site_location(site_code="ups_haslet_tx")
    record = apply_ingestion_site_to_canonical_record(
        {"title": "Test incident", "site": {"primary_label": "", "observed_location_text": []}},
        site_location=site,
    )
    assert record["customer"] == "UPS"
    assert record["site"]["ingestion_site"]["site_code"] == "ups_haslet_tx"
    assert record["site"]["primary_label"] == "UPS Haslet TX (TXRTH)"
    assert "UPS Haslet TX (TXRTH)" in record["site"]["observed_location_text"]
