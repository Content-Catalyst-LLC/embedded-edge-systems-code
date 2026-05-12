#!/usr/bin/env bash
set -euo pipefail

test -f companion_manifest.yml
test -f config/reliability_policy.yml
test -f config/fault_model.json
python3 -m json.tool config/fault_model.json >/dev/null
python3 -m json.tool pynq/overlay_manifest.json >/dev/null

echo "Manifest validation passed."
