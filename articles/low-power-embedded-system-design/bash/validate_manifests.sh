#!/usr/bin/env bash
set -euo pipefail

test -f companion_manifest.yml
test -f config/power_policy.yml
test -f config/power_manifest.json
python3 -m json.tool config/power_manifest.json >/dev/null
python3 -m json.tool pynq/overlay_manifest.json >/dev/null

echo "Manifest validation passed."
