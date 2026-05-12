#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Validating JSON manifests..."
python3 - <<PY
from pathlib import Path
import json

root = Path("$ARTICLE_DIR")
json_files = list(root.glob("config/*.json")) + list(root.glob("tinyml/*.json")) + list(root.glob("pynq/*.json"))

if not json_files:
    print("No JSON manifests found.")
else:
    for path in json_files:
        with path.open("r", encoding="utf-8") as handle:
            json.load(handle)
        print(f"Valid JSON: {path.relative_to(root)}")
PY

echo "Manifest validation complete."
