import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# the API lives in backend/ (src.main:backend_app)
for p in (ROOT / "backend",):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
