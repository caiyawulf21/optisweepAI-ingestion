import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
SRC = ROOT / "src"

if str(REPO_ROOT) not in sys.path:
    # Needed to import brain_service/providers, used by this pipeline's
    # stage hooks (BRAIN_INGESTION_ENABLED-gated Brain ingestion).
    sys.path.insert(0, str(REPO_ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
