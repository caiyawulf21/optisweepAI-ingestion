from shared_pipeline_stages.stage_11.gate_phrase_table import (
    GATE_PHRASE_DOC_ID,
    GATE_PHRASE_DOC_TYPE,
    build_gate_phrase_table,
    match_query_against_gate_table,
    smoke_gate_phrase_table,
)


def test_gate_phrase_table_smoke_hits_required_keys() -> None:
    table = build_gate_phrase_table(
        publish_version_id="publish_test",
        playbooks=[
            {
                "case_id": "228086",
                "support_user_language_examples": [
                    "AGVs aren't moving",
                    "rms showing no alarms",
                ],
                "observed_entry_symptoms": ["Nothing is moving"],
            }
        ],
    )
    assert table["id"] == GATE_PHRASE_DOC_ID
    assert table["doc_type"] == GATE_PHRASE_DOC_TYPE
    smoke = smoke_gate_phrase_table(table)
    assert smoke["passed"] is True
    assert "agvs_stopped" in smoke["hits"]
    assert "no_rms_alarm" in smoke["hits"]


def test_gate_phrase_table_merges_prior_and_new_phrases() -> None:
    prior = build_gate_phrase_table(
        publish_version_id="publish_old",
        playbooks=[],
    )
    prior["legacy_signal_phrases"]["agvs_stopped"].append("fleet frozen")
    table = build_gate_phrase_table(
        publish_version_id="publish_new",
        playbooks=[
            {
                "support_user_language_examples": ["zone unable to get a pair"],
            }
        ],
        prior_table=prior,
    )
    assert "fleet frozen" in table["legacy_signal_phrases"]["agvs_stopped"]
    assert "zone unable to get a pair" in table["legacy_signal_phrases"]["pairing_failure"]
    hits = match_query_against_gate_table("zone unable to get a pair", table)
    assert "pairing_failure" in hits
