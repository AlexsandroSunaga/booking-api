import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# legacy entry: app.main:app (repo root); backend entry: src.main:backend_app (backend/)
for p in (ROOT, ROOT / "backend"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
