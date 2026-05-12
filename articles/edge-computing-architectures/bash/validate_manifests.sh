#!/usr/bin/env bash
set -euo pipefail
ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 - <<PY
from pathlib import Path
import json, yaml
root = Path("$ARTICLE_DIR")
for path in list(root.glob("config/*.json")) + list(root.glob("tinyml/*.json")) + list(root.glob("pynq/*.json")):
    json.loads(path.read_text())
    print(f"Valid JSON: {path.relative_to(root)}")
for path in list(root.glob("config/*.yml")) + list(root.glob("runtime_assurance/*.yml")) + list(root.glob("security/*.yml")):
    yaml.safe_load(path.read_text())
    print(f"Valid YAML: {path.relative_to(root)}")
PY
echo "Manifest validation complete."
