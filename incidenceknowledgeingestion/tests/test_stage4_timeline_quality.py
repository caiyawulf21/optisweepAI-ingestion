from optisweep_incidence_ingestion.stage4_canonical_incident_record import (
    _artifacts_by_page_ref,
    _build_page_text_chunks,
    _format_artifact_evidence_for_page,
    build_stage4_evidence_handoff,
    check_timeline_chronology,
    deduplicate_timeline_events,
    filter_timeline_events,
    sort_timeline_events,
)


def _sample_event(
    *,
    event_id: str,
    event_type: str = "diagnostic_evidence_shared",
    summary: str,
    page_number: int = 1,
    within_page_order: int = 1,
    timestamp: str | None = None,
    timestamp_status: str = "missing",
    artifact_refs: list[str] | None = None,
    actor_name: str = "unknown",
) -> dict:
    return {
        "event_id": event_id,
        "event_order": 1,
        "timestamp": timestamp,
        "timestamp_status": timestamp_status,
        "source_order": {"page_number": page_number, "within_page_order": within_page_order},
        "event_type": event_type,
        "actor_name": actor_name,
        "actor_role": "unknown",
        "summary": summary,
        "details": "",
        "systems": [],
        "source_refs": [{"page_ref": f"case_228086:page_{page_number}"}],
        "artifact_refs": artifact_refs or [],
        "evidence_chunk_refs": [],
        "evidence_support_type": [],
        "confidence": "medium",
        "uncertainties": [],
    }


def test_filter_timeline_events_preserves_actor_name():
    events = [
        _sample_event(
            event_id="incident_228086_event_001",
            event_type="symptom_reported",
            summary="Site reported bots not moving.",
            actor_name="Kevin Buczek",
        )
    ]
    filtered = filter_timeline_events(events)
    assert filtered[0]["actor_name"] == "Kevin Buczek"


def test_filter_timeline_events_drops_support_coordination():
    events = [
        _sample_event(
            event_id="incident_228086_event_001",
            event_type="support_coordination",
            summary="Please add me to the call.",
        )
    ]
    assert filter_timeline_events(events) == []


def test_deduplicate_timeline_events_merges_duplicate_group_rms_evidence():
    left = _sample_event(
        event_id="incident_228086_event_004",
        summary="RMS screen evidence showed an abnormal blank state with a message indicating '.NET Control not created.'",
        page_number=3,
        artifact_refs=["artifact_incident_228086_page_003_embedded_image_01"],
    )
    left["systems"] = ["RMS", "ACB System 1"]
    right = _sample_event(
        event_id="incident_228086_event_005",
        summary="RMS screenshot showed '.NET Control not created.' on a mostly blank status page.",
        page_number=5,
        artifact_refs=["artifact_incident_228086_page_005_embedded_image_01"],
    )
    right["systems"] = ["RMS", "ACB System 1"]
    deduped, removed = deduplicate_timeline_events([left, right])
    assert removed == 1
    assert len(deduped) == 1


def test_deduplicate_timeline_events_merges_near_duplicate_artifact_evidence():
    left = _sample_event(
        event_id="incident_228086_event_004",
        summary="RMS screen showed '.NET Control not created.' on a blank status page.",
        page_number=3,
        artifact_refs=["artifact_incident_228086_page_003_embedded_image_01"],
    )
    right = _sample_event(
        event_id="incident_228086_event_005",
        summary="RMS screenshot showed '.NET Control not created.' on a mostly blank status page.",
        page_number=5,
        artifact_refs=["artifact_incident_228086_page_005_embedded_image_01"],
    )
    deduped, removed = deduplicate_timeline_events([left, right])
    assert removed == 1
    assert len(deduped) == 1
    assert "artifact_incident_228086_page_003_embedded_image_01" in deduped[0]["artifact_refs"]
    assert "artifact_incident_228086_page_005_embedded_image_01" in deduped[0]["artifact_refs"]


def test_sort_timeline_events_orders_by_page_then_timestamp():
    events = [
        _sample_event(
            event_id="incident_228086_event_010",
            summary="Later page event.",
            page_number=10,
            within_page_order=1,
            timestamp="2026-02-20T09:50:00",
            timestamp_status="visible",
        ),
        _sample_event(
            event_id="incident_228086_event_007",
            summary="Earlier page event.",
            page_number=7,
            within_page_order=1,
            timestamp="2026-02-20T09:03:00",
            timestamp_status="visible",
        ),
    ]
    sorted_events = sort_timeline_events(events)
    assert [event["event_id"] for event in sorted_events] == [
        "incident_228086_event_007",
        "incident_228086_event_010",
    ]


