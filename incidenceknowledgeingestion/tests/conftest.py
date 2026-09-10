import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
SRC = ROOT / "src"
OPERATIONAL_SRC = REPO_ROOT / "operationalknowledgeingestion" / "src"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(OPERATIONAL_SRC) not in sys.path:
    # stage6_runbook_finalization.py imports from optisweep_ingestion
    # (the operational pipeline's package), same as
    # extract_incident_knowledge.py's own sys.path setup already does for
    # the CLI -- this conftest previously omitted it, so any test file
    # that imports stage6_runbook_finalization directly (not through the
    # CLI) failed with ModuleNotFoundError: No module named
    # 'optisweep_ingestion', pre-existing and unrelated to any one test.
    sys.path.insert(0, str(OPERATIONAL_SRC))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
