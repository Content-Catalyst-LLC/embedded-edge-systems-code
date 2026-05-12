#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - <<PY
from pathlib import Path
import json
import yaml

root = Path("$ARTICLE_DIR")

json_files = list(root.glob("config/*.json")) + list(root.glob("tinyml/*.json")) + list(root.glob("pynq/*.json")) + list(root.glob("hardware/*.json"))
yaml_files = list(root.glob("config/*.yml")) + list(root.glob("config/*.yaml")) + list(root.glob("digital_twin/*.yml")) + list(root.glob("hil/*.yml"))

for path in json_files:
    json.loads(path.read_text(encoding="utf-8"))
    print(f"Valid JSON: {path.relative_to(root)}")

for path in yaml_files:
    yaml.safe_load(path.read_text(encoding="utf-8"))
    print(f"Valid YAML: {path.relative_to(root)}")
PY

echo "Manifest validation complete."
