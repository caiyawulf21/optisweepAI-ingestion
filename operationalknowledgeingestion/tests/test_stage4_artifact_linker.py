from operationalknowledgeingestion.src.optisweep_ingestion.tools.artifact_linker import (
    IMAGE_NOTE_MARKER,
    collect_candidate_artifact_ids,
    enrich_context_record,
    enrich_runbook_candidate,
    find_matching_artifact_ids,
)


def _artifacts() -> list[dict]:
    return [
        {
            "artifact_id": "artifact_fig_3_1_operator_station",
            "figure_id": "fig_3_1",
            "page_number": 24,
            "image_type": "photo",
            "short_description": "Operator station with panels removed for clarity.",
            "retrieval_text": "Figure 3-1 operator station overview with stacklights and HMI.",
            "tags": ["operator_station", "stacklight"],
        },
        {
            "artifact_id": "artifact_page_83_image_10",
            "page_number": 83,
            "image_type": "operator_station_screen",
            "short_description": "Visu_Dual_MCP jogging screen with axis controls.",
            "retrieval_text": "Navigate to the Visu_Dual_MCP screen and press JOG to open axis controls.",
            "tags": ["visu_dual_mcp", "jog"],
        },
    ]


def test_find_matching_artifact_ids_by_figure_and_screen_name() -> None:
    record = {
        "title": "Lock Out And Tag Out From Visu_Dual_MCP",
        "summary": "Navigate to the Visu_Dual_MCP screen and press CYCLE STOP.",
        "source_refs": [
            {"page": 18, "figure_id": "fig_3_1", "figure_number": "Figure 3-1"},
        ],
    }

    matched = find_matching_artifact_ids(record, _artifacts(), max_results=4)

    assert "artifact_fig_3_1_operator_station" in matched
    assert "artifact_page_83_image_10" in matched


def test_enrich_context_record_backfills_image_refs() -> None:
    context = {
        "context_id": "ctx_visu_dual_mcp_screen_reference_v1",
        "context_type": "hmi_screen_reference",
        "title": "Visu_Dual_MCP HMI screen reference",
        "summary": "Navigate to the Visu_Dual_MCP screen on the operator station HMI.",
        "details": "The operator station HMI includes a screen named Visu_Dual_MCP.",
        "key_terms": ["Visu_Dual_MCP", "operator station HMI"],
        "related_artifact_ids": [],
        "image_refs": [],
        "source_refs": [{"page": 18}],
    }

    enriched, notes = enrich_context_record(context, _artifacts())

    assert enriched["related_artifact_ids"]
    assert enriched["image_refs"] == enriched["related_artifact_ids"]
    assert notes


def test_enrich_runbook_candidate_links_artifacts_and_image_notes() -> None:
    candidate = {
        "candidate_id": "candidate_l2_operator_station_lockout_tagout_from_visu_dual_mcp",
        "title": "Lock Out And Tag Out From Visu_Dual_MCP",
        "summary": "Navigate to the Visu_Dual_MCP screen and press CYCLE STOP.",
        "rough_steps": [
            'At the operator station HMI, navigate to the "Visu_Dual_MCP" screen.',
            "Press CYCLE STOP.",
        ],
        "related_context_ids": ["ctx_visu_dual_mcp_screen_reference_v1"],
        "related_artifact_ids": [],
        "source_refs": [{"page": 18}],
    }
    contexts = [
        {
            "context_id": "ctx_visu_dual_mcp_screen_reference_v1",
            "title": "Visu_Dual_MCP HMI screen reference",
            "summary": "Navigate to the Visu_Dual_MCP screen.",
            "related_artifact_ids": [],
            "image_refs": [],
            "source_refs": [{"page": 18}],
        }
    ]

    enriched, notes = enrich_runbook_candidate(candidate, _artifacts(), {contexts[0]["context_id"]: contexts[0]})

    assert enriched["related_artifact_ids"]
    assert any(IMAGE_NOTE_MARKER in step for step in enriched["rough_steps"])
    assert notes


def test_collect_candidate_artifact_ids_uses_context_image_refs() -> None:
    candidate = {
        "candidate_id": "candidate_manual_start_operator_station",
        "title": "Start Operator Station",
        "summary": "Use the operator station control panel.",
        "related_artifact_ids": [],
        "related_context_ids": ["ctx_operator_station_overview_v1"],
        "source_refs": [{"page": 24}],
    }
    contexts = {
        "ctx_operator_station_overview_v1": {
            "context_id": "ctx_operator_station_overview_v1",
            "image_refs": ["artifact_fig_3_1_operator_station"],
            "related_artifact_ids": ["artifact_fig_3_1_operator_station"],
        }
    }

    artifact_ids = collect_candidate_artifact_ids(candidate, _artifacts(), contexts)

    assert "artifact_fig_3_1_operator_station" in artifact_ids


