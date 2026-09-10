from __future__ import annotations

from optisweep_ingestion.stage5_runbook_candidates import _role_from_title


def test_role_from_title_assigns_fortna_for_db_and_remote_surfaces() -> None:
    assert _role_from_title("Query Active AGV Errors From The WCS Database") == "L2_support"
    assert _role_from_title("Inspect Robotics state in SSMS") == "L2_support"
    assert _role_from_title("Check Windows Event Viewer for service faults") == "L1_support"
    assert _role_from_title("Release physical E-stop") == "operator"
    assert _role_from_title("Apply RMS soft stop pause") == "L2_support"
    assert _role_from_title("Normal tote scanning at operator station") == "operator"
