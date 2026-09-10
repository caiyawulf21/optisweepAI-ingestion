from shared_pipeline_stages.runbook_eligibility import (
    eligibility_errors_for_candidate,
    eligibility_errors_for_runbook,
)


def test_rejects_invented_bag_out_control_system() -> None:
    candidate = {
        "title": "Use Bag Out Control System to close destinations",
        "summary": "Run a Bag Out action in the OptiSweep Bag Out Control system.",
        "candidate_goal": "Close destinations using the Bag Out control system UI shown in the source.",
        "access_or_tools_needed": ["OptiSweep Bag Out Control system"],
        "rough_steps": [
            "Open the Bag Out control system UI/control shown in the source segment.",
            "Select system bag out as described by the source.",
        ],
        "likely_procedure_type": "operation",
    }
    errors = eligibility_errors_for_candidate(candidate)
    assert any("invented" in error or "verified live" in error or "training source" in error for error in errors)


def test_rejects_orientation_walkthrough_with_ocr_language() -> None:
    candidate = {
        "title": "Use the Ignition Walkthrough context to clarify what a referenced manual differs from",
        "summary": "Familiarize support with Ignition Walkthrough 120 orientation context.",
        "candidate_goal": "Clarify slide meaning during walkthrough.",
        "rough_steps": [
            "Find the frame labeled Ignition Walkthrough 120.",
            "Confirm the OCR text reads Ignition Walkthrough 120.",
            "Quote the contrast sentence from the training segment.",
        ],
        "likely_procedure_type": "reference",
    }
    errors = eligibility_errors_for_candidate(candidate)
    assert any("orientation" in error for error in errors)
    assert any("source/OCR" in error or "OCR" in error or "training source" in error for error in errors)


def test_rejects_vague_ask_controls_without_concrete_memory_check() -> None:
    runbook = {
        "title": "Use Ignition log in the web UI",
        "summary": "Review Ignition log and ask controls about memory details per the source.",
        "procedure_type": "diagnostic",
        "access_surface": ["tipper_hmi", "wcs_api"],
        "access_or_tools_needed": ["Ignition web UI"],
        "steps": [
            {
                "title": "Open log",
                "instruction": "Open the Ignition log referenced by the source.",
                "expected_result": "You can view the log.",
            },
            {
                "title": "Ask controls",
                "instruction": "If memory details may be implicated, ask controls about logs and memory details (per the source).",
                "expected_result": "Controls are engaged for interpretation/confirmation.",
            },
        ],
    }
    errors = eligibility_errors_for_runbook(runbook)
    assert any("vague" in error or "concrete" in error or "source/OCR" in error for error in errors)


def test_accepts_hospital_hmi_as_live_surface() -> None:
    candidate = {
        "title": "Verify hospital HMI induct position fields",
        "summary": "Open Hospital HMI and confirm induct/extract position fields populate.",
        "candidate_goal": "Confirm hospital lane HMI fields after induct.",
        "access_or_tools_needed": ["Hospital HMI"],
        "rough_steps": [
            "Open Hospital HMI for the affected lane.",
            "Check induct and extract position fields are populated.",
            "Escalate if fields remain blank after retry.",
        ],
        "likely_procedure_type": "diagnostic",
    }
    assert eligibility_errors_for_candidate(candidate) == []


def test_accepts_concrete_ignition_memory_diagnostic() -> None:
    runbook = {
        "title": "Check Ignition Gateway performance memory for crash spike",
        "summary": "Open Ignition Gateway Systems Overview performance page and inspect memory usage.",
        "procedure_type": "diagnostic",
        "access_surface": ["ignition_gateway"],
        "access_or_tools_needed": ["Ignition Gateway web UI"],
        "steps": [
            {
                "title": "Open performance page",
                "instruction": "In Ignition Gateway, open Status > Performance (sys.performance) in a browser.",
                "expected_result": "The memory usage chart is visible.",
            },
            {
                "title": "Interpret memory spike",
                "instruction": "Check whether memory shows a sudden spike then drop toward zero around the failure time.",
                "expected_result": "A sudden spike then drop to near zero implicates a gateway crash/restart; steady sawtooth implicates garbage collection.",
            },
        ],
    }
    assert eligibility_errors_for_runbook(runbook) == []