def test_prefer_same_section_over_nearby_qa_slide() -> None:
    artifacts = [
        {
            "artifact_id": "artifact_training_ignition_log_ui",
            "section_id": "training_segment_0012",
            "page_number": 12,
            "image_type": "training_video_frame",
            "title": "Ignition web UI log viewer",
            "nearby_text": "Open Ignition and review the gateway log for faults.",
            "retrieval_text": "Ignition web UI log viewer gateway faults",
            "tags": ["ignition", "log"],
        },
        {
            "artifact_id": "artifact_training_qa_lunch",
            "section_id": "training_segment_0040",
            "page_number": 40,
            "image_type": "training_video_frame",
            "title": "Questions Comments Concerns Lunch",
            "nearby_text": "Any questions? Lunch break agenda.",
            "retrieval_text": "Questions comments concerns lunch break",
            "tags": ["questions", "lunch"],
        },
        {
            "artifact_id": "artifact_training_db_nearby",
            "section_id": "training_segment_0013",
            "page_number": 13,
            "image_type": "training_video_frame",
            "title": "SSMS Helix Robotics module",
            "nearby_text": "SSMS Helix Robotics database module tables",
            "retrieval_text": "SSMS Helix Robotics database module",
            "tags": ["ssms", "robotics"],
        },
    ]
    candidate = {
        "candidate_id": "candidate_training_video_check_ignition_log_in_web_ui",
        "title": "Check Ignition Log In Web UI",
        "summary": "Open Ignition web UI and review the gateway log.",
        "rough_steps": ["Open Ignition", "Review the gateway log"],
        "related_artifact_ids": [],
        "source_refs": [{"page": 12, "section_id": "training_segment_0012"}],
    }

    matched = collect_candidate_artifact_ids(candidate, artifacts, max_results=3)

    assert matched[0] == "artifact_training_ignition_log_ui"
    assert "artifact_training_qa_lunch" not in matched


def test_training_linker_excludes_qa_and_unrelated_database_frames() -> None:
    artifacts = [
        {
            "artifact_id": "artifact_robot_command_database_model",
            "section_id": "training_segment_0014",
            "page_number": 14,
            "image_type": "training_video_frame",
            "title": "Robot Command Database Model",
            "short_description": "RobotCommandDatabaseModel active command status sent in progress",
            "retrieval_text": "Robot Command Database Model EmptyGoTo PickupTote command status",
            "ocr_text": "Robot Command Database Model",
            "tags": ["robot_command", "database"],
        },
        {
            "artifact_id": "artifact_agv_active_error_database",
            "section_id": "training_segment_0015",
            "page_number": 15,
            "image_type": "training_video_frame",
            "title": "AgvActiveErrorDatabaseModel",
            "short_description": "AGV active error database model ErrorCode SortGuid",
            "retrieval_text": "AgvActiveErrorDatabaseModel active errors archived activity",
            "ocr_text": "Agv Active Error Database Model",
            "tags": ["agv", "error", "database"],
        },
        {
            "artifact_id": "artifact_entity_logs_overview",
            "section_id": "training_segment_0008",
            "page_number": 8,
            "image_type": "training_video_frame",
            "title": "EntityLogs WCS databases",
            "short_description": "WCS created databases OptiSweep utilizes entity logs",
            "retrieval_text": "database model table entity logs overview",
            "ocr_text": "EntityLogs",
            "tags": ["database", "entitylogs"],
        },
        {
            "artifact_id": "artifact_questions_comments_lunch",
            "section_id": "training_segment_0055",
            "page_number": 55,
            "image_type": "training_video_frame",
            "title": "Questions Comments Concerns Lunch",
            "nearby_text": "check database heartbeats restart OptiSweep RMS",
            "retrieval_text": "questions comments concerns lunch restart database heartbeats",
            "tags": ["questions", "lunch"],
        },
    ]
    candidate = {
        "candidate_id": "candidate_training_video_robot_command_database_check_active_command_status",
        "title": "Check Robot Command Database model table for active robot command status",
        "summary": "Use RobotCommandDatabaseModel to determine whether a robot command is active.",
        "rough_steps": [
            "Open RobotCommandDatabaseModel",
            "Check sent versus in-progress timing fields",
        ],
        "related_artifact_ids": [],
        "related_context_ids": ["ctx_robot_command"],
        "source_refs": [{"page": 14, "section_id": "training_segment_0014"}],
    }
    contexts = {
        "ctx_robot_command": {
            "context_id": "ctx_robot_command",
            "related_artifact_ids": [
                "artifact_robot_command_database_model",
                "artifact_agv_active_error_database",
                "artifact_entity_logs_overview",
                "artifact_questions_comments_lunch",
            ],
            "image_refs": [
                "artifact_robot_command_database_model",
                "artifact_agv_active_error_database",
                "artifact_entity_logs_overview",
            ],
        }
    }

    matched = collect_candidate_artifact_ids(candidate, artifacts, contexts, max_results=4)

    assert matched[0] == "artifact_robot_command_database_model"
    assert "artifact_questions_comments_lunch" not in matched
    assert "artifact_entity_logs_overview" not in matched
    assert "artifact_agv_active_error_database" not in matched