def test_check_timeline_chronology_flags_out_of_order_visible_timestamps():
    events = [
        _sample_event(
            event_id="incident_228086_event_010",
            summary="Morning update.",
            page_number=7,
            timestamp="2026-02-20T09:24:00",
            timestamp_status="visible",
        ),
        _sample_event(
            event_id="incident_228086_event_011",
            summary="Earlier-looking timestamp likely from OCR noise.",
            page_number=7,
            within_page_order=2,
            timestamp="2026-02-20T05:24:00",
            timestamp_status="visible",
        ),
    ]
    warnings = check_timeline_chronology(sort_timeline_events(events))
    assert any("event_011" in warning for warning in warnings)


def test_build_page_text_chunks_injects_artifact_evidence_when_ocr_omitted():
    pages = [
        {
            "page_number": 3,
            "page_ref": "case_228086:page_3",
            "detected_page_type": "hmi_screenshot",
            "ocr_confidence": 28.39,
            "ocr_quality": "garbled",
            "ocr_word_count": 641,
            "artifact_ids": ["artifact_incident_228086_page_003_embedded_image_01"],
            "ocr_text": "",
            "ocr_note": "OCR text omitted from Stage 4 evidence chunks because quality is garbled.",
        }
    ]
    artifact_cards = [
        {
            "artifact_id": "artifact_incident_228086_page_003_embedded_image_01",
            "page_number": 3,
            "page_ref": "case_228086:page_3",
            "evidence_role": "diagnostic_evidence",
            "image_type": "hmi_screenshot",
            "short_description": "RMS page showing NET Control not created.",
            "retrieval_text": "RMS screenshot with NET Control not created message.",
            "source_supported_claims": [
                {"claim": "Screen shows NET Control not created.", "support_type": "visual_image", "source_refs": []}
            ],
        }
    ]
    chunks = _build_page_text_chunks(pages, 7000, artifacts_by_page_ref=_artifacts_by_page_ref(artifact_cards))
    assert "ARTIFACT artifact_incident_228086_page_003_embedded_image_01" in chunks[0]["text"]
    assert "NET Control not created" in chunks[0]["text"]


def test_build_stage4_evidence_handoff_tracks_pages_with_omitted_ocr():
    pages = [
        {
            "page_number": 1,
            "page_ref": "case_228086:page_1",
            "detected_page_type": "teams_chat_screenshot",
            "ocr_confidence": 90,
            "ocr_quality": "high",
            "ocr_word_count": 100,
            "artifact_ids": [],
            "ocr_text": "Teams chat with visible timestamps.",
            "ocr_note": "",
            "source_refs": [],
        },
        {
            "page_number": 3,
            "page_ref": "case_228086:page_3",
            "detected_page_type": "hmi_screenshot",
            "ocr_confidence": 20,
            "ocr_quality": "garbled",
            "ocr_word_count": 641,
            "artifact_ids": ["artifact_incident_228086_page_003_embedded_image_01"],
            "ocr_text": "",
            "ocr_note": "OCR text omitted from Stage 4 evidence chunks because quality is garbled.",
            "source_refs": [],
        },
    ]
    artifact_cards = [
        {
            "artifact_id": "artifact_incident_228086_page_003_embedded_image_01",
            "page_number": 3,
            "page_ref": "case_228086:page_3",
            "evidence_role": "diagnostic_evidence",
            "image_type": "hmi_screenshot",
            "short_description": "RMS screenshot.",
            "retrieval_text": "RMS screenshot.",
            "source_supported_claims": [],
            "state_assessment": {},
            "supports": {},
            "candidate_support_hints": {},
            "review_uncertainty": [],
            "quality_notes": [],
            "source_refs": [],
        }
    ]
    handoff = build_stage4_evidence_handoff(
        pages=pages,
        artifact_cards=artifact_cards,
        page_chunk_target_chars=7000,
        artifact_chunk_size=8,
    )
    assert handoff["pages_with_omitted_ocr"] == ["case_228086:page_3"]


def test_format_artifact_evidence_for_page_includes_claims():
    text = _format_artifact_evidence_for_page(
        [
            {
                "artifact_id": "artifact_incident_228086_page_003_embedded_image_01",
                "evidence_role": "diagnostic_evidence",
                "image_type": "hmi_screenshot",
                "short_description": "RMS screenshot.",
                "retrieval_text": "RMS screenshot with NET Control not created.",
                "source_supported_claims": [{"claim": "Screen shows NET Control not created.", "support_type": "visual_image"}],
            }
        ]
    )
    assert "artifact_incident_228086_page_003_embedded_image_01" in text
    assert "NET Control not created" in text
