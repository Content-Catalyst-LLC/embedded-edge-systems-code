#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - <<PY
from pathlib import Path
import json

root = Path("$ARTICLE_DIR")
json_files = list(root.glob("config/*.json")) + list(root.glob("tinyml/*.json")) + list(root.glob("pynq/*.json"))

for path in json_files:
    json.loads(path.read_text(encoding="utf-8"))
    print(f"Valid JSON: {path.relative_to(root)}")
PY

echo "Manifest validation complete."
